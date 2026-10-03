---
name: test-plan
description: Maps acceptance criteria to tests at the right level, with determinism controls, CI status, and recorded evidence. Use when planning verification for a change, automating checks, or proving a release is ready.
report_id: test_plan
title: Test Plan
version: 1
universal: false
tags: [testing]
produced_by: [qa_test_strategist, test_automation_engineer]
output:
  tag: report:test_plan
  format: table
  columns: [Acceptance criterion, Test, Level, Evidence]
  enums:
    Level: [unit, component, integration, e2e, manual]
  min_rows: 1
---

# Test Plan

Defines what "verified" means for this change.

## When to use
For any implementation or integration, and before a release decision.

## Produced by
- `qa_test_strategist`: the criteria-to-test map, regression list, and release criteria.
- `test_automation_engineer`: tool choice, determinism controls, CI wiring, and run evidence.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:test_plan role=ROLE_ID board=BOARD_ID -->
| Acceptance criterion | Test | Level (unit/component/integration/e2e/manual) | Tool | In CI? | Evidence |
Regression (existing flows): <flow> → <test>
Release criteria: <blocking thresholds>
<!-- /report:test_plan -->
```

## Core fields (required)
- **Acceptance criterion**: links to an [acceptance case](../acceptance-cases/SKILL.md) or ticket.
- **Test**: a file and test name, or manual steps.
- **Level**: the lowest level that gives confidence.
- **Evidence**: the command run, with its result summary (`pnpm test` → 20 passed).

## How to fill it in
1. Import the acceptance cases and the risk matrix.
2. Map each criterion to a test, and add regression tests for the flows the change touches.
3. Automate deterministically, then record each command and its output.

## On the board
Post uncovered criteria as `question` notes. Post evidence as `answer` notes. "Verification evidence" in the [decision record](../decision-record/SKILL.md) comes from this plan's Evidence column.

## Example

```markdown
<!-- report:test_plan role=qa_test_strategist board=BB-DESIGN-REPLAY -->
| Acceptance criterion | Test | Level | Tool | In CI? | Evidence |
|---|---|---|---|---|---|
| BB-101 arrow keys ignored in textarea | timeline.test.jsx "ignores editable targets" | component | vitest | yes | `pnpm test` → pass |
| BB-107 /replay redirects to /demo | open /replay in a browser | manual | browser | no | 308 redirect to /demo |
<!-- /report:test_plan -->
```

## Quality checks
- [ ] Every criterion has a test
- [ ] Touched existing flows have regression coverage
- [ ] No skipped or disabled tests
- [ ] Every Evidence cell holds a real command and result
