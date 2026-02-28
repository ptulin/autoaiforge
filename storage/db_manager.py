"""
SQLite database manager — raw news storage and retrieval.
Schema keeps last N days of data; older rows are purged automatically.
"""

import sqlite3
import json
from datetime import datetime, timedelta, timezone
from typing import Optional
from contextlib import contextmanager

from utils.logger import get_logger
import config

log = get_logger("db_manager")

# ─── DDL ──────────────────────────────────────────────────────────────────────
_SCHEMA = """
CREATE TABLE IF NOT EXISTS news_items (
    id          TEXT PRIMARY KEY,
    source      TEXT NOT NULL,
    title       TEXT NOT NULL,
    description TEXT,
    url         TEXT,
    published   TEXT,
    keyword     TEXT,
    extra       TEXT,
    ingested_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_news_source    ON news_items(source);
CREATE INDEX IF NOT EXISTS idx_news_published ON news_items(published);
CREATE INDEX IF NOT EXISTS idx_news_keyword   ON news_items(keyword);

CREATE TABLE IF NOT EXISTS run_log (
    run_date    TEXT PRIMARY KEY,
    items_added INTEGER DEFAULT 0,
    topics_found INTEGER DEFAULT 0,
    tools_built  INTEGER DEFAULT 0,
    tools_published INTEGER DEFAULT 0,
    summary     TEXT,
    completed_at TEXT
);
"""


@contextmanager
def _conn():
    con = sqlite3.connect(config.SQLITE_PATH, timeout=30)
    con.row_factory = sqlite3.Row
    try:
        yield con
    finally:
        con.close()


class DBManager:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        with _conn() as con:
            con.executescript(_SCHEMA)
            con.commit()
        log.info(f"SQLite ready at {config.SQLITE_PATH}")

    # ── News items ────────────────────────────────────────────────────────────

    def insert_news(self, items: list[dict]) -> int:
        """Insert news items; skip duplicates (by id). Returns count inserted."""
        inserted = 0
        now = datetime.now(timezone.utc).isoformat()
        with _conn() as con:
            for item in items:
                try:
                    con.execute(
                        """INSERT OR IGNORE INTO news_items
                           (id, source, title, description, url,
                            published, keyword, extra, ingested_at)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                        (
                            item.get("id", ""),
                            item.get("source", ""),
                            item.get("title", "")[:500],
                            (item.get("description") or "")[:2000],
                            item.get("url", ""),
                            item.get("published", ""),
                            item.get("keyword", ""),
                            json.dumps(item.get("extra", {})),
                            now,
                        ),
                    )
                    if con.execute("SELECT changes()").fetchone()[0]:
                        inserted += 1
                except Exception as e:
                    log.warning(f"Insert failed for item {item.get('id')}: {e}")
            con.commit()
        log.info(f"Inserted {inserted}/{len(items)} news items")
        return inserted

    def get_recent_news(
        self, hours: int = 48, limit: int = 2000
    ) -> list[dict]:
        """Return recent news items as dicts, newest first."""
        cutoff = (
            datetime.now(timezone.utc) - timedelta(hours=hours)
        ).isoformat()
        with _conn() as con:
            rows = con.execute(
                """SELECT * FROM news_items
                   WHERE ingested_at >= ?
                   ORDER BY ingested_at DESC
                   LIMIT ?""",
                (cutoff, limit),
            ).fetchall()
        return [dict(r) for r in rows]

    def get_titles_for_embedding(self, hours: int = 48) -> list[tuple[str, str]]:
        """Return (id, title + description snippet) for embedding."""
        rows = self.get_recent_news(hours=hours)
        results = []
        for r in rows:
            text = r["title"]
            if r["description"]:
                text += ". " + r["description"][:200]
            results.append((r["id"], text))
        return results

    def purge_old(self) -> int:
        """Delete news older than NEWS_RETENTION_DAYS. Returns count deleted."""
        cutoff = (
            datetime.now(timezone.utc) - timedelta(days=config.NEWS_RETENTION_DAYS)
        ).isoformat()
        with _conn() as con:
            con.execute("DELETE FROM news_items WHERE ingested_at < ?", (cutoff,))
            deleted = con.execute("SELECT changes()").fetchone()[0]
            con.commit()
        log.info(f"Purged {deleted} old news items")
        return deleted

    def count(self) -> int:
        with _conn() as con:
            return con.execute("SELECT COUNT(*) FROM news_items").fetchone()[0]

    # ── Run log ───────────────────────────────────────────────────────────────

    def log_run(self, run_date: str, stats: dict):
        with _conn() as con:
            con.execute(
                """INSERT OR REPLACE INTO run_log
                   (run_date, items_added, topics_found,
                    tools_built, tools_published, summary, completed_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (
                    run_date,
                    stats.get("items_added", 0),
                    stats.get("topics_found", 0),
                    stats.get("tools_built", 0),
                    stats.get("tools_published", 0),
                    stats.get("summary", ""),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            con.commit()

    def get_run_history(self, limit: int = 7) -> list[dict]:
        with _conn() as con:
            rows = con.execute(
                "SELECT * FROM run_log ORDER BY run_date DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]
