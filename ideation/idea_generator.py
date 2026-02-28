"""
Idea Generator — produces concrete, buildable Python tool/skill ideas
for each topic discovered by the analyzer.

Each idea is a structured JSON spec that the developer pipeline can
use to generate real, testable code.
"""

import json
from typing import Optional

from utils.logger import get_logger
from utils import llm_client
import config

log = get_logger("idea_generator")


# ─── Prompts ──────────────────────────────────────────────────────────────────

_IDEA_SYSTEM = (
    "You are a senior open-source Python developer specialising in AI developer tools. "
    "You design practical, creative, self-contained Python CLI tools and utility scripts "
    "that help developers work more effectively with AI. "
    "Focus on genuinely useful tools that can be built in 50-300 lines of Python."
)

_IDEA_PROMPT = """
Topic: {topic}
Description: {description}
Tool angle: {tool_angle}
Keywords: {keywords}

Generate exactly {n_ideas} distinct, buildable Python tool ideas related to this AI topic.
Each tool must be:
  - Self-contained Python script (50-300 lines)
  - Runnable from CLI or as a module
  - Testable with pytest unit tests
  - Using only freely available pip packages
  - Genuinely useful to AI developers

Return ONLY a JSON array where each object has:
{{
  "tool_name":      "snake_case_name",
  "display_name":   "Human Readable Name",
  "description":    "One-paragraph description of what this tool does and why it's useful",
  "tool_type":      one of ["cli_tool", "library", "api_wrapper", "data_processor", "automation"],
  "key_features":   ["feature 1", "feature 2", "feature 3"],
  "tech_stack":     ["package1", "package2"],
  "input_spec":     "What the tool takes as input (CLI args, stdin, files, etc.)",
  "output_spec":    "What the tool produces",
  "example_usage":  "python tool_name.py --example flag",
  "difficulty":     "easy" | "medium" | "hard",
  "novelty":        Brief explanation of what makes this unique/useful
}}

Do NOT suggest tools that are overly simple wrappers or already well-known tools.
Return ONLY the JSON array.
"""


# ─── Main ─────────────────────────────────────────────────────────────────────

class IdeaGenerator:
    def generate_for_topic(
        self,
        topic: dict,
        n_ideas: int = None,
    ) -> list[dict]:
        """
        Generate tool ideas for a single topic.
        Returns list of idea dicts.
        """
        n_ideas = n_ideas or config.IDEAS_PER_TOPIC

        prompt = _IDEA_PROMPT.format(
            topic=topic.get("topic", ""),
            description=topic.get("description", ""),
            tool_angle=topic.get("tool_angle", ""),
            keywords=", ".join(topic.get("keywords", [])),
            n_ideas=n_ideas,
        )

        try:
            result = llm_client.chat_json(
                prompt=prompt,
                system=_IDEA_SYSTEM,
                max_tokens=3000,
                temperature=0.8,  # More creative for ideation
            )

            if isinstance(result, list):
                ideas = result
            elif isinstance(result, dict):
                for key in ("ideas", "tools", "results", "data"):
                    if key in result and isinstance(result[key], list):
                        ideas = result[key]
                        break
                else:
                    ideas = [result]
            else:
                raise ValueError(f"Unexpected type: {type(result)}")

            validated = []
            for idea in ideas:
                if not isinstance(idea, dict) or not idea.get("tool_name"):
                    continue
                # Sanitise tool_name to valid python identifier
                raw_name = str(idea["tool_name"]).lower()
                raw_name = "".join(c if c.isalnum() or c == "_" else "_" for c in raw_name)
                raw_name = raw_name.strip("_")[:50]
                if not raw_name:
                    continue

                validated.append({
                    "tool_name":    raw_name,
                    "display_name": str(idea.get("display_name", raw_name))[:100],
                    "description":  str(idea.get("description", ""))[:500],
                    "tool_type":    str(idea.get("tool_type", "cli_tool")),
                    "key_features": list(idea.get("key_features", []))[:5],
                    "tech_stack":   list(idea.get("tech_stack", ["requests"]))[:8],
                    "input_spec":   str(idea.get("input_spec", ""))[:200],
                    "output_spec":  str(idea.get("output_spec", ""))[:200],
                    "example_usage":str(idea.get("example_usage", ""))[:200],
                    "difficulty":   str(idea.get("difficulty", "medium")),
                    "novelty":      str(idea.get("novelty", ""))[:300],
                    "topic":        topic.get("topic", ""),
                })

            log.info(f"Generated {len(validated)} ideas for topic: {topic.get('topic')}")
            return validated[:n_ideas]

        except Exception as e:
            log.error(f"Idea generation failed for topic '{topic.get('topic')}': {e}")
            return self._fallback_idea(topic, n_ideas)

    def generate_for_all_topics(
        self,
        topics: list[dict],
        n_ideas_per_topic: int = None,
        max_total: int = None,
        existing_tool_names: Optional[set] = None,
        existing_topics: Optional[set] = None,
        upgrade_topics: Optional[set] = None,
    ) -> list[dict]:
        """
        Generate ideas for all topics; cap at max_total.

        Deduplication / upgrade logic:
          - existing_topics: topic names that already have at least one tool.
            These are skipped unless the topic is in upgrade_topics.
          - existing_tool_names: snake_case tool names already in the collection.
            Used as a secondary filter — even if a topic is new, we skip an
            idea whose tool_name already exists (unless it's an upgrade).
          - upgrade_topics: topic names where existing tools should be refreshed.
            Tools generated for upgrade topics are tagged with is_upgrade=True.
        """
        max_total           = max_total or config.MAX_TOOLS_PER_RUN
        existing_tool_names = existing_tool_names or set()
        existing_topics     = existing_topics or set()
        upgrade_topics      = upgrade_topics or set()

        all_ideas: list[dict] = []

        for topic in topics:
            if len(all_ideas) >= max_total:
                break

            topic_name = topic.get("topic", "")
            is_upgrade = topic_name in upgrade_topics
            has_tool   = topic_name in existing_topics

            # Skip topics that already have tools unless flagged for upgrade
            if has_tool and not is_upgrade:
                log.info(
                    f"  ⏭  Skipping topic '{topic_name}' — tool already in collection"
                )
                continue

            if is_upgrade:
                log.info(f"  🔄 Upgrading tools for topic: '{topic_name}'")

            remaining = max_total - len(all_ideas)
            n         = min(n_ideas_per_topic or config.IDEAS_PER_TOPIC, remaining)
            ideas     = self.generate_for_topic(topic, n_ideas=n)

            # Secondary filter: skip any idea whose tool_name already exists
            # (prevents accidental exact-name collisions from the LLM)
            filtered: list[dict] = []
            for idea in ideas:
                tool_name = idea.get("tool_name", "")
                if tool_name in existing_tool_names and not is_upgrade:
                    log.info(
                        f"  ⏭  Skipping idea '{tool_name}' — name already in collection"
                    )
                    continue
                if is_upgrade:
                    idea["is_upgrade"] = True
                filtered.append(idea)

            all_ideas.extend(filtered)

        log.info(f"Total ideas generated: {len(all_ideas)}")
        return all_ideas

    @staticmethod
    def _fallback_idea(topic: dict, n: int) -> list[dict]:
        """Generate a generic fallback idea when LLM fails."""
        topic_name = topic.get("topic", "AI Tool")
        snake = topic_name.lower().replace(" ", "_")[:30]
        return [{
            "tool_name":    f"{snake}_helper",
            "display_name": f"{topic_name} Helper",
            "description":  f"A Python utility for working with {topic_name}",
            "tool_type":    "cli_tool",
            "key_features": ["Command-line interface", "JSON output", "Error handling"],
            "tech_stack":   ["requests", "click", "rich"],
            "input_spec":   "Command-line arguments",
            "output_spec":  "JSON or formatted text output",
            "example_usage": f"python {snake}_helper.py --help",
            "difficulty":   "easy",
            "novelty":      f"Useful utility for {topic_name} workflows",
            "topic":        topic.get("topic", ""),
        }][:n]
