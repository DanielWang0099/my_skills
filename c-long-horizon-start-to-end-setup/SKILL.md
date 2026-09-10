---
name: c-long-horizon-start-to-end-setup
description: Create content-first recursive Markdown planning systems with node-local tracking for long-horizon work. Use when the user asks to set up or manage extensive task completion, detailed task models, lean recursive node files, stage/subtask decomposition, long-running research, outreach, business-development, data collection, document-production, implementation, or execution workflows where later work must preserve user intent, recursive granularity, extensive task details, approval guardrails and evidence of completion, and completion rules without relying on conversation memory or a compressed goal prompt.
---

# Content-First Recursive Long-Horizon Task Setup

## Overview

Use this skill to build an operating folder of linked Markdown planning files with node-local tracking for long, detailed work that preserves operational details.

Before creating "execution files"/"operating-folder files" for the operating folder, Codex must complete two short consent checkpoints. The first defines the stage and subtask structure (where recursive subtasks within bigger tasks might exist). After that structure is approved, the second defines the details of the subtasks and "lazy points".

Only after both consent checkpoints have been approved should Codex create the following operating-folder files. Each file has one canonical and exclusive role:
- PROJECT_BRIEF.md — stable project contract for intent, scope, inputs, boundaries, global authority, and final success.
- TASK_MODEL.md — accepted semantic model defining the outcomes, deliverables, strategy, constraints, material decisions, unknowns, and coverage risks.
- TASK_ARCHITECTURE.md — stores the adaptive hierarchy, stage/subtask-to-node map, node registry, parent-child relationships, dynamic-discovery authority, architecture-relevant constraints and blockers, optional runtime human checkpoints, deferred or rejected nodes, and structural checks.
- MASTER_PROGRESS.md — live runtime control plane for work states, dynamic-structure updates, blockers, gate decisions, and the queue. Stores the live cursor, approvals, and completion state.
- OPERATING_INDEX.md — navigation entrypoint for read routes and update routing.
- Owning node files — local execution context, tracking, decisions, results, and completion evidence, and of highest priority, the task deep and rich details. A `Dynamic Discovery` node may update the child structure inside its approved stage scope.

The order of file creation is: PROJECT_BRIEF.md → TASK_MODEL.md → TASK_ARCHITECTURE.md → MASTER_PROGRESS.md → owning node files

Lastly, OPERATING_INDEX.md = navigation layer over all of them

The default final output includes five main root documents, adaptively deep recursive node files, and a short copy-ready Codex `/goals` prompt that points to the architecture entrypoint and active progress cursor. 

The skill allows the user to specify `parallelism` (which can enable parallel workflow). `parallelism` will be "disabled" by default and can be set to "enabled" for parallel execution. Default values will strictly follow the current skill as specified word by word. Non-default values have extensions indicated throughout the skill description; ignore them when not applicable.

## Core Workflow

### 1. Establish the durable folder 

- Prefer `outputs/<project-slug>/` for user-facing deliverables.
- Keep scratch work outside the final output folder unless the user asks otherwise.
- Use stable, lowercase file and folder names when creating recursive node paths.

### 2. Two-step detailed definition of task stages and subtasks before creating execution files.

- Step 1 - Structure: print only `Stages` and `Subtasks`. `Stages` lists the proposed ordered stages. `Subtasks` lists the main child work under each stage. Use names and short overviews; do not expand into detailed definitions or node files yet, instead focus on coverage and completeness of the work breakdown.

During step 1, make sure that the structure adapts to the task's nature. Repeatable inventory work requires reliability of completion. Code implementation requires behavioral, functional, and completeness coverage and quality assurance. Discovery work and research needs broadness and depth. 

Additionally, dynamic work that requires a "discovery stage" where the coverage is unknown (maybe the user asks for `each`, `every`, `per topic`, `per source`, `all pages`, or similar per-item coverage) should represent that work as a discovery subtask in the approved structure and later assign it the node type `Dynamic Discovery`. It defines sources, inclusion rules, exclusion rules, deduplication keys, a stopping rule, and the structural scope it may update. Discover the inventory, then expand the tracker with one row per item before producing per-item outputs. Record the bounded inventory and total count. A Dynamic Discovery node may create, split, or revise child subtask folders and node files inside its owning stage when that change is within its approved discovery scope. It must update `TASK_ARCHITECTURE.md`, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` before dependent production continues; if the semantic scope or authority changes materially, update `TASK_MODEL.md` and obtain any required approval. Do not claim exhaustive completion until the denominator is known, or until the approved discovery rule explains why it cannot be known.

For coding work, `Subtasks` must split to the lowest independently verifiable behavior branch, not to mechanical file edits. Split when one branch could pass while another fails, when fake data or stubs could look complete, or when different callers, states, data shapes, integrations, permissions, or error paths need separate proof. Coding split example: do not leave `implement diarization for audio` as one subtask if the real work includes distinct cases such as `When ASR model timestamps present + offline diarization`, `ASR timestamps missing + offline diarization`, `ASR timestamps missing + streaming diarization`, `diarization unavailable fallback`, and `speaker/time conflict resolution`. 

Most tasks will not need explicit human approval or work-revision checkpoints between runtime stages (runtime checkpoints, not task stage and subtask generation process); assume none unless the user specifically asks for them. If the user requests explicit runtime approval checkpoints between stages, include them in the structure and clearly mark them in the user-required stages.

Ask for explicit approval or changes to the Step 1 structure.

- Step 2 - Details: after Step 1 approval, print `Stages`, `Subtasks` and their details, and `Lazy Points`. Add a concise objective and scope boundary for each stage, define the expected outcome and necessary branches for each subtask, and list the lazy points.

`Lazy Points` lists places where execution could falsely look complete by sampling, bundling, undercounting, skipping sources, using vague done criteria, collapsing per-item work into one broad artifact, implementing only the happy path, using fake data, leaving stubs or hardcoded output, skipping existing callers, ignoring error branches, or leaving behavior branches unproved. Anywhere points that could make incomplete and underquality work look finished.

Each lazy point should name the shortcut and the evidence or count needed to prove it did not happen.

Step 2 must make small refinements that improve clarity and coverage without materially changing the approved structure.

Ask for explicit approval or changes to the Step 2 details. Do not treat silence as approval. Do not create execution files until both steps are explicitly approved.

### 3. Define the task model

- Create `TASK_MODEL.md` from `assets/templates/task-model.md`. Complete every applicable section concisely, defining the goal, success conditions, outcomes, deliverables, stage-level strategy and rationale, constraints, material decisions and unknowns, coverage risks, and details later runs must not lose. Do not build the architecture or recursive nodes until the model is substantive enough for a later run to understand the work without the original conversation.

If the user explicitly activates parameter `parallelism = enabled`, first finish the default linear setup, then read `references/extensions/parallelism.md`. Do not read that extension when the parameter is not explicitly enabled.

### 4. Build the recursive architecture

#### Task architecture setup

- Read `references/recursive-planning-architecture.md`.
- Create `TASK_ARCHITECTURE.md` from its template in `assets/templates/task-architecture.md`.
- Create recursive node files when detail, sequencing, local done checks, approval notes, or handoff rules would otherwise be lost.
- Keep tracking inside the owning node by default.
- Use the node's `## Tracking - Only One Line Active Or Modified` table for item status, output path or blocked/deferred reason, evidence or count, and next action.
- Do not let one broad leaf node own a per-item deliverable unless it has a tracking table or inventory that lists every item, status, output path or reason, and evidence note.
- Create separate tracking documents only when the inventory would make the node unreadable.
- In that case, the node must still show summary counts and link the tracker.
- Use adaptive depth: simple tasks may need only stage nodes; complex tasks should add subtasks and nested subtasks where meaningful detail would otherwise be lost.
- Prefer folders when a node has children, for example `stages/01-discovery/STAGE.md` and `stages/01-discovery/subtasks/source-map.md`.

#### Recursive nodes setup

- Use `assets/templates/recursive-node.md` as a composable template. Every node receives the small core: objective and success, scope, relevant context, decision latitude, working approach, and result/completion. The allowed node types are `Stage`, `Subtask`, and `Dynamic Discovery`.

- Enforce recursive guardrails at every node level.

Every child planning file must name its parent file.
Every child file must carry only the parent context needed to do that local work without rereading the whole tree.
Every node must include scope, a short execution plan, local done checks, guardrails, node-local tracking, child links when needed, and completion/handoff rules.
Every parent file with children must list child files and describe what each child controls.
Do not mark a parent done until required children are `done`, `deferred` with a reason, or explicitly `waived`.
Do not create orphan task files that are absent from `TASK_ARCHITECTURE.md`, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md`.
Use practical granularity.

Dynamic Discovery nodes must state their discovery contract and structural authority. They may create, split, revise, or reorganize child subtask folders and node files inside their owning stage subtree, while preserving node IDs and cross-links where possible. If an existing file node gains children, convert it to its parent folder with `SUBTASK.md` and update all links before production continues. They may not silently change `PROJECT_BRIEF.md`, another stage, the approved authority boundary, or the project's semantic scope. Every structural change must be reflected in the architecture registry, parent child lists, `MASTER_PROGRESS.md`, and `OPERATING_INDEX.md` before the affected production work continues.

Split a node when it contains multiple meaningful work steps, outputs, approval gates, different source sets, or likely partial-completion failure points.
Do not split a node into tiny mechanical steps whose child description would only restate one obvious action.
For coding, the smallest useful unit is the lowest independently verifiable behavior branch, not the smallest file edit, function edit, or command.
Leaf nodes should be meaningful units that can be completed in one focused execution pass with a short evidence note in tracking.

### 5. Initialize runtime state and the goal prompt

- Create `MASTER_PROGRESS.md` as the canonical runtime control plane.
- Work state is `planned`, `ready`, `active`, `blocked`, `done`, `deferred`, or `waived`.
- Gate state is separately `pending`, `approved`, `rejected`, or `waived`.
- `locked` is derived from an explicitly recorded unresolved prerequisite, architecture-relevant constraint or blocker, or pending runtime checkpoint; it is not another stored work state. `approved` is not a node work state.
- By default, exactly one execution node may be Active.
- By default, only one `## Tracking - Only One Line Active Or Modified` row may be active or modified.
- A Dynamic Discovery node may update the active stage structure during execution; after such an update, refresh the canonical architecture, state rows, parent links, and navigation before starting newly created production nodes.
- Locked nodes stay Locked until the recorded prerequisite, constraint, or checkpoint condition is satisfied.
- Runtime priority and state belong in the queue and progress files; `TASK_ARCHITECTURE.md` remains the structural map and does not duplicate them. Authorized Dynamic Discovery updates may revise its stage-local structure, but not its live status history.
- Keep a lightweight task-to-node trace in TASK_ARCHITECTURE.md.
- Do not treat silence as approval.

Create the final prompt in `PROJECT_BRIEF.md`, keep it under 4000 characters, and reference it from `OPERATING_INDEX.md`. It should tell a cold-start run to follow the index and a resuming run to read `MASTER_PROGRESS.md` plus the active node. The node's model and architecture references determine what additional context to load. Point Codex to `OPERATING_INDEX.md` and `MASTER_PROGRESS.md` as the entrypoint and active cursor. Tell Codex to read `PROJECT_BRIEF.md`, `TASK_MODEL.md`, `TASK_ARCHITECTURE.md`, `MASTER_PROGRESS.md`, and the active node before doing execution work.

Do not tell the execution goal to invoke this setup skill. If the user explicitly asks to start a goal, use `create_goal`; otherwise provide the prompt without starting one.

At the end of the setup turn, output the exact copy-ready prompt in the final assistant response under a clear `Final Codex Goal Prompt` heading. Do not only tell the user where the prompt was saved.

### 6. Validate the setup

- Confirm all required files exist.
- Confirm `TASK_MODEL.md` records both approved definition steps: Step 1 with stages and subtasks, and Step 2 with stages, subtasks, and lazy points.
- Confirm `TASK_ARCHITECTURE.md` contains every node file and no orphan nodes exist and is substantive and maps major work to nodes.
- Confirm architecture-relevant constraints and blockers are mapped to affected nodes with a planning response or resolution condition, while live runtime blockers remain in `MASTER_PROGRESS.md`.
- Confirm `MASTER_PROGRESS.md` contains active cursor, approvals, guardrails, short evidence notes, blockers, node statuses, and completion rule.
- Confirm each child file cites its parent and carries enough local parent context.
- Confirm every architecture node has exactly one canonical row in MASTER_PROGRESS.md.
- Confirm every Dynamic Discovery node states its discovery scope, inventory rules, structural modification authority, and required canonical-file update path.
- Confirm no parent is done while a required child is nonterminal.
- Confirm node files include scope, execution, tracking, child links when needed, and completion/handoff rules.
- When a local filesystem folder was created, run `scripts/audit_recursive_setup.py <output-folder>` as a deterministic structural and cross-file audit. The audit derives node paths and relationships from `TASK_ARCHITECTURE.md` and does not assume a fixed child-folder layout.
- Confirm the final prompt is under 4000 characters and points to the recursive entrypoint rather than restating the whole plan.
- Confirm the final assistant response includes the exact final prompt from `PROJECT_BRIEF.md`.

## Required Document Contracts

Each execution file has one canonical responsibility. Link to information owned elsewhere instead of maintaining duplicate editable copies.

- `OPERATING_INDEX.md` must provide the cold-start and resume read routes, document map, update routing, final prompt location, and links to all five root documents. The live execution cursor belongs in `MASTER_PROGRESS.md`; the index should point to it rather than duplicate it.

- `PROJECT_BRIEF.md` must preserve the original request, stable goal, source inputs, scope and boundaries, decision authority, final success standard, and the final copy-ready `/goals` prompt. Include roles or ownership when they materially affect execution.

- `TASK_MODEL.md` must preserve the accepted semantic model and both approved definition steps:
  - Step 1: approved stages and subtasks.
  - Step 2: detailed stages, subtasks, and lazy points.
  
  It must also include the goal and success standard, outcomes, deliverables, execution plan, ordered work model, applicable approvals or consequential actions, details later runs must not lose, decisions and unknowns, constraints, coverage risks, and unresolved items. For dynamic work, record the discovery contract and the approved structural scope of any Dynamic Discovery node. Keep the model readable and do not add internal semantic-ID columns, node paths, or live progress.

- `TASK_ARCHITECTURE.md` must be derived from the accepted `TASK_MODEL.md`, not invent a separate task structure. It must define the adaptive hierarchy, practical granularity rules, node naming and path rules, stage/subtask-to-node mapping, static node registry, allowed node types including `Dynamic Discovery`, parent relationships, node purpose, owned outcomes, quality needs, join, reconciliation, or handoff conditions where needed, dynamic structural authority where applicable, architecture-relevant constraints and blockers, optional runtime human checkpoints, deferred or rejected nodes, parent closure rules, and structural and orphan-node checks. Keep internal node IDs in the node registry; live state belongs in `MASTER_PROGRESS.md`.

- `MASTER_PROGRESS.md` must own the active execution cursor, active node, node work states, approval and gate decisions, blockers, runtime next action, next-node queue, and project completion rule. It may link to node-local guardrails and evidence, but should not duplicate their full narratives or static architecture.

- Recursive node files must use `assets/templates/recursive-node.md` as their composable template. Every node must include its parent file, only the parent context needed locally, owned and excluded scope, a short execution plan, decision latitude, guardrails, local done checks, node-local tracking under `## Tracking - Only One Line Active Or Modified`, child links when needed, a result and evidence note, a completion rule, and a handoff rule. `Dynamic Discovery` nodes must additionally record their discovery contract and bounded authority to modify their owning stage subtree.

- Every parent file with children must list the child files and describe what each child controls. Do not mark a parent done until all required children are `done`, `deferred` with a reason, or explicitly `waived`.

- Do not create orphan node files. Every node must be represented in `TASK_ARCHITECTURE.md`, have a canonical state row in `MASTER_PROGRESS.md`, and be reachable through `OPERATING_INDEX.md`.

- Use practical granularity. Add subtasks or deeper nested-subtask folders only when they preserve distinct ownership, context, dependencies, handoffs, outputs, source sets, approval boundaries, or meaningful execution detail.

## Approval And Compliance Rules

- Do not treat silence as approval.
- Do not proceed into a locked node because the next step seems obvious.
- Do not invent source evidence, contacts, claims, sender details, pricing, availability, or user intent.
- When research depends on current facts, browse or inspect current sources and record URLs plus access dates.
- For outreach/contact hunting tasks, prefer public role contacts and official forms. Do not infer email addresses unless the user explicitly approves that policy.
- For send-assistance tasks, prepare materials for the human owner and track confirmations. Do not send messages directly unless the user explicitly asks and the environment provides an approved sending tool.
- When blocked by missing authority or a material user decision, complete safe preparatory work, record the blocker once, and ask for the decision.

## Common Mistakes And Red Flags

- The same status, approval state, evidence narrative, or next action is editable in two files.
- A parent tracker repeats child status already stored in `MASTER_PROGRESS.md`.
- A setup checkpoint is repeated only to reproduce already approved content.
- Every node looks symmetrical even though some are containers, some execute work, and some discover inventories.
- A dynamic inventory begins production before its sources, inclusion rule, deduplication rule, or denominator are established.
- A Dynamic Discovery node changes a stage or creates a node without updating the architecture registry, canonical state rows, parent links, and navigation.
- A short precise section is padded to satisfy a word count.
- The agent stops for approval on reversible local choices, or proceeds through an actual consequential gate without approval.
- A soft recommended order is treated as a hard dependency.
- A plan is followed after new evidence has made the local method obsolete.

## References And Templates

Read common references only when their phase is reached:

- `references/recursive-planning-architecture.md` before creating architecture and nodes.

Read extension references only when a preceding instruction in this skill directly activates them:

- `references/extensions/parallelism.md` only after `parallelism = enabled` is explicitly activated, the default linear setup is complete, and the task is suitable for parallel work.

Do not read extension references by default or merely because they are present.

Use these assets as guiding starting points, not restrictive schemas. Each task may need its own variations; preserve the canonical document responsibilities and applicable cross-links.

- `assets/templates/operating-index.md`
- `assets/templates/project-brief.md`
- `assets/templates/task-model.md`
- `assets/templates/task-architecture.md`
- `assets/templates/master-progress.md`
- `assets/templates/recursive-node.md`

Replace placeholders, remove inapplicable conditional modules, and keep IDs and links accurate. Do not create extra root documents unless information genuinely cannot live in the five canonical documents or the owning nodes. Do not create separate skills or rely on recursive skill invocation.

## Final Response Contract

When setup is complete, report:

- the output folder;
- a concise description of the created root documents and node depth;
- unresolved decisions, approvals, or blockers;
- `Final Codex Goal Prompt`, containing the exact copy-ready prompt from `PROJECT_BRIEF.md` in a fenced `text` block.

Do not omit the prompt from the final response. The user should be able to start the follow-on Codex goal directly from the final answer without opening the generated files first.
