---
name: adr
description: Architecture Decision Record covering context, options considered, decision, and consequences. Use for any one-way-door technical choice (framework, storage, protocol, boundary, major dependency).
report_id: adr
title: Architecture Decision Record
version: 1
universal: false
tags: [architecture]
produced_by: [software_architect]
output:
  tag: report:adr
  format: fields
  labels: [Context, Options, Decision, Consequences]
  enums:
    Status: [proposed, accepted, superseded]
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

# Architecture Decision Record

Records why a hard-to-reverse choice was made, and what was rejected.

## When to use
For every decision the board labels a one-way door, and for any choice someone will later ask "why did we do this?"

## Produced by
- `software_architect`: owns ADRs for system shape.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:adr role=ROLE_ID board=BOARD_ID -->
## ADR-n: <decision title>
- Status: proposed | accepted | superseded by ADR-m
- Context: <forces, constraints, evidence>
- Options:
  1. <option> — pros / cons
  2. <option> — pros / cons
- Decision: <chosen option and why it beat the others>
- Consequences: <what gets easier, harder, and what we must now do>
<!-- /report:adr -->
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
<!-- report:adr role=software_architect board=BB-DESIGN-REPLAY -->
## ADR-1: Serve replay as a client-only route
- Status: accepted
- Context: the replay is deterministic, and the live board streams from /api/blackboard (C-1)
- Options: 1. /demo client route; 2. reuse /blackboard/[id] with a replay flag
- Decision: option 1, because it keeps replay isolated from live API state
- Consequences: note rendering is duplicated unless NoteCard is shared
<!-- /report:adr -->
```

## Quality checks
- [ ] At least two options
- [ ] Negative consequences listed
- [ ] Context cites evidence
