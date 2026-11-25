"""Builds the static Mbuso Management Solutions proposal site into ../site.
Shared header, footer and icons live here so every page stays consistent."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent.parent / "site"

# Lucide-style icons: one family, 2px stroke.
P = {
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "pause": '<rect x="6" y="4" width="4" height="16" rx="1"/><rect x="14" y="4" width="4" height="16" rx="1"/>',
    "play": '<path d="M7 4v16l13-8z"/>',
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "box": '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="m3 8 9 5 9-5"/><path d="M12 13v8"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "left": '<path d="m15 18-6-6 6-6"/>',
    "right": '<path d="m9 18 6-6-6-6"/>',
    "expand": '<path d="M15 3h6v6"/><path d="M9 21H3v-6"/><path d="M21 3l-7 7"/><path d="M3 21l7-7"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "instagram": '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/>',
    "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"/><path d="M21 3v5h-5"/>',
    "cap": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    "badge": '<circle cx="12" cy="8" r="6"/><path d="M8.2 13.4 7 22l5-3 5 3-1.2-8.6"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
    "sprout": '<path d="M7 20h10"/><path d="M12 20v-9"/><path d="M12 11c0-4 3-6 7-6 0 4-3 6-7 6z"/><path d="M12 13c0-3-2-5-6-5 0 3 2 5 6 5z"/>',
    "external": '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
}
def ic(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{P[name]}</svg>'

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("hub.html", "The Hub"), ("impact.html", "Impact"), ("contact.html", "Contact")]

PHONE_DISPLAY, PHONE_TEL = "086 102 2020", "+27861022020"
EMAIL = "mail@mbusoms.co.za"
FB = "https://www.facebook.com/dkstrategist/"
IG = "https://www.instagram.com/mbusomanagementsolutions/"

def head(title, desc, page):
    full = title if page == "index.html" else f"{title} | Mbuso Management Solutions"
    return f"""<!doctype html>
<html lang="en-ZA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self' mailto:; upgrade-insecure-requests">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="robots" content="noindex, nofollow">
<title>{escape(full)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:title" content="{escape(full)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="img/it-4.webp">
<link rel="icon" href="img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<link rel="preload" href="fonts/montserrat-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.css">
<script src="js/site.js" defer></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
"""

def header(page):
    links = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}</a></li>' for h, t in NAV)
    mlinks = "".join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == page else ""}>{t}{ic("right")}</a></li>' for h, t in NAV + [("learnerships.html", "Learnerships")])
    return f"""<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="Mbuso Management Solutions home"><img src="img/logo-360.png" width="180" height="105" alt="Mbuso Management Solutions"></a>
    <nav class="nav" aria-label="Main"><ul>{links}</ul></nav>
    <a class="btn btn-dark header-cta" href="learnerships.html"{" aria-current=\"page\"" if page == "learnerships.html" else ""}>Learnerships {ic("arrow", "btn-arrow")}</a>
    <button class="icon-btn menu-btn" type="button" data-menu-open aria-haspopup="dialog" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu">{ic("menu")}</button>
  </div>
</header>
<dialog class="mobile-menu" id="mobile-menu" aria-label="Menu">
  <div class="wrap mobile-menu-inner">
    <div class="mobile-menu-top">
      <a class="brand" href="index.html" aria-label="Mbuso Management Solutions home"><img src="img/logo-360.png" width="180" height="105" alt="Mbuso Management Solutions"></a>
      <button class="icon-btn menu-btn" type="button" data-menu-close aria-label="Close menu">{ic("x")}</button>
    </div>
    <nav aria-label="Mobile"><ul>{mlinks}</ul></nav>
    <div class="mobile-menu-foot">
      <a class="plain" href="tel:{PHONE_TEL}">{ic("phone")}<span class="num">{PHONE_DISPLAY}</span></a>
      <a class="plain" href="mailto:{EMAIL}">{ic("mail")}{EMAIL}</a>
    </div>
  </div>
</dialog>
<main id="main">
"""

def footer():
    return f"""</main>
<footer class="site-footer on-dark">
  <div class="wrap footer-top">
    <div class="footer-brand">
      <img src="img/logo-white-360.png" width="180" height="105" alt="Mbuso Management Solutions">
      <p>We facilitate sustainable growth by delivering industrialisation solutions that integrate human development, economic empowerment and innovative technologies.</p>
      <div class="social">
        <a href="{FB}" target="_blank" rel="noopener noreferrer" aria-label="Facebook (opens in a new tab)">{ic("facebook")}</a>
        <a href="{IG}" target="_blank" rel="noopener noreferrer" aria-label="Instagram (opens in a new tab)">{ic("instagram")}</a>
      </div>
    </div>
    <div>
      <h2>Explore</h2>
      <ul>
        <li><a href="about.html">About us</a></li>
        <li><a href="services.html">Services</a></li>
        <li><a href="services.html#accreditations">Accreditations</a></li>
        <li><a href="hub.html">Itireleng Hub</a></li>
        <li><a href="impact.html">Impact and CSI</a></li>
        <li><a href="learnerships.html">Learnerships</a></li>
      </ul>
    </div>
    <div>
      <h2>Services</h2>
      <ul>
        <li><a href="services.html#training">Training and development</a></li>
        <li><a href="services.html#industrial">Industrial operations</a></li>
        <li><a href="services.html#consulting">Strategy and consulting</a></li>
      </ul>
    </div>
    <div>
      <h2>Contact</h2>
      <ul>
        <li><a href="tel:{PHONE_TEL}" class="num">{PHONE_DISPLAY}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><span>Tijger Valley Office Park #15,<br>7 Pony Street, Silverlakes,<br>Pretoria East, <span class="num">0084</span></span></li>
      </ul>
    </div>
  </div>
  <div class="wrap footer-bottom">
    <p>&copy; <span class="num" data-year>2026</span> Mbuso Management Solutions (Pty) Ltd. Reg. no. <span class="num">2012/074900/07</span>.</p>
    <ul>
      <li><a href="legal.html#privacy">Privacy</a></li>
      <li><a href="legal.html#terms">Terms</a></li>
      <li><a href="legal.html#cookies">Cookies</a></li>
    </ul>
  </div>
</footer>
<div class="toast-region" aria-live="polite"></div>
<dialog class="photo-viewer" id="photo-viewer" aria-label="Photo viewer">
  <div class="viewer-top"><span class="viewer-count num"></span><button class="viewer-btn viewer-close" type="button" aria-label="Close photo">{ic("x")}</button></div>
  <div class="viewer-stage"><img alt=""></div>
  <button class="viewer-btn viewer-prev" type="button" aria-label="Previous photo">{ic("left")}</button>
  <button class="viewer-btn viewer-next" type="button" aria-label="Next photo">{ic("right")}</button>
  <p class="viewer-caption"></p>
</dialog>
</body>
</html>
"""

def page_hero(img, alt, crumb, title_html):
    return f"""<section class="page-banner">
  <div class="wrap">
    <div class="banner">
      <img src="img/{img}" alt="{escape(alt)}" fetchpriority="high">
      <div class="banner-content hero-rise">
        <ol class="crumbs"><li><a href="index.html">Home</a></li><li><span aria-current="page">{crumb}</span></li></ol>
        <h1 class="display h1">{title_html}</h1>
      </div>
    </div>
  </div>
</section>
"""

def cta(title_html, text):
    return f"""<div class="wrap cta-shell">
  <section class="cta on-dark reveal">
    <div>
      <h2 class="display h2">{title_html}</h2>
      <p>{text}</p>
    </div>
    <div class="even-cols fit-md">
      <a class="btn btn-light" href="contact.html">Start a conversation {ic("arrow", "btn-arrow")}</a>
      <a class="btn btn-outline-light" href="tel:{PHONE_TEL}" aria-label="Call {PHONE_DISPLAY}"><span class="num">{PHONE_DISPLAY}</span></a>
    </div>
  </section>
</div>
"""

def ticks(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{ic('check')}<span>{i}</span></li>" for i in items) + "</ul>"

import re as _re
def strip_accents(html):
    # Headings stay one colour; maroon is kept for accents, not words in titles.
    prev = None
    while prev != html:
        prev = html
        html = _re.sub(r'<span class="accent">((?:(?!<span class="accent">).)*?)</span>', r'\1', html, flags=_re.S)
    return html


# ---- Responsive images: every photo gets real dimensions, srcset and sizes
from PIL import Image as _PILImage
_IMG_DIR = OUT / "img"
def _dims(name):
    with _PILImage.open(_IMG_DIR / name) as im:
        return im.size
def _variants(name):
    stem = name[:-5]
    out = []
    for t in (640, 1024):
        if (_IMG_DIR / f"{stem}-{t}.webp").exists():
            out.append((f"img/{stem}-{t}.webp", t))
    w, _ = _dims(name)
    out.append((f"img/{name}", w))
    return out
def _sizes_for(context):
    if 'class="slide' in context or 'class="banner' in context:
        return "100vw"
    if 'class="zoomable' in context:
        return "(min-width: 1024px) 25vw, 50vw"
    if 'class="pillar' in context:
        return "(min-width: 1024px) 400px, (min-width: 640px) 50vw, 100vw"
    return "(min-width: 1024px) 600px, 100vw"
_IMG_RE = _re.compile(r'<img\b([^>]*?)\bsrc="img/([a-z0-9-]+\.webp)"([^>]*)>')
def responsive_images(html):
    def fix(m):
        before, name, after = m.group(1), m.group(2), m.group(3)
        attrs = before + after
        attrs = _re.sub(r'\s(width|height|srcset|sizes)="[^"]*"', "", attrs)
        w, h = _dims(name)
        ctx = html[max(0, m.start() - 260):m.start()]
        srcset = ", ".join(f"{u} {wd}w" for u, wd in _variants(name))
        lazy_slide = 'data-defer' in attrs
        attrs = attrs.replace(" data-defer", "")
        if lazy_slide:
            return f'<img data-src="img/{name}" data-srcset="{srcset}" sizes="{_sizes_for(ctx)}" width="{w}" height="{h}"{attrs}>'
        return f'<img src="img/{name}" srcset="{srcset}" sizes="{_sizes_for(ctx)}" width="{w}" height="{h}"{attrs}>'
    return _IMG_RE.sub(fix, html)

def write(name, title, desc, body):
    body = responsive_images(strip_accents(body))
    html = head(title, desc, name) + header(name) + body + footer()
    (OUT / name).write_text(html, encoding="utf-8")
    print("wrote", name, len(html))

# ------------------------------------------------------------------ HOME
SLIDES = [
    ("it-4.webp", "Learners at computers during a database management training session",
     "Database management training for the North West Department of Public Works and Roads"),
    ("ohs-18.webp", "A large group of delegates in an occupational health and safety class",
     "Occupational health and safety training"),
    ("matric-camp.webp", "Grade 12 learners in school uniform seated in a hall during a matric camp",
     "Grade 12 matric incubation camp, Dr Kenneth Kaunda District"),
    ("workshop-tables.webp", "Delegates seated at conference tables during a facilitated workshop",
     "Facilitated workshop session"),
    ("ohs-22.webp", "A learner practising CPR on a training mannequin while a facilitator watches",
     "CPR training, part of occupational health and safety training"),
]
slides_html = "".join(
    f'<li class="slide{" is-active" if i == 0 else ""}" data-caption="{escape(c)}" aria-hidden="{"false" if i == 0 else "true"}">'
    f'<img src="img/{s}" alt="{escape(a)}" {"fetchpriority=\"high\"" if i == 0 else ("loading=\"lazy\"" if i == 1 else "data-defer")}></li>'
    for i, (s, a, c) in enumerate(SLIDES))
dots_html = "".join(
    f'<button class="dot" type="button" aria-label="Show photo {i+1} of {len(SLIDES)}" aria-current="{"true" if i == 0 else "false"}"></button>'
    for i in range(len(SLIDES)))

home = f"""<section class="hero" data-slideshow aria-roledescription="carousel" aria-label="Mbuso Management Solutions at work">
  <ul class="slides">{slides_html}</ul>
  <div class="wrap hero-inner">
    <div class="hero-panel on-dark">
      <div class="hero-rise">
        <span class="hero-motto">Strategy | Training | Industrialisation</span>
        <h1 class="display hero-title"><span class="light">We develop</span> people, strategies and industries</h1>
        <p class="hero-text">Since <span class="num">2003</span>, government, state-owned enterprises, mining houses and listed companies have trusted us to plan for growth, build scarce skills and turn that training into real production.</p>
        <div class="even-cols fit-md">
          <a class="btn btn-light" href="services.html">Explore our services {ic("arrow", "btn-arrow")}</a>
          <a class="btn btn-outline-light" href="hub.html">Visit the Hub</a>
        </div>
      </div>
    </div>
    <div class="hero-foot">
      <p class="slide-caption" aria-live="polite">{escape(SLIDES[0][2])}</p>
      <div class="slide-rail">
        <div class="dots" role="group" aria-label="Choose a photo">{dots_html}</div>
        <button class="icon-btn pause-btn" type="button" aria-label="Pause slideshow">{ic("pause", "i-pause")}{ic("play", "i-play").replace("<svg", "<svg hidden")}</button>
      </div>
    </div>
  </div>
</section>
<section class="trust section-tight" aria-label="At a glance">
  <div class="wrap"><div class="trust-grid">
    <div class="trust-item"><strong>2003</strong><span>Founded, more than two decades of practice</span></div>
    <div class="trust-item"><strong>6</strong><span>Accrediting bodies: QCTO and five SETAs</span></div>
    <div class="trust-item"><strong>25</strong><span>Government, mining and corporate clients listed</span></div>
    <div class="trust-item"><strong>1&nbsp;000</strong><span>People the Itireleng Hub can accommodate</span></div>
  </div></div>
</section>

<section class="section">
  <div class="wrap split split-wide-left">
    <div class="reveal">
      <span class="eyebrow">Who we are</span>
      <p class="statement">A one-stop partner for <strong>holistic development</strong>: we plan the strategy, train the people and run the production lines they work on.</p>
    </div>
    <div class="reveal">
      <p class="lead">Mbuso Management Solutions is a black-owned strategy, training and industrialisation firm. Our head office is in Pretoria and our operations are anchored in Matlosana, North West, at our own learning and manufacturing hub.</p>
      <p class="muted">We call it a closed loop. Learners gain accredited skills, then move straight into industrial work at the Hub, which keeps delivery steady even when markets are not.</p>
      <a class="text-link" href="about.html">Read our story {ic("arrow")}</a>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Three pillars, <span class="accent">one</span> partner</h2>
      <p>Each pillar works on its own. Together they take a client from plan to skilled people to working production.</p>
    </div>
    <div class="grid grid-3">
      <a class="pillar group reveal" href="services.html#training">
        <div class="frame"><img class="photo-zoom" src="img/it-3.webp" alt="Learners working at computers in a training room" loading="lazy" width="1440" height="581"></div>
        <div class="pillar-body">
          <span class="pillar-label">Pillar one</span><h3 class="display h3">Training and development</h3>
          <p>Accredited skills programmes, learnerships, artisan training, Recognition of Prior Learning, leadership and entrepreneurship.</p>
          <span class="text-link">Training {ic("arrow")}</span>
        </div>
      </a>
      <a class="pillar group reveal" href="services.html#industrial">
        <div class="frame"><img class="photo-zoom" src="img/textile-hub.webp" alt="Women of the Itireleng Textile Hub standing in front of the factory" loading="lazy" width="445" height="334"></div>
        <div class="pillar-body">
          <span class="pillar-label">Pillar two</span><h3 class="display h3">Industrial operations</h3>
          <p>Textile production at the Itireleng Textile Hub, an industrial bakery, and woodworking and casket manufacturing.</p>
          <span class="text-link">Industrial operations {ic("arrow")}</span>
        </div>
      </a>
      <a class="pillar group reveal" href="services.html#consulting">
        <div class="frame"><img class="photo-zoom" src="img/workshop-room.webp" alt="A facilitator leading a strategy session in a conference room" loading="lazy" width="1280" height="960"></div>
        <div class="pillar-body">
          <span class="pillar-label">Pillar three</span><h3 class="display h3">Strategy and consulting</h3>
          <p>Strategy design and implementation, organisational development, culture audits, skills audits and job evaluation.</p>
          <span class="text-link">Strategy and consulting {ic("arrow")}</span>
        </div>
      </a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split-wide-right">
    <div class="deco reveal"><div class="frame frame-accent ratio-16x9"><img src="img/hub-model.webp" alt="3D model of the Itireleng Learning and Manufacturing Hub showing its buildings and grounds" loading="lazy" width="1037" height="574"></div></div>
    <div class="reveal">
      <span class="eyebrow">Itireleng Learning and Manufacturing Hub</span>
      <h2 class="display h2">A former mine site, now a place to live, learn and <span class="accent">work</span></h2>
      <p class="lead mt-1">In Umuzimuhle, Orkney, we turned a derelict mining property into a skills, engineering and manufacturing campus.</p>
      <div class="facts mt-2">
        <div class="panel fact"><span class="fact-value">30</span><span class="fact-label">Classrooms</span></div>
        <div class="panel fact"><span class="fact-value">1&nbsp;000</span><span class="fact-label">People the Hub can accommodate</span></div>
        <div class="panel fact"><span class="fact-value">5</span><span class="fact-label">Industrial workshops</span></div>
        <div class="panel fact"><span class="fact-value">20</span><span class="fact-label">Offices</span></div>
      </div>
      <a class="btn btn-primary mt-2" href="hub.html">See the Hub {ic("arrow", "btn-arrow")}</a>
    </div>
  </div>
</section>

<section class="section band-dark on-dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Our method</span><h2 class="display h2">No intervention without diagnosis</h2></div>
      <p>Motivation alone does not change an organisation. We measure first, then give people the tools to do the job, then stay to make sure it holds.</p>
    </div>
    <ol class="process reveal">
      <li><span class="p-icon">{ic("search")}</span><span class="stage">Before</span><h3 class="display h3">Diagnose</h3><p>Organisational health tests, leadership and culture assessments, pre-training assessments, focus groups and interviews.</p></li>
      <li><span class="p-icon">{ic("users")}</span><span class="stage">During</span><h3 class="display h3">Intervene</h3><p>Facilitation, business simulations, role plays and case studies, formative assessments and personal development plans.</p></li>
      <li><span class="p-icon">{ic("refresh")}</span><span class="stage">After</span><h3 class="display h3">Sustain</h3><p>Ongoing coaching, a site visit a month later, follow-up workshops and support through implementation.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Results we can <span class="accent">point to</span></h2>
      <a class="text-link" href="impact.html">All impact stories {ic("arrow")}</a>
    </div>
    <div class="facts facts-4 reveal">
      <div class="panel fact"><span class="fact-value">100</span><span class="fact-label">Women and youth signed up to the Itireleng Textile Hub</span></div>
      <div class="panel fact"><span class="fact-value">150</span><span class="fact-label">Learners from five municipalities in a SALGA water learnership</span></div>
      <div class="panel fact"><span class="fact-value">60</span><span class="fact-label">Township learners supported from Grade 9 to matric</span></div>
      <div class="panel fact"><span class="fact-value">2019</span><span class="fact-label">First Grade 12 matric camps hosted at the Hub</span></div>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Trusted by those who build <span class="accent">South Africa</span></h2>
      <p>A selection of the government, mining, finance and development partners we have worked with.</p>
    </div>
    <div class="clients reveal">
      <div class="panel client-group"><h3>Mining and energy</h3><ul><li>Anglo American PLC</li><li>Harmony Gold</li><li>Gold Fields</li><li>Kopanang Gold Mine</li></ul></div>
      <div class="panel client-group"><h3>Government and agencies</h3><ul><li>SALGA</li><li>National Youth Development Agency</li><li>National Skills Fund</li><li>Department of Mineral and Petroleum Resources</li></ul></div>
      <div class="panel client-group"><h3>Business and foundations</h3><ul><li>Standard Bank</li><li>Nelson Mandela Foundation</li><li>Cyril Ramaphosa Foundation</li><li>Gauteng Gambling Board</li></ul></div>
    </div>
    <p class="mt-2"><a class="text-link" href="about.html#clients">See all clients {ic("arrow")}</a></p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Accredited delivery</span>
      <h2 class="display h2">Qualifications backed by the <span class="accent">QCTO</span> and five SETAs</h2>
    </div>
    <div class="reveal">
      <p class="lead">Our programmes are accredited with the QCTO, EW SETA, AgriSETA, FP&amp;M SETA, MICT SETA and Services SETA, from artisan plumbing and cable jointing to clothing manufacturing and New Venture Creation.</p>
      <a class="text-link" href="services.html#accreditations">View accredited qualifications {ic("arrow")}</a>
    </div>
  </div>
</section>

{cta('Ready to plan your next <span class="accent">phase of growth</span>?', 'Tell us about your organisation, your people or your project. We will set up a first conversation with our team.')}
"""
write("index.html", "Mbuso Management Solutions | Strategy, Training and Industrialisation",
      "Mbuso Management Solutions is a black-owned strategy, training and industrialisation firm with a learning and manufacturing hub in Matlosana, North West.", home)

# ------------------------------------------------------------------ ABOUT
VALUES = [("Faith", "We trust and believe that our business is on purpose and is divinely guided and protected."),
          ("Integrity", "All we do is above board and rooted in self-respect."),
          ("Innovation", "We stay at the front of change and take our markets to new ways of thinking."),
          ("Excellence", "We deliver the highest quality and real value for money."),
          ("Respect", "We show care, consideration and kindness in every interaction."),
          ("Partnerships", "We draw on the strengths of others for a shared competitive edge.")]
values_html = "".join(f'<div class="panel value"><h3 class="display h3">{t}</h3><p>{d}</p></div>' for t, d in VALUES)

CLIENTS = [
    ("Mining and energy", ["Anglo American PLC", "Harmony Gold", "Gold Fields", "Kopanang Gold Mine", "Intasol Tailings", "Cox Energy"]),
    ("National and provincial government", ["Department of Mineral and Petroleum Resources", "Department of Agriculture, Land Reform and Rural Development", "North West Department of Public Works and Roads", "Gauteng Gambling Board"]),
    ("Local government", ["South African Local Government Association", "Chris Hani District Municipality", "Matlosana Local Municipality"]),
    ("Development and funding", ["National Youth Development Agency", "National Skills Fund", "Small Enterprise Development and Finance Agency", "National Research Foundation", "Local Government SETA", "Energy and Water SETA"]),
    ("Foundations and education", ["Nelson Mandela Foundation", "Cyril Ramaphosa Foundation", "Ikalafeng Special School"]),
    ("Business", ["Standard Bank", "MXN Development", "South African National Taxi Council (Gauteng)"]),
]
clients_html = "".join(f'<div class="panel client-group"><h3>{g}</h3><ul>' + "".join(f"<li>{c}</li>" for c in cs) + "</ul></div>" for g, cs in CLIENTS)

about = page_hero("workshop-tables.webp", "Delegates at a facilitated workshop", "About us", '<span class="light">Built on more than</span> two decades of practice') + f"""
<section class="section">
  <div class="wrap split split-wide-left">
    <div class="reveal">
      <span class="eyebrow">Our story</span>
      <h2 class="display h2">From motivation and training to <span class="accent">industrialisation</span></h2>
    </div>
    <div class="reveal">
      <p class="lead">Daddy Khuselo founded Mbuso Management Solutions in January <span class="num">2003</span> as a motivation, training and consulting company. Two decades later it is a strategic partner to government, state-owned enterprises, listed companies and communities.</p>
      <p>Along the way we learned that motivation on its own does not change results. People need practical, accredited skills, and they need somewhere to use them. That is why we established the Itireleng Learning and Manufacturing Hub, where certified talent moves directly into our own industrial production lines.</p>
      <p>Our head office is in Pretoria, Gauteng. Our operations are anchored in Matlosana, Dr Kenneth Kaunda District, North West. We are a Premium Client of the Small Enterprise Development Agency, and the Industrial Development Corporation supports the equipping of the factories we run.</p>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap grid grid-2">
    <div class="panel panel-lg panel-fill reveal">
      <span class="eyebrow">Mission</span>
      <p class="statement">We facilitate sustainable growth by delivering industrialisation solutions that integrate human development, economic empowerment and innovative <span class="accent">technologies</span>.</p>
    </div>
    <div class="panel panel-lg panel-fill reveal">
      <span class="eyebrow">Vision</span>
      <p class="statement">A global authority on holistic <span class="accent">development</span>.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display h2">The values we <span class="accent">work by</span></h2></div>
    <div class="values reveal">{values_html}</div>
  </div>
</section>

<section class="section band">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Our model</span>
      <h2 class="display h2">Holistic development, from personal mastery to <span class="accent">enterprise</span></h2>
      <p class="lead mt-1">Our development model starts with the person. Personal mastery is the foundation, technical skills make people employable, and business skills grow leaders and entrepreneurs. Spiritual enrichment anchors it all.</p>
      <p class="muted">In strategy work we balance the technical side of planning with the human side of change, so people are not left behind as organisations evolve. Then we stay to help clients implement.</p>
    </div>
    <div class="deco deco-alt reveal"><div class="frame ratio-4x3"><img src="img/ohs-20.webp" alt="A facilitator presenting to a class beside a whiteboard" loading="lazy" width="1078" height="680"></div></div>
  </div>
</section>

<section class="section" id="founder">
  <div class="wrap split split-wide-right">
    <div class="deco reveal"><div class="frame frame-accent ratio-4x5"><img src="img/daddy-khuselo.webp" alt="Daddy Khuselo, founder and CEO of Mbuso Management Solutions, presenting at a workshop" loading="lazy" width="637" height="796"></div></div>
    <div class="reveal">
      <span class="eyebrow">Founder and CEO</span>
      <h2 class="display h2">Daddy <span class="accent">Khuselo</span></h2>
      <p class="lead mt-1">Business strategist, published author, organisational development practitioner, training expert and industrialist.</p>
      <p>DK began as an electrical engineer and has spent his career connecting human capital development with sustainable economic projects, so that growth is inclusive and people are not left behind. He has advised the Nelson Mandela Foundation, Anglo American, Gold Fields, the National Youth Development Agency, the Gauteng Gambling Board and SALGA.</p>
      {ticks(["National Diploma in Electrical Engineering, Tshwane University of Technology", "Programme in Business Administration, University of Johannesburg", "Advanced Programme in Organisational Development, UNISA", "Mastering Strategy Programme, Gordon Institute of Business Science", "Author of The Rivonia Junction (2017), a guide to turning a passion into a thriving career and business", "Former ministerial appointee to the council of Johannesburg Central College (2014 to 2019)"])}
    </div>
  </div>
</section>

<section class="section band" id="clients">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Clients we have <span class="accent">served</span></h2>
      <p>Strategy, training and development work across the public and private sectors.</p>
    </div>
    <div class="clients reveal">{clients_html}</div>
  </div>
</section>

{cta('Work with a partner who stays through <span class="accent">implementation</span>', 'From a single workshop to a multi-year development programme, we start by understanding your organisation.')}
"""
write("about.html", "About us", "The story, mission, values and founder of Mbuso Management Solutions, and the clients it has served since 2003.", about)

# ------------------------------------------------------------------ SERVICES
ACC = [("QCTO", ["Occupational Certificate: Plumbing Hand (Artisan)", "Plumbing Hand (Assistant Plumber)", "Energy Efficiency", "Solar Hot Water Installation", "Occupational Health and Safety"]),
       ("EW SETA", ["Hot Water Systems and Installation", "Water and Wastewater Treatment Operations Processes", "Water and Wastewater Reticulation Services", "Cable Jointing", "Basic Electrician"]),
       ("AgriSETA", ["Animal Production", "Plant Production", "Poultry Production", "Horticulture"]),
       ("FP&amp;M SETA", ["Clothing, Textile, Footwear and Leather Manufacturing", "Furniture Making"]),
       ("MICT SETA", ["End User Computing", "Systems Development", "Technical Support"]),
       ("Services SETA", ["New Venture Creation"])]
acc_rows = "".join(f'<tr><th scope="row">{b}</th><td><ul>' + "".join(f"<li>{q}</li>" for q in qs) + "</ul></td></tr>" for b, qs in ACC)

services = page_hero("it-0.webp", "A learner working at a computer during training", "Services", '<span class="light">What we</span> do') + f"""
<section class="section">
  <div class="wrap">
    <p class="statement reveal">Three pillars that work alone or together, so one partner can take you <strong>from plan, to skilled people, to production</strong>.</p>
  </div>
</section>

<section class="section band" id="training">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Pillar one</span>
      <h2 class="display h2">Training and <span class="accent">development</span></h2>
      <p class="lead mt-1">We focus on critical and scarce skills that the mainstream education system does not offer but the economy needs, so learners can earn and employees can grow.</p>
      {ticks(["Accredited skills programmes", "Learnerships and artisan training", "Recognition of Prior Learning", "Work-integrated learning, reskilling and upskilling", "Leadership development", "Entrepreneurial training", "Student and graduate development workshops"], "ticks ticks-2")}
    </div>
    <div class="grid grid-2 reveal">
      <div class="frame ratio-4x5"><img src="img/ohs-13.webp" alt="A learner practising chest compressions on a CPR mannequin" loading="lazy" width="1078" height="680"></div>
      <div class="frame ratio-4x5"><img src="img/it-7.webp" alt="A learner concentrating during a computer course" loading="lazy" width="1440" height="581"></div>
    </div>
  </div>
</section>

<section class="section" id="industrial">
  <div class="wrap split split-wide-right">
    <div class="deco reveal"><div class="frame ratio-4x3"><img src="img/textile-hub.webp" alt="Members of the Itireleng Textile Hub outside the factory" loading="lazy" width="445" height="334"></div></div>
    <div class="reveal">
      <span class="eyebrow">Pillar two</span>
      <h2 class="display h2">Industrial <span class="accent">operations</span></h2>
      <p class="lead mt-1">At the Itireleng Hub, training leads straight to production. Our ventures give learners practical exposure and a path to employment.</p>
      {ticks(["Textile and clothing production at the Itireleng Textile Hub", "Industrial bakery operations", "Woodworking and casket manufacturing", "Incubation and mentorship for SMMEs and cooperatives"])}
      <a class="text-link mt-2" href="hub.html">Inside the Hub {ic("arrow")}</a>
    </div>
  </div>
</section>

<section class="section band" id="consulting">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Pillar three</span>
      <h2 class="display h2">Strategy and <span class="accent">consulting</span></h2>
      <p class="lead mt-1">Listed entities and established brands trust us with their medium to long-term strategies and the change management that makes them happen.</p>
      {ticks(["Business model analysis and development", "Strategy design and implementation", "Strategic planning facilitation", "Organisational development and structure design", "Culture audits and skills audits", "Job evaluation", "Leadership coaching and mentorship", "Project and facility management"], "ticks ticks-2")}
    </div>
    <div class="deco deco-alt reveal"><div class="frame ratio-4x3"><img src="img/conference.webp" alt="Delegates listening during a conference session" loading="lazy" width="960" height="640"></div></div>
  </div>
</section>

<section class="section" id="accreditations">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Accredited <span class="accent">qualifications</span></h2>
      <p>Programmes we are accredited to deliver, by certifying body.</p>
    </div>
    <div class="table-wrap reveal">
      <table class="acc">
        <thead><tr><th scope="col">Body</th><th scope="col">Qualifications</th></tr></thead>
        <tbody>{acc_rows}</tbody>
      </table>
    </div>
  </div>
</section>

{cta('Need a programme built around <span class="accent">your people</span>?', 'We can combine accredited training, practical work at the Hub and strategy support into one plan.')}
"""
write("services.html", "Services", "Training and development, industrial operations, and strategy and consulting from Mbuso Management Solutions, with QCTO and SETA accredited qualifications.", services)

# ------------------------------------------------------------------ HUB
hub = page_hero("hub-model.webp", "3D model of the Itireleng Hub", "Itireleng Learning and Manufacturing Hub", '<span class="light">Where learning</span> becomes work') + f"""
<section class="section">
  <div class="wrap split split-wide-left">
    <div class="reveal">
      <span class="eyebrow">Umuzimuhle, Orkney</span>
      <h2 class="display h2">A mining property, given a second <span class="accent">life</span></h2>
    </div>
    <div class="reveal">
      <p class="lead">When mining closures threatened Matlosana, Daddy Khuselo saw an opportunity in a derelict former mine site. Mbuso Management Solutions secured it from a mining house and turned its training rooms, accommodation and workshops into a learning, innovation and manufacturing hub.</p>
      <p>Today the Hub gives learners theory, practical exposure and possible employment in one place, through our in-house engineering and manufacturing facilities.</p>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <div class="facts facts-4 reveal">
      <div class="panel fact"><span class="fact-value">30</span><span class="fact-label">Classrooms</span></div>
      <div class="panel fact"><span class="fact-value">1&nbsp;000</span><span class="fact-label">People the Hub can accommodate</span></div>
      <div class="panel fact"><span class="fact-value">5</span><span class="fact-label">Industrial workshops</span></div>
      <div class="panel fact"><span class="fact-value">2</span><span class="fact-label">Halls, plus kitchen and recreation facilities</span></div>
    </div>
    <p class="caption">The Hub also has an office block with 20 offices and a retail park, and sits close to a clinic.</p>
  </div>
</section>

<section class="section band">
  <div class="wrap split split-wide-right">
    <div class="deco reveal"><div class="frame ratio-4x3"><img src="img/textile-hub.webp" alt="The Itireleng Textile Hub class of 2020 outside the factory" loading="lazy" width="445" height="334"></div></div>
    <div class="reveal">
      <span class="eyebrow">Itireleng Textile Hub</span>
      <h2 class="display h2">A <span class="num">2&nbsp;000</span> m² factory built for <span class="accent">quality</span></h2>
      <p class="lead mt-1">The Textile Hub manufactures clothing and textile products to SABS standards, with areas for storage, cutting, machining, branding and embroidery, packing and dispatch.</p>
      {ticks(["Around 100 women and youth, many already running businesses, are incubated at the Hub", "Mentoring by experienced industry players on markets, supply chains and SABS quality", "Formal training towards SETA qualifications in clothing manufacturing and New Venture Creation", "Help to reach markets and funding through development finance institutions and corporate sponsors"])}
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">Grade 12 matric incubation camps</span>
      <h2 class="display h2">Thousands of matric learners hosted <span class="accent">since <span class="num">2019</span></span></h2>
      <p class="lead mt-1">Our camps support the matric results of the Dr Kenneth Kaunda District, and the Department of Education has recognised the Hub as a preferred Grade 12 camp venue.</p>
      <p class="muted">The camps have created more than 200 temporary jobs and income for more than 10 local SMMEs. We procure locally, from electrical materials and plumbing to mattresses, security and gardening services.</p>
    </div>
    <div class="deco reveal"><div class="frame ratio-3x2"><img src="img/matric-camp.webp" alt="Grade 12 learners in uniform during a matric camp session" loading="lazy" width="1368" height="912"></div></div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Partners behind the <span class="accent">Hub</span></h2>
      <p>The Hub is a platform for development institutions, SETAs and industry to roll out programmes at scale.</p>
    </div>
    <div class="grid grid-3">
      <div class="panel panel-fill reveal"><h3 class="display h3">Small Enterprise Development Agency</h3><p class="muted mt-1 mb-0">MMS is a SEDA Premium Client, with support from SEDA Dr Kenneth Kaunda and the North West Province.</p></div>
      <div class="panel panel-fill reveal"><h3 class="display h3">Industrial Development Corporation</h3><p class="muted mt-1 mb-0">Financial support to equip the factories at the Hub and build industrialists' competitiveness.</p></div>
      <div class="panel panel-fill reveal"><h3 class="display h3">Incubators and agencies</h3><p class="muted mt-1 mb-0">Partnerships with enterprise development incubators such as Lepharo and with the Mineworkers Development Agency.</p></div>
    </div>
  </div>
</section>

{cta('Bring your programme to the <span class="accent">Hub</span>', 'Classrooms, accommodation and workshops in one place for learnerships, camps and incubation programmes.')}
"""
write("hub.html", "Itireleng Learning and Manufacturing Hub", "The Itireleng Learning and Manufacturing Hub in Orkney, North West: classrooms, accommodation for 1 000 people, industrial workshops and the Itireleng Textile Hub.", hub)

# ------------------------------------------------------------------ IMPACT
GAL = [("it-4.webp", "Learners during database management training", "Database management training, North West Department of Public Works and Roads", "wide"),
       ("it-2.webp", "Two learners working at computers", "Database management training", ""),
       ("it-5.webp", "A facilitator helping a learner at a computer", "Database management training", ""),
       ("ohs-15.webp", "Delegates seated at tables during a safety course", "Occupational health and safety training", ""),
       ("ohs-16.webp", "Two delegates listening during a course", "Occupational health and safety training", ""),
       ("ohs-21.webp", "Delegates at a table during a training session", "Occupational health and safety training", ""),
       ("ohs-22.webp", "A learner performing CPR on a mannequin", "CPR assessment", ""),
       ("matric-camp.webp", "Matric learners in a hall during a camp", "Grade 12 matric incubation camp", "wide"),
       ("it-9.webp", "Learners working through course material at computers", "Database management training", ""),
       ("workshop-room.webp", "A facilitator presenting in a conference room", "Facilitated workshop", "")]
gal_html = "".join(
    f'<a class="zoomable group{" wide" if w else ""}" href="img/{s}" data-viewer data-alt="{escape(a)}" data-caption="{escape(c)}" aria-label="Open photo: {escape(c)}">'
    f'<img class="photo-zoom" src="img/{s}" alt="{escape(a)}" loading="lazy"><span class="zoom-hint">{ic("expand")}</span></a>'
    for s, a, c, w in GAL)

impact = page_hero("matric-camp.webp", "Matric learners during a camp", "Impact and CSI", '<span class="light">Development that</span> reaches communities') + f"""
<section class="section">
  <div class="wrap split split-wide-left">
    <div class="reveal">
      <span class="eyebrow">New Horizons Skills Development Project</span>
      <h2 class="display h2">Our community development <span class="accent">wing</span></h2>
    </div>
    <div class="reveal">
      <p class="lead">New Horizons Skills Development Project is a registered non-profit organisation (NPO <span class="num">197-584</span>) and the community development arm of Mbuso Management Solutions. It works nationally through community-specific skills programmes.</p>
      {ticks(["Train youth and women in self-mastery, self-confidence and goal setting", "Provide sector-based critical and scarce skills that improve employability", "Build business acumen and creative skills", "Create innovative solutions for different sectors of the economy", "Build partnerships for youth and women development"])}
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal"><h2 class="display h2">High-impact <span class="accent">success stories</span></h2></div>
    <div class="grid grid-2">
      <article class="panel panel-fill reveal">
        <span class="eyebrow num">2014 to 2017</span>
        <h3 class="display h3">Mathematics, Science and English project</h3>
        <p class="muted mt-1">Our flagship project in Khuma Township, Matlosana, took 60 needy but deserving Grade 9 learners through to Grade 12 with Saturday and holiday classes. After matric, they received financial and non-financial support to study further, and most are now completing their studies.</p>
      </article>
      <article class="panel panel-fill reveal">
        <span class="eyebrow">Since 2019</span>
        <h3 class="display h3">Grade 12 matric incubation camps</h3>
        <p class="muted mt-1">The Hub hosts matric camps for schools across the Dr Kenneth Kaunda District. The camps have created more than 200 temporary jobs and brought income to more than 10 local SMMEs.</p>
      </article>
      <article class="panel panel-fill reveal">
        <span class="eyebrow">Itireleng Textile Hub</span>
        <h3 class="display h3">Women and youth in manufacturing</h3>
        <p class="muted mt-1">Around 100 women and youth are incubated at the Textile Hub, working towards SETA qualifications and learning to produce to SABS quality.</p>
      </article>
      <article class="panel panel-fill reveal">
        <span class="eyebrow">Water and energy skills</span>
        <h3 class="display h3">Learnerships with SALGA and EW SETA</h3>
        <p class="muted mt-1">150 learners from five municipalities enrolled in a one-year water treatment and reticulation learnership with SALGA, and 50 young people trained in cable jointing and termination with the Energy and Water SETA.</p>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <h2 class="display h2">Recent <span class="accent">training</span></h2>
      <p>Photos from our programmes. Select any photo to view it larger.</p>
    </div>
    <div class="gallery reveal">{gal_html}</div>
  </div>
</section>

<section class="section-tight band">
  <div class="wrap split">
    <div class="reveal">
      <span class="eyebrow">In the media</span>
      <h2 class="display h2">Mine to school <span class="accent">conversion</span></h2>
    </div>
    <div class="reveal">
      <p class="lead">The Big Issue South Africa told the story of how Daddy Khuselo turned a derelict mining site into a thriving hub for learning and enterprise.</p>
      <a class="btn btn-outline" href="https://www.bigissue.org.za/mine-to-school-conversion/" target="_blank" rel="noopener noreferrer">Read the article {ic("arrow", "btn-arrow")}<span class="sr-only"> (opens in a new tab)</span></a>
    </div>
  </div>
</section>

{cta('Partner with us on <span class="accent">community development</span>', 'Corporate social investment, enterprise development and skills programmes that reach the people who need them.')}
"""
write("impact.html", "Impact and CSI", "New Horizons Skills Development Project, the Mathematics, Science and English project, matric camps and other impact from Mbuso Management Solutions.", impact)

# ------------------------------------------------------------------ CONTACT
topics = ["Strategy and consulting", "Training and skills development", "Industrial operations and the Hub", "Partnerships and CSI", "Something else"]
topic_opts = '<option value="" selected disabled>Choose a topic</option>' + "".join(f"<option>{t}</option>" for t in topics)
contact = page_hero("ohs-21.webp", "Delegates around a table during training", "Contact", '<span class="light">Start a</span> conversation') + f"""
<section class="section">
  <div class="wrap contact-grid">
    <div class="reveal">
      <h2 class="display h2">Talk to our <span class="accent">team</span></h2>
      <p class="lead mt-1">Tell us what you need, from a strategy session to a full learnership. We will put you in touch with the right person.</p>
      <ul class="contact-list mt-2">
        <li><span class="contact-icon">{ic("phone")}</span><div><strong>Telephone</strong><a class="num" href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></div></li>
        <li><span class="contact-icon">{ic("mail")}</span><div><strong>Email</strong><a href="mailto:{EMAIL}">{EMAIL}</a></div></li>
        <li><span class="contact-icon">{ic("pin")}</span><div><strong>Head office</strong><address>Tijger Valley Office Park #15<br>7 Pony Street, Silverlakes<br>Pretoria East, <span class="num">0084</span></address><a class="text-link mt-1" href="https://www.google.com/maps/search/?api=1&amp;query=Tijger+Valley+Office+Park+7+Pony+Street+Silverlakes+Pretoria" target="_blank" rel="noopener noreferrer">Get directions {ic("external")}</a></div></li>
        <li><span class="contact-icon">{ic("box")}</span><div><strong>Postal address</strong><address>PO Box <span class="num">12713</span>, Hatfield<br>Pretoria, <span class="num">0028</span></address></div></li>
      </ul>
    </div>
    <div class="panel panel-lg reveal">
      <form class="form" id="contact-form" novalidate>
        <div class="form-grid">
          <div><label class="field-label" for="name">Full name</label><input class="field" id="name" name="name" type="text" autocomplete="name" maxlength="80" required aria-describedby="name-error"><p class="field-error" id="name-error"></p></div>
          <div><label class="field-label" for="phone">Phone <span class="opt">(optional)</span></label><input class="field num" id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" placeholder="e.g. 082 123 4567" aria-describedby="phone-error"><p class="field-error" id="phone-error"></p></div>
          <div class="span-2"><label class="field-label" for="email">Email</label><input class="field" id="email" name="email" type="email" autocomplete="email" inputmode="email" maxlength="120" required aria-describedby="email-error"><p class="field-error" id="email-error"></p></div>
          <div class="span-2"><label class="field-label" for="organisation">Organisation <span class="opt">(optional)</span></label><input class="field" id="organisation" name="organisation" type="text" autocomplete="organization" maxlength="120" aria-describedby="organisation-error"><p class="field-error" id="organisation-error"></p></div>
          <div class="span-2"><label class="field-label" for="topic">What is your enquiry about?</label><select class="field" id="topic" name="topic" required aria-describedby="topic-error">{topic_opts}</select><p class="field-error" id="topic-error"></p></div>
          <div class="span-2"><label class="field-label" for="message">Message</label><textarea class="field" id="message" name="message" rows="5" maxlength="2000" required aria-describedby="message-count message-error" data-counter="message-count"></textarea><div class="field-meta"><p class="field-error" id="message-error"></p><p class="field-help num" id="message-count" aria-live="polite">0 / 2000</p></div></div>
        </div>
        <div class="hp" aria-hidden="true"><label for="website">Leave this empty</label><input id="website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <div>
          <label class="consent" for="consent"><input type="checkbox" id="consent" name="consent" aria-describedby="consent-error"><span>I agree that Mbuso Management Solutions may use these details to reply to my enquiry, as set out in the <a class="link" href="legal.html#privacy">privacy policy</a>.</span></label>
          <p class="field-error" id="consent-error"></p>
        </div>
        <button class="btn btn-primary btn-lg btn-block" type="submit">Prepare my email {ic("arrow", "btn-arrow")}</button>
        <p class="field-help center mt-0">Your email app opens with the message ready to send. Nothing is stored on this website.</p>
      </form>
    </div>
  </div>
</section>
"""
write("contact.html", "Contact", "Contact Mbuso Management Solutions in Pretoria East: telephone 086 102 2020, email mail@mbusoms.co.za.", contact)


# ------------------------------------------------------------------ LEARNERSHIPS
FIELDS = [
    ("Trades and energy", "QCTO and EW SETA", ["Plumbing Hand (Artisan and Assistant Plumber)", "Solar Hot Water Installation", "Hot Water Systems and Installation", "Energy Efficiency", "Basic Electrician", "Cable Jointing"]),
    ("Water and wastewater", "EW SETA", ["Water and Wastewater Treatment Operations Processes", "Water and Wastewater Reticulation Services"]),
    ("Agriculture", "AgriSETA", ["Animal Production", "Plant Production", "Poultry Production", "Horticulture"]),
    ("Clothing and furniture", "FP&amp;M SETA", ["Clothing, Textile, Footwear and Leather Manufacturing", "Furniture Making"]),
    ("Computers and IT", "MICT SETA", ["End User Computing", "Systems Development", "Technical Support"]),
    ("Business and safety", "Services SETA and QCTO", ["New Venture Creation", "Occupational Health and Safety"]),
]
fields_html = "".join(
    f'<article class="panel panel-fill reveal"><span class="eyebrow">{b}</span><h3 class="display h3">{t}</h3>'
    + '<ul class="ticks mt-1">' + "".join(f"<li>{ic('check')}<span>{q}</span></li>" for q in qs) + "</ul></article>"
    for t, b, qs in FIELDS)
field_opts = '<option value="" selected disabled>Choose a field</option>' + "".join(f"<option>{t.replace('&amp;','&amp;')}</option>" for t, _, _ in FIELDS) + "<option>Not sure yet</option>"
qual_opts = '<option value="" selected disabled>Choose one</option>' + "".join(f"<option>{q}</option>" for q in ["Below Grade 12", "Grade 12 (matric)", "Certificate or diploma", "Degree"])

learn = page_hero("ohs-13.webp", "A learner practising CPR on a training mannequin", "Learnerships", '<span class="light">Skills that</span> lead to work') + f"""
<section class="section">
  <div class="wrap split split-wide-left">
    <div class="reveal">
      <span class="eyebrow">Learn, practise, earn</span>
      <p class="statement">We focus on the <strong>critical and scarce skills</strong> the economy needs but mainstream education does not offer.</p>
    </div>
    <div class="reveal">
      <p class="lead">Our accredited programmes combine classroom theory with practical work. At the Itireleng Hub in Orkney, learners can study, stay and gain hands-on exposure in our own workshops and factories.</p>
      <p class="muted">Programmes run when funding and intakes open. Register your interest below and our training team will have your details when a suitable programme becomes available.</p>
      <a class="btn btn-primary mt-1" href="#register">Register your interest {ic("arrow", "btn-arrow")}</a>
    </div>
  </div>
</section>

<section class="section band">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Ways in</span><h2 class="display h2">Four routes into skills and work</h2></div>
      <p>Whether you are starting out, already working, or running a small business, there is a route that fits.</p>
    </div>
    <div class="grid grid-2">
      <article class="panel panel-fill reveal"><span class="route-icon">{ic("cap")}</span><h3 class="display h3">Learnerships and artisan training</h3><p class="muted mt-1 mb-0">Structured, accredited programmes that combine theory and workplace practice, leading to a recognised qualification.</p></article>
      <article class="panel panel-fill reveal"><span class="route-icon">{ic("badge")}</span><h3 class="display h3">Recognition of Prior Learning</h3><p class="muted mt-1 mb-0">Already skilled but without a certificate? RPL assesses what you know and can do, so your experience counts towards a qualification.</p></article>
      <article class="panel panel-fill reveal"><span class="route-icon">{ic("briefcase")}</span><h3 class="display h3">Work-integrated learning, reskilling and upskilling</h3><p class="muted mt-1 mb-0">Fast-track development for employees, so teams keep pace as roles and technology change.</p></article>
      <article class="panel panel-fill reveal"><span class="route-icon">{ic("sprout")}</span><h3 class="display h3">Incubation and mentorship</h3><p class="muted mt-1 mb-0">Mentoring for women, youth, SMMEs and cooperatives, such as the members of the Itireleng Textile Hub, with help to reach markets and funding.</p></article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">Accredited fields</span><h2 class="display h2">What you can train in</h2></div>
      <p>Programmes we are accredited to deliver. Which ones open, and when, depends on intakes and funding.</p>
    </div>
    <div class="grid grid-3">{fields_html}</div>
  </div>
</section>

<section class="section band-dark on-dark">
  <div class="wrap">
    <div class="section-head reveal">
      <div><span class="eyebrow">How it works</span><h2 class="display h2">From application to practice</h2></div>
      <p>Each programme has its own entry requirements and selection process, which we explain when an intake opens.</p>
    </div>
    <ol class="process reveal">
      <li><span class="p-icon">{ic("mail")}</span><span class="stage">Step one</span><h3 class="display h3">Register your interest</h3><p>Tell us who you are and which field interests you. We keep your details for upcoming intakes.</p></li>
      <li><span class="p-icon">{ic("search")}</span><span class="stage">Step two</span><h3 class="display h3">Assessment and selection</h3><p>When a programme opens, candidates who meet its requirements are invited to apply and be assessed.</p></li>
      <li><span class="p-icon">{ic("cap")}</span><span class="stage">Step three</span><h3 class="display h3">Train and practise</h3><p>Learn in the classroom, then build practical skills in our workshops, with mentoring along the way.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="wrap split split-wide-right">
    <div class="deco deco-alt reveal"><div class="frame frame-accent ratio-4x3"><img src="img/it-9.webp" alt="Learners working through course material at computers" loading="lazy" width="1440" height="581"></div></div>
    <div class="reveal">
      <span class="eyebrow">For employers</span>
      <h2 class="display h2">Develop your people with us</h2>
      <p class="lead mt-1">We design and deliver learnerships, skills programmes and RPL for organisations that want to grow their own talent, from a single team to a multi-year programme.</p>
      {ticks(["Accredited programmes with the QCTO and five SETAs", "Classrooms, accommodation and workshops at the Itireleng Hub", "Skills audits to find the gaps before training starts"])}
      <a class="text-link mt-2" href="contact.html">Talk to us about a programme {ic("arrow")}</a>
    </div>
  </div>
</section>

<section class="section band" id="register">
  <div class="wrap contact-grid">
    <div class="reveal">
      <span class="eyebrow">Register your interest</span>
      <h2 class="display h2">Be ready for the next intake</h2>
      <p class="lead mt-1">Share a few details and the field you are interested in. Registering does not guarantee a place, and there is no fee to register.</p>
      <div class="note mt-2">{ic("info")}<p>Be careful of anyone who asks for money to secure a learnership. If someone asks for payment in our name, check with us first on <span class="num">{PHONE_DISPLAY}</span>.</p></div>
    </div>
    <div class="panel panel-lg reveal">
      <form class="form" id="interest-form" novalidate>
        <div class="form-grid">
          <div><label class="field-label" for="i-name">Full name</label><input class="field" id="i-name" name="name" type="text" autocomplete="name" maxlength="80" required aria-describedby="i-name-error"><p class="field-error" id="i-name-error"></p></div>
          <div><label class="field-label" for="i-phone">Cellphone</label><input class="field num" id="i-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" placeholder="e.g. 082 123 4567" required aria-describedby="i-phone-error"><p class="field-error" id="i-phone-error"></p></div>
          <div class="span-2"><label class="field-label" for="i-email">Email <span class="opt">(optional)</span></label><input class="field" id="i-email" name="email" type="email" autocomplete="email" inputmode="email" maxlength="120" aria-describedby="i-email-error"><p class="field-error" id="i-email-error"></p></div>
          <div class="span-2"><label class="field-label" for="i-town">Town or city</label><input class="field" id="i-town" name="town" type="text" autocomplete="address-level2" maxlength="60" required aria-describedby="i-town-error"><p class="field-error" id="i-town-error"></p></div>
          <div><label class="field-label" for="i-field">Field of interest</label><select class="field" id="i-field" name="field" required aria-describedby="i-field-error">{field_opts}</select><p class="field-error" id="i-field-error"></p></div>
          <div><label class="field-label" for="i-qual">Highest qualification</label><select class="field" id="i-qual" name="qualification" required aria-describedby="i-qual-error">{qual_opts}</select><p class="field-error" id="i-qual-error"></p></div>
          <div class="span-2"><label class="field-label" for="i-message">Anything else we should know? <span class="opt">(optional)</span></label><textarea class="field" id="i-message" name="message" rows="3" maxlength="1000" aria-describedby="i-message-count i-message-error" data-counter="i-message-count"></textarea><div class="field-meta"><p class="field-error" id="i-message-error"></p><p class="field-help num" id="i-message-count" aria-live="polite">0 / 1000</p></div></div>
        </div>
        <div class="hp" aria-hidden="true"><label for="i-website">Leave this empty</label><input id="i-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
        <div>
          <label class="consent" for="i-consent"><input type="checkbox" id="i-consent" name="consent" aria-describedby="i-consent-error"><span>I agree that Mbuso Management Solutions may keep these details to contact me about learnerships, as set out in the <a class="link" href="legal.html#privacy">privacy policy</a>.</span></label>
          <p class="field-error" id="i-consent-error"></p>
        </div>
        <button class="btn btn-primary btn-lg btn-block" type="submit">Prepare my registration {ic("arrow", "btn-arrow")}</button>
        <p class="field-help center mt-0">Your email app opens with your details ready to send to {EMAIL}. Nothing is stored on this website.</p>
      </form>
    </div>
  </div>
</section>
"""
write("learnerships.html", "Learnerships", "Learnerships, artisan training, Recognition of Prior Learning and incubation from Mbuso Management Solutions, accredited with the QCTO and five SETAs. Register your interest.", learn)

# ------------------------------------------------------------------ LEGAL
legal = f"""<section class="section">
  <div class="wrap wrap-read">
    <span class="eyebrow">Legal</span>
    <h1 class="display h1-plain">Privacy, terms and <span class="accent">cookies</span></h1>
    <p class="muted mt-1">Last updated 24 November <span class="num">2026</span>. Draft for review by Mbuso Management Solutions before publication.</p>
    <nav class="even-row even-min-9 mt-2" aria-label="Legal sections">
      <a class="btn btn-outline" href="#privacy">Privacy policy</a>
      <a class="btn btn-outline" href="#terms">Terms of use</a>
      <a class="btn btn-outline" href="#cookies">Cookie policy</a>
    </nav>
    <div class="prose">
      <h2 id="privacy">Privacy policy</h2>
      <p>Mbuso Management Solutions (Pty) Ltd (registration number <span class="num">2012/074900/07</span>) respects your privacy and processes personal information in line with the Protection of Personal Information Act, <span class="num">2013</span> (POPIA).</p>
      <h3>What this website collects</h3>
      <p>This website does not collect or store personal information itself. It has no accounts, analytics, advertising or tracking.</p>
      <p>The contact form checks your details in your browser and then opens your own email app with a message addressed to {EMAIL}. Nothing is sent until you press send in your email app. When you do, we receive the details you chose to include: your name, organisation, email address, phone number and message.</p>
      <p>The learnership registration form works the same way. If you send it, we receive your name, cellphone number, email address if given, town, field of interest, highest qualification and any message. We keep these details only to contact you about suitable learnerships, and you may ask us to delete them at any time.</p>
      <h3>How we use your information</h3>
      <ul>
        <li>To reply to your enquiry and arrange the services you ask about.</li>
        <li>To contact you about learnerships and training intakes, if you registered your interest.</li>
        <li>To keep a record of our correspondence with you.</li>
      </ul>
      <p>We do not sell your information or use it for marketing without your consent.</p>
      <h3>Third parties</h3>
      <p>Emails are handled by our email provider. Links to Facebook, Instagram, Google Maps and news websites take you to those services, which have their own privacy policies.</p>
      <h3>Your rights</h3>
      <p>You may ask what personal information we hold about you, ask us to correct or delete it, or object to how we use it. Contact us at <a class="link" href="mailto:{EMAIL}">{EMAIL}</a>. You may also lodge a complaint with the Information Regulator of South Africa.</p>

      <h2 id="terms">Terms of use</h2>
      <p>By using this website you agree to these terms.</p>
      <ul>
        <li>The content is for general information about Mbuso Management Solutions and its services. It is not professional advice for your specific situation.</li>
        <li>We work to keep information accurate and current, but programmes, accreditations and figures may change. Please confirm details with us before relying on them.</li>
        <li>Text, photographs and logos on this website belong to Mbuso Management Solutions or are used with permission. Please do not reuse them without written consent.</li>
        <li>Links to other websites are provided for convenience. We are not responsible for their content.</li>
        <li>These terms are governed by the laws of the Republic of South Africa.</li>
      </ul>

      <h2 id="cookies">Cookie policy</h2>
      <p>This website does not set cookies and does not use analytics or tracking technologies. Fonts and images are served from this website itself, so visiting it does not share your information with font or advertising services.</p>
      <p>If this changes, for example if analytics are added, we will update this policy and ask for your consent first where required.</p>
    </div>
  </div>
</section>
"""
write("legal.html", "Privacy, terms and cookies", "Privacy policy, terms of use and cookie policy for the Mbuso Management Solutions website.", legal)

# 404
notfound = f"""<section class="section">
  <div class="wrap">
    <span class="eyebrow">Page not found</span>
    <h1 class="display h1-plain">This page has <span class="accent">moved</span></h1>
    <p class="lead mt-1">The page you are looking for is not here. It may have moved when we updated our website.</p>
    <div class="even-cols fit-md mt-2"><a class="btn btn-primary" href="index.html">Go to the home page {ic("arrow", "btn-arrow")}</a><a class="btn btn-outline" href="contact.html">Contact us</a></div>
  </div>
</section>
"""
write("404.html", "Page not found", "This page could not be found.", notfound)
