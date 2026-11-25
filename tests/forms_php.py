"""Real sending: runs the site under PHP with a stand-in mail program and submits
both forms in Chrome, with and without JavaScript. Run: python3 tests/forms_php.py"""
import asyncio, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from playwright.async_api import async_playwright

SITE = Path(__import__("os").environ.get("MBUSO_TEST_SITE") or Path(__file__).resolve().parent.parent / "site")
PORT = 8798
BASE = f"http://127.0.0.1:{PORT}/"
work = Path(tempfile.mkdtemp())
log = work / "mail.log"
stub = work / "sendmail"
stub.write_text(f'#!/bin/sh\necho "ARGS: $*" >> {log}\ncat >> {log}\necho "----END----" >> {log}\n')
stub.chmod(0o755)

res = []
def ok(name, cond, detail=""):
    res.append(("PASS" if cond else "FAIL") + f"  {name} {detail}")

def mails():
    return log.read_text().count("----END----") if log.exists() else 0

async def main():
    shutil.rmtree(Path(tempfile.gettempdir()) / "mbuso-forms", ignore_errors=True)
    srv = subprocess.Popen(["php", "-d", f"sendmail_path={stub}", "-S", f"127.0.0.1:{PORT}", "-t", str(SITE)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(1)
    try:
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page(viewport={"width": 390, "height": 844})
            # contact form, JavaScript on
            await pg.goto(BASE + "contact.html", wait_until="networkidle")
            await pg.fill("#name", "Thandi Mokoena"); await pg.fill("#email", "thandi@example.co.za")
            await pg.fill("#organisation", "Acme Mining"); await pg.fill("#phone", "082 123 4567")
            await pg.select_option("#topic", "Partnerships and CSI")
            await pg.fill("#message", "We would like to discuss a learnership for 40 staff.")
            await pg.check("#consent")
            await pg.wait_for_timeout(3200)            # a person takes longer than 3 seconds
            before = mails()
            await pg.click("#contact-form button[type=submit]")
            await pg.wait_for_selector("#contact-form .form-status.is-ok", timeout=5000)
            st = await pg.text_content("#contact-form .form-status")
            ok("contact form sends by email", mails() == before + 1, st)
            ok("form clears after sending", await pg.input_value("#name") == "" and not await pg.is_checked("#consent"))
            body = log.read_text()
            ok("email has the visitor's details and Reply-To", "Acme Mining" in body and "<thandi@example.co.za>" in body and "To: mail@mbusoms.co.za" in body)
            await pg.screenshot(path="/tmp/mbuso-shots-form-sent.png")
            # learnership form, JavaScript on
            await pg.goto(BASE + "learnerships.html", wait_until="networkidle")
            await pg.fill("#i-name", "Lerato Dlamini"); await pg.fill("#i-phone", "082 765 4321")
            await pg.fill("#i-town", "Klerksdorp"); await pg.select_option("#i-field", "Agriculture")
            await pg.select_option("#i-qual", "Grade 12 (matric)"); await pg.check("#i-consent")
            await pg.wait_for_timeout(3200)
            before = mails()
            await pg.click("#interest-form button[type=submit]")
            await pg.wait_for_selector("#interest-form .form-status.is-ok", timeout=5000)
            ok("learnership form sends by email", mails() == before + 1)
            ok("learnership email subject names the field", "Learnership interest" in __import__("base64").b64decode(
                log.read_text().split("Subject: =?UTF-8?B?")[-1].split("?=")[0]).decode())
            # server-side rejection is shown on the right field (bypass the browser checks)
            await pg.goto(BASE + "contact.html", wait_until="networkidle")
            await pg.wait_for_timeout(3200)
            r = await pg.evaluate("""async()=>{const f=new FormData(document.getElementById('contact-form'));
                f.set('name','A');f.set('email','bad');f.set('topic','Hacked');f.set('message','hello there friend');f.set('consent','yes');
                const x=await fetch('send.php',{method:'POST',body:f,headers:{Accept:'application/json'}});return [x.status, await x.json()]}""")
            ok("server rejects bad email and a tampered topic", r[0] == 422 and set(r[1]["fields"]) == {"email", "topic"}, str(r))
            await b.close()
            # JavaScript off: plain form post, then the thank-you page
            b = await p.chromium.launch()
            ctx = await b.new_context(java_script_enabled=False, reduced_motion="reduce")
            pg = await ctx.new_page()
            await pg.goto(BASE + "contact.html")
            await pg.fill("#name", "No Script"); await pg.fill("#email", "noscript@example.com")
            await pg.select_option("#topic", "Something else"); await pg.fill("#message", "Sent with JavaScript switched off.")
            await pg.check("#consent")
            await pg.wait_for_timeout(100)
            before = mails()
            await pg.click("#contact-form button[type=submit]")
            await pg.wait_for_load_state("load")
            # t is empty without JavaScript, so the timing check is skipped server-side
            ok("without JavaScript the form still sends and shows the thank-you page",
               "thanks.html" in pg.url and mails() == before + 1, pg.url)
            await b.close()
    finally:
        srv.terminate()
    print("\n".join(res))
    fails = sum(r.startswith("FAIL") for r in res)
    print(f"\n{len(res) - fails}/{len(res)} passed")
    sys.exit(1 if fails else 0)

asyncio.run(main())
