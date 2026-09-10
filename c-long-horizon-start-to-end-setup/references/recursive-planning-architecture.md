# Recursive Planning Architecture

Use this reference after `TASK_MODEL.md` is substantive and before creating node files. Architecture maps the semantic work model into a resumable graph without duplicating live state.

## Table of Contents

- [Internal Tracking IDs](#internal-tracking-ids)
- [Document Model](#document-model)
- [Adaptive Hierarchy](#adaptive-hierarchy)
- [Stable Identity And Paths](#stable-identity-and-paths)
- [Recursive Granularity](#recursive-granularity)
- [Dynamic Discovery Nodes](#dynamic-discovery-nodes)
- [Stage And Subtask To Node Map](#stage-and-subtask-to-node-map)
- [Node Registry](#node-registry)
- [Architecture-Relevant Constraints And Blockers](#architecture-relevant-constraints-and-blockers)
- [Runtime Human Checkpoints (If Applicable)](#runtime-human-checkpoints-if-applicable)
- [Deferred Or Rejected Nodes](#deferred-or-rejected-nodes)
- [Parent-Child Context](#parent-child-context)
- [Setup Stages](#setup-stages)
- [Cross-Link Check](#cross-link-check)
- [Setup Completeness](#setup-completeness)

## Internal Tracking IDs

IDs in nodes are internal tracking labels. They support cross-file recording and step-by-step execution, but should not surface in user-facing explanations or internal model reasoning. Use them only for progress tracking and cursor reliability.

## Document Model

| Layer | File | Canonical responsibility |
| --- | --- | --- |
| Navigation | `OPERATING_INDEX.md` | Cold-start and resume routes; document/update map |
| Intent | `PROJECT_BRIEF.md` | Stable purpose, scope, sources, hard boundaries, authority |
| Semantic model | `TASK_MODEL.md` | Outcomes, deliverables, strategy, constraints, decisions, risks |
| Architecture | `TASK_ARCHITECTURE.md` | Stage/subtask map, node registry, ownership, quality needs, dynamic-discovery authority, architecture constraints/blockers, and optional runtime checkpoints |
| Runtime state | `MASTER_PROGRESS.md` | Work state, active work, gate decisions, blockers, queue |
| Local execution | `stages/**` | Node objectives, context, judgment, applicable tracking, results |

The architecture document owns the structural plan, not execution history. It remains static between authorized structural updates. Its Node Registry is the sole editable list of node IDs. Other architecture tables use node paths and names rather than IDs. The registry also records each node's type, parent relationship, purpose, owned outcome, quality needs, and any join, reconciliation, or handoff condition. A Dynamic Discovery node may revise the child structure inside its approved stage subtree during execution, but the resulting structure must be recorded here before dependent production continues.

## Adaptive Hierarchy

Use enough depth to prevent detail loss:

- **Stage:** a major phase, transition, or approval boundary.
- **Subtask:** a coherent executable unit within a stage or another subtask. A nested subtask is used when the parent contains meaningful work that would otherwise be blurred.
- **Dynamic Discovery:** a node that discovers an unknown or changing inventory or work shape and may create, split, revise, or reorganize child subtasks within its owning stage subtree under an explicit structural authority contract.

All stages, subtasks, and Dynamic Discovery nodes in the `TASK_MODEL.md` must be mapped accordingly to their nodes.

Split when a child preserves distinct reasoning, outputs, inputs, sources, decisions, approval boundaries, failure modes, or handoffs. Keep a node intact when a child would only restate an obvious action.

Leaf nodes should be finishable in one focused execution pass, but “focused” does not mean tiny. A behavior spanning several files can be one leaf; a one-file feature with several independently failing behavior paths may require several leaves.

Keep tracking inside the owning node by default. Use separate tracking documents only when a node-local table would be too large; if separated, keep summary counts and tracker links in the node.

For coding work, split by independently verifiable behavior branches rather than by mechanical file edits. Branches may involve contracts, integrations, states, data shapes, callers, permissions, and error paths.

## Stable Identity And Paths

Give each node a stable ID such as `N-001`. Renaming or moving a file does not change its ID.

Stages, subtasks, and Dynamic Discovery nodes at every depth use the same lean node contract: scope, execution, tracking, child links when needed, and completion/handoff. Guardrails do not stop at the stage level.

Default layout and naming example:

Use this as the default layout, not a mandatory structure. Keep the five canonical root documents at the operating-folder root for predictable navigation. Adapt the child folder names and recursion depth to the task's complexity and the existing workspace conventions.

```text
OPERATING_INDEX.md
PROJECT_BRIEF.md
TASK_MODEL.md
TASK_ARCHITECTURE.md
MASTER_PROGRESS.md
stages/
  01-intake-and-source-map/
    STAGE.md
    subtasks/
      01-official-sources.md
      02-stakeholder-map.md
  02-production/
    STAGE.md
    subtasks/
      01-draft-deliverables.md
      02-content-check.md
```

If a subtask has children, make the subtask a folder with its own `SUBTASK.md` node file and place its child subtasks inside that folder:

```text
stages/02-production/
  STAGE.md
  subtasks/
    01-draft-deliverables/
      SUBTASK.md
      01-draft.md
      02-review.md
```

Omit `subtasks/` or deeper folders when they do not preserve distinct ownership, context, dependencies, or handoffs. For smaller tasks, keep fewer child files; for more complex tasks, add recursive levels only where they prevent meaningful detail from being lost. Do not create empty hierarchy levels.

For smaller tasks, keep fewer child files. For complex tasks, add depth before execution begins.


## Recursive Granularity

Split a node when splitting preserves meaningful execution detail:

- Multiple outputs or audiences live inside the parent.
- Different sources, tools, or work modes are needed.
- A child has its own approval, consequential side effect, ambiguity, or failure mode.
- The parent is likely to be partially completed or skimmed if left as one large task.
- Later work needs a clear handoff from one local unit to the next.

Do not split a node when a child would only say "change one line", "do the obvious next step", or repeat the parent. Smallest useful units can still be reasonably large tasks. The point is complete completion, not tiny paperwork.

Each leaf must have:

- A concrete purpose.
- Node-local tracking with one line active or modified at a time by default.
- Local done checks.
- A status update path in `MASTER_PROGRESS.md`.
- A handoff or closure rule.

## Dynamic Discovery Nodes

Use `Dynamic Discovery` when the work cannot name its complete item set or child structure during initial setup. The node must define:

- discovery sources, inclusion and exclusion rules, deduplication key, stopping rule, and expected inventory denominator;
- the owning stage subtree it may modify, including whether it may create or split child subtask folders and node files;
- the handoff from discovery to production, including the inventory or structural result that production receives;
- the canonical update sequence: update the parent node and affected stage files, `TASK_ARCHITECTURE.md`, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` before newly created work starts.

The authority is structural, not semantic. A Dynamic Discovery node may not silently change the project's intent, authority, hard scope boundary, another stage, or a material outcome. If discovery changes those items, update `TASK_MODEL.md` and obtain any required approval before continuing. Preserve node IDs and links when moving or splitting existing work; if a file node gains children, convert it to its parent folder with `SUBTASK.md` and update all links. Record deferred or rejected proposals instead of silently deleting them. If no Dynamic Discovery node is needed, write `None planned`.

## Stage And Subtask To Node Map

Map every approved stage, subtask, and Dynamic Discovery node from `TASK_MODEL.md` to the node file or files that will own it. Use paths and names in this map; internal IDs belong only in the Node Registry.

## Node Registry

Keep one canonical row for each node. The registry is the only architecture table that uses internal IDs. Include the node file, type, parent relationship, related-node relationship, purpose, primary outcome or deliverable, quality needs, and any join, reconciliation, or handoff condition in the same table.

## Architecture-Relevant Constraints And Blockers

Record constraints and known blockers that shape the node structure, scope, sequencing, ownership, or completion conditions. Map each one to the affected stage, subtask, or node file and state the planning response or resolution condition. Keep live runtime blocker status in `MASTER_PROGRESS.md` rather than duplicating it here. If none are known during setup, mark the section `None planned`.

## Runtime Human Checkpoints (If Applicable)

Most tasks are intended to run linearly without runtime human intervention. Do not create a dependency or gate table merely to restate ordinary stage order. Leave the runtime-checkpoint table empty or mark it `None planned` unless a human must review or decide before execution continues. When a checkpoint is needed, record the stage or node path, objective, required review or decision, input or evidence, and resume condition. Live decisions belong in `MASTER_PROGRESS.md`.

## Deferred Or Rejected Nodes

Preserve material node proposals that were deferred or rejected, together with the reason and revisit condition. If there are none, mark the section `None planned`.

## Parent-Child Context

Every child node must include:

- Parent file path.
- Minimal parent context that matters locally.
- The portion of work this child owns and does not own.
- A local tracking table inside `## Tracking - Only One Line Active Or Modified`, or summary counts plus a linked tracker in that section when the inventory is too large.
- Local done rule.
- Handoff target or unlock rule.

Every parent with children must include:

- Child file path.
- Child purpose.
- What detail the child owns.
- A link to the child's state in `MASTER_PROGRESS.md`.
- Join, reconciliation, or handoff condition.

When a subtask gains children, keep the parent subtask as `SUBTASK.md` inside its folder and place the child subtask node files beside it. A subtask without children may remain a single Markdown file under its stage's `subtasks/` folder.

If a child cannot identify what part of the parent it owns or what context matters locally, the parent is underspecified. Fix the parent before continuing.

A parent node cannot close until each required child is `done`, `deferred` with a reason, or explicitly `waived`. Keep the completion rule in the parent node and its live state in `MASTER_PROGRESS.md`.

## Setup Stages

During setup, use these gates internally. Do not generate a permanent setup tracker unless the user explicitly asks for one:

1. Structure consent
   - Before creating execution files, print only `Stages` and `Subtasks` using names and short overviews.
   - Identify the work shape. For repeatable inventory work, if the request implies `each`, `every`, `per topic`, `per source`, `all pages`, or similar coverage, enumerate known items in `Subtasks` or define a `Dynamic Discovery` node before production.
   - For coding work, split to the lowest independently verifiable behavior branch. Do not split into tiny file edits, but do split when fake data, stubs, hardcoded output, happy-path-only code, skipped callers, different data shapes, integrations, permissions, or error branches could make the task falsely look complete.
   - Coding split example: `implement diarization for audio` should split when needed into `ASR timestamps present + offline diarization`, `ASR timestamps missing + offline diarization`, `ASR timestamps missing + streaming diarization`, `diarization unavailable fallback`, and `speaker/time conflict resolution`.
   - Wait for explicit user approval or requested changes.
   - Do not treat silence as approval.

2. Detail consent
   - After structure approval, print `Stages`, `Subtasks`, and `Lazy Points`.
   - Add a concise objective and scope boundary for each stage. Define the expected outcome and necessary branches for each subtask.
   - In `Lazy Points`, name the shortcut and the evidence or count that will prove it did not happen.
   - Small refinements are allowed when they improve clarity without materially changing the approved structure. Substantial additions, removals, or reorganizations return to structure consent.
   - Wait for explicit user approval or requested changes.
   - Do not treat silence as approval.

3. Detailed execution planning
   - Create `TASK_MODEL.md` before recursive architecture.
   - Record both approved definition steps using stages, subtasks, and lazy points.
   - Write the task plan: goal, expected outputs, ordered work plan, approvals or consequential actions, and details later runs must not lose.
   - Build the lightweight task-to-node trace that maps important work to node files.

4. Intake capture
   - Record the user request, source inputs, assumptions, unknowns, boundaries, and non-goals.
   - Capture exact facts that must not be lost later.

5. Recursive decomposition
   - Identify stages, subtasks, Dynamic Discovery nodes, nested subtasks when needed, and optional runtime human checkpoints.
   - Decide adaptive depth based on complexity and chance of detail loss.
   - Derive the node list from `TASK_MODEL.md`, not only from intuitive phase names.
   - Treat ordinary stage order as the task's linear execution plan; record a runtime checkpoint only when a human review or decision is actually required.

6. Document architecture
   - Create the operating index, brief, task model, architecture map, progress cursor, and planned node paths. Do not add parallelism sections unless the parallelism extension is active.
   - Assign each kind of information to exactly one primary home.

7. Node and tracker creation
   - Create all required root files and initial node files.
   - Add concise scope, execution steps, done checks, guardrails, integrated tracking, completion rules, and update protocol. Dynamic Discovery nodes also receive their discovery and structural-authority module.
   - Separate tracking documents are an exception for very large inventories; the owning node still keeps summary counts and a link.

8. Cross-link check
   - Confirm every child is listed by its parent.
   - Confirm every child names its parent.
   - Confirm all planned nodes appear in `TASK_ARCHITECTURE.md` and `OPERATING_INDEX.md`.
   - Confirm root documents point to each other consistently.

9. Final goal prompt
   - Write a prompt under 4000 characters.
   - Point to `OPERATING_INDEX.md` and `MASTER_PROGRESS.md`.
   - Tell Codex to start from the active cursor, read linked files, update node-local tracking, obey explicit runtime checkpoints, and request approval before side effects.

## Cross-Link Check

Before setup is complete, check:

- `OPERATING_INDEX.md` lists all root documents and points to the execution cursor in `MASTER_PROGRESS.md`.
- `TASK_MODEL.md` includes the task-to-node trace and context-loss details.
- `TASK_ARCHITECTURE.md` maps approved stages, subtasks, and Dynamic Discovery nodes, lists every node file, and records architecture-relevant constraints or blockers.
- Every Dynamic Discovery node names its owning stage subtree, discovery contract, structural authority, and canonical-file update sequence.
- When `parallelism = enabled`, follow the extension's setup checks after the linear setup is complete. Otherwise, omit parallelism sections and routes.
- Every node file has a parent path except the project root entrypoint.
- Every node file has `## Tracking - Only One Line Active Or Modified`. If a large external tracker is necessary, summary counts and the tracker link stay inside that section.
- Every parent lists its child files.
- `MASTER_PROGRESS.md` active cursor points to an existing node.
- `MASTER_PROGRESS.md` contains approval gates, guardrails, short evidence notes, and next-node queue.
- `PROJECT_BRIEF.md` and `TASK_MODEL.md` do not duplicate live progress fields.
- The final goal prompt references file paths instead of restating the full plan.

## Setup Completeness

Prefer more detail in generated project files when detail loss would make later execution weaker. The setup is acceptable only when another Codex run can open `OPERATING_INDEX.md`, follow the read order, find the active cursor, and execute the next step without relying on earlier conversation memory.
