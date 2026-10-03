---
name: chart-spec
description: Chart specification giving the question answered, a takeaway title, chart type, highlight, source/n, and caveats. Use for any chart in a deck, post, report, or dashboard.
---

# Chart Spec

One chart, one question, one honest takeaway.

## When to use
Before building any chart, and when auditing charts in decks or posts.

## Produced by
- `data_storyteller`: owns it.

## Template
```markdown
| Chart | Question | Takeaway title | Type | Highlight | Source (n) | Caveat |
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
| C1 slide 9 | Did onboarding v2 reduce churn? | "Churn fell 18% after onboarding v2" | line | v2 cohort | billing DB, Jul–Sep, n=4,210 | early signal; seasonal effects possible |
```

## Quality checks
- [ ] The title states the takeaway
- [ ] Axes are honest
- [ ] Source and n are shown
