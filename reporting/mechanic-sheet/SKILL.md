---
name: mechanic-sheet
description: Game mechanic and system sheet listing purpose, player decision, inputs, outputs, edge cases, and tuning values flagged [PLACEHOLDER]. Use when designing or reviewing mechanics, progression, or economies.
report_id: mechanic_sheet
title: Mechanic Sheet
version: 1
universal: false
tags: [game-mechanics]
produced_by: [game_systems_designer]
output:
  tag: report:mechanic_sheet
  format: table
  columns: [Mechanic, Purpose, Player decision, Inputs, Outputs, Edge cases]
  min_rows: 1
---

# Mechanic Sheet

Documents a mechanic well enough that engineers can build it and playtests can falsify it.

## When to use
For every new or changed mechanic, system, or economy lever.

## Produced by
- `game_systems_designer`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:mechanic_sheet role=ROLE_ID board=BOARD_ID -->
Loops: moment-to-moment / session / long-term
| Mechanic | Purpose | Player decision | Inputs | Outputs | Edge cases | Tuning (values) |
| Resource | Sources | Sinks | Target flow |
<!-- /report:mechanic_sheet -->
```

## Core fields (required)
- **Mechanic**: its name.
- **Purpose**: the experience goal.
- **Player decision**: the meaningful choice it creates. If there is none, cut the mechanic.
- **Inputs** / **Outputs**: player inputs and game-state changes.
- **Edge cases**: including failure states and exploits.

## How to fill it in
1. Write the three loops.
2. Fill a row per mechanic. Tag every number `[PLACEHOLDER]` with a rationale.
3. Model resource sources and sinks, and define what "broken" looks like before playtesting.

## On the board
Post each mechanic's decision as a `claim` note. `playtest_analyst` answers with [research findings](../research-findings/SKILL.md). `gameplay_engineer` responds with a [budget sheet](../budget-sheet/SKILL.md).

## Example

```markdown
<!-- report:mechanic_sheet role=game_systems_designer board=BB-DESIGN-REPLAY -->
| Mechanic | Purpose | Player decision | Inputs | Outputs | Edge cases | Tuning |
|---|---|---|---|---|---|---|
| Dash | evasion as skill expression | dodge now, or save it for the gap | dash + direction | 4m move with i-frames | dash into a wall gives no i-frames | cooldown 1.2s [PLACEHOLDER] |
<!-- /report:mechanic_sheet -->
```

## Quality checks
- [ ] Every mechanic names a player decision
- [ ] No untagged magic numbers
- [ ] Every resource has a sink
