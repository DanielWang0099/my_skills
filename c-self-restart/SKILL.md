---
name: c-self-restart
description: Use only when the user asks to restart the coding agent itself AND continue/resume the workflow afterwards (restart and continue, reinvoke after exit, resume after restart). Do NOT use for plain close/quit/reboot requests with no continuation.
---

# Self Restart

## Overview

The agent cannot restart its own process. It writes a one-shot shell script to the OS temp dir that restarts the host, reinvokes the same CLI targeting the same chat session, then deletes itself. No trace remains.

Registry rule: config and skills load once per **host process** start. Reinvoking a session inside the same live process (`run --session` against a running app/server) does NOT pick up new skills — that is a resume, not a restart. A real restart always starts a fresh host process first.

## When to Use

- User asks for restart/reinvoke **plus continuation**: "restart and continue", "reboot and pick up where you left off", "reinvoke yourself with ...".
- A medium/long multi-step workflow needs a clean agent process (stuck state, env change, upgrade) to continue uninterrupted.

When NOT to use (do not even load this skill):

- Plain "close codex", "quit", "restart the computer" with **no mention of continuing** — that's a shell/exit action, not this.
- Normal continuation in the same session — just keep working.
- Restarting a service, server, or app the user built.

## Auto-Restart Gate (all steps in order)

Unconfirmed agent restart is allowed **only** if every step passes. Otherwise, ask first.

1. **Task length.** Very short single-step task → ask first. Medium/long multi-step workflow → proceed to step 2.
2. **User presence.** User sending many messages back-to-back right now = actively watching → ask first. User idle / absent (fire-and-forget workflow) → eligible, proceed to step 3.
3. **Other chats hard check.** List sessions on this app (`codex agents`, `opencode session list`, `claude agents` / resume picker). If **any** other chat is running or recent → do NOT restart, report and ask. Only the current session may exist.
4. **Device vs agent.** Restarting the **device/OS** always needs explicit hard confirmation, even if steps 1–3 pass. Restarting only the **agent process** may proceed unconfirmed once steps 1–3 pass.

## Session Targeting

Default to reopening the **current** chat, with a prompt written for the circumstances (goal + cwd + next step, max 20 lines). Offer chat choice only when ambiguous.

| Runtime | Other chats? | Reinvoke same chat |
|---|---|---|
| Codex | `codex agents` | `codex resume <SESSION_ID> "<prompt>"` or `codex queue --thread <ID> --message "<prompt>"` |
| OpenCode | `opencode session list` | `opencode run --session <ID> "<prompt>"` |
| Claude Code | `claude agents` / `claude -r` picker | `claude --resume <ID> "<prompt>"` |

Detect runtime: explicit user choice > env var (`$CODEX_THREAD_ID`, `$OPENCODE_SESSION_ID`, `$CLAUDE_SESSION_ID`) > parent CLI > ask once.

## Implementation

1. Pass the gate above. Detect host: desktop-hosted (session lives in the OpenCode/Codex desktop app, e.g. `pgrep -f OpenCode.app` matches) vs pure CLI/TUI.
2. Write prompt file (goal + cwd + next step, max 20 lines) to a unique temp path (`mktemp`; if the sandbox `mktemp` returns a literal name, append `$$-$RANDOM`).
3. Write restart script to a unique temp path:
   - CLI host: sleep 2 → pre-flight kill of any stale `<cli> run --session <ID>` processes → reinvoke line per table with a timeout (10 min; kill and log on expiry) → self-delete.
   - Desktop host (macOS OpenCode): sleep 2 → graceful quit `osascript -e 'tell application "OpenCode" to quit'` → poll up to 30s for the process to exit → `open -a OpenCode` → wait ~10s for boot → pre-flight kill of stale resume runs → reinvoke line per table with a timeout (10 min; kill and log on expiry) → self-delete. Never force-kill (`pkill -9`) — it loses session state. Never quit anything except the one host app.
4. `chmod +x`, launch detached (`nohup ... > log 2>&1 &`), state the resume line, then exit immediately — continuing would duplicate the resumed session. Do not touch the session in the app until the headless run finishes (check the log), or two executors will share one session and wedge it.
5. Resume prompt must be headless-safe: the detached run cannot answer permission approvals, so it hangs forever on any `ask`. Keep it to read-only verify steps, or pre-approve every path it writes (e.g. `permission.external_directory` allow-rules) before restarting. Cross-directory copies without pre-approval belong in the live session afterwards, not in the resume prompt.
6. On resume, FIRST action: check the skill is actually registered (skill tool list). If yes → proceed, including any standing propagate-on-success instruction. If no → do NOT copy/propagate anything; diagnose (wrong host restarted? attached to old server?) and report. LAST action: append a `DONE` marker line to the restart log so the originator can confirm completion.

## Unknown CLI Commands

If your app's list/resume commands differ from the table (flags change across versions): research first (`<cli> --help`, official docs), verify the command works, then patch this skill's table and sync the fix to the common repo (`~/Documents/skills/`). Never guess flags in the restart script.

## Common Mistakes

- Plain close/reboot with no continuation → don't load this skill.
- User actively chatting, other chats running, or device reboot → gate steps 2–4 forbid unconfirmed restart.
- `run --session` against the same live process and calling it a restart → registry stays stale. Fresh host process first.
- Fresh session instead of same chat → always resume/target per the table.
- Force-killing the desktop app → session state loss. Graceful quit only.
- Fixed temp paths → always unique per session; missing `rm -f "$0"` → artifact lingers.
- Propagating a skill the resumed self never verified → always verify first (step 6).
- Resume prompt needing approvals → headless run hangs on `ask` forever. Read-only verify, or pre-approve writes (step 5).
- Touching the session in the app while the headless resume runs → double executor wedges the session. Watch the log, not the chat.
