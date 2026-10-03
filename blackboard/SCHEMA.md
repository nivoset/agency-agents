# Blackboard Role Frontmatter Schema

Every role file in `blackboard/<division>/<role-id>.md` carries the standard Agency
frontmatter (`name`, `description`, `color`, `emoji`, `vibe`) **plus** a `blackboard:`
block. The extra block lets a blackboard orchestrator pick roles, write dispatches,
predict disagreements, and know when a role is finished, all without reading the body.

The block maps directly onto the blackboard skill's structures:

| Frontmatter key | Blackboard structure it feeds |
|---|---|
| `id` | `Role.id` / dispatch `name` / `handle` (`/root/<id>`) |
| `speciality` | `Role.speciality` / dispatch `speciality` |
| `why_template` | `Role.rationale` / announcement `why` (fill in `{topic}`) |
| `deliverable` | announcement `deliverable` |
| `signature_questions` | seed for the dispatch `question` |
| `authority` | dispatch `authority` |
| `default_paths.read` / `default_paths.write` | dispatch `read_paths` / `write_paths` |
| `note_bias` | which `Note.kind` (`claim`, `question`, `answer`) the role mostly posts |
| `done_when` | the role's `no_missing_items` condition in the completeness pass |
| `return_schema` | dispatch `return_schema` (defaults to the shared schema below) |

## Keys

```yaml
blackboard:
  id: end_user_advocate            # REQUIRED snake_case, unique, == file name with - → _
  division: core                   # REQUIRED one of the division folders
  domains: [software, game]        # REQUIRED subset of: software, game, presentation, conflict, social, visual
  speciality: "..."                # REQUIRED one line, what this role reviews/proposes
  why_template: "..."              # REQUIRED one line, why this role is on the board for {topic}
  summon_when: [...]               # REQUIRED signals that this role should be dispatched
  skip_when: [...]                 # REQUIRED signals that this role adds noise, not signal
  key_pushes: [...]                # REQUIRED 3–5 things this role ALWAYS pushes the board toward
  pushes_back_on: [...]            # REQUIRED proposals this role predictably challenges
  blind_spots: [...]               # REQUIRED what this role under-weights (pair to cover it)
  signature_questions: [...]       # REQUIRED questions the role reliably brings to a board
  evidence: [...]                  # REQUIRED what this role accepts as evidence
  deliverable: "..."               # REQUIRED what the role returns
  note_bias: [question, claim]     # REQUIRED Note kinds in priority order
  tensions:                        # REQUIRED productive disagreements with other roles
    - with: product_manager
      over: "..."
  pairs_with: [...]                # REQUIRED roles that complete this role's blind spots
  authority: propose-only          # REQUIRED propose-only | review-only | implement
  done_when: "..."                 # REQUIRED condition for returning `no_missing_items`
  based_on: [path/to/agent.md]     # REQUIRED existing Agency agents this role draws from
  default_paths:                   # OPTIONAL, for repo-backed boards
    read: ["app/**"]
    write: []
  return_schema: [...]             # OPTIONAL, overrides the shared return schema
```

### Shared return schema

Unless a role overrides it, every dispatch returns:

```
status, claims/results, evidence, uncertainty, implication/next action, changed paths
```

`status` is one of `passed`, `blocked`, `needs_decision`, or `no_missing_items`.

### Note discipline (all roles)

- Post **one** note per round: `claim`, `question`, or `answer`.
- Give `confidence` as `low` / `medium` / `high`. Use `high` only when you can cite evidence.
- Use `refersTo` when you build on or challenge another note. Never repeat a point already on the board.
- A `question` must be answerable. Name who should answer it, or say what evidence would settle it.

## Panels

`blackboard/panels.yaml` lists ready-made boards for each domain. Each has 2–5 `core`
roles (the `RolesProposalSchema` limit) and an `optional` bench. The orchestrator
starts from a panel, swaps roles using `summon_when` / `skip_when`, and keeps the
board at five roles or fewer.

## Validation

```bash
python3 scripts/blackboard-index.py          # validate only
python3 scripts/blackboard-index.py --write  # validate + regenerate blackboard/index.json
```

The validator checks that required keys are present, that ids are unique and match
their file names, and that cross-references resolve: `tensions.with`, `pairs_with`,
panel roles, and `based_on` paths must all point to something that exists.
