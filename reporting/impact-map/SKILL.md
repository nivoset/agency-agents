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

# Change Impact Map

Shows where new work touches existing code, and how the board will prove nothing broke.

## When to use
Before porting or integrating anything into an existing codebase.

## Produced by
- `integration_architect`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
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
