from __future__ import annotations
from typing import List

from contract_ai.models import ClausePatch
from contract_ai.utils.section_extractor import extract_sections, Section


def apply_patches(original_text: str, patches: List[ClausePatch]) -> str:
    sections = extract_sections(original_text)
    patch_map = {p.target_section: p for p in patches}

    out_lines = []
    # Reconstruct with the same numbering headers if present
    # We assume headers existed; if not, treat as full doc.
    if len(sections) == 1 and sections[0].title == "Full Document":
        # naive: append patch text at end
        amended = original_text.strip()
        for p in patches:
            amended += "\n\n" + p.new_text.strip()
        return amended + "\n"

    # For numbered headers, re-render as "n. Title"
    # We'll keep original numbering by walking sections and incrementing.
    for idx, sec in enumerate(sections, start=1):
        header = f"{idx}. {sec.title}"
        if sec.title in patch_map:
            out_lines.append(header)
            out_lines.append(patch_map[sec.title].new_text.strip())
        else:
            out_lines.append(header)
            out_lines.append(sec.body.strip())

        out_lines.append("")  # blank line between sections

    # Add patches targeting non-existing sections at end
    for p in patches:
        if p.target_section not in {s.title for s in sections}:
            out_lines.append(p.new_text.strip())
            out_lines.append("")

    return "\n".join(out_lines).strip() + "\n"