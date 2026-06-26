from backend.app.services.gap_analyzer import analyze_gap
from backend.app.services.jd_parser import parse_job_description
from backend.app.services.apply_navigator import build_apply_navigation_plan
from backend.app.models import ApplyNavigationRequest, ApplyPackage, BrowserField, TailoredResume, ProvenanceItem, ProviderName
from backend.app.services.resume_context import parse_resume_context


def test_parse_resume_context_extracts_skills_and_metrics():
    resume = parse_resume_context("# Product Manager\nBuilt Agentic AI RAG platform. Reduced effort 60%.")
    assert "agentic ai" in resume.skills
    assert "rag" in resume.skills
    assert any("60%" in metric for metric in resume.metrics)


def test_parse_job_description_extracts_domain_terms():
    jd = parse_job_description("AI Product Manager needed for RAG, API, healthcare data platform.")
    assert "ai" in jd.domain_keywords
    assert "rag" in jd.domain_keywords
    assert "api" in jd.must_have


def test_gap_analysis_returns_missing_terms():
    resume = parse_resume_context("Product Manager with RAG experience.")
    jd = parse_job_description("AI Product Manager with RAG, Snowflake, API experience.")
    gap = analyze_gap(resume, jd)
    assert "rag" in gap.matched_keywords
    assert "snowflake" in gap.missing_keywords


def test_apply_navigation_blocks_submit_and_drafts_answers():
    jd = parse_job_description("AI Product Manager role.")
    tailored = TailoredResume(
        markdown="# Draft",
        summary="AI Product Manager with RAG and API experience.",
        skills=["RAG", "API"],
        bullets=[ProvenanceItem(output="Reduced effort by 60%.", sources=["resume_context"])],
        provider_used=ProviderName.deterministic,
    )
    package = ApplyPackage(
        recruiter_message="Interested in the role.",
        why_this_role="Strong fit for AI product work.",
        top_proof_points=["Reduced effort by 60%."],
        application_answers=["Strong fit for AI product work."],
        safety_note="Draft only.",
    )
    plan = build_apply_navigation_plan(
        ApplyNavigationRequest(
            job_description=jd,
            tailored_resume=tailored,
            apply_package=package,
            visible_fields=[BrowserField(field_id="why", label="Why are you interested in this role?")],
        )
    )
    assert plan.submit_allowed is False
    assert plan.field_drafts[0].suggested_value == "Strong fit for AI product work."
