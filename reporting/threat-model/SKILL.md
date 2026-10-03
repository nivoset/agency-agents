---
name: threat-model
description: STRIDE-style threat model listing asset, threat, likelihood, impact, fix, and verification. Use for new trust boundaries, auth changes, user input, LLM features reading untrusted content, and new dependencies.
---

# Threat Model

Shows how a feature can be abused, and the safest fix that still ships.

## When to use
Whenever a change adds a trust boundary, input, privilege, or dependency.

## Produced by
- `security_reviewer`: owns it.

## Template
```markdown
Trust boundaries: <list>
| Asset | Threat (STRIDE / LLM Top 10) | Likelihood | Impact | Fix | Verify |
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
| Board page | Tampering/XSS: model output rendered as markdown | M | H | sanitize with rehype-sanitize | test renders <script> as text |
```

## Quality checks
- [ ] Every new boundary is covered
- [ ] Every fix has a verify step
- [ ] No exploit payloads against real third-party systems
