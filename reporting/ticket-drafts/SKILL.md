---
name: ticket-drafts
description: Table of implementation-ready ticket drafts with acceptance evidence, dependencies, and status. Use when a board's decisions turn into work items, a capability hierarchy, or a sprint plan.
report_id: ticket_drafts
title: Ticket Drafts
version: 1
universal: false
tags: [planning]
produced_by: [board_facilitator, product_manager]
output:
  tag: report:ticket_drafts
  format: table
  columns: [Ticket, Acceptance evidence, Depends on, Status]
  enums:
    Status: [draft, ready, in progress, done]
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

# Ticket Drafts

Turns decisions into work another agent or engineer can pick up without re-reading the board.

## When to use
After decisions settle and implementation is expected.

## Produced by
- `board_facilitator`: writes the capability hierarchy and the final ticket table.
- `product_manager`: proposes priority and the scope cut for each ticket.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:ticket_drafts role=ROLE_ID board=BOARD_ID -->
Capability: CAP-nn <outcome>
| Ticket | Capability | Priority | Acceptance evidence | Depends on | Status |
| BB-101 <verb-first title> | CAP-01 | must | <observable check that proves done> | None | Draft |
<!-- /report:ticket_drafts -->
```

## Core fields (required)
- **Ticket**: an id plus a verb-first title.
- **Acceptance evidence**: an observable, testable result. Prefer a named test or command.
- **Depends on**: ticket ids, or `None`.
- **Status**: `Draft`, `Ready`, `In progress`, or `Done (evidence)`.

## How to fill it in
1. Group tickets under capabilities, which are user-facing outcomes.
2. Write acceptance evidence first. If you can't, the ticket is too vague. Split it.
3. Order tickets by dependency, and note which can run in parallel.

## On the board
Lives inside the [decision record](../decision-record/SKILL.md) under "Feature / ticket drafts". Acceptance evidence should reference [acceptance cases](../acceptance-cases/SKILL.md) or the [test plan](../test-plan/SKILL.md).

## Example

```markdown
<!-- report:ticket_drafts role=product_manager board=BB-DESIGN-REPLAY -->
| Ticket | Capability | Priority | Acceptance evidence | Depends on | Status |
|---|---|---|---|---|---|
| BB-101 Timeline keyboard controls | CAP-01 | must | `timeline.test.jsx` "ignores editable targets" passes | None | ready |
| BB-106 Version-scoped notes | CAP-01 | should | note added at v5 shows only at v5 (`notes.test.jsx`) | BB-101 | draft |
<!-- /report:ticket_drafts -->
```

## Quality checks
- [ ] Every ticket has testable acceptance evidence
- [ ] There are no dependency cycles
- [ ] Titles start with a verb or an outcome
