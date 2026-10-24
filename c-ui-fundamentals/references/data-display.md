# Data display: tables, lists, cards, stats, charts, dashboards

Read this when the UI presents data. Data views break in predictable ways: columns that do not line up, one long value that wrecks a layout, numbers that are hard to compare, and charts nobody can read on a phone.

## Contents
- Tables
- Lists and card grids
- Stat tiles and KPIs
- Charts
- Numbers and dates
- Dashboards

## Tables

- Use a real `<table>` for tabular data, with `<th scope>` for headers and a caption or `aria-label`.
- Alignment: text left, numbers right (tabular figures, the same number of decimals within a column). Put units in the column header rather than repeating them in every cell. Keep date formats identical down a column.
- Status is text plus color, never color alone.
- Row padding is comfortable even at a dense setting (about 8px vertical at minimum), with consistent row height and a clearly distinct header. Use row dividers or zebra striping, not both. Which one is a style choice.
- Long tables get a sticky header. Wide tables scroll inside their own container (a sticky first column helps). On narrow screens, decide deliberately between horizontal scroll and reflowing rows into stacked cards.
- Prevent one long value from blowing out a column: set column widths or `table-layout: fixed`, truncate with an ellipsis, and make the full value reachable (tooltip, expand, detail view).
- Sorting shows its current state (arrow plus `aria-sort`). Filtering shows what is applied and offers a clear-all.
- Empty and no-results states replace the body with a message and an action ("Clear filters"), not an empty grid with only headers.
- Long data uses pagination or virtualization and shows counts ("1-25 of 312").
- Row actions sit in a consistent place. Icon-only actions have accessible names and adequate hit areas.

## Lists and card grids

- Use `grid-template-columns: repeat(auto-fill, minmax(<min>, 1fr))` so the grid reflows without breakpoints.
- Cards in a row have equal height, with actions or footers pinned to the bottom so they line up across cards.
- Images in cards share one aspect ratio and use `object-fit` so mixed source sizes do not produce a ragged grid.
- A clickable card has one primary link target (a stretched link). Do not nest buttons and links in ways that fight over the click.
- Text inside cards is truncated or clamped by a deliberate rule so card heights stay predictable.

## Stat tiles and KPIs

- Each tile has a label, a value, and context: time period, comparison, and a delta with sign and direction.
- Never show a delta in color alone. Add an arrow or a +/- sign.
- Format values consistently (units, compact notation such as 1.2M under a single rule) and avoid false precision.
- Tiles are visually weighted by importance. Twelve equally loud tiles communicate nothing.

## Charts

- A title or caption states what is being shown. Axes are labeled with units. Number formats use separators or compact notation.
- Bar charts start at zero. Use 3 to 6 axis ticks. Gridlines are quiet and never louder than the data.
- Prefer direct labels to a legend when there are few series. When a legend is needed, its order matches the visual order.
- Color: no more than about six categories. Keep each category's color the same across every chart on the page. Make series distinguishable by lightness or pattern as well as hue so color-blind readers can tell them apart.
- Text inside charts is at least about 11 to 12px and still fits at 360px width. Charts resize with their container.
- Make the data reachable without a mouse: keyboard-reachable tooltips or an adjacent summary or table.
- Each chart has its own loading, empty, and error state, sized to avoid layout shift.
- Avoid 3D, avoid dual axes unless truly necessary, and use pie or donut charts only for a few parts that sum to a whole.
- Time axes use even intervals. Label the timezone where it matters.

## Numbers and dates

- Format with `Intl.NumberFormat` and `Intl.DateTimeFormat` rather than hand-built strings, so locale, grouping, and currency are right.
- Keep decimals, negative-number style, and date format consistent across the whole product.
- Relative times ("3 hours ago") should expose the absolute time on hover or focus.

## Dashboards

- Lead with the few metrics that matter most, then group related views under clear headings.
- Controls (date range, filters) live in one consistent place and clearly show the current selection.
- Every widget handles its own loading and error state, so one failing request does not blank the page.
- Align widgets to a shared grid. Mixed widths with ragged edges read as unfinished.
