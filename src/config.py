from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
BACKUPS_DATA_DIR = DATA_DIR / "backups"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
SRC_DIR = PROJECT_ROOT / "src"
REFERENCES_DIR = PROJECT_ROOT / "references"
REFERENCES_SOURCES_DIR = REFERENCES_DIR / "sources"
REFERENCES_CODING_NOTES_DIR = REFERENCES_DIR / "coding_notes"
REFERENCES_METHODOLOGY_DIR = REFERENCES_DIR / "methodology"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

COLLAPSE_DATASET_PATH = PROCESSED_DATA_DIR / "collapse_dataset_expanded.csv"
PILOT_CODING_SHEET_PATH = INTERIM_DATA_DIR / "pilot_coding_sheet.csv"
