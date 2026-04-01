# Targeted Revision Log

This log records the targeted revision pass applied only to the flagged high-priority rows from [sanity_review_flags.md](d:/ADRIAN/projects/Collapse_Pathways/reports/sanity_review_flags.md#L1).
The goal was limited correction, not full recoding.

## Western Roman Empire

| Row ID | What Changed | Why It Changed |
|---|---|---|
| `rome_west_275_300` | `phase_label` `post-collapse -> stressed`; `collapse_outcome` `2 -> 1`; note rewritten. | The earlier label treated post-third-century recovery as if the West were already in a post-collapse phase. The case analysis emphasized substantial recovery under Aurelian and the early Tetrarchy, so a stressed recovery row is more consistent. |
| `rome_west_300_325` | `phase_label` `post-collapse -> stressed`; `collapse_outcome` `2 -> 1`; note rewritten. | This row reflects reconstruction and stabilization rather than severe decline. The revision preserves long-term strain without overstating collapse. |
| `rome_west_325_350` | `phase_label` `post-collapse -> stressed`; `collapse_outcome` `2 -> 1`; note rewritten. | The previous coding implied an early post-collapse sequence in a case that later still has its main terminal collapse. This revision keeps the row strained but not already collapsed. |
| `rome_west_350_375` | Scores left unchanged; note rewritten. | The flagged issue was partly note quality. The row remains defensibly coded as `decline` with low territorial loss because this is still before the decisive post-376 rupture. |
| `rome_west_375_400` | `territorial_loss` `1 -> 2`; note rewritten. | After Adrianople and Gothic settlement, low territorial loss looked too conservative. The change captures erosion of effective control without jumping to terminal-collapse scores. |
| `rome_west_400_425` | `territorial_loss` `1 -> 2`; note rewritten. | The Rhine crossing, loss of Britain, and repeated usurpations make the earlier low territorial-loss score look undercoded for this late pre-terminal window. |

## Byzantine Decline

| Row ID | What Changed | Why It Changed |
|---|---|---|
| `byzantine_1075_1100` | Scores left unchanged; note rewritten. | The earlier `decline / collapse_outcome = 2` coding remains defensible because the post-1071 Anatolian rupture was a real structural break. The revision only makes the note more specific about partial recovery under Alexios I. |
| `byzantine_1100_1125` | Scores left unchanged; note rewritten. | This row was flagged because severe-decline coding appears early in a long case, but the narrower post-Manzikert military-fiscal base still justifies the score. The note now states that more clearly. |
| `byzantine_1125_1150` | Scores left unchanged; note rewritten. | The case analysis supports ongoing serious weakness despite Komnenian recovery, so the score was left in place and only the note was improved. |

## Maya

| Row ID | What Changed | Why It Changed |
|---|---|---|
| `maya_900_925` | `political_fragmentation` `2 -> 3`; `territorial_loss` `1 -> 2`; note rewritten. | The sanity review correctly flagged undercoding. Severe southern lowland fragmentation still persists in this immediate post-collapse window even though the wider Maya world continues elsewhere. |
| `maya_925_950` | `political_fragmentation` `1 -> 2`; `territorial_loss` `1 -> 2`; note rewritten. | The previous row likely understated the persistence of southern lowland losses. Scores were raised only to moderate levels to preserve caution about wider regional survival. |

## Ming/Qing Transition

| Row ID | What Changed | Why It Changed |
|---|---|---|
| `ming_qing_1650_1675` | Scores left unchanged; note rewritten. | The `post-collapse` treatment remains defensible because the main Ming collapse already occurred in the previous row, while this period is better read as violent transition and Qing consolidation. |
| `ming_qing_1675_1700` | Scores left unchanged; note rewritten. | The earlier low fragmentation and territorial-loss scores were kept because this row is intended to capture post-transition stabilization under Qing rule rather than continued Ming terminal collapse. |

## Scope Note

- No unflagged cases were modified.
- No schema changes were made.
- Factor values remain restricted to `0, 1, 2, 3, 9`.
- A timestamped safety backup of the dataset was created before revision: `collapse_dataset_expanded_backup_targeted_revision_20260401_183447.csv`.
