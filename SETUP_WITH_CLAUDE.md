# 🤖 Set Up AutoAIForge by Talking to Claude

No terminal. No config files. Just copy the prompt below into a Claude conversation
(claude.ai or Claude Code) and Claude will walk you through everything step by step.

---

## How it works

Claude will:
1. Create the GitHub repo for you
2. Push all the code automatically
3. Guide you to get 3 free API keys (takes ~5 minutes)
4. Add them all as GitHub Secrets for you
5. Trigger the first pipeline run
6. Set up daily email reports

You only need to:
- Click a few buttons on external sites (Groq, Google Cloud, Gmail)
- Paste keys/codes back to Claude when asked

---

## Step 1 — Fork the repo

Click **Fork** at: https://github.com/ptulin/autoaiforge
*(or use it as a template — top right button)*

---

## Step 2 — Start a Claude conversation

Open **https://claude.ai** and paste this exact prompt:

---

```
I want to deploy AutoAIForge — an autonomous AI tool factory that scrapes AI news
nightly, generates Python tools with an LLM, tests them, and publishes them to GitHub.

The source code is at: https://github.com/ptulin/autoaiforge

Please help me set it up completely. Here's what needs to happen:
1. I need a GitHub repo set up with the workflow file enabled
2. I need these 3 free API keys added as GitHub Secrets:
   - GROQ_API_KEY (from console.groq.com)
   - YOUTUBE_API_KEY (from Google Cloud Console)
   - GMAIL_APP_PASSWORD (from myaccount.google.com/apppasswords)
3. I want a daily email summary sent to [YOUR EMAIL HERE]

Please guide me one step at a time, wait for my confirmation before moving to the next step,
and handle all the GitHub API calls yourself — I'll just paste keys to you when you ask.

My GitHub username is: [YOUR GITHUB USERNAME HERE]
```

---

## That's it

Claude will take it from there. The whole setup takes about 10 minutes of back-and-forth.

---

## What you'll need during setup

| What Claude asks for | Where to get it | Time |
|---|---|---|
| GitHub device code authorization | github.com/login/device | 30 sec |
| Groq API key | console.groq.com → API Keys → Create | 2 min |
| YouTube API key | Google Cloud Console → APIs → YouTube Data API v3 → Credentials | 3 min |
| Gmail App Password | myaccount.google.com/apppasswords | 1 min |

All free. No credit card needed.

---

## After setup

- Pipeline runs every night at **2:00 AM UTC** automatically
- You get an email every morning with what was built
- New tools appear at: `https://github.com/YOUR_USERNAME/autoaiforge-tools`
- Full logs at: `https://github.com/YOUR_USERNAME/autoaiforge/actions`
