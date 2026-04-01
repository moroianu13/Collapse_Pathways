# Project Map

## What Each Major Folder Does

- `data/raw`
  - Original or starter inputs that are not the main working dataset.
- `data/interim`
  - Pilot sheets, case subsets, and first-pass intermediate extracts.
- `data/processed`
  - Main working datasets, audit files, and the global fragility scoring templates.
- `data/backups`
  - Timestamped backups of the main historical dataset.
- `notebooks`
  - Analysis, review, and presentation notebooks.
- `references/sources`
  - Source inventories and source-tracking files.
- `references/coding_notes`
  - Case coding notes, note templates, and first-pass filled drafts.
- `references/methodology`
  - Coding guides, factor definitions, case lists, pilot rationale, and the global scoring protocol.
- `reports`
  - Written summaries, sanity-review notes, revision logs, and final presentation-ready text.
- `src`
  - Validation scripts, dataset utilities, export helpers, and coding workflow scripts.

## Which Notebooks To Open First

- `notebooks/12_core_findings_summary.ipynb`
  - Best starting point for the main historical findings.
- `notebooks/15_global_fragility_scored_current_world.ipynb`
  - Best starting point for the present-day global overlap score.
- `notebooks/16_global_fragility_scenarios.ipynb`
  - Best starting point for scenario comparison and sensitivity analysis.
- `notebooks/11_uncertainty_aware_summary.ipynb`
  - Best if you want to understand where the dataset is strongest and weakest.
- `notebooks/08_case_category_analysis.ipynb`
  - Best for comparing cases at the category level.

## Which Datasets Are The Main Ones

- `data/processed/collapse_dataset_expanded.csv`
  - Main historical collapse-pattern dataset.
- `data/processed/auto_coding_audit.csv`
  - Row-level audit summary for the current dataset.
- `data/processed/global_fragility_manual_template.csv`
  - Historical-weighted factor structure for the present-day extension.
- `data/processed/global_fragility_current_scoring_template.csv`
  - Current-world manual scoring sheet with the present draft scores.

## Where The Final Results Live

- `reports/final_summary.md`
  - Concise final written summary of the project findings.
- `PROJECT_STATUS.md`
  - Practical status snapshot, limitations, and next priorities.
- `README.md`
  - Clean overview of the full project.
- `notebooks/12_core_findings_summary.ipynb`
  - Main historical interpretation notebook.
- `notebooks/15_global_fragility_scored_current_world.ipynb`
  - Present-day baseline global fragility score.
- `notebooks/16_global_fragility_scenarios.ipynb`
  - Sensitivity analysis around the global fragility score.
