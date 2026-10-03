---
name: board-note
description: Format for a single note posted to a blackboard (claim, question, or answer, with confidence and refersTo). Use whenever a blackboard role contributes during a round. Every role uses this.
report_id: board_note
title: Board Note
version: 1
universal: true
tags: [evidence, synthesis]
output:
  tag: report:board_note
  format: yaml
  keys: [kind, body, confidence, refersTo]
  enums:
    kind: [claim, question, answer]
    confidence: [low, medium, high]
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

# Board Note

The unit of conversation on a blackboard. Each role posts **one** note per round.

## When to use
Every round, for every seated role. Use it in place of free-form chat on the board.

## Produced by
- All roles (universal). Each role's `note_bias` frontmatter says which kinds it should favor.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate.py` in this skill; see `validation` in the frontmatter). Put your own role id in `role=` and the board id in `board=`.
```yaml
<!-- report:board_note role=ROLE_ID board=BOARD_ID -->
kind: claim | question | answer
body: "1–4 sentences. Concrete. Cites a path, a note id, or a source."
confidence: low | medium | high
refersTo: [n-3, n-7]   # or null
<!-- /report:board_note -->
```

## Core fields (required)
- **kind**: `claim` is a recommendation or observation. `question` is something that must be resolved, and names who should answer it or what evidence would settle it. `answer` directly resolves an open question.
- **body**: one point only. If you have two points, post the second one next round.
- **confidence**: `high` only when you can cite evidence. Opinion is `low` or `medium`.
- **refersTo**: ids of the notes you build on or challenge. Use `null` only for a new thread.

## How to fill it in
1. Read the whole board, including notes posted earlier in this round.
2. Skip anything already said. Add new signal, or answer an open question in your area.
3. Pick the kind, guided by your `note_bias`. Write the body, set confidence, and link with `refersTo`.

## On the board
Notes map 1:1 to the blackboard skill's `NoteSchema`. The facilitator later lifts claims that survive into the [decision record](../decision-record/SKILL.md) table, with the note id as evidence.

## Example

```yaml
<!-- report:board_note role=end_user_advocate board=BB-DESIGN-REPLAY -->
- kind: question
  body: "What does the user see if the stream errors mid-round? `use-blackboard-stream.ts` has no error branch. For backend_engineer."
  confidence: high
  refersTo: [n-4]
<!-- /report:board_note -->
```

## Quality checks
- [ ] One point, 1–4 sentences
- [ ] Not a repeat of an existing note
- [ ] `high` confidence has cited evidence
- [ ] Questions name who answers, or what evidence settles them
