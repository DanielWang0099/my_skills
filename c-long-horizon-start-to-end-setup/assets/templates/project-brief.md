# [Project Name] - Project Brief

This file preserves the original request, stable intent, and decision authority. Detailed outcomes and execution planning live in `TASK_MODEL.md`; runtime state lives in `MASTER_PROGRESS.md`.

## Table of Contents

- [Original Request](#original-request)
- [Goal](#goal)
- [Source Inputs](#source-inputs)
- [Scope And Boundaries](#scope-and-boundaries)
- [Decision Authority](#decision-authority)
- [Final Success Standard](#final-success-standard)
- [Final Codex Goal Prompt](#final-codex-goal-prompt)

## Original Request

[Quote or faithfully summarize the request so later work does not depend on conversation memory. Preserve exact wording where it carries an important preference or boundary.]

## Goal

[Describe the real-world result and why it matters when that affects execution.]

## Source Inputs

| Input | Type | Location / URL | Access date, if relevant | Relevance or limits |
| --- | --- | --- | --- | --- |
| [Readable input name] | [File, URL, instruction, or dataset] | [Path or URL] | [Date or N/A] | [What it supplies and any limitation] |

List the project inputs here. Keep sources found during execution with the results they support. Reference inputs by readable names and links.

## Scope And Boundaries

In scope:

- [Included result, population, system, audience, region, or time period]

Out of scope:

- [Excluded nearby work]

Hard boundaries:

- [Task-specific source, budget, deadline, quality, privacy, or action boundary]

## Decision Authority

[Record what Codex may decide or execute independently, including actions already authorized and their limits. Identify decisions reserved for the user or another named authority. Include roles or ownership only when they materially affect execution.]

Apply the authority granted for this project. Record later runtime decisions in `MASTER_PROGRESS.md#gate-decisions`, with the decision's scope and source.

## Final Success Standard

- [Observable final outcome]
- [Critical quality or coverage condition]
- [Required handoff or user-usable state]

Detailed outcomes and deliverables live in `TASK_MODEL.md`; completion evidence lives in the nodes that produce the results.

## Final Codex Goal Prompt

Keep the final prompt under 4000 characters and output it verbatim in the setup response. Run it from the operating-folder root, using relative paths. The execution prompt should follow these files without invoking the setup skill.

```text
From the operating-folder root, open OPERATING_INDEX.md and complete the workflow using its read routes. On a cold start, read PROJECT_BRIEF.md, TASK_MODEL.md, TASK_ARCHITECTURE.md, MASTER_PROGRESS.md, and the current node. When resuming with the project context available, follow the index's resume route. Use MASTER_PROGRESS.md for the execution protocol, current work, runtime decisions, and next action. Follow each node's objective, prerequisites, scope, and completion checks; adapt its approach within the recorded authority. Save local results and evidence in their owning nodes or trackers, keep runtime records current, and preserve enough unfinished-work context to resume. If progress requires missing authority or information, record the blocker and request what is needed while continuing permitted work where possible. Mark the project complete only when the completion rule in MASTER_PROGRESS.md and the final success standard in PROJECT_BRIEF.md are satisfied.
```
