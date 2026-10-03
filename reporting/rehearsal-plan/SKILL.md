---
name: rehearsal-plan
description: Delivery readiness plan covering rehearsal runs, timing marks, demo fallbacks, and a Q&A bank. Use before any live or recorded talk, demo, or high-stakes spoken conversation.
---

# Rehearsal Plan

Makes the talk survive the room.

## When to use
Before any live or recorded talk, demo, or prepared hard conversation.

## Produced by
- `delivery_coach`: owns it.

## Template
```markdown
Rehearsals: | Run | Date | Full length? | Duration | Notes |
Timing marks: <beat → minute>
Demo fallback: | Demo | Live dependency | Fallback asset | Tested? |
Q&A bank: | Question | Answer (≤30s) |
Opening / closing lines: <memorized text>
```

## Core fields (required)
- **Rehearsals**: at least two full-length timed runs.
- **Timing marks**: checkpoints from the [beat chart](../beat-chart/SKILL.md).
- **Demo fallback**: a tested recording or screenshots for every live dependency.
- **Q&A bank**: the ten most likely questions, drawn from the [objection map](../objection-map/SKILL.md).

## How to fill it in
1. Schedule the runs and record their durations.
2. Set timing marks, and cut content when runs exceed the slot.
3. Build and test the demo fallbacks, then write the Q&A answers.

## On the board
Overruns are `claim` notes to `presentation_story_architect`, asking for cuts. Untested fallbacks block completeness.

## Example
```markdown
| 2 | 10/10 | yes | 27:40 / 25:00 | cut example 2 in section 3 |
| Live API demo | network | demo.mp4 (90s) | yes |
```

## Quality checks
- [ ] Two full timed runs within the slot
- [ ] Every live dependency has a tested fallback
- [ ] Opening and closing lines are memorized
