---
name: boundary-brief
description: The user's non-negotiables, a risk assessment (good-faith vs. harassment or manipulation), boundary statements, and an escalation path. Use in any conflict or public response where the user could be pressured into conceding, or put at risk.
report_id: boundary_brief
title: Boundary Brief
version: 1
universal: false
tags: [boundaries, risk]
produced_by: [boundary_keeper]
output:
  tag: report:boundary_brief
  format: fields
  labels: [Non-negotiables, Risk, Boundary statements, Escalation]
  enums:
    Risk: [low, medium, high]
  min_rows: 1
---

# Boundary Brief

Makes sure de-escalation never turns into capitulation, and that safety comes first.

## When to use
Before drafting any conflict reply, and immediately when there are signs of harassment, threats, or pile-ons.

## Produced by
- `boundary_keeper`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:boundary_brief role=ROLE_ID board=BOARD_ID -->
Non-negotiables: <what the user will not concede under any wording>
Risk: low | medium | high: <good-faith disagreement / pattern / pile-on / threat, with evidence>
Boundary statements: <"I will…" statements about the user's own actions>
Escalation: <none / mute / block / report / step away / real-world support>
<!-- /report:boundary_brief -->
```

## Core fields (required)
- **Non-negotiables**: confirmed with the user, not assumed.
- **Risk**: a level and the evidence for it.
- **Boundary statements**: about the user's own actions, not about controlling others.
- **Escalation**: required when risk is high.

## How to fill it in
1. Ask or confirm what the user will not concede.
2. Assess the pattern and the risk from the message history.
3. Write calm boundary statements, and set the escalation path.

## On the board
High risk overrides the other conflict roles: no engagement drafts, only escalation. The non-negotiables must appear in the [conflict map](../conflict-map/SKILL.md) and in every [draft variant](../draft-variants/SKILL.md).

## Example

```markdown
<!-- report:boundary_brief role=boundary_keeper board=BB-DESIGN-REPLAY -->
Non-negotiables: won't retract the bug report's content; will apologize for its tone
Risk: medium (3 accounts posted the same claim within an hour, a pile-on)
Boundary statements: "I'll post one clarification and step away from the thread."
Escalation: mute the thread; report it if threats appear
<!-- /report:boundary_brief -->
```

## Quality checks
- [ ] Non-negotiables are confirmed with the user
- [ ] Every risk level cites evidence
- [ ] No retaliation is suggested
