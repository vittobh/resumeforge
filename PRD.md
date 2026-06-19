# ResumeForge — PRD + SRS

| Field | Value |
|---|---|
| Product name | ResumeForge (working name) |
| Version | 0.1 — Proof of Concept |
| Author | Vittobha Vignesh S |
| Status | Draft for build |
| Target stack | Python 3.11+, Anthropic Claude API / OpenAI API, python-docx, Streamlit |

## 1. Executive summary
ResumeForge is a single-feature POC that takes a candidate's master resume (`.docx` or `.md`) and a target job description, asks the user 5 strategic discovery questions to extract uncovered context, and generates a tailored, ATS-optimised 2-page Word resume aligned to the target role with ATS ≥ 94% and Human ≥ 90% scores.

The product encodes a manual workflow proven across multiple successful senior-PM resume optimisations into a repeatable AI pipeline.

**Core insight:** 90% of resume quality lift comes from extracting context the user forgot to include — not from rewriting what's already there. The 5-question discovery loop is the differentiator.

## 2. Problem statement
Existing AI resume tools (Rezi, Teal, Enhancv, Kickresume) optimise the words already on the resume. They miss the 30–40% of relevant context that lives in the candidate's head — team sizes, real KPI numbers, scope of influence, technical trade-offs, customer-discovery rigor.

Result: cosmetic improvements, not strategic ones. ATS scores improve marginally; human scores stagnate because hiring managers don't see new substance.

ResumeForge solves this by:
- Asking 5 high-leverage discovery questions before generation
- Mapping user answers to specific bullets and sections
- Generating tailored output with traceable provenance (which answer drove which bullet)

## 3. Goals & non-goals

### 3.1 Goals (POC scope)
- Accept `.docx` or `.md` master resume + pasted JD
- Ask 5 structured discovery questions tuned to JD gaps
- Generate ATS-optimised 2-page `.docx` output
- Achieve ATS ≥ 94% and Human ≥ 90% on target role
- Local-first; no user data persisted server-side in POC

### 3.2 Non-goals (POC)
- Multi-resume profile management
- LinkedIn profile sync
- Cover-letter generation
- Interview prep
- Subscription / billing
- Mobile app

## 4. Target users
| Persona | Need | Frequency |
|---|---|---|
| Active job seeker (mid-senior PM / eng / data) | One-shot resume tailoring per role | 5–20 times in a job-search cycle |
| Passive candidate | Quick refresh when a recruiter pings | 1–3 times per quarter |
| Career coach | Bulk-tailor for clients | 10–50 per week |

**POC focus:** active job seeker, single-user, local app.

## 5. User journey (POC)
1. User uploads master resume (`.docx` / `.md`)
2. User pastes target JD (raw text)
3. System parses both, identifies coverage gaps
4. System asks 5 strategic discovery questions (tuned to gaps)
5. User answers (free text or voice transcript)
6. User selects format preferences (font, page count, sections)
7. System generates tailored `.docx`
8. User downloads + reviews ATS/Human score breakdown

## 6. The 5-question discovery framework

| # | Category | What it extracts |
|---|---|---|
| Q1 | Business Impact Metrics | Revenue, retention, adoption, NPS, time-to-market, cost saved |
| Q2 | Leadership & Influence | Team size, mentorship, cross-functional partners, stakeholder seniority |
| Q3 | Technical Depth & Architecture | Trade-offs, build-vs-buy, system-design choices, tech-stack decisions |
| Q4 | Customer Discovery & Validation | User-research scope, interviews, A/B tests, validation rigor |
| Q5 | Innovation & Transformation | 0-to-1 launches, playbooks, org change, experiments shipped |

Each question is dynamically rephrased based on JD parsing.

## 7. Functional requirements

### FR-1 — Resume ingestion
- Accept `.docx`, `.md`, `.pdf` (read-only)
- Extract structured sections: Summary, Skills, Experience, Education, Certifications, Tools
- Identify role periods, companies, project labels, bullets

### FR-2 — JD parsing
- Accept raw JD text (paste)
- Extract: role title, seniority, must-have skills, nice-to-have skills, sector keywords, soft skills, tools mentioned
- Build a JD keyword frequency map for ATS targeting

### FR-3 — Gap analysis
- Compare resume content vs JD requirements
- Score current resume on: keyword coverage, sector alignment, seniority signal, quantification density
- Identify the 5 highest-leverage gaps to ask about

### FR-4 — Discovery question generation
- Tune the 5 questions to JD-specific gaps
- Show 1–4 multiple-choice options per question where applicable
- Accept free-text fallback

### FR-5 — Resume generation
- Synthesise master resume + JD context + user answers
- Apply formatting rules (Calibri 9.5pt, black, 2 pages, hard page break, 3 skill blocks × 2 lines strict)
- Preserve user-edited content; only modify what was flagged as gap
- Output `.docx` with validated XML

### FR-6 — Score report
- ATS keyword coverage check against JD
- Human-score heuristics (concrete verbs, quantification density, AI-slang detection, length per section)
- Surface both scores + improvement suggestions

### FR-7 — Export
- Download tailored `.docx`
- Optional: export as `.md` for version control

## 8. Non-functional requirements
| Category | Requirement |
|---|---|
| Performance | Full pipeline < 90 seconds |
| Accuracy | ATS ≥ 94%, Human ≥ 90% |
| Privacy | No resume data persisted server-side in POC |
| Cost | < $0.50 per generation (Anthropic rates) |
| Usability | Zero-config; offline-capable with local LLM swap |
| Compatibility | `.docx` opens cleanly in Word / Google Docs / LibreOffice |
| Validation | Generated `.docx` passes XML validation before download |

## 9. System architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                      STREAMLIT FRONTEND (UI)                     │
│  Upload · Paste JD · Q&A · Preferences · Download · Scoreboard   │
└──────────────────────────┬───────────────────────────────────────┘
                           │
        ┌──────────────────▼──────────────────┐
        │       FASTAPI BACKEND (LOCAL)        │
        │  /ingest  /analyse  /generate  /score │
        └──────────────────┬──────────────────┘
                           │
   ┌───────────────────────┼───────────────────────┐
   │                       │                       │
┌──▼──────────┐    ┌───────▼────────┐    ┌────────▼────────┐
│  Resume     │    │   JD Parser    │    │  Discovery      │
│  Parser     │    │  (spaCy +      │    │  Engine         │
│ (python-    │    │   Claude)      │    │  (Claude prompt │
│  docx /     │    └───────┬────────┘    │   templates)    │
│  markdown)  │            │             └────────┬────────┘
└──┬──────────┘            │                      │
   │                       │                      │
   └──────────┬────────────┴──────────────────────┘
              │
       ┌──────▼────────────────────────────────┐
       │   GAP ANALYSER + KEYWORD MAP          │
       │   (Pandas + scikit-learn TF-IDF)      │
       └──────┬────────────────────────────────┘
              │
       ┌──────▼────────────────────────────────┐
       │   GENERATION ORCHESTRATOR             │
       │   (direct Anthropic SDK)              │
       └──────┬────────────────────────────────┘
              │
   ┌──────────┼──────────────────┬─────────────┐
   │          │                  │             │
┌──▼────┐ ┌───▼─────┐    ┌───────▼──────┐  ┌───▼─────┐
│ Docx  │ │  Score  │    │ ATS Validator│  │ Cache   │
│ Writer│ │ Engine  │    │ (Heuristic + │  │(SQLite) │
└───────┘ └─────────┘    │  LLM judge)  │  └─────────┘
                         └──────────────┘
```

## 10. Tech stack
| Layer | Choice |
|---|---|
| Language | Python 3.11+ |
| Deps | `uv` or `poetry` |
| Tests | `pytest` |
| Docx | `python-docx` ≥ 1.1.0 |
| Conversion | `pypandoc` |
| Markdown | `markdown-it-py` |
| PDF read | `pdfplumber` |
| LLM (primary) | `anthropic` (Claude Opus) |
| LLM (fallback) | `openai` |
| Token counting | `tiktoken` |
| NLP | `spaCy` (en_core_web_sm) |
| Keyword | `scikit-learn` TF-IDF, `rapidfuzz`, `nltk` |
| UI | `Streamlit` ≥ 1.32 |
| API | `FastAPI` + `uvicorn` |
| Storage | SQLite + Pydantic v2 |
| Logs | `structlog`, `rich` |
| Deploy | Docker, GitHub Actions CI |

## 11. Data model
```python
class MasterResume(BaseModel):
    user_id: str
    raw_text: str
    sections: dict[str, SectionContent]
    parsed_at: datetime

class JobDescription(BaseModel):
    raw_text: str
    role_title: str
    seniority: str
    must_have_skills: list[str]
    nice_to_have_skills: list[str]
    sector_keywords: list[str]
    soft_skills: list[str]
    tools_mentioned: list[str]

class DiscoveryQuestion(BaseModel):
    question_id: str
    category: str
    prompt: str
    options: list[str] | None
    user_answer: str | None

class GenerationRequest(BaseModel):
    master_resume: MasterResume
    jd: JobDescription
    answers: list[DiscoveryQuestion]
    format_prefs: FormatPrefs

class FormatPrefs(BaseModel):
    font: str = "Calibri"
    font_size_pt: float = 9.5
    page_count: int = 2
    use_colour: bool = False
    page_break_after_role: str | None = None

class GeneratedResume(BaseModel):
    docx_bytes: bytes
    md_text: str
    ats_score: float
    human_score: float
    keyword_coverage: dict[str, bool]
    suggestions: list[str]
    generation_cost_usd: float
```

## 12. Prompt strategy

### 12.1 System prompt (high level)
```
You are ResumeForge, an expert resume optimiser that has produced
100+ successful senior-PM resumes scoring ATS 94%+ and Human 90%+.

Rules:
- No AI slang ("translating probabilistic", "outcome-based", "leverage")
- Concrete verbs and specific numbers only
- 2-page Word doc, Calibri 9.5pt, black only
- 3 core skill blocks × strictly 2 lines each
- Hard page break after the most recent role's projects
- Achievement bullet on every project with real KPI numbers
- Mirror the target JD's exact keyword phrasing where factually true
```

### 12.2 Pipeline (4 LLM calls, streaming)
1. Parse JD → extract structured requirements
2. Generate 5 discovery questions → tuned to gaps
3. Synthesise tailored bullets → merge master + answers + JD
4. Score & critique → ATS + human pass

## 13. Scoring

### ATS score (0–100)
```
ATS = (
  0.40 × must_have_keyword_coverage +
  0.20 × nice_to_have_keyword_coverage +
  0.15 × tools_match +
  0.10 × sector_keyword_density +
  0.10 × section_completeness +
  0.05 × format_compliance
) × 100
```

### Human score (0–100)
```
Human = (
  0.25 × quantification_density +
  0.20 × concrete_verb_ratio +
  0.15 × ai_slang_absence +
  0.15 × seniority_signal_match +
  0.15 × narrative_coherence (LLM judge) +
  0.10 × visual_scanability
) × 100
```

Computed locally — deterministic heuristics + 1 LLM judge call.

## 14. POC milestones
| Week | Milestone |
|---|---|
| W1 | Repo setup, docx parser, JD parser, Streamlit shell |
| W2 | Gap analyser + 5-question discovery engine |
| W3 | Generation orchestrator + docx writer |
| W4 | ATS + Human scoring engine |
| W5 | End-to-end testing on 10 real resumes/JDs |
| W6 | Bug fixes, polish, demo-ready POC |

## 15. Risks & mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM hallucinates fake achievements | High | High | Strict "only use user answers + master resume" prompt; LLM judge verifies provenance |
| Docx breaks across Word/Docs | Medium | Medium | XML validation step; test on Word, Docs, LibreOffice in CI |
| API costs spike | Low | Medium | Token budget per generation; SQLite cache |
| Low-quality user answers | Medium | High | Fallback: skip Q's, flag in score report |
| 2-page overflow on long careers | Medium | Low | Auto-trim Additional Projects / Tools sections |

## 16. Roadmap
- **v0.2** — multi-profile + LinkedIn import
- **v0.3** — cover-letter generation tied to same JD
- **v0.4** — browser extension
- **v0.5** — recruiter mode
- **v1.0** — SaaS with billing

## 17. Appendix A — Sample JD-tuned discovery questions
**AI PM role**
- Q3 (Technical): *"What model evaluation framework did you use? Latency, cost, accuracy trade-offs?"*
- Q5 (Innovation): *"Did you launch any 0-to-1 GenAI capability? Pilot to scale numbers?"*

**Automotive retail PM role**
- Q4 (Discovery): *"Any dealer or OEM partner research? Direct customer interviews with dealership ops?"*
- Q1 (Impact): *"Vehicle inventory turn, dealer adoption rate, or sales-velocity improvements?"*

**Fintech / BFSI PM role**
- Q3 (Technical): *"Payment integration choices? Stripe vs Adyen vs in-house?"*
- Q5 (Innovation): *"Regulatory framework navigation — what compliance frameworks did you ship under?"*

## 18. Appendix B — Sample output provenance map
| Bullet in final resume | Source |
|---|---|
| "Scaled platform from 1,000 to 20,000 users in 3 months" | Q1 answer |
| "Selected GPT-4o via multi-criteria decision matrix" | Master resume + JD keyword "model selection" |
| "Closed $5M+ investment via full RFP cycle" | Master resume (unchanged) |
| "Collaborated with sales, marketing, and customer success on B2B GTM" | Q2 answer |

Provenance logged per bullet — debugs hallucinations, improves prompts.

## 19. Open questions
- LLM choice: Claude Opus (structured output + style) vs GPT-4o (cheaper, faster)?
- UI: Streamlit (fast POC) vs Next.js (better long-term UX)?
- Pricing model: per-generation credits, monthly subscription, or both?
- Privacy: ship a fully-local LLM option (Llama 3, Mistral) for cloud-averse users?

## 20. Success criteria for POC
- ✅ 10 real resume + JD pairs run end-to-end
- ✅ Average ATS ≥ 94%
- ✅ Average Human ≥ 90%
- ✅ Generation < 90 seconds
- ✅ Cost < $0.50 / generation
- ✅ Zero docx validation failures across 10 outputs
- ✅ 7/10 users prefer ResumeForge output over original in blind A/B
