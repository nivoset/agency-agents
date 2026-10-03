---
name: decision-record
description: The blackboard's final board.md synthesis, covering scope, non-goals, a claims/evidence/decisions table, blocking questions, a completeness pass, and verification evidence. Use when a facilitator closes a blackboard session or updates its board version.
report_id: decision_record
title: Decision Record
version: 1
universal: false
tags: [synthesis, planning, evidence]
produced_by: [board_facilitator]
output:
  tag: report:decision_record
  format: sections
  headings: [Resolved scope, Non-goals, 'Claims, evidence, and decisions', Blocking questions, completeness pass, Verification evidence]
  columns: [ID, Claim or decision, Evidence, Interpretation / next action]
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

# Decision Record

The single source of truth a blackboard produces. It contains only claims that some role actually made.

## When to use
At the end of every board, and whenever the board version increments.

## Produced by
- `board_facilitator`: writes it and owns every line.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:decision_record role=ROLE_ID board=BOARD_ID -->
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
<!-- /report:decision_record -->
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
<!-- report:decision_record role=board_facilitator board=BB-DESIGN-REPLAY -->
# Blackboard: Decision Replay Integration
- Board ID: BB-DESIGN-REPLAY | Version: 1 | Readiness: final-ready | Authority: propose-only
## Resolved scope
Integrate the replay at `/demo`. Keep `/`, `/blackboard`, and both API routes.
## Non-goals
- Persisting replay notes (not requested)
## Claims, evidence, and decisions
| ID | Claim or decision | Evidence | Interpretation / next action |
|---|---|---|---|
| D-1 | Replay stays independent of live API state | user request; C-1 | don't wire replay to /api/* |
## Blocking questions
None. Route choice is reversible.
## Required completeness pass
- integration_architect: no_missing_items
- end_user_advocate: no_missing_items
## Verification evidence
- `pnpm test`: 20 passed
<!-- /report:decision_record -->
```

## Quality checks
- [ ] Every table row cites evidence
- [ ] No claim that no role made
- [ ] Every deferred item has a re-entry condition
- [ ] Readiness is `final-ready` only after all roles return `no_missing_items`
