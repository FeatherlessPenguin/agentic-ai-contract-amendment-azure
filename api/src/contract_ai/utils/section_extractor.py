from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Section:
    title: str
    body: str


SECTION_RE = re.compile(r"^\s*\d+\.\s+(.+?)\s*$", re.MULTILINE)


def extract_sections(contract_text: str) -> List[Section]:
    """
    Extracts numbered sections like:
    '3. Limitation of Liability'
    Returns sections with title + body.
    """
    matches = list(SECTION_RE.finditer(contract_text))
    if not matches:
        return [Section(title="Full Document", body=contract_text)]

    sections: List[Section] = []
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(contract_text)
        body = contract_text[start:end].strip()
        sections.append(Section(title=title, body=body))
    return sections


def sections_to_map(sections: List[Section]) -> Dict[str, str]:
    return {s.title: s.body for s in sections}