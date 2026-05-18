---
title: You're Offline
---

# You're offline

No internet connection. Pages you've visited before are still available — use the navigation to browse cached content.

```
┌──────────────────────────────────────────────────────────┐
│                  Offline Access Flow                     │
└─────────────────────────┬────────────────────────────────┘
                          │
          ┌───────────────┴──────────────┐
          ▼                              ▼
┌──────────────────┐           ┌──────────────────────┐
│  Download KB     │           │  Local MkDocs Serve  │
│                  │           │                      │
│ git clone / pull │           │ mkdocs serve         │
│ the repo         │           │ → http://127.0.0.1   │
│                  │           │    :8000             │
└────────┬─────────┘           └──────────┬───────────┘
         │                                │
         └────────────────┬───────────────┘
                          ▼
               ┌──────────────────────┐
               │  Browse cached KB    │
               │  without internet    │
               │  Full nav available  │
               └──────────────────────┘
```
