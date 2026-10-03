---
name: claim-ledger
description: Ledger separating the claims in a dispute or draft into fact, value, or feeling, each with status, source, and materiality, plus the crux. Use for arguments citing facts, posts making assertions, and decks with contested numbers.
report_id: claim_ledger
title: Claim Ledger
version: 1
universal: false
tags: [fact-checking, evidence]
produced_by: [fact_disentangler]
output:
  tag: report:claim_ledger
  format: table
  columns: [Claim, Type, Status, Source, Material]
  labels: [Crux]
  enums:
    Type: [fact, value, feeling]
    Status: [verified, 'false', disputed, unverifiable, n/a]
    Material: ['yes', 'no']
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

# Claim Ledger

Pulls apart the facts, values, and feelings that are tangled together in an argument.

## When to use
Whenever a disagreement or draft contains checkable assertions.

## Produced by
- `fact_disentangler`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:claim_ledger role=ROLE_ID board=BOARD_ID -->
| # | Claim | Type (fact/value/feeling) | Status (verified/false/disputed/unverifiable) | Source | Material? |
Crux: <the one fact that would change minds> → evidence that would settle it: <...>
<!-- /report:claim_ledger -->
```

## Core fields (required)
- **Claim**: quoted or closely paraphrased, with who said it.
- **Type**: fact claims are checkable. Value and feeling claims are not checked, only acknowledged.
- **Status**: for facts only.
- **Source**: primary where possible.
- **Material**: whether it matters to the main point. Don't derail over trivia.

## How to fill it in
1. Extract every assertion and classify it.
2. Check the material facts against primary sources.
3. Name the crux and the evidence that would settle it.

## On the board
Verified or false facts are `answer` notes. The crux goes to `diplomatic_wordsmith`, so the reply addresses it. For numbers, coordinate with [chart specs](../chart-spec/SKILL.md).

## Example

```markdown
<!-- report:claim_ledger role=fact_disentangler board=BB-DESIGN-REPLAY -->
| # | Claim | Type | Status | Source | Material |
|---|---|---|---|---|---|
| 1 | "Outages doubled" (A) | fact | verified | incident log Q3: 2 → 4 | yes |
| 2 | "Failure rate per deploy fell" (B) | fact | verified | deploy log Q3 | yes |
| 3 | "You don't care about on-call" (A) | feeling | n/a | none | no |
Crux: count outages per deploy or in absolute terms? Agreeing on the denominator settles it.
<!-- /report:claim_ledger -->
```

## Quality checks
- [ ] Values aren't treated as facts, and facts aren't treated as opinions
- [ ] Every fact status has a source
- [ ] A crux is named
