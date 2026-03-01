"""
email_sender.py — Nightly AI Tools Digest

Reads today's tools from tools_index.json → fetches confirmed subscribers
from Supabase → sends personalized HTML email digest via Resend.

Env vars required:
  SUPABASE_URL            — e.g. https://xxxx.supabase.co
  SUPABASE_SERVICE_ROLE_KEY — service role key (bypasses RLS)
  RESEND_API_KEY          — from resend.com
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date, datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fetch_json(url: str, headers: dict = None) -> dict | list:
    req = urllib.request.Request(url, headers=headers or {})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def post_json(url: str, data: dict, headers: dict = None) -> dict:
    body = json.dumps(data).encode()
    h = {"Content-Type": "application/json", **(headers or {})}
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode()}") from e


def topic_emoji(topic: str) -> str:
    mapping = {
        "Machine Learning": "🧠", "NLP": "💬", "Computer Vision": "👁️",
        "Robotics": "🤖", "Data Science": "📊", "Security": "🔒",
        "DevTools": "🛠️", "API": "🔌", "Cloud": "☁️", "Audio": "🎵",
        "Video": "🎬", "Image Generation": "🎨", "Agents": "🕵️",
        "RAG": "📚", "FineTuning": "⚙️", "Benchmark": "📈",
    }
    for k, v in mapping.items():
        if k.lower() in topic.lower():
            return v
    return "🔧"


# ---------------------------------------------------------------------------
# Supabase helpers
# ---------------------------------------------------------------------------

def get_subscribers(supabase_url: str, service_key: str) -> list[dict]:
    """Fetch all confirmed subscribers from Supabase."""
    url = f"{supabase_url}/rest/v1/subscribers?confirmed=eq.true&select=email,topics,subscribe_all,unsubscribe_token"
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }
    return fetch_json(url, headers)


# ---------------------------------------------------------------------------
# Email builder
# ---------------------------------------------------------------------------

def build_email(tools: list[dict], subscriber: dict, site_url: str) -> str:
    email = subscriber["email"]
    unsub_token = subscriber.get("unsubscribe_token", "")
    unsub_url = f"{site_url}/api/unsubscribe?token={unsub_token}&email={urllib.parse.quote(email)}"

    today = date.today().strftime("%B %d, %Y")

    # Filter tools by subscriber's topic preferences
    if not subscriber.get("subscribe_all", True) and subscriber.get("topics"):
        wanted_topics = {t.lower() for t in subscriber["topics"]}
        display_tools = [t for t in tools if t.get("topic", "").lower() in wanted_topics]
        if not display_tools:
            display_tools = tools  # fallback: send all if no matches
    else:
        display_tools = tools

    if not display_tools:
        return None  # Nothing to send

    tool_cards = ""
    for tool in display_tools[:8]:  # cap at 8 tools per email
        emoji = topic_emoji(tool.get("topic", ""))
        tool_url = f"{site_url}/tool/{tool.get('date', '')}/{tool.get('tool_name', '')}"
        github_url = tool.get("github_url", "#")
        tests = "✅ Tests passing" if tool.get("tests_passed") else "⚠️ Tests skipped"

        tool_cards += f"""
        <div style="background:#0d1424;border:1px solid #1e2d4a;border-radius:10px;padding:20px;margin-bottom:16px">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
            <span style="background:#1e3a5f;color:#60a5fa;border:1px solid #2563eb;padding:3px 10px;border-radius:20px;font-size:12px;font-weight:600">
              {emoji} {tool.get('topic', '')}
            </span>
            <span style="color:#334155;font-size:12px">{tests}</span>
          </div>
          <h3 style="color:#fff;font-size:16px;font-weight:700;margin:0 0 8px">{tool.get('display_name', tool.get('tool_name', ''))}</h3>
          <p style="color:#94a3b8;font-size:14px;margin:0 0 14px;line-height:1.5">{tool.get('description', '')[:180]}{'…' if len(tool.get('description','')) > 180 else ''}</p>
          <div style="display:flex;gap:10px">
            <a href="{tool_url}" style="background:#2563eb;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none;font-size:13px;font-weight:600">View Details</a>
            <a href="{github_url}" style="background:#1e2d4a;color:#94a3b8;padding:8px 16px;border-radius:6px;text-decoration:none;font-size:13px">GitHub →</a>
          </div>
        </div>"""

    count = len(display_tools)
    more_count = max(0, count - 8)

    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#050914;color:#e2e8f0;margin:0;padding:0">
  <div style="max-width:600px;margin:0 auto;padding:32px 16px">

    <!-- Header -->
    <div style="text-align:center;margin-bottom:32px;padding:24px;background:#0d1424;border:1px solid #1e2d4a;border-radius:12px">
      <div style="font-size:40px;margin-bottom:8px">🤖</div>
      <h1 style="color:#fff;margin:0 0 4px;font-size:22px">AutoAIForge Daily Digest</h1>
      <p style="color:#60a5fa;margin:0;font-size:14px">{today} · {count} new tool{'s' if count != 1 else ''} generated</p>
    </div>

    <!-- Tools -->
    {tool_cards}

    {"<div style='text-align:center;margin:20px 0'><a href='" + site_url + "' style='color:#60a5fa;text-decoration:none;font-size:14px'>View all " + str(more_count) + " more tools →</a></div>" if more_count > 0 else ""}

    <!-- CTA -->
    <div style="text-align:center;margin:28px 0;padding:24px;background:#0d1424;border:1px solid #1e2d4a;border-radius:12px">
      <a href="{site_url}" style="display:inline-block;background:#2563eb;color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px">
        Browse All AI Tools →
      </a>
    </div>

    <!-- Footer -->
    <div style="text-align:center;margin-top:24px">
      <p style="color:#334155;font-size:12px">
        You're receiving this because you subscribed to AutoAIForge.<br>
        <a href="{unsub_url}" style="color:#475569">Unsubscribe</a> ·
        <a href="{site_url}" style="color:#475569">Visit Site</a>
      </p>
    </div>

  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Send via Resend
# ---------------------------------------------------------------------------

def send_email(resend_key: str, to: str, subject: str, html: str):
    import urllib.parse
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {resend_key}",
        "Content-Type": "application/json",
    }
    data = {
        "from": "AutoAIForge <noreply@disruptiveexperience.com>",
        "to": [to],
        "subject": subject,
        "html": html,
    }
    return post_json(url, data, headers)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import urllib.parse  # noqa — needed in scope for send_email helper

    supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
    resend_key = os.getenv("RESEND_API_KEY", "")
    site_url = os.getenv("NEXT_PUBLIC_SITE_URL", "https://aitools.disruptiveexperience.com")

    # Gracefully skip if secrets aren't configured yet
    if not all([supabase_url, service_key, resend_key]):
        print("⚠️  Email sender: missing env vars (SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY / RESEND_API_KEY). Skipping.")
        return

    # Load today's tools from tools_index.json
    index_path = "generated_tools/tools_index.json"
    if not os.path.exists(index_path):
        print(f"⚠️  {index_path} not found. Skipping email digest.")
        return

    with open(index_path) as f:
        index = json.load(f)

    today_str = date.today().isoformat()
    today_tools = [t for t in index.get("tools", []) if t.get("date") == today_str]

    if not today_tools:
        print(f"No tools generated today ({today_str}). Skipping email digest.")
        return

    print(f"📧 Sending digest: {len(today_tools)} tools to subscribers...")

    # Fetch confirmed subscribers
    try:
        subscribers = get_subscribers(supabase_url, service_key)
    except Exception as e:
        print(f"⚠️  Failed to fetch subscribers: {e}")
        return

    if not subscribers:
        print("No confirmed subscribers yet. Skipping.")
        return

    print(f"Found {len(subscribers)} confirmed subscriber(s)")

    today_display = date.today().strftime("%B %d")
    subject = f"🤖 {len(today_tools)} New AI Tools Today ({today_display}) — AutoAIForge"

    sent = 0
    failed = 0
    for sub in subscribers:
        html = build_email(today_tools, sub, site_url)
        if not html:
            print(f"  Skipping {sub['email']} — no matching tools for their topics")
            continue
        try:
            send_email(resend_key, sub["email"], subject, html)
            sent += 1
            print(f"  ✅ Sent to {sub['email']}")
        except Exception as e:
            failed += 1
            print(f"  ❌ Failed {sub['email']}: {e}")

    print(f"\n📧 Email digest complete: {sent} sent, {failed} failed")


if __name__ == "__main__":
    main()
