---
name: objection-map
description: Audience segments with the objections or misreadings each will have and the response that answers them. Use for pitches, talks, launch posts, and sensitive announcements.
report_id: objection_map
title: Objection Map
version: 1
universal: false
tags: [audience, community, risk]
produced_by: [audience_proxy, community_response_forecaster]
output:
  tag: report:objection_map
  format: table
  columns: [Segment, Objection, Response, Status]
  enums:
    Status: [answered, partially, open]
  min_rows: 1
---

# Objection Map

Answers the hard questions in the content, before the audience asks them.

## When to use
For any persuasive talk, pitch, or post, and before anything that could be misread publicly.

## Produced by
- `audience_proxy`: listener segments, priors, objections, and where each is answered in the talk.
- `community_response_forecaster`: likely replies and misreadings, copy fixes, and the reply bank.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:objection_map role=ROLE_ID board=BOARD_ID -->
| Segment | Priors / likely reaction | Objection | Response | Status |
Reply bank (social): <question → reply> | Rules: reply / ignore / escalate | Monitor: <who, window>
<!-- /report:objection_map -->
```

## Core fields (required)
- **Segment**: a real stakeholder group (CFO, SRE attendees, free-tier users).
- **Objection**: in their words, including the worst-faith reading.
- **Response**: where and how it is answered (slide 4 adds payback; the post adds a free-tier line).
- **Status**: `answered`, `partially`, or `open`.

## How to fill it in
1. Segment the audience and note each segment's priors.
2. List the top three objections or misreadings per segment.
3. Fix the content to answer them, then record where. Pre-write replies for social.

## On the board
Objections are `question` notes aimed at the content owner. Each is resolved by an `answer` once the deck or copy changes. Escalate harassment to `boundary_keeper`.

## Example

```markdown
<!-- report:objection_map role=community_response_forecaster board=BB-DESIGN-REPLAY -->
| Segment | Priors | Objection | Response | Status |
|---|---|---|---|---|
| Free-tier users | burned by past price hikes | "Is the free tier going away?" | line 2 of the post: "Free tier unchanged" | answered |
| Team admins | worried about seat counts | "Do I pay for viewers?" | FAQ link in the first reply | partially |
<!-- /report:objection_map -->
```

## Quality checks
- [ ] Every top objection has a response
- [ ] No strawman segments
- [ ] The reply bank exists for public posts
