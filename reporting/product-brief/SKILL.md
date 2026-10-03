---
name: product-brief
description: One-page brief stating the problem, user, outcome metric, kill criteria, prioritized scope, and non-goals. Use at the start of a product, feature, game mode, campaign, or pitch board, before specialists optimize.
---

# Product Brief

Makes sure the board solves the right problem at the right size.

## When to use
At the start of any feature, product, or campaign board, and whenever scope is contested.

## Produced by
- `product_manager`: owns it.

## Template
```markdown
Problem: <user pain, with evidence>
User: <who exactly>
Outcome metric: <measurable change + target + check date>
Kill criteria: <what result makes us stop>
| Priority (must/should/won't) | Item | Rationale |
Non-goals: <item> — re-entry condition: <...>
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
Problem: reviewers can't see why a plan changed (6 support threads in Sept)
Outcome metric: median review time −30% by Nov 15 | Kill: no change after 4 weeks
```

## Quality checks
- [ ] The metric is measurable and dated
- [ ] Every must-have has an acceptance case
- [ ] Every non-goal has a re-entry condition
