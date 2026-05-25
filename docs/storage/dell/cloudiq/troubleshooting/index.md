# CloudIQ — Troubleshooting


```text
┌─────────────────────────────────── Dell CloudIQ — Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CloudIQ troubleshooting: connectivity issues, missing telemetry, alert and report failures  │   │
│   │     Connectivity: SCG not connecting to cloud — check proxy, DNS, firewall, cert validity     │   │
│   │   Data issues: missing health scores, stale metrics — verify array credentials and SCG logs   │   │
│   │    Alert/report issues: false positives, email failures — check policy thresholds and SMTP    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify symptom → check SCG Diagnostics → verify array creds → escalate to Dell SR                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Connectivity        │  │         Data Issues         │  │        Alert / Report       │   │
│   │      SCG not connecting     │  │      Missing telemetry      │  │       False positives       │   │
│   │         Proxy errors        │  │         Stale scores        │  │         Alert storms        │   │
│   │         DNS failures        │  │      Array not visible      │  │        Email not sent       │   │
│   │        Firewall block       │  │        Cred failures        │  │         Export fails        │   │
│   │       Cert validation       │  │        Telemetry lag        │  │       Dashboard stale       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Check SCG web UI > Diagnostics for connection status; check CloudIQ portal System Status page      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Symptom      │      Cause       │       Check       │       Fix        │   Escalate If    │   │
│   │   SCG offline    │  Firewall/proxy  │  SCG Diagnostics  │ Open 443 egress  │   >30 min down   │   │
│   │   No telemetry   │    Bad creds     │  Array cred test  │  Re-enter creds  │   >1 h missing   │   │
│   │   False alert    │  Low threshold   │  Policy settings  │ Raise threshold  │   Storm > 50/h   │   │
│   │  Email missing   │   SMTP config    │     Test email    │  Fix SMTP relay  │ After 2 retries  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SCG Diagnostics page shows green/red per array · CloudIQ portal shows last telemetry time│
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCG Diagnostics = SCG web UI page showing cloud connectivity status and per-array collection state │
│    System Status   = CloudIQ portal banner showing cloud-side outages or maintenance windows          │
│    Stale scores    = Health score not refreshed in >2 h; usually indicates SCG connectivity loss      │
│    Cred failure    = SCG cannot log into array; verify array admin password has not been rotated      │
│    Telemetry lag   = Data arriving late; check SCG clock skew (NTP), proxy latency, load              │
│    False positive  = Alert firing on a healthy condition; tune threshold or add suppression rule      │
│    Alert storm     = Burst of alerts from a single event; suppress root alert; dismiss children       │
│    SMTP relay      = Email server used by CloudIQ to send report and alert notifications              │
│    Export fails    = Large export times out; reduce date range; try CSV instead of PDF                │
│    Dashboard stale = Cached view; force refresh or log out and back in to clear cache                 │
│    Cert validation = SCG verifies Dell cloud cert chain; fails if clock skew or proxy MITM            │
│    SR escalation   = Open Dell Service Request if issue not resolved by standard troubleshooting      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
