---
name: chart-spec
description: Chart specification giving the question answered, a takeaway title, chart type, highlight, source/n, and caveats. Use for any chart in a deck, post, report, or dashboard.
report_id: chart_spec
title: Chart Spec
version: 1
universal: false
tags: [data-viz, evidence]
produced_by: [data_storyteller]
output:
  tag: report:chart_spec
  format: table
  columns: [Chart, Question, Takeaway title, Type, Source]
  min_rows: 1
validation:
  script: scripts/validate.py
  command: uv run --script <dir>/scripts/validate.py --format json <file>
  command_for_role: uv run --script <dir>/scripts/validate.py --format json --role <role> --board <board> <file>
  fallback_command: python3 <dir>/scripts/validate.py --format json <file>
  placeholders:
    <dir>: Absolute path of this skill's folder (the one containing SKILL.md)
    <file>: Path to the agent output to validate; '-' reads stdin
    <role>: Role id that produced the output (blackboard.id of the role)
    <board>: Board id the output belongs to (board= attribute on the report tag)
  requires: [uv]
  fallback_requires: [python3>=3.9, pyyaml>=6.0]
  dependencies: PEP 723 inline metadata in scripts/validate.py (uv installs them on first run)
  output: json
  exit_codes:
    0: valid
    1: invalid
    2: usage_error
---

# Chart Spec

One chart, one question, one honest takeaway.

## When to use
Before building any chart, and when auditing charts in decks or posts.

## Produced by
- `data_storyteller`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:chart_spec role=ROLE_ID board=BOARD_ID -->
| Chart | Question | Takeaway title | Type | Highlight | Source (n) | Caveat |
<!-- /report:chart_spec -->
```

## Core fields (required)
- **Chart**: an id and its placement (slide 9, post 2).
- **Question**: the decision-relevant question the chart answers.
- **Takeaway title**: a full sentence stating the finding.
- **Type**: chosen for the question (change over time → line, comparison → bar, part-to-whole → stacked bar, not pie-3D).
- **Source**: the dataset, the date, and n.

## How to fill it in
1. Write the question, then the takeaway title. If you can't write a title, there's no chart.
2. Pick the type and the single highlighted series.
3. Check honesty: bars start at zero, the time window isn't cherry-picked, and uncertainty is shown when it matters.

## On the board
Verify statistical claims with `fact_disentangler` (a [claim ledger](../claim-ledger/SKILL.md)). Hand legibility conflicts to `slide_designer`.

## Example

```markdown
<!-- report:chart_spec role=data_storyteller board=BB-DESIGN-REPLAY -->
| Chart | Question | Takeaway title | Type | Highlight | Source | Caveat |
|---|---|---|---|---|---|---|
| C1 (slide 9) | Did onboarding v2 reduce churn? | "Churn fell 18% after onboarding v2" | line | v2 cohort | billing DB, Jul–Sep, n=4,210 | early signal; seasonal effects possible |
<!-- /report:chart_spec -->
```

## Quality checks
- [ ] The title states the takeaway
- [ ] Axes are honest
- [ ] Source and n are shown
