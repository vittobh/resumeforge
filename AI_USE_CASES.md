# AI Use Cases (2026) — ResumeForge

## Agentic upgrade
Today ResumeForge is a 4-LLM-call pipeline. Tomorrow it's a multi-agent crew:

| Agent | Role | Tool |
|---|---|---|
| JD Parser | Extract role / seniority / must-haves / sector | deterministic parser + Gemini free tier fallback |
| Gap Analyser | TF-IDF + semantic match vs master resume | sentence-transformers + scikit-learn |
| Discovery Question Builder | 5 JD-tuned high-leverage questions | Gemini free tier / Groq free plan / Ollama local |
| Writer | Bullet generation with provenance | Gemini free tier first, Groq fallback, Ollama local fallback |
| Critic | ATS + Human + AI-slang detector | deterministic scorer first, Gemini judge optional |
| Style Enforcer | Calibri 9.5pt · 2-page · no AI slang | python-docx + Promptfoo regression |

Orchestrated via **LangGraph** or **CrewAI** with **Aider** in the loop for prompt self-improvement.

## Recommended stack (free/MIT)
- **LLMs:** Gemini API free tier (primary hosted MVP), Groq free plan (fast fallback), Ollama + local models (private zero-cost fallback), OpenRouter/OpenAI/Anthropic only as optional paid adapters
- **Coding agents:** Claude Code, Cursor, Aider, OpenHands, Gemini CLI
- **NLP:** spaCy · sentence-transformers · rapidfuzz
- **Eval:** Promptfoo · DeepEval · Inspect (UK AISI)
- **Observability:** Langfuse · Arize Phoenix
- **Doc:** python-docx · pypandoc · pdfplumber · Marker (PDF → MD)
- **Vector / RAG (optional v0.3 cover-letter context):** Qdrant · Chroma · pgvector
- **MCP servers:** LinkedIn (planned), Notion, Google Drive

## Concrete prompt patterns

**System prompt (style enforcer):**
```
You are ResumeForge. Output 3 bullets per role. Rules:
- Concrete verbs + specific numbers only.
- No AI slang ("leverage", "outcome-based", "translate probabilistic").
- Mirror JD keywords ONLY where factually true vs source.
- Format: "<Verb> <object> <by mechanism>, <result with number>."
Refuse to fabricate metrics — if user did not provide a number, omit the bullet.
```

**User prompt (discovery → bullet):**
```
Role: {jd.role} ({jd.seniority})
Must-haves: {jd.must_have}
User answers:
Q1 (impact): {a1}
Q2 (leadership): {a2}
Q3 (technical): {a3}
Q4 (discovery): {a4}
Q5 (innovation): {a5}
Master-resume context: {relevant_section}
Produce 3 bullets with provenance tag (Q1/Q2/.../MR) per bullet.
```

## Eval hook (Promptfoo)
```yaml
prompts: ['file://prompts/resume_bullet.txt']
providers: ['anthropic:claude-sonnet-4-6', 'google:gemini-2-pro', 'xai:grok-2']
tests:
  - vars: { role: 'Senior AI PM', answers: '...' }
    assert:
      - type: contains  # must include user-provided KPI
        value: '99%'
      - type: llm-rubric
        value: 'No AI slang; concrete verb; ≤ 25 words; numbers present'
      - type: javascript
        value: 'output.split("\\n").length === 3'
```

## Cost envelope
| Path | Tokens (in/out) | MVP provider strategy |
|---|---|---|
| JD parse | 800 / 200 | deterministic first; Gemini free tier fallback |
| 5 questions | 1.2k / 600 | Gemini free tier / Groq free plan |
| Bullet gen × 3 roles | 4.5k / 900 | Gemini free tier first; Ollama local if quota hit |
| Critic | 3k / 300 | deterministic first; Gemini optional |
| **Total** | ~10k / 2k | **Target $0 for MVP demo path** |

Target: $0 for MVP demo path. Paid providers become opt-in adapters after product validation.

## Why this differentiates from Rezi / Teal / Enhancv
Those tools optimise words already on the page. ResumeForge **extracts uncovered context first** (the 5-question discovery loop), then writes — that's where the ATS + Human score lift compounds.
