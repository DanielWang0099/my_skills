# [Project Name] - Operating Index

This is the navigation entrypoint. Follow the read routes below and update information in its owning file. Paths inside the operating folder are relative to its root.

## Start Here

### Cold Start

Use this route whenever the project context is unavailable, including a new session continuing an existing project.

1. Read `PROJECT_BRIEF.md` for the original request, intent, boundaries, and decision authority.
2. Read `TASK_MODEL.md` for outcomes, strategy, constraints, and details that execution must preserve.
3. Read `TASK_ARCHITECTURE.md` for node ownership, relationships, constraints, and any runtime checkpoints.
4. Read `MASTER_PROGRESS.md`, then open the node identified by its execution cursor and the relevant local tracker.

### Resume

1. Read `MASTER_PROGRESS.md` and open the node identified by its execution cursor.
2. Check its saved results, unfinished work, and prerequisites.
3. Follow model, architecture, authority, or parent links when the current decision needs that context.

## Document Map

| File | Canonical responsibility |
| --- | --- |
| `OPERATING_INDEX.md` | Read routes, document map, and update routing |
| `PROJECT_BRIEF.md` | Stable request, intent, inputs, scope, authority, and final success |
| `TASK_MODEL.md` | Outcomes, deliverables, strategy, constraints, decisions, unknowns, and coverage risks |
| `TASK_ARCHITECTURE.md` | Node registry, ownership, relationships, structural authority, constraints, and optional checkpoints |
| `MASTER_PROGRESS.md` | Execution cursor, node states, gate decisions, blockers, and runtime queue |
| `stages/**` | Node context, local approach, item tracking, results, and completion evidence |

Find node files through `TASK_ARCHITECTURE.md#node-registry` and their parent child lists. Adapt the node-directory entry above to the actual folder layout.

## Update Routing

- Original request, intent, inputs, scope, hard boundaries, or authority changed → `PROJECT_BRIEF.md`.
- Outcome, deliverable, strategy, material decision, unknown, or coverage risk changed → `TASK_MODEL.md`.
- Node identity, path, parent, ownership, structural authority, constraint, or checkpoint definition changed → `TASK_ARCHITECTURE.md`.
- Node work state, cursor, gate decision, blocker, or runtime priority changed → `MASTER_PROGRESS.md`.
- Local approach, item state, observation, decision, artifact, or completion evidence changed → owning node or its linked tracker.
- Document locations or read routes changed → this index.

For an authorized Dynamic Discovery change, refresh the affected architecture entries, parent links, state rows, and navigation before the new work starts. Preserve tables of contents when sections are added, renamed, or removed.

Never maintain the same mutable value in two places. Reference its owning record with a link.

## Final Goal Prompt Location

The copy-ready execution prompt is in `PROJECT_BRIEF.md#final-codex-goal-prompt`.
