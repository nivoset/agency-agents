---
name: content-brief
description: Social content brief giving goal, audience, platform and format, CTA, success metric with check-in time, and timing. Use before writing any post, thread, carousel, video, or campaign.
report_id: content_brief
title: Content Brief
version: 1
universal: false
tags: [social, metrics, audience]
produced_by: [social_strategist]
output:
  tag: report:content_brief
  format: fields
  labels: [Goal, Audience, Platform, CTA, Metric]
  enums:
    Goal: [awareness, engagement, traffic, conversion, community]
  min_rows: 1
---

# Content Brief

Every post gets one job, written down before anyone writes the copy.

## When to use
At the start of every social board.

## Produced by
- `social_strategist`: owns it.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:content_brief role=ROLE_ID board=BOARD_ID -->
Goal: awareness | engagement | traffic | conversion | community
Audience: <specific segment>
Platform/format: <platform → native format>
CTA: <one action>
Metric: <number + check at T+48h>
Timing: <date/time + reason>
Pillar: <content pillar>
<!-- /report:content_brief -->
```

## Core fields (required)
- **Goal**: exactly one.
- **Audience**: specific, and present on the chosen platform.
- **Platform**: a native format for each platform.
- **CTA**: exactly one.
- **Metric**: chosen before posting, with a check-in time.

## How to fill it in
1. Choose the goal, then the audience.
2. Choose the platforms where that audience is, and a native format for each.
3. Set the CTA, the metric, and the timing. Check the news cycle for sensitive dates.

## On the board
Post it as round-1 `claim` notes. `hook_copywriter` and `platform_native_editor` write [draft variants](../draft-variants/SKILL.md) against it, and `community_response_forecaster` builds an [objection map](../objection-map/SKILL.md).

## Example

```markdown
<!-- report:content_brief role=social_strategist board=BB-DESIGN-REPLAY -->
Goal: conversion (waitlist signups)
Audience: engineering managers at 20–200 person companies
Platform/format: LinkedIn carousel (8 slides) + X thread (5 posts)
CTA: join the waitlist
Metric: 150 signups, checked at T+48h
Timing: Tuesday 9am PT, outside the conference news cycle
<!-- /report:content_brief -->
```

## Quality checks
- [ ] One goal and one CTA
- [ ] The metric is set before posting
- [ ] A native format for each platform
