from __future__ import annotations
from typing import List

from contract_ai.models import ClausePatch, ReviewResult


def review(patches: List[ClausePatch]) -> ReviewResult:
    # MVP stub — later becomes LLM-based consistency checks
    inconsistencies = []
    return ReviewResult(patches=patches, inconsistencies_found=inconsistencies)