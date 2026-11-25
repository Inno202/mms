import asyncio, sys, json, subprocess, time
from playwright.async_api import async_playwright
BASE="http://127.0.0.1:8765/"
PAGES=["index.html","about.html","services.html","hub.html","impact.html","learnerships.html","contact.html","legal.html","404.html"]
WIDTHS=[1280,390,360]
async def main():
    srv=subprocess.Popen([sys.executable,"-m","http.server","8765","-d","/home/claude/site"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(1)
    report=[]
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for w in WIDTHS:
            ctx=await b.new_context(viewport={"width":w,"height":900 if w>500 else 800}, device_scale_factor=1, reduced_motion="reduce")
            for pg in PAGES:
                page=await ctx.new_page(); errs=[]
                page.on("console", lambda m, e=errs: e.append(m.text) if m.type in ("error","warning") else None)
                page.on("pageerror", lambda ex, e=errs: e.append("PAGEERROR "+str(ex)))
                page.on("requestfailed", lambda r, e=errs: e.append("FAILED "+r.url))
                await page.goto(BASE+pg, wait_until="networkidle")
                await page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
                await page.evaluate("async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,60));}window.scrollTo(0,0);}")
                await page.wait_for_load_state("networkidle")
                broken=await page.evaluate("[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
                if broken: errs.append("BROKEN IMG "+str(broken))
                await page.wait_for_timeout(300)
                sw=await page.evaluate("[document.documentElement.scrollWidth, document.documentElement.clientWidth]")
                over=await page.evaluate("""(()=>{const W=document.documentElement.clientWidth;return [...document.querySelectorAll('body *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.right>W+1)&&getComputedStyle(e).position!=='fixed'&&!e.closest('dialog')}).slice(0,5).map(e=>e.tagName+'.'+e.className+' '+Math.round(e.getBoundingClientRect().right))})()""")
                fonts=await page.evaluate("document.fonts.check('600 20px \"Source Serif 4\"') && document.fonts.check('400 16px \"Source Sans 3\"')")
                report.append({"w":w,"page":pg,"scroll":sw,"overflow":over,"fonts":fonts,"errs":errs})
                await page.screenshot(path=f"/home/claude/test/shots/{pg[:-5]}-{w}.png", full_page=True)
                await page.close()
            await ctx.close()
        await b.close()
    srv.terminate()
    for r in report: print(json.dumps(r))
asyncio.run(main())
