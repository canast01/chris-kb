# SRDF/S — Hardening

```text
┌───────────────────────────────────────── SRDF/S — Hardening ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  SRDF/S — Hardening Checklist                                 │   │
│   │               [ ] Disable default/admin accounts; create named admin accounts only            │   │
│   │                   [ ] Enable MFA for all interactive logins via IdP / SAML SSO                │   │
│   │     [ ] Restrict management port (Dark fiber FC (< 5 ms RTT)) to jump host / management VLAN  │   │
│   │               [ ] Enable audit logging and forward to SIEM (syslog, TLS port 6514)            │   │
│   │                 [ ] Apply all security patches within 30 days of vendor release               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Network Hardening                                       │   │
│   │               [ ] Separate backup VLAN — no direct production host access to repo             │   │
│   │    [ ] Firewall: allow only Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC · 9443 (Unisphere) │   │
│   │                  [ ] Disable unused ports and protocols on management interface               │   │
│   │              [ ] Immutable repository: enable WORM or object lock on backup target            │   │
│   │                 [ ] Encryption in transit: disable TLS 1.0/1.1; enforce TLS 1.2+              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [SRDF/S Security](../index.md) reference.

---

## Management API Security

The Unisphere REST API should be secured:

- Enable HTTPS only (disable HTTP on port 8080)
- Use client certificate authentication for service accounts
- Scope API accounts to minimum required capabilities
- Rotate service account certificates annually

Verify TLS configuration:
```bash
curl -k https://<unisphere>:8443/univmax/restapi/system/version
# Production systems should use trusted CA cert (remove -k flag)
```

---

## Operational Hardening Checklist

| Item | Guidance |
|---|---|
| SYMCLI confirmation prompts | Set `SYMCLI_CONFIRM=prompt` on all production SE hosts |
| Break-glass account for full resync | Restrict `symrdf establish -full` to a named break-glass account only |
| Two-person rule for failover | All production SRDF failovers require peer approval before execution |
| Monitoring accounts | Never assign `StorageAdmin` to automated monitoring or backup accounts |
| SRDF zones | Hard-zone SRDF director ports; no other initiators/targets in SRDF zones |
| API HTTP | Disable HTTP on port 8080; enforce HTTPS only on Unisphere |
| Audit log forwarding | Forward SRDF events to SIEM via Unisphere syslog integration |
| Certificate rotation | Rotate service account certificates annually |
