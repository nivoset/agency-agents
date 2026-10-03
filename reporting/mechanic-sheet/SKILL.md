---
name: mechanic-sheet
description: Game mechanic and system sheet listing purpose, player decision, inputs, outputs, edge cases, and tuning values flagged [PLACEHOLDER]. Use when designing or reviewing mechanics, progression, or economies.
---

# Mechanic Sheet

Documents a mechanic well enough that engineers can build it and playtests can falsify it.

## When to use
For every new or changed mechanic, system, or economy lever.

## Produced by
- `game_systems_designer`: owns it.

## Template
```markdown
Loops: moment-to-moment / session / long-term
| Mechanic | Purpose | Player decision | Inputs | Outputs | Edge cases | Tuning (values) |
| Resource | Sources | Sinks | Target flow |
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
| Dash | evasion skill expression | dodge now vs. save for gap | dash button + direction | 4m i-frame move | dash into wall = no i-frames | cooldown 1.2s [PLACEHOLDER] |
```

## Quality checks
- [ ] Every mechanic names a player decision
- [ ] No untagged magic numbers
- [ ] Every resource has a sink
