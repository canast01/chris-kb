# SRM Security — Access Control

## vCenter RBAC for DR Operators

Define a dedicated `DR-Operator` role in vCenter with only the privileges required for SRM operations:

```yaml
Privileges to include:
  Site Recovery Manager:
    - Site Recovery.Manage
    - Site Recovery.Test
    - Site Recovery.Recovery
  Datastore:
    - Datastore.AllocateSpace
  Network:
    - Network.Assign (for network customisation)
  Virtual Machine:
    - Virtual Machine.Provisioning.* (for recovery)
```
┌──────────────────────────────────────── SRM — Access Control ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 SRM — RBAC and Access Control                                 │   │
│   │     Auth: vCenter SSO / AD integration; SRM admin role; site-pairing certificate exchange     │   │
│   │             Principle of least privilege: each role gets only required permissions            │   │
│   │              Service accounts: dedicated, non-interactive; rotation every 90 days             │   │
│   │               Emergency break-glass: documented, monitored, time-limited access               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   │       Role       │   Access Level   │    Typical User   │   Review Freq    │    Granted By    │   │
│   │      Admin       │ Full config/ops  │   Sr Backup Eng   │    Quarterly     │  Security team   │   │
│   │     Operator     │ Start/stop jobs  │     Backup Eng    │    Quarterly     │    Team lead     │   │
│   │     Monitor      │  Read-only view  │      NOC / L1     │    Quarterly     │    Team lead     │   │
│   │   Service Acct   │  API / headless  │     Automation    │   Per rotation   │  Security team   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two vCenter instances (protected + recovery site) · SRA installed on SRM server · Array replication l│
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRM           = Site Recovery Manager; VMware product for DR orchestration and testing               │
│  SRA           = Storage Replication Adapter; plugin linking SRM to specific array replication        │
│  Protection Group= logical grouping of VMs covered by a single replication consistency group          │
│  Recovery Plan = automated DR runbook: power-off order, datastore failover, IP customization          │
│  IP Customization= per-VM network settings applied at recovery site (different subnet/gateway)        │
│  Test Failover = non-disruptive plan validation using snapshot; production unaffected                 │
│  Planned Migration= graceful workload movement; VMs shutdown at protected, started at recovery        │
│  Emergency Failover= disaster scenario; VMs powered on from latest available replica                  │
│  Failback      = after recovery, re-protect VMs and migrate back to production site                   │
│  Re-protect    = reverses replication direction; DR site becomes new protected site                   │
│  Recovery Point= specific replication snapshot used for VM recovery; RPO = interval                   │
│  vCenter Pair  = SRM connection between two vCenter instances enables cross-site orchestration        │
│  Startup Priority= ordering within recovery plan; lower number = powers on first                      │
│  Site Pair     = trust relationship between protected and recovery SRM servers                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Local SRM Account (Break-Glass)

Access local SRM accounts at `https://<srm-appliance>:5480` (VAMI). Use only when vCenter SSO is unavailable. Rotate the local admin password after each use and store in a sealed break-glass envelope or PAM vault.

---

## Audit: Where SRM Logs DR Operations

SRM records all operations in multiple locations. Use these for compliance, change auditing, and post-DR review.

### Audit Log Locations

| Log Source | Location / Access Method | What It Records |
|---|---|---|
| SRM Events | vCenter UI → Site Recovery → Events tab | All SRM operations: plan runs, test start/end, errors |
| vCenter Tasks | vCenter UI → Tasks — filter by SRM task type | Task completion, duration, initiating user |
| Recovery History | SRM UI → Recovery Plans → select plan → History | Per-plan execution records with timestamps and outcomes |
| SRM appliance syslog | `/var/log/vmware/dr/` on SRM appliance (SSH) | Detailed server-side logs for troubleshooting |
| vCenter Audit Log | vCenter UI → Administration → Events → export | Includes RBAC changes affecting SRM roles |

### Key Commands for Log Review

```bash
# SSH to SRM appliance (admin or root)
ssh admin@<srm-appliance>

# View live SRM server log
tail -f /var/log/vmware/dr/dr.log

# Search for recovery plan execution events
grep -i "recovery plan\|RECOVERY_STARTED\|RECOVERY_COMPLETE\|RECOVERY_FAILED" \
  /var/log/vmware/dr/dr.log

# Search for authentication events (login/logout, permission denied)
grep -i "authentication\|login\|permission denied\|unauthorized" \
  /var/log/vmware/dr/dr.log | tail -50
```

### Exporting Recovery History for Compliance

In the SRM UI: **Recovery Plans** → select plan → **History** → **Export** — produces a CSV with plan name, start time, end time, result, and initiating user. Retain exports for audit evidence per your retention policy (typically 1–3 years for DR events).
