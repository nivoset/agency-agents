---
name: decision-record
description: The blackboard's final board.md synthesis, covering scope, non-goals, a claims/evidence/decisions table, blocking questions, a completeness pass, and verification evidence. Use when a facilitator closes a blackboard session or updates its board version.
---

# Decision Record

The single source of truth a blackboard produces. It contains only claims that some role actually made.

## When to use
At the end of every board, and whenever the board version increments.

## Produced by
- `board_facilitator`: writes it and owns every line.

## Template
```markdown
# Blackboard: <topic>
- Board ID / Version / Owner / Parent readiness (draft | final-ready) / Authority
## Resolved scope
## Non-goals
## Claims, evidence, and decisions
| ID | Claim or decision | Evidence | Interpretation / next action |
## Review roles
- <role_id> — <status>; <one-line outcome>
## Blocking questions
## Assumptions and deferred work      (each with a re-entry condition)
## Required completeness pass
## Verification evidence
```

## Core fields (required)
- **Resolved scope**: the topic restated as what will and won't change.
- **Non-goals**: each with the reason it is excluded.
- **Claims, evidence, and decisions**: `C-n` for claims and `D-n` for decisions. Evidence is a note id, a path, or a command.
- **Blocking questions**: only questions that are genuinely the user's to answer, or "None" with the reason.
- **completeness pass**: each role's final `no_missing_items` status.
- **Verification evidence**: commands run and their results.

## How to fill it in
1. Write the scope and non-goals before dispatching.
2. After each round, lift claims that survived challenge into the table, citing note ids.
3. Turn agreed claims into `D-n` decisions. Put [ticket drafts](../ticket-drafts/SKILL.md) under a features section if work follows.
4. Run the completeness pass and record the results.

## On the board
Built from [board notes](../board-note/SKILL.md) and [dispatch returns](../dispatch-return/SKILL.md). Saved as `.planning/blackboard/<BOARD-ID>/board.md` next to `dispatch.yaml`.

## Example
```markdown
| D-1 | Replay stays independent of live API state | User request + C-1, C-2 | Don't wire replay to /api/* |
```

## Quality checks
- [ ] Every table row cites evidence
- [ ] No claim that no role made
- [ ] Every deferred item has a re-entry condition
- [ ] Readiness is `final-ready` only after all roles return `no_missing_items`
