"""
Tool Builder — generates working Python tools from idea specs.

Algorithm:
  1. Build detailed code-generation prompt from the idea spec
  2. Ask LLM to generate: tool code, test code, requirements, README
  3. Write to sandbox directory
  4. Run test_runner → if fails, feed error back to LLM (up to MAX_CORRECTION_LOOPS)
  5. Return BuiltTool if all tests pass, None if all attempts fail
"""

import json
import os
import shutil
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from utils.logger import get_logger
from utils import llm_client
from developer.test_runner import TestRunner, TestResult
import config

log = get_logger("tool_builder")


# ─── Data classes ─────────────────────────────────────────────────────────────

@dataclass
class BuiltTool:
    tool_name:    str
    display_name: str
    description:  str
    topic:        str
    tool_path:    Path          # Directory containing all files
    code:         str
    test_code:    str
    requirements: list[str]
    readme:       str
    test_result:  TestResult
    loops_needed: int


# ─── Prompts ──────────────────────────────────────────────────────────────────

_BUILD_SYSTEM = """\
You are an expert Python developer. You write clean, working, well-documented
Python tools. Your code MUST:
- Run correctly with no unhandled exceptions
- Include proper CLI argument parsing (use argparse, not sys.argv directly)
- Handle edge cases (empty input, network errors, missing files, etc.)
- Use only the specified packages from tech_stack plus Python stdlib
- Have a working __main__ guard
- NOT use hardcoded file paths or personal API keys
- Be self-contained in a single .py file

The test code MUST:
- Use pytest
- Test the main functions directly (not just CLI)
- Include at least 3 meaningful test cases
- Mock external network calls (use unittest.mock)
- All tests must pass without network access
"""

_BUILD_PROMPT = """\
Build a complete Python tool based on this specification:

TOOL NAME: {tool_name}
DISPLAY NAME: {display_name}
DESCRIPTION: {description}
TYPE: {tool_type}
KEY FEATURES: {features}
TECH STACK (use ONLY these + stdlib): {tech_stack}
INPUT: {input_spec}
OUTPUT: {output_spec}
EXAMPLE USAGE: {example_usage}

Return ONLY a JSON object with exactly these keys:
{{
  "code": "complete Python source code for the tool (string, newlines as \\n)",
  "test_code": "complete pytest test file (string, newlines as \\n)",
  "requirements": ["package1==version", "package2"],
  "readme": "markdown README content (string)"
}}

Requirements:
- The tool file should be named {tool_name}.py
- The test file should be named test_{tool_name}.py
- Requirements must include exact versions where possible
- README must include: description, installation, usage examples, features
- Code must be 50-300 lines
- Test code must have 3+ passing tests (mock all external calls)
"""

_FIX_PROMPT = """\
The following Python tool code has failing tests. Fix ALL failing tests.

TOOL NAME: {tool_name}
ORIGINAL SPEC: {description}

CURRENT TOOL CODE:
```python
{code}
```

CURRENT TEST CODE:
```python
{test_code}
```

TEST ERRORS:
```
{errors}
```

Return ONLY a JSON object with the same structure as before:
{{
  "code": "fixed Python source code",
  "test_code": "fixed pytest test file",
  "requirements": ["package1", "package2"],
  "readme": "markdown README"
}}

Fix the code and/or tests to make ALL tests pass.
Ensure mocks are correct and tests don't depend on network access.
"""


# ─── Main class ───────────────────────────────────────────────────────────────

class ToolBuilder:
    def __init__(self):
        self._runner = TestRunner()

    def build(self, idea: dict) -> Optional[BuiltTool]:
        """
        Build and test a tool from an idea spec.
        Returns BuiltTool if successful, None if all correction loops fail.
        """
        tool_name = idea["tool_name"]
        log.info(f"Building tool: {tool_name} …")

        # Create a clean sandbox directory for this tool
        sandbox = config.SANDBOX_DIR / tool_name
        if sandbox.exists():
            shutil.rmtree(sandbox)
        sandbox.mkdir(parents=True)

        # Initial code generation
        try:
            generated = self._generate_initial(idea)
        except Exception as e:
            log.error(f"Initial generation failed for {tool_name}: {e}")
            return None

        code         = generated.get("code", "")
        test_code    = generated.get("test_code", "")
        requirements = generated.get("requirements", [])
        readme       = generated.get("readme", "")

        if not code or not test_code:
            log.error(f"LLM returned empty code for {tool_name}")
            return None

        # Correction loop
        for loop in range(config.MAX_CORRECTION_LOOPS):
            self._write_files(sandbox, tool_name, code, test_code, requirements)
            result = self._runner.run(sandbox, tool_name, requirements)

            if result.passed:
                log.info(f"✅ {tool_name} passed tests on loop {loop + 1}")
                return BuiltTool(
                    tool_name=tool_name,
                    display_name=idea.get("display_name", tool_name),
                    description=idea.get("description", ""),
                    topic=idea.get("topic", ""),
                    tool_path=sandbox,
                    code=code,
                    test_code=test_code,
                    requirements=requirements,
                    readme=readme or self._default_readme(idea),
                    test_result=result,
                    loops_needed=loop + 1,
                )

            log.warning(
                f"⚠️  {tool_name} tests failed (loop {loop + 1}/{config.MAX_CORRECTION_LOOPS})"
                f" — {result.error_summary[:200]}"
            )

            if loop < config.MAX_CORRECTION_LOOPS - 1:
                try:
                    fixed = self._generate_fix(
                        idea, code, test_code, result.error_summary
                    )
                    code         = fixed.get("code", code)
                    test_code    = fixed.get("test_code", test_code)
                    requirements = fixed.get("requirements", requirements)
                    readme       = fixed.get("readme", readme)
                except Exception as e:
                    log.error(f"Fix generation failed on loop {loop+1}: {e}")

        log.error(f"❌ {tool_name} failed after {config.MAX_CORRECTION_LOOPS} loops")
        # Clean up failed sandbox
        try:
            shutil.rmtree(sandbox)
        except Exception:
            pass
        return None

    def build_all(self, ideas: list[dict]) -> list[BuiltTool]:
        """Build all ideas; collect successful tools."""
        built = []
        for idea in ideas:
            try:
                tool = self.build(idea)
                if tool:
                    built.append(tool)
            except Exception as e:
                log.error(f"Unexpected error building {idea.get('tool_name')}: {e}")
        log.info(f"Built {len(built)}/{len(ideas)} tools successfully")
        return built

    # ── LLM calls ─────────────────────────────────────────────────────────────

    @staticmethod
    def _generate_initial(idea: dict) -> dict:
        prompt = _BUILD_PROMPT.format(
            tool_name=idea["tool_name"],
            display_name=idea.get("display_name", idea["tool_name"]),
            description=idea.get("description", ""),
            tool_type=idea.get("tool_type", "cli_tool"),
            features=", ".join(idea.get("key_features", [])),
            tech_stack=", ".join(idea.get("tech_stack", ["requests"])),
            input_spec=idea.get("input_spec", "command-line arguments"),
            output_spec=idea.get("output_spec", "formatted text"),
            example_usage=idea.get("example_usage", ""),
        )
        return llm_client.chat_json(
            prompt=prompt,
            system=_BUILD_SYSTEM,
            max_tokens=6000,
            temperature=0.3,
        )

    @staticmethod
    def _generate_fix(idea: dict, code: str, test_code: str, errors: str) -> dict:
        prompt = _FIX_PROMPT.format(
            tool_name=idea["tool_name"],
            description=idea.get("description", "")[:300],
            code=code[:4000],
            test_code=test_code[:3000],
            errors=errors[:2000],
        )
        return llm_client.chat_json(
            prompt=prompt,
            system=_BUILD_SYSTEM,
            max_tokens=6000,
            temperature=0.2,
        )

    # ── File helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _write_files(
        sandbox: Path,
        tool_name: str,
        code: str,
        test_code: str,
        requirements: list[str],
    ):
        (sandbox / f"{tool_name}.py").write_text(code, encoding="utf-8")
        (sandbox / f"test_{tool_name}.py").write_text(test_code, encoding="utf-8")
        req_content = "\n".join(requirements) + "\n" if requirements else ""
        (sandbox / "requirements.txt").write_text(req_content, encoding="utf-8")

    @staticmethod
    def _default_readme(idea: dict) -> str:
        return textwrap.dedent(f"""
        # {idea.get('display_name', idea['tool_name'])}

        {idea.get('description', '')}

        ## Topic
        {idea.get('topic', '')}

        ## Installation
        ```bash
        pip install -r requirements.txt
        ```

        ## Usage
        ```bash
        {idea.get('example_usage', f"python {idea['tool_name']}.py --help")}
        ```

        ## Features
        {chr(10).join(f'- {f}' for f in idea.get('key_features', []))}

        ---
        *Auto-generated by AutoAIForge 🤖*
        """).strip()
