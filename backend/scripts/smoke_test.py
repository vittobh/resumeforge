from __future__ import annotations

import asyncio
import json
from pathlib import Path

from backend.app.models import PreferenceProfile, TailorRequest
from backend.app.services.jd_parser import parse_job_description
from backend.app.services.meta_orchestrator import run_tailor_pipeline
from backend.app.services.resume_context import parse_resume_context


async def main() -> None:
    root = Path(__file__).resolve().parents[1]
    resume_md = (root / "data" / "sample_resume_context.md").read_text()
    job_payload = json.loads((root / "data" / "sample_linkedin_job.json").read_text())

    resume = parse_resume_context(resume_md)
    job = parse_job_description(**job_payload)
    request = TailorRequest(
        resume_context=resume,
        job_description=job,
        preferences=PreferenceProfile(domain_emphasis=["Agentic AI", "RAG", "Enterprise SaaS"]),
        discovery_answers={"Q1": "Reduced manual effort by 50-80% through workflow automation."},
        allow_llm_final_polish=False,
    )
    result = await run_tailor_pipeline(request)
    print(json.dumps(result.model_dump(), indent=2))


if __name__ == "__main__":
    asyncio.run(main())

