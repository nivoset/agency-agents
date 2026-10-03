---
name: rehearsal-plan
description: Delivery readiness plan covering rehearsal runs, timing marks, demo fallbacks, and a Q&A bank. Use before any live or recorded talk, demo, or high-stakes spoken conversation.
report_id: rehearsal_plan
title: Rehearsal Plan
version: 1
universal: false
tags: [delivery]
produced_by: [delivery_coach]
output:
  tag: report:rehearsal_plan
  format: fields
  labels: [Rehearsals, Timing marks, Demo fallback, Q&A bank]
  min_rows: 1
---

# Rehearsal Plan

Makes the talk survive the room.

## When to use
Before any live or recorded talk, demo, or prepared hard conversation.

## Produced by
- `delivery_coach`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:rehearsal_plan role=ROLE_ID board=BOARD_ID -->
Rehearsals: | Run | Date | Full length? | Duration | Notes |
Timing marks: <beat → minute>
Demo fallback: | Demo | Live dependency | Fallback asset | Tested? |
Q&A bank: | Question | Answer (≤30s) |
Opening / closing lines: <memorized text>
<!-- /report:rehearsal_plan -->
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
<!-- report:rehearsal_plan role=delivery_coach board=BB-DESIGN-REPLAY -->
Rehearsals:
| Run | Date | Full length? | Duration | Notes |
|---|---|---|---|---|
| 1 | 10/08 | yes | 29:10 of 25:00 | cut example 2 in section 3 |
| 2 | 10/10 | yes | 24:40 of 25:00 | on time |
Timing marks: hook → 1:30, insight → 5:30, demo → 12:00, ask → 23:00
Demo fallback: live API demo → demo.mp4 (90s), tested 10/10
Q&A bank: "Does it work offline?" → "No. The recording shows the flow if the network drops."
<!-- /report:rehearsal_plan -->
```

## Quality checks
- [ ] Two full timed runs within the slot
- [ ] Every live dependency has a tested fallback
- [ ] Opening and closing lines are memorized
