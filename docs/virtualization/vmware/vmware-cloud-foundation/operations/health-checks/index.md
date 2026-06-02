# VCF — Health Checks


<div class="kb-summary">
Health Checks reference covering Common Operational Issues.
</div>

VCF Daily Health Check — Coverage Map
```text
┌─────────────────────────────────────────────────────┐
│  SDDC Manager                                       │
│  ├─ Dashboard: all domains green?                   │
│  ├─ Security → Certs: no expiry < 60 days?          │
│  ├─ LCM → Bundles: critical patches pending?        │
│  └─ Admin → Backup: last backup timestamp OK?       │
└──────────────────────┬──────────────────────────────┘
```
┌─────────────────────────────── VMware Cloud Foundation — Health Checks ───────────────────────────────┐
│                                                                                                       │
│  VCF health checks span SDDC Manager, all vCenters, NSX managers, vSAN clusters,                      │
│  and certificate validity across all workload and management domains.                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             SDDC Manager Health              │  │               Component Health              │   │
│   │         Dashboard: all green status          │  │           All vCenters: connected           │   │
│   │          Free pool: hosts available          │  │              NSX: all nodes UP              │   │
│   │            Backup: last run <24h             │  │              vSAN: health green             │   │
│   │         LCM: no upgrade in progress          │  │           Credentials: not expired          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SDDC Manager dashboard gives holistic view; drill into each domain for detail.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Certificate Health              │  │           Network & Storage Health          │   │
│   │          SDDC Mgr cert expiry >30d           │  │            vSAN: resync = 0 bytes           │   │
│   │            vCenter STS cert check            │  │              NSX: BGP/routes OK             │   │
│   │             NSX cert expiry >30d             │  │             MTU: vSAN test pass             │   │
│   │            Rotate before expiry!             │  │             Hosts: all connected            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All VCF components run as VMs on the management domain; SDDC Manager health                          │
│  depends on underlying ESXi hosts and vSAN datastore availability.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = checks aggregated health of all VCF components                                       │
│  LCM           = Lifecycle Manager; controls upgrade pipelines                                        │
│  Free pool     = unassigned hosts; availability affects domain growth                                 │
│  STS cert      = SSO Security Token Service cert; 2yr expiry                                          │
│  NSX cert      = NSX Manager and edge certs; auto-renew in 8.0+                                       │
│  Credentials   = SDDC Mgr manages passwords for all components                                        │
│  vSAN resync   = 0 bytes = no data movement in progress                                               │
│  BGP           = NSX routing protocol to physical network                                             │
│  MTU test      = vSAN jumbo frame validation across all hosts                                         │
│  Backup health = SDDC Mgr tracks last backup success timestamp                                        │
│  Rotate cert   = use SDDC Mgr to rotate certs >30d before expiry                                      │
│  Domain view   = per-domain health in SDDC Mgr Workload Domains tab                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
