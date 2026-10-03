---
name: interface-contract
description: Contract table for components or endpoints, covering interface, inputs, outputs, errors, and role-specific columns (state owner, a11y, idempotency, timeout). Use when designing or reviewing APIs, components, events, or module boundaries.
report_id: interface_contract
title: Interface Contract
version: 1
universal: false
tags: [frontend, backend, integration]
produced_by: [backend_engineer, frontend_engineer]
output:
  tag: report:interface_contract
  format: table
  columns: [Interface, Input, Output, Errors]
  min_rows: 1
---

# Interface Contract

Defines what goes in and what comes out at a boundary, and what happens when it fails.

## When to use
For new or changed endpoints, components, events, or module interfaces.

## Produced by
- `backend_engineer`: endpoints and services (schemas, idempotency, timeouts).
- `frontend_engineer`: components (props, events, state owner, keyboard/ARIA).

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:interface_contract role=ROLE_ID board=BOARD_ID -->
| Interface | Input | Output | Errors | <role columns: State owner / Keyboard-ARIA / Idempotent? / Timeout> |
<!-- /report:interface_contract -->
```

## Core fields (required)
- **Interface**: the endpoint (`POST /api/blackboard`) or component (`<NoteCard>`).
- **Input**: request schema or props, typed. Link the zod or TS type where it exists.
- **Output**: response schema, stream event types, or emitted events.
- **Errors**: every failure mode, and what the caller sees for each.

## How to fill it in
1. List every boundary the change adds or alters.
2. Define the inputs and outputs as types. Point to source.
3. Enumerate errors, including timeouts, invalid input, and empty states.

## On the board
Contract disagreements between frontend and backend show up as `question` notes. Settle them with an `answer` that updates the row. Each error row should have a test in the [test plan](../test-plan/SKILL.md).

## Example

```markdown
<!-- report:interface_contract role=backend_engineer board=BB-DESIGN-REPLAY -->
| Interface | Input | Output | Errors | Idempotent? | Timeout |
|---|---|---|---|---|---|
| GET /api/blackboard?sessionId | sessionId: string | SSE events: roles, note, synthesis, done, error | 404 unknown session; error event then close on failure | yes | 120s |
<!-- /report:interface_contract -->
```

## Quality checks
- [ ] Every error has a caller-visible behavior
- [ ] Types are linked to source
- [ ] Breaking changes are flagged
