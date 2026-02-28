# AutoAIForge 🤖

> **Autonomous AI Tool Factory** — Scrapes AI news nightly, identifies trending topics,
> and autonomously builds, tests, and publishes Python developer tools to GitHub.

Inspired by the "OpenClaw" concept: a fully automated pipeline that stays ahead of
AI news by generating usable tools *the morning news drops*.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        GitHub Actions (FREE scheduler)                   │
│                        Cron: 2:00 AM UTC daily                           │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │
         ┌─────────────────────▼─────────────────────┐
         │              main.py (Orchestrator)         │
         └──┬──────────┬──────────┬──────────┬────────┘
            │          │          │          │
   ┌────────▼──┐  ┌────▼────┐  ┌─▼────────┐ │
   │  SCRAPERS │  │STORAGE  │  │ANALYZER  │ │
   │           │  │         │  │          │ │
   │ YouTube   │  │ SQLite  │  │ LLM      │ │
   │ HN API    │→ │  (news) │→ │ topic    │ │
   │ Reddit    │  │         │  │ identify │ │
   │ ArXiv     │  │ChromaDB │  └──────────┘ │
   │ Dev.to    │  │(vectors)│              │
   │ GitHub ↑  │  └─────────┘              │
   └───────────┘                           │
                              ┌────────────▼────────────┐
                              │  IDEATION (Groq LLM)     │
                              │  3-5 tool ideas/topic    │
                              └────────────┬────────────┘
                                           │
                              ┌────────────▼────────────┐
                              │  DEVELOPER (Groq LLM)    │
                              │  Code gen → pytest       │
                              │  Up to 5 fix loops       │
                              └────────────┬────────────┘
                                           │
                              ┌────────────▼────────────┐
                              │  PUBLISHER (PyGitHub)    │
                              │  → autoaiforge-tools     │
                              │    /tools/YYYY-MM-DD/    │
                              └─────────────────────────┘
```

## Free Service Stack

| Component | Service | Cost |
|-----------|---------|------|
| **Scheduler** | GitHub Actions cron | FREE (unlimited for public repos) |
| **LLM (primary)** | Groq API (llama-3.1-70b) | FREE (14,400 req/day) |
| **LLM (fallback)** | Together.ai | FREE ($25 credit) |
| **Embeddings** | sentence-transformers (local) | FREE |
| **Vector DB** | ChromaDB (in-memory, per-run) | FREE |
| **Raw storage** | SQLite (committed to repo) | FREE |
| **News: YouTube** | YouTube Data API v3 | FREE (10,000 units/day) |
| **News: HN** | HN Algolia API | FREE (no auth) |
| **News: Reddit** | Reddit JSON API | FREE (no auth) |
| **News: ArXiv** | ArXiv export API | FREE |
| **News: Dev.to** | Dev.to API | FREE |
| **Publishing** | GitHub API (PyGitHub) | FREE |

**Total cost: $0/month**

---

## Quick Start

### Option A: One-Click (Recommended)

```bash
git clone https://github.com/YOUR_USERNAME/autoaiforge.git
cd autoaiforge
bash setup.sh
```

### Option B: Manual

```bash
# 1. Install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. Run
python main.py
```

---

## GitHub Actions Deployment (Automated Nightly Runs)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial AutoAIForge setup"
gh repo create autoaiforge --public --push
```

### Step 2: Add GitHub Secrets

Go to **Settings → Secrets and variables → Actions** and add:

| Secret | Value | Where to get it |
|--------|-------|----------------|
| `GROQ_API_KEY` | Your Groq key | [console.groq.com](https://console.groq.com) → Free signup |
| `YOUTUBE_API_KEY` | YouTube key | [Google Cloud Console](https://console.cloud.google.com) → Enable YouTube Data API v3 |
| `TOGETHER_API_KEY` | Together.ai key | [api.together.ai](https://api.together.ai) → Free $25 credit |
| `WEBHOOK_URL` | Slack/Discord webhook | Optional: daily summary notifications |

> `GITHUB_TOKEN` is automatically provided by GitHub Actions — no setup needed.

### Step 3: Enable & Trigger

1. Go to **Actions** tab → Enable workflows
2. Click **AutoAIForge Daily Run → Run workflow** for an immediate test
3. Check the **autoaiforge-tools** repo for output

The pipeline runs automatically at **2:00 AM UTC** every night.

---

## Pipeline Steps

| Step | What happens |
|------|-------------|
| **1. Scrape** | Fetches AI news from YouTube, HackerNews, Reddit, ArXiv, Dev.to, GitHub |
| **2. Store** | Saves raw items to SQLite; builds vector index (ChromaDB) |
| **3. Analyze** | LLM identifies top 10 trending AI topics |
| **4. Ideate** | LLM generates 3-5 Python tool ideas per topic |
| **5. Build** | LLM generates code + tests; pytest validates; up to 5 auto-fix loops |
| **6. Publish** | Passing tools committed to `autoaiforge-tools` repo |

---

## Output Structure

The `autoaiforge-tools` repo (auto-created) looks like:

```
autoaiforge-tools/
├── INDEX.md                        ← Daily index of all tools
└── tools/
    ├── 2025-01-15/
    │   ├── llm_benchmark_runner/
    │   │   ├── llm_benchmark_runner.py
    │   │   ├── test_llm_benchmark_runner.py
    │   │   ├── requirements.txt
    │   │   ├── README.md
    │   │   └── metadata.json
    │   └── rag_pipeline_debugger/
    │       └── ...
    └── 2025-01-16/
        └── ...
```

---

## Configuration

All config is via environment variables (`.env` locally, GitHub Secrets in Actions):

```bash
# Required (pick at least one LLM)
GROQ_API_KEY=gsk_...

# Optional
YOUTUBE_API_KEY=AIza...
TOGETHER_API_KEY=...
WEBHOOK_URL=https://hooks.slack.com/...

# Tuning (optional overrides)
TOP_TOPICS_COUNT=10         # Topics to identify per run
IDEAS_PER_TOPIC=3           # Tool ideas per topic
MAX_TOOLS_PER_RUN=5         # Cap on tools generated per night
MAX_CORRECTION_LOOPS=5      # LLM self-fix attempts per tool
NEWS_RETENTION_DAYS=30      # Days of news to keep in SQLite
```

---

## Security Notes

- Generated code runs inside a sandboxed subprocess with a 60s timeout
- GitHub Actions provides process-level isolation per job
- No sensitive data is embedded in generated tools
- All tools are published publicly — review the output before using in production

---

## Local Development

```bash
# Run full pipeline
python main.py

# Run individual steps
python -c "from scraper.rss_scraper import scrape_all_free_sources; print(len(scrape_all_free_sources()))"

# Run tests
pytest tests/ -v

# Dry run (scrape + analyze, no tools built)
MAX_TOOLS_PER_RUN=0 python main.py
```

---

## Extending AutoAIForge

- **Add a news source**: Create a new scraper in `scraper/` and call it from `main.py`
- **Change LLM provider**: Add to `PROVIDERS` list in `utils/llm_client.py`
- **Change schedule**: Edit `cron` in `.github/workflows/autoaiforge.yml`
- **Add notifications**: Set `WEBHOOK_URL` for Slack/Discord summaries

---

*Built with ❤️ and 🤖 | Zero cost, fully autonomous*
