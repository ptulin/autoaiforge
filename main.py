#!/usr/bin/env python3
"""
AutoAIForge — Autonomous AI Tool Generation Pipeline
=====================================================

Daily pipeline (runs automatically via GitHub Actions cron):

  1. Scrape AI news → SQLite
  2. Embed & index → ChromaDB (in-memory, per-run)
  3. Identify top topics → LLM
  4. Ideate Python tools → LLM
  5. Build & test tools → Subprocess (up to 5 correction loops)
  6. Publish to GitHub → PyGitHub API
  7. Commit updated SQLite → Git
  8. Send optional webhook summary

Zero user interaction required. All errors are caught and logged.
"""

import sys
import json
import time
import traceback
import requests
from datetime import datetime, timezone
from pathlib import Path

# ── Bootstrap path so sub-modules resolve correctly ───────────────────────────
sys.path.insert(0, str(Path(__file__).parent))

import config
from config import validate as validate_config
from utils.logger import get_logger

log = get_logger("main")


def run_pipeline() -> dict:
    """
    Execute the full AutoAIForge pipeline.
    Returns a stats dict for logging/notification.
    """
    stats = {
        "run_date":       config.RUN_DATE,
        "items_scraped":  0,
        "items_added":    0,
        "topics_found":   0,
        "ideas_generated":0,
        "tools_built":    0,
        "tools_published":0,
        "errors":         [],
        "published_urls": [],
    }

    start_time = time.time()

    # ── 0. Validate configuration ──────────────────────────────────────────────
    log.info("=" * 60)
    log.info(f"AutoAIForge starting run: {config.RUN_TS}")
    log.info("=" * 60)

    missing = validate_config()
    if missing:
        # Non-fatal: log and continue; individual modules handle missing keys
        for m in missing:
            log.warning(f"CONFIG WARNING: {m}")

    # ── 1. News Scraping ───────────────────────────────────────────────────────
    log.info("[STEP 1/6] News Scraping")
    all_items: list[dict] = []

    # YouTube (if key available)
    try:
        from scraper.youtube_scraper import YouTubeScraper
        yt = YouTubeScraper()
        yt_items = yt.scrape_all_keywords()
        all_items.extend(yt_items)
        log.info(f"  YouTube: {len(yt_items)} items")
    except Exception as e:
        log.error(f"  YouTube scraper error: {e}")
        stats["errors"].append(f"YouTube: {e}")

    # Free RSS/API sources (always run)
    try:
        from scraper.rss_scraper import scrape_all_free_sources
        rss_items = scrape_all_free_sources()
        all_items.extend(rss_items)
        log.info(f"  RSS/API sources: {len(rss_items)} items")
    except Exception as e:
        log.error(f"  RSS scraper error: {e}")
        stats["errors"].append(f"RSS: {e}")

    stats["items_scraped"] = len(all_items)
    log.info(f"  Total scraped: {len(all_items)} items")

    if not all_items:
        log.warning("No news items scraped — aborting pipeline")
        stats["errors"].append("No items scraped")
        return stats

    # ── 2. Storage ─────────────────────────────────────────────────────────────
    log.info("[STEP 2/6] Storing & Indexing")

    try:
        from storage.db_manager import DBManager
        db = DBManager()
        db.purge_old()  # Clean up old data first
        added = db.insert_news(all_items)
        stats["items_added"] = added
        log.info(f"  SQLite: {added} new items (total: {db.count()})")
    except Exception as e:
        log.error(f"  DB error: {e}")
        stats["errors"].append(f"DB: {e}")
        db = None

    # Build vector index from recent items
    vector_store = None
    try:
        from storage.vector_store import VectorStore
        vs = VectorStore()
        if db and vs._ready:
            recent_pairs = db.get_titles_for_embedding(hours=48)
            indexed = vs.index_items(recent_pairs)
            log.info(f"  Vector store: {indexed} items indexed")
            vector_store = vs
    except Exception as e:
        log.error(f"  Vector store error: {e}")
        stats["errors"].append(f"VectorStore: {e}")

    # Collect items for analysis
    recent_items = db.get_recent_news(hours=48) if db else all_items[:500]

    # ── 3. Topic Analysis ──────────────────────────────────────────────────────
    log.info("[STEP 3/6] Topic Analysis")

    topics: list[dict] = []
    try:
        from analyzer.topic_analyzer import TopicAnalyzer
        analyzer = TopicAnalyzer(vector_store=vector_store)
        topics   = analyzer.analyze(recent_items, n_topics=config.TOP_TOPICS_COUNT)
        stats["topics_found"] = len(topics)
        log.info(f"  Found {len(topics)} topics:")
        for i, t in enumerate(topics, 1):
            log.info(f"    {i:2d}. [{t['relevance']}/10] {t['topic']}")
    except Exception as e:
        log.error(f"  Topic analysis failed: {e}")
        stats["errors"].append(f"TopicAnalysis: {e}")

    if not topics:
        log.warning("No topics identified — aborting development pipeline")
        _save_db_to_git(db)
        return stats

    # ── 4. Ideation ────────────────────────────────────────────────────────────
    log.info("[STEP 4/6] Idea Generation")

    ideas: list[dict] = []
    try:
        from ideation.idea_generator import IdeaGenerator
        gen   = IdeaGenerator()
        ideas = gen.generate_for_all_topics(
            topics,
            n_ideas_per_topic=config.IDEAS_PER_TOPIC,
            max_total=config.MAX_TOOLS_PER_RUN,
        )
        stats["ideas_generated"] = len(ideas)
        log.info(f"  Generated {len(ideas)} tool ideas:")
        for idea in ideas:
            log.info(f"    • {idea['tool_name']}: {idea['description'][:80]}")
    except Exception as e:
        log.error(f"  Idea generation failed: {e}")
        stats["errors"].append(f"Ideation: {e}")

    if not ideas:
        log.warning("No ideas generated — skipping development")
        _save_db_to_git(db)
        return stats

    # ── 5. Tool Development ────────────────────────────────────────────────────
    log.info("[STEP 5/6] Tool Development & Testing")

    built_tools = []
    try:
        from developer.tool_builder import ToolBuilder
        builder     = ToolBuilder()
        built_tools = builder.build_all(ideas)
        stats["tools_built"] = len(built_tools)
        log.info(f"  Built {len(built_tools)}/{len(ideas)} tools successfully")
        for tool in built_tools:
            log.info(f"    ✅ {tool.tool_name} (loops: {tool.loops_needed})")
    except Exception as e:
        log.error(f"  Tool development failed: {e}")
        stats["errors"].append(f"Development: {e}")

    if not built_tools:
        log.warning("No tools built successfully")
        _save_db_to_git(db)
        return stats

    # ── 6. Publishing ──────────────────────────────────────────────────────────
    log.info("[STEP 6/6] Publishing to GitHub")

    try:
        from publisher.github_publisher import GitHubPublisher
        publisher = GitHubPublisher()
        urls      = publisher.publish_tools(built_tools)
        stats["tools_published"] = len(urls)
        stats["published_urls"]  = urls
        log.info(f"  Published {len(urls)} tools:")
        for url in urls:
            log.info(f"    🔗 {url}")
    except Exception as e:
        log.error(f"  Publishing failed: {e}")
        stats["errors"].append(f"Publishing: {e}")

    # ── Finalize ───────────────────────────────────────────────────────────────
    elapsed = time.time() - start_time
    stats["elapsed_seconds"] = round(elapsed, 1)

    if db:
        try:
            db.log_run(config.RUN_DATE, stats)
        except Exception as e:
            log.warning(f"Failed to log run: {e}")
        _save_db_to_git(db)

    _print_summary(stats)
    _send_webhook(stats)

    return stats


def _save_db_to_git(db):
    """
    Commit the SQLite database back to the repository.
    In GitHub Actions, GITHUB_TOKEN allows pushing to the same repo.
    """
    import subprocess
    try:
        # Configure git (required in GitHub Actions)
        subprocess.run(
            ["git", "config", "user.email", "autoaiforge@bot.local"],
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "AutoAIForge Bot"],
            capture_output=True,
        )

        repo_root = Path(__file__).parent
        db_path   = Path(config.SQLITE_PATH)

        if not db_path.exists():
            return

        subprocess.run(["git", "add", str(db_path)], capture_output=True, cwd=repo_root)

        # Also add logs
        log_dir = Path(config.LOGS_DIR)
        if log_dir.exists():
            subprocess.run(["git", "add", str(log_dir)], capture_output=True, cwd=repo_root)

        result = subprocess.run(
            ["git", "commit", "-m",
             f"🤖 AutoAIForge data update [{config.RUN_DATE}] [skip ci]"],
            capture_output=True,
            text=True,
            cwd=repo_root,
        )

        if result.returncode == 0:
            # Push using the remote set by GitHub Actions
            push = subprocess.run(
                ["git", "push"],
                capture_output=True,
                text=True,
                cwd=repo_root,
            )
            if push.returncode == 0:
                log.info("Database committed and pushed to repo")
            else:
                log.warning(f"Git push failed: {push.stderr[:200]}")
        else:
            if "nothing to commit" in result.stdout:
                log.debug("No changes to commit (DB unchanged)")
            else:
                log.warning(f"Git commit failed: {result.stderr[:200]}")

    except Exception as e:
        log.warning(f"Git save failed (non-fatal): {e}")


def _print_summary(stats: dict):
    """Print a clean run summary."""
    log.info("")
    log.info("=" * 60)
    log.info("AUTOAIFORGE RUN COMPLETE")
    log.info("=" * 60)
    log.info(f"  Date:            {stats['run_date']}")
    log.info(f"  Items scraped:   {stats['items_scraped']}")
    log.info(f"  Items stored:    {stats['items_added']}")
    log.info(f"  Topics found:    {stats['topics_found']}")
    log.info(f"  Ideas generated: {stats['ideas_generated']}")
    log.info(f"  Tools built:     {stats['tools_built']}")
    log.info(f"  Tools published: {stats['tools_published']}")
    log.info(f"  Elapsed:         {stats.get('elapsed_seconds', '?')}s")
    if stats["errors"]:
        log.warning(f"  Errors ({len(stats['errors'])}):")
        for err in stats["errors"]:
            log.warning(f"    - {err}")
    if stats["published_urls"]:
        log.info("  Published URLs:")
        for url in stats["published_urls"]:
            log.info(f"    🔗 {url}")
    log.info("=" * 60)


def _send_webhook(stats: dict):
    """
    Send a brief summary to an optional Slack/Discord webhook.
    WEBHOOK_URL env var — leave empty to disable.
    """
    if not config.WEBHOOK_URL:
        return

    tools_list = "\n".join(f"• {u}" for u in stats.get("published_urls", []))
    text = (
        f"*AutoAIForge [{stats['run_date']}]*\n"
        f"Scraped: {stats['items_scraped']} | "
        f"Topics: {stats['topics_found']} | "
        f"Tools built: {stats['tools_built']} | "
        f"Published: {stats['tools_published']}\n"
        + (f"URLs:\n{tools_list}" if tools_list else "No tools published today")
    )
    try:
        requests.post(
            config.WEBHOOK_URL,
            json={"text": text},
            timeout=10,
        )
        log.info("Webhook notification sent")
    except Exception as e:
        log.warning(f"Webhook failed: {e}")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        stats = run_pipeline()
        exit_code = 0 if stats["tools_published"] >= 0 else 1
    except KeyboardInterrupt:
        log.info("Interrupted by user")
        exit_code = 130
    except Exception as e:
        log.critical(f"Pipeline crashed: {e}")
        traceback.print_exc()
        exit_code = 1

    sys.exit(exit_code)
