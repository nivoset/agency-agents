---
name: risk-register
description: Ranked register of risks with likelihood, impact, mitigation, and status (refuted, mitigated, accepted). Use for pre-mortems, red-teaming, test-risk matrices, and architecture risk sections.
---

# Risk Register

Lists what could go wrong, ranked, and records what the board decided to do about each risk.

## When to use
Before expensive or irreversible decisions, when planning verification, or when a board converges too quickly.

## Produced by
- `red_team_skeptic`: attacks on the leading proposal, each with a falsifying test as its mitigation.
- `qa_test_strategist`: the test risk matrix, with each risk's mitigation as the covering test.
- `software_architect`: architectural risks for the proposal.

## Template
```markdown
| # | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner | Status |
```

## Core fields (required)
- **Risk**: the specific failure, stated as "If X then Y".
- **Likelihood** and **Impact**: L, M, or H, with a one-phrase rationale where it isn't obvious.
- **Mitigation**: a test, check, design change, or monitoring step. For red-team risks, the falsifying test.
- **Status**: `open`, `refuted`, `mitigated`, or `accepted`. Accepted risks need a reason.

## How to fill it in
1. List candidate risks, including the load-bearing assumption.
2. Rate them, keep the top 5–10, and drop noise.
3. Attach a mitigation to each, and update the status as evidence arrives.

## On the board
Post the top risk as a `claim` or `question` note. When evidence refutes a risk, post an `answer` linking to it and set status `refuted`. The facilitator carries accepted risks into the [decision record](../decision-record/SKILL.md).

## Example
```markdown
| 1 | If replay code calls /api/*, demo burns tokens | M | H | test mocks fetch, asserts 0 calls | test_automation_engineer | mitigated |
```

## Quality checks
- [ ] Every risk has a mitigation or an explicit acceptance
- [ ] The register is ranked, highest risk first
- [ ] No `open` high-high risk at completeness
