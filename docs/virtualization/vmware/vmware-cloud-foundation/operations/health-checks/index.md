# VCF — Health Checks

```
VCF Daily Health Check — Coverage Map
┌─────────────────────────────────────────────────────┐
│  SDDC Manager                                       │
│  ├─ Dashboard: all domains green?                   │
│  ├─ Security → Certs: no expiry < 60 days?          │
│  ├─ LCM → Bundles: critical patches pending?        │
│  └─ Admin → Backup: last backup timestamp OK?       │
└──────────────────────┬──────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────────────┐
│ NSX Manager  │ │ vCenter  │ │ SDDC Manager          │
│              │ │ per WLD  │ │ appliance disk        │
│ Fabric/Nodes:│ │          │ │                       │
│ all Up?      │ │ Hosts:   │ │ df -h                 │
│              │ │ Connected│ │ Alert if /data > 80%  │
│ BGP peers:   │ │          │ │                       │
│ Established? │ │ vSAN:    │ │                       │
│              │ │ Skyline  │ │                       │
│ Transport    │ │ Health   │ │                       │
│ zones: OK?   │ │ green?   │ │                       │
└──────────────┘ └──────────┘ └──────────────────────┘
```

## Daily Health Check

**SDDC Manager:**

1. Dashboard — all workload domains show **Healthy**; no domains in Warning or Error state
2. Security → Certificates — no certificates expiring within 60 days
3. Lifecycle Management → Bundle Management — review available updates; note critical patches
4. Administration → Backup — confirm last successful backup timestamp

**NSX Manager:**

5. System → Fabric → Nodes — all transport nodes and edge nodes show **Up**
6. Networking → Tier-0 Gateways → BGP neighbours — all peers in **Established** state
7. System → Fabric → Transport Zones — all zones healthy

**vCenter (per workload domain):**

```powershell
# Check all hosts connected
Get-VMHost | Where-Object {$_.ConnectionState -ne "Connected"} | Select Name, ConnectionState

# Check for snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)} |
  Select VM, Name, Created, SizeGB

# vSAN Skyline Health — check for critical (red) alerts in vCenter → vSAN Cluster → Skyline Health
```

**SDDC Manager appliance disk:**

```bash
ssh vcf@<sddc-manager-ip>
df -h
# Alert if /data or / is above 80%
```

## Common Operational Issues

| Symptom | Where to Check | Action |
|---|---|---|
| Workload domain shows Warning | SDDC Manager → Dashboard | Review component health; expand domain view |
| NSX transport node degraded | NSX Manager → System → Fabric → Nodes | Check NSX agent on affected ESXi host |
| Certificate expiry warning | SDDC Manager → Security → Certificates | Use Certificate Management to renew |
| LCM upgrade stuck | SDDC Manager → Administration → Tasks | Review task details; check `/var/log/vmware/vcf/sddc-manager/` |
| SDDC Manager disk full | SSH → `df -h` | Archive old LCM bundle downloads from `/nfs/vmware/vcf/nfs-mount/` |
| BGP peer down | NSX Manager → Networking → Tier-0 → BGP | Check edge node uptime; verify upstream router config |
