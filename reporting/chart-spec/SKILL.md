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
---

# Chart Spec

One chart, one question, one honest takeaway.

## When to use
Before building any chart, and when auditing charts in decks or posts.

## Produced by
- `data_storyteller`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
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
