# [Node Name]

Node ID: N-###
Node type: Stage / Subtask / Dynamic Discovery
Parent file: [Relative parent path, or `TASK_ARCHITECTURE.md` for a root stage]
Parent ID: [ROOT or parent node ID]
Task model basis: `TASK_MODEL.md#[task-trace-or-constraint-anchor]`
Progress cursor: `MASTER_PROGRESS.md`

## Objective And Success

[What this node must accomplish and what observable result makes it successful. State the result this node should optimize for.]

## Scope

### Owns

- [The exact work, items, or deliverable family this node controls]

### Does Not Own

- [Nearby work handled by another node, or "None"]

## Relevant Parent Context

[Only the parent intent, constraint, decision, or handoff context needed to execute this node locally.]

## Decision Latitude

[Choices this node may make independently and decisions that must be escalated.]

## Working Approach

Prerequisites: [Required node outputs or conditions within this stage, or None]

1. [Execution step]
2. [Execution step]

## Child Nodes (If Applicable)

If this node has children, list each child file and what it controls. If it has no children, write `None planned`.

- `[relative/child/path.md]` — [Child ownership and handoff]

## Dynamic Discovery (Only For Dynamic Discovery Nodes)

Discovery sources: [Sources or discovery method]
Inclusion and exclusion rules: [What enters or stays out]
Deduplication key: [Stable identity rule]
Stopping rule and denominator: [When discovery is sufficient and how coverage is counted]
Approved structural scope: [The owning stage subtree this node may modify]

Structural modification authority:

- May create, split, revise, or reorganize child subtask folders and node files inside the approved structural scope.
- Must update the parent node, `TASK_ARCHITECTURE.md`, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` before newly created work starts.
- Must preserve node IDs and links where possible and record deferred or rejected proposals instead of silently deleting them.
- Must escalate changes to project intent, authority, hard scope, another stage, or a material outcome.

Discovery handoff: [Inventory or structural result that production receives]

## Guardrails

- [Source, scope, quality, authority, or side-effect guardrail]

## Local Done Checks

- [Observable check proving this node's owned work is complete]

## Tracking - Only One Line Active Or Modified

| Item | State | Output / Reason | Evidence / Count | Next Action |
| --- | --- | --- | --- | --- |
| [Owned item or child] | Planned / Ready / Active / Blocked / Done / Deferred / Waived | [Output path or blocked/deferred reason] | [Short evidence note or count] | [Next action] |

By default, keep only one row `Active` or `Modified` at a time in this node. Live node state belongs in `MASTER_PROGRESS.md`.

## Result And Completion

Result: [What was produced, decided, or verified.]

Evidence: [Short local evidence note, result link, source, test, count, or reconciliation record.]

## Completion Rule

[Conditions for this node to be complete. If this node has children, state the terminal child states required before closure.]

## Handoff Rule

[What the next node or parent receives and what must be updated before handoff.]
