# Calendar Preferences Memory

Purpose: store only stable, explicitly confirmed preferences and life context
that help with calendar planning.

## Confirmed preferences

- Default planning timezone: ask the user or use their configured timezone; do
  not infer it.
- Prefer proactive, secretary-style calendar support: check the full affected
  date range, surface conflicts, and distinguish proposals from actual writes.
- Consider buffers and meal breaks only when the user asks for them or
  explicitly marks them as protected time.

## Boundaries

- Do not store events, contacts, meeting links, credentials, message
  transcripts, temporary availability, or inferred preferences here.
- Add or change an entry only when the user explicitly asks to remember or save
  that preference or life detail.
