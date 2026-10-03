---
name: impact-map
description: Change impact map listing each affected path, the change, its risk, the mitigation, and a preservation check. Use when integrating prototypes, upgrades, dependencies, or global styles into an existing system.
report_id: impact_map
title: Change Impact Map
version: 1
universal: false
tags: [integration, risk]
produced_by: [integration_architect]
output:
  tag: report:impact_map
  format: table
  columns: [Path, Change, Risk, Mitigation, Preservation check]
  min_rows: 1
---

# Change Impact Map

Shows where new work touches existing code, and how the board will prove nothing broke.

## When to use
Before porting or integrating anything into an existing codebase.

## Produced by
- `integration_architect`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:impact_map role=ROLE_ID board=BOARD_ID -->
| Path | Change | Risk (conflict) | Mitigation | Preservation check |
<!-- /report:impact_map -->
```

## Core fields (required)
- **Path**: a real file or glob in the repository.
- **Change**: add, modify, delete, or redirect, plus a summary.
- **Risk**: what could break, such as global styles, key handlers, routes, or dependency versions.
- **Mitigation**: scoping, isolation, a flag, or a shim.
- **Preservation check**: the test or command that proves existing behavior still works.

## How to fill it in
1. Inventory the incoming code's global effects: CSS roots, listeners, host mutations, and dependencies.
2. Map each one to the existing paths it touches.
3. Give every row a preservation check, and hand those checks to the [test plan](../test-plan/SKILL.md).

## On the board
High-risk rows become `claim` notes. Preservation checks feed `@preserve` [acceptance cases](../acceptance-cases/SKILL.md).

## Example

```markdown
<!-- report:impact_map role=integration_architect board=BB-DESIGN-REPLAY -->
| Path | Change | Risk | Mitigation | Preservation check |
|---|---|---|---|---|
| app/globals.css | none (keep) | archive :root and html,body rules override the theme | scope under .replay-root | visual check of / and /blackboard |
| next.config.ts | add /replay → /demo redirect | redirect loop | single permanent redirect | `curl -I /replay` returns 308 to /demo |
<!-- /report:impact_map -->
```

## Quality checks
- [ ] Every global effect is listed
- [ ] Every row has a preservation check
- [ ] Paths are real
