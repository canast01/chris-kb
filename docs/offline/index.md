---
title: You're Offline
---

# You're offline


<div class="kb-summary">
Offline fallback page: displayed automatically when the KB site is accessed without a network connection via the service worker cache.
</div>

```text
┌────────────────────────────────── Offline — No Internet Connection ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               This page is displayed when the browser cannot reach the KB server              │   │
│   │         Pages visited before going offline are available from the service worker cache        │   │
│   │                 Use the navigation menu to browse cached content while offline                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Service worker = Browser background script; caches pages for offline access (PWA pattern)          │
│    PWA            = Progressive Web App; installable; works offline using service worker cache        │
│    Cache          = Local copy of page content stored by the service worker on first visit            │
│    Fallback page  = Shown when a requested URL is not in cache and network is unavailable             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
No internet connection. Pages you've visited before are still available — use the navigation to browse cached content.

