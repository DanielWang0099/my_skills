---
name: c-self-restart
description: Use when a multi-step workflow you are running cannot continue or be verified until the agent's own host process restarts, and the work should resume afterwards without the user stepping in. This is an autonomy skill - restart and resume on your own instead of asking permission. Typical triggers - you just created, installed, or edited a skill, MCP server, plugin, hook, config, or env var that only loads at process start and the remaining steps depend on it (e.g. the new skill is missing from your skill list, or a tool returns "not found"); the CLI/app was upgraded mid-workflow; the host process is stuck in a state a fresh start would clear. Also use when the user explicitly asks to restart and continue/resume (restart and continue, reinvoke after exit, resume after restart). Do NOT use for plain close/quit/reboot with no continuation, for changes that are already live, or for restarting services the user built.
---

# Self Restart

## Overview

The agent cannot restart its own process. It writes a one-shot shell script to the OS temp dir that restarts the host, reinvokes the same CLI targeting the same chat session, then deletes itself. The restart log stays, so the user can see what happened and why.

Registry rule: config and skills load once per **host process** start. Reinvoking a session inside the same live process (`run --session` against a running app/server) does NOT pick up new skills - that is a resume, not a restart. A real restart always starts a fresh host process first.

**This is an autonomy skill.** Its whole purpose is that the work keeps going without the user. When the restart-necessity test passes, the default is to restart and resume on your own: don't ask permission, don't wait for confirmation, and don't hand the task back. Uncertainty about the user's presence, the task's length, or anything else that is not a hard stop resolves toward restarting. (Uncertainty about whether a restart is *needed* is different: verify first, the ladder below is cheap.) You stop and ask only at a hard stop (see the Restart Gate), and you always leave a trace: the reason is logged and stated in your final message.

Two facts shape everything below:

- **The detached script is on its own.** It inherits none of your live session's environment (PATH, env vars, working directory assumptions), and there is no chat to correct it if a step fails. So everything it needs must be resolved to absolute values and proven to work *before* the host is closed.
- **Your memory of a restart does not survive the restart.** A re-opened session cannot remember "I already tried this" unless that fact is recorded somewhere outside the chat that does not depend on the attempt succeeding.

This skill answers three questions, in order:

1. **Is a restart needed?** The restart-necessity test (When to Use). Decided by the situation, not by the user's wording.
2. **Is anything stopping me?** The Restart Gate: a short list of hard stops. If none applies, restart without asking.
3. **Can it actually complete?** The Preflight (Implementation), which runs before the point of no return.

Passing the first makes restarting the default. The second is the only place you may stop and ask. The third decides whether it is safe to launch at all.

## When to Use

**Check the restart record first** (see Loop Guard). If one exists for this session and is not `done`, you are re-entering an earlier attempt, not facing a fresh decision. Do not restart; go to Loop Guard.

Otherwise, trigger on need, not on wording. Consider a restart when all three hold:

1. **It loads only at process start.** Something the remaining work depends on (skill, MCP server, plugin, hook, config, env var, CLI upgrade) is read once per host process, or the host process is in a state a fresh start would clear (stuck state, stale server).
2. **It is not live yet.** You verified it: the skill is missing from your skill list, the tool is absent or returns "not found", the config has no effect. And there is no cheaper fix (see ladder below).
3. **Work remains.** There are further steps that should continue afterwards without the user having to come back and say "continue".

An explicit user request to restart **plus continuation** ("restart and continue", "reboot and pick up where you left off", "reinvoke yourself with ...") also qualifies, even if you would not have noticed the need yourself.

**Plan ahead.** If you can foresee the need while planning (for example "write skill, then use skill"), put the restart into the plan up front and run the gate then, rather than discovering the problem mid-run.

### Cheapest-first ladder

Stop at the first rung that solves it:

1. **Verify it is not already live.** Re-check the skill/tool list. Many changes are picked up without anything else.
2. **Documented reload.** If this runtime has a reload command for the thing that changed, use it. Check `<cli> --help` or the official docs; never guess flags.
   - If local browser use suddenly reports disabled despite being enabled in settings, verify the setting and try cheaper fixes first; a host restart may restore access. Recheck after restarting; do not bypass access restrictions or restart again automatically if it still fails.
3. **Restart the agent process only** (this skill).
4. **Restart the device/OS.** Always needs explicit hard confirmation (hard stop 2 in the Restart Gate).

### When NOT to use (do not even load this skill)

- Plain "close codex", "quit", "restart the computer" with **no mention of continuing** and no workflow that needs one - that is a shell/exit action, not this.
- Normal continuation in the same session - just keep working.
- The change is already live (rung 1 of the ladder).
- Restarting a service, server, or app the user built.
- A restart record for this session exists and is not `done` (see Loop Guard).

## Restart Gate (autonomy by default)

The default is to restart without asking. Only the two hard stops below pause you; nothing else does. Task length, user presence, and unclear presence are not reasons to ask.

**Hard stops** - stop, report why, and ask:

1. **Another chat is running.** List sessions on this app (`codex agents`, `opencode session list`, `claude agents` / resume picker). If **any other chat is running** (actively executing a turn or holding a live process) -> do NOT restart, report and ask. Chats that are merely recent but idle do not block. If the listing does not show run state, check whether the session has a live process; if you find none, treat it as idle and proceed.
2. **Device/OS restart.** Restarting the **device/OS** always needs explicit hard confirmation. Restarting only the **agent process** never does.

The Loop Guard and the Preflight can also stop a restart, but those are safety checks you act on yourself, not questions for the user.

**Not stops - restart anyway:**

- **Short tasks.** The necessity test already requires remaining work that depends on the restart. That is enough.
- **User presence.** Absent or unclear: restart. Present: say in one line what is happening and that the work will resume on its own ("Restarting to load the new skill; I'll pick up from here automatically"), then restart without waiting for a reply. The only exceptions are an explicit instruction from the user not to restart, and the hard stops above.
- **Anything else unclear** that is not a hard stop: restart.

When a hard stop applies, tell the user in one short message why a restart is needed, what is blocking it, and what will resume afterwards. One message, not a menu.

## Loop Guard

A restart that does not fix the problem, or that fails halfway, must never retrigger itself. The guard therefore has to live outside the chat and must not depend on the resume prompt having been delivered, because a failed restart is exactly the case where it was not.

**Restart record.** A small state file in a stable per-user location (not the per-run temp dir), keyed by session ID, for example `<state dir>/c-self-restart/<SESSION_ID>.state`. It holds `status`, `attempts`, `reason`, `started`, and the path of the log. Statuses:

`launching` -> `resumed` -> `done`, or `failed` at any point.

**Rules**

- Write `status=launching, attempts=1` **before** launching anything.
- Read the record at the start of any turn that might restart (before the necessity test). If it exists and is not `done`, this is a re-entry: do not restart. Read the log, diagnose what went wrong, report it, and stop. This holds even when the session was reopened mid-turn and nothing in the chat mentions a restart.
- If the record is `done`, the earlier workflow finished; a later workflow may restart once more.
- At most **one** agent-initiated restart per workflow. Never auto-retry a failed attempt: the environment was wrong, and the same attempt will fail the same way.
- The resume prompt's first line is still the marker `restarted-by: c-self-restart, count=1`. It is a visible, secondary signal for humans and for the resumed run. It is not the guard.
- The user can clear the record (delete the file) or explicitly ask to try again. An explicit new user request is a fresh decision and is not blocked by it.

## Session Targeting

Default to reopening the **current** chat, with a prompt written for the circumstances (marker + goal + cwd + next step, max 20 lines). Offer chat choice only when ambiguous.

| Runtime | Running chats? | Reinvoke same chat |
|---|---|---|
| Codex | `codex agents` | `codex resume <SESSION_ID> "<prompt>"` or `codex queue --thread <ID> --message "<prompt>"` |
| OpenCode | `opencode session list` | `opencode run --session <ID> "<prompt>"` |
| Claude Code | `claude agents` / `claude -r` picker | `claude --resume <ID> "<prompt>"` |

In the restart script, the CLI name in these commands is replaced by its resolved absolute path (Implementation step 2). A bare command name is not safe in a detached script.

Detect runtime: explicit user choice > env var (`$CODEX_THREAD_ID`, `$OPENCODE_SESSION_ID`, `$CLAUDE_SESSION_ID`) > parent CLI > ask once.

## Implementation

1. **Pass the checks.** Read the restart record (Loop Guard), then the restart-necessity test and the gate. Detect host: desktop-hosted (session lives in the OpenCode/Codex desktop app, e.g. `pgrep -f OpenCode.app` matches) vs pure CLI/TUI.
2. **Resolve everything the script needs to absolute values.** The detached script gets only a minimal default environment, so do not rely on anything it would have to look up.
   - **CLI binary.** In this order: a runtime-provided path variable if set (e.g. `$CODEX_APP_RUNTIME_CLI_PATH`) > `command -v <cli>` in the live session > the executable path of the running CLI/host process > the app bundle location. Use the absolute path in the script, never the bare name. The CLI may live inside an app bundle and not be on the system PATH at all.
   - **Host app** name or path (desktop host).
   - **Environment.** Bake the live session's `PATH` and any variable the reinvoke needs into the script as exports.
3. **Preflight - prove it will finish before the point of no return.** The point of no return is closing the host. Everything below runs first, while the live session can still react:
   - The CLI path is executable, and the reinvoke subcommand exists (for example `"$CLI" <subcommand> --help` succeeds; never guess flags).
   - The script passes a syntax check (`bash -n`).
   - The prompt file is written and readable, and the state directory is writable.
   - If any check fails: do not restart. Report exactly what failed and carry on as far as you can without the restart. Nothing was launched, so no restart record is needed.
4. **Write the prompt file** to a unique temp path (`mktemp`; if the sandbox `mktemp` returns a literal name, append `$$-$RANDOM`). Contents, max 20 lines:
   - Line 1: the marker `restarted-by: c-self-restart, count=1`
   - Why the restart happened (what must be live afterwards)
   - Goal + cwd + the next step to continue with
5. **Write the restart script** to a unique temp path. Log the reason for the restart as its first line. The script must:
   - Use the absolute CLI path and the baked-in environment from step 2.
   - Check the exit code of every step; on any failure log `FAILED: <step>`, set the record to `failed`, and exit non-zero. Never retry.
   - Install a `trap` so it removes itself on **any** exit, success or failure. The log always stays. On failure the prompt file also stays and its path is logged, so the user can resume by hand.
   - If a failure happens after the host was closed, still reopen the host so the user is not left without it, then record `failed` and stop.
   - CLI host sequence: sleep 2 -> pre-flight kill of any stale `<cli> run --session <ID>` processes -> reinvoke line per table with a timeout (10 min; kill and log on expiry) -> self-delete.
   - Desktop host sequence (macOS OpenCode): wait long enough for the current turn to finish (for example 15 seconds) -> graceful quit `osascript -e 'tell application "OpenCode" to quit'` -> poll up to 30s for the process to exit -> `open -a OpenCode` -> wait ~10s for boot -> pre-flight kill of stale resume runs -> reinvoke line per table with a timeout (10 min; kill and log on expiry) -> self-delete. The app may still require its quit confirmation; the delay does not guarantee otherwise. Never force-kill (`pkill -9`) - it loses session state. Never quit anything except the one host app.
6. **Record, then launch.** Write the restart record (`launching`), `chmod +x`, launch detached (`nohup ... > log 2>&1 &`).
7. **Hand off and exit.** State the resume line, the reason, and the paths of the log and the record in your final message, then exit immediately - continuing would duplicate the resumed session. Do not touch the session in the app until the headless run finishes (check the log), or two executors will share one session and wedge it.
8. **Make the resume prompt headless-safe.** The detached run cannot answer permission approvals, so it hangs forever on any `ask`. Before restarting, list what the remaining steps will read, write, and run:
   - If everything is covered by existing permissions or can be pre-approved (e.g. `permission.external_directory` allow-rules) before restarting, the resume prompt may carry the full continuation.
   - If some steps would need approvals you cannot pre-grant, the resume prompt covers only read-only verify steps, and the remainder waits for the user in the live session. Say so up front in your final message; if that leaves nothing useful to continue, skip the restart and report why instead.
9. **On resume:**
   - **FIRST action:** read the record and the marker, set the record to `resumed`, then check the thing that required the restart is actually live (skill in the skill tool list, MCP tool present, config effective). If yes -> proceed with the continuation, including any standing propagate-on-success instruction. If no -> do NOT copy/propagate anything and do NOT restart again (loop guard); diagnose (wrong host restarted? attached to old server?) and report.
   - **LAST action:** append a `DONE` marker line to the restart log and set the record to `done`, so the originator can confirm completion.

## Pairing with other skills

This skill triggers from a situation, and situations are easy to overlook, so add a one-line hook where the situation arises. Examples to paste into the instructions of the workflow concerned:

- In a skill-creation or skill-editing workflow: "If the new or edited skill is needed later in this same run, load c-self-restart after writing it."
- In an MCP/plugin/hook setup workflow: "If remaining steps use the server/plugin/hook you just configured, load c-self-restart to check whether a restart is needed."
- In a CLI upgrade workflow: "After upgrading the host CLI mid-workflow, load c-self-restart before continuing."

## Unknown CLI Commands

If your app's list/resume commands differ from the table (flags change across versions): research first (`<cli> --help`, official docs), verify the command works, then patch this skill's table and sync the fix to the common repo (`~/Documents/skills/`). Never guess flags in the restart script.

## Common Mistakes

- Waiting for the user to ask for a restart when the restart-necessity test already passes -> that is the case this skill exists for. Check the hard stops and restart.
- Restarting because it "might help" without verifying the thing is actually not live -> climb the ladder first.
- Plain close/reboot with no continuation -> don't load this skill.
- Asking permission when no hard stop applies -> this skill exists for autonomy. User presence, short tasks, and unclear presence are not stops; only a running chat or a device reboot is. Recent but idle chats do not block.
- A bare command name in the detached script -> it runs with a minimal PATH and crashes, often after the host is already closed. Resolve absolute paths and bake in the environment.
- Closing the host before proving the script can finish -> run the Preflight first; the quit is the point of no return.
- A loop guard that lives only in the resume prompt -> it vanishes exactly when delivery fails. Keep the restart record outside the chat and write it before launching.
- Retrying after a failed attempt, or restarting on re-entry because the chat shows no marker -> read the record; a non-`done` record means stop and diagnose.
- Script that exits early and leaves itself behind -> use a `trap` so it always removes itself; keep the log.
- `run --session` against the same live process and calling it a restart -> registry stays stale. Fresh host process first.
- Fresh session instead of same chat -> always resume/target per the table.
- Force-killing the desktop app -> session state loss. Graceful quit only.
- Fixed temp paths -> always unique per session.
- Propagating a skill the resumed self never verified -> always verify first (step 9).
- Resume prompt needing approvals -> headless run hangs on `ask` forever. Pre-approve writes, or limit the prompt to read-only verify (step 8).
- Touching the session in the app while the headless resume runs -> double executor wedges the session. Watch the log, not the chat.
- Restarting silently with no reason in the log or final message -> a returning user cannot tell what happened. Always log and state the reason.
