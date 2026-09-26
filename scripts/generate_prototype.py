from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from fintech_sim import generate_prototype, validate_prototype  # noqa: E402


def main() -> int:
    manifest = generate_prototype(PROJECT_ROOT)
    validation = validate_prototype(PROJECT_ROOT, write_report=True)
    print(f"Generated {manifest['row_counts']['transfers']:,} synthetic transfers.")
    print(f"Validation status: {'PASS' if validation['all_passed'] else 'FAIL'}")
    print(f"Report: {validation['report_path']}")
    return 0 if validation["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
