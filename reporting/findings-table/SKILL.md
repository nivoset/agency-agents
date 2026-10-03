---
name: findings-table
description: Review findings as Finding / Evidence / Severity / Fix rows. Use for any review pass (UX, accessibility, developer experience, art, brand voice) that reports problems with something that already exists or is drafted.
report_id: findings_table
title: Findings Table
version: 1
universal: false
tags: [evidence, risk]
produced_by: [accessibility_inclusion_reviewer, art_director, brand_voice_guardian, developer_experience_advocate, end_user_advocate]
output:
  tag: report:findings_table
  format: table
  columns: [Finding, Evidence, Severity, Fix]
  enums:
    Severity: [blocker, major, minor]
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

# Findings Table

The shared format for review output. Roles add their own columns, such as criterion, principle, or who is affected, but never drop the core four.

## When to use
Whenever a role is reviewing an artifact (code, flow, deck, asset, post) rather than proposing a new one.

## Produced by
- `end_user_advocate`: user-impact findings, adding a who-is-affected column.
- `accessibility_inclusion_reviewer`: findings mapped to WCAG or game-accessibility criteria.
- `developer_experience_advocate`: API, doc, and error-message findings.
- `art_director`: art review notes, each tagged with the principle at stake.
- `brand_voice_guardian`: off-voice lines, each with a rewrite.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:findings_table role=ROLE_ID board=BOARD_ID -->
| # | Finding | Evidence | Severity | Fix | <role-specific columns> |
<!-- /report:findings_table -->
```

## Core fields (required)
- **Finding**: what is wrong, in one sentence, naming the artifact or location.
- **Evidence**: a path and line, a screenshot, a criterion id, a quote, or repro steps.
- **Severity**: `blocker` (the task can't be completed or ship), `major`, or `minor`.
- **Fix**: the minimum change that resolves it, not a redesign.

## How to fill it in
1. Review against your role's standard (criteria, style guide, voice chart, user path).
2. Log one row per distinct problem, and merge duplicates.
3. Sort by severity, blockers first.

## On the board
Post blockers as `claim` notes with `high` confidence. The full table goes in `claims/results` of your [dispatch return](../dispatch-return/SKILL.md). In the completeness pass, `no_missing_items` means no blocker or major row remains open.

## Example

```markdown
<!-- report:findings_table role=accessibility_inclusion_reviewer board=BB-DESIGN-REPLAY -->
| # | Finding | Evidence | Severity | Fix | Criterion |
|---|---|---|---|---|---|
| 1 | Version change not announced | BlackboardApp.jsx:410 | major | aria-live="polite" region reading "Version 6 of 10" | WCAG 2.2 SC 4.1.3 |
| 2 | Tool rail buttons have no handler | ToolRail.jsx:22 | major | disable and label "Coming later" | WCAG 2.2 SC 4.1.2 |
<!-- /report:findings_table -->
```

## Quality checks
- [ ] Every row has evidence
- [ ] Severity uses the three-level scale
- [ ] Fixes are minimal and specific
