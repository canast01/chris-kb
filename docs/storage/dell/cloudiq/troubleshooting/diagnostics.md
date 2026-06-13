---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# CloudIQ — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Log Locations, Before Calling Support.
</div>

```text
┌────────────────────────────────────── Dell CloudIQ Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Diagnose CloudIQ issues with SCG CLI commands, log bundles, and API connectivity       │   │
│   │             scg connectivity --test: validates HTTPS outbound to CloudIQ endpoints            │   │
│   │               scg log collect: bundles all SCG logs for Dell support case upload              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              # Step 1 — Check SCG service status                              │   │
│   │                                       ssh admin@<SCG_IP>                                      │   │
│   │                                           scg status                                          │   │
│   │                                                                                               │   │
│   │                             # Step 2 — Test outbound connectivity                             │   │
│   │                                    scg connectivity --test                                    │   │
│   │                                                                                               │   │
│   │                           # Step 3 — Test specific device connection                          │   │
│   │                                scg device test --id <device_id>                               │   │
│   │                                                                                               │   │
│   │                              # Step 4 — Collect logs for support                              │   │
│   │                         scg log collect --output /tmp/scg_logs.tar.gz                         │   │
│   │                                                                                               │   │
│   │                                 # Step 5 — View SCG system log                                │   │
│   │                                  tail -f /var/log/scg/scg.log                                 │   │
│   │                                                                                               │   │
│   │                     # Step 6 — Check DNS resolution for CloudIQ endpoints                     │   │
│   │                                   nslookup cloudiq.dell.com                                   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    scg connectivity = Tests TCP/HTTPS reachability to all required CloudIQ cloud endpoints            │
│    scg device test  = Authenticates to specific storage system and reports poll success/fail          │
│    scg log collect  = Bundles SCG application logs, config (sanitised), and diagnostics               │
│    /var/log/scg     = SCG application log directory; scg.log for main service events                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

For systems connected via a **proxy**, verify proxy settings in the SCG web UI under **Settings > Proxy** and confirm the proxy allows HTTPS to `cloudiq.dell.com` and `esrs3.emc.com` on port 443.

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Log Locations

| Log | Location | Use |
|---|---|---|
| SCG telemetry forwarding logs | `/var/log/dsagw/` on the SCG host | Diagnose why a system is not reporting; look for connection refused or TLS errors |
| SCG application logs | `/var/log/esrs/` | Broader SCG service errors |
| CloudIQ audit log | CloudIQ portal: **Admin > Audit Log** | Track user actions, API calls, and configuration changes |
| Browser console | Browser DevTools (F12) > Console | Diagnose UI rendering errors or failed API calls in the CloudIQ dashboard |

## Before Calling Support

Collect the following before opening a Dell support case for a CloudIQ issue:

- **SCG version**: visible in SCG web UI under **Settings > About**
- **CloudIQ system list screenshot**: screenshot of the Systems page showing which systems are and are not reporting
- **API error response**: full JSON error body and HTTP status code from any failing API call, with timestamp
- **SCG connectivity test output**: output of `curl -k https://esrs3.emc.com` and `systemctl status dsagw`
- **dsagw logs**: relevant lines from `/var/log/dsagw/` around the time the issue started
- **Browser console errors**: for dashboard UI issues, export the browser console log with timestamps

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
