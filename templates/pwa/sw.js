const VERSION = "000109";

const CACHE_NAME = `PWA-CACHE-${VERSION}`;

const STATIC_RESOURCES = [
    "/offline/",
    "/static/app/style.css",
    "/static/app/bulma/css/bulma.min.css",
    "/static/pwa/manifest.json",
    "/static/app/js/app.js",
    "/static/app/js/control.js",
//   Images
    "/static/app/images/icons/logo.png",
    "/static/app/images/icons/favicon.png",
    // Other Online Resources
    // "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,500;0,700;1,400&display=swap",
    // "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css",
];


// Install SW

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                return cache.addAll(STATIC_RESOURCES);
            })
    );
});

// Actiavte the SW and delete the prevous Caches

self.addEventListener("activate", (event) => {
    event.waitUntil(
        (async () => {
        const names = await caches.keys();
        await Promise.all(
            names.map((name) => {
            if (name !== CACHE_NAME) {
                return caches.delete(name);
            }
            }),
        );
        // Lets the SW to take control of the Website Imediately
        await clients.claim();
        })(),
    );
});
  
// Finish Up 

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                // If the request fails, serve a fallback page
                return caches.match('/offline/');
            })
    );
});