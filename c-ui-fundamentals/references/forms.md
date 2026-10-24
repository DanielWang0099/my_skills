# Forms and inputs

Read this when the UI contains any input: sign-up and login, settings, checkout, search, filters, multi-step flows. Forms are where unpolished UI costs users the most, because mistakes here block them from finishing what they came to do.

## Contents
- Labels and layout
- Input types and attributes
- Validation and errors
- Buttons and submission
- Checkboxes, radios, switches, selects
- Passwords
- Multi-step flows and settings pages

## Labels and layout

- Every field has a visible label, linked with `for` and `id`. Placeholder text can show an example format, but it disappears on typing and usually fails contrast, so it never replaces the label.
- Place labels consistently (above fields is the most robust on narrow screens; beside fields is fine on wide, simple forms). Do not mix placements within one form.
- Default to one column. Use multiple columns only for short, clearly related fields (city and postal code, first and last name).
- Field width hints at expected input: a postal code is short, a street address is long. Do not stretch every input to the full container on a wide screen. Cap form width (roughly 480 to 640px for a single column).
- Group related fields under a heading or `<fieldset>` with `<legend>`. Radio and checkbox groups always use fieldset and legend.
- Spacing: label tight to its field, helper text tight below, then a clearly larger gap before the next field.
- Inputs and buttons placed side by side share the same height.

## Input types and attributes

Browsers do a lot of work for you when the right attributes are present:

- `type="email" | "tel" | "url" | "number" | "date" | "search" | "password"` as appropriate. Use `inputmode="numeric"` for digit-only codes where `type="number"` would add spinners or strip leading zeros.
- `autocomplete` values (`name`, `email`, `username`, `current-password`, `new-password`, `one-time-code`, `street-address`, `postal-code`, `cc-number`...) so browsers and password managers can fill the field.
- `required`, `min`, `max`, `minlength`, `pattern` where they match real rules.
- `autocapitalize="off"` and `spellcheck="false"` for emails, usernames, and codes.
- Text inputs are at least 16px on mobile, otherwise iOS zooms the page on focus.

## Validation and errors

- Validate on blur or on submit, not on every keystroke. Exceptions: password strength meters and username availability, which are useful live.
- Put the error message directly next to the field it concerns (usually below it), and make it specific: "Enter a date in the format DD/MM/YYYY", not "Invalid input".
- Connect it for assistive tech: `aria-invalid="true"` on the input and `aria-describedby` pointing to the message.
- Do not rely on a red border alone. Pair it with an icon or message text.
- On a failed submit, keep everything the user typed, move focus to the first invalid field, and for long forms add a summary at the top that links to each problem.
- Show format hints before the user errs (helper text below the field), not only after.
- Mark required or optional, whichever is the minority, and do it consistently.

## Buttons and submission

- The primary button label is the outcome ("Create account", "Save changes", "Place order"), not "Submit".
- One primary button per form. Cancel and secondary actions are visually quieter. Primary placement is consistent across the product.
- While submitting: show progress on the button, block double submits, and restore the button if it fails.
- Do not leave the submit button disabled with no explanation. Prefer an enabled button that reports what is missing, unless the missing requirement is obvious from the form itself.
- Confirm success and say what happens next.
- Warn before navigating away from unsaved changes.

## Checkboxes, radios, switches, selects

- The entire label is clickable, and the hit area is at least 44px tall on touch.
- Use a switch for settings that apply immediately, and a checkbox for choices applied when the form is submitted.
- Radios for 2 to 5 mutually exclusive options that should be visible together. A select for longer lists. A searchable combobox for very long lists.
- Prefer native `<select>` unless you will also build keyboard navigation, type-ahead, and ARIA. A broken custom dropdown is worse than a plain native one.
- Custom-styled checkboxes and radios still need a visible focus ring, checked and indeterminate states, and a disabled state.
- Option text is phrased so the answer is unambiguous. A switch label describes the "on" state.

## Passwords

- Offer a show/hide toggle (a real button with an accessible name).
- Do not block paste.
- State the requirements before the user types, not after they fail.
- Use `autocomplete="current-password"` for login and `new-password` for sign-up and change.

## Multi-step flows and settings pages

- Show the current step and total, label the steps, and let people go back without losing data.
- Settings pages decide on one save model and make it obvious: either autosave with a visible confirmation, or an explicit Save button that reveals unsaved state.
- Separate destructive settings (delete account, remove project) from ordinary ones. Their confirmation names the specific thing being deleted and states the consequence.
- Group settings by topic with clear headings, and describe each in one line of plain language, not implementation terms.
