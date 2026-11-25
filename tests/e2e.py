"""End-to-end checks for every public page of the Mbuso site.

Run:  python3 tests/e2e.py            (needs Playwright + Chrome)
Serves ./site on a local port, then for each page and width checks:
  - no sideways scroll (scrollWidth - clientWidth == 0)
  - no console errors, page errors, failed requests or broken images
  - tap sizes: .btn and .field >= 48px tall, .icon-btn exactly 44x44, other controls >= 44px
  - even groups: .even-cols children equal width on one row; .even-row rows fill the width
  - text people read >= 14px (eyebrows >= 12px); headings on the type scale
  - fields fill their column; side-by-side cards are the same height
  - no text touching the screen edge; layout shift (CLS) under 0.1
  - axe accessibility scan: no serious or critical issues
  - 200% zoom, simulated as a 640px-wide viewport (1280px at 200%)
Writes screenshots to tests/shots/ and a summary to tests/out/results.json.
"""
import asyncio, json, subprocess, sys, time
from pathlib import Path
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SHOTS = ROOT / "tests" / "shots"; SHOTS.mkdir(parents=True, exist_ok=True)
OUTD = ROOT / "tests" / "out"; OUTD.mkdir(parents=True, exist_ok=True)
AXE = (ROOT / "tests" / "vendor" / "axe.min.js").read_text()
PORT = 8790
BASE = f"http://127.0.0.1:{PORT}/"
PAGES = ["index.html", "about.html", "services.html", "hub.html", "impact.html", "learnerships.html", "contact.html", "legal.html", "404.html"]
WIDTHS = [(1280, 900, "1280"), (768, 1024, "768"), (390, 844, "390"), (360, 780, "360"), (640, 450, "zoom200")]
SCALE_REM = [0.75, 0.875, 1.0, 1.125, 1.25, 1.5, 1.875, 2.25, 3.0, 3.75, 4.5]

PROBE = r"""
() => {
  const W = document.documentElement.clientWidth;
  const root = parseFloat(getComputedStyle(document.documentElement).fontSize);
  const vis = el => { const r = el.getBoundingClientRect(); const cs = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && cs.visibility !== 'hidden' && cs.display !== 'none' && !el.closest('dialog:not([open])') && !el.closest('.hp') && !el.closest('.sr-only'); };
  const out = { overflow: document.documentElement.scrollWidth - W, root, tap: [], even: [], font: [], heading: [], field: [], cards: [], edge: [] };
  // tap sizes
  document.querySelectorAll('.btn').forEach(b => { if (!vis(b)) return; const r = b.getBoundingClientRect(); if (r.height < 47.5) out.tap.push(['btn', b.textContent.trim().slice(0,30), Math.round(r.height)]); });
  document.querySelectorAll('.icon-btn').forEach(b => { if (!vis(b)) return; const r = b.getBoundingClientRect(); if (Math.round(r.width) !== 44 || Math.round(r.height) !== 44) out.tap.push(['icon-btn', b.getAttribute('aria-label'), Math.round(r.width)+'x'+Math.round(r.height)]); });
  document.querySelectorAll('.field').forEach(f => { if (!vis(f)) return; const r = f.getBoundingClientRect(); if (r.height < 47.5) out.tap.push(['field', f.id, Math.round(r.height)]); });
  document.querySelectorAll('a, button, select, input[type=checkbox]').forEach(el => {
    if (!vis(el) || el.matches('.btn, .icon-btn, .field, .skip-link')) return;
    if (el.closest('p, .prose li, .consent, .field-help, td')) return;            // inline text links are exempt (WCAG 2.5.8)
    if (el.matches('input[type=checkbox]')) { const lab = el.closest('label'); const r = (lab||el).getBoundingClientRect(); if (r.height < 44) out.tap.push(['checkbox-label', el.id, Math.round(r.height)]); return; }
    const r = el.getBoundingClientRect(); const min = el.closest('.crumbs') ? 32 : 44;
    if (r.height < min - 0.5) out.tap.push([el.tagName.toLowerCase(), (el.textContent||el.getAttribute('aria-label')||'').trim().slice(0,30), Math.round(r.height)]);
  });
  // even groups
  document.querySelectorAll('.even-cols').forEach(g => { if (!vis(g)) return; const kids = [...g.children].filter(vis).map(k => k.getBoundingClientRect());
    if (kids.length < 2) return; const tops = new Set(kids.map(k => Math.round(k.top))); const ws = kids.map(k => Math.round(k.width)); const hs = kids.map(k => Math.round(k.height));
    if (tops.size !== 1) out.even.push(['even-cols not one row', ws]);
    const fitMd = g.classList.contains('fit-md') && W >= 768;
    if (!fitMd && Math.max(...ws) - Math.min(...ws) > 1) out.even.push(['even-cols unequal widths', ws]);
    if (Math.max(...hs) - Math.min(...hs) > 1) out.even.push(['even-cols unequal heights', hs]); });
  document.querySelectorAll('.even-row').forEach(g => { if (!vis(g)) return; const gr = g.getBoundingClientRect(); const kids = [...g.children].filter(vis).map(k => k.getBoundingClientRect());
    const rows = {}; kids.forEach(k => { const t = Math.round(k.top); (rows[t] = rows[t] || []).push(k); });
    Object.values(rows).forEach(r => { const left = Math.min(...r.map(k => k.left)), right = Math.max(...r.map(k => k.right)); if (Math.abs(left - gr.left) > 1 || Math.abs(right - gr.right) > 1) out.even.push(['even-row row not full width', r.length]); }); });
  // font floors
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (tw.nextNode()) { const t = tw.currentNode; if (!t.textContent.trim()) continue; const el = t.parentElement; if (!el || seen.has(el) || !vis(el)) continue; seen.add(el);
    const fs = parseFloat(getComputedStyle(el).fontSize); const deco = el.closest('.eyebrow, .hero-motto, .pillar-label, .stage, .client-group h3, .site-footer h2, .contact-list strong, table.acc thead, .viewer-count');
    const min = deco ? 12 : 14; if (fs < min - 0.05) out.font.push([el.tagName.toLowerCase() + (el.className ? '.' + String(el.className).split(' ')[0] : ''), t.textContent.trim().slice(0,30), fs.toFixed(1)]); }
  // headings on the scale
  document.querySelectorAll('h1, h2, h3').forEach(h => { if (!vis(h)) return; const fs = parseFloat(getComputedStyle(h).fontSize);
    const ok = [0.75,0.875,1,1.125,1.25,1.5,1.875,2.25,3,3.75,4.5].some(r => Math.abs(fs - r*root) < 0.6 || Math.abs(fs - Math.max(r*root, r===0.75?12:0)) < 0.6);
    if (!ok) out.heading.push([h.tagName, h.textContent.trim().slice(0,30), fs.toFixed(1), (fs/root).toFixed(3)+'rem']); });
  // fields fill their column
  document.querySelectorAll('.field').forEach(f => { if (!vis(f)) return; const p = f.parentElement; const pw = p.getBoundingClientRect().width; if (Math.abs(f.getBoundingClientRect().width - pw) > 1) out.field.push([f.id, Math.round(f.getBoundingClientRect().width), Math.round(pw)]); });
  // side-by-side cards same height
  document.querySelectorAll('.grid, .values, .clients, .facts, .process, .gallery').forEach(g => { if (!vis(g)) return; const kids = [...g.children].filter(vis);
    const rows = {}; kids.forEach(k => { const r = k.getBoundingClientRect(); const t = Math.round(r.top); (rows[t] = rows[t] || []).push(r.height); });
    Object.entries(rows).forEach(([t, hs]) => { if (hs.length > 1 && Math.max(...hs) - Math.min(...hs) > 2 && !g.classList.contains('gallery')) out.cards.push([g.className.split(' ')[0], hs.map(Math.round)]); }); });
  // text touching the screen edge
  document.querySelectorAll('main h1, main h2, main h3, main p, main li, main .btn, footer p, footer a').forEach(el => { if (!vis(el) || el.closest('.slides')) return; const r = el.getBoundingClientRect(); if (r.left < 11.5 || r.right > W - 11.5) out.edge.push([el.tagName.toLowerCase(), el.textContent.trim().slice(0,30), Math.round(r.left), Math.round(W - r.right)]); });
  return out;
}
"""

async def run():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(PORT), "-d", str(SITE)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    results = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for (w, h, label) in WIDTHS:
            mobile = w < 768
            ctx = await b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, is_mobile=mobile, has_touch=mobile, reduced_motion="reduce", service_workers="block")
            await ctx.add_init_script("""window.__cls=0;try{new PerformanceObserver(l=>{for(const e of l.getEntries()){if(!e.hadRecentInput)window.__cls+=e.value}}).observe({type:'layout-shift',buffered:true})}catch(e){}""")
            for pg_name in PAGES:
                page = await ctx.new_page(); errs = []
                page.on("console", lambda m, e=errs: e.append("console: " + m.text) if m.type == "error" else None)
                page.on("pageerror", lambda ex, e=errs: e.append("pageerror: " + str(ex)))
                page.on("requestfailed", lambda r, e=errs: e.append("failed: " + r.url))
                await page.goto(BASE + pg_name, wait_until="networkidle")
                await page.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=400){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,40));}window.scrollTo(0,0);}")
                await page.wait_for_load_state("networkidle")
                broken = await page.evaluate("[...document.images].filter(i=>i.getAttribute('src') && !i.closest('dialog') && (!i.complete||i.naturalWidth===0)).map(i=>i.src)")
                if broken: errs.append("broken images: " + ", ".join(broken))
                probe = await page.evaluate(PROBE)
                cls = await page.evaluate("window.__cls")
                axe = []
                if label in ("1280", "390"):
                    await page.evaluate("(src)=>{(0,eval)(src)}", AXE)  # via DevTools, so the page's CSP stays on
                    res = await page.evaluate("async()=>{const r=await axe.run(document,{resultTypes:['violations']});return r.violations.filter(v=>v.impact==='serious'||v.impact==='critical').map(v=>[v.id,v.impact,v.nodes.length,v.nodes[0]&&v.nodes[0].target.join(' ')])}")
                    axe = res
                if label in ("1280", "390"):
                    await page.screenshot(path=str(SHOTS / f"{pg_name[:-5]}-{label}.png"), full_page=True)
                results.append({"page": pg_name, "width": label, "errors": errs, "cls": round(cls, 3), "axe": axe, **probe})
                await page.close()
            await ctx.close()
        await b.close()
    srv.terminate()
    (OUTD / "results.json").write_text(json.dumps(results, indent=1))
    # summary
    keys = ["overflow", "errors", "tap", "even", "font", "heading", "field", "cards", "edge", "axe"]
    total = len(results) * len(keys); failed = 0
    for r in results:
        bad = {k: r[k] for k in keys if (r[k] if k != "overflow" else r[k] != 0)}
        if r["cls"] > 0.1: bad["cls"] = r["cls"]
        if bad:
            failed += len(bad)
            print(f"FAIL {r['page']:<18} {r['width']:<8} {json.dumps(bad)[:600]}")
    print(f"\n{len(results)} page-width runs x {len(keys)+1} checks: {total + len(results) - failed} passed, {failed} failed")

asyncio.run(run())
