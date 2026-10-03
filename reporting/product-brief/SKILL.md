---
name: product-brief
description: One-page brief stating the problem, user, outcome metric, kill criteria, prioritized scope, and non-goals. Use at the start of a product, feature, game mode, campaign, or pitch board, before specialists optimize.
report_id: product_brief
title: Product Brief
version: 1
universal: false
tags: [planning, metrics]
produced_by: [product_manager]
output:
  tag: report:product_brief
  format: fields
  labels: [Problem, User, Outcome metric, Kill criteria, Non-goals]
  min_rows: 1
---

# Product Brief

Makes sure the board solves the right problem at the right size.

## When to use
At the start of any feature, product, or campaign board, and whenever scope is contested.

## Produced by
- `product_manager`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:product_brief role=ROLE_ID board=BOARD_ID -->
Problem: <user pain, with evidence>
User: <who exactly>
Outcome metric: <measurable change + target + check date>
Kill criteria: <what result makes us stop>
| Priority (must/should/won't) | Item | Rationale |
Non-goals: <item> — re-entry condition: <...>
<!-- /report:product_brief -->
```

## Core fields (required)
- **Problem**: evidence-backed, or labeled as an assumption.
- **User**: a specific segment, not "everyone".
- **Outcome metric**: a number, a direction, and a date.
- **Kill criteria**: set before launch.
- **Non-goals**: each with a re-entry condition.

## How to fill it in
1. State the problem using research or support data. Ask `ux_researcher` if there is none.
2. Pick one outcome metric and its kill criteria.
3. Draw the must / should / won't line. Must-haves become [ticket drafts](../ticket-drafts/SKILL.md).

## On the board
Post the problem and the metric as `claim` notes in round 1. The facilitator copies scope and non-goals into the [decision record](../decision-record/SKILL.md).

## Example

```markdown
<!-- report:product_brief role=product_manager board=BB-DESIGN-REPLAY -->
Problem: reviewers can't see why a plan changed (6 support threads in September)
User: engineering leads reviewing blackboard plans
Outcome metric: median review time down 30% by Nov 15
Kill criteria: no change after 4 weeks of use
| Priority | Item | Rationale |
|---|---|---|
| must | timeline + rationale | core of the problem |
| won't | persisted notes | no evidence of need yet |
Non-goals: persisted notes (re-entry: repeat usage above 3 per week)
<!-- /report:product_brief -->
```

## Quality checks
- [ ] The metric is measurable and dated
- [ ] Every must-have has an acceptance case
- [ ] Every non-goal has a re-entry condition
