from __future__ import annotations
from contract_ai.models import AgentOutput, ClausePatch


def draft_ai_disclosure() -> AgentOutput:
    clause = """8. Disclosure of Artificial Intelligence Use
Each party shall disclose any material use of AI systems in drafting or materially modifying this Agreement, including the use of AI to generate contractual language. Where AI is used, the party shall ensure no Confidential Information is provided to external AI systems without prior written approval from the other party."""
    patch = ClausePatch(
        target_section="Disclosure of Artificial Intelligence Use",
        new_text=clause,
        reason="Add hypothetical AI disclosure requirement.",
        sources_used=["Hypothetical AI disclosure requirement (demo)"],
    )
    return AgentOutput(agent_name="ai_disclosure_agent", patches=[patch])