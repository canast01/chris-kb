# SRDF/A — Hardening

> Part of the [SRDF/A](../../) reference.

---

## Network Port Requirements

| Port | Protocol | Purpose |
|---|---|---|
| 3260 | TCP | iSCSI (if used for management) |
| 5000 | TCP | Solutions Enabler SYMAPI |
| 443 | HTTPS | Unisphere REST API |
| Custom | FCIP | SRDF replication over IP (configurable per director) |

Restrict FCIP and Solutions Enabler API ports to array management IPs only using firewall ACLs.

---

## Audit Logging

All SRDF operations generate entries in the PowerMax audit log:

```bash
symevent list -sid <SID> -type rdf         # List all RDF events
symevent show -sid <SID> -event_id <ID>    # Detail on specific event
```

Forward to SIEM via syslog:
- Configure Unisphere: Settings → Notifications → Syslog → add SIEM IP, port 514 (UDP) or 6514 (TLS)
- Alert on event types: `SRDF Split`, `SRDF Failover`, `SRDF Suspend`, `SRDF Establish`
