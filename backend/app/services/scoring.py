from __future__ import annotations

from backend.app.models import JobDescription, ScoreReport, TailoredResume


AI_SLANG = {"leverage", "synergy", "cutting-edge", "game-changing", "seamless"}


def score_resume(jd: JobDescription, tailored: TailoredResume) -> ScoreReport:
    text = tailored.markdown.lower()
    jd_terms = set(jd.must_have + jd.tools + jd.domain_keywords)
    covered = [term for term in jd_terms if term.lower() in text]
    coverage = len(covered) / max(len(jd_terms), 1)
    ats_score = min(98, 70 + int(coverage * 28))
    slang_hits = [term for term in AI_SLANG if term in text]
    human_score = max(70, 92 - len(slang_hits) * 4)

    suggestions = []
    if coverage < 0.7:
        suggestions.append("Add more role-specific keywords where factually supported.")
    if not any(ch.isdigit() for ch in text):
        suggestions.append("Add measurable business outcomes from resume context.")
    suggestions.append("Validate each generated bullet against original evidence before applying.")

    return ScoreReport(
        ats_score=ats_score,
        human_score=human_score,
        keyword_coverage=round(coverage, 2),
        ai_slang_risk="medium" if slang_hits else "low",
        unsupported_claim_risk="low",
        suggestions=suggestions,
    )

