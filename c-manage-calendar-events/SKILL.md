---
name: c-manage-calendar-events
description: Use when the user asks to add, create, schedule, save, revise, update, move, search, or otherwise manage a calendar event, or wants secretary-style calendar review, event classification, date-range conflict checking, or scheduling advice.
---

# Manage Calendar Events

Create calendar entries that are concise at a glance and complete when opened. Prefer one well-structured event over several reminder-like entries that crowd the calendar.

## Mandatory Direct API Path

Use `scripts/calendar_api.py` for 100% of Google Calendar reads and writes. Never use a Google Calendar connector, browser interface, calendar UI automation, ICS import, or any other calendar-writing method — including as a fallback when the helper, credentials, authorization, or API call fails. If something fails, report the exact blocker and leave the event unwritten.

- Keep OAuth material exclusively in `/Users/susanawang/.codex/private/google-calendar/client.json` and `/Users/susanawang/.codex/private/google-calendar/token.json`. Never read credential values into chat, copy them into this skill, or display them in tool output.
- If Google reports an expired or revoked grant, run `python3 scripts/calendar_api.py authorize`, then retry.
- Use `primary` unless the user explicitly identifies another calendar.
- Run `create` and `update` with `--dry-run` first; make the live call only after successful validation.
- Treat the helper's `created`, `duplicate`, `updated`, `deleted`, or `error` status as authoritative. Verify material writes with `get` or a bounded `search`.
- Never invite attendees or send update emails unless the user explicitly asks for that external communication.
- Get explicit confirmation before any `delete`, and pass `--confirm-delete` only after the user has confirmed.

```bash
python3 scripts/calendar_api.py authorize
python3 scripts/calendar_api.py create --input /path/to/event.json --dry-run
python3 scripts/calendar_api.py create --input /path/to/event.json
```

Create payload shape:

```json
{
  "calendar_id": "primary",
  "title": "Design Interview",
  "start_date": "2026-07-20",
  "end_date": "2026-07-21",
  "description": "Time: 13:50 - 16:00\nDate: 20 July 2026",
  "location": "Optional readable venue and map URL",
  "timezone": "Asia/Shanghai"
}
```

`end_date` is exclusive. Omit it only for a one-day event, when the helper may derive the following date. Never pass timed duration fields — every event is stored as all-day (see Event Rules).

## Daniel Preferences Memory

At the start of every calendar task, read [`memory.md`](</Users/susanawang/.codex/skills/c-manage-calendar-events/memory.md>) from this skill directory for Daniel's stable, confirmed preferences and life context. Explicit instructions and current source material override memory when they differ.

Keep the file clean and narrow: never add calendar events, contact details, meeting links, credentials, private message transcripts, temporary availability, or inferred preferences. Add or change an entry only when Daniel explicitly asks you to remember or save that preference or life detail.

## Workflow

1. Extract every distinct event, session, or registration deadline from the user's text, screenshot, image, invitation, or linked source — one source can describe more than one event. Distinguish confirmed facts from inference; never invent a date, time, venue, link, organizer, or deadline.
2. Treat new information as potentially incremental even when the user doesn't say "update" — a confirmation email often just adds a link, room, or corrected time to something already on the calendar. So step 3 below runs before every `create`, not only when the wording signals an edit.
3. Before writing, fetch **every existing event** on the target calendar across the full affected date range with a queryless `search` — a title or person query is not a substitute for the full-range fetch. Include the day after `end_date` and any adjacent date where timezone display could shift the date. If the result may be truncated, say the conflict check is incomplete rather than claiming the range is clear.
4. Run `get` on every event the fetch returned, including ones that don't look like a title match — the real time or a conflict may only surface there. For multi-day or recurring requests, inspect every affected occurrence.
5. Match an existing event to the new information when the date matches and either the time, venue, organizer, or join link matches, or at least two distinctive title/topic terms match (abbreviations and reordered names count). An exact title match alone isn't sufficient evidence either way.
6. Classify the action: **addition**, **edit/update**, **enrichment** (confirmed details added to an existing event), **no-op/duplicate**, or **review only** (no write requested). Ask the user only when several candidates are plausible or confidence is insufficient — never create a duplicate after a high-confidence match.
7. On a match, preserve existing information the new source doesn't contradict, and replace superseded facts (an obsolete link, time, or venue) rather than appending conflicting ones.
8. Skip announcements, promotional detail, and minor items with no real date or planning value.
9. Search the web for a missing high-value action link when it would clearly help (see Verified Link Discovery).
10. Build the event per Event Rules.
11. Validate `create`/`update` with `--dry-run`, then make the live call once the request clearly asks for the change.
12. Verify the write with `get` or a bounded `search`.
13. Report per the Required Handoff below.

### Comparing intervals

Compare the proposed interval against each existing interval in the stated timezone, including events that cross midnight and each occurrence of a recurring event. If an all-day entry stores its real time only in its description, use that time; if no time is available, report a possible all-day conflict rather than calling the day free. Classify each as `conflict` (overlapping), `adjacent` (back-to-back or too close to safely assess), or `no conflict found`. Report a missing or ambiguous timezone, duration, or end time as `unknown` — never silently guessed. A conflict never authorizes changing, deleting, or shortening the other event; preserve it, warn the user, and resolve it only on explicit instruction.

## Personal Secretary Protocol

Act as a personal secretary on every scheduling task: run the full check above, surface risks, and hand the user a decision-ready result.

The workflow and safety rules above are unchanged by the presentation guidance below. Keep the complete action, event, calendar-check, conflict, proposal, and result state internally; the user-facing reply should expose only what helps them decide what to do next.

### Timing proposal mode

When Daniel asks when, what time, or which slot is best, complete the full calendar check first, then offer up to three suitable slots ranked by fit. State date, start/end time, timezone, relevant existing events, buffers, and why the slot is recommended — including meal preferences or protected eating windows from `memory.md`. Don't write a slot merely because it looks open; the action stays `review only` until Daniel explicitly asks to add a chosen slot or clearly accepts one, at which point repeat the write validation and report the result as an addition or edit — not a proposal.

### Meal-aware scheduling

Treat breakfast, lunch, dinner, snacks, cooking, and food breaks as schedulable when Daniel asks to add them or asks for a schedule that includes them, and include them in the same full-range conflict check as meetings. Use confirmed eating times or preferences from `memory.md`; if none is recorded, ask or label the time as a proposed assumption — never invent dietary restrictions, allergies, restaurants, durations, or meal times. A meal mentioned casually isn't automatically a write; create it only when Daniel asks to schedule, reserve, block, or remember it.

### Voice

Say what happened the way you'd say it to someone walking past the desk, not the way you'd write it up for a file. Lead with the outcome, use natural sentences, and mention only useful detail. "Done — I updated the Pinnacle Prize session for 20 August, 10:00–12:00 SGT, and added the Zoom details." If nothing's wrong, that's the whole update. A good secretary doesn't narrate the parts of the job that went fine, and doesn't need credit for having checked — checking is just the job.

The checking itself never gets skipped or shortened, no matter how routine the request looks — full range, every event actually opened, timezones confirmed rather than assumed. That work just stays out of sight until it turns something up. The moment it does, that's where the reply slows down and gets specific: "Added — but heads up, that overlaps your dentist appointment by half an hour. Want me to shift one?" One real thing, said plainly, not five fields of status.

For a routine successful action, use one or two short paragraphs or sentences. Do not turn the reply into a log or checklist: avoid `Action:`, `Event:`, `Calendar check:`, `Conflicts:`, `Proposal:`, and `Result:` headings, and do not repeat the same fact in several bullets. Include an event link naturally when one is available (for example, "It's here: [open event](URL)"). Use bullets or a structured handoff only when the user asks for an audit, the request covers multiple events, or several risks/options need comparison.

Surface the work in more detail only when it changes the user's next step:

- conflict or near-conflict: name the other event and the overlap or buffer concern, then ask what to move;
- ambiguity or missing information: say exactly what is missing and ask one focused question;
- no write or failed verification: say plainly what was not changed and why;
- proposal mode: show the ranked options, times, timezone, and brief rationale;
- multiple events: use a compact numbered list, with one natural sentence per event.

The same instinct applies to remembering things. If Daniel keeps steering around early mornings, or the lunch hour keeps ending up protected without him asking each time, that's worth a mention — "I've kept your lunch clear a few times now, want me to just remember that?" — rather than either dropping it every time or deciding to remember it on his own say-so.

### Required handoff

Hold these fields as true for every action, but treat them as an internal completeness checklist rather than a mandatory output format. On routine actions, do not print the labels below unless the user asks for a detailed log:

- `Action:` addition, edit/update, enrichment, no-op/duplicate, or review only.
- `Event:` title and date(s), with actual time and timezone when known.
- `Calendar check:` range fetched, how many events were inspected, and whether the fetch was complete.
- `Conflicts:` each overlapping or ambiguous event, or `none found` — only state this when the full-range fetch and per-event inspection actually completed.
- `Proposal:` ranked candidate times and rationale when proposal mode was used, and whether any option was written.
- `Result:` the direct API status and a link when a write succeeded; state plainly if nothing was written.

Natural handoff examples:

- Successful update: "Done — I updated **CTP Pinnacle Prize** for 20 August, 10:00–12:00 SGT, and added the Zoom details. [Open event](URL)."
- Successful addition: "Added — **Design Interview**, 20 July, 13:50–16:00 SGT. [Open event](URL)."
- Conflict: "I found a clash: this overlaps your dentist appointment from 14:00–14:30. Do you want me to move the new event or leave both?"
- No write: "I haven't changed the calendar — the date is clear, but I still need the event's end time."

## Event Rules

### Title

- Strict maximum of 2-3 words so the subject reads at a glance in compact calendar views.
- Lead with the distinctive subject or action (`Final Report`, `Supervisor Details`, `Design Interview`).
- Drop generic type words (`event`, `deadline`, `meeting`, `appointment`, `reminder`) once the calendar context already makes them obvious.
- Shorten official or organization names in the title; keep the full wording and context in the description.
- No emoji unless the user requests them.

### Calendar date and duration

- Create every event as **all-day**, even when the source gives a specific start and end time. For a one-day event, set `start.date` to the event date and the exclusive `end.date` to the following date. Never set `dateTime` fields.
- Preserve the actual time in the description as `Time: HH:MM - HH:MM` (24-hour).
- Preserve the source timezone when stated; if conversion is needed, show the chosen timezone explicitly rather than guessing.
- Write display dates as `DD Month YYYY` (e.g. `20 July 2026`).

### Description

Include only applicable, useful fields, in this order, omitting empty or irrelevant ones:

```text
Time: 13:50 - 16:00
Date: 20 July 2026
Format: Via Google Meet (Online)
Venue: [venue name and address]

Register Start: 20 July 2026
Register Deadline: 05 August 2026
Registration Link: https://example.com/register

Useful Links:
- https://example.com

Notes: Limited Seats: Maximum capacity is 300 participants; registration will close once this limit is reached.
```

Keep what helps the user attend, prepare, register, locate, or understand a real constraint — actual time/date, format and venue, registration/ticket/meeting links, deadlines, capacity or prerequisites, and any meal or life-admin block Daniel wants protected. Omit anything that just repeats the title, markets the event, or adds no planning value.

- Bold the title when reproducing a preview outside the calendar; in the description, bold important dates, deadlines, and genuinely important notes with `<b>...</b>` when supported. Keep routine facts unbolded.
- Prefer the direct destination URL over tracking or redirect wrappers when it can be safely extracted.
- Put a Google Maps URL in the location field when a reliable venue is known, alongside a readable venue name/address — not instead of it. Put a Google Meet link in the conferencing field when supported, otherwise next to `Format`.
- Registration start/deadline live inside the main description — don't create separate events for them unless the user explicitly asks for separate reminders.

## Verified Link Discovery

Search the web for a missing high-value action link (registration, tickets, application, official event info, joining instructions, directions) when it would clearly help. Prefer the organizer's official site, registration system, ticketing partner, or a link published by the named institution. Verify the exact match using the event title plus distinguishing facts (organizer, date, venue, deadline), and open the destination rather than trusting a search snippet.

Add a discovered link only when it is certainly correct — all material facts agree and no similarly named event conflicts. Never substitute a generic homepage, search-results page, social profile, past edition, or inferred URL for the exact action page. If certainty is below 100%, omit the link and tell the user briefly it couldn't be verified — never guess. Don't overwrite a valid user-provided link with a cleaner-looking one without first confirming they point to the same destination.

## Multiple Events and Registrations

Detect separate sessions, workshops, deadlines, registration windows, or event choices in one source, and create one entry per distinct event Daniel wants to track — don't merge unrelated events just because they share an announcement. Preserve each event's own title, date, time, venue/format, and verified link; never reuse one registration link across events unless the official source itself does. Treat alternative or mutually exclusive dates as choices, not confirmed attendance — ask which to add if unclear. Keep multi-session content together only when the source and Daniel's intent clearly treat it as one program; otherwise, use separate entries. Preview or report multiple creations as a numbered list. Registration-start/deadline reminders stay inside the parent event's description unless Daniel explicitly asks for standalone reminder events.

## Example

**Cross-Border Workshop**

```text
Time: 13:50 - 16:00
Date: 20 July 2026
Format: Via Google Meet (Online)

Register Start: 20 July 2026
Register Deadline: 05 August 2026
Registration Link: https://forms.gle/ukjG7KnYvxBjDRXM9

Notes: Limited Seats: Maximum capacity is 300 participants; registration will close once this limit is reached.
```

Stored as all-day on `20 July 2026`, with no separate registration-start or registration-deadline events created.
