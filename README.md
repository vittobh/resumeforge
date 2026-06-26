# ResumeForge — AI Resume Optimisation Tool

> A POC that turns a master resume + a job description into a tailored, ATS-optimised 2-page Word resume — gated by a 5-question discovery loop that extracts the 30–40% of context most candidates forget to include.

**Author:** Vittobha Vignesh S · **Status:** Draft for build · **Version:** 0.1 (POC)
**Stack:** Python 3.11+ · Free/reusable LLM provider layer (Gemini free tier · Groq free plan · Ollama local) · `python-docx` · Streamlit · FastAPI

See the full PRD/SRS → **[PRD.md](PRD.md)**.

MVP product plan → **[MVP.md](MVP.md)**.

## Core insight
> 90% of resume quality lift comes from extracting context the user forgot to include — not from rewriting what's already there.

Existing tools (Rezi, Teal, Enhancv, Kickresume) optimise the words already on the page. They miss the team sizes, real KPI numbers, scope of influence, technical trade-offs, and customer-discovery rigor that lives in the candidate's head. ResumeForge fixes that by asking 5 strategic questions — JD-tuned — before generation.

## The 5-question discovery framework
| # | Category | Extracts |
|---|---|---|
| Q1 | Business Impact | Revenue, retention, adoption, NPS, time-to-market, cost saved |
| Q2 | Leadership & Influence | Team size, mentorship, cross-functional partners, stakeholder seniority |
| Q3 | Technical Depth | Trade-offs, build-vs-buy, system-design choices, stack decisions |
| Q4 | Customer Discovery | User-research scope, interviews, A/B tests, validation rigor |
| Q5 | Innovation & Transformation | 0-to-1 launches, playbooks, org change, experiments shipped |

## Success criteria
- ATS score ≥ **94%** · Human score ≥ **90%**
- End-to-end pipeline < **90 seconds**
- Cost target: **$0 for MVP demo path** using deterministic fallback + Gemini free tier / Groq free plan / Ollama local where available
- Zero `.docx` validation failures across 10 test outputs
- 7/10 users prefer ResumeForge output over original in blind A/B

## Architecture (high level)
```
Streamlit UI → FastAPI → [Resume Parser · JD Parser · Discovery Engine]
                              ↓
                     Gap Analyser (TF-IDF + spaCy)
                              ↓
                  Generation Orchestrator (Free LLM Router)
                    Gemini free tier · Groq free plan · Ollama local
                              ↓
              [Docx Writer · Score Engine · ATS Validator · SQLite Cache]
```

## Roadmap
- **v0.1 POC** — single-user local app, .docx output, ATS + Human scoring
- **v0.2** — multi-profile management + LinkedIn import
- **v0.3** — cover-letter generation tied to same JD
- **v0.4** — browser extension ("tailor to this LinkedIn job")
- **v0.5** — recruiter mode (bulk-tailor for client roster)
- **v1.0** — SaaS launch with billing

## Why this matters for my portfolio
ResumeForge encodes my manual resume-optimisation workflow — proven across multiple successful senior-PM searches — into a repeatable AI pipeline. It demonstrates: PRD discipline, prompt-engineering rigor, eval methodology (ATS + Human scoring), provenance tracking, and cost-aware architecture. It also dogfoods the [pm-os](https://github.com/vittobh/pm-os) approach: a one-page PRD becomes a real product.

---
License: MIT


---

## 🚀 Live Prototype
**[https://vittobh.github.io/resumeforge/](https://vittobh.github.io/resumeforge/)**

Working front-end prototype: upload resume → paste JD → answer 5 discovery questions → see ATS + Human scores + provenance map. Mock backend by default; paste your Anthropic key into browser localStorage to attempt live Claude calls.

DnD Auto Mode is now available in the prototype:
- drag/drop Markdown or text resume context
- paste/drop JD
- auto-parse JD
- auto-generate discovery questions
- auto-generate resume draft, scores, provenance, and apply package
- stop before any external save, upload, message, or submit action

## 🤖 AI Use Cases (2026)
See **[AI_USE_CASES.md](AI_USE_CASES.md)** for the full agentic upgrade plan, recommended OSS stack (Claude, Gemini, Grok, Ollama, Aider, OpenHands, Promptfoo, Langfuse, etc.), concrete prompt patterns, eval harness, and cost envelope.

## 🧭 Browser Skill
See **[browser-skill/SKILL.md](browser-skill/SKILL.md)** and **[browser-skill/PATTERNS.md](browser-skill/PATTERNS.md)** for reusable browser navigation, click, typing, verification, and save-confirmation patterns. Use this with Codex Chrome plugin, Gemini CLI, Claude Code, Cursor, or any AI agent that operates a browser.

## 🔌 Backend API
Backend scaffold lives in **[backend/](backend/)**.

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --reload --app-dir ..
```

Smoke test without frontend:

```bash
cd backend
PYTHONPATH=.. python scripts/smoke_test.py
```

LLM policy: deterministic-first. Groq is used only for final 10% polish when `GROQ_API_KEY` is provided locally through environment variables. Never commit `.env`.

## ⚠️ Limitations
See **[LIMITATIONS.md](LIMITATIONS.md)** — what's mocked, what needs API keys, what needs a server proxy.

UI: light + dark mode (toggle in header, respects system preference).
