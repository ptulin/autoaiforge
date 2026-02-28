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
        "run_date":         config.RUN_DATE,
        "items_scraped":    0,
        "items_added":      0,
        "topics_found":     0,
        "ideas_generated":  0,
        "tools_built":      0,
        "tools_published":  0,
        "errors":           [],
        "published_urls":   [],
        # Rich detail for email
        "topics_list":      [],   # [{topic, description, relevance}]
        "ideas_list":       [],   # [{tool_name, display_name, description, topic}]
        "built_tools_list": [],   # [{name, display_name, description, topic, url}]
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
        _send_email(stats)
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
        stats["topics_list"]  = [
            {"topic": t["topic"], "description": t.get("description",""), "relevance": t.get("relevance",5)}
            for t in topics
        ]
        log.info(f"  Found {len(topics)} topics:")
        for i, t in enumerate(topics, 1):
            log.info(f"    {i:2d}. [{t['relevance']}/10] {t['topic']}")
    except Exception as e:
        log.error(f"  Topic analysis failed: {e}")
        stats["errors"].append(f"TopicAnalysis: {e}")

    if not topics:
        log.warning("No topics identified — aborting development pipeline")
        _save_db_to_git(db)
        _send_email(stats)
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
        stats["ideas_list"] = [
            {
                "tool_name":    idea.get("tool_name", ""),
                "display_name": idea.get("display_name", idea.get("tool_name", "")),
                "description":  idea.get("description", ""),
                "topic":        idea.get("topic", ""),
            }
            for idea in ideas
        ]
        log.info(f"  Generated {len(ideas)} tool ideas:")
        for idea in ideas:
            log.info(f"    • {idea['tool_name']}: {idea['description'][:80]}")
    except Exception as e:
        log.error(f"  Idea generation failed: {e}")
        stats["errors"].append(f"Ideation: {e}")

    if not ideas:
        log.warning("No ideas generated — skipping development")
        _save_db_to_git(db)
        _send_email(stats)
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
        _send_email(stats)
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

        # Build enriched built-tools list for the email
        url_map = {u.split("/")[-1]: u for u in urls}
        stats["built_tools_list"] = [
            {
                "name":         t.tool_name,
                "display_name": t.display_name,
                "description":  t.description,
                "topic":        t.topic,
                "url":          url_map.get(t.tool_name, ""),
            }
            for t in built_tools
        ]
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
    _send_email(stats)

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

        # Also add generated tools (published to this repo now)
        tools_dir = Path(config.TOOLS_DIR)
        if tools_dir.exists():
            subprocess.run(["git", "add", str(tools_dir)], capture_output=True, cwd=repo_root)

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


def _send_email(stats: dict):
    """
    Send a daily HTML summary email via Gmail SMTP.
    Shows hot topics, all tool ideas, and all built tools with GitHub links.
    Requires GMAIL_APP_PASSWORD secret to be set.
    """
    if not config.GMAIL_APP_PASSWORD:
        log.info("Email skipped — GMAIL_APP_PASSWORD not set")
        return

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    actions_url = "https://github.com/ptulin/autoaiforge/actions"
    repo_url    = "https://github.com/ptulin/autoaiforge"

    # ── Topics section ─────────────────────────────────────────────────────────
    topics_html = ""
    topics_list = stats.get("topics_list", [])
    if topics_list:
        rows = ""
        for t in topics_list:
            rows += f"""
            <tr>
              <td style="padding:6px 12px;font-weight:600;white-space:nowrap;">
                🔥 {t['topic']}
              </td>
              <td style="padding:6px 12px;color:#586069;font-size:13px;">
                {t.get('description','')[:120]}
              </td>
            </tr>"""
        topics_html = f"""
        <h3 style="margin-top:28px;color:#24292e;">🔥 Today's Hot AI Topics</h3>
        <table style="width:100%;border-collapse:collapse;border:1px solid #e1e4e8;border-radius:6px;overflow:hidden;">
          {rows}
        </table>"""

    # ── Ideas section ──────────────────────────────────────────────────────────
    ideas_html = ""
    ideas_list = stats.get("ideas_list", [])
    if ideas_list:
        rows = ""
        for i, idea in enumerate(ideas_list):
            bg = "background:#f6f8fa;" if i % 2 == 0 else ""
            rows += f"""
            <tr style="{bg}">
              <td style="padding:8px 12px;font-weight:600;">
                💡 {idea.get('display_name', idea.get('tool_name',''))}
              </td>
              <td style="padding:8px 12px;font-size:13px;color:#586069;">
                {idea.get('description','')[:150]}
              </td>
              <td style="padding:8px 12px;font-size:12px;color:#959da5;white-space:nowrap;">
                📌 {idea.get('topic','')[:40]}
              </td>
            </tr>"""
        ideas_html = f"""
        <h3 style="margin-top:28px;color:#24292e;">💡 Tool Ideas Generated ({len(ideas_list)})</h3>
        <table style="width:100%;border-collapse:collapse;border:1px solid #e1e4e8;border-radius:6px;overflow:hidden;">
          {rows}
        </table>"""

    # ── Built tools section ────────────────────────────────────────────────────
    built_html = ""
    built_list = stats.get("built_tools_list", [])
    if built_list:
        rows = ""
        for i, tool in enumerate(built_list):
            bg     = "background:#f6f8fa;" if i % 2 == 0 else ""
            url    = tool.get("url", "")
            link   = (f'<a href="{url}" style="color:#0366d6;font-size:12px;">📂 View on GitHub</a>'
                      if url else '<span style="color:#959da5;font-size:12px;">committing…</span>')
            rows += f"""
            <tr style="{bg}">
              <td style="padding:10px 12px;font-weight:600;">
                ✅ {tool.get('display_name', tool.get('name',''))}
              </td>
              <td style="padding:10px 12px;font-size:13px;color:#586069;">
                {tool.get('description','')[:150]}
              </td>
              <td style="padding:10px 12px;white-space:nowrap;">
                {link}
              </td>
            </tr>"""
        built_html = f"""
        <h3 style="margin-top:28px;color:#24292e;">🔨 Tools Built &amp; Tested ({len(built_list)})</h3>
        <p style="font-size:13px;color:#586069;margin:4px 0 12px;">
          These tools passed all automated tests and are committed to the repo.
        </p>
        <table style="width:100%;border-collapse:collapse;border:1px solid #e1e4e8;border-radius:6px;overflow:hidden;">
          {rows}
        </table>"""
    elif stats.get("tools_built", 0) == 0 and stats.get("ideas_generated", 0) > 0:
        built_html = """
        <h3 style="margin-top:28px;color:#24292e;">🔨 Tools Built &amp; Tested</h3>
        <p style="color:#cb2431;font-size:13px;">
          ⚠️ No tools passed tests this run. Check the Actions log for details.
        </p>"""

    # ── Errors section ─────────────────────────────────────────────────────────
    errors_html = ""
    if stats.get("errors"):
        errs = "".join(f"<li style='margin:4px 0;'>{e}</li>" for e in stats["errors"])
        errors_html = f"""
        <div style="margin-top:20px;padding:12px 16px;background:#fff5f5;border:1px solid #f97583;border-radius:6px;">
          <strong style="color:#cb2431;">⚠️ Issues this run:</strong>
          <ul style="margin:8px 0 0;padding-left:20px;color:#586069;font-size:13px;">{errs}</ul>
        </div>"""

    # ── Stats summary row ──────────────────────────────────────────────────────
    n_scraped   = stats.get('items_scraped', 0)
    n_topics    = stats.get('topics_found', 0)
    n_ideas     = stats.get('ideas_generated', 0)
    n_built     = stats.get('tools_built', 0)
    n_published = stats.get('tools_published', 0)
    elapsed     = stats.get('elapsed_seconds', '?')

    subject_emoji = "🚀" if n_published > 0 else ("🔨" if n_built > 0 else "📰")
    subject_tools = (f"{n_published} tools live"  if n_published > 0
                     else (f"{n_built} tools built" if n_built > 0
                           else f"{n_ideas} ideas, 0 built"))

    html = f"""
    <html><body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
                        max-width:720px;margin:auto;padding:24px;color:#24292e;">

      <h2 style="border-bottom:3px solid #0366d6;padding-bottom:10px;margin-bottom:16px;">
        🤖 AutoAIForge Daily Report — {stats['run_date']}
      </h2>

      <!-- Stats bar -->
      <table style="width:100%;border-collapse:collapse;background:#f6f8fa;
                    border:1px solid #e1e4e8;border-radius:8px;overflow:hidden;margin-bottom:8px;">
        <tr>
          <td style="padding:10px 14px;text-align:center;border-right:1px solid #e1e4e8;">
            <div style="font-size:22px;font-weight:700;">{n_scraped}</div>
            <div style="font-size:11px;color:#586069;text-transform:uppercase;letter-spacing:.5px;">articles</div>
          </td>
          <td style="padding:10px 14px;text-align:center;border-right:1px solid #e1e4e8;">
            <div style="font-size:22px;font-weight:700;">{n_topics}</div>
            <div style="font-size:11px;color:#586069;text-transform:uppercase;letter-spacing:.5px;">topics</div>
          </td>
          <td style="padding:10px 14px;text-align:center;border-right:1px solid #e1e4e8;">
            <div style="font-size:22px;font-weight:700;">{n_ideas}</div>
            <div style="font-size:11px;color:#586069;text-transform:uppercase;letter-spacing:.5px;">ideas</div>
          </td>
          <td style="padding:10px 14px;text-align:center;border-right:1px solid #e1e4e8;">
            <div style="font-size:22px;font-weight:700;">{n_built}</div>
            <div style="font-size:11px;color:#586069;text-transform:uppercase;letter-spacing:.5px;">built</div>
          </td>
          <td style="padding:10px 14px;text-align:center;">
            <div style="font-size:22px;font-weight:700;color:#28a745;">{n_published}</div>
            <div style="font-size:11px;color:#586069;text-transform:uppercase;letter-spacing:.5px;">published</div>
          </td>
        </tr>
      </table>

      {topics_html}
      {ideas_html}
      {built_html}
      {errors_html}

      <!-- Footer -->
      <p style="margin-top:32px;font-size:12px;color:#959da5;
                border-top:1px solid #e1e4e8;padding-top:16px;line-height:1.8;">
        ⏱ Runtime: {elapsed}s &nbsp;|&nbsp;
        <a href="{actions_url}" style="color:#0366d6;">Full logs (GitHub Actions)</a> &nbsp;|&nbsp;
        <a href="{repo_url}/tree/main/generated_tools/{stats['run_date']}"
           style="color:#0366d6;">Browse today's tools on GitHub</a>
      </p>
    </body></html>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"{subject_emoji} AutoAIForge [{stats['run_date']}]: {subject_tools}"
    msg["From"]    = config.EMAIL_FROM
    msg["To"]      = config.EMAIL_TO
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(config.EMAIL_FROM, config.GMAIL_APP_PASSWORD)
            smtp.sendmail(config.EMAIL_FROM, config.EMAIL_TO, msg.as_string())
        log.info(f"📧 Daily email sent to {config.EMAIL_TO}")
    except Exception as e:
        log.warning(f"Email failed (non-fatal): {e}")


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
