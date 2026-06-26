from __future__ import annotations

from backend.app.models import TailorRequest, TailorResponse
from backend.app.services.apply_package import build_apply_package
from backend.app.services.discovery_engine import build_discovery_questions
from backend.app.services.gap_analyzer import analyze_gap
from backend.app.services.resume_generator import generate_resume
from backend.app.services.scoring import score_resume


async def run_tailor_pipeline(request: TailorRequest) -> TailorResponse:
    """Meta-agent style orchestration without heavy CrewAI/LangChain dependency.

    This keeps the MVP small and reusable. Each service maps to an agent role:
    gap agent, discovery agent, writer agent, critic agent, apply package agent.
    """

    gap = analyze_gap(request.resume_context, request.job_description)
    questions = build_discovery_questions(request.job_description, gap)
    tailored = await generate_resume(
        request.resume_context,
        gap,
        request.preferences,
        request.discovery_answers,
        allow_llm_final_polish=request.allow_llm_final_polish,
    )
    score = score_resume(request.job_description, tailored)
    apply_package = build_apply_package(request.job_description, tailored)
    return TailorResponse(
        gap_analysis=gap,
        discovery_questions=questions,
        tailored_resume=tailored,
        score=score,
        apply_package=apply_package,
    )

