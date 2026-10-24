/*
 * layout_audit.js - measure a RENDERED page for the compositional defects that
 * make a UI look broken even when every element is "there".
 *
 * It evaluates to an array of findings (strings). An empty array means none of
 * the checks below tripped, which is necessary but not sufficient: still look
 * at a screenshot.
 *
 * Usage
 *   Browser console:  paste the whole file and read the returned array.
 *   Playwright:       const findings = await page.evaluate(fs.readFileSync('layout_audit.js', 'utf8'));
 *   Puppeteer:        same call as Playwright.
 * Run it at least at ~375px and ~1280px viewport widths, and again after any
 * state change that swaps content (error, empty, loaded).
 *
 * Checks
 *   text-off-centre  text sits noticeably higher/lower than centre inside its box
 *   control-padding  input/select with unequal top and bottom padding
 *   control-size     single-line input that is unusually tall
 *   peer-height      controls in one row differ slightly in height (near-miss)
 *   peer-text-size   controls in one row use different font sizes
 *   edge-near-miss   stacked siblings whose left (or box right) edges almost align
 *   dead-space       dialog/panel much taller than its content
 *   viewport-edge    fixed dialog nearly touching the viewport edge
 *   horizontal-scroll / overflow   content wider than its box or the page
 *   tiny-text        rendered text below 12px
 *   orphan-label     heading/label as the last thing in a stack, with nothing under it
 */
(() => {
  const out = [];
  const R = (e) => e.getBoundingClientRect();
  const CS = (e) => getComputedStyle(e);
  const num = (v) => parseFloat(v) || 0;
  const r1 = (n) => Math.round(n * 10) / 10;
  const visible = (e) => {
    const s = CS(e), b = R(e);
    return s.display !== 'none' && s.visibility !== 'hidden' && s.opacity !== '0' && b.width > 0 && b.height > 0;
  };
  const name = (e) => {
    const t = (e.innerText || e.value || '').trim().replace(/\s+/g, ' ').slice(0, 24);
    const cls = e.classList && e.classList.length ? '.' + [...e.classList].slice(0, 2).join('.') : '';
    return e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + cls + (t ? ` "${t}"` : '');
  };
  const flag = (rule, e, msg) => out.push(`[${rule}] ${name(e)}: ${msg}`);

  const CONTROL = 'button, [role="button"], select, summary, textarea, input:not([type=hidden]):not([type=checkbox]):not([type=radio]):not([type=range]):not([type=color])';
  const DIALOGISH = 'dialog, [role="dialog"], [aria-modal="true"], [class*="modal" i], [class*="dialog" i], [class*="popover" i], [class*="drawer" i], [class*="sheet" i]';

  const hasPaint = (e) => {
    const s = CS(e);
    const bg = s.backgroundColor;
    const filled = bg && bg !== 'rgba(0, 0, 0, 0)' && bg !== 'transparent';
    const bordered = ['Top', 'Right', 'Bottom', 'Left'].some((k) => num(s['border' + k + 'Width']) > 0 && s['border' + k + 'Style'] !== 'none');
    return filled || bordered;
  };

  // Union rectangle of the element's own (direct) text nodes.
  const ownText = (e) => {
    const rng = document.createRange();
    let t = Infinity, b = -Infinity, l = Infinity, r = -Infinity, any = false;
    for (const n of e.childNodes) {
      if (n.nodeType !== 3 || !n.textContent.trim()) continue;
      rng.selectNodeContents(n);
      for (const q of rng.getClientRects()) {
        if (!q.width) continue;
        any = true; t = Math.min(t, q.top); b = Math.max(b, q.bottom); l = Math.min(l, q.left); r = Math.max(r, q.right);
      }
    }
    return any ? { top: t, bottom: b, left: l, right: r } : null;
  };

  const boxedText = (e) => {
    const s = CS(e), b = R(e);
    return s.display !== 'inline' && b.height <= 140 && hasPaint(e) && !!ownText(e);
  };
  const isUnit = (e) => e.matches(CONTROL) || boxedText(e);

  const all = [...document.querySelectorAll('body *')].filter(visible);

  // 1. Text/padding centring inside boxes
  for (const e of all) {
    const s = CS(e), b = R(e);
    if (e.matches('input, select, textarea')) {
      const pt = num(s.paddingTop), pb = num(s.paddingBottom);
      if (Math.abs(pt - pb) > 2) flag('control-padding', e, `top padding ${r1(pt)}px vs bottom ${r1(pb)}px, so text sits off-centre`);
      if (e.matches('input') && b.height > 72) flag('control-size', e, `single-line input is ${r1(b.height)}px tall; check the height is intentional and the text is centred`);
      continue;
    }
    if (!boxedText(e)) continue;
    const t = ownText(e);
    const above = t.top - (b.top + num(s.borderTopWidth));
    const below = b.bottom - num(s.borderBottomWidth) - t.bottom;
    if (Math.abs(above - below) > Math.max(2, b.height * 0.12)) {
      flag('text-off-centre', e, `${r1(above)}px above the text and ${r1(below)}px below it inside a ${r1(b.height)}px box`);
    }
  }

  // 2. Peers in one row: heights and text sizes
  const parents = new Set(all.map((e) => e.parentElement).filter(Boolean));
  for (const p of parents) {
    const units = [...p.children].filter(visible).map((c) => (isUnit(c) ? c : c.querySelector(CONTROL))).filter((u) => u && visible(u));
    if (units.length < 2) continue;
    units.sort((a, b) => R(a).top - R(b).top);
    const rows = [];
    for (const u of units) {
      const ub = R(u);
      const row = rows.find((g) => {
        const gb = g.box, overlap = Math.min(ub.bottom, gb.bottom) - Math.max(ub.top, gb.top);
        return overlap >= 0.5 * Math.min(ub.height, gb.height);
      });
      if (row) { row.items.push(u); row.box = { top: Math.min(row.box.top, ub.top), bottom: Math.max(row.box.bottom, ub.bottom), height: Math.max(row.box.height, ub.height) }; }
      else rows.push({ items: [u], box: { top: ub.top, bottom: ub.bottom, height: ub.height } });
    }
    for (const { items } of rows) {
      if (items.length < 2) continue;
      const hs = items.map((u) => R(u).height);
      const hMin = Math.min(...hs), hMax = Math.max(...hs);
      if (hMax - hMin > 2 && hMax / hMin < 1.6) {
        flag('peer-height', items[hs.indexOf(hMax)], `row of ${items.length} controls has heights ${hs.map(r1).join(' / ')}px; give peers one shared height`);
      }
      const texty = items.filter((u) => u.matches('input, select, textarea') || (u.innerText || '').trim().length > 2);
      const fs = texty.map((u) => num(CS(u).fontSize));
      if (fs.length > 1 && Math.max(...fs) - Math.min(...fs) > 1) {
        flag('peer-text-size', texty[0], `controls in one row use font sizes ${fs.map(r1).join(' / ')}px`);
      }
    }
  }

  // 3. Stacked siblings: do they share edges?
  const ink = (e) => {
    let l = Infinity, r = -Infinity;
    const walk = (n) => {
      if (n.nodeType === 3) {
        if (!n.textContent.trim()) return;
        const rng = document.createRange(); rng.selectNodeContents(n);
        for (const q of rng.getClientRects()) if (q.width) { l = Math.min(l, q.left); r = Math.max(r, q.right); }
        return;
      }
      if (n.nodeType !== 1 || !visible(n)) return;
      if (hasPaint(n) || n.matches('img, svg, canvas, video')) { const b = R(n); l = Math.min(l, b.left); r = Math.max(r, b.right); return; }
      n.childNodes.forEach(walk);
    };
    walk(e);
    return l === Infinity ? null : { l, r };
  };
  for (const p of parents) {
    const s = CS(p);
    const stacked = s.display === 'block' || s.display === 'flow-root' || ((s.display === 'flex' || s.display === 'inline-flex') && s.flexDirection.startsWith('column'));
    if (!stacked) continue;
    const kids = [...p.children].filter((c) => {
      const cs = CS(c);
      return visible(c) && cs.position !== 'absolute' && cs.position !== 'fixed' && !cs.display.startsWith('inline') && !/^(script|style)$/i.test(c.tagName);
    });
    if (kids.length < 3) continue;
    const pb = R(p), pc = (pb.left + pb.right) / 2;
    const rows = kids.map((c) => ({ c, i: ink(c), painted: hasPaint(c) })).filter((x) => {
      if (!x.i) return false;
      const centred = Math.abs((x.i.l + x.i.r) / 2 - pc) < 3 && x.i.r - x.i.l < (pb.width - 8);
      return !centred;
    });
    const near = (key, list) => {
      const sorted = [...list].sort((a, b) => a.i[key] - b.i[key]);
      for (let k = 1; k < sorted.length; k++) {
        const d = Math.abs(sorted[k].i[key] - sorted[k - 1].i[key]);
        if (d > 1 && d <= 16) flag('edge-near-miss', sorted[k].c, `${key === 'l' ? 'left' : 'right'} edge is ${r1(sorted[k].i[key])}px but ${name(sorted[k - 1].c)} is at ${r1(sorted[k - 1].i[key])}px; align them exactly or make the difference deliberate`);
      }
    };
    near('l', rows);
    near('r', rows.filter((x) => x.painted));
  }

  // 4. Dialogs and panels: dead space, viewport edge
  const vw = innerWidth, vh = innerHeight;
  for (const e of document.querySelectorAll(DIALOGISH)) {
    if (!visible(e)) continue;
    const b = R(e), s = CS(e);
    const scrolls = e.scrollHeight > e.clientHeight + 1 && /(auto|scroll)/.test(s.overflowY);
    if (!scrolls) {
      let bottom = -Infinity;
      for (const d of e.querySelectorAll('*')) { if (visible(d) && CS(d).position !== 'absolute' && CS(d).position !== 'fixed') bottom = Math.max(bottom, R(d).bottom); }
      if (bottom > -Infinity) {
        const free = b.bottom - num(s.borderBottomWidth) - num(s.paddingBottom) - bottom;
        if (free > Math.max(80, b.height * 0.12)) flag('dead-space', e, `${r1(free)}px of empty space below the last content in a ${r1(b.height)}px container; size it to its content`);
      }
    }
    const fullBleed = b.width >= vw - 1 && b.height >= vh - 1;
    if ((s.position === 'fixed' || s.position === 'absolute') && !fullBleed) {
      const gaps = { top: b.top, left: b.left, right: vw - b.right, bottom: vh - b.bottom };
      const tight = Object.entries(gaps).filter(([, g]) => g >= 0 && g < 16).map(([k, g]) => `${k} ${r1(g)}px`);
      if (tight.length) flag('viewport-edge', e, `almost touches the viewport edge (${tight.join(', ')}); keep at least 16px of margin`);
    }
  }

  // 5. Overflow
  const de = document.documentElement;
  if (de.scrollWidth > innerWidth + 1) flag('horizontal-scroll', de, `page is ${de.scrollWidth}px wide in a ${innerWidth}px viewport`);
  for (const e of all) {
    const s = CS(e);
    if (e.matches('input, textarea, select, html, body') || s.display === 'inline') continue;
    if (s.overflowX === 'visible' && e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1) flag('overflow', e, `content is ${e.scrollWidth}px wide inside a ${e.clientWidth}px box`);
    const b = R(e);
    if (b.right > innerWidth + 1 && s.position !== 'fixed') flag('overflow', e, `extends ${r1(b.right - innerWidth)}px past the right edge of the viewport`);
  }

  // 6. Tiny text
  const seen = new Set();
  for (const e of all) {
    if (!ownText(e)) continue;
    const fs = num(CS(e).fontSize);
    if (fs < 12 && !seen.has(fs)) { seen.add(fs); flag('tiny-text', e, `${r1(fs)}px text; keep rendered text at 12px or larger`); }
  }

  // 7. Orphan labels
  for (const e of all) {
    if (!e.matches('h1, h2, h3, h4, h5, h6, legend, [class*="label" i], [class*="title" i], [class*="heading" i]')) continue;
    const t = ownText(e);
    if (!t || (e.innerText || '').trim().length > 40) continue;
    const p = e.parentElement;
    if (!p || [...p.children].filter(visible).length < 3) continue;
    const ps = CS(p);
    if (!(ps.display === 'block' || ps.display === 'flow-root' || (ps.display === 'flex' && ps.flexDirection.startsWith('column')))) continue;
    const later = [...p.children].filter(visible).filter((c) => R(c).top > R(e).top + 1);
    if (!later.length && num(CS(e).fontWeight) >= 600) flag('orphan-label', e, 'a label with nothing beneath it; render the section only when it has content');
  }

  return out;
})();
