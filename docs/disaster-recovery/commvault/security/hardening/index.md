# Commvault — Hardening


<div class="kb-summary">
Hardening reference covering Network Security, Security Hardening Checklist.
</div>

```
┌─────────────────────────── Commvault Security Hardening — OS, Network, App ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      OS Hardening     │   Network Hardening   │     App Hardening     │       Monitoring      │   │
│   │    CIS Benchmark L1   │      Backup VLAN      │   Disable HTTP (80)   │      SIEM syslog      │   │
│   │  Remove unused roles  │   Host firewall ACLs  │     TLS 1.2+ only     │     Audit log ship    │   │
│   │   Disable guest/anon  │     Port whitelist    │  Disable weak ciphers │     Alert on fail     │   │
│   │  Patching: 30-day SLA │   No direct internet  │   Passphrase policy   │     Quarterly scan    │   │
│   │   AV exclusions set   │    Jump host access   │    FIPS 140-2 mode    │    Vuln disclosure    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CommServe and MAs are high-value targets; treat them as Tier 0 critical infrastructure             │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Port Hardening — Required Ports Only                             │   │
│   │          CommServe inbound: 8400 (clients), 8401 (GUI/console), 443 (Command Center)          │   │
│   │             MediaAgent inbound: 8403 (data tunnel from clients), NDMP 10000 (NAS)             │   │
│   │              SQL Server: 1433 inbound from CommServe host only (not from network)             │   │
│   │                Block all other inbound; allow CS→MA 8403 outbound for push jobs               │   │
│   │           iDRAC/iLO management: separate OOB network, no IP routing from backup VLAN          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe physical server preferred; not shared with production workloads                            │
│  Dedicated backup VLAN with ACLs; firewall between production and backup VLANs                        │
│  Out-of-band access via iDRAC/iLO on separate management network                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CIS Benchmark  = Center for Internet Security hardening guide; Level 1 = baseline                    │
│  Backup VLAN    = Isolated network segment for backup traffic; separate from prod                     │
│  AV Exclusions  = Antivirus must exclude CV DDB path and library mount paths                          │
│  FIPS Mode      = CommServe/MA configured to use only FIPS-validated crypto libs                      │
│  Weak Ciphers   = TLS_RSA_WITH_3DES, RC4, MD5; disable via OS TLS configuration                       │
│  Jump Host      = Bastion server required to access CommServe console; no direct RDP                  │
│  Tier 0         = Most critical infrastructure; same security tier as AD domain controllers           │
│  Port Whitelist = Firewall ACL allowing only required CV ports; deny-all default                      │
│  NDMP           = Network Data Management Protocol (port 10000); NAS backup protocol                  │
│  SIEM           = Security Information and Event Management; receives CV audit syslog                 │
│  Vuln Scan      = Quarterly Nessus/Qualys scan of CommServe and MA servers                            │
│  OOB Network    = Out-of-band management network for iDRAC/iLO; isolated from data                    │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Network Security

| Port | Purpose | Restriction |
|---|---|---|
| 8400/TCP | CommServe communication | Restrict to admin management subnets |
| 8403/TCP | MediaAgent data movement | Allow from client subnets to MediaAgent IPs only |
| 443/HTTPS | Command Center web UI | Restrict to admin subnets |

## Security Hardening Checklist

- [ ] RBAC configured — all users assigned to roles via AD groups
- [ ] No shared admin credentials
- [ ] Encryption enabled for all regulated data policies
- [ ] DDB encryption enabled
- [ ] 2FA enabled for Command Center
- [ ] CommServe management ports (8400, 8403) firewall-restricted
- [ ] CyberArk integration active for service account passwords
- [ ] Audit log forwarded to SIEM; alerts configured
- [ ] CommServe OS and SQL Server on supported, patched versions
