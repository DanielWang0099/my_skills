# [Project Name] - Task Model

This file is the detailed plan for executing the task approved during the initial stages. It serves as a pillar for the recursive architecture, which should be derived to support complete execution of this plan rather than invented as an empty structure.

## Table of Contents

- [Approved Two-Step Definition](#approved-two-step-definition)
- [Goal](#goal)
- [Outcomes](#outcomes)
- [Deliverables](#deliverables)
- [Work Model](#work-model)
- [Approvals And Human Checkpoints](#approvals-and-human-checkpoints-if-applicable)
- [Details Later Runs Must Not Lose](#details-later-runs-must-not-lose)
- [Decisions And Unknowns](#decisions-and-unknowns)
- [Constraints](#constraints)
- [Coverage Risks](#coverage-risks)
- [Unresolved Items](#unresolved-items)
- [Model Completion Note](#model-completion-note)

## Approved Two-Step Definition

This section records the two approvals completed before creating the operating-folder files. Keep this section focused on stages, subtasks, and lazy points.

### Step 1 - Structure Approval

#### Stages

Approved stage names and short overviews.

- [Approved stage name and short overview]

#### Subtasks

Approved subtasks for each stage.

For repeatable inventory work, enumerate known per-item work or name a `Dynamic Discovery` node that will enumerate it before production. A Dynamic Discovery node may later revise child structure within its approved stage subtree, but its sources, bounds, inclusion/exclusion rules, deduplication key, stopping rule, and structural authority must be defined. For coding work, split by independently verifiable behavior branch, contract, integration path, state, data shape, caller, or error path, not by mechanical file edits.

Subtasks may be recursively divided into nested subtasks when the parent contains multiple meaningful units whose scope, context, handoff, or completion evidence would otherwise be lost.

- [Approved subtask]

### Step 2 - Detail Approval

Small refinements that improve clarity without materially changing the Step 1 structure. Prioritize substantial details, work division, and coverage.

#### Stages with subtasks and rich details

- [Approved stage, subtask, and rich details]

#### Lazy Points (false-completion risks)

Name each shortcut plus the evidence or count needed to prove it did not happen. For coding work, use lazy points to force branch decomposition when fake data, stubs, hardcoded output, happy-path-only code, skipped callers, missing error paths, or unproven behavior branches could make the task look complete.

- [Where execution could falsely look complete by sampling, bundling, undercounting, skipping sources, collapsing per-item work into one broad artifact, using vague done criteria, implementing only the happy path, fake data, stubs, hardcoded output, skipped callers, missing error paths, or unproven branches] -> [Required evidence/count]

## Goal

[Describe the final outcome in plain language. Include why the work matters only when that changes how the task should be executed. Include the most important quality or coverage condition.]

## Outcomes

| Outcome | Required qualities | Consumer (if applicable) | Success condition |
| --- | --- | --- | --- |
| [Observable result] | [Content, usability, format, coverage, or integration qualities] | [Who or what uses it] | [Useful condition, not merely file existence] |

## Deliverables

| Supports outcomes | Deliverable | Required qualities | Success condition |
| --- | --- | --- | --- |
| [Outcome(s) supported] | [Artifact or operational result] | [Content, usability, format, coverage, or integration qualities] | [Observable condition proving it is fit for use] |

## Work Model

[Explain the execution strategy, causal logic, and why recursive structure helps. Treat it as an initial strategy that may adapt inside approved scope.]

| Stage | Purpose | Inputs | Produces | Ordering rationale |
| --- | --- | --- | --- | --- |
| [Stage name] | [Why this stage exists] | [Required inputs] | [Outcomes, deliverables, decisions, or inventory] | [Hard dependency, recommended order, or independent] |

For repeatable work, state whether the inventory is known or dynamic. If dynamic, a Dynamic Discovery node establishes sources, bounds, inclusion/exclusion, deduplication, stopping rule, denominator, and the stage subtree it may revise before per-item production.

For implementation, describe meaningful behavior branches, contracts, integrations, callers, states, data shapes, permissions, fallbacks, and error paths where they affect the plan. Do not decompose into mechanical file edits.

## Approvals And Human Checkpoints (if applicable)

| Action or decision | When it matters | Who decides | Default if unresolved | Where tracked |
| --- | --- | --- | --- | --- |
| [Approval, decision, send, publish, spend, irreversible step, or consequential assumption] | [Stage/node] | [Owner] | [Default or blocked] | `MASTER_PROGRESS.md#gate-decisions` or [node path] |

## Details Later Runs Must Not Lose

- [Specific preference, source interpretation, interface expectation, exception, tradeoff, or caution that changes later decisions]

## Decisions And Unknowns

| Decision or unknown | Why it matters | Resolution method or authority | Affects |
| --- | --- | --- | --- |
| [Material question] | [Consequence] | [Codex decision rule, experiment, or named authority] | [Outcome, deliverable, stage, subtask, or gate] |

Do not list ordinary local implementation choices that Codex can safely resolve from context.

## Constraints

| Constraint | Hard or preference | Applies to |
| --- | --- | --- |
| [Boundary or invariant] | Hard / Preference | [Outcome, deliverable, stage, subtask, or whole project] |

Preferences guide optimization. Hard constraints may not be crossed without the relevant authority.

## Coverage Risks

| How incomplete work could look finished | Why material | Structural response |
| --- | --- | --- |
| [Sampling, bundling, undercounting, skipped source/caller, happy path, fake integration, vague done, or unusable output] | [Consequence] | [Branch, inventory rule, completion signal, experiment, dependency, or gate] |

Each material risk must compile into work design. Do not create a second proof table for it.

## Unresolved Items

- [Unresolved model item and what would resolve it, or “None currently”]

## Model Completion Note

The model is ready for architecture when outcomes, deliverables, strategy, constraints, material decisions, coverage risks, and context-loss details are clear enough to assign coherent nodes without relying on the original conversation.
