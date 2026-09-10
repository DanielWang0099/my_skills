# Parallelism Extension

Use this reference only after `parallelism = enabled` and the default linear setup is complete. It prepares the execution files for parallel work selected and managed by the main agent at runtime.

## 1. Prepare The Nodes

Review the current stage plans and make each node's prerequisites explicit: the outputs or conditions within its stage that must be satisfied before its work starts. Preserve its scope, local checks, and completion rules.

Keep the existing hierarchy. The main agent may assign independent nodes or different items within one node to parallel workers. Assignments can span different parents or depths within the current stage; their work must not overlap.

For generated node files, use `## Tracking` and replace the single-active-row instruction with assignment-based tracking: multiple item rows may be active when their assignments are recorded in `MASTER_PROGRESS.md`. Keep one canonical node-state row in the master file and item results in the owning node or its linked tracker.

## 2. Add The Runtime Protocol

Add `## Parallel Execution` to `MASTER_PROGRESS.md` during setup, including the protocol below and an assignment table. Leave the table empty until work is assigned; record any already active work as an assignment owned by the main agent. Preserve the ordinary node states, queue, approvals, and completion rules, and route the execution cursor to the assignment record. Include these instructions in the generated file so later runs can execute without reading this extension.

### Runtime Protocol

1. The main agent selects work within the current stage after checking prerequisites, independence, output ownership, and available tools and worker capacity. Shared read-only inputs are allowed. Run work sequentially when concurrent execution is unavailable or would cause conflicts.
2. Before starting a worker, record its assignment and give it the owning node, exact work or items, permitted outputs, relevant context, and completion checks. Several workers may handle different items in the same node without creating child files.
3. The main agent controls assignments, shared planning files, and shared trackers. Workers write their assigned outputs and report results, evidence, unfinished work, and blockers. The main agent may delegate updates to a separate node file or tracker when it has one writer.
4. Collect and check results, update the assignment and owning node's tracking, and select the next ready work. Adjust worker counts and pending assignments as needed, preserving completed work and preventing duplicate ownership. Before reassigning active work, confirm its previous worker has stopped or released it.
5. Apply the existing completion checks before marking a node done or starting work that needs its output. Finish the current stage and settle its workers before starting the next stage.

### Assignment Record

Record the current stage as `Active stage: [Stage node path]`. Track each assignment with its owning node, exact scope, worker reference when available, state, result/evidence link, and next action or blocker. The main agent may adapt the table to the task while preserving this information.

| Assignment | Node file | Assigned work | Worker | State | Result / evidence | Next action / blocker |
| --- | --- | --- | --- | --- | --- | --- |

Use the existing work states: `planned`, `ready`, `active`, `blocked`, `done`, `deferred`, or `waived`. An unmet prerequisite keeps work planned with the reason recorded. An active assignment keeps its owning node active; completing one assignment does not complete the node's remaining work. Parallel execution permits multiple active nodes and item rows.

### Pause And Resume

Keep assignments current when starting work, receiving results, changing ownership, or pausing. Record partial outputs and the next action so a later run can continue.

On resume, the main agent reads the assignment record and checks worker availability and saved outputs before continuing or replacing unfinished assignments. A saved active state does not establish that a worker is still running. Preserve verified results and resolve uncertain ownership before repeating work.

## 3. Connect Navigation And Discovery

Add a short route in `OPERATING_INDEX.md` directing the main agent to `MASTER_PROGRESS.md#parallel-execution` on start and resume, then to the assigned nodes and trackers.

For Dynamic Discovery nodes, preserve the existing discovery contract and structural authority. Add to their discovery handoff: record newly identified items before the main agent assigns them to workers, and keep active assignments stable while adding further work. If discovery changes node structure, update the architecture, parent links, state rows, and navigation before affected work continues.

## 4. Check The Prepared Setup

Confirm that the runtime protocol and assignment record are present in `MASTER_PROGRESS.md`, the index routes to them, and node prerequisites and tracking support the assignments. Adapt the default one-at-a-time instruction to the parallel runtime protocol, and refresh affected tables of contents and internal links. Check that all concurrent work belongs to the active stage and assigned outputs have clear ownership. Run the setup audit after the transformation.

When `parallelism = disabled`, retain the default linear setup and omit this extension's runtime section and navigation route.
