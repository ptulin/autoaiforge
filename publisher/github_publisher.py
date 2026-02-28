"""
GitHub Publisher — saves all passing tools to the local generated_tools/ folder.

Strategy (revised):
  - The GitHub Actions GITHUB_TOKEN is scoped only to the current repo.
  - Calling /user endpoint with a fine-grained token returns 403.
  - Instead, we write tool files locally under generated_tools/{date}/{name}/
  - _save_db_to_git() in main.py then commits the whole generated_tools/ folder.
  - URLs point to the files in the main autoaiforge repo (always accessible).
  - If a PAT with cross-repo access is ever added, a separate tools-repo
    publisher can be layered in later.
"""

import json
import os
from pathlib import Path
from typing import Optional

from utils.logger import get_logger
from developer.tool_builder import BuiltTool
import config

log = get_logger("github_publisher")


class GitHubPublisher:
    def __init__(self):
        self._ready    = True
        self._username = (
            os.getenv("GITHUB_REPOSITORY_OWNER")
            or config.GITHUB_USERNAME
            or "ptulin"
        )
        log.info(f"Publisher ready — will commit tools to repo as: {self._username}")

    # ── Public API ─────────────────────────────────────────────────────────────

    def publish_tools(self, tools: list["BuiltTool"]) -> list[str]:
        """
        Write all tools to generated_tools/{date}/{name}/ on disk.
        Returns list of GitHub URLs for the committed tool folders.
        (Actual git commit is done by _save_db_to_git() in main.py.)
        """
        if not tools:
            return []

        run_date = config.RUN_DATE
        urls     = []

        for tool in tools:
            try:
                url = self._save_tool(tool, run_date)
                if url:
                    urls.append(url)
                    log.info(f"Saved {tool.tool_name} → {url}")
            except Exception as e:
                log.error(f"Failed to save {tool.tool_name}: {e}")

        log.info(f"Saved {len(urls)}/{len(tools)} tools to generated_tools/")
        return urls

    # ── Internal ───────────────────────────────────────────────────────────────

    def _save_tool(self, tool: "BuiltTool", run_date: str) -> Optional[str]:
        """Write a tool's files to the generated_tools directory."""
        tool_dir = config.TOOLS_DIR / run_date / tool.tool_name
        tool_dir.mkdir(parents=True, exist_ok=True)

        # Write all files
        (tool_dir / f"{tool.tool_name}.py").write_text(tool.code, encoding="utf-8")
        (tool_dir / f"test_{tool.tool_name}.py").write_text(tool.test_code, encoding="utf-8")
        (tool_dir / "requirements.txt").write_text(
            "\n".join(tool.requirements) + "\n", encoding="utf-8"
        )
        (tool_dir / "README.md").write_text(tool.readme, encoding="utf-8")
        # GitHub URL in the main autoaiforge repo
        repo_name = os.getenv("GITHUB_REPOSITORY", f"{self._username}/autoaiforge").split("/")[-1]
        github_url = (
            f"https://github.com/{self._username}/{repo_name}"
            f"/tree/main/generated_tools/{run_date}/{tool.tool_name}"
        )
        readme_url = (
            f"https://raw.githubusercontent.com/{self._username}/{repo_name}"
            f"/main/generated_tools/{run_date}/{tool.tool_name}/README.md"
        )

        (tool_dir / "metadata.json").write_text(
            json.dumps({
                "tool_name":    tool.tool_name,
                "display_name": tool.display_name,
                "description":  tool.description,
                "topic":        tool.topic,
                "date":         run_date,
                "generated":    config.RUN_TS,
                "loops_needed": tool.loops_needed,
                "tests_passed": tool.test_result.passed,
                "github_url":   github_url,
                "readme_url":   readme_url,
            }, indent=2),
            encoding="utf-8",
        )

        return github_url
