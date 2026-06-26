from __future__ import annotations

from backend.app.models import ApplyPackage, JobDescription, TailoredResume


def build_apply_package(jd: JobDescription, tailored: TailoredResume) -> ApplyPackage:
    proof_points = [item.output for item in tailored.bullets[:5]]
    company = jd.company or "your team"
    role = jd.title
    recruiter_message = (
        f"Hi, I am interested in the {role} role at {company}. "
        f"My background aligns with {', '.join(tailored.skills[:5])}. "
        "I have included a tailored resume and would welcome a conversation."
    )
    why_this_role = (
        f"This role matches my experience in {', '.join(tailored.skills[:6])}. "
        "I am especially interested in applying product strategy, AI/data platform thinking, and measurable delivery discipline to this opportunity."
    )
    return ApplyPackage(
        recruiter_message=recruiter_message,
        why_this_role=why_this_role,
        top_proof_points=proof_points,
        application_answers=[why_this_role, recruiter_message],
        safety_note="Draft only. User must confirm before filling, uploading, messaging, saving, or submitting on any external site.",
    )

