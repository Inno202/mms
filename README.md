# Mbuso Management Solutions — website proposal

A static, multi-page website concept for Mbuso Management Solutions (MMS). It tells the 2026 story (Strategy | Training | Industrialisation) and replaces mbusoms.co.za. Prepared by Poti Thembile, November 2026.

## Open it
Double-click `site/index.html`, or upload the contents of the `site` folder to any web host. You don't need a build step, a database or a server language.

## Pages
Home (photo slideshow with dots and a pause button) · About · Services (with accreditations) · The Hub · Impact (with a photo gallery) · Learnerships (with a register-your-interest form; it is the nav-bar button) · Contact · Legal (privacy, terms, cookies) · 404

## Content still to confirm with MMS
- Years in business: the site says "since 2003" / "more than two decades".
- Hub size: the site lists facilities (30 classrooms, 1 000 beds, 5 workshops, 20 offices) and avoids quoting an area.
- Accreditations: the site uses the 2026 profile table (QCTO and five SETAs) and gives no accreditation number.
- Matric camps: the site says "thousands since 2019".
- Learnerships: the page shows no intake dates or entry requirements. Add them when MMS confirms open programmes.
- Team: only the founder is named. A photo of the founder presenting is on the About page.
- Client names: the site shows them as text only, until MMS confirms it may use logos.
- Photos: they come from MMS's own Instagram posts (February 2026), its old website and its 2026 profile. Replace them with high-resolution originals when available.

## Before going live
1. Remove `<meta name="robots" content="noindex, nofollow">` from every page and delete `robots.txt` (they keep this proposal out of search engines).
2. Have MMS review the legal page.
3. Point the domain at the host and confirm HTTPS works.

## Security check (20 tips)
1 Hide API keys ............ Done: the site uses no keys or secrets.
2 Purge Git secrets ........ Done: there are no secrets in the files. Run a scan when the site is put in a repository.
3 Use public DB key ........ Not applicable: there is no database.
4 Row-level security ....... Not applicable: there is no database.
5 Encrypt sensitive data ... Done: the site stores no personal data. HTTPS is enforced (see 19).
6 Server-side auth ......... Not applicable: there are no accounts or protected pages.
7 Lock record access ....... Not applicable: there are no records.
8 Block field tampering .... Done: the form accepts only the listed enquiry topics, so a tampered value is rejected (tested).
9 Secure session cookies ... Not applicable: the site sets no cookies.
10 Hash passwords .......... Not applicable: there are no passwords.
11 Rate limit login ........ Not applicable: there is no login.
12 Bot protection .......... Done: the form has a hidden honeypot field. It sends nothing to a server, so it can't be spammed through the site.
13 Parameterise queries .... Not applicable: there are no queries.
14 Validate all input ...... Done: both forms check every field for length and format, accept only the listed options, and require consent (tested).
15 Escape user content ..... Done: messages are shown as plain text only, and outside links use rel="noopener noreferrer".
16 Restrict file uploads ... Not applicable: there are no uploads.
17 Trim API responses ...... Not applicable: there is no API.
18 Security headers ........ Done: each page has a CSP meta tag allowing scripts, styles, fonts and images from the site itself only, with no inline code. `.htaccess` (Apache) and `_headers` (Netlify/Cloudflare) add HSTS, CSP with frame-ancestors, nosniff, Referrer-Policy, Permissions-Policy and X-Frame-Options.
19 Force HTTPS ............. Done in `.htaccess` (301 redirect plus HSTS) and with upgrade-insecure-requests. Needs you: turn on HTTPS at the host.
20 Scan dependencies ....... Done: there are no packages or third-party scripts. Fonts are self-hosted under the SIL Open Font License.

Privacy: no analytics, tracking or cookies, and no Google Fonts or Maps embeds. "Get directions" is a plain link.

## Tests run
- Every page at 1280, 390 and 360 px wide: no sideways scrolling, no console errors, all photos load, fonts load.
- Slideshow: dots, pause/play, auto-advance, and no autoplay when the visitor has reduced motion switched on.
- Photo viewer: open, arrow keys, close.
- Mobile menu: open, close, aria-expanded.
- Contact form: required fields, bad formats, tampered topic, consent and honeypot.
- Learnership form: required fields, the optional email is still checked when filled in, consent, and email hand-off.
- Tap targets are at least 44 px on phones.

Neither form can be tested end to end, because it opens the visitor's own email app with the message filled in. To have messages arrive without the email app, connect a form service or a small server script after the proposal is accepted.

## Editing
The pages are generated from `build/build.py` (run `python3 build/build.py`). For small text changes, edit the HTML files directly.
