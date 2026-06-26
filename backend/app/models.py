from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ProviderName(str, Enum):
    deterministic = "deterministic"
    groq = "groq"


class PreferenceProfile(BaseModel):
    target_track: str = "AI Product Manager"
    tone: str = "technical product"
    resume_length: str = "2 pages"
    keyword_aggression: Literal["light", "balanced", "high"] = "balanced"
    domain_emphasis: list[str] = Field(default_factory=list)
    location_preference: str | None = None


class ResumeContext(BaseModel):
    source_type: Literal["markdown", "text"] = "markdown"
    raw_text: str
    roles: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    links: list[str] = Field(default_factory=list)


class JobDescription(BaseModel):
    raw_text: str
    title: str = "Unknown role"
    company: str | None = None
    location: str | None = None
    seniority: str | None = None
    must_have: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    domain_keywords: list[str] = Field(default_factory=list)


class GapAnalysis(BaseModel):
    matched_keywords: list[str]
    missing_keywords: list[str]
    recommended_focus: list[str]
    strongest_roles: list[str]


class DiscoveryQuestion(BaseModel):
    question_id: str
    category: str
    prompt: str


class ProvenanceItem(BaseModel):
    output: str
    sources: list[str]
    confidence: float = 0.8
    unsupported_claim: bool = False


class TailoredResume(BaseModel):
    markdown: str
    summary: str
    skills: list[str]
    bullets: list[ProvenanceItem]
    provider_used: ProviderName
    llm_used_for_final_polish: bool = False


class ScoreReport(BaseModel):
    ats_score: int
    human_score: int
    keyword_coverage: float
    ai_slang_risk: Literal["low", "medium", "high"]
    unsupported_claim_risk: Literal["low", "medium", "high"]
    suggestions: list[str]


class ApplyPackage(BaseModel):
    recruiter_message: str
    why_this_role: str
    top_proof_points: list[str]
    application_answers: list[str]
    safety_note: str


class BrowserField(BaseModel):
    field_id: str
    label: str
    field_type: str = "text"
    required: bool = False
    current_value: str | None = None


class FieldDraft(BaseModel):
    field_id: str
    label: str
    suggested_value: str
    source: str
    confidence: float = 0.75
    requires_user_confirmation: bool = True


class ApplyNavigationRequest(BaseModel):
    job_description: JobDescription
    tailored_resume: TailoredResume
    apply_package: ApplyPackage
    visible_fields: list[BrowserField]


class ApplyNavigationPlan(BaseModel):
    field_drafts: list[FieldDraft]
    blocked_actions: list[str]
    next_safe_step: str
    submit_allowed: bool = False


class TailorRequest(BaseModel):
    resume_context: ResumeContext
    job_description: JobDescription
    preferences: PreferenceProfile = Field(default_factory=PreferenceProfile)
    discovery_answers: dict[str, str] = Field(default_factory=dict)
    allow_llm_final_polish: bool = False


class TailorResponse(BaseModel):
    gap_analysis: GapAnalysis
    discovery_questions: list[DiscoveryQuestion]
    tailored_resume: TailoredResume
    score: ScoreReport
    apply_package: ApplyPackage
