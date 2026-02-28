# api/src/redline/diff_engine.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from html import escape
from typing import List, Tuple, Optional

from diff_match_patch import diff_match_patch


@dataclass
class RedlineResult:
    original_html: str
    amended_html: str
    side_by_side_html: str


def _diff_to_marked_html(diffs: List[Tuple[int, str]]) -> str:
    """
    Convert diff-match-patch diffs into safe HTML with <ins>/<del>.
    Operation codes:
      -1 = deletion, 0 = equal, 1 = insertion
    """
    parts: List[str] = []

    for op, text in diffs:
        safe = escape(text)

        # Preserve line breaks and spaces in HTML rendering
        safe = safe.replace("\n", "<br/>")
        safe = safe.replace("\t", "&nbsp;" * 4)
        safe = safe.replace("  ", "&nbsp;&nbsp;")

        if op == 0:
            parts.append(safe)
        elif op == 1:
            parts.append(f"<ins>{safe}</ins>")
        elif op == -1:
            parts.append(f"<del>{safe}</del>")
        else:
            parts.append(safe)

    return "".join(parts)


def generate_redline_html(
    original_text: str,
    amended_text: str,
    *,
    title_left: str = "Original",
    title_right: str = "Amended",
    context_cleanup: bool = True,
) -> RedlineResult:
    """
    Returns:
      - original_html: marked original with deletions highlighted
      - amended_html: marked amended with insertions highlighted
      - side_by_side_html: complete standalone HTML page (2 columns)
    """
    dmp = diff_match_patch()

    # Compute diffs
    diffs = dmp.diff_main(original_text, amended_text)

    # Clean up diffs to be more human-readable
    if context_cleanup:
        dmp.diff_cleanupSemantic(diffs)
        dmp.diff_cleanupEfficiency(diffs)

    # Build left/right marked views:
    # For the original view, show deletions (<del>) but hide insertions.
    # For the amended view, show insertions (<ins>) but hide deletions.
    diffs_for_left: List[Tuple[int, str]] = []
    diffs_for_right: List[Tuple[int, str]] = []

    for op, text in diffs:
        if op == 0:
            diffs_for_left.append((0, text))
            diffs_for_right.append((0, text))
        elif op == -1:
            diffs_for_left.append((-1, text))
            # deletion doesn't appear in amended
            # so omit from right
        elif op == 1:
            # insertion doesn't appear in original
            # so omit from left
            diffs_for_right.append((1, text))

    left_html = _diff_to_marked_html(diffs_for_left)
    right_html = _diff_to_marked_html(diffs_for_right)

    # Standalone HTML page (side-by-side)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Redline Comparison</title>
  <style>
    :root {{
      --border: #e5e7eb;
      --bg: #ffffff;
      --muted: #6b7280;
      --panel: #f9fafb;
    }}
    body {{
      margin: 0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
      background: var(--bg);
      color: #111827;
    }}
    header {{
      padding: 16px 20px;
      border-bottom: 1px solid var(--border);
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 10;
    }}
    header .title {{
      font-size: 16px;
      font-weight: 600;
      margin: 0;
    }}
    header .meta {{
      font-size: 12px;
      color: var(--muted);
      margin-top: 4px;
    }}
    .wrap {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      padding: 12px;
    }}
    .panel {{
      border: 1px solid var(--border);
      border-radius: 10px;
      overflow: hidden;
      background: #fff;
      display: flex;
      flex-direction: column;
      min-height: calc(100vh - 88px);
    }}
    .panel h2 {{
      margin: 0;
      padding: 10px 12px;
      font-size: 13px;
      font-weight: 600;
      border-bottom: 1px solid var(--border);
      background: var(--panel);
    }}
    .content {{
      padding: 12px;
      overflow: auto;
      font-size: 13px;
      line-height: 1.5;
      white-space: normal;
      word-wrap: break-word;
    }}
    /* Highlights */
    del {{
      background: #fee2e2;
      text-decoration: line-through;
      padding: 0 1px;
      border-radius: 3px;
    }}
    ins {{
      background: #dcfce7;
      text-decoration: none;
      padding: 0 1px;
      border-radius: 3px;
    }}
    /* Mobile */
    @media (max-width: 900px) {{
      .wrap {{
        grid-template-columns: 1fr;
      }}
      .panel {{
        min-height: auto;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="title">Contract Redline (Deterministic Diff)</div>
    <div class="meta">Generated {now}</div>
  </header>

  <main class="wrap">
    <section class="panel">
      <h2>{escape(title_left)}</h2>
      <div class="content">{left_html}</div>
    </section>
    <section class="panel">
      <h2>{escape(title_right)}</h2>
      <div class="content">{right_html}</div>
    </section>
  </main>
</body>
</html>
"""
    return RedlineResult(
        original_html=left_html,
        amended_html=right_html,
        side_by_side_html=page,
    )