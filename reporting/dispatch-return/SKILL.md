---
name: dispatch-return
description: Standard payload a blackboard role returns at the end of a dispatch (status, claims/results, evidence, uncertainty, implication/next action, changed paths). Use when finishing any dispatched role task or completeness pass. Every role uses this.
---

# Dispatch Return

The envelope a role hands back to the facilitator. The role's specific report goes inside `claims/results`.

## When to use
At the end of every dispatch, and for the final completeness pass.

## Produced by
- All roles (universal). The facilitator consumes it.

## Template
```markdown
status: passed | blocked | needs_decision | no_missing_items
claims/results:
  - <claim, or the role's report, e.g. a findings_table or risk_register>
evidence:
  - <path:line, note id, URL, command + output>
uncertainty:
  - <what you couldn't verify and why>
implication/next action:
  - <what the board or user should do next>
changed paths:
  - <files written, or "none" for propose-only>
```

## Core fields (required)
- **status**: `no_missing_items` only in the completeness pass, when your role's `done_when` holds. Use `needs_decision` when a choice belongs to the user.
- **claims/results**: your role's report(s), as listed in its `reports` frontmatter.
- **evidence**: every claim traces to something checkable.
- **uncertainty**: say what you don't know. Never leave it blank when you're unsure.
- **implication/next action**: one action per claim, at most.
- **changed paths**: must be empty under `propose-only` or `review-only` authority.

## How to fill it in
1. Produce your role's report(s) using their skills.
2. Pair every claim with evidence, or move it to uncertainty.
3. Check your `done_when` and set the status.

## On the board
Matches the dispatch `return_schema` in `dispatch.yaml`. The facilitator records status and outcome under "Review roles" in the [decision record](../decision-record/SKILL.md).

## Example
```markdown
status: passed
claims/results: [impact_map: 5 rows, 2 high-risk]
evidence: [archive app/globals.css:1-12, next.config.ts]
uncertainty: [did not run the build; only read config]
implication/next action: [scope replay CSS under .replay-root before porting]
changed paths: none
```

## Quality checks
- [ ] Status is consistent with `done_when`
- [ ] No claim without evidence
- [ ] Changed paths respect the dispatch's authority
