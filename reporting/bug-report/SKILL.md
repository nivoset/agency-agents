---
name: bug-report
description: Reproducible defect reports with steps, expected, actual, environment, severity, and root-cause cluster. Use for exploratory testing, bug bashes, playtest bugs, and demo rehearsals.
---

# Bug Report

A defect someone else can reproduce on the first try.

## When to use
Whenever testing finds a defect, whether in an exploratory charter, a bug bash, a playtest, or a rehearsal.

## Produced by
- `exploratory_tester`: charter findings, clustered by root cause.
- `playtest_analyst`: bugs separated from feel, clarity, and balance issues.

## Template
```markdown
Charter: <area> / <time-box>
| # | Title | Steps | Expected | Actual | Environment | Severity | Cluster |
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
| 3 | Double-click Next skips a version | 1. Open /demo at v4 2. Double-click Next | v5 | v6 | Chrome 129, macOS, commit 79176aa | major | debounce |
```

## Quality checks
- [ ] Reproduced at least twice
- [ ] Environment is complete
- [ ] Duplicates merged into clusters
