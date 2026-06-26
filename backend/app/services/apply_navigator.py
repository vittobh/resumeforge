from __future__ import annotations

from backend.app.models import ApplyNavigationPlan, ApplyNavigationRequest, FieldDraft


def _answer_for_label(label: str, request: ApplyNavigationRequest) -> tuple[str, str]:
    lowered = label.lower()
    package = request.apply_package
    resume = request.tailored_resume

    if "why" in lowered and ("role" in lowered or "company" in lowered or "join" in lowered):
        return package.why_this_role, "apply_package.why_this_role"
    if "cover" in lowered or "message" in lowered or "note" in lowered:
        return package.recruiter_message, "apply_package.recruiter_message"
    if "summary" in lowered or "profile" in lowered:
        return resume.summary, "tailored_resume.summary"
    if "skill" in lowered:
        return ", ".join(resume.skills[:12]), "tailored_resume.skills"
    if "experience" in lowered or "achievement" in lowered:
        return "\n".join(package.top_proof_points[:3]), "apply_package.top_proof_points"
    if "salary" in lowered or "compensation" in lowered:
        return "", "user_required.salary_preference"
    if "notice" in lowered or "availability" in lowered:
        return "", "user_required.availability"

    return package.application_answers[0] if package.application_answers else resume.summary, "apply_package.application_answers"


def build_apply_navigation_plan(request: ApplyNavigationRequest) -> ApplyNavigationPlan:
    drafts: list[FieldDraft] = []
    blocked: list[str] = [
        "Do not click final Submit/Apply until user explicitly confirms.",
        "Do not upload files until user confirms exact file.",
        "Do not send recruiter message until user confirms destination and text.",
    ]

    for field in request.visible_fields:
        value, source = _answer_for_label(field.label, request)
        requires_user = True
        if source.startswith("user_required"):
            value = ""
            blocked.append(f"Need user input for field: {field.label}")
        drafts.append(
            FieldDraft(
                field_id=field.field_id,
                label=field.label,
                suggested_value=value,
                source=source,
                confidence=0.86 if value else 0.0,
                requires_user_confirmation=requires_user,
            )
        )

    next_safe_step = "Review generated field drafts with user; fill only after confirmation."
    return ApplyNavigationPlan(
        field_drafts=drafts,
        blocked_actions=blocked,
        next_safe_step=next_safe_step,
        submit_allowed=False,
    )

