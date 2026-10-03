---
name: bug-report
description: Reproducible defect reports with steps, expected, actual, environment, severity, and root-cause cluster. Use for exploratory testing, bug bashes, playtest bugs, and demo rehearsals.
report_id: bug_report
title: Bug Report
version: 1
universal: false
tags: [testing]
produced_by: [exploratory_tester, playtest_analyst]
output:
  tag: report:bug_report
  format: table
  columns: [Steps, Expected, Actual, Environment, Severity]
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

# Bug Report

A defect someone else can reproduce on the first try.

## When to use
Whenever testing finds a defect, whether in an exploratory charter, a bug bash, a playtest, or a rehearsal.

## Produced by
- `exploratory_tester`: charter findings, clustered by root cause.
- `playtest_analyst`: bugs separated from feel, clarity, and balance issues.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:bug_report role=ROLE_ID board=BOARD_ID -->
Charter: <area> / <time-box>
| # | Title | Steps | Expected | Actual | Environment | Severity | Cluster |
<!-- /report:bug_report -->
```

## Core fields (required)
- **Steps**: the minimal numbered steps from a known state.
- **Expected** / **Actual**: one sentence each.
- **Environment**: build or commit, browser or device, OS, and relevant settings (zoom, reduced motion, network).
- **Severity**: `blocker`, `major`, or `minor`.

## How to fill it in
1. Reproduce twice and trim the steps to the minimum.
2. Capture evidence (recording, log, screenshot) and link it in the title or steps.
3. Cluster rows by suspected root cause, and merge duplicates.

## On the board
Post blockers immediately as `claim` notes with `high` confidence. The full list goes in your [dispatch return](../dispatch-return/SKILL.md). Each blocker needs an owner before completeness.

## Example

```markdown
<!-- report:bug_report role=exploratory_tester board=BB-DESIGN-REPLAY -->
Charter: timeline controls / 30 min
| # | Title | Steps | Expected | Actual | Environment | Severity | Cluster |
|---|---|---|---|---|---|---|---|
| 3 | Double-click Next skips a version | 1. Open /demo at v4 2. Double-click Next | v5 | v6 | Chrome 129, macOS 15, commit 79176aa | major | debounce |
<!-- /report:bug_report -->
```

## Quality checks
- [ ] Reproduced at least twice
- [ ] Environment is complete
- [ ] Duplicates merged into clusters
