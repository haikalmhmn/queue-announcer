// Queue Announcer service worker.
// Network first, so every PC always gets the newest version when online.
// Falls back to the last saved copy when the internet is down, so the app keeps working.
var CACHE = 'queue-announcer';

self.addEventListener('install', function () { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });

self.addEventListener('fetch', function (e) {
  var req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return;
  var isPage = req.mode === 'navigate';
  e.respondWith(
    fetch(req, { cache: 'no-store' }).then(function (res) {
      if (res && res.ok) {
        var copy = res.clone();
        var key = isPage ? new Request(new URL('./', self.registration.scope)) : req;
        caches.open(CACHE).then(function (c) { c.put(key, copy); });
      }
      return res;
    }).catch(function () {
      return caches.open(CACHE).then(function (c) {
        if (isPage) return c.match(new URL('./', self.registration.scope).href);
        return c.match(req, { ignoreSearch: true });
      }).then(function (hit) { return hit || Response.error(); });
    })
  );
});
