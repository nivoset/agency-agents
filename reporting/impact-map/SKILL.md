---
name: impact-map
description: Change impact map listing each affected path, the change, its risk, the mitigation, and a preservation check. Use when integrating prototypes, upgrades, dependencies, or global styles into an existing system.
---

# Change Impact Map

Shows where new work touches existing code, and how the board will prove nothing broke.

## When to use
Before porting or integrating anything into an existing codebase.

## Produced by
- `integration_architect`: owns it.

## Template
```markdown
| Path | Change | Risk (conflict) | Mitigation | Preservation check |
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
| app/globals.css | none (keep) | archive :root + html,body rules override theme | scope under .replay-root | visual check of / and /blackboard |
```

## Quality checks
- [ ] Every global effect is listed
- [ ] Every row has a preservation check
- [ ] Paths are real
