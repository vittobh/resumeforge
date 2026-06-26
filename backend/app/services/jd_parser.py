from __future__ import annotations

import re

from backend.app.models import JobDescription


TOOLS = [
    "python",
    "sql",
    "snowflake",
    "salesforce",
    "aws",
    "azure",
    "gcp",
    "jira",
    "confluence",
    "figma",
    "tableau",
    "power bi",
    "langchain",
    "langgraph",
    "openai",
    "gemini",
    "groq",
]

DOMAINS = [
    "ai",
    "agentic",
    "rag",
    "healthcare",
    "bfsi",
    "fintech",
    "insurance",
    "saas",
    "data",
    "platform",
    "api",
    "compliance",
    "kyc",
    "aml",
]


def _keywords(text: str, vocabulary: list[str]) -> list[str]:
    lowered = text.lower()
    return sorted({term for term in vocabulary if term in lowered})


def parse_job_description(raw_text: str, title: str | None = None, company: str | None = None, location: str | None = None) -> JobDescription:
    first_line = next((line.strip() for line in raw_text.splitlines() if line.strip()), "")
    inferred_title = title or first_line[:90] or "Unknown role"
    seniority = "senior" if re.search(r"\bsenior|lead|principal|staff\b", raw_text, re.I) else None

    must_have = _keywords(
        raw_text,
        [
            "product management",
            "roadmap",
            "stakeholder",
            "user stories",
            "prd",
            "analytics",
            "experimentation",
            "api",
            "agile",
            "scrum",
            "data",
            "ai",
            "rag",
            "agentic",
        ],
    )

    return JobDescription(
        raw_text=raw_text,
        title=inferred_title,
        company=company,
        location=location,
        seniority=seniority,
        must_have=must_have,
        nice_to_have=[],
        tools=_keywords(raw_text, TOOLS),
        domain_keywords=_keywords(raw_text, DOMAINS),
    )

