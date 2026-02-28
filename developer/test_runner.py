"""
Test Runner — executes pytest in a sandboxed subprocess.

Security note: Generated code runs in a subprocess with a timeout.
GitHub Actions provides process-level isolation.
"""

import os
import subprocess
import sys
import shutil
import venv
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from utils.logger import get_logger
import config

log = get_logger("test_runner")


@dataclass
class TestResult:
    passed:        bool
    returncode:    int
    stdout:        str
    stderr:        str
    error_summary: str   # Compact error digest for the fix prompt


class TestRunner:
    """
    Creates a minimal virtual environment per tool (or reuses a shared one),
    installs requirements, runs pytest, and returns the result.
    """

    # Shared venv to avoid reinstalling common packages every loop
    _SHARED_VENV = config.SANDBOX_DIR / "_venv"
    _VENV_PYTHON: Optional[str] = None

    def __init__(self):
        self._ensure_venv()

    # ── Public API ─────────────────────────────────────────────────────────────

    def run(
        self,
        tool_dir: Path,
        tool_name: str,
        requirements: list[str],
    ) -> TestResult:
        """Install requirements and run pytest for the given tool directory."""
        test_file = tool_dir / f"test_{tool_name}.py"
        if not test_file.exists():
            return TestResult(
                passed=False,
                returncode=1,
                stdout="",
                stderr="",
                error_summary=f"Test file {test_file} not found",
            )

        # Install requirements into shared venv
        if requirements:
            self._install(requirements, tool_dir)

        # Run pytest
        env = {**os.environ, "PYTHONPATH": str(tool_dir)}
        cmd = [
            self._VENV_PYTHON, "-m", "pytest",
            str(test_file),
            "-v", "--tb=short", "--no-header",
            f"--timeout={config.TEST_TIMEOUT_SECONDS}",
        ]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=config.TEST_TIMEOUT_SECONDS + 10,
                cwd=str(tool_dir),
                env=env,
            )
            stdout = proc.stdout
            stderr = proc.stderr
            passed = proc.returncode == 0
            error_summary = self._summarise_errors(stdout, stderr, proc.returncode)

            if passed:
                log.info(f"Tests PASSED for {tool_name}")
            else:
                log.warning(f"Tests FAILED for {tool_name}:\n{error_summary}")

            return TestResult(
                passed=passed,
                returncode=proc.returncode,
                stdout=stdout,
                stderr=stderr,
                error_summary=error_summary,
            )

        except subprocess.TimeoutExpired:
            msg = f"Tests timed out after {config.TEST_TIMEOUT_SECONDS}s"
            log.error(msg)
            return TestResult(passed=False, returncode=124,
                              stdout="", stderr=msg, error_summary=msg)
        except Exception as e:
            msg = f"Test runner exception: {e}"
            log.error(msg)
            return TestResult(passed=False, returncode=1,
                              stdout="", stderr=str(e), error_summary=msg)

    # ── Internal ───────────────────────────────────────────────────────────────

    def _ensure_venv(self):
        """Create shared venv if it doesn't exist; locate python binary."""
        venv_dir = self.__class__._SHARED_VENV

        if not venv_dir.exists():
            log.info(f"Creating shared test venv at {venv_dir} …")
            venv.create(str(venv_dir), with_pip=True)
            # Upgrade pip silently
            python = self._venv_python(venv_dir)
            subprocess.run(
                [python, "-m", "pip", "install", "--quiet", "--upgrade", "pip",
                 "pytest", "pytest-timeout", "pytest-mock"],
                capture_output=True,
            )

        self.__class__._VENV_PYTHON = self._venv_python(venv_dir)
        log.debug(f"Test venv python: {self._VENV_PYTHON}")

    @staticmethod
    def _venv_python(venv_dir: Path) -> str:
        """Return path to python binary inside a venv."""
        if sys.platform == "win32":
            return str(venv_dir / "Scripts" / "python.exe")
        return str(venv_dir / "bin" / "python")

    def _install(self, requirements: list[str], tool_dir: Path):
        """Install requirements.txt into the shared venv."""
        req_file = tool_dir / "requirements.txt"
        if not req_file.exists() or not requirements:
            return

        # Filter out packages that shouldn't be installed in CI
        safe_pkgs = [
            r for r in requirements
            if not any(bad in r.lower() for bad in ["git+", "svn+", "http://", "https://"])
        ]
        if not safe_pkgs:
            return

        log.debug(f"Installing: {safe_pkgs}")
        proc = subprocess.run(
            [self._VENV_PYTHON, "-m", "pip", "install", "--quiet"] + safe_pkgs,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if proc.returncode != 0:
            log.warning(f"pip install warning: {proc.stderr[:300]}")

    @staticmethod
    def _summarise_errors(stdout: str, stderr: str, returncode: int) -> str:
        """Extract the most relevant error lines for the fix prompt."""
        combined = stdout + "\n" + stderr
        lines    = combined.splitlines()

        # Extract FAILED, ERROR, AssertionError, Exception lines
        important = [
            line for line in lines
            if any(kw in line for kw in
                   ["FAILED", "ERROR", "Error", "Exception", "assert",
                    "ImportError", "ModuleNotFoundError", "SyntaxError",
                    "TypeError", "AttributeError", "NameError"])
        ]

        if important:
            return "\n".join(important[:40])

        # Fallback: last 30 lines
        tail = lines[-30:] if len(lines) > 30 else lines
        return "\n".join(tail)
