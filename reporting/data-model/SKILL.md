---
name: data-model
description: Data model with entities, fields, invariants, indexes, retention, and migration (up/backfill/down). Use for new persistent state, schema changes, save formats, or analytics events.
---

# Data Model

Shapes data that will outlive the code, and makes every change reversible.

## When to use
For any new or changed persistent data, including game saves and analytics events.

## Produced by
- `data_architect`: owns it.

## Template
```markdown
| Entity | Fields (type) | Invariants | Indexes | Retention |
Migration: up: <...> | backfill: <...> | down: <...> (tested? y/n)
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
| Note | id, session_id, round, role_id, kind, body, confidence, refers_to[] | round ≥ 1; refers_to ids exist | (session_id, round) | with session; deleted on session delete |
```

## Quality checks
- [ ] Every index maps to an access pattern
- [ ] PII is marked and minimized
- [ ] Rollback is tested
