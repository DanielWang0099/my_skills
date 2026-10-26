# Schedule Preferences

The variable layer for `SKILL.md`. Read at the start of every scheduling task; edited by the assistant as it learns (add, modify, delete). The user's explicit instruction in the current conversation always overrides anything here.

- One short line per preference. Modify an entry instead of adding a conflicting one; delete entries that are withdrawn or replaced.
- Protected or avoided time carries a strength: **hard** (never schedule over it) or **soft** (avoid it, mention it if used).
- Never store events, contact details, meeting links, credentials, message transcripts, or temporary availability.

## Context

- Timezone: not set. Ask once, then save it here. Never infer it.
- Other calendars to check for availability: none recorded. Writes go to the primary calendar unless the user names another.
- Working days and hours: not recorded.

## Protected time

- None recorded.
- Format: `<what>: <days> <HH:MM-HH:MM> (hard|soft)`

## Meals and buffers

- Create meal or buffer blocks only when the user asks for them or marks them as protected time.
- Eating times: not recorded. If a slot touches a typical meal time, flag it and ask; don't assume.
- Dietary needs and restrictions: none recorded. Never assume any.
- Travel time between places: not recorded.

## Event format

- Storage: create every event as all-day, even when the source gives a start and end time. For a one-day event, set the start date to the event date and the exclusive end date to the next day. Never set timed start/end fields.
- Real time: keep it in the description as `Time: HH:MM - HH:MM` (24-hour). Use that time, not the all-day span, when checking for conflicts.
- Timezone: keep the source timezone when stated; if converting, show the chosen timezone explicitly.
- Title: strict maximum of 2-3 words. Lead with the distinctive subject (`Final Report`, `Design Interview`). Drop generic words like event, deadline, meeting, appointment, reminder. Shorten organization names; put the full wording in the description. No emoji unless asked.
- Dates: display as `DD Month YYYY` (e.g. `20 July 2026`).
- Description fields, in this order, skipping empty ones:

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

- Bold important dates, deadlines, and genuinely important notes with `<b>...</b>` where supported. Keep routine facts unbolded.
- Location field: put a Google Maps URL there when the venue is reliably known, alongside a readable venue name and address, not instead of it.
- Meet links: use the conferencing field when supported; otherwise place the link next to `Format`.
- Registration start and deadline stay in the parent event's description. Don't create separate reminder events unless asked.

## Communication

- Routine success: one or two natural sentences, outcome first, with the event link.
- Use lists only for several events, an audit, or comparing options.
- Proposals: up to three ranked slots, each with date, start-end, timezone, and a short reason.
- Ask before saving a preference that was only inferred from a pattern.

## Scheduling tendencies and dislikes

- None recorded.
