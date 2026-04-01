from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    from .config import INTERIM_DATA_DIR, PILOT_CODING_SHEET_PATH, PROJECT_ROOT
except ImportError:
    from config import INTERIM_DATA_DIR, PILOT_CODING_SHEET_PATH, PROJECT_ROOT

import pandas as pd


def resolve_path(path_value: str | None, default_path: Path) -> Path:
    if path_value is None:
        return default_path

    candidate = Path(path_value)
    if candidate.is_absolute():
        return candidate

    return (PROJECT_ROOT / candidate).resolve()


def build_default_output_path(case_name: str) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "_", case_name.lower()).strip("_")
    return INTERIM_DATA_DIR / f"{slug}_pilot_subset.csv"


def export_case_subset(case_name: str, input_path: Path, output_path: Path) -> int:
    df = pd.read_csv(input_path)

    if "case_name" not in df.columns:
        print(f"Input file is missing required column 'case_name': {input_path}")
        return 1

    case_subset = df[df["case_name"] == case_name].copy()
    if case_subset.empty:
        print(f"No rows found for case_name={case_name!r} in {input_path}")
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    case_subset.to_csv(output_path, index=False)

    print(f"Exported {len(case_subset)} rows for {case_name!r}")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export a single case subset from the pilot coding sheet.",
    )
    parser.add_argument("case_name", help="Exact case_name value to export.")
    parser.add_argument(
        "--input",
        dest="input_path",
        default=None,
        help="Optional path to the pilot CSV. Defaults to data/interim/pilot_coding_sheet.csv.",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        default=None,
        help="Optional output CSV path. Defaults to data/interim/<case_name>_pilot_subset.csv.",
    )
    return parser.parse_args(argv[1:])


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    input_path = resolve_path(args.input_path, PILOT_CODING_SHEET_PATH)
    output_default = build_default_output_path(args.case_name)
    output_path = resolve_path(args.output_path, output_default)

    if not input_path.exists():
        print(f"Pilot CSV not found: {input_path}")
        return 1

    return export_case_subset(args.case_name, input_path, output_path)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
