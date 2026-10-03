---
name: objection-map
description: Audience segments with the objections or misreadings each will have and the response that answers them. Use for pitches, talks, launch posts, and sensitive announcements.
---

# Objection Map

Answers the hard questions in the content, before the audience asks them.

## When to use
For any persuasive talk, pitch, or post, and before anything that could be misread publicly.

## Produced by
- `audience_proxy`: listener segments, priors, objections, and where each is answered in the talk.
- `community_response_forecaster`: likely replies and misreadings, copy fixes, and the reply bank.

## Template
```markdown
| Segment | Priors / likely reaction | Objection | Response | Status |
Reply bank (social): <question → reply> | Rules: reply / ignore / escalate | Monitor: <who, window>
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
| Free-tier users | "simplified pricing" = hike | Is free going away? | add line 2: "Free tier unchanged" | answered |
```

## Quality checks
- [ ] Every top objection has a response
- [ ] No strawman segments
- [ ] The reply bank exists for public posts
