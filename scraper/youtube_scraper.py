"""
YouTube Data API v3 scraper — free tier (10 000 quota units/day).
Each search.list call costs 100 units → max ~90 searches/day.
We track quota usage to stay within limits.
"""

import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional

from utils.logger import get_logger
import config

log = get_logger("youtube_scraper")

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    YT_OK = True
except ImportError:
    YT_OK = False
    log.warning("google-api-python-client not installed — YouTube scraping disabled")


def _yesterday_rfc3339() -> str:
    """ISO 8601 timestamp for 48 h ago (wider window to catch more content)."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    return cutoff.strftime("%Y-%m-%dT%H:%M:%SZ")


def _make_id(video_id: str) -> str:
    return f"yt_{video_id}"


class YouTubeScraper:
    def __init__(self):
        self._client = None
        self._quota_used = 0
        self._ready = False

        if not config.YOUTUBE_API_KEY:
            log.warning("YOUTUBE_API_KEY not set — YouTube scraping disabled")
            return
        if not YT_OK:
            return

        try:
            self._client = build(
                "youtube", "v3",
                developerKey=config.YOUTUBE_API_KEY,
                cache_discovery=False,
            )
            self._ready = True
            log.info("YouTube client ready")
        except Exception as e:
            log.error(f"YouTube client init failed: {e}")

    # ── Public API ─────────────────────────────────────────────────────────────

    def scrape_keyword(
        self, keyword: str, max_results: int = None
    ) -> list[dict]:
        """Return news items for a single keyword."""
        if not self._ready:
            return []
        if self._quota_used + 100 > config.YOUTUBE_QUOTA_BUDGET:
            log.warning("YouTube quota budget reached — skipping remaining keywords")
            return []

        max_results = max_results or config.YOUTUBE_MAX_RESULTS_PER_QUERY
        try:
            request = self._client.search().list(
                q=keyword,
                type="video",
                part="id,snippet",
                maxResults=min(max_results, 50),
                order="date",
                publishedAfter=_yesterday_rfc3339(),
                relevanceLanguage="en",
            )
            response = request.execute()
            self._quota_used += 100
            items = response.get("items", [])
            log.info(
                f"YouTube '{keyword}': {len(items)} results "
                f"(quota used: {self._quota_used})"
            )
            return [self._parse_item(item, keyword) for item in items]
        except Exception as e:
            log.error(f"YouTube search failed for '{keyword}': {e}")
            return []

    def scrape_all_keywords(self) -> list[dict]:
        """Scrape all configured keywords; respects quota budget."""
        results: list[dict] = []
        for keyword in config.SEARCH_KEYWORDS:
            if self._quota_used + 100 > config.YOUTUBE_QUOTA_BUDGET:
                log.warning(f"Stopping YouTube scrape at budget limit after {len(results)} items")
                break
            results.extend(self.scrape_keyword(keyword))
        log.info(f"YouTube total: {len(results)} items, quota used: {self._quota_used}")
        return self._deduplicate(results)

    # ── Internal ───────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_item(item: dict, keyword: str) -> dict:
        snippet = item.get("snippet", {})
        vid_id  = item.get("id", {}).get("videoId", "")
        return {
            "id":          _make_id(vid_id),
            "source":      "youtube",
            "title":       snippet.get("title", ""),
            "description": snippet.get("description", "")[:500],
            "url":         f"https://www.youtube.com/watch?v={vid_id}",
            "published":   snippet.get("publishedAt", ""),
            "keyword":     keyword,
            "extra": {
                "channel":    snippet.get("channelTitle", ""),
                "channel_id": snippet.get("channelId", ""),
                "thumbnail":  snippet.get("thumbnails", {}).get("default", {}).get("url", ""),
            },
        }

    @staticmethod
    def _deduplicate(items: list[dict]) -> list[dict]:
        seen = set()
        out  = []
        for item in items:
            if item["id"] not in seen:
                seen.add(item["id"])
                out.append(item)
        return out
