from __future__ import annotations

from numbers import Integral, Real
from pathlib import Path

import pandas as pd

try:
    from .config import COLLAPSE_DATASET_PATH
except ImportError:
    from config import COLLAPSE_DATASET_PATH


REQUIRED_COLUMNS = [
    "case_id",
    "case_name",
    "case_type",
    "region",
    "period_start",
    "period_end",
    "time_window_years",
    "phase_label",
    "collapse_outcome",
    "collapse_within_next_window",
    "political_fragmentation",
    "elite_conflict",
    "succession_crisis",
    "legitimacy_crisis",
    "administrative_overload",
    "corruption_governance_failure",
    "social_inequality",
    "social_unrest_rebellion",
    "demographic_pressure",
    "migration_pressure",
    "ethnic_sectarian_fragmentation",
    "urban_decline",
    "fiscal_crisis",
    "taxation_extraction_pressure",
    "trade_disruption",
    "inflation_currency_instability",
    "resource_dependency",
    "agricultural_decline",
    "drought_climate_stress",
    "flood_environmental_shock",
    "temperature_anomaly",
    "ecological_degradation",
    "food_insecurity",
    "external_invasion_pressure",
    "civil_war_internal_conflict",
    "military_overstretch",
    "territorial_loss",
    "institutional_rigidity",
    "adaptive_capacity",
    "logistics_food_storage_resilience",
    "alliance_network_strength",
    "recovery_capacity",
    "data_confidence",
    "source_count",
    "notes",
]

FACTOR_COLUMNS = [
    "political_fragmentation",
    "elite_conflict",
    "succession_crisis",
    "legitimacy_crisis",
    "administrative_overload",
    "corruption_governance_failure",
    "social_inequality",
    "social_unrest_rebellion",
    "demographic_pressure",
    "migration_pressure",
    "ethnic_sectarian_fragmentation",
    "urban_decline",
    "fiscal_crisis",
    "taxation_extraction_pressure",
    "trade_disruption",
    "inflation_currency_instability",
    "resource_dependency",
    "agricultural_decline",
    "drought_climate_stress",
    "flood_environmental_shock",
    "temperature_anomaly",
    "ecological_degradation",
    "food_insecurity",
    "external_invasion_pressure",
    "civil_war_internal_conflict",
    "military_overstretch",
    "territorial_loss",
    "institutional_rigidity",
    "adaptive_capacity",
    "logistics_food_storage_resilience",
    "alliance_network_strength",
    "recovery_capacity",
]

VALID_FACTOR_VALUES = {"0", "1", "2", "3", "9", ""}


def load_collapse_dataset(dataset_path: str | Path | None = None) -> pd.DataFrame:
    path = Path(dataset_path) if dataset_path is not None else COLLAPSE_DATASET_PATH
    return pd.read_csv(path)


def get_required_columns() -> list[str]:
    return REQUIRED_COLUMNS.copy()


def get_factor_columns() -> list[str]:
    return FACTOR_COLUMNS.copy()


def validate_factor_values(df: pd.DataFrame) -> pd.DataFrame:
    invalid_rows: list[dict[str, object]] = []

    for column in get_factor_columns():
        if column not in df.columns:
            continue

        normalized_values = df[column].map(_normalize_factor_value)
        invalid_mask = ~normalized_values.isin(VALID_FACTOR_VALUES)

        for row_index in df.index[invalid_mask]:
            invalid_rows.append(
                {
                    "row_number": int(row_index) + 2,
                    "case_id": _normalize_case_id(df.at[row_index, "case_id"]) if "case_id" in df.columns else "<missing case_id column>",
                    "column": column,
                    "invalid_value": normalized_values.at[row_index],
                }
            )

    return pd.DataFrame(
        invalid_rows,
        columns=["row_number", "case_id", "column", "invalid_value"],
    )


def summarize_missingness(df: pd.DataFrame) -> pd.DataFrame:
    missing_count = pd.Series(
        {_column: int(_missing_mask(df[_column]).sum()) for _column in df.columns},
        name="missing_count",
    )

    return (
        missing_count.to_frame()
        .assign(missing_pct=lambda frame: frame["missing_count"] / len(df) * 100 if len(df) else 0.0)
        .sort_values(["missing_count", "missing_pct"], ascending=False)
    )


def detect_duplicate_case_id_rows(df: pd.DataFrame) -> pd.DataFrame:
    if "case_id" not in df.columns:
        return pd.DataFrame(columns=df.columns)

    case_ids = df["case_id"].map(_normalize_case_id)
    duplicate_mask = case_ids.ne("") & case_ids.duplicated(keep=False)
    return df.loc[duplicate_mask].sort_values("case_id").copy()


def _missing_mask(series: pd.Series) -> pd.Series:
    if pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series):
        return series.isna() | series.fillna("").astype(str).str.strip().eq("")

    return series.isna()


def _normalize_case_id(value: object) -> str:
    if pd.isna(value):
        return ""

    return str(value).strip()


def _normalize_factor_value(value: object) -> str:
    if pd.isna(value):
        return ""

    if isinstance(value, str):
        stripped = value.strip()
        if stripped == "":
            return ""
        try:
            numeric_value = float(stripped)
        except ValueError:
            return stripped
        if numeric_value.is_integer():
            return str(int(numeric_value))
        return stripped

    if isinstance(value, Integral):
        return str(int(value))

    if isinstance(value, Real):
        numeric_value = float(value)
        if numeric_value.is_integer():
            return str(int(numeric_value))
        return str(value)

    return str(value).strip()
