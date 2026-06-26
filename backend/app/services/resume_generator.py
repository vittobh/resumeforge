from __future__ import annotations

from backend.app.models import GapAnalysis, PreferenceProfile, ProvenanceItem, ResumeContext, TailoredResume
from backend.app.services.llm_provider import LlmProvider


def _pick_metrics(resume: ResumeContext) -> list[str]:
    return [metric.strip().rstrip(".") for metric in resume.metrics if any(ch.isdigit() for ch in metric)][:5]


async def generate_resume(
    resume: ResumeContext,
    gap: GapAnalysis,
    preferences: PreferenceProfile,
    answers: dict[str, str],
    allow_llm_final_polish: bool = False,
) -> TailoredResume:
    metrics = _pick_metrics(resume)
    skills = sorted(set(resume.skills + gap.matched_keywords + preferences.domain_emphasis))[:18]
    summary = (
        f"{preferences.target_track} with experience across {', '.join(skills[:5]) or 'product strategy, data products, and enterprise platforms'}. "
        f"Focus: {', '.join(gap.recommended_focus)}"
    )

    bullet_texts = [
        f"Owned roadmap and delivery for {preferences.target_track.lower()} initiatives, aligning stakeholder needs with measurable product outcomes.",
        f"Translated JD priorities into role-specific proof points across {', '.join(skills[:6]) or 'product, data, and AI workflows'}.",
        f"Strengthened application narrative with grounded evidence from resume context and discovery answers.",
    ]
    if metrics:
        bullet_texts.insert(0, f"Delivered measurable outcomes: {'; '.join(metrics[:3])}.")
    for qid, answer in list(answers.items())[:3]:
        if answer.strip():
            bullet_texts.append(f"{answer.strip()}")

    bullets = [ProvenanceItem(output=text, sources=["resume_context", "gap_analysis"], confidence=0.82) for text in bullet_texts[:7]]
    markdown = "\n".join([
        f"# Tailored Resume Draft: {preferences.target_track}",
        "",
        "## Summary",
        summary,
        "",
        "## Core Skills",
        ", ".join(skills),
        "",
        "## Selected Bullets",
        *[f"- {item.output}" for item in bullets],
    ])

    provider_used = "deterministic"
    llm_used = False
    if allow_llm_final_polish:
        markdown, provider_used, llm_used = await LlmProvider().final_polish(markdown)

    return TailoredResume(
        markdown=markdown,
        summary=summary,
        skills=skills,
        bullets=bullets,
        provider_used=provider_used,
        llm_used_for_final_polish=llm_used,
    )
