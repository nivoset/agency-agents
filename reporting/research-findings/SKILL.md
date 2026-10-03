---
name: research-findings
description: Research plan or results, giving the question, method, sample, findings, confidence, and design implication. Use for usability studies, interviews, analytics reads, surveys, and game playtests.
report_id: research_findings
title: Research Findings
version: 1
universal: false
tags: [research, evidence, user-experience]
produced_by: [playtest_analyst, ux_researcher]
output:
  tag: report:research_findings
  format: table
  columns: [Question, Method, Sample, Findings, Confidence, Implication]
  enums:
    Confidence: [low, medium, high]
  min_rows: 1
---

# Research Findings

Puts observed behavior on the board in place of opinion.

## When to use
When the board debates what users or players want, or a critical assumption needs checking. Also use it to plan a study before it runs.

## Produced by
- `ux_researcher`: usability, interview, and analytics findings.
- `playtest_analyst`: playtest results, each against its pre-set threshold.

## Template
Wrap the report in its output tag so tools can find and check it (`scripts/validate_report.py`). Put your own role id in `role=` and the board id in `board=`.
```markdown
<!-- report:research_findings role=ROLE_ID board=BOARD_ID -->
| Question | Method | Sample | Threshold (optional) | Findings | Confidence | Implication |
<!-- /report:research_findings -->
```

## Core fields (required)
- **Question**: the decision-relevant question.
- **Method**: moderated test, survey, telemetry, interview, and so on.
- **Sample**: n and profile. Never omit it.
- **Findings**: what was observed, with counts ("4 of 5").
- **Confidence**: low, medium, or high, matched to the method and n.
- **Implication**: what the board should change or decide.

## How to fill it in
1. Write the question and the success threshold before the study.
2. Run the study, or extract findings from existing data.
3. Report counts, not adjectives. Separate what users said from what they did.

## On the board
A study plan goes in as a `question` note. Results go in as `answer` notes that refer back to the claim they test. Tag assumptions on the board as evidence-backed or assumption.

## Example

```markdown
<!-- report:research_findings role=ux_researcher board=BB-DESIGN-REPLAY -->
| Question | Method | Sample | Threshold | Findings | Confidence | Implication |
|---|---|---|---|---|---|---|
| Do reviewers find the workspace switcher? | moderated task | 5 internal reviewers | 4 of 5 | 1 of 5 found it unaided | medium | move the switcher into the header |
<!-- /report:research_findings -->
```

## Quality checks
- [ ] Sample stated
- [ ] Threshold set before results (playtests)
- [ ] Implications are actionable
