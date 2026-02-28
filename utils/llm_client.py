"""
Multi-provider LLM client — GitHub Models (primary, FREE with GITHUB_TOKEN)
→ Groq → Together.ai (fallbacks).
All providers expose an OpenAI-compatible /chat/completions endpoint.

GitHub Models is the zero-config primary:
  - Free for all GitHub users
  - Uses GITHUB_TOKEN which is auto-provided by GitHub Actions
  - Models: gpt-4o, gpt-4o-mini, Meta-Llama, Phi, Mistral, etc.
"""

import json
import time
import requests
from typing import Optional

from utils.logger import get_logger
import config

log = get_logger("llm_client")

# ─── Provider registry ────────────────────────────────────────────────────────
# GitHub Models is primary — free, uses the same GITHUB_TOKEN auto-provided
# by GitHub Actions (zero extra configuration needed).
PROVIDERS = [
    {
        "name": "github_models",
        "base_url": "https://models.inference.ai.azure.com",
        "api_key": config.GITHUB_TOKEN,
        "model": "gpt-4o",
        "fast_model": "gpt-4o-mini",
        "max_tokens": 4096,
        "rpm_limit": 60,
    },
    {
        "name": "groq",
        "base_url": config.GROQ_BASE_URL,
        "api_key": config.GROQ_API_KEY,
        "model": config.GROQ_MODEL_LARGE,
        "fast_model": config.GROQ_MODEL_FAST,
        "max_tokens": 4096,
        "rpm_limit": 30,
    },
    {
        "name": "together",
        "base_url": config.TOGETHER_BASE_URL,
        "api_key": config.TOGETHER_API_KEY,
        "model": config.TOGETHER_MODEL,
        "fast_model": config.TOGETHER_MODEL,
        "max_tokens": 4096,
        "rpm_limit": 60,
    },
]


def _call_provider(
    provider: dict,
    messages: list[dict],
    max_tokens: int = 4096,
    temperature: float = 0.7,
    fast: bool = False,
) -> Optional[str]:
    """Single attempt to one provider. Returns text or None on failure."""
    api_key = provider["api_key"]
    if not api_key:
        log.debug(f"Provider {provider['name']} has no API key — skipping")
        return None

    model = provider["fast_model"] if fast else provider["model"]
    url   = f"{provider['base_url']}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=90)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 10))
            log.warning(f"{provider['name']} rate-limited — sleeping {retry_after}s")
            time.sleep(retry_after)
            resp = requests.post(url, headers=headers, json=payload, timeout=90)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except requests.exceptions.HTTPError as e:
        log.error(f"{provider['name']} HTTP error: {e} — {resp.text[:300]}")
    except Exception as e:
        log.error(f"{provider['name']} error: {e}")
    return None


def chat(
    prompt: str,
    system: str = "You are a helpful AI assistant.",
    max_tokens: int = 4096,
    temperature: float = 0.7,
    fast: bool = False,
    retries: int = 2,
) -> str:
    """
    Call the best available LLM provider.
    Raises RuntimeError if all providers fail.
    """
    messages = [
        {"role": "system", "content": system},
        {"role": "user",   "content": prompt},
    ]

    for provider in PROVIDERS:
        for attempt in range(retries):
            result = _call_provider(
                provider, messages, max_tokens=max_tokens,
                temperature=temperature, fast=fast,
            )
            if result:
                log.debug(f"LLM response from {provider['name']} ({len(result)} chars)")
                return result
            if attempt < retries - 1:
                time.sleep(2 ** attempt)

    raise RuntimeError("All LLM providers failed. Check API keys.")


def chat_json(
    prompt: str,
    system: str = "You are a helpful AI assistant. Always respond with valid JSON.",
    max_tokens: int = 4096,
    temperature: float = 0.5,
    fast: bool = False,
) -> dict:
    """
    Call LLM and parse the response as JSON.
    Strips markdown fences if present. Raises ValueError on parse failure.
    """
    raw = chat(prompt, system=system, max_tokens=max_tokens,
               temperature=temperature, fast=fast)

    # Strip markdown code fences
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first and last fence lines
        inner = []
        in_block = False
        for line in lines:
            if line.startswith("```"):
                in_block = not in_block
                continue
            if in_block or not text.startswith("```"):
                inner.append(line)
        text = "\n".join(inner).strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        # Try to extract JSON object/array from messy response
        import re
        match = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except json.JSONDecodeError:
                pass
        raise ValueError(f"LLM returned non-JSON: {text[:300]}\n{e}")
