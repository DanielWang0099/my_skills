---
name: c-self-restart
description: Use when a multi-step workflow you are running cannot continue or be verified until the agent's own host process restarts, and the work should resume afterwards without the user stepping in. Typical triggers - you just created, installed, or edited a skill, MCP server, plugin, hook, config, or env var that only loads at process start and the remaining steps depend on it (e.g. the new skill is missing from your skill list, or a tool returns "not found"); the CLI/app was upgraded mid-workflow; the host process is stuck in a state a fresh start would clear. Also use when the user explicitly asks to restart and continue/resume (restart and continue, reinvoke after exit, resume after restart). Do NOT use for plain close/quit/reboot with no continuation, for changes that are already live, or for restarting services the user built.
---

# Self Restart

## Overview

The agent cannot restart its own process. It writes a one-shot shell script to the OS temp dir that restarts the host, reinvokes the same CLI targeting the same chat session, then deletes itself. The restart log stays, so the user can see what happened and why.

Registry rule: config and skills load once per **host process** start. Reinvoking a session inside the same live process (`run --session` against a running app/server) does NOT pick up new skills - that is a resume, not a restart. A real restart always starts a fresh host process first.

This skill answers two separate questions, in order:

1. **Is a restart needed?** The restart-necessity test (When to Use). Decided by the situation, not by the user's wording.
2. **Am I allowed to do it without asking?** The Auto-Restart Gate. Decided by task length, user presence, other chats, and device vs agent.

Passing the first only makes a restart *eligible*. The second decides whether you may proceed unconfirmed or must ask first.

## When to Use

Trigger on need, not on wording. Consider a restart when all three hold:

1. **It loads only at process start.** Something the remaining work depends on (skill, MCP server, plugin, hook, config, env var, CLI upgrade) is read once per host process, or the host process is in a state a fresh start would clear (stuck state, stale server).
2. **It is not live yet.** You verified it: the skill is missing from your skill list, the tool is absent or returns "not found", the config has no effect. And there is no cheaper fix (see ladder below).
3. **Work remains.** There are further steps that should continue afterwards without the user having to come back and say "continue".

An explicit user request to restart **plus continuation** ("restart and continue", "reboot and pick up where you left off", "reinvoke yourself with ...") also qualifies, even if you would not have noticed the need yourself.

**Plan ahead.** If you can foresee the need while planning (for example "write skill, then use skill"), put the restart into the plan up front and run the gate then, rather than discovering the problem mid-run.

### Cheapest-first ladder

Stop at the first rung that solves it:

1. **Verify it is not already live.** Re-check the skill/tool list. Many changes are picked up without anything else.
2. **Documented reload.** If this runtime has a reload command for the thing that changed, use it. Check `<cli> --help` or the official docs; never guess flags.
3. **Restart the agent process only** (this skill).
4. **Restart the device/OS.** Always needs explicit hard confirmation (gate step 4).

### When NOT to use (do not even load this skill)

- Plain "close codex", "quit", "restart the computer" with **no mention of continuing** and no workflow that needs one - that is a shell/exit action, not this.
- Normal continuation in the same session - just keep working.
- The change is already live (rung 1 of the ladder).
- Restarting a service, server, or app the user built.
- You are inside a resumed run that carries the restart marker (see Loop Guard).

## Auto-Restart Gate (all steps in order)

Unconfirmed agent restart is allowed **only** if every step passes. Otherwise, announce the need and ask first.

1. **Task length.** Very short single-step task -> ask first. Medium/long multi-step workflow -> proceed to step 2.
2. **User presence.** Judge from what you can actually observe, not from guesses:
   - **Eligible (user absent):** the request contained autonomy language ("run this end to end", "I'll be away", "don't wait for me", "fire and forget"), or the user has sent no message for a long stretch while the workflow ran.
   - **Ask first (user present):** the user messaged recently, is mid-conversation, or is sending messages back-to-back.
   - **Unclear -> ask first.**
   - **Standing consent counts as this step passing.** If the user's global/agent instructions explicitly allow self-restart when the restart-necessity test passes, treat presence as already answered. Standing consent never waives steps 3 or 4.
3. **Other chats hard check.** List sessions on this app (`codex agents`, `opencode session list`, `claude agents` / resume picker). If **any** other chat is running or recent -> do NOT restart, report and ask. Only the current session may exist.
4. **Device vs agent.** Restarting the **device/OS** always needs explicit hard confirmation, even if steps 1-3 pass. Restarting only the **agent process** may proceed unconfirmed once steps 1-3 pass.

When asking first, say why a restart is needed, what will resume afterwards, and what the user is being asked to approve. One short message, not a menu.

## Loop Guard

Autonomous triggering needs a hard stop, otherwise a restart that does not fix the problem (wrong host restarted, attached to an old server) will retrigger itself forever.

- At most **one** agent-initiated restart per workflow.
- The resume prompt's first line is the marker: `restarted-by: c-self-restart, count=1`.
- A run that starts with that marker never restarts again on its own. If the thing that required the restart is still not live, it diagnoses, reports, and stops.
- An explicit new request from the user to restart is a fresh decision and is not blocked by the marker.

## Session Targeting

Default to reopening the **current** chat, with a prompt written for the circumstances (marker + goal + cwd + next step, max 20 lines). Offer chat choice only when ambiguous.

| Runtime | Other chats? | Reinvoke same chat |
|---|---|---|
| Codex | `codex agents` | `codex resume <SESSION_ID> "<prompt>"` or `codex queue --thread <ID> --message "<prompt>"` |
| OpenCode | `opencode session list` | `opencode run --session <ID> "<prompt>"` |
| Claude Code | `claude agents` / `claude -r` picker | `claude --resume <ID> "<prompt>"` |

Detect runtime: explicit user choice > env var (`$CODEX_THREAD_ID`, `$OPENCODE_SESSION_ID`, `$CLAUDE_SESSION_ID`) > parent CLI > ask once.

## Implementation

1. Pass the restart-necessity test, the gate, and the loop guard (no marker present). Detect host: desktop-hosted (session lives in the OpenCode/Codex desktop app, e.g. `pgrep -f OpenCode.app` matches) vs pure CLI/TUI.
2. Write the prompt file to a unique temp path (`mktemp`; if the sandbox `mktemp` returns a literal name, append `$$-$RANDOM`). Contents, max 20 lines:
   - Line 1: the marker `restarted-by: c-self-restart, count=1`
   - Why the restart happened (what must be live afterwards)
   - Goal + cwd + the next step to continue with
3. Write the restart script to a unique temp path. Log the reason for the restart as its first line, so a returning user can see why it happened:
   - CLI host: sleep 2 -> pre-flight kill of any stale `<cli> run --session <ID>` processes -> reinvoke line per table with a timeout (10 min; kill and log on expiry) -> self-delete.
   - Desktop host (macOS OpenCode): sleep 2 -> graceful quit `osascript -e 'tell application "OpenCode" to quit'` -> poll up to 30s for the process to exit -> `open -a OpenCode` -> wait ~10s for boot -> pre-flight kill of stale resume runs -> reinvoke line per table with a timeout (10 min; kill and log on expiry) -> self-delete. Never force-kill (`pkill -9`) - it loses session state. Never quit anything except the one host app.
4. `chmod +x`, launch detached (`nohup ... > log 2>&1 &`), state the resume line and the reason in your final message, then exit immediately - continuing would duplicate the resumed session. Do not touch the session in the app until the headless run finishes (check the log), or two executors will share one session and wedge it.
5. The resume prompt must be headless-safe: the detached run cannot answer permission approvals, so it hangs forever on any `ask`. Before restarting, list what the remaining steps will read, write, and run:
   - If everything is covered by existing permissions or can be pre-approved (e.g. `permission.external_directory` allow-rules) before restarting, the resume prompt may carry the full continuation.
   - If some steps would need approvals you cannot pre-grant, the resume prompt covers only read-only verify steps, and the remainder waits for the user in the live session. In that case say so up front in your final message; if that defeats the purpose of the workflow, ask the user before restarting.
6. On resume:
   - **FIRST action:** read the marker, then check the thing that required the restart is actually live (skill in the skill tool list, MCP tool present, config effective). If yes -> proceed with the continuation, including any standing propagate-on-success instruction. If no -> do NOT copy/propagate anything and do NOT restart again (loop guard); diagnose (wrong host restarted? attached to old server?) and report.
   - **LAST action:** append a `DONE` marker line to the restart log so the originator can confirm completion.

## Pairing with other skills

This skill triggers from a situation, and situations are easy to overlook, so add a one-line hook where the situation arises. Examples to paste into the instructions of the workflow concerned:

- In a skill-creation or skill-editing workflow: "If the new or edited skill is needed later in this same run, load c-self-restart after writing it."
- In an MCP/plugin/hook setup workflow: "If remaining steps use the server/plugin/hook you just configured, load c-self-restart to check whether a restart is needed."
- In a CLI upgrade workflow: "After upgrading the host CLI mid-workflow, load c-self-restart before continuing."

## Unknown CLI Commands

If your app's list/resume commands differ from the table (flags change across versions): research first (`<cli> --help`, official docs), verify the command works, then patch this skill's table and sync the fix to the common repo (`~/Documents/skills/`). Never guess flags in the restart script.

## Common Mistakes

- Waiting for the user to ask for a restart when the restart-necessity test already passes -> that is the case this skill exists for. Run the gate instead.
- Restarting because it "might help" without verifying the thing is actually not live -> climb the ladder first.
- Plain close/reboot with no continuation -> don't load this skill.
- User actively chatting, other chats running, or device reboot -> gate steps 2-4 forbid unconfirmed restart.
- Treating standing consent as waiving the other-chats check or the device confirmation -> it only answers user presence.
- No marker in the resume prompt, or ignoring it on resume -> restart loop. One agent-initiated restart per workflow.
- `run --session` against the same live process and calling it a restart -> registry stays stale. Fresh host process first.
- Fresh session instead of same chat -> always resume/target per the table.
- Force-killing the desktop app -> session state loss. Graceful quit only.
- Fixed temp paths -> always unique per session; missing `rm -f "$0"` -> artifact lingers.
- Propagating a skill the resumed self never verified -> always verify first (step 6).
- Resume prompt needing approvals -> headless run hangs on `ask` forever. Pre-approve writes, or limit the prompt to read-only verify (step 5).
- Touching the session in the app while the headless resume runs -> double executor wedges the session. Watch the log, not the chat.
- Restarting silently with no reason in the log or final message -> a returning user cannot tell what happened. Always log and state the reason.
