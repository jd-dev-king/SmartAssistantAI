"use strict";

const CACHE_NAME =
    "smart-assistant-ai-v2-cache-7.1";

const APP_FILES = [
    "./",
    "./index.html",
    "./style.css",
    "./script.js",
    "./manifest.webmanifest",
    "./assets/smart-ai-logo.png"
];


/* ---------------------------------
   INSTALL
---------------------------------- */

self.addEventListener(
    "install",
    event => {
        event.waitUntil(
            caches
                .open(CACHE_NAME)
                .then(async cache => {
                    const results =
                        await Promise.allSettled(
                            APP_FILES.map(
                                async filePath => {
                                    const response =
                                        await fetch(
                                            filePath,
                                            {
                                                cache:
                                                    "reload"
                                            }
                                        );

                                    if (!response.ok) {
                                        throw new Error(
                                            `${filePath} returned ${response.status}`
                                        );
                                    }

                                    await cache.put(
                                        filePath,
                                        response
                                    );

                                    return filePath;
                                }
                            )
                        );

                    for (const result of results) {
                        if (
                            result.status ===
                            "rejected"
                        ) {
                            console.error(
                                "Could not cache application file:",
                                result.reason
                            );
                        }
                    }

                    /*
                     * Require the main page to exist.
                     * Optional files may fail without
                     * preventing service-worker installation.
                     */

                    const cachedIndex =
                        await cache.match(
                            "./index.html"
                        );

                    if (!cachedIndex) {
                        throw new Error(
                            "index.html could not be cached"
                        );
                    }
                })
        );

        self.skipWaiting();
    }
);


/* ---------------------------------
   ACTIVATE
---------------------------------- */

self.addEventListener(
    "activate",
    event => {
        event.waitUntil(
            caches
                .keys()
                .then(cacheNames => {
                    return Promise.all(
                        cacheNames
                            .filter(
                                cacheName =>
                                    cacheName !==
                                    CACHE_NAME
                            )
                            .map(
                                cacheName =>
                                    caches.delete(
                                        cacheName
                                    )
                            )
                    );
                })
                .then(() =>
                    self.clients.claim()
                )
        );
    }
);


/* ---------------------------------
   FETCH
---------------------------------- */

self.addEventListener(
    "fetch",
    event => {
        if (
            event.request.method !== "GET"
        ) {
            return;
        }

        const requestUrl =
            new URL(event.request.url);

        const isLocalRequest =
            requestUrl.origin ===
            self.location.origin;

        if (!isLocalRequest) {
            /*
             * Weather, dictionary, Wikipedia,
             * jokes, and other APIs remain
             * network-only.
             */

            event.respondWith(
                fetch(event.request)
            );

            return;
        }

        event.respondWith(
            fetch(event.request)
                .then(response => {
                    if (
                        response &&
                        response.ok
                    ) {
                        const copy =
                            response.clone();

                        caches
                            .open(CACHE_NAME)
                            .then(cache => {
                                cache.put(
                                    event.request,
                                    copy
                                );
                            });
                    }

                    return response;
                })
                .catch(async () => {
                    const cachedResponse =
                        await caches.match(
                            event.request
                        );

                    if (cachedResponse) {
                        return cachedResponse;
                    }

                    if (
                        event.request.mode ===
                        "navigate"
                    ) {
                        return (
                            caches.match(
                                "./index.html"
                            )
                        );
                    }

                    return new Response(
                        "Offline resource unavailable.",
                        {
                            status: 503,
                            headers: {
                                "Content-Type":
                                    "text/plain"
                            }
                        }
                    );
                })
        );
    }
);