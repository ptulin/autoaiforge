"""
GitHub Publisher — commits all passing tools to a public 'autoaiforge-tools' repo.

Strategy:
  - Use PyGitHub to create the repo if it doesn't exist
  - Use the GitHub Contents API to add/update files (no git clone needed)
  - Commit all tool files under tools/YYYY-MM-DD/<tool_name>/
  - Update a root index.md with the day's tools
  - Works in GitHub Actions using the auto-provided GITHUB_TOKEN
"""

import json
import base64
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from utils.logger import get_logger
from developer.tool_builder import BuiltTool
import config

log = get_logger("github_publisher")

try:
    from github import Github, GithubException, InputGitTreeElement
    GH_OK = True
except ImportError:
    GH_OK = False
    log.warning("PyGitHub not installed — publishing disabled")


class GitHubPublisher:
    def __init__(self):
        self._gh    = None
        self._repo  = None
        self._ready = False

        if not GH_OK:
            log.warning("PyGitHub not available")
            return
        if not config.GITHUB_TOKEN:
            log.warning("GITHUB_TOKEN not set — publishing disabled")
            return

        try:
            self._gh   = Github(config.GITHUB_TOKEN)
            user       = self._gh.get_user()
            self._user = user
            log.info(f"GitHub authenticated as: {user.login}")
            self._repo  = self._get_or_create_repo()
            self._ready = bool(self._repo)
        except Exception as e:
            log.error(f"GitHub init failed: {e}")

    # ── Public API ─────────────────────────────────────────────────────────────

    def publish_tools(self, tools: list["BuiltTool"]) -> list[str]:
        """
        Publish all tools to GitHub.
        Returns list of URLs for published tools.
        """
        if not self._ready or not tools:
            return []

        run_date = config.RUN_DATE
        urls     = []

        for tool in tools:
            try:
                url = self._publish_tool(tool, run_date)
                if url:
                    urls.append(url)
            except Exception as e:
                log.error(f"Failed to publish {tool.tool_name}: {e}")

        # Update root index after all tools committed
        if urls:
            try:
                self._update_index(tools, run_date)
            except Exception as e:
                log.warning(f"Index update failed: {e}")

        log.info(f"Published {len(urls)}/{len(tools)} tools to GitHub")
        return urls

    # ── Internal ───────────────────────────────────────────────────────────────

    def _get_or_create_repo(self):
        """Get or create the tools repository."""
        username = self._user.login
        full_name = f"{username}/{config.TOOLS_REPO_NAME}"
        try:
            repo = self._gh.get_repo(full_name)
            log.info(f"Using existing repo: {full_name}")
            return repo
        except GithubException as e:
            if e.status == 404:
                log.info(f"Creating new repo: {full_name}")
                return self._user.create_repo(
                    config.TOOLS_REPO_NAME,
                    description=config.TOOLS_REPO_DESC,
                    private=False,
                    auto_init=True,
                    has_wiki=False,
                    has_projects=False,
                )
            raise

    def _publish_tool(self, tool: "BuiltTool", run_date: str) -> Optional[str]:
        """Commit a single tool's files to the repo."""
        base_path = f"tools/{run_date}/{tool.tool_name}"

        files = {
            f"{base_path}/{tool.tool_name}.py":       tool.code,
            f"{base_path}/test_{tool.tool_name}.py":  tool.test_code,
            f"{base_path}/requirements.txt":           "\n".join(tool.requirements) + "\n",
            f"{base_path}/README.md":                  tool.readme,
            f"{base_path}/metadata.json":              json.dumps({
                "tool_name":    tool.tool_name,
                "display_name": tool.display_name,
                "description":  tool.description,
                "topic":        tool.topic,
                "generated":    config.RUN_TS,
                "loops_needed": tool.loops_needed,
                "tests_passed": tool.test_result.passed,
            }, indent=2),
        }

        committed_count = 0
        for path, content in files.items():
            success = self._upsert_file(
                path=path,
                content=content,
                message=f"🤖 AutoAIForge: Add {tool.tool_name} [{run_date}]",
            )
            if success:
                committed_count += 1

        if committed_count > 0:
            url = f"https://github.com/{self._user.login}/{config.TOOLS_REPO_NAME}/tree/main/{base_path}"
            log.info(f"Published {tool.tool_name}: {url}")
            return url
        return None

    def _upsert_file(self, path: str, content: str, message: str) -> bool:
        """Create or update a file in the repo."""
        encoded = base64.b64encode(content.encode("utf-8")).decode()
        try:
            # Check if file exists to get its SHA (needed for updates)
            existing_sha = None
            try:
                existing = self._repo.get_contents(path)
                existing_sha = existing.sha
            except GithubException as e:
                if e.status != 404:
                    raise

            if existing_sha:
                self._repo.update_file(
                    path=path,
                    message=message,
                    content=encoded,
                    sha=existing_sha,
                )
            else:
                self._repo.create_file(
                    path=path,
                    message=message,
                    content=encoded,
                )
            return True
        except Exception as e:
            log.error(f"Failed to upsert {path}: {e}")
            return False

    def _update_index(self, tools: list["BuiltTool"], run_date: str):
        """Update root INDEX.md with today's generated tools."""
        try:
            existing = self._repo.get_contents("INDEX.md")
            existing_content = base64.b64decode(existing.content).decode("utf-8")
            existing_sha = existing.sha
        except GithubException:
            existing_content = self._initial_index()
            existing_sha = None

        # Build today's section
        lines = [f"\n## {run_date}\n"]
        for tool in tools:
            url = (
                f"https://github.com/{self._user.login}/{config.TOOLS_REPO_NAME}"
                f"/tree/main/tools/{run_date}/{tool.tool_name}"
            )
            lines.append(f"- **[{tool.display_name}]({url})** — {tool.description[:100]}")
            lines.append(f"  - Topic: `{tool.topic}` | Tests: ✅ {tool.test_result.passed}")
        section = "\n".join(lines)

        # Prepend today's section after the header
        header_end = existing_content.find("\n## ")
        if header_end == -1:
            new_content = existing_content + section
        else:
            new_content = existing_content[:header_end] + section + existing_content[header_end:]

        if existing_sha:
            self._repo.update_file("INDEX.md", f"📋 Update index [{run_date}]",
                                    base64.b64encode(new_content.encode()).decode(),
                                    existing_sha)
        else:
            self._repo.create_file("INDEX.md", f"📋 Create index [{run_date}]",
                                    base64.b64encode(new_content.encode()).decode())

    @staticmethod
    def _initial_index() -> str:
        return """\
# AutoAIForge Tools Index 🤖

Daily AI tools auto-generated from trending news.
Each tool is built, tested, and ready to use.

> Generated by [AutoAIForge](https://github.com/autoaiforge/autoaiforge)

"""
