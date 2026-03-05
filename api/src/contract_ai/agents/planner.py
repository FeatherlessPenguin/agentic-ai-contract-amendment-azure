from __future__ import annotations
from contract_ai.models import PlannerPlan


def plan(contract_text: str) -> PlannerPlan:
    # MVP stub — later this becomes an Azure OpenAI call
    clauses_detected = []
    lowered = contract_text.lower()
    if "liability" in lowered:
        clauses_detected.append("liability")
    if "dispute" in lowered or "governed by" in lowered:
        clauses_detected.append("dispute_resolution")
    if "ownership" in lowered or "intellectual property" in lowered:
        clauses_detected.append("ownership_ip")
    clauses_to_modify = list(set(clauses_detected + ["ai_disclosure"]))

    return PlannerPlan(
        contract_type="msa",
        clauses_detected=clauses_detected,
        clauses_to_modify=clauses_to_modify,
        jurisdictions=["ontario", "federal"],
        notes="Stub planner (LLM to be added)."
    )