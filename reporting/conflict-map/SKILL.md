---
name: conflict-map
description: Map of a disagreement giving each party's position, interest, and strongest view, plus temperature, stuck point, and the recommended next move and channel. Use before replying to a heated message, thread, or dispute.
---

# Conflict Map

Shows what each side actually needs, so the reply answers that instead of the surface argument.

## When to use
Before responding in any conflict: a thread, an email, a review comment, a family chat, or a team dispute.

## Produced by
- `conflict_mediator`: parties, positions, interests, temperature, stuck point, next move, and channel.
- `steelman_interpreter`: each party's strongest view, its underlying need, and the true part to concede.

## Template
```markdown
| Party | Position | Interest (underlying need) | Strongest view | True part to concede | Temperature (1–5) |
Stuck point: ...
Recommended next move: ... | Channel/timing: ... | Non-negotiables kept: <from boundary_brief>
```

## Core fields (required)
- **Party**: everyone with a stake, including the user.
- **Interest**: the need behind the position (being heard, safety, fairness, status, autonomy).

## How to fill it in
1. Quote positions from the actual messages.
2. Infer interests, and label them as inferences.
3. Steelman each party and find something true to concede.
4. Choose the move and the channel. "Don't reply yet" is a valid move.

## On the board
Interests and concessions are `claim` notes. Non-negotiables come from the [boundary brief](../boundary-brief/SKILL.md). The wording comes from [draft variants](../draft-variants/SKILL.md).

## Example
```markdown
| Teammate | "you never test anything" | stop 3am pages | two pages last week were preventable | 2nd page was preventable | 4 |
Next move: acknowledge + offer pairing on alert rules | Channel: DM, today
```

## Quality checks
- [ ] Every party has an interest
- [ ] Inferences are labeled
- [ ] The move preserves the non-negotiables
