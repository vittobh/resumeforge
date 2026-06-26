from __future__ import annotations

from backend.app.models import GapAnalysis, JobDescription, ResumeContext


def analyze_gap(resume: ResumeContext, jd: JobDescription) -> GapAnalysis:
    resume_terms = {item.lower() for item in resume.skills}
    jd_terms = {item.lower() for item in jd.must_have + jd.tools + jd.domain_keywords}
    matched = sorted(resume_terms & jd_terms)
    missing = sorted(jd_terms - resume_terms)

    focus = []
    if "agentic" in jd_terms or "rag" in jd_terms:
        focus.append("Emphasize AI platform, RAG evaluation, tool calling, and governance proof.")
    if "healthcare" in jd_terms:
        focus.append("Highlight FHIR, HL7, HIPAA-aware workflow, and healthcare data products.")
    if "bfsi" in jd_terms or "kyc" in jd_terms:
        focus.append("Highlight BFSI workflows, KYC/AML, reconciliation, and risk controls.")
    if not focus:
        focus.append("Emphasize product strategy, roadmap ownership, stakeholder alignment, and measurable outcomes.")

    return GapAnalysis(
        matched_keywords=matched,
        missing_keywords=missing[:20],
        recommended_focus=focus,
        strongest_roles=resume.roles[:5],
    )

