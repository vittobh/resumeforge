# ResumeForge MVP PRD

## 1. Product Summary

ResumeForge is an AI job-application copilot that turns a master resume and target job description into a tailored, ATS-friendly, human-readable application package.

The MVP differentiator is not generic rewriting. It is a 5-question discovery loop that extracts missing context before generation:

- business impact
- leadership scope
- technical trade-offs
- customer discovery
- innovation / transformation

This solves the core problem in job-search AI tools: most resume tools optimize what is already written, but the strongest evidence often lives in the candidate's memory. ResumeForge also reduces cycle time across the full application path: browse job, capture JD, customize resume context, generate apply package, navigate application flow, and stop before final user-approved submission.

## 2. MVP Objective

Build a web MVP that proves candidates can create a stronger role-specific application package in under 10 minutes and reduce manual application preparation time by 70% by combining:

1. LinkedIn job capture from user's browser
2. master resume upload or Markdown career context
3. preference-based tailoring
4. JD parsing
5. gap analysis
6. five discovery questions
7. tailored bullet generation
8. ATS + human score review
9. exportable resume draft
10. apply-ready snippets
11. guided browser navigation until final save/submit gate

## 3. Target User

Primary:

- mid-career to senior product managers
- AI product managers
- data product managers
- enterprise SaaS product owners
- candidates applying to 5-20 roles in a search cycle

Secondary:

- career coaches
- resume writers
- job seekers in technical, data, consulting, healthcare, BFSI, and SaaS roles

## 4. Problem Statement

Candidates know their strongest work, but their resume often misses:

- quantified impact
- scale of ownership
- stakeholder complexity
- technical decision-making
- discovery and validation rigor
- role-specific vocabulary

Existing SaaS tools help with templates, ATS keywords, match scores, bullet rewriting, and job tracking. They rarely force the candidate to recover missing context before generation.

## 5. Market Scan

| Competitor | Category | What They Do | Observed Gap For ResumeForge |
|---|---|---|---|
| Teal | AI resume builder + job tracker | Resume builder, job matching, ATS score, keyword scanner, AI bullet/summary generation, multiple resume versions | Strong job-search suite, but differentiation is workflow breadth. ResumeForge can win on deep discovery, provenance, and role-specific evidence extraction. |
| Rezi | AI resume builder | AI keyword targeting, ATS-friendly resume creation, cover letters, resume optimization against job descriptions | Strong ATS and keyword story. ResumeForge should avoid keyword-stuffing positioning and emphasize grounded content + user-supplied proof. |
| Jobscan | ATS scanner + job-search platform | Resume scanner, match-rate report, ATS-specific recommendations, LinkedIn optimization, job tracker, AI Optimize | Strong scoring and ATS credibility. ResumeForge can complement/compete by creating better source content before scoring. |
| Kickresume | AI resume / cover letter builder | GPT-powered resume writer, templates, ATS compatibility, cover letters, website builder | Strong design/templates. ResumeForge should not compete primarily on visual templates in MVP. |
| Enhancv | AI resume builder | ChatGPT-powered resume writing, templates, resume sections, resume examples | Strong resume building UX. ResumeForge should compete on discovery-first PM/technical resume intelligence. |
| Resume Worded | Resume + LinkedIn feedback | Instant resume and LinkedIn feedback, scoring, career profile optimization | Strong feedback engine. ResumeForge should add generation with provenance and source traceability. |
| SkillSyncer | ATS keyword scanner | Compares resume to JD, identifies missing skills/keywords, auto-optimizes job-specific keywords | Strong keyword-gap utility. ResumeForge should focus on truthful skill evidence and anti-hallucination controls. |
| Careerflow | Career copilot / job-search suite | AI resume builder, ATS-friendly scoring, job-specific keywords, job fit analyzer, broader job search workflow | Strong all-in-one positioning. ResumeForge MVP should stay narrow and excellent before expanding to suite. |
| Career.io | Job-search suite | Resume optimization, job tracker, interview prep, recommendations, career tools | Broad career platform. ResumeForge can differentiate as a focused resume tailoring engine for product/AI/data roles. |

## 5.1 Top 5 Must-Have Features By RICE

RICE assumptions:

- Reach = number of users / sessions affected in MVP.
- Impact = expected lift in resume quality and apply success confidence.
- Confidence = evidence strength from competitor scan, public GitHub patterns, and observed job-seeker workflow.
- Effort = relative build effort for MVP.

| Rank | Feature | Reach | Impact | Confidence | Effort | RICE | Why Must-Have |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | Markdown Resume Context Vault | 9 | 9 | 8 | 3 | 216 | Creates a reusable source of truth for roles, metrics, skills, projects, and portfolio links. Public GitHub tools often stop at upload + rewrite; Markdown context makes ResumeForge versionable, auditable, and agent-friendly. |
| 2 | LinkedIn Job Capture + JD Parser | 9 | 8 | 8 | 4 | 144 | LinkedIn is the primary job discovery surface for target users. MVP should let user open a LinkedIn job, then ResumeForge extracts visible title, company, location, and JD into structured requirements. |
| 3 | Preference-Based Tailoring Engine | 8 | 8 | 7 | 3 | 149 | User chooses target track, tone, role level, domain focus, section emphasis, and keyword aggressiveness. Competitors optimize broadly; ResumeForge should tailor like a forward-deployed AI PM assistant. |
| 4 | Guided Apply Navigator | 9 | 9 | 7 | 5 | 113 | Main time-saver. Agent helps browse the job page, identify form fields, prepare answers, upload/copy resume content when approved, and stop before final submit. This turns ResumeForge from resume builder into application copilot. |
| 5 | Five-Question Discovery + Provenance | 8 | 9 | 8 | 5 | 115 | Core trust differentiator. Extracts missing evidence before writing, then maps bullets back to resume context, JD, or answer source. Avoids generic AI wording and hallucinated claims. |

### RICE Decision

MVP must build the smallest path that proves these five features work together:

```text
LinkedIn JD capture -> Markdown resume context -> preferences -> discovery questions -> tailored resume with provenance -> guided apply package.
```

Do not start with Naukri. Naukri is important for India hiring, but it should be Phase 1 after LinkedIn-first MVP proves the agent workflow.

### Public Strategy Signals Reused

Public GitHub repos commonly implement:

- resume upload
- ATS score
- keyword matching
- PDF/Docx export
- JD comparison
- Streamlit/Flask frontends

ResumeForge should reuse the strategy, not copy code:

- use simple upload/paste flows from open-source resume builders
- use deterministic keyword coverage before LLM scoring
- use Markdown as durable context storage
- use provenance mapping as differentiator
- keep save/submit behind user confirmation

Competitor strategy reuse:

- From Teal/Careerflow: job-search workflow and job-specific versions
- From Rezi/SkillSyncer: ATS keyword targeting
- From Jobscan/Resume Worded: scoring and feedback
- From Kickresume/Enhancv: clean generated output and readable resume sections

ResumeForge wedge:

```text
Discovery-first + provenance-first resume tailoring for AI/Product/Data roles.
```

## 6. Strategic Positioning

### Positioning Statement

ResumeForge is a discovery-first AI resume tailoring tool for product, AI, and data professionals who need role-specific resumes grounded in real evidence, not generic AI rewrites.

### Why Now

- AI resume tools are mainstream.
- ATS matching is commoditized.
- Job seekers use ChatGPT manually but lack structure, scoring, provenance, and formatting.
- Recruiters increasingly detect generic AI writing.
- Differentiation moves from "AI can write" to "AI can extract better evidence and prove it is grounded."

## 7. MVP Scope

### In Scope

- LinkedIn-first job capture from user's active Chrome session
- Upload master resume as `.docx`, `.md`, or pasted text
- Maintain Markdown career context as reusable source of truth
- Paste target job description as fallback
- Capture application preferences:
  - target track
  - tone
  - role level
  - domain focus
  - keyword aggressiveness
  - preferred resume length
  - location / remote preference
- Parse JD into:
  - title
  - seniority
  - must-have skills
  - nice-to-have skills
  - tools
  - domain keywords
- Parse resume into:
  - summary
  - skills
  - experience
  - projects
  - education
  - certifications
- Generate 5 discovery questions based on JD gaps
- Accept free-text answers
- Generate:
  - updated professional summary
  - prioritized skills block
  - 3-5 tailored bullets per relevant role
  - optional project section
- Show provenance:
  - master resume
  - JD keyword
  - discovery answer
  - model inference
- Show scores:
  - ATS keyword coverage
  - human quality score
  - quantification density
  - AI-slang risk
  - unsupported-claim risk
- Export:
  - Markdown preview
  - `.docx` in later MVP increment
- Generate apply-ready package:
  - recruiter note
  - LinkedIn message
  - "why this role" answer
  - top proof points
  - application field answer drafts
- Guided browser navigation:
  - observe page
  - identify fields
  - prepare draft answers
  - fill only after user approval
  - stop before final submit

### Out Of Scope

- Unattended auto-apply
- bypassing LinkedIn/Naukri login, CAPTCHA, or platform restrictions
- Naukri/LinkedIn profile editing
- Multi-user collaboration
- Billing
- Recruiter CRM
- Full job tracker
- Interview prep
- Cover letter generation

## 8. MVP User Journey

1. User opens target LinkedIn job in Chrome.
2. ResumeForge reads visible job content from user's session.
3. User loads Markdown career context or uploads master resume.
4. User chooses preference profile.
5. System parses JD and resume context.
6. System shows gap summary.
7. System asks 5 high-leverage discovery questions.
8. User answers in free text.
9. System generates tailored resume draft.
10. System generates apply-ready snippets.
11. User sees ATS/Human scores and provenance.
12. User edits draft if needed.
13. System navigates application fields and prepares answers.
14. User confirms before save, upload, message, or submit.
15. User exports Markdown or `.docx`.

## 9. Functional Requirements

### FR-1 Resume Context Ingestion

System must accept resume input through:

- Markdown career context
- file upload
- pasted text fallback
- sample resume for demo mode

Acceptance criteria:

- User can load `.md` resume context.
- User can upload a resume or use sample data.
- Parsed sections display in preview.
- If parsing fails, system gives readable error and pasted-text fallback.

### FR-2 LinkedIn Job Capture

System must read visible LinkedIn job content from the user's authenticated browser session.

Acceptance criteria:

- User opens a LinkedIn job page manually.
- System captures job title, company, location, and JD.
- System does not inspect cookies, passwords, or hidden session data.
- System falls back to pasted JD if page capture fails.

### FR-3 JD Parsing

System must extract role requirements from raw JD text.

Acceptance criteria:

- User can paste JD and click `Parse JD`.
- System shows top keywords, must-haves, seniority, tools, and domain.
- Empty JD blocks generation.

### FR-4 Guided Apply Navigator

System must reduce custom-application time by helping navigate application forms and prepare field-specific answers.

Acceptance criteria:

- System observes page and lists detected application fields.
- System maps each field to a draft answer from resume context, JD, and preferences.
- System asks before filling external application fields.
- System always stops before final submit.
- System verifies filled values where user approved fill.

### FR-3 Gap Analysis

System compares resume content to JD.

Acceptance criteria:

- System shows top missing keywords.
- System shows weak sections.
- System recommends which experience/project should be emphasized.

### FR-4 Discovery Loop

System generates 5 questions.

Acceptance criteria:

- Exactly 5 questions render after JD parse.
- Questions map to impact, leadership, technical depth, discovery, innovation.
- User can answer each question.
- Generation blocks if fewer than 3 answers exist.

### FR-5 Resume Generation

System generates tailored resume content.

Acceptance criteria:

- Output includes summary, skill blocks, bullets, and optional project section.
- Bullets use measurable action-result format.
- Unsupported claims are flagged.
- AI-slang phrases are minimized.

### FR-6 Provenance Map

System shows source for each generated bullet.

Acceptance criteria:

- Each bullet maps to one or more sources:
  - resume
  - JD
  - discovery answer
  - model inference
- Unsupported bullets show warning.

### FR-7 Score Report

System scores output.

Acceptance criteria:

- ATS score shows keyword coverage.
- Human score shows clarity, specificity, metrics, relevance.
- User gets 3 concrete improvement suggestions.

### FR-8 Export

System supports export.

Acceptance criteria:

- MVP supports Markdown copy/download.
- `.docx` export added after formatting validation.

## 10. Non-Functional Requirements

| Category | Requirement |
|---|---|
| Speed | End-to-end generation under 90 seconds |
| Privacy | No resume data stored by default |
| Cost | Target under $0.50 per generation |
| Quality | ATS score target >= 90, human score target >= 85 |
| Trust | No ungrounded metric fabrication |
| Accessibility | Keyboard navigable core flow |
| Browser | Works on Chrome desktop first |

## 11. Data Model

```json
{
  "resume": {
    "raw_text": "string",
    "sections": {
      "summary": "string",
      "skills": ["string"],
      "experience": ["object"],
      "projects": ["object"]
    }
  },
  "job_description": {
    "raw_text": "string",
    "title": "string",
    "seniority": "string",
    "must_have": ["string"],
    "nice_to_have": ["string"],
    "tools": ["string"],
    "domain_keywords": ["string"]
  },
  "discovery_answers": [
    {
      "question_id": "Q1",
      "category": "Business Impact",
      "answer": "string"
    }
  ],
  "generated_resume": {
    "summary": "string",
    "skills": ["string"],
    "bullets": [
      {
        "text": "string",
        "sources": ["resume", "jd", "Q1"],
        "confidence": 0.9,
        "unsupported_claim": false
      }
    ],
    "scores": {
      "ats": 92,
      "human": 88,
      "ai_slang_risk": "low"
    }
  }
}
```

## 12. Key MVP Screens

1. Landing / value proposition
2. Resume upload
3. JD paste + parser result
4. Gap analysis summary
5. Discovery questions
6. Generated resume draft
7. ATS + human score report
8. Provenance map
9. Export panel

## 13. Differentiation

ResumeForge should not claim to be the broadest job-search platform.

It should win on:

- discovery-first evidence extraction
- provenance per generated bullet
- anti-hallucination controls
- quantified PM/AI/data resume writing
- recruiter-readable, not AI-fluffy, output
- honest score and improvement loop

## 14. MVP Metrics

| Metric | Target |
|---|---|
| Time to first tailored draft | < 10 minutes |
| Generation time | < 90 seconds |
| User answers completed | >= 4 / 5 |
| ATS score lift | +15 points vs baseline |
| Human score lift | +20 points vs baseline |
| Unsupported bullet rate | < 5% |
| User keeps generated bullets | >= 60% |
| Export completion | >= 70% |

## 15. Pricing Hypothesis

MVP can test:

- Free: 3 generations / month, Markdown export, basic score
- Pro: $9-15 / month, unlimited generations, `.docx`, saved versions
- Coach: $29-49 / month, multi-client workspace, notes, export history

Do not build billing in MVP. Validate willingness through waitlist and manual payment interest.

## 16. Roadmap

### Phase 0: Current Prototype

- Static UI
- Mock parse
- Mock scores
- Mock generated bullets
- Browser skill docs

### Phase 1: MVP

- Real parsing for pasted text / Markdown
- JD keyword extraction
- Discovery questions
- LLM generation
- Markdown export
- Score + provenance map

### Phase 2: Trust Layer

- `.docx` export
- unsupported-claim detector
- factual consistency check
- version history
- promptfoo regression tests

### Phase 3: SaaS

- login
- saved resumes
- JD history
- Stripe billing
- private workspace
- analytics

### Phase 4: Expansion

- cover letters
- LinkedIn/Naukri profile summary generation
- Chrome extension
- interview prep
- job tracker

## 17. Risks

| Risk | Mitigation |
|---|---|
| Generic AI output | Force discovery answers and provenance |
| Fabricated metrics | Require source-backed numbers, flag unsupported claims |
| ATS over-optimization | Cap keyword density and optimize human score too |
| Privacy concern | Local-first mode, no default server persistence |
| Crowded market | Narrow positioning: PM/AI/data role evidence extraction |
| Export quality | Validate `.docx` XML before download |

## 18. Open Questions

- Should MVP focus only on Product Manager resumes first?
- Should `.docx` be in MVP or Phase 2?
- Should output be 1-page, 2-page, or configurable?
- Should users be able to maintain a career evidence vault?
- Should scoring use deterministic rules first or LLM judge first?

## 19. Source Notes

Market observations were checked against public product pages:

- Teal describes AI resume building, job matching, job-description-based match score, keyword scanner, ATS checker, job tracker, and unlimited resume versions.
- Rezi describes AI keyword targeting, ATS-friendly optimization, job-description-based resume tailoring, and cover letters.
- Jobscan positions around ATS-specific scanning, match-rate reports, AI Optimize, LinkedIn optimization, job tracker, and auto-apply with review.
- Kickresume positions around GPT-powered resume writing, templates, ATS compatibility, cover letters, and portfolio website creation.
- SkillSyncer focuses on comparing resume to job descriptions and identifying missing skills/keywords.
- Careerflow positions as broader career copilot with AI resume builder, ATS score, keyword improvements, and job fit analyzer.
