---
name: budget-sheet
description: Performance and size budgets showing what is budgeted, the limit, the measured value, and target hardware or platform. Use for frame time, triangles, texture memory, draw calls, particles, bundle size, and Web Vitals.
report_id: budget_sheet
title: Budget Sheet
version: 1
universal: false
tags: [performance-budget]
produced_by: [frontend_engineer, gameplay_engineer, modeler_3d, technical_artist, vfx_artist]
output:
  tag: report:budget_sheet
  format: table
  columns: [Budget, Limit, Measured, Target]
  enums:
    Status: [ok, over, not measured]
  min_rows: 1
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
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:budget_sheet role=ROLE_ID board=BOARD_ID -->
| Budget | Limit | Measured | Target (hardware / platform) | Status | Exception rationale |
<!-- /report:budget_sheet -->
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
<!-- report:budget_sheet role=vfx_artist board=BB-DESIGN-REPLAY -->
| Budget | Limit | Measured | Target | Status | Exception rationale |
|---|---|---|---|---|---|
| Boss fight VFX overdraw | 3.0x | 4.2x | Switch (docked) | over | reduce smoke layers from 6 to 3 |
| Hit spark particles | 200 | 140 | Switch (docked) | ok | none |
<!-- /report:budget_sheet -->
```

## Quality checks
- [ ] Every limit has units and a target
- [ ] Measurements come from target hardware
- [ ] Every overage has a fallback
