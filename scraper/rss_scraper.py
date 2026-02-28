"""
Free-tier RSS/API scraper — no authentication required.
Sources:
  • HackerNews Algolia API     (completely free, no key)
  • Reddit JSON API            (public feeds, no key)
  • ArXiv RSS                  (free academic papers)
  • Dev.to API                 (free, no key)
  • GitHub Trending            (web scrape)
  • Hugging Face Papers        (RSS)
"""

import hashlib
import time
import re
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests

from utils.logger import get_logger
import config

log = get_logger("rss_scraper")

HEADERS = {
    "User-Agent": (
        "AutoAIForge/1.0 (autonomous AI news aggregator; "
        "github.com/autoaiforge) python-requests"
    )
}
TIMEOUT = 20  # seconds


def _req(url: str, params: dict = None) -> Optional[dict]:
    """GET request with retry and error handling."""
    for attempt in range(3):
        try:
            r = requests.get(url, headers=HEADERS, params=params, timeout=TIMEOUT)
            r.raise_for_status()
            return r.json() if "json" in r.headers.get("content-type", "") else r.text
        except requests.exceptions.Timeout:
            log.warning(f"Timeout on {url} (attempt {attempt+1})")
        except requests.exceptions.HTTPError as e:
            log.warning(f"HTTP {e.response.status_code} for {url}")
            break
        except Exception as e:
            log.warning(f"Request error {url}: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
    return None


def _make_id(prefix: str, raw: str) -> str:
    return f"{prefix}_{hashlib.md5(raw.encode()).hexdigest()[:12]}"


# ─── HackerNews ───────────────────────────────────────────────────────────────

def scrape_hackernews(query: str = "AI", limit: int = 100) -> list[dict]:
    """Search HN via Algolia API."""
    cutoff = int((datetime.now(timezone.utc) - timedelta(hours=48)).timestamp())
    url    = "https://hn.algolia.com/api/v1/search_by_date"
    params = {
        "query":      query,
        "tags":       "story",
        "numericFilters": f"created_at_i>{cutoff}",
        "hitsPerPage": limit,
    }
    data = _req(url, params)
    if not isinstance(data, dict):
        return []

    items = []
    for hit in data.get("hits", []):
        items.append({
            "id":          _make_id("hn", hit.get("objectID", "")),
            "source":      "hackernews",
            "title":       hit.get("title", ""),
            "description": f"Points: {hit.get('points', 0)} | Comments: {hit.get('num_comments', 0)}",
            "url":         hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
            "published":   hit.get("created_at", ""),
            "keyword":     query,
            "extra":       {"points": hit.get("points", 0), "author": hit.get("author", "")},
        })
    return items


def scrape_all_hackernews() -> list[dict]:
    """Scrape HN for multiple AI-related queries."""
    all_items = []
    queries = ["AI", "LLM", "Claude", "machine learning", "open source AI", "language model"]
    for q in queries:
        all_items.extend(scrape_hackernews(query=q, limit=50))
        time.sleep(0.5)  # Be polite
    return _deduplicate(all_items)


# ─── Reddit ───────────────────────────────────────────────────────────────────

def scrape_reddit_subreddit(subreddit: str, limit: int = 50) -> list[dict]:
    """Fetch new posts from a subreddit via public JSON API."""
    url  = f"https://www.reddit.com/r/{subreddit}/new.json"
    data = _req(url, params={"limit": limit})
    if not isinstance(data, dict):
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    items  = []
    for post in data.get("data", {}).get("children", []):
        d = post.get("data", {})
        created = datetime.fromtimestamp(d.get("created_utc", 0), tz=timezone.utc)
        if created < cutoff:
            continue
        title  = d.get("title", "")
        url_   = d.get("url", "")
        self_t = d.get("selftext", "")[:300]
        items.append({
            "id":          _make_id("reddit", d.get("id", title)),
            "source":      f"reddit/{subreddit}",
            "title":       title,
            "description": self_t or d.get("url", ""),
            "url":         f"https://reddit.com{d.get('permalink', '')}",
            "published":   created.isoformat(),
            "keyword":     subreddit,
            "extra":       {
                "score":      d.get("score", 0),
                "comments":   d.get("num_comments", 0),
                "flair":      d.get("link_flair_text", ""),
            },
        })
    return items


def scrape_all_reddit() -> list[dict]:
    """Scrape all configured subreddits."""
    all_items = []
    for sub in config.REDDIT_SUBREDDITS:
        all_items.extend(scrape_reddit_subreddit(sub))
        time.sleep(1)  # Reddit rate-limits aggressively
    return _deduplicate(all_items)


# ─── ArXiv ────────────────────────────────────────────────────────────────────

def scrape_arxiv(query: str = "artificial+intelligence", max_results: int = 50) -> list[dict]:
    """Query ArXiv API for recent papers."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y%m%d")
    url    = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"ti:{query} OR abs:{query}",
        "sortBy":       "submittedDate",
        "sortOrder":    "descending",
        "max_results":  max_results,
    }
    try:
        r = requests.get(url, params=params, headers=HEADERS, timeout=30)
        r.raise_for_status()
    except Exception as e:
        log.warning(f"ArXiv request failed: {e}")
        return []

    # Parse Atom XML (no external XML parser needed)
    items = []
    entries = re.findall(r"<entry>(.*?)</entry>", r.text, re.DOTALL)
    for entry in entries[:max_results]:
        title_match   = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
        summary_match = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
        id_match      = re.search(r"<id>(.*?)</id>", entry)
        pub_match     = re.search(r"<published>(.*?)</published>", entry)

        title   = re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else ""
        summary = re.sub(r"\s+", " ", summary_match.group(1)).strip()[:400] if summary_match else ""
        link    = id_match.group(1).strip() if id_match else ""
        pub     = pub_match.group(1).strip() if pub_match else ""

        if title:
            items.append({
                "id":          _make_id("arxiv", link),
                "source":      "arxiv",
                "title":       title,
                "description": summary,
                "url":         link,
                "published":   pub,
                "keyword":     query,
                "extra":       {},
            })
    return items


def scrape_all_arxiv() -> list[dict]:
    queries = ["large+language+model", "AI+agent", "code+generation", "multimodal"]
    all_items = []
    for q in queries:
        all_items.extend(scrape_arxiv(query=q, max_results=30))
        time.sleep(1)
    return _deduplicate(all_items)


# ─── Dev.to ───────────────────────────────────────────────────────────────────

def scrape_devto(tag: str = "ai", per_page: int = 50) -> list[dict]:
    """Dev.to public API — no auth needed."""
    url  = "https://dev.to/api/articles"
    data = _req(url, params={"tag": tag, "per_page": per_page, "state": "fresh"})
    if not isinstance(data, list):
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(hours=48)
    items  = []
    for art in data:
        pub_str  = art.get("published_at") or art.get("created_at", "")
        try:
            pub_dt = datetime.fromisoformat(pub_str.rstrip("Z")).replace(tzinfo=timezone.utc)
        except Exception:
            pub_dt = cutoff  # Include if can't parse

        items.append({
            "id":          _make_id("devto", str(art.get("id", ""))),
            "source":      "dev.to",
            "title":       art.get("title", ""),
            "description": art.get("description", "")[:300],
            "url":         art.get("url", ""),
            "published":   pub_str,
            "keyword":     tag,
            "extra":       {
                "reactions":  art.get("positive_reactions_count", 0),
                "comments":   art.get("comments_count", 0),
                "reading_time": art.get("reading_time_minutes", 0),
            },
        })
    return items


def scrape_all_devto() -> list[dict]:
    tags = ["ai", "machinelearning", "llm", "artificialintelligence", "claudeai"]
    all_items = []
    for tag in tags:
        all_items.extend(scrape_devto(tag=tag))
        time.sleep(0.5)
    return _deduplicate(all_items)


# ─── GitHub Trending ──────────────────────────────────────────────────────────

def scrape_github_trending() -> list[dict]:
    """Scrape GitHub trending page for AI repos (no auth needed for web)."""
    url  = "https://api.github.com/search/repositories"
    params = {
        "q":     "topic:artificial-intelligence pushed:>2024-01-01 stars:>50",
        "sort":  "updated",
        "order": "desc",
        "per_page": 50,
    }
    try:
        r = requests.get(url, headers={**HEADERS, "Accept": "application/vnd.github+json"},
                         params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        log.warning(f"GitHub trending failed: {e}")
        return []

    items = []
    for repo in data.get("items", []):
        items.append({
            "id":          _make_id("gh", repo.get("full_name", "")),
            "source":      "github",
            "title":       f"{repo.get('full_name', '')} — {repo.get('description', '')}",
            "description": repo.get("description", ""),
            "url":         repo.get("html_url", ""),
            "published":   repo.get("updated_at", ""),
            "keyword":     "github trending AI",
            "extra":       {
                "stars":    repo.get("stargazers_count", 0),
                "language": repo.get("language", ""),
                "topics":   repo.get("topics", []),
            },
        })
    return items


# ─── Aggregator ───────────────────────────────────────────────────────────────

def scrape_all_free_sources() -> list[dict]:
    """Run all free scrapers and return combined, deduplicated results."""
    log.info("Starting free-source RSS/API scraping …")
    all_items: list[dict] = []

    for fn, name in [
        (scrape_all_hackernews, "HackerNews"),
        (scrape_all_reddit,     "Reddit"),
        (scrape_all_arxiv,      "ArXiv"),
        (scrape_all_devto,      "Dev.to"),
        (scrape_github_trending,"GitHub Trending"),
    ]:
        try:
            batch = fn()
            log.info(f"{name}: {len(batch)} items")
            all_items.extend(batch)
        except Exception as e:
            log.error(f"{name} scraper crashed: {e}")

    all_items = _deduplicate(all_items)
    log.info(f"Free sources total: {len(all_items)} unique items")
    return all_items


def _deduplicate(items: list[dict]) -> list[dict]:
    seen = set()
    out  = []
    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            out.append(item)
    return out
