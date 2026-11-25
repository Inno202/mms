"""Screenshots for review: button groups and both forms at 360px and 1280px.
Full pages at 390px and 1280px are written by tests/e2e.py."""
import asyncio, subprocess, sys, time
from pathlib import Path
from playwright.async_api import async_playwright
ROOT = Path(__file__).resolve().parent.parent
S = ROOT / "tests" / "shots"; S.mkdir(parents=True, exist_ok=True)
async def main():
    srv = subprocess.Popen([sys.executable, "-m", "http.server", "8792", "-d", str(ROOT / "site")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
    base = "http://127.0.0.1:8792/"
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        ctx = await b.new_context(viewport={"width": 360, "height": 780}, is_mobile=True, has_touch=True, reduced_motion="reduce", service_workers="block")
        pg = await ctx.new_page()
        await pg.goto(base + "index.html", wait_until="networkidle")
        await (await pg.query_selector(".hero-panel .even-cols")).screenshot(path=str(S / "group-buttons-360.png"))
        await pg.goto(base + "legal.html", wait_until="networkidle")
        await (await pg.query_selector(".even-row")).screenshot(path=str(S / "group-wrap-360.png"))
        for name, sel in (("contact", "#contact-form"), ("learnerships", "#interest-form")):
            await pg.goto(base + f"{name}.html", wait_until="networkidle")
            await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
            await pg.evaluate(f"document.querySelector('{sel} button[type=submit]').click()"); await pg.wait_for_timeout(300)
            await (await pg.query_selector(sel)).screenshot(path=str(S / f"form-{name}-errors-360.png"))
        await ctx.close()
        pg = await b.new_page(viewport={"width": 1280, "height": 900})
        for name, sel in (("contact", "#contact-form"), ("learnerships", "#interest-form")):
            await pg.goto(base + f"{name}.html", wait_until="networkidle")
            await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
            box = await pg.evaluate(f"(()=>{{const r=document.querySelector('{sel}').closest('section').getBoundingClientRect();return [r.top+scrollY,r.height]}})()")
            await pg.screenshot(path=str(S / f"form-{name}-1280.png"), full_page=True, clip={"x": 0, "y": box[0], "width": 1280, "height": min(box[1], 1400)})
        await b.close()
    srv.terminate()
asyncio.run(main())
