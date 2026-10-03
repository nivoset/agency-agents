---
name: findings-table
description: Review findings as Finding / Evidence / Severity / Fix rows. Use for any review pass (UX, accessibility, developer experience, art, brand voice) that reports problems with something that already exists or is drafted.
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
```markdown
| # | Finding | Evidence | Severity | Fix | <role-specific columns> |
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
| 1 | Version change not announced | BlackboardApp.jsx:410; SC 4.1.3 | major | aria-live="polite" region with "Version 6 of 10" |
```

## Quality checks
- [ ] Every row has evidence
- [ ] Severity uses the three-level scale
- [ ] Fixes are minimal and specific
