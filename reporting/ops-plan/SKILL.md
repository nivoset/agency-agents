---
name: ops-plan
description: Operational readiness plan covering deploy strategy, tested rollback, SLOs, alerts with owners, and a runbook. Use before shipping services, launches, live events, or pipeline changes.
---

# Ops Plan

Makes a change shippable, observable, and recoverable.

## When to use
Before any production deploy of new or changed services, and before launches.

## Produced by
- `reliability_engineer`: owns it.

## Template
```markdown
Deploy: <strategy: flag / canary / blue-green / big-bang (justify)>
Rollback: <steps> — tested: <date/evidence>
SLOs: <indicator, target, window>
Alerts: | Alert | Condition | Owner | Response |
Runbook: | Failure mode | Detect | Mitigate | Recover |
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
Deploy: behind REPLAY_ENABLED flag | Rollback: flip flag (tested on preview 10/02)
Alerts: | SSE error rate > 2% 5m | on-call | check orchestrator logs |
```

## Quality checks
- [ ] Rollback is tested
- [ ] Every alert has an owner
- [ ] The runbook covers the top three failure modes
