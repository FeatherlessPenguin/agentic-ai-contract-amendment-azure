# api/src/tests/test_redline.py
from contract_ai.redline.diff_engine import generate_redline_html


def test_redline_generates_html():
    original = "Hello world.\nLiability is capped at $10,000.\n"
    amended = "Hello world!\nLiability is capped at $25,000.\nAI use must be disclosed.\n"

    result = generate_redline_html(original, amended)

    assert "<del>" in result.side_by_side_html or "<ins>" in result.side_by_side_html
    assert "Contract Redline" in result.side_by_side_html
    assert "Liability" in result.side_by_side_html