from __future__ import annotations

from typing import List, Literal, Optional, Dict
from pydantic import BaseModel, Field


Jurisdiction = Literal["federal", "ontario"]


class DraftAmendmentRequest(BaseModel):
    contract_text: str = Field(..., min_length=1)
    province: Literal["ON"] = "ON"
    include_federal: bool = True
    amendment_goal: str = Field(
        default="Add an AI use disclosure requirement (hypothetical)."
    )


class PlannerPlan(BaseModel):
    contract_type: str = "unknown"
    clauses_detected: List[str] = Field(default_factory=list)
    clauses_to_modify: List[str] = Field(default_factory=list)
    jurisdictions: List[Jurisdiction] = Field(default_factory=lambda: ["ontario", "federal"])
    notes: Optional[str] = None


class LawSnippet(BaseModel):
    jurisdiction: Jurisdiction
    topic: str
    source_title: str
    source_url: Optional[str] = None
    text: str


class CompressedContext(BaseModel):
    topic: str
    jurisdiction_summary: Dict[Jurisdiction, str] = Field(default_factory=dict)


class ClausePatch(BaseModel):
    target_section: str
    new_text: str
    reason: str
    sources_used: List[str] = Field(default_factory=list)


class AgentOutput(BaseModel):
    agent_name: str
    patches: List[ClausePatch] = Field(default_factory=list)


class ReviewResult(BaseModel):
    patches: List[ClausePatch]
    inconsistencies_found: List[str] = Field(default_factory=list)
    definitions_added: List[str] = Field(default_factory=list)


class DraftAmendmentResponse(BaseModel):
    amended_text: str
    redline_html: str
    audit_trail: dict