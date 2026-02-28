"""
Topic Analyzer — identifies the top N trending AI topics from recent news.

Strategy (hybrid):
  1. Retrieve all recent news titles + descriptions from the vector store
  2. Cluster via sentence-transformer cosine-similarity groups (if available)
  3. Ask the LLM to identify the top N distinct topics and their relevance
  4. Return structured topic list for the ideation phase
"""

import json
import re
from typing import Optional

from utils.logger import get_logger
from utils import llm_client
import config

log = get_logger("topic_analyzer")


# ─── Prompts ──────────────────────────────────────────────────────────────────

_TOPIC_SYSTEM = (
    "You are an expert AI researcher and trend analyst. "
    "You identify the most significant, distinct, and actionable AI topics "
    "from a large corpus of recent news. Focus on concrete technical developments."
)

_TOPIC_PROMPT = """
Below are {n_items} recent AI news titles and snippets from the last 48 hours.
Identify exactly {n_topics} distinct, trending AI topics that would be most
valuable for developing open-source Python developer tools around.

For each topic output ONLY a JSON array with objects containing:
  - "topic":       Short topic name (3-7 words)
  - "description": One sentence explaining what this topic is about
  - "keywords":    List of 3-5 specific keywords for this topic
  - "relevance":   Score 1-10 indicating how much buzz/impact this has
  - "tool_angle":  One sentence on what kind of Python tool would be useful here

Return ONLY the JSON array, no other text.

NEWS CORPUS:
{corpus}
"""


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _build_corpus(items: list[dict], max_items: int = 80) -> str:
    """Format news items into a compact corpus string for the LLM.
    Capped at 80 items (~5000 tokens) to stay under GitHub Models 8k limit.
    """
    lines = []
    for i, item in enumerate(items[:max_items]):
        title = item.get("title", "").strip()
        desc  = (item.get("description") or "").strip()[:80]
        src   = item.get("source", "")
        line  = f"{i+1}. [{src}] {title}"
        if desc:
            line += f" — {desc}"
        lines.append(line)
    return "\n".join(lines)


def _fallback_topics(items: list[dict], n: int) -> list[dict]:
    """
    Keyword-based fallback topic extraction when LLM is unavailable.
    Groups items by keyword and returns top N by count.
    """
    from collections import Counter
    keyword_counts: Counter = Counter()
    for item in items:
        kw = item.get("keyword", "").strip()
        if kw:
            keyword_counts[kw] += 1

    topics = []
    for kw, count in keyword_counts.most_common(n):
        topics.append({
            "topic":       kw,
            "description": f"Trending topic with {count} articles: {kw}",
            "keywords":    kw.split()[:5],
            "relevance":   min(10, count // 2 + 1),
            "tool_angle":  f"Build a Python tool related to {kw}",
        })
    return topics[:n]


# ─── Main ─────────────────────────────────────────────────────────────────────

class TopicAnalyzer:
    def __init__(self, vector_store=None):
        self._vs = vector_store  # Optional, used for semantic grouping

    def analyze(
        self,
        news_items: list[dict],
        n_topics: int = None,
    ) -> list[dict]:
        """
        Identify top N topics from news items.
        Returns list of topic dicts (sorted by relevance desc).
        """
        n_topics = n_topics or config.TOP_TOPICS_COUNT

        if not news_items:
            log.warning("No news items to analyze")
            return []

        log.info(f"Analyzing {len(news_items)} items for top {n_topics} topics …")

        corpus = _build_corpus(news_items)
        prompt = _TOPIC_PROMPT.format(
            n_items=min(len(news_items), 80),
            n_topics=n_topics,
            corpus=corpus,
        )

        try:
            result = llm_client.chat_json(
                prompt=prompt,
                system=_TOPIC_SYSTEM,
                max_tokens=2048,
                temperature=0.4,
            )

            # Result may be list directly or wrapped in a key
            if isinstance(result, list):
                topics = result
            elif isinstance(result, dict):
                # Try common wrapper keys
                for key in ("topics", "results", "data", "items"):
                    if key in result and isinstance(result[key], list):
                        topics = result[key]
                        break
                else:
                    topics = [result]  # Single topic returned as dict
            else:
                raise ValueError(f"Unexpected LLM output type: {type(result)}")

            # Validate and normalise
            validated = []
            for t in topics:
                if not isinstance(t, dict) or not t.get("topic"):
                    continue
                validated.append({
                    "topic":       str(t.get("topic", ""))[:100],
                    "description": str(t.get("description", ""))[:300],
                    "keywords":    list(t.get("keywords", []))[:5],
                    "relevance":   int(t.get("relevance", 5)),
                    "tool_angle":  str(t.get("tool_angle", ""))[:300],
                })

            validated.sort(key=lambda x: x["relevance"], reverse=True)
            log.info(f"Identified {len(validated)} topics")
            return validated[:n_topics]

        except Exception as e:
            log.error(f"LLM topic analysis failed: {e} — using keyword fallback")
            return _fallback_topics(news_items, n_topics)

    def get_topic_summary(self, topics: list[dict]) -> str:
        """Human-readable summary of topics for logging/notifications."""
        lines = ["=== TODAY'S TOP AI TOPICS ==="]
        for i, t in enumerate(topics, 1):
            lines.append(
                f"{i:2d}. [{t['relevance']}/10] {t['topic']}\n"
                f"      {t['description']}"
            )
        return "\n".join(lines)
