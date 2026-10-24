---
name: c-ui-fundamentals
description: A style-neutral quality baseline for any user interface Codex builds or edits - web pages, apps, components, dashboards, forms, landing pages, settings screens, HTML/CSS/React/Vue/Tailwind output. Prevents UI that is technically present but visibly broken, such as text off-centre in controls, mismatched heights, ragged edges, dead space, overflow on phones, and contradictory states. Also covers spacing, typography, contrast, hierarchy, interactive states, empty/loading/error states, responsiveness, forms and basic accessibility, without prescribing any aesthetic, palette, typeface or layout style. Use this whenever a task produces or modifies a UI, even if the user never mentions design, polish or quality, and use it alongside any style-specific guidance or the user's own brand or design system, which decide the look while this skill guards the quality floor.
---

# UI Fundamentals

A quality floor for any interface you build or edit. It answers one question: what separates UI that feels finished from UI that feels like a draft? It deliberately says nothing about what the UI should look like.

## How this fits with everything else

- The user's brief, brand, design system, or existing codebase decide the **look**: palette, typeface, shape language, density, tone. Follow them exactly, including when the look is plain, dense, loud, or unconventional.
- If other design guidance is loaded alongside this skill, it decides the look. This skill decides whether the result is **well made**.
- If nothing specifies a look, choose one that fits the product and its audience, then apply it consistently. This skill does not nominate a house style, so do not treat any example value below as one. Numbers here are the points where problems begin, not target aesthetics.

Why it works this way: polish is mostly the absence of small mistakes. A stark monospace table and a soft, rounded onboarding flow can both be polished, and both turn unpolished in the same ways: cramped padding, inconsistent spacing, weak contrast, missing states, broken on a phone. People forgive plain. They do not forgive sloppy.

## Where broken UI actually comes from

Most horrible-looking UI is not an ugly style. Every element exists, but the relationships between them are wrong. The same few causes recur, so check for them explicitly:

1. **Control internals.** Text that is not vertically centred in its button, chip, or input; peers in one row with different heights or text sizes; a chevron overlapping text. Give controls one shared height, centre their content with flex (`display: inline-flex; align-items: center`), and never pair a tall box with top-heavy padding.
2. **Containers sized by magic numbers instead of content.** Fixed or viewport-sized modals and panels leave dead space and crowd the screen edge. Let content set the size, cap it with `max-height` and scroll the body, and keep at least 16px from the viewport edge.
3. **Every child sets its own horizontal geometry.** Per-child margins, widths, and padding give each block a different left and right edge. Set horizontal padding once on the container and let children stretch.
4. **Rows that drift or overflow instead of aligning.** A message and its action landing in opposite corners, a header that spills off a phone. Flex rows use `align-items: center`, the text item gets `flex: 1; min-width: 0`, the action gets `flex: none`, and the row can wrap at narrow widths.
5. **Incoherent state.** An error and a result showing together, one message said three times, an action that cannot change the outcome (Retry on "not found"), a section label with nothing under it. Derive one status and render one branch. Each message does one job. An action must help in that situation.
6. **Filler.** Sections rendered for data that does not exist, redundant text, numbering on items that are not a sequence. If there is nothing to show, show nothing.

`references/component-patterns.md` has render-tested CSS for the structures involved (shared control height, chip, icon button, select, input with inline button, alert row, dialog shell, wrapping header).

## Workflow

1. **Read the constraints.** Framework, component library, existing tokens, existing styles, target devices. Reuse the project's tokens and components before inventing new ones.
2. **Set up the system before building components.** Declare tokens (section 1), then build only from them.
3. **Build every state, not just the happy path** (section 8). A UI that only works with the data it was designed around is the most common kind of unfinished.
4. **Review before delivering.** If you can render the page, run `scripts/layout_audit.js` at about 375px and 1280px (and again after states change), fix every finding, then look at a screenshot. The script measures the failures in the section above, but it cannot judge taste. If you cannot render, walk the checklist at the end of this file. Fix problems rather than listing them as caveats.

---

## 1. Systems over one-offs

Inconsistency is the largest single source of "unpolished". It happens when every value is chosen locally and independently. Fix it by declaring a small set of tokens once (CSS custom properties, a theme object, a Tailwind config, whatever the project uses) and using only those:

- **Spacing scale** on a 4px or 8px base (for example 4, 8, 12, 16, 24, 32, 48, 64).
- **Type scale**: a limited set of sizes with paired line-heights, and a limited set of weights.
- **Color roles, not raw colors**: background, surface, text, text-muted, border, primary (plus hover and active), focus ring, and semantic success, warning, danger, info.
- **Radius**: a small set. The same kind of element gets the same radius.
- **Elevation and borders**: one convention for how things separate from their surroundings.
- **Motion**: a couple of durations and one or two easings.
- **Layers**: named z-index values (dropdown, sticky, overlay, modal, toast) so nobody reaches for `z-index: 9999`.

The values are yours to choose or inherit. What matters is that once declared, components contain no stray one-offs: no `margin-left: 13px`, no hex code that is not in the palette.

## 2. Spacing and grouping

- Spacing communicates grouping. Space inside a group is smaller than space between groups. A label sits closer to its field than to the previous field; a heading sits closer to its content than to the content above it.
- Padding inside containers is consistent and roomy enough that content never feels pressed against an edge. As a floor: controls need at least about 8px vertical and 12px horizontal padding, panels at least 16px.
- Page gutters are at least 16px on phones. Text never touches the viewport edge.
- Space siblings with `gap` on flex or grid rather than margins on each child. That avoids doubled margins and stray trailing space.
- Use more space between sections than between items. The same gap everywhere gives a flat rhythm with no visible structure.

## 3. Typography

- Build hierarchy from size, weight, and color. Use a handful of sizes and no more than three weights, and make each level distinguishable at a glance.
- Reading text is at least 16px. Dense app UI, tables, and labels can go to 14px. Nothing goes below 12px.
- Line-height: about 1.4 to 1.6 for body text, tighter (about 1.1 to 1.3) for large headings.
- Cap running text at roughly 45 to 75 characters per line (`max-width: 65ch`). Do not center-align paragraphs longer than two or three lines.
- Always give a font stack with fallbacks, so a failed webfont does not drop to a browser-default serif. Form controls do not inherit fonts by default; set `font: inherit` on them.
- Right-align numeric columns and use tabular figures (`font-variant-numeric: tabular-nums`) so digits line up.
- Handle long strings: wrap (`overflow-wrap: anywhere`) or truncate with an ellipsis, but never overflow. Use `text-wrap: balance` on headings to avoid one-word last lines.

## 4. Color and contrast

- Text contrast is at least 4.5:1 against its actual background (3:1 for large text, 24px or 19px bold and up). Borders that identify controls, meaningful icons, and focus rings need 3:1.
- The usual failures are muted or secondary text, placeholder text, text on tinted or colored surfaces, and text over images. Check those first. Put a scrim or solid container behind text that sits on an image.
- Keep the palette small: neutrals, one primary, semantic colors. Add more only for a reason, such as chart series.
- Never rely on color alone for meaning (errors, status, chart series, links inside prose). Add an icon, text, underline, or pattern.
- Semantic colors mean the same thing everywhere. Do not use the danger color as decoration or style a destructive action as primary.
- If supporting light and dark, define each as its own set of role tokens and check contrast in both. Do not mechanically invert. If only one theme was requested, build only that one. Set `color-scheme` to match so native controls and scrollbars follow.

## 5. Layout and alignment

- Elements in a column share a left edge (or a deliberate alternative). Elements in a row share a baseline or center line. If two things are almost aligned, align them exactly or make the difference obviously intentional.
- Constrain content width with a container (`max-width`) so layouts do not stretch across a wide monitor. A single-line input spanning 1400px is a tell.
- Use grid and flex rather than fixed positions. Avoid fixed heights on content containers; let content set the height and use `min-height`.
- Peers in a row (buttons, inputs, cards, stat tiles) get equal height and consistent internal alignment.
- Give flex and grid children that contain text `min-width: 0` so they can shrink or truncate instead of blowing out the layout.
- Sticky or fixed headers and footers must not cover content. Add `scroll-padding` and bottom padding.
- Icons sit on the same line box as their text, vertically centered, sized from the adjacent text size, with a consistent gap.
- Do not nest bordered or shadowed containers inside each other (card in card in card) unless each layer carries distinct meaning. Do not stack border, shadow, and outline on the same edge.

## 6. Hierarchy and focus

- Each view or region has one primary action, visibly stronger than the rest. Secondary and tertiary actions are progressively quieter. If three buttons look equally loud, nothing is primary.
- Visual weight follows importance. What the user came for is most prominent. Chrome, metadata, and helper text recede.
- Destructive actions look different from safe ones, are not adjacent and identical to them, and ask for confirmation when irreversible.
- Reading order and DOM order match: the most important information comes first.

## 7. Interactive states

Every interactive element needs distinct, visible states for default, hover (pointer devices), `:focus-visible`, active or pressed, and disabled. Add loading, selected or current, and invalid where relevant.

- Never remove the focus outline without a replacement at least as visible. The ring must be visible on every background it can appear on.
- Touch targets are at least 44x44 CSS px (24x24 is the absolute minimum, with spacing). Give small icon buttons padding to reach the size rather than enlarging the icon.
- Clickable things look clickable and have the right cursor. Non-clickable things do not look like buttons or links.
- Do not hide essential actions behind hover. Touch devices have no hover.
- Pending actions show progress within about 100ms, block repeat submission, and recover cleanly on failure.
- Transitions run about 100 to 250ms on specific properties (color, background, opacity, transform), not `transition: all`, and never delay input. Wrap non-essential motion in `prefers-reduced-motion`. Motion is optional; state feedback is not.
- Use real elements: `<button>` for actions, `<a href>` for navigation. A clickable `<div>` loses keyboard, focus, and screen-reader behavior.

## 8. States beyond the happy path

For every data-driven view, design and build:

- **Loading**: a skeleton or spinner sized so the page does not jump when content arrives. No blank flash.
- **Empty**: say what belongs here and offer the one action that fills it.
- **Error**: say what went wrong and what to do next, offer retry, and keep the user's input.
- **Edge content**: zero, one, and many items; very long and very short text; missing images (fall back to initials or a neutral placeholder); large numbers.
- **Success**: confirm actions that have side effects.

Use realistic sample content: plausible names, varied lengths, believable numbers and dates. Avoid lorem ipsum, "Item 1", ten identical rows, and a button labeled "Button". Realistic content also exposes layout bugs that tidy placeholder text hides.

Reserve space for images and media (`width` and `height`, or `aspect-ratio` with `object-fit`) so content does not shift as they load. Decide for each text element whether long content wraps, truncates (with the full text reachable), or clamps. It should never overflow.

## 9. Responsive behavior

- Include `<meta name="viewport" content="width=device-width, initial-scale=1">`.
- Design the narrow layout first and add complexity as space grows. Prefer fluid sizing (`%`, `fr`, `minmax`, `clamp`) over fixed pixel widths, and set breakpoints where the content breaks rather than at device names.
- No horizontal page scroll at 360px. Wide content (tables, code, charts) scrolls inside its own container or reflows.
- Navigation collapses sensibly. Spacing and tap targets grow on touch; they do not shrink.
- Look at roughly 360-390, 768, and 1280+ widths. Text should remain usable when zoomed to 200%.
- Use `100dvh` rather than `100vh` for full-height mobile layouts, and respect safe-area insets for edge-to-edge designs.

## 10. Consistency across the UI

- The same function looks the same everywhere: every primary button identical, every text input the same height, radius, and border treatment.
- One icon family with consistent size and stroke. Every icon-only button has an accessible name (`aria-label`). Do not mix emoji and icon-set glyphs as icons unless the style deliberately calls for it.
- Same word for the same action throughout. One capitalization convention. Consistent date, number, and currency formats (`Intl.NumberFormat` and `Intl.DateTimeFormat` handle this).
- If the codebase already has a modal, toast, or button component, use it instead of writing a near-duplicate.

## 11. Accessibility essentials

These are cheap and cover most of the real-world damage:

- Semantic structure: one `h1`, headings in order, landmarks (`header`, `nav`, `main`, `footer`), lists as lists, tables as tables with `th`.
- Every input has an associated visible label. Images have `alt` (empty `alt=""` when decorative). `<html>` has `lang`.
- Everything works by keyboard in a logical order with no traps. Dialogs move focus in, trap it, close on Esc, and restore focus on close.
- Use ARIA only where native elements cannot do the job. Use `role="status"` or `aria-live` for async messages, and `aria-invalid` with a described error on invalid fields.
- Font sizes in `rem` so user text-size settings work.

## 12. Copy

Words are part of the interface, so keep them as deliberate as spacing:

- Buttons name the outcome ("Save changes", "Send invite"), not "Submit" or "OK".
- Errors say what happened and how to fix it, without blaming the user. Empty states invite an action.
- Pick one capitalization style and keep it. Leave no placeholder text behind.

---

## Polish is not decoration

Polishing means removing mistakes, not adding effects. Do not add gradients, shadows, animation, illustrations, or extra sections to make something "feel designed". Those are style decisions and belong to the brief. When a layout feels flat or amateur, the usual fix is stronger hierarchy, better spacing, or exact alignment, not ornament. Do not add features or sections nobody asked for.

## Tells of unpolished UI

Scan for these before delivering:

- Browser defaults showing through: unstyled buttons, selects, or inputs; default blue underlined links where unintended; the 8px body margin; a default serif from a failed font stack.
- Text or controls touching container or viewport edges; similar containers with different padding.
- Near-miss alignment; peers in a row with unequal heights; an icon off-center from its label.
- Low-contrast muted text; placeholder text doing the job of a label; removed focus outlines.
- Everything the same size and weight, or several competing primary buttons.
- Mixed radii, shadows, borders, or icon styles with no logic; border plus shadow plus outline on one edge.
- One-off pixel and hex values; `z-index: 9999`.
- Layout that breaks with real content: overflowing text, huge empty gaps, unbounded line lengths.
- Layout shift on load; images popping in and pushing content.
- Horizontal scroll on a phone; tiny tap targets; hover-only controls.
- Blank screen while loading, an endless spinner, a raw error string, an empty table showing only headers.
- Placeholder content: lorem ipsum, "Item 1", "Click here", identical sample rows.
- Icon-only buttons without names; clickable divs; text that looks like a link and links that look like text.
- Left-aligned numbers, inconsistent decimals, unlabeled axes or units.
- Modals that cannot be dismissed, do not trap focus, or let the page scroll behind them.

## Before you deliver

1. Spacing, type, color, and radius all come from declared tokens. No stray one-off values.
2. Spacing reflects grouping. Padding is consistent. Mobile gutters are at least 16px.
3. Type hierarchy is clear, body text is 16px (14px if dense), line length is capped, fonts have fallbacks.
4. Contrast holds for muted text, text on tinted or image backgrounds, input borders, and the focus ring.
5. Each view has one clear primary action. Destructive actions are distinct.
6. Every interactive element has hover, focus-visible, active, and disabled states (plus loading where relevant), and targets are large enough.
7. Loading, empty, and error states exist. Long, short, and zero content have been considered. No lorem ipsum.
8. No horizontal scroll at 360px. Looks right at about 768px and 1280px+.
9. Forms and data displays follow the reference files below.
10. The keyboard path works, semantic elements are used, images have alt text, icon buttons are named.
11. Same things look the same. Nothing was added purely as decoration. The look matches the brief.
12. If renderable, `layout_audit.js` reports no findings at phone and desktop widths.

## Reference files

- `references/forms.md`: read when the UI has any inputs, such as forms, auth, settings, checkout, or multi-step flows.
- `references/data-display.md`: read for tables, lists, card grids, stat tiles, charts, or dashboards.
- `references/component-patterns.md`: read when building headers, toolbars, dialogs, chips, selects, inputs, or alerts.
- `scripts/layout_audit.js`: run in a rendered page (browser console, Playwright, or Puppeteer) to measure off-centre text, peer mismatches, ragged edges, dead space, overflow, tiny text, and orphan labels.
- `assets/base.css`: a structural reset with no colors, fonts, sizes, radii, or shadows, so it imposes no style. Merge it into the project's global CSS, or inline it in single-file output. It covers `box-sizing`, control font inheritance, media sizing, a zero-specificity focus-visible ring, cursors, reduced motion, and truncation helpers.
