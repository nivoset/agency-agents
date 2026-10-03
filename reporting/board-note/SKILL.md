---
name: board-note
description: Format for a single note posted to a blackboard (claim, question, or answer, with confidence and refersTo). Use whenever a blackboard role contributes during a round. Every role uses this.
---

# Board Note

The unit of conversation on a blackboard. Each role posts **one** note per round.

## When to use
Every round, for every seated role. Use it in place of free-form chat on the board.

## Produced by
- All roles (universal). Each role's `note_bias` frontmatter says which kinds it should favor.

## Template
```yaml
kind: claim | question | answer
body: "1–4 sentences. Concrete. Cites a path, a note id, or a source."
confidence: low | medium | high
refersTo: [n-3, n-7]   # or null
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
kind: question
body: "What does the user see if the stream errors mid-round? `use-blackboard-stream.ts` has no error branch. For backend_engineer."
confidence: high
refersTo: [n-4]
```

## Quality checks
- [ ] One point, 1–4 sentences
- [ ] Not a repeat of an existing note
- [ ] `high` confidence has cited evidence
- [ ] Questions name who answers, or what evidence settles them
