---
name: conflict-map
description: Map of a disagreement giving each party's position, interest, and strongest view, plus temperature, stuck point, and the recommended next move and channel. Use before replying to a heated message, thread, or dispute.
report_id: conflict_map
title: Conflict Map
version: 1
universal: false
tags: [de-escalation]
produced_by: [conflict_mediator, steelman_interpreter]
output:
  tag: report:conflict_map
  format: table
  columns: [Party, Interest]
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

# Conflict Map

Shows what each side actually needs, so the reply answers that instead of the surface argument.

## When to use
Before responding in any conflict: a thread, an email, a review comment, a family chat, or a team dispute.

## Produced by
- `conflict_mediator`: parties, positions, interests, temperature, stuck point, next move, and channel.
- `steelman_interpreter`: each party's strongest view, its underlying need, and the true part to concede.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:conflict_map role=ROLE_ID board=BOARD_ID -->
| Party | Position | Interest (underlying need) | Strongest view | True part to concede | Temperature (1–5) |
Stuck point: ...
Recommended next move: ... | Channel/timing: ... | Non-negotiables kept: <from boundary_brief>
<!-- /report:conflict_map -->
```

## Core fields (required)
- **Party**: everyone with a stake, including the user.
- **Interest**: the need behind the position (being heard, safety, fairness, status, autonomy).

## How to fill it in
1. Quote positions from the actual messages.
2. Infer interests, and label them as inferences.
3. Steelman each party and find something true to concede.
4. Choose the move and the channel. "Don't reply yet" is a valid move.

## On the board
Interests and concessions are `claim` notes. Non-negotiables come from the [boundary brief](../boundary-brief/SKILL.md). The wording comes from [draft variants](../draft-variants/SKILL.md).

## Example

```markdown
<!-- report:conflict_map role=conflict_mediator board=BB-DESIGN-REPLAY -->
| Party | Position | Interest | Strongest view | True part to concede | Temperature |
|---|---|---|---|---|---|
| Teammate | "you never test anything" | stop the 3am pages | two pages last week were preventable | the second page was preventable | 4 |
| User | "I test the critical paths" | be seen as reliable | coverage is focused on risk | none needed | 3 |
Stuck point: both are arguing about testing in general, not the alert
Recommended next move: acknowledge the preventable page and offer to pair on alert rules
Channel/timing: DM, today
<!-- /report:conflict_map -->
```

## Quality checks
- [ ] Every party has an interest
- [ ] Inferences are labeled
- [ ] The move preserves the non-negotiables
