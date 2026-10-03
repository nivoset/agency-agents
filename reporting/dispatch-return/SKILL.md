---
name: dispatch-return
description: Standard payload a blackboard role returns at the end of a dispatch (status, claims/results, evidence, uncertainty, implication/next action, changed paths). Use when finishing any dispatched role task or completeness pass. Every role uses this.
report_id: dispatch_return
title: Dispatch Return
version: 1
universal: true
tags: [evidence, synthesis]
output:
  tag: report:dispatch_return
  format: yaml
  keys: [status, claims/results, evidence, uncertainty, implication/next action, changed paths]
  enums:
    status: [passed, blocked, needs_decision, no_missing_items]
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

# Dispatch Return

The envelope a role hands back to the facilitator. The role's specific report goes inside `claims/results`.

## When to use
At the end of every dispatch, and for the final completeness pass.

## Produced by
- All roles (universal). The facilitator consumes it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:dispatch_return role=ROLE_ID board=BOARD_ID -->
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
<!-- /report:dispatch_return -->
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

```yaml
<!-- report:dispatch_return role=integration_architect board=BB-DESIGN-REPLAY -->
status: passed
claims/results:
  - "impact_map: 5 rows, 2 high-risk (returned as its own report block)"
evidence:
  - "archive app/globals.css:1-12"
  - next.config.ts
uncertainty:
  - "Did not run the build; read config only"
implication/next action:
  - "Scope replay CSS under .replay-root before porting"
changed paths: []
<!-- /report:dispatch_return -->
```

## Quality checks
- [ ] Status is consistent with `done_when`
- [ ] No claim without evidence
- [ ] Changed paths respect the dispatch's authority
