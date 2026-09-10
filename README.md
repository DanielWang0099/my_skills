# Custom Agent Skills

A small simple repo of personal skills. The ratings are absolute, trustworthy
(as the trust-me-bro benchmarks for LLMs), and they are not subjected to any
bias :D

| Status | Skill | Personal rating | Opinion |
| --- | --- | --- | --- |
| <img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use"> | `c-diagnostic-teaching` | <span role="img" title="0 out of 5 stars" aria-label="0 out of 5 stars">✩✩✩✩✩</span> | Not used much; when used, it was not helpful. Needs refinement. |
| <img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use"> | `c-explain-diff-html` | <span title="Not rated yet" aria-label="Not rated yet">N/A</span> | Haven't used it much yet. |
| <img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use"> | `c-long-horizon-start-to-end-setup` | <span role="img" title="4 out of 5 stars" aria-label="4 out of 5 stars">⭐⭐⭐⭐✩</span> | Works really well on Codex for overnight runs; the parallel-agent workflow may need refinement. |
| <img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use"> | `c-academic-research-suite` | <span title="Not rated yet" aria-label="Not rated yet">N/A</span> | Haven't used it much yet. |
| <img src="https://img.shields.io/badge/Setup%20needed-f59e0b?style=for-the-badge" alt="Setup needed"> | `c-manage-calendar-events` | <span role="img" title="3 out of 5 stars" aria-label="3 out of 5 stars">⭐⭐⭐✩✩</span> | Setup is a bit painful. Many native plugins already offer similar fucntionalities so idk why i recreated one. Not bad; still useful. |
| <img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use"> | `c-self-restart` | <span role="img" title="3 out of 5 stars" aria-label="3 out of 5 stars">⭐⭐⭐✩✩</span> | Not bad, but the trigger conditions need refinement. An unsupervised-restart skill should not ask for confirmation before using itself; it still needs more testing as a newer skill. |

Ratings are personal experience, not an objective benchmark. N/A means there
is not enough usage data to rate the skill yet.

## Table of contents

- [c-diagnostic-teaching — Ready to use](#c-diagnostic-teaching)
- [c-explain-diff-html — Ready to use](#c-explain-diff-html)
- [c-long-horizon-start-to-end-setup — Ready to use](#c-long-horizon-start-to-end-setup)
- [c-academic-research-suite — Ready to use](#c-academic-research-suite)
- [c-manage-calendar-events — Setup needed](#c-manage-calendar-events)
- [c-self-restart — Ready to use](#c-self-restart)

## If you love my skills, install all 9

There are six top-level skills in this repository right now. The other three
are too shy. This prompt installs every skill that actually exists:

```text
Please install every top-level skill from
https://github.com/DanielWang0099/my_skills into the agent's supported skills
directory. Clone that repository and discover each of these skill directories:
c-academic-research-suite, c-diagnostic-teaching, c-explain-diff-html,
c-long-horizon-start-to-end-setup, c-manage-calendar-events, and c-self-restart.
Preserve each directory's complete folder structure and supporting files.

Make all six currently available skills discoverable. Do not copy OAuth files,
tokens, API keys, personal preference files, private notes, or machine-specific
paths into the installed skill directories. Keep optional external services,
cross-model APIs, full-runtime adapters, and process-restart behavior disabled
unless the user explicitly asks to configure them. Report which skills are ready
to use and which need setup, including any missing files, dependencies, keys, or
paths.
```

## c-diagnostic-teaching

<p><img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use">&nbsp;&nbsp;<span role="img" title="0 out of 5 stars" aria-label="0 out of 5 stars">✩✩✩✩✩</span></p>

Activates when there is evidence that a technical explanation has not been
understood. It identifies the specific misunderstanding, adapts the
explanation and pacing, and verifies understanding with targeted checks.

**LLM installation prompt**

```text
Install the c-diagnostic-teaching skill from
https://github.com/DanielWang0099/my_skills/tree/main/c-diagnostic-teaching.
Clone or fetch the repository if needed, then copy that complete skill
directory into the agent's supported skills directory, preserve SKILL.md, and
make it available for technical explanations that need diagnosis after a
misunderstanding. No additional configuration is required.
```

## c-explain-diff-html

<p><img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use">&nbsp;&nbsp;<span title="Not rated yet" aria-label="Not rated yet">N/A</span></p>

Produces a self-contained HTML explanation of a code diff with system
background, conceptual intuition, diagrams, a code walkthrough, and a
knowledge check. The generated artifact is intended to be written outside the
repository.

**LLM installation prompt**

```text
Install the c-explain-diff-html skill from
https://github.com/DanielWang0099/my_skills/tree/main/c-explain-diff-html.
Clone or fetch the repository if needed, preserve that complete skill
directory, and make it available for requests to explain a diff, branch,
commit, or pull request as a self-contained HTML teaching artifact. No
additional configuration is required.
```

## c-long-horizon-start-to-end-setup

<p><img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use">&nbsp;&nbsp;<span role="img" title="4 out of 5 stars" aria-label="4 out of 5 stars">⭐⭐⭐⭐✩</span></p>

Creates a durable Markdown planning structure for work that should not depend
on conversation memory alone. It manages project context, recursive task
structure, progress, navigation, approval checkpoints, and completion evidence.
It is suited to long-running and unattended workflows; parallel-agent
orchestration may require further refinement.

**LLM installation prompt**

```text
Install the c-long-horizon-start-to-end-setup skill from
https://github.com/DanielWang0099/my_skills/tree/main/c-long-horizon-start-to-end-setup.
Clone or fetch the repository if needed, then copy that complete skill
directory into the agent's supported skills directory. Preserve its approval
checkpoints, recursive Markdown structure, progress tracking, and completion
evidence. No additional configuration is required.
```

## c-academic-research-suite

<p><img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use">&nbsp;&nbsp;<span title="Not rated yet" aria-label="Not rated yet">N/A</span></p>

A Codex adapter for a research workflow suite covering deep research, literature
reviews, academic writing, peer review, research-to-paper pipelines, experiment
planning, citation checks, and integrity checks. Its core workflows are
prompt-driven and require no additional configuration.

**LLM installation prompt**

```text
Install the complete c-academic-research-suite directory from
https://github.com/DanielWang0099/my_skills/tree/main/c-academic-research-suite,
including SKILL.md, manifest.json, ars/, and codex/. Make the prompt-driven
research, writing, review, and pipeline workflows available. Do not enable
optional external services or the full-runtime adapter during installation.
```

## c-manage-calendar-events

<p><img src="https://img.shields.io/badge/Setup%20needed-f59e0b?style=for-the-badge" alt="Setup needed">&nbsp;&nbsp;<span role="img" title="3 out of 5 stars" aria-label="3 out of 5 stars">⭐⭐⭐✩✩</span></p>

A direct Google Calendar workflow with range-wide conflict checking, duplicate
detection, dry-run validation, all-day event formatting, and write
verification. It requires OAuth configuration because it performs authenticated
calendar reads and writes.

- **Runtime:** Python 3 and internet access.
- **Path to:** private OAuth directory
  `~/.codex/private/google-calendar/` (or
  `CODEX_GOOGLE_CALENDAR_PRIVATE_DIR`).
- **Key:** Google OAuth client credentials in `client.json`; `token.json` is
  generated after authorization.

**LLM installation prompt**

```text
Install the complete c-manage-calendar-events skill directory from
https://github.com/DanielWang0099/my_skills/tree/main/c-manage-calendar-events,
preserving SKILL.md, memory.md, and scripts/calendar_api.py. Configure the
helper to use the private directory ~/.codex/private/google-calendar by
default, or honor CODEX_GOOGLE_CALENDAR_PRIVATE_DIR when set. Keep
client.json, token.json, and personal preference files outside the repository;
never print or commit their contents. Honor
CODEX_CALENDAR_PREFERENCES_FILE when set. Do not perform authorization or a
live calendar write during installation.
```

## c-self-restart

<p><img src="https://img.shields.io/badge/Ready%20to%20use-2ea44f?style=for-the-badge" alt="Ready to use">&nbsp;&nbsp;<span role="img" title="3 out of 5 stars" aria-label="3 out of 5 stars">⭐⭐⭐✩✩</span></p>

A guarded workflow for restarting an agent process and resuming the same
session. It requires a compatible host runtime, a resumable session, and
verified runtime-specific agent-list and resume commands. Its trigger
conditions and confirmation behavior require further testing.

**LLM installation prompt**

```text
Install the c-self-restart skill from
https://github.com/DanielWang0099/my_skills/tree/main/c-self-restart and
preserve its guarded restart-and-resume workflow. Use it only when the user
explicitly requests a restart and continuation. Do not add a redundant
confirmation after that explicit request; instead, verify the current host's
agent-list and resume commands before execution. Detect the active runtime from
the supported session identifiers, use unique temporary paths, and never guess
changed CLI flags.
```

## Credits and licenses

- **Academic Research Suite:** adapted from [Academic Research
  Skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu
  (`Imbad0202`). See the bundled CC BY-NC 4.0 notices in
  `c-academic-research-suite/ars/LICENSE` and
  `c-academic-research-suite/ars/LICENSE.academic-research-skills`.
- **Explain Diff HTML:** adapted from Geoffrey Litt's
  [original gist](https://gist.github.com/geoffreylitt/a29df1b5f9865506e8952488eac3d524).
  Thanks, Geoffrey.
