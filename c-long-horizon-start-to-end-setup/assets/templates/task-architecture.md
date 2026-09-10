# [Project Name] - Task Architecture

This file is the structural setup map for translating the accepted `TASK_MODEL.md` into an adaptive recursive node structure. Use it to decide what stages and nodes are needed, what each node owns, what quality detail must be preserved, and whether any runtime human checkpoints are required. Live execution state belongs in `MASTER_PROGRESS.md`.

## Table of Contents

- [Internal Tracking IDs](#internal-tracking-ids)
- [Stage And Subtask To Node Map](#stage-and-subtask-to-node-map)
- [Node Registry](#node-registry)
- [Architecture-Relevant Constraints And Blockers](#architecture-relevant-constraints-and-blockers)
- [Runtime Human Checkpoints (If Applicable)](#runtime-human-checkpoints-if-applicable)
- [Deferred Or Rejected Nodes](#deferred-or-rejected-nodes)
- [Structural Check](#structural-check)

## Internal Tracking IDs

IDs in nodes are internal tracking labels. They support cross-file recording and step-by-step execution, but should not surface in user-facing explanations or internal model reasoning. Use them only for progress tracking and cursor reliability.

## Stage And Subtask To Node Map

Map the approved setup structure to the files that will own execution. Use paths and names here, not internal IDs.

| Stage | Subtask | Node file | What the node controls | Outcome or quality detail preserved |
| --- | --- | --- | --- | --- |
| [Approved stage] | [Approved subtask] | `[path/to/node.md]` | [Owned scope and boundary] | [Outcome, branch, evidence, or quality need] |

## Node Registry

Use this as the canonical list of node files and internal IDs. Give every node one stable ID, one file, one type, and one parent relationship. Put the node's purpose, owned outcome, quality needs, and any join, reconciliation, or handoff condition in this same table.

| Node ID | Node file | Type | Parent ID | Related node IDs / relationship | Purpose | Outcome / deliverable owned | Quality needs | Join / reconciliation / handoff condition |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N-001 | `[path/to/node.md]` | Stage / Subtask / Dynamic Discovery | ROOT | [IDs and relationship, or none] | [Why this node exists] | [Primary outcome or deliverable] | [Completion quality, coverage, or verification needs] | [Required handoff, join, reconciliation, or None] |

## Architecture-Relevant Constraints And Blockers

Record constraints and known blockers that affect the node structure, scope, sequencing, ownership, or completion conditions. Do not copy live runtime status here; update `MASTER_PROGRESS.md` when a blocker appears or changes during execution. If none are known during setup, write `None planned`.

| Constraint or blocker | Affected stage, subtask, or node file | What it constrains or blocks | Planning response or resolution condition |
| --- | --- | --- | --- |
| [Constraint or known blocker] | [Stage, subtask, or node path] | [Scope, sequence, input, authority, quality, or completion effect] | [Boundary, owner, evidence, or condition needed] |

## Runtime Human Checkpoints (If Applicable)

Most tasks will have no runtime human checkpoint. Leave this table empty or mark it `None planned` when execution should proceed from start to end without a human decision. Add a row only when a human must review or decide before execution continues.

| Stage or node file | Checkpoint objective | Human review or decision | Required input or evidence | Resume condition |
| --- | --- | --- | --- | --- |
| [Stage or node path] | [What the checkpoint protects] | [Decision or review required] | [What must be available] | [What allows execution to continue] |

## Deferred Or Rejected Nodes

Preserve material node proposals that are not created so they are not mistaken for omissions. If there are none, write `None planned`.

| Proposed stage, subtask, or node | Reason deferred or rejected | Revisit condition | Related approved scope, if any |
| --- | --- | --- | --- |
| [Proposed node] | [Why it is not created now] | [Observable condition, or never] | [Owning node or scope note] |

## Structural Check

- [ ] The stage/subtask map covers every approved stage and subtask in `TASK_MODEL.md` and assigns each to an owning node file.
- [ ] Registry paths exactly match the actual node files; every registered node has one row and there are no duplicate IDs or paths.
- [ ] The Node Registry is the only table containing internal node IDs; the other tables use names and paths.
- [ ] Every non-root parent relationship resolves and the recursive graph has no cycle.
- [ ] Every node maps back to accepted work in `TASK_MODEL.md`; no material structure was invented outside the approved model.
- [ ] Architecture-relevant constraints and blockers are mapped to affected stages, subtasks, or node files with a planning response or resolution condition; live runtime status is not duplicated here.
- [ ] Every important outcome and deliverable has one primary owning node, with its quality needs recorded in the registry or node file.
- [ ] Every `Dynamic Discovery` node defines its discovery contract, owning-stage subtree, structural modification authority, and canonical update sequence.
- [ ] Any structure created or revised by a Dynamic Discovery node is represented in the registry, parent child lists, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` before dependent work starts.
- [ ] Every child file names its parent, and every parent file lists its child files and what each child controls.
- [ ] Every node with children has its own parent node file (`STAGE.md` or `SUBTASK.md`) and lists the child subtask files beside it.
- [ ] Every likely lazy point has an owning node with local tracking, a checklist, a bounded inventory, a behavior-branch split, or equivalent evidence.
- [ ] Runtime human checkpoint rows, when present, name the stage or node, objective, required review or decision, input or evidence, and resume condition. Ordinary linear order is not represented as a dependency table.
- [ ] Every runtime human checkpoint, when present, is also represented by a corresponding live decision or approval record in `MASTER_PROGRESS.md`.
- [ ] Deferred or rejected proposals have a reason and revisit condition, or the section is marked `None planned`.
- [ ] Parent closure rules account for every required child reaching `done`, `deferred` with a reason, or explicitly `waived`.
- [ ] Every node has exactly one canonical state row in `MASTER_PROGRESS.md`, and its active cursor points to a listed node.
- [ ] This file does not duplicate live status, runtime approval decisions, evidence narratives, live blocker updates, or next actions.
- [ ] No orphan node files exist outside the registry, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` links.
