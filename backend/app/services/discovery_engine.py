from __future__ import annotations

from backend.app.models import DiscoveryQuestion, GapAnalysis, JobDescription


def build_discovery_questions(jd: JobDescription, gap: GapAnalysis) -> list[DiscoveryQuestion]:
    role = jd.title
    missing = ", ".join(gap.missing_keywords[:6]) or "role-specific requirements"
    return [
        DiscoveryQuestion(question_id="Q1", category="Business Impact", prompt=f"What measurable business impact can prove fit for {role}? Include revenue, adoption, cost, speed, CSAT, or accuracy."),
        DiscoveryQuestion(question_id="Q2", category="Leadership", prompt="What team size, stakeholder seniority, vendor ownership, or cross-functional scope should be shown?"),
        DiscoveryQuestion(question_id="Q3", category="Technical Depth", prompt=f"What technical decisions map to these gaps: {missing}? Mention APIs, data, AI architecture, or platform trade-offs."),
        DiscoveryQuestion(question_id="Q4", category="Discovery", prompt="What customer/user research, interviews, experiments, UAT, or validation evidence should be included?"),
        DiscoveryQuestion(question_id="Q5", category="Transformation", prompt="What 0-to-1 launch, migration, automation, operating model, or process transformation proves seniority?"),
    ]

