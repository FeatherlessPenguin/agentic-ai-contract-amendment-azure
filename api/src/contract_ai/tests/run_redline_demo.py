# api/src/tests/run_redline_demo.py
from pathlib import Path
from contract_ai.redline.diff_engine import generate_redline_html

original = """MASTER SERVICES AGREEMENT

3. Limitation of Liability
Except for gross negligence or willful misconduct, each party's liability is limited to fees paid in the preceding 12 months.
"""

amended = """MASTER SERVICES AGREEMENT

3. Limitation of Liability
Except for gross negligence or willful misconduct, each party's liability is limited to fees paid in the preceding 12 months.

8. Disclosure of Artificial Intelligence Use
Each party shall disclose any material use of AI systems in drafting or materially modifying this Agreement, including the use of AI to generate contractual language.
"""

out = generate_redline_html(original, amended)
Path("redline_demo.html").write_text(out.side_by_side_html, encoding="utf-8")
print("Wrote redline_demo.html — open it in your browser.")