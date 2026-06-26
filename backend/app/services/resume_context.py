from __future__ import annotations

import re

from backend.app.models import ResumeContext


SKILL_HINTS = {
    "agentic ai",
    "rag",
    "langgraph",
    "mcp",
    "product strategy",
    "roadmap",
    "prd",
    "brd",
    "api",
    "snowflake",
    "healthcare",
    "bfsi",
    "fhir",
    "hl7",
    "salesforce",
}


def parse_resume_context(raw_text: str, source_type: str = "markdown") -> ResumeContext:
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    headings = [line.lstrip("# ").strip() for line in lines if line.startswith("#")]
    metrics = [
        line.lstrip("- ").strip()
        for line in lines
        if re.search(r"\d", line) and re.search(r"%|\+|x|X|\$|years?|months?|releases?|stories?|wireframes?", line, re.I)
    ]
    links = re.findall(r"https?://[^\s)]+", raw_text)

    lowered = raw_text.lower()
    skills = sorted({skill for skill in SKILL_HINTS if skill in lowered})

    roles = [h for h in headings if any(token in h.lower() for token in ["manager", "owner", "consultant", "leader", "analyst"])]
    projects = [h for h in headings if any(token in h.lower() for token in ["project", "platform", "product", "ai", "data"])]

    return ResumeContext(
        source_type=source_type,
        raw_text=raw_text,
        roles=roles[:12],
        projects=projects[:12],
        skills=skills,
        metrics=metrics[:40],
        links=links[:20],
    )
