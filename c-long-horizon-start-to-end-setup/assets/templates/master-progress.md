# [Project Name] - Master Progress

This file records the execution cursor, node states, runtime decisions, blockers, and next work. Local results and evidence stay in the owning nodes or their linked trackers.

## Table of Contents

- [Current Cursor](#current-cursor)
- [Node State](#node-state)
- [Execution Protocol](#execution-protocol)
- [Gate Decisions](#gate-decisions)
- [Blockers](#blockers)
- [Runtime Queue](#runtime-queue)
- [Pause And Resume](#pause-and-resume)
- [Completion Rule](#completion-rule)

## Current Cursor

Point to the node being executed or resumed. Before execution begins, point to the first ready node. A blocked node may remain here while its blocker is resolved; after project completion, use `None`.

| Node ID | Node file | Next action |
| --- | --- | --- |
| [Registered node ID] | [Node path] | [Concrete next action or blocker reference] |

## Node State

Keep one canonical row for every node in `TASK_ARCHITECTURE.md`. Copy its stable ID from the registry. Record item states in the owning node's tracker.

| Node ID | Work state | Blocker / gate ref | Result link | Updated |
| --- | --- | --- | --- | --- |
| [Registered node ID] | ready | none | [Owning node result or tracker link, or None] | YYYY-MM-DD |

Work states: `planned`, `ready`, `active`, `blocked`, `done`, `deferred`, `waived`.

`ready` means the prerequisites are satisfied; `active` means execution has started. Parent containers can remain planned while their children execute. Use `blocked` for a material obstacle, and record the reason or authority for deferred or waived work in its owning node.

`locked` is derived from an unresolved prerequisite, constraint, or required checkpoint. Approval is recorded separately as a gate decision.

## Execution Protocol

1. Open the current node and check its objective, prerequisites, guardrails, and local tracking. Follow `OPERATING_INDEX.md` when additional project context is needed.
2. By default, execute one node and keep one tracking row active at a time. Adapt the local approach within the approved scope when evidence warrants it.
3. Record results and checks in the owning node or tracker, then update its state and result link here. Use the node's completion checks before marking it `done`.
4. Follow the authority recorded in `PROJECT_BRIEF.md` and applicable gate decisions. Record a blocker once; continue other permitted ready work when possible, updating the cursor and queue. Request only the missing decision, access, or information needed.
5. After an authorized Dynamic Discovery change, update the architecture registry, parent links, node-state rows, and navigation before affected work continues.
6. Advance through the node's handoff and the runtime queue. Check the parent completion rule after its required children finish.

## Gate Decisions

Record actual runtime checkpoints or approval-dependent actions. Link each decision to the affected node and its checkpoint or authority definition. Preserve the decision's author, date, and scope in a short note or durable reference. If none apply, write `None currently` and leave the table empty.

| Gate | Affected node | Checkpoint / authority reference | Gate state | Decision reference | Updated |
| --- | --- | --- | --- | --- | --- |

Gate states: `pending`, `approved`, `rejected`, `waived`. Reference each gate by its distinct descriptive name. Apply existing authorization within its recorded scope; do not infer approval from silence.

## Blockers

Keep each blocker here once, using a distinct descriptive name. Affected node-state rows reference that name. Separate multiple blocker or gate references with semicolons. If none exist, write `None currently` and leave the table empty.

| Blocker | Affects | Description | Needed from / resolution condition | State |
| --- | --- | --- | --- | --- |

Use blocker states `open` or `resolved`.

## Runtime Queue

| Order | Next node ID | Why next | Ready condition |
| --- | --- | --- | --- |
| 1 | [Registered node ID] | [Priority or continuity reason] | [Required output, condition, or gate reference] |

This queue is runtime priority, not another dependency graph. Keep node work states in `Node State`.

## Pause And Resume

Before pausing, save partial results and the unfinished item in the owning node or tracker. Update the cursor, next action, and any blocker here so another run can continue from the saved work.

On resume, follow the index's read route, inspect the saved outputs and tracking, and confirm what remains before repeating an action. Record any correction to the saved state in its canonical location.

## Completion Rule

The project is complete when:

- every required node is `done`, `deferred` with a reason, or explicitly `waived`, and parent completion checks pass;
- every required outcome and deliverable in `TASK_MODEL.md` meets its acceptance conditions or has been explicitly removed from scope by the proper authority;
- result links lead to the owning nodes or trackers, their local checks pass, and the brief's final success standard is met;
- exhaustive work accounts for every item under its discovery contract, with completed items and documented exceptions reconciled against the inventory;
- no unresolved blocker or required approval prevents the remaining obligations from being satisfied.

Deferring work records an exception; it does not satisfy an outstanding required outcome.
