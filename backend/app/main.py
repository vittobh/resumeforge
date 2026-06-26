from __future__ import annotations

from fastapi import FastAPI

from backend.app.models import ApplyNavigationPlan, ApplyNavigationRequest, ResumeContext, TailorRequest, TailorResponse
from backend.app.services.apply_navigator import build_apply_navigation_plan
from backend.app.services.jd_parser import parse_job_description
from backend.app.services.meta_orchestrator import run_tailor_pipeline
from backend.app.services.resume_context import parse_resume_context

app = FastAPI(title="ResumeForge Backend", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "llm_policy": "deterministic-first, Groq only for final polish when enabled"}


@app.post("/context/parse-md", response_model=ResumeContext)
def parse_context(payload: dict[str, str]) -> ResumeContext:
    return parse_resume_context(payload.get("markdown", ""), source_type="markdown")


@app.post("/jobs/parse")
def parse_job(payload: dict[str, str]):
    return parse_job_description(
        raw_text=payload.get("raw_text", ""),
        title=payload.get("title"),
        company=payload.get("company"),
        location=payload.get("location"),
    )


@app.post("/tailor/generate", response_model=TailorResponse)
async def tailor_generate(request: TailorRequest) -> TailorResponse:
    return await run_tailor_pipeline(request)


@app.post("/apply/navigation-plan", response_model=ApplyNavigationPlan)
def apply_navigation_plan(request: ApplyNavigationRequest) -> ApplyNavigationPlan:
    return build_apply_navigation_plan(request)
