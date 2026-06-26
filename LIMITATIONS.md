# Limitations & API Key Requirements

This prototype is **front-end-only with mock data**. Real AI features require API keys and (for most calls) a server-side proxy due to browser CORS.

## API keys

MVP should not store provider keys in browser localStorage for production. Use backend environment variables or a small proxy.

Preferred free/reusable provider order:

1. deterministic local pipeline for parse/score
2. Gemini API free tier for hosted generation
3. Groq free plan for fast hosted fallback
4. Ollama local for private zero-cost fallback
5. paid providers only as optional adapters

Open browser DevTools → Console and run **one** of:

```js
localStorage.setItem('GEMINI_API_KEY',    'AIza...');
localStorage.setItem('GROQ_API_KEY',      'your_groq_key_here');
```

Then reload. The "Live AI" badge will appear and supported buttons will attempt real calls.

## CORS reality (2026)
- **Gemini / Groq** — use backend proxy or server-side env vars.
- **Ollama / vLLM** — local; require a backend you run yourself.
- **OpenAI / Anthropic / OpenRouter** — optional paid adapters only.

## What's mocked vs real in this prototype
| Capability | Status | Becomes real with |
|---|---|---|
| All forms / mock data | ✅ works locally | — |
| LLM calls | 🔶 mock/deterministic by default | Gemini free tier / Groq free plan / Ollama local through backend |
| Voice (Whisper) | 🔶 Web Speech API fallback | Run Whisper locally |
| Vector RAG | 🔶 mocked | Qdrant / pgvector + embeddings provider |
| Third-party integrations (Stripe, Jira, Square, Twilio, Health Connect) | 🔶 mocked | OAuth setup + server |
| Persistence | 🔶 in-memory only | SQLite / Postgres backend |

## Recommended path to production
1. Front this prototype with a small FastAPI / Cloudflare Worker proxy.
2. Inject API keys server-side; clients never see them.
3. Replace mock data with real persistence.
4. Wire MCP servers for the third-party integrations.
5. Add Promptfoo / Langfuse for eval + observability.

See **`AI_USE_CASES.md`** for the full agentic upgrade plan.
