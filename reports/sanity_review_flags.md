# Sanity Review Flags

This report flags rows and row groups in the first-pass machine-assisted coding draft that may deserve human review.
These are heuristic flags, not confirmed errors.
The dataset was not modified during this pass.

## Possible Overconfidence

- `Easter Island` rows `easter_island_1200_1225` through `easter_island_1675_1700`: 24 factor columns stay identical across all 20 windows. That may be intentional for a highly debated transformation case, but it is still worth checking whether some of those fixed values should vary by period or remain `9`.
- `Bronze Age Collapse States` rows `bronze_age_-1300_-1275` through `bronze_age_-1125_-1100`: 10 factors remain constant across all windows in a heterogeneous multi-polity case, especially `succession_crisis`, `corruption_governance_failure`, `social_inequality`, `demographic_pressure`, `ethnic_sectarian_fragmentation`, `taxation_extraction_pressure`, `inflation_currency_instability`, `flood_environmental_shock`, `temperature_anomaly`, and `ecological_degradation`.
- Rows with `institutional_rigidity >= 2` and `adaptive_capacity >= 2` but notes that do not explicitly explain why both are high at once should be checked for justification, especially `rome_west_150_175` through `rome_west_200_225`, `rome_west_350_375` through `rome_west_400_425`, `khmer_1175_1200` through `khmer_1225_1250`, `maya_700_725` through `maya_750_775`, `bronze_age_-1300_-1275` through `bronze_age_-1250_-1225`, and `akkadian_-2300_-2275` through `akkadian_-2275_-2250`.
- `byzantine_1025_1050` and `byzantine_1050_1075`: the combination of moderate rigidity and moderate adaptive capacity may be defensible, but the notes are brief enough that the coexistence is not clearly justified.

## Possible Undercoding

- `rome_west_350_375`, `rome_west_375_400`, and `rome_west_400_425`: `territorial_loss` stays at `1` late in the western Roman decline sequence, which may understate pre-425 loss of effective control and strategic erosion.
- `maya_900_925` and `maya_925_950`: `territorial_loss` and later `political_fragmentation` may be too low for late southern lowland post-collapse conditions, even though the notes correctly emphasize wider Maya continuity beyond the hardest-hit core.
- `ming_qing_1675_1700`: `political_fragmentation = 1` and `territorial_loss = 1` may be reasonable for stabilized Qing rule, but this row is worth checking because the current coding may blur post-transition consolidation with the earlier Ming collapse sequence.
- `rome_west_325_350`: `political_fragmentation = 1` and `territorial_loss = 1` are low for a row currently labeled `post-collapse`; if the intent is recovery after the third-century crisis, the phase label may need review more than the factor scores.

## Possible Timeline Inconsistency

- `rome_west_275_300`, `rome_west_300_325`, and `rome_west_325_350`: `phase_label = post-collapse` appears very early for a long western Roman chronology. This may reflect recovery after the third-century crisis, but it should be reviewed because the same case later reaches a more familiar terminal western collapse.
- `byzantine_1075_1100`, `byzantine_1100_1125`, and `byzantine_1125_1150`: `collapse_outcome = 2` appears in the first third of a very long decline case. That may be justified by the post-1071 rupture, but it is worth confirming that the coding is not compressing the later Komnenian recovery too much.
- `mesopotamian_-2025_-2000`, `mesopotamian_-2000_-1975`, and `mesopotamian_-1975_-1950`: the collapse and post-collapse sequence appears early by relative-position heuristics. This may be appropriate because the case starts near the Ur III end, but the chronology should be explicitly confirmed.
- `ming_qing_1650_1675` and `ming_qing_1675_1700`: both are labeled `post-collapse`, which is plausible for a transition case, but they should be checked to ensure the dataset is not mixing Ming terminal collapse with later Qing consolidation in one uninterrupted collapse timeline.

## Possible Note-Quality Issues

- `Western Roman Empire` rows `rome_west_-100_-75` through `rome_west_125_150`: the same note is repeated across 10 rows, which makes the early stable phase easy to scan but may be too generic for later row-level review.
- `Khmer Empire` rows `khmer_1000_1025` through `khmer_1150_1175`: the same note is repeated across 7 rows; consider whether later human review should differentiate pre-decline subperiods more clearly.
- `Easter Island` has several long repeated-note blocks, especially `easter_island_1300_1325` through `easter_island_1425_1450` and `easter_island_1550_1575` through `easter_island_1675_1700`, which may be fine methodologically but do reduce row-specific interpretability.
- `Classic Mesopotamian States` rows `mesopotamian_-1950_-1925` through `mesopotamian_-1875_-1850` and `mesopotamian_-1700_-1675` through `mesopotamian_-1625_-1600` reuse identical notes across four-row blocks; those should be checked once row-level source notes are added.
- `Byzantine Decline` rows `byzantine_1075_1100` through `byzantine_1150_1175` and `byzantine_1325_1350` through `byzantine_1375_1400` use repeated notes across long spans, which may flatten important internal variation.
- The shortest and most generic notes appear in rows such as `byzantine_1000_1025`, `mesopotamian_-2050_-2025`, `byzantine_1025_1050`, and `byzantine_1050_1075`; these are readable, but they do not carry much row-specific nuance.

## Review Priority Suggestions

- First review priority: `rome_west_275_300` through `rome_west_400_425`, `byzantine_1075_1100` through `byzantine_1125_1150`, and `maya_900_925` through `maya_925_950`.
- Second review priority: all `Easter Island` rows, all `Bronze Age Collapse States` rows, and `Classic Mesopotamian States` rows around the Ur III collapse/post-collapse boundary.
- Third review priority: repeated-note blocks in `Khmer Empire`, `Western Roman Empire`, and `Byzantine Decline`.
