/* Mbuso Management Solutions — site behaviour. No third-party code, no tracking. */
(function () {
  "use strict";
  var doc = document.documentElement;
  doc.classList.add("js");
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* Header border once the page scrolls */
  var header = document.querySelector(".site-header");
  function onScroll() { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();


  /* Dialogs and the back button: opening pushes a history entry, so the phone's
     back button closes the menu or photo viewer before it leaves the page. */
  var closingFromHistory = false;
  function trackDialog(dlg) {
    if (!dlg) return;
    dlg.addEventListener("close", function () {
      if (!closingFromHistory && history.state && history.state.mbusoDialog === dlg.id) history.back();
    });
  }
  function openDialog(dlg) {
    if (!dlg || dlg.open) return;
    dlg.showModal();
    try { history.pushState({ mbusoDialog: dlg.id }, ""); } catch (e) {}
  }
  window.addEventListener("popstate", function () {
    var open = document.querySelector("dialog[open]");
    if (open) { closingFromHistory = true; open.close(); closingFromHistory = false; }
  });

  /* Mobile menu */
  var menu = document.getElementById("mobile-menu");
  var menuOpen = document.querySelector("[data-menu-open]");
  if (menu && menuOpen && typeof menu.showModal === "function") {
    trackDialog(menu);
    menuOpen.addEventListener("click", function () {
      openDialog(menu);
      menuOpen.setAttribute("aria-expanded", "true");
    });
    menu.addEventListener("close", function () {
      menuOpen.setAttribute("aria-expanded", "false");
      menuOpen.focus();
    });
    menu.querySelectorAll("[data-menu-close]").forEach(function (el) {
      el.addEventListener("click", function () { menu.close(); });
    });
    // Following a link: close without stepping back in history, so the link wins
    menu.querySelectorAll("nav a").forEach(function (el) {
      el.addEventListener("click", function () { closingFromHistory = true; menu.close(); closingFromHistory = false; });
    });
    window.addEventListener("resize", function () { if (window.innerWidth >= 1100 && menu.open) menu.close(); });
    menu.addEventListener("click", function (e) { if (e.target === menu) menu.close(); }); // tap outside the drawer
  }

  /* Toasts */
  var toastRegion = document.querySelector(".toast-region");
  var ICON_OK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';
  var ICON_ERR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>';
  function toast(message, isError) {
    if (!toastRegion) return;
    var t = document.createElement("div");
    t.className = "toast" + (isError ? " is-error" : "");
    t.setAttribute("role", isError ? "alert" : "status");
    t.innerHTML = isError ? ICON_ERR : ICON_OK;
    var span = document.createElement("span");
    span.textContent = message; // text only, never HTML
    t.appendChild(span);
    toastRegion.appendChild(t);
    setTimeout(function () {
      t.classList.add("is-leaving");
      setTimeout(function () { t.remove(); }, 320);
    }, isError ? 7000 : 4500);
  }

  /* Home slideshow: dots, pause, swipe, keyboard; no autoplay with reduced motion */
  var hero = document.querySelector("[data-slideshow]");
  if (hero) {
    var slides = Array.prototype.slice.call(hero.querySelectorAll(".slide"));
    var dots = Array.prototype.slice.call(hero.querySelectorAll(".dot"));
    var caption = hero.querySelector(".slide-caption");
    var pauseBtn = hero.querySelector(".pause-btn");
    var current = 0, timer = null, DELAY = 6500;
    var playing = !reduceMotion.matches;

    function warm(slide) {
      var img = slide.querySelector("img"); if (!img) return;
      if (img.dataset.src) { img.srcset = img.dataset.srcset || ""; img.src = img.dataset.src; delete img.dataset.src; delete img.dataset.srcset; }
      if (img.loading === "lazy") img.loading = "eager";
    }
    function show(i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, n) {
        var on = n === current;
        s.classList.toggle("is-active", on);
        s.setAttribute("aria-hidden", on ? "false" : "true");
        if (on) warm(s);
      });
      dots.forEach(function (d, n) { d.setAttribute("aria-current", n === current ? "true" : "false"); });
      if (caption) caption.textContent = slides[current].getAttribute("data-caption") || "";
      // warm the next photo so the fade never shows an empty frame
      warm(slides[(current + 1) % slides.length]);
    }
    function schedule() { clearTimeout(timer); if (playing) timer = setTimeout(function () { show(current + 1); schedule(); }, DELAY); }
    function setPlaying(p) {
      playing = p;
      if (pauseBtn) {
        pauseBtn.setAttribute("aria-label", p ? "Pause slideshow" : "Play slideshow");
        pauseBtn.querySelector(".i-pause").toggleAttribute("hidden", !p);
        pauseBtn.querySelector(".i-play").toggleAttribute("hidden", p);
      }
      schedule();
    }
    dots.forEach(function (d, n) { d.addEventListener("click", function () { show(n); schedule(); }); });
    if (pauseBtn) pauseBtn.addEventListener("click", function () { setPlaying(!playing); });
    hero.addEventListener("keydown", function (e) {
      if (e.target.closest("a, input, textarea")) return;
      if (e.key === "ArrowRight") { show(current + 1); schedule(); }
      if (e.key === "ArrowLeft") { show(current - 1); schedule(); }
    });
    var sx = null;
    hero.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener("touchend", function (e) {
      if (sx === null) return;
      var dx = e.changedTouches[0].clientX - sx; sx = null;
      if (Math.abs(dx) > 50) { show(current + (dx < 0 ? 1 : -1)); schedule(); }
    }, { passive: true });
    document.addEventListener("visibilitychange", function () { if (document.hidden) clearTimeout(timer); else schedule(); });
    reduceMotion.addEventListener && reduceMotion.addEventListener("change", function (e) { if (e.matches) setPlaying(false); });
    show(0);
    setPlaying(playing);
  }

  /* Reveal sections as they scroll in */
  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion.matches) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Full-screen photo viewer for galleries */
  var viewer = document.getElementById("photo-viewer");
  var items = Array.prototype.slice.call(document.querySelectorAll("[data-viewer]"));
  if (viewer && items.length && typeof viewer.showModal === "function") {
    var vImg = viewer.querySelector(".viewer-stage img");
    var vCount = viewer.querySelector(".viewer-count");
    var vCap = viewer.querySelector(".viewer-caption");
    var at = 0, opener = null;
    trackDialog(viewer);
    function load(i) {
      at = (i + items.length) % items.length;
      var it = items[at];
      vImg.style.opacity = "0";
      var src = it.getAttribute("href");
      var pre = new Image();
      pre.onload = function () { vImg.src = src; vImg.alt = it.getAttribute("data-alt") || ""; vImg.style.opacity = "1"; };
      pre.src = src;
      vCount.textContent = (at + 1) + " / " + items.length;
      vCap.textContent = it.getAttribute("data-caption") || "";
      [at + 1, at - 1].forEach(function (n) { var p = new Image(); p.src = items[(n + items.length) % items.length].getAttribute("href"); });
    }
    items.forEach(function (it, i) {
      it.addEventListener("click", function (e) { e.preventDefault(); opener = it; load(i); openDialog(viewer); viewer.querySelector(".viewer-close").focus(); });
    });
    viewer.querySelector(".viewer-close").addEventListener("click", function () { viewer.close(); });
    viewer.querySelector(".viewer-prev").addEventListener("click", function () { load(at - 1); });
    viewer.querySelector(".viewer-next").addEventListener("click", function () { load(at + 1); });
    viewer.addEventListener("keydown", function (e) { if (e.key === "ArrowRight") load(at + 1); if (e.key === "ArrowLeft") load(at - 1); });
    viewer.addEventListener("click", function (e) { if (e.target === viewer || e.target.classList.contains("viewer-stage")) viewer.close(); });
    viewer.addEventListener("close", function () { if (opener) opener.focus(); });
    var vx = null;
    viewer.addEventListener("touchstart", function (e) { vx = e.touches[0].clientX; }, { passive: true });
    viewer.addEventListener("touchend", function (e) { if (vx === null) return; var dx = e.changedTouches[0].clientX - vx; vx = null; if (Math.abs(dx) > 50) load(at + (dx < 0 ? 1 : -1)); }, { passive: true });
  }

  /* Forms: validate here for helpful messages, then hand the message to the visitor's
     own email app. Nothing is sent to or stored on any server. */
  function setupForm(form, RULES, prefix, consentMsg, compose) {
    function setError(field, text) {
      var err = document.getElementById(field.id + "-error");
      field.setAttribute("aria-invalid", text ? "true" : "false");
      if (err) err.textContent = text || "";
    }
    function check(field) {
      var r = RULES[field.name]; if (!r) return true;
      var v = field.value.trim();
      if (!v && r.optional) { setError(field, ""); return true; }
      if (r.max && v.length > r.max) { setError(field, "Please keep this under " + r.max + " characters."); return false; }
      var ok = v.length > 0 && (!r.min || v.length >= r.min) && (!r.re || r.re.test(v)) && (!r.allowed || r.allowed.indexOf(v) !== -1);
      setError(field, ok ? "" : (r.msg || "Please check this field."));
      return ok;
    }
    Array.prototype.forEach.call(form.elements, function (f) {
      if (!RULES[f.name]) return;
      f.addEventListener("blur", function () { if (f.value) check(f); });
      f.addEventListener("input", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
      f.addEventListener("change", function () { if (f.getAttribute("aria-invalid") === "true") check(f); });
    });
    var consent = form.querySelector('input[name="consent"]');
    var consentErr = consent ? document.getElementById(consent.id + "-error") : null;
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (form.querySelector(".hp input").value) return; // a bot filled the hidden field
      var first = null;
      Object.keys(RULES).forEach(function (k) { var f = form.elements[k]; if (f && !check(f) && !first) first = f; });
      if (consent && !consent.checked) { consentErr.textContent = consentMsg; if (!first) first = consent; }
      else if (consentErr) consentErr.textContent = "";
      if (first) { first.focus(); toast("Please check the highlighted fields.", true); return; }
      var btn = form.querySelector("button[type=submit]");
      btn.disabled = true;
      btn.setAttribute("aria-busy", "true");
      var spin = document.createElement("span");
      spin.className = "spinner"; spin.setAttribute("role", "status"); spin.setAttribute("aria-label", "Preparing your message");
      btn.appendChild(spin);
      var get = function (k) { return form.elements[k].value.trim(); };
      var m = compose(get);
      window.location.href = "mailto:mail@mbusoms.co.za?subject=" + encodeURIComponent(m.subject) + "&body=" + encodeURIComponent(m.body);
      setTimeout(function () {
        btn.disabled = false;
        btn.removeAttribute("aria-busy");
        if (spin.parentNode) spin.remove();
        toast("Your message is ready in your email app. If it did not open, email mail@mbusoms.co.za directly.");
      }, 600);
    });
  }
  var EMAIL_RE = /^[^\s@<>()]+@[^\s@<>()]+\.[^\s@<>()]{2,}$/;
  var PHONE_RE = /^[+0-9 ()-]{9,20}$/;

  var contactForm = document.getElementById("contact-form");
  if (contactForm) setupForm(contactForm, {
    name: { max: 80, msg: "Please enter your name." },
    organisation: { max: 120, optional: true },
    email: { max: 120, re: EMAIL_RE, msg: "Please enter a valid email address, for example name@company.co.za." },
    phone: { max: 20, optional: true, re: PHONE_RE, msg: "Please enter a phone number using digits, spaces or +." },
    topic: { msg: "Please choose what your enquiry is about.", allowed: ["Strategy and consulting", "Training and skills development", "Industrial operations and the Hub", "Partnerships and CSI", "Something else"] },
    message: { min: 10, max: 2000, msg: "Please write a short message (at least 10 characters)." }
  }, "", "Please agree so we may use your details to reply.", function (get) {
    return { subject: "Website enquiry: " + get("topic"),
      body: "Name: " + get("name") + "\nOrganisation: " + (get("organisation") || "-") + "\nEmail: " + get("email") + "\nPhone: " + (get("phone") || "-") + "\n\n" + get("message") };
  });

  var interestForm = document.getElementById("interest-form");
  if (interestForm) setupForm(interestForm, {
    name: { max: 80, msg: "Please enter your full name." },
    phone: { max: 20, re: PHONE_RE, msg: "Please enter your cellphone number, for example 082 123 4567." },
    email: { max: 120, optional: true, re: EMAIL_RE, msg: "Please enter a valid email address, or leave it empty." },
    town: { max: 60, msg: "Please enter your town or city." },
    field: { msg: "Please choose a field of interest.", allowed: ["Trades and energy", "Water and wastewater", "Agriculture", "Clothing and furniture", "Computers and IT", "Business and safety", "Not sure yet"] },
    qualification: { msg: "Please choose your highest qualification.", allowed: ["Below Grade 12", "Grade 12 (matric)", "Certificate or diploma", "Degree"] },
    message: { max: 1000, optional: true }
  }, "i-", "Please agree so we may keep your details for learnerships.", function (get) {
    return { subject: "Learnership interest: " + get("field"),
      body: "Name: " + get("name") + "\nCellphone: " + get("phone") + "\nEmail: " + (get("email") || "-") + "\nTown: " + get("town") + "\nField of interest: " + get("field") + "\nHighest qualification: " + get("qualification") + "\n\n" + (get("message") || "") };
  });


  /* Live length counters on long text ("120 / 2000"); maxlength stops typing at the limit */
  document.querySelectorAll("textarea[data-counter]").forEach(function (ta) {
    var out = document.getElementById(ta.getAttribute("data-counter"));
    var max = ta.getAttribute("maxlength");
    function upd() { if (out) out.textContent = ta.value.length + " / " + max; }
    ta.addEventListener("input", upd); upd();
  });


  /* Offline copy: a service worker that always fetches the newest page first */
  if ("serviceWorker" in navigator && /^https?:$/.test(location.protocol) && window.isSecureContext) {
    try { navigator.serviceWorker.register("sw.js").catch(function () {}); } catch (e) {}
  }

  /* Footer year */
  var y = document.querySelector("[data-year]");
  if (y) y.textContent = String(new Date().getFullYear());
})();
