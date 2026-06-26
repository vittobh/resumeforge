from __future__ import annotations

import os
import json
import urllib.error
import urllib.request


from backend.app.models import ProviderName


class LlmProvider:
    """Free-first LLM provider. Groq is used only for final 10% polish when allowed."""

    def __init__(self) -> None:
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.model = os.getenv("RESUMEFORGE_LLM_MODEL", "llama-3.1-8b-instant")

    def available(self) -> bool:
        return bool(self.groq_key)

    async def final_polish(self, text: str) -> tuple[str, ProviderName, bool]:
        if not self.available():
            return text, ProviderName.deterministic, False

        prompt = (
            "Polish this resume/application text only for clarity and recruiter readability. "
            "Do not add facts, numbers, companies, tools, or claims. Preserve markdown.\n\n"
            f"{text}"
        )
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a strict resume editor. No fabrication."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 1200,
        }
        request = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.groq_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, KeyError, json.JSONDecodeError):
            return text, ProviderName.deterministic, False

        polished = data["choices"][0]["message"]["content"].strip()
        return polished or text, ProviderName.groq, True
