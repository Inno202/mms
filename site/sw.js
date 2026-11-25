/* Mbuso Management Solutions — offline copy.
   Network first: visitors always get the newest page when online; the cached copy
   is used only when the network fails. Bump VERSION on each release. */
const VERSION = "mbuso-2026-11-25";
const CORE = ["./", "index.html", "about.html", "services.html", "hub.html", "impact.html", "learnerships.html", "contact.html", "legal.html", "404.html", "css/site.css", "js/site.js", "img/logo-360.png"];

self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(VERSION).then((c) => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k)))).then(() => self.clients.claim())
  );
});
self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  event.respondWith(
    fetch(req)
      .then((res) => {
        if (res.ok) { const copy = res.clone(); caches.open(VERSION).then((c) => c.put(req, copy)); }
        return res;
      })
      .catch(() => caches.match(req).then((hit) => hit || (req.mode === "navigate" ? caches.match("404.html") : undefined)))
  );
});
