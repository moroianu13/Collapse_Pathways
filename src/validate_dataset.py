from __future__ import annotations

import sys
from pathlib import Path

try:
    from .config import COLLAPSE_DATASET_PATH, PROJECT_ROOT
    from .dataset_utils import (
        detect_duplicate_case_id_rows,
        get_required_columns,
        load_collapse_dataset,
        summarize_missingness,
        validate_factor_values,
    )
except ImportError:
    from config import COLLAPSE_DATASET_PATH, PROJECT_ROOT
    from dataset_utils import (
        detect_duplicate_case_id_rows,
        get_required_columns,
        load_collapse_dataset,
        summarize_missingness,
        validate_factor_values,
    )


def resolve_dataset_path(argument: str | None) -> Path:
    if argument is None:
        return COLLAPSE_DATASET_PATH

    candidate = Path(argument)
    if candidate.is_absolute():
        return candidate

    return (PROJECT_ROOT / candidate).resolve()


def main(argv: list[str]) -> int:
    dataset_path = resolve_dataset_path(argv[1] if len(argv) > 1 else None)

    if not dataset_path.exists():
        print(f"Dataset not found: {dataset_path}")
        return 1

    df = load_collapse_dataset(dataset_path)
    missing_columns = [column for column in get_required_columns() if column not in df.columns]
    invalid_factor_values = validate_factor_values(df)
    missing_value_summary = summarize_missingness(df)
    duplicate_case_id_rows = detect_duplicate_case_id_rows(df)
    duplicate_case_id_counts = (
        duplicate_case_id_rows["case_id"].value_counts().sort_index()
        if not duplicate_case_id_rows.empty and "case_id" in duplicate_case_id_rows.columns
        else None
    )

    print(f"Loaded dataset: {dataset_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print()

    print("Required column check")
    if missing_columns:
        print("  Missing required columns:")
        for column in missing_columns:
            print(f"  - {column}")
    else:
        print("  All required columns are present.")
    print()

    print("Factor value check")
    if not invalid_factor_values.empty:
        print("  Invalid factor values found:")
        for row in invalid_factor_values.itertuples(index=False):
            print(
                f"  - row {row.row_number} ({row.case_id}): {row.column}={row.invalid_value!r} "
                "(expected 0, 1, 2, 3, 9, or empty)"
            )
    else:
        print("  All factor columns contain only 0, 1, 2, 3, 9, or empty values.")
    print()

    print("Missing-value summary")
    for column, row in missing_value_summary.iterrows():
        print(f"  - {column}: {int(row.missing_count)} missing ({row.missing_pct:.1f}%)")
    print()

    print("Duplicate case_id check")
    if duplicate_case_id_counts is not None:
        print("  Duplicate case_id values found:")
        for case_id, count in duplicate_case_id_counts.items():
            print(f"  - {case_id}: {count} rows")
    else:
        print("  No duplicate case_id values found.")

    has_errors = bool(missing_columns or not invalid_factor_values.empty or duplicate_case_id_counts is not None)
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
