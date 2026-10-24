# Component patterns

Structural CSS for the components that most often come out broken. These patterns were rendered and checked with `scripts/layout_audit.js` at 375px and 1280px. They contain layout only. Colors, radii, fonts, and exact sizes are placeholders: swap in the project's tokens. Using them does not impose a look.

```css
:root { --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 24px; --control-h: 40px; --radius: 8px; }
*, *::before, *::after { box-sizing: border-box; }
```

## One control height, content centred
Every button, select, input, and chip in a row shares `--control-h` and the same font size. Centre content with flex rather than padding tricks.
```css
.control { height: var(--control-h); display: inline-flex; align-items: center; gap: var(--space-2);
           padding: 0 var(--space-3); font: inherit; border-radius: var(--radius); }
.icon-btn { width: var(--control-h); height: var(--control-h); display: inline-grid; place-items: center; padding: 0; }
```
Use real `<button>` for actions. Give icon-only buttons an `aria-label`. A non-interactive chip may use `.control` styling or a smaller token, but it must still centre its text.

## Select with a custom chevron
Reserve room for the chevron in padding so text never collides with it, and let the pseudo-element ignore clicks.
```css
.select { position: relative; display: inline-flex; }
.select select { appearance: none; font: inherit; height: var(--control-h);
                 padding: 0 calc(var(--space-3) * 2 + .5em) 0 var(--space-3); border-radius: var(--radius); }
.select::after { content: ""; position: absolute; right: var(--space-3); top: 50%; width: .5em; height: .5em;
                 border-right: 2px solid currentColor; border-bottom: 2px solid currentColor;
                 transform: translateY(-70%) rotate(45deg); pointer-events: none; }
```

## Input with an inline button (clear, search, reveal)
The wrapper draws the box and the focus ring. The input inside is borderless. Text stays centred because the wrapper has a fixed height and centres its children.
```css
.field { display: flex; align-items: center; gap: var(--space-2); height: var(--control-h);
         padding: 0 var(--space-3); border: 1px solid; border-radius: var(--radius); }
.field input { flex: 1; min-width: 0; border: 0; background: transparent; font: inherit; outline: none; }
.field:focus-within { outline: 2px solid; outline-offset: 2px; }  /* set the colour from your focus token */
```

## Alert / banner row: icon, message, action
One row, centred on the cross axis. The message takes the free space and can wrap. The action never shrinks or drifts to a corner.
```css
.alert { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-4); border: 1px solid; border-radius: var(--radius); }
.alert p { flex: 1; min-width: 0; margin: 0; }
.alert .control { flex: none; }
```
Only include an action that can change the outcome. "Retry" fits a network failure. It does not fit "no results", where a better action is to edit the query.

## Dialog shell sized by content
The panel is as tall as its content, capped by the viewport. Only the body scrolls. Margin from the viewport edge comes from the overlay's padding.
```css
.overlay { position: fixed; inset: 0; display: grid; grid-template-columns: minmax(0, 1fr); place-items: center; padding: var(--space-4); }
.panel { width: min(100%, 36rem); min-width: 0; max-height: 100%; display: flex; flex-direction: column; }
.panel-header { flex: none; display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-3); padding: var(--space-4) var(--space-5); }
.panel-header h1 { flex: 1 1 8rem; min-width: 0; margin: 0; }
.panel-body { overflow: auto; min-height: 0; padding: 0 var(--space-5) var(--space-5); display: flex; flex-direction: column; gap: var(--space-4); }
```
- Horizontal padding lives on `.panel-body` once. Children stretch to the same edges, so give them no margins or widths of their own.
- `flex-wrap: wrap` on the header, together with `min-width: 0` on the panel and a `minmax(0, 1fr)` grid column, is what keeps a row of controls from forcing the dialog wider than a phone.

## One status, one rendering
Derive a single status and render exactly one branch, so contradictory states cannot appear together.
```js
const status = loading ? 'loading' : error ? 'error' : results.length ? 'results' : query ? 'empty' : 'idle';
// render only the block for `status`; fallback or secondary content appears inside its own branch, labelled once
```
