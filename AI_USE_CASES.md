# AI Use Cases (2026) — ResumeForge

## Agentic upgrade
Today ResumeForge is a 4-LLM-call pipeline. Tomorrow it's a multi-agent crew:

| Agent | Role | Tool |
|---|---|---|
| JD Parser | Extract role / seniority / must-haves / sector | Claude Sonnet 4.6 |
| Gap Analyser | TF-IDF + semantic match vs master resume | sentence-transformers + scikit-learn |
| Discovery Question Builder | 5 JD-tuned high-leverage questions | Claude Opus 4.7 |
| Writer | Bullet generation with provenance | Claude / Gemini / Grok (parallel A/B) |
| Critic | ATS + Human + AI-slang detector | LLM-as-judge (Gemini 2.x long-context for full doc) |
| Style Enforcer | Calibri 9.5pt · 2-page · no AI slang | python-docx + Promptfoo regression |

Orchestrated via **LangGraph** or **CrewAI** with **Aider** in the loop for prompt self-improvement.

## Recommended stack (free/MIT)
- **LLMs:** Claude Opus 4.7 / Sonnet 4.6 (primary), Gemini 2.x (long-context critic), Grok (second-opinion judge), Ollama + Llama 3 (private fallback)
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
| Path | Tokens (in/out) | Cost @ 2026 Anthropic rates |
|---|---|---|
| JD parse | 800 / 200 | $0.005 |
| 5 questions | 1.2k / 600 | $0.012 |
| Bullet gen × 3 roles | 4.5k / 900 | $0.040 |
| Critic | 3k / 300 | $0.020 |
| **Total** | ~10k / 2k | **~$0.08** |

Target: < $0.50 per generation — comfortable headroom.

## Why this differentiates from Rezi / Teal / Enhancv
Those tools optimise words already on the page. ResumeForge **extracts uncovered context first** (the 5-question discovery loop), then writes — that's where the ATS + Human score lift compounds.
