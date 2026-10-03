---
name: ops-plan
description: Operational readiness plan covering deploy strategy, tested rollback, SLOs, alerts with owners, and a runbook. Use before shipping services, launches, live events, or pipeline changes.
report_id: ops_plan
title: Ops Plan
version: 1
universal: false
tags: [operations]
produced_by: [reliability_engineer]
output:
  tag: report:ops_plan
  format: fields
  labels: [Deploy, Rollback, SLOs, Alerts, Runbook]
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

# Ops Plan

Makes a change shippable, observable, and recoverable.

## When to use
Before any production deploy of new or changed services, and before launches.

## Produced by
- `reliability_engineer`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:ops_plan role=ROLE_ID board=BOARD_ID -->
Deploy: <strategy: flag / canary / blue-green / big-bang (justify)>
Rollback: <steps> — tested: <date/evidence>
SLOs: <indicator, target, window>
Alerts: | Alert | Condition | Owner | Response |
Runbook: | Failure mode | Detect | Mitigate | Recover |
<!-- /report:ops_plan -->
```

## Core fields (required)
- **Deploy**: strategy, with a reason.
- **Rollback**: steps and test evidence.
- **SLOs**: user-impact indicators.
- **Alerts**: each with an owner and a response.
- **Runbook**: the top failure modes.

## How to fill it in
1. Pick the deploy strategy based on risk.
2. Write and test the rollback.
3. Define SLOs, then the alerts that protect them, then the runbook entries.

## On the board
Missing rollback is a `question` note that blocks completeness. The plan's evidence goes into "Verification evidence" in the [decision record](../decision-record/SKILL.md).

## Example

```markdown
<!-- report:ops_plan role=reliability_engineer board=BB-DESIGN-REPLAY -->
Deploy: behind the REPLAY_ENABLED flag
Rollback: flip the flag (tested on preview, 10/02)
SLOs: SSE stream success ≥ 99% over 7 days
Alerts: SSE error rate > 2% for 5 minutes → on-call checks orchestrator logs
Runbook: stream hangs → restart worker → replay session from DB
<!-- /report:ops_plan -->
```

## Quality checks
- [ ] Rollback is tested
- [ ] Every alert has an owner
- [ ] The runbook covers the top three failure modes
