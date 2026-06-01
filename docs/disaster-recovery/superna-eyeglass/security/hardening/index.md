# Superna Eyeglass — Hardening


<div class="kb-summary">
Hardening reference covering Audit Log Forwarding, Appliance Patching.
</div>

```
┌──────────────────────────────────── Superna Eyeglass — Hardening ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                             Superna Eyeglass — Hardening Checklist                            │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │       [ ] Restrict management port (443 (Eyeglass web UI)) to jump host / management VLAN     │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │        [ ] Firewall: allow 443 (web UI) · 8080 (REST API) · 8116 (Isilon/PowerScale mgmt)     │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ESXi VM (Eyeglass appliance) · PowerScale cluster pair (production + DR) · SyncIQ replication link   │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass      = Superna Eyeglass; software appliance for NAS DR and ransomware protection            │
│  RAPA          = Ransomware Protection with Automated Response; detects and quarantines threats       │
│  SyncIQ        = PowerScale built-in replication; Eyeglass monitors and orchestrates policies         │
│  DFS-N         = Windows Distributed File System Namespace; Eyeglass automates failover of DFS        │
│  Failover      = Eyeglass-orchestrated shift of NAS access from production to DR cluster              │
│  Failback      = reversing failover; Eyeglass re-syncs DR changes back and cuts back to product       │
│  Quota Sync    = Eyeglass replicates SmartQuotas from source to DR to preserve user limits            │
│  Export Sync   = NFS exports and SMB shares replicated so clients can reconnect at DR site            │
│  Quarantine    = RAPA isolation of suspect directory; blocks writes, alerts ops team                  │
│  Shadow Copy   = Eyeglass exposes PowerScale snapshots as Windows Previous Versions for NFS sha       │
│  Runbook       = Eyeglass DR Assistant guided checklist for pre-checks, failover, and validation      │
│  igls          = Eyeglass CLI; used for status, sync, DR, and RAPA operations                         │
│  SmartConnect  = PowerScale DNS load balancing; failover changes SmartConnect zone delegation         │
│  Configuration = shares, exports, quotas, NFS aliases; Eyeglass syncs these between clusters          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
| Control | Detail |
|---|---|
| Audit log | All failover and configuration events logged; forward to SIEM |
| Appliance hardening | Disable unused services; keep appliance patched to current release |
| Service account rotation | Eyeglass service account credentials rotated every 90 days (coordinate with CyberArk policy) |

## Audit Log Forwarding

All failover events are recorded in the Eyeglass audit log. Forward the audit log to a SIEM:

1. Eyeglass Admin UI: Configuration → Syslog
2. Enter SIEM IP, port 514 (UDP) or 6514 (TLS)

Alert in SIEM on:
- Failover initiated (any event)
- DR readiness score < 100% for > 15 minutes
- Eyeglass appliance unreachable

## Appliance Patching

- Keep the Eyeglass appliance updated to the current release — Superna releases patches that address security vulnerabilities in the appliance OS and application stack
- Disable any unused services on the Eyeglass appliance via the Admin UI
- Verify the appliance VM guest OS is on the Superna supported OS list (Admin UI → System Info)
