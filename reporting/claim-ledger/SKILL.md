---
name: claim-ledger
description: Ledger separating the claims in a dispute or draft into fact, value, or feeling, each with status, source, and materiality, plus the crux. Use for arguments citing facts, posts making assertions, and decks with contested numbers.
---

# Claim Ledger

Pulls apart the facts, values, and feelings that are tangled together in an argument.

## When to use
Whenever a disagreement or draft contains checkable assertions.

## Produced by
- `fact_disentangler`: owns it.

## Template
```markdown
| # | Claim | Type (fact/value/feeling) | Status (verified/false/disputed/unverifiable) | Source | Material? |
Crux: <the one fact that would change minds> → evidence that would settle it: <...>
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
| 1 | "Outages doubled" (A) | fact | verified by count (2→4); per-deploy rate fell | incident log Q3 | yes |
Crux: should outages be counted per deploy or absolute?
```

## Quality checks
- [ ] Values aren't treated as facts, and facts aren't treated as opinions
- [ ] Every fact status has a source
- [ ] A crux is named
