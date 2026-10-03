---
name: adr
description: Architecture Decision Record covering context, options considered, decision, and consequences. Use for any one-way-door technical choice (framework, storage, protocol, boundary, major dependency).
---

# Architecture Decision Record

Records why a hard-to-reverse choice was made, and what was rejected.

## When to use
For every decision the board labels a one-way door, and for any choice someone will later ask "why did we do this?"

## Produced by
- `software_architect`: owns ADRs for system shape.

## Template
```markdown
## ADR-n: <decision title>
- Status: proposed | accepted | superseded by ADR-m
- Context: <forces, constraints, evidence>
- Options:
  1. <option> — pros / cons
  2. <option> — pros / cons
- Decision: <chosen option and why it beat the others>
- Consequences: <what gets easier, harder, and what we must now do>
```

## Core fields (required)
- **Context**: facts and constraints, with evidence paths.
- **Options**: at least two real alternatives, including "do nothing" where viable.
- **Decision**: the choice, plus the deciding reason.
- **Consequences**: both positive and negative, with follow-up work.

## How to fill it in
1. Name the decision and confirm it really is a one-way door.
2. Gather the context from the repository and requirements. Ask `prior_art_scout` for precedents.
3. Compare the options honestly, then decide and list the consequences.

## On the board
Post the proposed decision as a `claim` note, inviting `red_team_skeptic` to challenge it. Once accepted, the facilitator records it as `D-n` citing ADR-n.

## Example
```markdown
## ADR-1: Serve replay as a client-only route
- Options: 1. /demo client route; 2. reuse /blackboard/[id] with a replay flag
- Decision: 1. It keeps replay isolated from live API state (C-1)
- Consequences: duplicated note rendering; must share NoteCard
```

## Quality checks
- [ ] At least two options
- [ ] Negative consequences listed
- [ ] Context cites evidence
