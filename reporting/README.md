# Reporting Skills

One skill per **report type** that blackboard roles produce. Every role in
[`blackboard/`](../blackboard/README.md) declares:

- `blackboard.tags`: what kind of work it does, from [`blackboard/tags.yaml`](../blackboard/tags.yaml)
- `blackboard.reports`: which report types it hands back, as ids from [`reports.yaml`](reports.yaml)

Each report id has a skill here at `reporting/<id with - for _>/SKILL.md`. The skill
says when to use the report, gives its template and required core fields, explains how
to fill it in and how it moves through the board, and ends with an example and quality
checks.

## How the pieces match

The validator (`python3 scripts/blackboard-index.py`) enforces all of these, and CI runs it:

| Rule | Checked against |
|---|---|
| Every role tag exists in `tags.yaml`, and every tag in the vocabulary is used | roles + reports |
| Every role report exists in `reports.yaml` and has a skill folder | roles → registry → `reporting/*/SKILL.md` |
| Each skill's **Produced by** section lists exactly the roles whose `reports` include it | skill ↔ roles |
| Each skill's **Template** contains every `core_fields` entry | skill ↔ registry |
| Each role's **Deliverable** section links its report skills and contains their core fields | role body ↔ registry |
| No skill folder exists without a registry entry | folder ↔ registry |

Roles may **add** columns to a report, such as a criterion column on accessibility
findings, but never drop core fields.

## How to use

**Running a board (facilitator):**
1. Seat roles from [`blackboard/panels.yaml`](../blackboard/panels.yaml).
2. In each dispatch, set `deliverable` to the role's report ids, for example `deliverable: impact_map`.
3. Give each role the skills for its reports along with its own body, plus the universal
   [`board_note`](board-note/SKILL.md) and [`dispatch_return`](dispatch-return/SKILL.md).
4. Roles post [board notes](board-note/SKILL.md) during rounds, and return their reports inside a
   [dispatch return](dispatch-return/SKILL.md) as `claims/results`.
5. Merge the results into the [decision record](decision-record/SKILL.md). Each role's report
   `Quality checks` together with its `done_when` decide `no_missing_items`.

**Looking things up:** `blackboard/index.json` maps `reports.<id>.produced_by` (who writes a
report) and `tags.<tag>.roles` (who does a kind of work), so an orchestrator can pick roles
by report or by tag without parsing markdown.

**As Claude Code skills:** each folder is a standard skill, with a `SKILL.md` that has only
`name` and `description` frontmatter. Copy the whole folder so the cross-links between
skills still work:

```bash
mkdir -p .claude/skills && cp -r reporting/*/ .claude/skills/   # project
cp -r reporting/*/ ~/.claude/skills/                             # or user-wide
```

Report metadata (tags, core fields) lives in `reports.yaml`, not in the skill
frontmatter. That keeps the skills spec-compliant.

## Report types

### Universal (every role)

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Board Note](board-note/SKILL.md) | `board_note` | kind, body, confidence, refersTo | all roles |
| [Dispatch Return](dispatch-return/SKILL.md) | `dispatch_return` | status, claims/results, evidence, uncertainty, implication/next action, changed paths | all roles |

### Board synthesis & planning

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Decision Record](decision-record/SKILL.md) | `decision_record` | Resolved scope, Non-goals, Claims, evidence, and decisions, Blocking questions, completeness pass, Verification evidence | `board_facilitator` |
| [Ticket Drafts](ticket-drafts/SKILL.md) | `ticket_drafts` | Ticket, Acceptance evidence, Depends on, Status | `board_facilitator`, `product_manager` |
| [Product Brief](product-brief/SKILL.md) | `product_brief` | Problem, User, Outcome metric, Kill criteria, Non-goals | `product_manager` |
| [Acceptance Cases](acceptance-cases/SKILL.md) | `acceptance_cases` | Given, When, Then | `end_user_advocate`, `product_manager` |

### Review, risk & evidence

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Findings Table](findings-table/SKILL.md) | `findings_table` | Finding, Evidence, Severity, Fix | `accessibility_inclusion_reviewer`, `art_director`, `brand_voice_guardian`, `developer_experience_advocate`, `end_user_advocate` |
| [Risk Register](risk-register/SKILL.md) | `risk_register` | Risk, Likelihood, Impact, Mitigation, Status | `qa_test_strategist`, `red_team_skeptic`, `software_architect` |
| [Reference List](reference-list/SKILL.md) | `reference_list` | Ref, Example, Source, Borrow, Avoid | `prior_art_scout` |
| [Research Findings](research-findings/SKILL.md) | `research_findings` | Question, Method, Sample, Findings, Confidence, Implication | `playtest_analyst`, `ux_researcher` |
| [Claim Ledger](claim-ledger/SKILL.md) | `claim_ledger` | Claim, Type, Status, Source, Material | `fact_disentangler` |

### Testing / QA

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Test Plan](test-plan/SKILL.md) | `test_plan` | Acceptance criterion, Test, Level, Evidence | `qa_test_strategist`, `test_automation_engineer` |
| [Bug Report](bug-report/SKILL.md) | `bug_report` | Steps, Expected, Actual, Environment, Severity | `exploratory_tester`, `playtest_analyst` |

### Software

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Architecture Decision Record](adr/SKILL.md) | `adr` | Context, Options, Decision, Consequences | `software_architect` |
| [Change Impact Map](impact-map/SKILL.md) | `impact_map` | Path, Change, Risk, Mitigation, Preservation check | `integration_architect` |
| [Interface Contract](interface-contract/SKILL.md) | `interface_contract` | Interface, Input, Output, Errors | `backend_engineer`, `frontend_engineer` |
| [Data Model](data-model/SKILL.md) | `data_model` | Entity, Fields, Invariants, Indexes, Retention, Migration | `data_architect` |
| [Threat Model](threat-model/SKILL.md) | `threat_model` | Asset, Threat, Likelihood, Impact, Fix, Verify | `security_reviewer` |
| [Ops Plan](ops-plan/SKILL.md) | `ops_plan` | Deploy, Rollback, SLOs, Alerts, Runbook | `reliability_engineer` |

### Game design

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Mechanic Sheet](mechanic-sheet/SKILL.md) | `mechanic_sheet` | Mechanic, Purpose, Player decision, Inputs, Outputs, Edge cases | `game_systems_designer` |
| [Beat Chart](beat-chart/SKILL.md) | `beat_chart` | Beat, Purpose, Timing, Intensity | `level_designer`, `motion_designer`, `narrative_designer`, `presentation_story_architect` |

### Graphics & animation (2D / 3D)

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Asset Manifest](asset-manifest/SKILL.md) | `asset_manifest` | Asset, Spec, Status | `animator_2d`, `animator_3d`, `game_audio_designer`, `illustrator_2d`, `modeler_3d`, `vfx_artist` |
| [Budget Sheet](budget-sheet/SKILL.md) | `budget_sheet` | Budget, Limit, Measured, Target | `frontend_engineer`, `gameplay_engineer`, `modeler_3d`, `technical_artist`, `vfx_artist` |
| [Style Guide](style-guide/SKILL.md) | `style_guide` | Rule, Do, Don't | `art_director`, `brand_voice_guardian`, `ui_visual_designer` |

### Presentations

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Slide Spec](slide-spec/SKILL.md) | `slide_spec` | Slide, Focal point, Layout, Build steps, Alt text | `slide_designer` |
| [Chart Spec](chart-spec/SKILL.md) | `chart_spec` | Chart, Question, Takeaway title, Type, Source | `data_storyteller` |
| [Objection Map](objection-map/SKILL.md) | `objection_map` | Segment, Objection, Response, Status | `audience_proxy`, `community_response_forecaster` |
| [Rehearsal Plan](rehearsal-plan/SKILL.md) | `rehearsal_plan` | Rehearsals, Timing marks, Demo fallback, Q&A bank | `delivery_coach` |

### Defusing arguments

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Conflict Map](conflict-map/SKILL.md) | `conflict_map` | Party, Interest | `conflict_mediator`, `steelman_interpreter` |
| [Boundary Brief](boundary-brief/SKILL.md) | `boundary_brief` | Non-negotiables, Risk, Boundary statements, Escalation | `boundary_keeper` |
| [Draft Variants](draft-variants/SKILL.md) | `draft_variants` | Variant, Rationale | `diplomatic_wordsmith`, `hook_copywriter`, `platform_native_editor` |

### Social posts

| Report | id | Core fields | Produced by |
|---|---|---|---|
| [Content Brief](content-brief/SKILL.md) | `content_brief` | Goal, Audience, Platform, CTA, Metric | `social_strategist` |

## Roles → tags and reports

| Role | Tags | Reports |
|---|---|---|
| [Boundary Keeper](../blackboard/conflict/boundary-keeper.md) | boundaries, risk | `boundary_brief` |
| [Conflict Mediator](../blackboard/conflict/conflict-mediator.md) | de-escalation | `conflict_map` |
| [Diplomatic Wordsmith](../blackboard/conflict/diplomatic-wordsmith.md) | persuasion, copywriting, de-escalation | `draft_variants` |
| [Fact Disentangler](../blackboard/conflict/fact-disentangler.md) | fact-checking, evidence | `claim_ledger` |
| [Steelman Interpreter](../blackboard/conflict/steelman-interpreter.md) | de-escalation, audience | `conflict_map` |
| [Accessibility & Inclusion Reviewer](../blackboard/core/accessibility-inclusion-reviewer.md) | accessibility, inclusion | `findings_table` |
| [Board Facilitator](../blackboard/core/board-facilitator.md) | planning, synthesis | `decision_record`, `ticket_drafts` |
| [End User Advocate](../blackboard/core/end-user-advocate.md) | user-experience, accessibility, risk | `findings_table`, `acceptance_cases` |
| [Prior Art Scout](../blackboard/core/prior-art-scout.md) | research, evidence | `reference_list` |
| [Red Team Skeptic](../blackboard/core/red-team-skeptic.md) | risk, evidence | `risk_register` |
| [Game Audio Designer](../blackboard/game/game-audio-designer.md) | audio, game-feel, accessibility | `asset_manifest` |
| [Game Systems Designer](../blackboard/game/game-systems-designer.md) | game-mechanics, metrics | `mechanic_sheet` |
| [Gameplay Engineer](../blackboard/game/gameplay-engineer.md) | game-feel, performance-budget | `budget_sheet` |
| [Level Designer](../blackboard/game/level-designer.md) | level-design, game-mechanics | `beat_chart` |
| [Narrative Designer](../blackboard/game/narrative-designer.md) | narrative, storytelling | `beat_chart` |
| [Playtest Analyst](../blackboard/game/playtest-analyst.md) | research, testing, game-feel | `research_findings`, `bug_report` |
| [Technical Artist](../blackboard/game/technical-artist.md) | performance-budget, art-direction, 2d, 3d | `budget_sheet` |
| [Audience Proxy](../blackboard/presentation/audience-proxy.md) | audience, risk | `objection_map` |
| [Data Storyteller](../blackboard/presentation/data-storyteller.md) | data-viz, evidence | `chart_spec` |
| [Delivery Coach](../blackboard/presentation/delivery-coach.md) | delivery | `rehearsal_plan` |
| [Presentation Story Architect](../blackboard/presentation/presentation-story-architect.md) | storytelling, slides | `beat_chart` |
| [Slide Designer](../blackboard/presentation/slide-designer.md) | slides, art-direction, accessibility | `slide_spec` |
| [Product Manager](../blackboard/product/product-manager.md) | planning, metrics | `product_brief`, `ticket_drafts`, `acceptance_cases` |
| [UX Researcher](../blackboard/product/ux-researcher.md) | research, user-experience, evidence | `research_findings` |
| [Exploratory Tester](../blackboard/quality/exploratory-tester.md) | testing, user-experience | `bug_report` |
| [QA Test Strategist](../blackboard/quality/qa-test-strategist.md) | testing, risk | `test_plan`, `risk_register` |
| [Test Automation Engineer](../blackboard/quality/test-automation-engineer.md) | testing, automation | `test_plan` |
| [Brand Voice Guardian](../blackboard/social/brand-voice-guardian.md) | brand, copywriting | `style_guide`, `findings_table` |
| [Community Response Forecaster](../blackboard/social/community-response-forecaster.md) | community, risk, audience | `objection_map` |
| [Hook Copywriter](../blackboard/social/hook-copywriter.md) | copywriting, social | `draft_variants` |
| [Platform Native Editor](../blackboard/social/platform-native-editor.md) | platform, social, accessibility | `draft_variants` |
| [Social Strategist](../blackboard/social/social-strategist.md) | social, metrics, audience | `content_brief` |
| [Backend Engineer](../blackboard/software/backend-engineer.md) | backend, integration | `interface_contract` |
| [Data Architect](../blackboard/software/data-architect.md) | data, architecture | `data_model` |
| [Developer Experience Advocate](../blackboard/software/developer-experience-advocate.md) | developer-experience | `findings_table` |
| [Frontend Engineer](../blackboard/software/frontend-engineer.md) | frontend, accessibility, performance-budget | `interface_contract`, `budget_sheet` |
| [Integration Architect](../blackboard/software/integration-architect.md) | integration, architecture, risk | `impact_map` |
| [Reliability Engineer](../blackboard/software/reliability-engineer.md) | operations, risk | `ops_plan` |
| [Security Reviewer](../blackboard/software/security-reviewer.md) | security, risk | `threat_model` |
| [Software Architect](../blackboard/software/software-architect.md) | architecture, risk | `adr`, `risk_register` |
| [2D Animator](../blackboard/visual/animator-2d.md) | 2d, animation | `asset_manifest` |
| [3D Animator & Rigger](../blackboard/visual/animator-3d.md) | 3d, animation, rigging | `asset_manifest` |
| [Art Director](../blackboard/visual/art-director.md) | art-direction, 2d, 3d | `style_guide`, `findings_table` |
| [2D Illustrator](../blackboard/visual/illustrator-2d.md) | 2d, art-direction | `asset_manifest` |
| [3D Modeler](../blackboard/visual/modeler-3d.md) | 3d | `asset_manifest`, `budget_sheet` |
| [Motion Designer](../blackboard/visual/motion-designer.md) | motion, animation, social | `beat_chart` |
| [UI Visual Designer](../blackboard/visual/ui-visual-designer.md) | ui, accessibility | `style_guide` |
| [VFX Artist](../blackboard/visual/vfx-artist.md) | vfx, 2d, 3d, game-feel | `asset_manifest`, `budget_sheet` |

## Adding a report type

1. Add an entry to `reports.yaml` with `title`, `tags`, and `core_fields`.
2. Create `reporting/<id-with-dashes>/SKILL.md` with `name` and `description` frontmatter and these
   sections: When to use, Produced by, Template, Core fields, How to fill it in, On the board,
   Example, and Quality checks.
3. Add the id to the `blackboard.reports` of each producing role. Link the skill from the role's
   Deliverable section and include the core fields in its template.
4. Run `python3 scripts/blackboard-index.py --write`.
