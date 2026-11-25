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


## Responsive system (25 November 2026)
Shared pieces live in `site/css/site.css`: tokens (colour, fonts, type scale, easing, radius), plus the classes `.btn` (`btn-primary`, `btn-dark`, `btn-outline`, `btn-light`, `btn-outline-light`), `.icon-btn`, `.field`, `.panel`, `.frame`, `.even-row`, `.even-cols`, `.link` and `.num`.

- The root font scales from 14px to 16px with the screen. Text sizes come from one rem scale; touch sizes are in px (buttons and fields at least 48px, icon buttons 44 x 44).
- Every group of buttons uses `.even-cols` (one row of equal columns) or `.even-row` (wraps, and every row fills the width).
- Forms are one column on phones and two from 640px. Long fields span both columns. Fields use 16px text so iPhones don't zoom in. Long text fields show a live counter.
- The phone's back button closes an open menu or photo viewer before it leaves the page.
- Photos have real dimensions, 640 and 1024px versions with `srcset`/`sizes`, and lazy loading below the first screen. Later slideshow photos load only when their turn is near.
- `site/sw.js` keeps an offline copy. It fetches the network first, so a new release shows on the next visit. Bump `VERSION` in it on each release.

Decisions that differ from the Bokamoso rules, and why:
- **Button shape:** buttons use Mbuso's soft rectangle (10px radius), not Bokamoso's pill, so the two colleagues' sites don't look alike. The behaviour (sizes, press effect, even groups) is the same.
- **Page titles on phones:** these start at 2.25rem (text-4xl) instead of text-5xl, because Montserrat is about 35% wider than Bokamoso's serif. At text-5xl, words like "communities" overflowed a 360px phone. From 640px the titles step up to 5xl, then 6xl, then 7xl at 1024px.
- **Hero headline:** the headline in the hero panel reaches 7xl only from 1280px, where the panel is wide enough for "strategies" at that size.
- **Button labels:** they use max(0.95rem, 14px), so they never drop below 14px on small phones.
- **Services page title:** it now reads "What we do" ("Strategy, training and industrialisation" put a 17-letter word in a phone-sized title).
- **Phone menu breakpoint:** the menu switches to the full nav bar at 1100px (previously 1040px), so the six links and the Learnerships button never crowd.

Not applicable on this site: sign-in, checkout, staff dialogs, user roles, React.lazy, chips/filters and passwords. It's a static brochure site with no accounts, so "signed in as each role" could not be tested.

## Build and test
    python3 build/build.py        # regenerates the HTML pages in site/
    python3 tests/e2e.py          # every page at 1280, 768, 390, 360 and 200% zoom: overflow, tap sizes, even groups, font floors, type scale, fields, card heights, edges, CLS, axe
    python3 tests/interact.py     # slideshow, viewer, menu, back button, both forms, spinner, counters, deferred slides
    python3 tests/screenshots.py  # button groups and forms at 360px and 1280px
Needs Python 3, Playwright and Chrome. axe-core is vendored in tests/vendor.
