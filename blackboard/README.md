# Blackboard Division

Role agents built for **blackboard sessions**, where a facilitator seats a small panel of
specialists. Each specialist posts `claim` / `question` / `answer` notes to a shared board,
and the facilitator writes one evidence-bound synthesis at the end.

Every file here is a normal Agency agent with the usual frontmatter and body, plus a
`blackboard:` frontmatter block. That block describes how the role behaves on a board:
what it **always pushes for**, what it **pushes back on**, its **blind spots**, whom it
**disagrees with productively**, what counts as **evidence** for it, and when it is
**done**. An orchestrator can choose and brief roles from frontmatter alone.

- Schema: [`SCHEMA.md`](SCHEMA.md)
- Ready-made panels: [`panels.yaml`](panels.yaml)
- Machine-readable index (generated): [`index.json`](index.json)
- Validator: `python3 scripts/blackboard-index.py [--write]`

## Domains covered

| Domain | Panels |
|---|---|
| Software | `feature_design`, `integration_change`, `architecture_review`, `api_and_data`, `release_readiness` |
| Game design | `core_loop`, `level_and_content`, `game_feel`, `game_qa` |
| Graphics & animation (2D + 3D) | `art_2d`, `art_3d`, `brand_graphics`, `motion_piece` |
| Presentations | `talk`, `data_deck`, `pitch`, `live_demo` |
| Defusing arguments | `defuse_reply`, `factual_dispute`, `hard_conversation`, `public_pile_on` |
| Social media posts | `single_post`, `campaign`, `sensitive_announcement`, `talk_to_social` |

## Roster

### Core (cross-domain)
| Role | id | Key push |
|---|---|---|
| 🧑‍🏫 [Board Facilitator](core/board-facilitator.md) | `board_facilitator` | Smallest panel, evidence-bound synthesis, completeness pass |
| 🙋 [End User Advocate](core/end-user-advocate.md) | `end_user_advocate` | Every failure state is recoverable; no fake affordances |
| 🧨 [Red Team Skeptic](core/red-team-skeptic.md) | `red_team_skeptic` | Find the load-bearing assumption and test it |
| ♿ [Accessibility & Inclusion Reviewer](core/accessibility-inclusion-reviewer.md) | `accessibility_inclusion_reviewer` | Keyboard/AT parity, contrast, reduced motion, representation |
| 🔭 [Prior Art Scout](core/prior-art-scout.md) | `prior_art_scout` | Show three real examples before inventing |

### Product
| Role | id | Key push |
|---|---|---|
| 🧭 [Product Manager](product/product-manager.md) | `product_manager` | Problem, outcome metric, smallest slice, non-goals |
| 🔬 [UX Researcher](product/ux-researcher.md) | `ux_researcher` | Observed behavior over opinions |

### Testing / QA
| Role | id | Key push |
|---|---|---|
| 🧪 [QA Test Strategist](quality/qa-test-strategist.md) | `qa_test_strategist` | Every acceptance criterion maps to a passing check |
| 🤖 [Test Automation Engineer](quality/test-automation-engineer.md) | `test_automation_engineer` | Deterministic tests in CI |
| 🐛 [Exploratory Tester](quality/exploratory-tester.md) | `exploratory_tester` | Charters on the riskiest paths, minimal repros |

### Software
| Role | id | Key push |
|---|---|---|
| 🏛️ [Software Architect](software/software-architect.md) | `software_architect` | Care on one-way doors; ADRs |
| 🔌 [Integration Architect](software/integration-architect.md) | `integration_architect` | Preserve existing flows; scope global effects |
| 🖥️ [Frontend Engineer](software/frontend-engineer.md) | `frontend_engineer` | Semantic, fast, keyboard-friendly UI |
| ⚙️ [Backend Engineer](software/backend-engineer.md) | `backend_engineer` | Contracts, idempotency, explicit errors |
| 🗄️ [Data Architect](software/data-architect.md) | `data_architect` | Invariants and reversible migrations |
| 🛡️ [Security Reviewer](software/security-reviewer.md) | `security_reviewer` | Threat model; untrusted input is data |
| 📟 [Reliability Engineer](software/reliability-engineer.md) | `reliability_engineer` | Tested rollback, SLOs, runbooks |
| 📚 [Developer Experience Advocate](software/developer-experience-advocate.md) | `developer_experience_advocate` | Working quickstart, actionable errors |

### Game design
| Role | id | Key push |
|---|---|---|
| 🎮 [Game Systems Designer](game/game-systems-designer.md) | `game_systems_designer` | Meaningful decisions; no magic numbers |
| 🗺️ [Level Designer](game/level-designer.md) | `level_designer` | Teach through space; greybox first |
| 📜 [Narrative Designer](game/narrative-designer.md) | `narrative_designer` | Story the player does |
| 🕹️ [Gameplay Engineer](game/gameplay-engineer.md) | `gameplay_engineer` | Feel and frame budget; data-driven tuning |
| 🎯 [Playtest Analyst](game/playtest-analyst.md) | `playtest_analyst` | Thresholds before tests; triage bug/feel/clarity/balance |
| 🔊 [Game Audio Designer](game/game-audio-designer.md) | `game_audio_designer` | Readable with eyes closed |
| 🛠️ [Technical Artist](game/technical-artist.md) | `technical_artist` | Budgets and automated pipelines |

### Graphics & animation (2D and 3D)
| Role | id | Key push |
|---|---|---|
| 🎨 [Art Director](visual/art-director.md) | `art_director` | One coherent style; readability first |
| 🧩 [UI Visual Designer](visual/ui-visual-designer.md) | `ui_visual_designer` | Tokens and every component state |
| 🖌️ [2D Illustrator](visual/illustrator-2d.md) | `illustrator_2d` | Readable at display size, on-palette |
| 🎞️ [2D Animator](visual/animator-2d.md) | `animator_2d` | Key poses, timing, responsive startup |
| 🧊 [3D Modeler](visual/modeler-3d.md) | `modeler_3d` | Clean topology, LODs, budgets |
| 🦾 [3D Animator & Rigger](visual/animator-3d.md) | `animator_3d` | Clean rigs, defined transitions, no sliding |
| 🌀 [Motion Designer](visual/motion-designer.md) | `motion_designer` | Motion with a job; works muted |
| ✨ [VFX Artist](visual/vfx-artist.md) | `vfx_artist` | Telegraph → impact → aftermath within budget |

### Presentations
| Role | id | Key push |
|---|---|---|
| 🎤 [Presentation Story Architect](presentation/presentation-story-architect.md) | `presentation_story_architect` | One takeaway, a hook, an ask |
| 🖼️ [Slide Designer](presentation/slide-designer.md) | `slide_designer` | Three seconds, back row, one point |
| 🤨 [Audience Proxy](presentation/audience-proxy.md) | `audience_proxy` | Answer the top objections in the talk |
| 🎙️ [Delivery Coach](presentation/delivery-coach.md) | `delivery_coach` | Timed rehearsal and demo fallbacks |
| 📊 [Data Storyteller](presentation/data-storyteller.md) | `data_storyteller` | Takeaway titles, honest axes |

### Defusing arguments
| Role | id | Key push |
|---|---|---|
| 🤝 [Conflict Mediator](conflict/conflict-mediator.md) | `conflict_mediator` | Interests over positions; right channel |
| 🪞 [Steelman Interpreter](conflict/steelman-interpreter.md) | `steelman_interpreter` | Answer their strongest view |
| 🕊️ [Diplomatic Wordsmith](conflict/diplomatic-wordsmith.md) | `diplomatic_wordsmith` | Warm, honest reply in two lengths |
| 🧶 [Fact Disentangler](conflict/fact-disentangler.md) | `fact_disentangler` | Facts vs. values vs. feelings; name the crux |
| 🧱 [Boundary Keeper](conflict/boundary-keeper.md) | `boundary_keeper` | Kind is not compliant; safety first |

### Social media posts
| Role | id | Key push |
|---|---|---|
| 📣 [Social Strategist](social/social-strategist.md) | `social_strategist` | One job per post, measured |
| 🪝 [Hook Copywriter](social/hook-copywriter.md) | `hook_copywriter` | Specific, honest hooks with variants |
| 📱 [Platform Native Editor](social/platform-native-editor.md) | `platform_native_editor` | Native format and norms per platform |
| 🌡️ [Community Response Forecaster](social/community-response-forecaster.md) | `community_response_forecaster` | Fix misreadings before posting |
| 🏷️ [Brand Voice Guardian](social/brand-voice-guardian.md) | `brand_voice_guardian` | Recognizable without the logo |

## Using a role in a blackboard session

1. **Pick a panel.** Match the topic to a panel in `panels.yaml`, then use each role's
   `summon_when` / `skip_when` to swap roles. Stay at 2–5 roles.
2. **Check tensions.** Every role lists `tensions`. If none of the seated roles disagree with
   each other, add the role named in one of their tensions.
3. **Write dispatches from frontmatter.** For example, the `integration_change` panel
   produces:

   ```yaml
   announcement:
     - name: integration_architect            # blackboard.id
       speciality: route, component, style, and dependency integration   # blackboard.speciality
       why: identify framework and existing-workflow conflicts before implementation  # why_template
       deliverable: compatibility evidence, affected paths, risks, and next action    # blackboard.deliverable
   dispatches:
     - name: integration_architect
       question: What are the safest integration points and material compatibility risks?  # panel first_question / signature_questions
       authority: propose-only                  # blackboard.authority
       read_paths: [app/**, components/**, lib/**, package.json]   # default_paths.read
       write_paths: []                          # default_paths.write
       handle: /root/integration_architect
       return_schema: status, claims/results, evidence, uncertainty, implication/next action, changed paths
   ```

4. **Run rounds.** Give each role its body as the system prompt and the board as context.
   Each role posts one note per round, biased toward its `note_bias` kinds.
5. **Completeness pass.** Ask each role whether its `done_when` holds for the final draft.
   Finish when every role returns `no_missing_items`.

## Adding a role

1. Create `blackboard/<division>/<role-id>.md`. The file name in kebab-case must match
   `blackboard.id` in snake_case.
2. Fill every required key in [`SCHEMA.md`](SCHEMA.md). Point `based_on` at the existing
   Agency agents the role draws from.
3. Seat the role in at least one panel (`core` or `optional`).
4. Run `python3 scripts/blackboard-index.py --write` and commit the regenerated `index.json`.
