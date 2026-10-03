---
name: ticket-drafts
description: Table of implementation-ready ticket drafts with acceptance evidence, dependencies, and status. Use when a board's decisions turn into work items, a capability hierarchy, or a sprint plan.
---

# Ticket Drafts

Turns decisions into work another agent or engineer can pick up without re-reading the board.

## When to use
After decisions settle and implementation is expected.

## Produced by
- `board_facilitator`: writes the capability hierarchy and the final ticket table.
- `product_manager`: proposes priority and the scope cut for each ticket.

## Template
```markdown
Capability: CAP-nn <outcome>
| Ticket | Capability | Priority | Acceptance evidence | Depends on | Status |
| BB-101 <verb-first title> | CAP-01 | must | <observable check that proves done> | None | Draft |
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
| BB-106 Version-scoped notes | CAP-01 | should | note added at v5 shows at v5 only; whitespace ignored (`notes.test.jsx`) | BB-101 | Draft |
```

## Quality checks
- [ ] Every ticket has testable acceptance evidence
- [ ] There are no dependency cycles
- [ ] Titles start with a verb or an outcome
