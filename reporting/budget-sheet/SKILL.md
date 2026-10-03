---
name: budget-sheet
description: Performance and size budgets showing what is budgeted, the limit, the measured value, and target hardware or platform. Use for frame time, triangles, texture memory, draw calls, particles, bundle size, and Web Vitals.
---

# Budget Sheet

Turns "make it fast" into numbers you can check.

## When to use
Whenever art, effects, mechanics, or UI must run on a target device or platform.

## Produced by
- `technical_artist`: limits per asset class (tris, texture memory, draw calls, bones).
- `gameplay_engineer`: frame time per system.
- `frontend_engineer`: Web Vitals and bundle-size budgets.
- `modeler_3d`: per-asset triangle and texture use against its class budget.
- `vfx_artist`: particle and overdraw budgets at worst-case counts.

## Template
```markdown
| Budget | Limit | Measured | Target (hardware / platform) | Status | Exception rationale |
```

## Core fields (required)
- **Budget**: the measured item (e.g. "Hero character tris", "Combat AI ms/frame", "LCP").
- **Limit**: a number with units.
- **Measured**: from a profiler or tool on the target, or `not yet measured`.
- **Target**: the minimum-spec device or platform the limit applies to.

## How to fill it in
1. Set limits from the platform's total budget, top-down.
2. Measure on the target, not the dev machine.
3. Mark over-budget rows, and give each a rationale and a fallback (LOD, cut, optimization).

## On the board
Over-budget rows are `claim` notes with evidence (a profiler capture). Budget splits between roles, such as logic vs. rendering, are settled with `answer` notes.

## Example
```markdown
| Boss fight VFX overdraw | 3.0x | 4.2x | Switch (docked) | over | reduce smoke layers 6→3 |
```

## Quality checks
- [ ] Every limit has units and a target
- [ ] Measurements come from target hardware
- [ ] Every overage has a fallback
