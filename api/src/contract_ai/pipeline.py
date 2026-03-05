from __future__ import annotations

from contract_ai.agents import planner
from contract_ai.agents.ai_disclosure_agent import draft_ai_disclosure
from contract_ai.agents.reviewer import review
from contract_ai.models import DraftAmendmentRequest, DraftAmendmentResponse
from contract_ai.patching.patch_apply import apply_patches
from contract_ai.redline.diff_engine import generate_redline_html


def run_pipeline(req: DraftAmendmentRequest) -> DraftAmendmentResponse:
    plan = planner.plan(req.contract_text)

    # For now: just AI disclosure patch to prove the full loop
    agent_outputs = [draft_ai_disclosure()]

    patches = []
    for out in agent_outputs:
        patches.extend(out.patches)

    review_result = review(patches)
    amended_text = apply_patches(req.contract_text, review_result.patches)
    redline = generate_redline_html(req.contract_text, amended_text)

    audit = {
        "planner_plan": plan.model_dump(),
        "agent_outputs": [o.model_dump() for o in agent_outputs],
        "review_result": review_result.model_dump(),
    }

    return DraftAmendmentResponse(
        amended_text=amended_text,
        redline_html=redline.side_by_side_html,
        audit_trail=audit,
    )