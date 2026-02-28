"""
X (Twitter) auto-poster for AutoAIForge.

Reads the latest tools from generated_tools/tools_index.json and posts
a daily tweet announcing new tools.

Requires GitHub Secrets:
  X_API_KEY
  X_API_SECRET
  X_ACCESS_TOKEN
  X_ACCESS_TOKEN_SECRET

Install: pip install tweepy
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import tweepy
except ImportError:
    print("tweepy not installed — skipping X post")
    sys.exit(0)


SITE_URL = "https://disruptiveexperience.com/aitools"
MAX_TOOL_LINE_LEN = 40   # Truncate long tool names
MAX_TOOLS_IN_TWEET = 5   # Twitter post limit


def get_today_tools() -> list[dict]:
    """Read today's tools from the local tools_index.json."""
    index_path = Path(__file__).parents[1] / "generated_tools" / "tools_index.json"
    if not index_path.exists():
        print(f"tools_index.json not found at {index_path}")
        return []

    try:
        data = json.loads(index_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to read tools_index.json: {e}")
        return []

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_tools = [t for t in data.get("tools", []) if t.get("date") == today]
    return today_tools[:MAX_TOOLS_IN_TWEET]


def build_tweet(tools: list[dict]) -> str:
    """Compose the tweet text (max 280 chars)."""
    n = len(tools)
    if n == 0:
        return ""

    lines = []
    lines.append(f"🤖 {n} new AI dev tool{'s' if n > 1 else ''} generated today by AutoAIForge:\n")

    for t in tools:
        name = t.get("display_name") or t.get("tool_name", "Unknown Tool")
        if len(name) > MAX_TOOL_LINE_LEN:
            name = name[:MAX_TOOL_LINE_LEN - 1] + "…"
        lines.append(f"• {name}")

    lines.append(f"\n🔗 {SITE_URL}")
    lines.append("\n#AI #DevTools #OpenSource #AutoAIForge")

    tweet = "\n".join(lines)

    # Safety trim to 280 chars (Twitter limit)
    if len(tweet) > 280:
        tweet = tweet[:277] + "…"

    return tweet


def post_tweet(tweet: str) -> bool:
    """Post the tweet using Twitter API v2 via Tweepy."""
    api_key        = os.getenv("X_API_KEY")
    api_secret     = os.getenv("X_API_SECRET")
    access_token   = os.getenv("X_ACCESS_TOKEN")
    access_secret  = os.getenv("X_ACCESS_TOKEN_SECRET")

    if not all([api_key, api_secret, access_token, access_secret]):
        missing = [k for k, v in {
            "X_API_KEY": api_key,
            "X_API_SECRET": api_secret,
            "X_ACCESS_TOKEN": access_token,
            "X_ACCESS_TOKEN_SECRET": access_secret,
        }.items() if not v]
        print(f"X posting skipped — missing env vars: {', '.join(missing)}")
        return False

    try:
        client = tweepy.Client(
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_secret,
        )
        response = client.create_tweet(text=tweet)
        tweet_id = response.data["id"]
        print(f"✅ Posted to X: https://twitter.com/i/web/status/{tweet_id}")
        return True
    except tweepy.TweepyException as e:
        print(f"❌ X post failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error posting to X: {e}")
        return False


def main():
    tools = get_today_tools()
    if not tools:
        print("No tools generated today — skipping X post")
        sys.exit(0)

    tweet = build_tweet(tools)
    print("── Tweet Preview ─────────────────────────────────────────")
    print(tweet)
    print(f"Length: {len(tweet)} chars")
    print("──────────────────────────────────────────────────────────")

    success = post_tweet(tweet)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
