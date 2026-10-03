# Reporting Skills

One skill per **report type** that blackboard roles produce. Each `SKILL.md` is the
single source of truth for its report. The frontmatter says what the report is, who
produces it, its topic tags, and the **output spec** that tools use to validate what an
agent actually returns.

Every role in [`blackboard/`](../blackboard/README.md) declares:

- `blackboard.tags`: what kind of work it does, from [`blackboard/tags.yaml`](../blackboard/tags.yaml)
- `blackboard.reports`: the `report_id`s of the skills here that it hands back

## Skill frontmatter

```yaml
---
name: risk-register                 # skill name (== folder)
description: ...                    # when to use it (what Claude Code reads to trigger the skill)
report_id: risk_register            # id used in role frontmatter and output tags
title: Risk Register
version: 1                          # bump when the output spec changes incompatibly
universal: false                    # true = every role uses it (board_note, dispatch_return)
tags: [risk]                        # topic tags from blackboard/tags.yaml
produced_by: [qa_test_strategist, red_team_skeptic, software_architect]  # must match roles' reports
output:                             # machine-checkable spec for agent output
  tag: report:risk_register         # output tag agents wrap the report in
  format: table                     # table | fields | sections | yaml | gherkin
  columns: [Risk, Likelihood, Impact, Mitigation, Status]  # required table columns (header starts with)
  labels: []                        # required "Label:" lines
  headings: []                      # required markdown headings
  keys: []                          # required YAML keys (format: yaml)
  steps: []                         # required Given/When/Then steps (format: gherkin)
  enums:                            # allowed values, checked wherever the column/label/key appears
    Status: [open, refuted, mitigated, accepted]
  min_rows: 1                       # minimum table rows / YAML items / scenarios
---
```

Only the keys a report needs are present. The **core fields** of a report are the union of
`columns`, `labels`, `headings`, `keys`, and `steps`.

## Output tags

Agents wrap every report they return, wherever it appears in their output (inside a code
fence or not):

```markdown
<!-- report:risk_register role=red_team_skeptic board=BB-DESIGN-REPLAY -->
| # | Risk | Likelihood | Impact | Mitigation | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | If replay calls /api/*, the demo burns tokens | M | H | test asserts 0 fetch calls | qa | mitigated |
<!-- /report:risk_register -->
```

- `report:<report_id>` names the spec to validate against.
- `role=<role id>` is required. It must be a real role, and for non-universal reports it must be in `produced_by`.
- `board=<board id>` is optional, and other `key=value` attributes are kept and passed through.

## Validating agent output

### Per skill (for a skill handler)

Every skill folder ships its own runnable validator, and its frontmatter says how to call it:

```yaml
validation:
  script: scripts/validate.py                    # relative to <dir>
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
  exit_codes: {0: valid, 1: invalid, 2: usage_error}
```

**Handler contract:**
1. Pick `command`, or `command_for_role` when you know the role and board. Use
   `fallback_command` when uv isn't available but PyYAML is.
2. Split the template into argv *first* (shell-style), then replace each `<placeholder>`
   inside each token. Never re-split substituted values, so paths with spaces are safe.
   Every placeholder used is listed under `placeholders`.
3. Run it, then read the exit code and the JSON on stdout:

```json
{"skill": "risk-register", "report_id": "risk_register", "version": 1, "file": "out.md",
 "valid": false, "blocks": [{"line": 3, "role": "red_team_skeptic", "board": "BB-1"}],
 "errors": [{"line": 3, "message": "row 1: Status='kinda' not in ['open', ...]"}]}
```

A usage error (exit 2) prints `{"valid": false, "usage_error": "..."}` instead.

The script checks only blocks tagged with its own `report:<report_id>`, and ignores other
report tags. Extra flags: `--allow-missing` (exit 0 when no block is present),
`--roles-dir <dir>` (also check that role ids exist), and `--skill <dir>` (validate against
another skill's SKILL.md). The reference substitution is `render_command()` in
`scripts/blackboard-index.py`, which CI uses to run every skill's commands from a copied
skill folder whose path contains a space.

**Dependencies (uv):** `scripts/validate.py` carries PEP 723 metadata
(`dependencies = ["pyyaml>=6.0"]`), so `uv run --script` builds an isolated environment
on first use. There's no per-skill `pyproject.toml` to install. The repo's own tooling uses
the root `pyproject.toml` / `uv.lock` (`uv sync`, then `uv run scripts/...`).

All 32 copies are byte-identical to `scripts/skill_validate.py`. Edit that file, then run
`uv run scripts/blackboard-index.py --write`.

### Whole files, every report type

```bash
uv run scripts/validate_report.py output.md                          # check every tagged block
uv run scripts/validate_report.py --role red_team_skeptic output.md  # + require all of the role's reports
uv run scripts/validate_report.py --require test_plan,risk_register output.md
uv run scripts/validate_report.py --json output.md
```

Both validators report the same problems: unknown report types and roles, a role tagging a
report it doesn't produce, missing columns, labels, headings, keys, or steps, values outside
`enums`, too few rows, ragged table rows, and unclosed or mismatched tags.

## How the pieces are kept in sync

`uv run scripts/blackboard-index.py` (run in CI) enforces:

| Rule | Between |
|---|---|
| Role tags and skill tags exist in `tags.yaml`, and every tag is used | roles, skills ↔ vocabulary |
| Every role report is a real `report_id` | roles → skills |
| `produced_by` and the **Produced by** section both equal the roles that list the report | skill ↔ roles |
| `output.tag` is `report:<report_id>`, and folder and name match the id | skill internal |
| The **Template** is wrapped in the output tag and contains every core field | skill ↔ its spec |
| The **Example** is one tagged block that passes `validate_report.py` | skill ↔ its spec |
| `scripts/validate.py` exists, is executable, and is byte-identical to `scripts/skill_validate.py` | skill ↔ canonical script |
| `validation` placeholders are all declared and all used, and every command runs `<dir>/scripts/validate.py` | skill internal |
| Each command, run from a copied skill folder, exits 0 on the Example and 1 on output with no report | skill ↔ runtime |
| Each role's **Deliverable** links its report skills and contains their core fields | role ↔ skills |
| The tables below match the current skills and roles | README ↔ index |

`uv run scripts/test_validate_report.py` tests both validators.

## Using these skills

**Running a board (facilitator):**
1. Seat roles from [`blackboard/panels.yaml`](../blackboard/panels.yaml).
2. Give each role its own body plus the skills for its `reports`, along with the universal
   [`board_note`](board-note/SKILL.md) and [`dispatch_return`](dispatch-return/SKILL.md).
3. Collect the tagged output and validate it. Use each report skill's `validation.command_for_role`
   through your skill handler, or `uv run scripts/validate_report.py --role <id>` for the whole file.
   If it fails, send the errors back to the role.
4. Merge the valid reports into the [decision record](decision-record/SKILL.md).

**Lookup:** `blackboard/index.json` exposes `reports.<id>` (with `output` specs and
`produced_by`) and `tags.<tag>.roles`.

**As Claude Code skills:** copy the folders together so the cross-links still work:

```bash
mkdir -p .claude/skills && cp -r reporting/*/ .claude/skills/   # project
cp -r reporting/*/ ~/.claude/skills/                             # or user-wide
```

The extra frontmatter keys (`report_id`, `output`, and so on) are ignored by Claude Code.
Strict Agent Skills linters that allow only `name`, `description`, `license`,
`allowed-tools`, and `metadata` will flag them.

<!-- BEGIN GENERATED: python3 scripts/blackboard-index.py --write -->
## Report types

| Report | Output tag | Format | Required output | Tags | Produced by |
|---|---|---|---|---|---|
| [Acceptance Cases](acceptance-cases/SKILL.md) | `report:acceptance_cases` | gherkin | steps: Given, When, Then | testing, user-experience, planning | `end_user_advocate`, `product_manager` |
| [Architecture Decision Record](adr/SKILL.md) | `report:adr` | fields | labels: Context, Options, Decision, Consequences<br>enums: Status=proposed/accepted/superseded | architecture | `software_architect` |
| [Asset Manifest](asset-manifest/SKILL.md) | `report:asset_manifest` | table | columns: Asset, Spec, Status<br>enums: Status=planned/thumbnail/rough/final/in-engine/approved | 2d, 3d, animation, audio, vfx | `animator_2d`, `animator_3d`, `game_audio_designer`, `illustrator_2d`, `modeler_3d`, `vfx_artist` |
| [Beat Chart](beat-chart/SKILL.md) | `report:beat_chart` | table | columns: Beat, Purpose, Timing, Intensity<br>enums: Intensity=1/2/3/4/5 | storytelling, level-design, narrative, motion | `level_designer`, `motion_designer`, `narrative_designer`, `presentation_story_architect` |
| [Board Note](board-note/SKILL.md) | `report:board_note` | yaml | keys: kind, body, confidence, refersTo<br>enums: kind=claim/question/answer; confidence=low/medium/high | evidence, synthesis | all roles |
| [Boundary Brief](boundary-brief/SKILL.md) | `report:boundary_brief` | fields | labels: Non-negotiables, Risk, Boundary statements, Escalation<br>enums: Risk=low/medium/high | boundaries, risk | `boundary_keeper` |
| [Budget Sheet](budget-sheet/SKILL.md) | `report:budget_sheet` | table | columns: Budget, Limit, Measured, Target<br>enums: Status=ok/over/not measured | performance-budget | `frontend_engineer`, `gameplay_engineer`, `modeler_3d`, `technical_artist`, `vfx_artist` |
| [Bug Report](bug-report/SKILL.md) | `report:bug_report` | table | columns: Steps, Expected, Actual, Environment, Severity<br>enums: Severity=blocker/major/minor | testing | `exploratory_tester`, `playtest_analyst` |
| [Chart Spec](chart-spec/SKILL.md) | `report:chart_spec` | table | columns: Chart, Question, Takeaway title, Type, Source | data-viz, evidence | `data_storyteller` |
| [Claim Ledger](claim-ledger/SKILL.md) | `report:claim_ledger` | table | columns: Claim, Type, Status, Source, Material<br>labels: Crux<br>enums: Type=fact/value/feeling; Status=verified/false/disputed/unverifiable/n/a; Material=yes/no | fact-checking, evidence | `fact_disentangler` |
| [Conflict Map](conflict-map/SKILL.md) | `report:conflict_map` | table | columns: Party, Interest | de-escalation | `conflict_mediator`, `steelman_interpreter` |
| [Content Brief](content-brief/SKILL.md) | `report:content_brief` | fields | labels: Goal, Audience, Platform, CTA, Metric<br>enums: Goal=awareness/engagement/traffic/conversion/community | social, metrics, audience | `social_strategist` |
| [Data Model](data-model/SKILL.md) | `report:data_model` | table | columns: Entity, Fields, Invariants, Indexes, Retention<br>labels: Migration | data | `data_architect` |
| [Decision Record](decision-record/SKILL.md) | `report:decision_record` | sections | columns: ID, Claim or decision, Evidence, Interpretation / next action<br>headings: Resolved scope, Non-goals, Claims, evidence, and decisions, Blocking questions, completeness pass, Verification evidence | synthesis, planning, evidence | `board_facilitator` |
| [Dispatch Return](dispatch-return/SKILL.md) | `report:dispatch_return` | yaml | keys: status, claims/results, evidence, uncertainty, implication/next action, changed paths<br>enums: status=passed/blocked/needs_decision/no_missing_items | evidence, synthesis | all roles |
| [Draft Variants](draft-variants/SKILL.md) | `report:draft_variants` | table | columns: Variant, Rationale<br>min_rows: 2 | copywriting, persuasion | `diplomatic_wordsmith`, `hook_copywriter`, `platform_native_editor` |
| [Findings Table](findings-table/SKILL.md) | `report:findings_table` | table | columns: Finding, Evidence, Severity, Fix<br>enums: Severity=blocker/major/minor | evidence, risk | `accessibility_inclusion_reviewer`, `art_director`, `brand_voice_guardian`, `developer_experience_advocate`, `end_user_advocate` |
| [Change Impact Map](impact-map/SKILL.md) | `report:impact_map` | table | columns: Path, Change, Risk, Mitigation, Preservation check | integration, risk | `integration_architect` |
| [Interface Contract](interface-contract/SKILL.md) | `report:interface_contract` | table | columns: Interface, Input, Output, Errors | frontend, backend, integration | `backend_engineer`, `frontend_engineer` |
| [Mechanic Sheet](mechanic-sheet/SKILL.md) | `report:mechanic_sheet` | table | columns: Mechanic, Purpose, Player decision, Inputs, Outputs, Edge cases | game-mechanics | `game_systems_designer` |
| [Objection Map](objection-map/SKILL.md) | `report:objection_map` | table | columns: Segment, Objection, Response, Status<br>enums: Status=answered/partially/open | audience, community, risk | `audience_proxy`, `community_response_forecaster` |
| [Ops Plan](ops-plan/SKILL.md) | `report:ops_plan` | fields | labels: Deploy, Rollback, SLOs, Alerts, Runbook | operations | `reliability_engineer` |
| [Product Brief](product-brief/SKILL.md) | `report:product_brief` | fields | labels: Problem, User, Outcome metric, Kill criteria, Non-goals | planning, metrics | `product_manager` |
| [Reference List](reference-list/SKILL.md) | `report:reference_list` | table | columns: Ref, Example, Source, Borrow, Avoid | research, evidence | `prior_art_scout` |
| [Rehearsal Plan](rehearsal-plan/SKILL.md) | `report:rehearsal_plan` | fields | labels: Rehearsals, Timing marks, Demo fallback, Q&A bank | delivery | `delivery_coach` |
| [Research Findings](research-findings/SKILL.md) | `report:research_findings` | table | columns: Question, Method, Sample, Findings, Confidence, Implication<br>enums: Confidence=low/medium/high | research, evidence, user-experience | `playtest_analyst`, `ux_researcher` |
| [Risk Register](risk-register/SKILL.md) | `report:risk_register` | table | columns: Risk, Likelihood, Impact, Mitigation, Status<br>enums: Likelihood=L/M/H/low/medium/high; Impact=L/M/H/low/medium/high; Status=open/refuted/mitigated/accepted | risk | `qa_test_strategist`, `red_team_skeptic`, `software_architect` |
| [Slide Spec](slide-spec/SKILL.md) | `report:slide_spec` | table | columns: Slide, Focal point, Layout, Build steps, Alt text | slides | `slide_designer` |
| [Style Guide](style-guide/SKILL.md) | `report:style_guide` | table | columns: Rule, Do, Don't | art-direction, ui, brand | `art_director`, `brand_voice_guardian`, `ui_visual_designer` |
| [Test Plan](test-plan/SKILL.md) | `report:test_plan` | table | columns: Acceptance criterion, Test, Level, Evidence<br>enums: Level=unit/component/integration/e2e/manual | testing | `qa_test_strategist`, `test_automation_engineer` |
| [Threat Model](threat-model/SKILL.md) | `report:threat_model` | table | columns: Asset, Threat, Likelihood, Impact, Fix, Verify<br>enums: Likelihood=L/M/H/low/medium/high; Impact=L/M/H/low/medium/high | security, risk | `security_reviewer` |
| [Ticket Drafts](ticket-drafts/SKILL.md) | `report:ticket_drafts` | table | columns: Ticket, Acceptance evidence, Depends on, Status<br>enums: Status=draft/ready/in progress/done | planning | `board_facilitator`, `product_manager` |

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

<!-- END GENERATED -->

## Adding a report type

1. Create `reporting/<id-with-dashes>/SKILL.md` with the frontmatter above and these sections:
   When to use, Produced by, Template (wrapped in the output tag), Core fields, How to fill it in,
   On the board, Example (one tagged block that validates), and Quality checks.
2. Add the id to the `blackboard.reports` of each producing role. Link the skill from the role's
   Deliverable section and include the core fields in its template.
3. Copy the `validation:` block from an existing skill. Run `uv run scripts/blackboard-index.py --write`
   to install `scripts/validate.py`, then run `uv run scripts/test_validate_report.py`.
