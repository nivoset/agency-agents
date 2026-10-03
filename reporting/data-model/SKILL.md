---
name: data-model
description: Data model with entities, fields, invariants, indexes, retention, and migration (up/backfill/down). Use for new persistent state, schema changes, save formats, or analytics events.
report_id: data_model
title: Data Model
version: 1
universal: false
tags: [data]
produced_by: [data_architect]
output:
  tag: report:data_model
  format: table
  columns: [Entity, Fields, Invariants, Indexes, Retention]
  labels: [Migration]
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

# Data Model

Shapes data that will outlive the code, and makes every change reversible.

## When to use
For any new or changed persistent data, including game saves and analytics events.

## Produced by
- `data_architect`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:data_model role=ROLE_ID board=BOARD_ID -->
| Entity | Fields (type) | Invariants | Indexes | Retention |
Migration: up: <...> | backfill: <...> | down: <...> (tested? y/n)
<!-- /report:data_model -->
```

## Core fields (required)
- **Entity**: a domain name, not a table-implementation name.
- **Fields**: names and types, with PII marked.
- **Invariants**: rules that must always hold.
- **Indexes**: tied to named access patterns.
- **Retention**: how long data is kept and why, plus the deletion path.
- **Migration**: additive-first, with a backfill and a tested rollback.

## How to fill it in
1. Model the entities and invariants from the domain.
2. List the access patterns, then the indexes that serve them.
3. Write the migration and rollback, and get them tested.

## On the board
Ask early whether data needs to persist at all (`question` to `product_manager`). Destructive migrations are a [risk register](../risk-register/SKILL.md) item.

## Example

```markdown
<!-- report:data_model role=data_architect board=BB-DESIGN-REPLAY -->
| Entity | Fields | Invariants | Indexes | Retention |
|---|---|---|---|---|
| Note | id, session_id, round, role_id, kind, body, confidence, refers_to[] | round ≥ 1; refers_to ids exist | (session_id, round) | deleted with its session |
Migration: up: create notes table | backfill: none | down: drop table (tested: yes)
<!-- /report:data_model -->
```

## Quality checks
- [ ] Every index maps to an access pattern
- [ ] PII is marked and minimized
- [ ] Rollback is tested
