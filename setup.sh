#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# AutoAIForge — One-click local setup + GitHub deployment
# Usage: bash setup.sh
# ═══════════════════════════════════════════════════════════════════════════════
set -euo pipefail

BOLD="\033[1m"
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
BLUE="\033[34m"
RESET="\033[0m"

banner() { echo -e "\n${BOLD}${BLUE}━━━ $1 ━━━${RESET}\n"; }
ok()     { echo -e "${GREEN}✅  $1${RESET}"; }
warn()   { echo -e "${YELLOW}⚠️   $1${RESET}"; }
fail()   { echo -e "${RED}❌  $1${RESET}"; }
info()   { echo -e "    $1"; }

# ── 0. Check prerequisites ────────────────────────────────────────────────────
banner "AutoAIForge Setup"
echo "This script sets up AutoAIForge for local development and GitHub Actions deployment."

# Python
if ! command -v python3 &>/dev/null; then
    fail "Python 3 not found. Install from https://python.org"
    exit 1
fi
PY_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if python3 -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)"; then
    ok "Python $PY_VER"
else
    fail "Python 3.10+ required (found $PY_VER)"
    exit 1
fi

# Git
if ! command -v git &>/dev/null; then
    fail "git not found. Install git first."
    exit 1
fi
ok "git $(git --version | awk '{print $3}')"

# ── 1. Virtual environment ────────────────────────────────────────────────────
banner "Virtual Environment"
if [ ! -d ".venv" ]; then
    info "Creating virtual environment …"
    python3 -m venv .venv
fi
ok "Virtual environment ready"

# Activate
# shellcheck disable=SC1091
source .venv/bin/activate
info "Using: $(which python)"

# ── 2. Install dependencies ───────────────────────────────────────────────────
banner "Installing Dependencies"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
ok "All packages installed"

# Pre-download embedding model
info "Downloading sentence-transformer model (all-MiniLM-L6-v2) …"
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')" 2>&1 | tail -1
ok "Embedding model ready"

# ── 3. Environment file ───────────────────────────────────────────────────────
banner "API Key Configuration"

if [ -f ".env" ]; then
    warn ".env already exists — skipping creation (delete it to regenerate)"
else
    cat > .env << 'EOF'
# AutoAIForge — Environment Variables
# ======================================
# Fill in your free API keys below.
# Then add these same keys as GitHub Secrets for automated runs.

# ── REQUIRED: At least one LLM key ──────────────────────────────────────────
# Groq (recommended — free, fast): https://console.groq.com → API Keys
GROQ_API_KEY=

# Together.ai (fallback — free $25 credit): https://api.together.ai
TOGETHER_API_KEY=

# Hugging Face (fallback — free): https://huggingface.co/settings/tokens
HF_TOKEN=

# ── OPTIONAL: YouTube Data API ───────────────────────────────────────────────
# Free 10,000 quota units/day
# 1. Go to https://console.cloud.google.com
# 2. Create project → Enable "YouTube Data API v3"
# 3. Credentials → Create API Key
YOUTUBE_API_KEY=

# ── AUTO: GitHub (provided by GitHub Actions) ────────────────────────────────
# For local testing: https://github.com/settings/tokens (needs repo + workflow scope)
GITHUB_TOKEN=
GITHUB_USERNAME=

# ── OPTIONAL: Webhook (Slack/Discord) ────────────────────────────────────────
WEBHOOK_URL=

# ── OPTIONAL: Tools repo name (default: autoaiforge-tools) ───────────────────
TOOLS_REPO_NAME=autoaiforge-tools
EOF
    ok ".env created — fill in your API keys"
fi

echo ""
echo -e "${BOLD}📋 Keys you need to add to .env (and GitHub Secrets):${RESET}"
echo ""
echo -e "  ${BOLD}REQUIRED${RESET} (get one of these):"
echo "    🔑 GROQ_API_KEY     → https://console.groq.com  (free, 30 sec signup)"
echo ""
echo -e "  ${BOLD}OPTIONAL but recommended${RESET}:"
echo "    🔑 YOUTUBE_API_KEY  → https://console.cloud.google.com (free 10k/day)"
echo "    🔑 GITHUB_TOKEN     → https://github.com/settings/tokens"
echo ""

# ── 4. Test local run ─────────────────────────────────────────────────────────
banner "Local Test Run"

if [ -f ".env" ]; then
    # shellcheck disable=SC1091
    export $(grep -v '^#' .env | grep -v '^$' | xargs) 2>/dev/null || true
fi

if [ -z "${GROQ_API_KEY:-}" ] && [ -z "${TOGETHER_API_KEY:-}" ] && [ -z "${HF_TOKEN:-}" ]; then
    warn "No LLM API key set in .env — skipping test run"
    info "Add GROQ_API_KEY to .env and re-run: bash setup.sh"
else
    info "Running pipeline dry-run (scrape + analyze only) …"
    MAX_TOOLS_PER_RUN=0 python main.py && ok "Dry run succeeded!" || warn "Dry run completed with warnings (check logs/)"
fi

# ── 5. GitHub setup instructions ─────────────────────────────────────────────
banner "GitHub Actions Setup (Free Scheduler)"

echo "To enable automated nightly runs:"
echo ""
echo -e "  ${BOLD}Step 1:${RESET} Push this repo to GitHub"
echo "    git add ."
echo "    git commit -m 'Initial AutoAIForge setup'"
echo "    git remote add origin https://github.com/YOUR_USERNAME/autoaiforge.git"
echo "    git push -u origin main"
echo ""
echo -e "  ${BOLD}Step 2:${RESET} Add GitHub Secrets"
echo "    Go to: Settings → Secrets and variables → Actions → New repository secret"
echo ""
echo "    Add these secrets:"
echo "      GROQ_API_KEY       → your Groq key"
echo "      YOUTUBE_API_KEY    → your YouTube key (optional)"
echo "      TOGETHER_API_KEY   → your Together.ai key (optional)"
echo "      WEBHOOK_URL        → Slack/Discord webhook (optional)"
echo ""
echo -e "  ${BOLD}Step 3:${RESET} Enable GitHub Actions"
echo "    Go to: Actions tab → Enable workflows"
echo ""
echo -e "  ${BOLD}That's it!${RESET} AutoAIForge will run at 2 AM UTC every night. 🎉"
echo "  Manual trigger: Actions → AutoAIForge Daily Run → Run workflow"
echo ""

ok "Setup complete! AutoAIForge is ready."
