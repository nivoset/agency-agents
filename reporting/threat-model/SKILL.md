---
name: threat-model
description: STRIDE-style threat model listing asset, threat, likelihood, impact, fix, and verification. Use for new trust boundaries, auth changes, user input, LLM features reading untrusted content, and new dependencies.
report_id: threat_model
title: Threat Model
version: 1
universal: false
tags: [security, risk]
produced_by: [security_reviewer]
output:
  tag: report:threat_model
  format: table
  columns: [Asset, Threat, Likelihood, Impact, Fix, Verify]
  enums:
    Likelihood: [L, M, H, low, medium, high]
    Impact: [L, M, H, low, medium, high]
  min_rows: 1
---

# Threat Model

Shows how a feature can be abused, and the safest fix that still ships.

## When to use
Whenever a change adds a trust boundary, input, privilege, or dependency.

## Produced by
- `security_reviewer`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:threat_model role=ROLE_ID board=BOARD_ID -->
Trust boundaries: <list>
| Asset | Threat (STRIDE / LLM Top 10) | Likelihood | Impact | Fix | Verify |
<!-- /report:threat_model -->
```

## Core fields (required)
- **Asset**: what is worth protecting (data, a privilege, cost, reputation).
- **Threat**: the category plus a concrete scenario.
- **Likelihood** / **Impact**: with rationale.
- **Fix**: the safest workable control.
- **Verify**: a test or check that proves the fix.

## How to fill it in
1. Draw the trust boundaries in text.
2. Walk STRIDE, plus prompt-injection and tool-misuse threats for any LLM feature.
3. Pick the safest fix and define its verification.

## On the board
High and critical threats are `claim` notes with `high` confidence, and they block completeness until fixed or accepted by the user.

## Example

```markdown
<!-- report:threat_model role=security_reviewer board=BB-DESIGN-REPLAY -->
Trust boundaries: browser ↔ /api/blackboard; orchestrator ↔ model API
| Asset | Threat | Likelihood | Impact | Fix | Verify |
|---|---|---|---|---|---|
| Board page | Tampering/XSS: model output rendered as markdown | M | H | sanitize with rehype-sanitize | test renders a script tag as text |
<!-- /report:threat_model -->
```

## Quality checks
- [ ] Every new boundary is covered
- [ ] Every fix has a verify step
- [ ] No exploit payloads against real third-party systems
