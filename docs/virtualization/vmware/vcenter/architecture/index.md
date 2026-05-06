# vCenter Architecture

## Deployment Model

vCenter Server is delivered as the **vCenter Server Appliance (VCSA)** — a Photon OS-based virtual appliance. Since vCenter 7.0, the Platform Services Controller (PSC) is embedded directly in the appliance (external PSC is deprecated). The embedded database is PostgreSQL.

A single VCSA manages the full vSphere inventory: datacenters, clusters, hosts, VMs, datastores, networks, and policies.

## Core Components

| Component | Role |
|---|---|
| vCenter Server | Core management service — inventory, scheduling, HA/DRS orchestration |
| Embedded PSC | Authentication, SSO, certificate authority (VMCA), licensing |
| PostgreSQL (embedded) | vCenter inventory and events database |
| vSphere Client (HTML5) | Primary management UI — `https://<vcenter>/ui` |
| vSphere API | REST and SOAP API endpoints for automation |
| Update Manager (vLCM) | Patch and lifecycle management for ESXi hosts |

## vCenter HA

vCenter HA (VCHA) provides active/passive failover for the VCSA itself. It requires three nodes:

- **Active** — serves all management traffic
- **Passive** — hot standby, continuously replicates from active
- **Witness** — tie-breaker for split-brain scenarios; can be a small VM (2 vCPU / 1 GB RAM)

Shared storage is **not** required — replication is network-based over a dedicated HA network (typically a /24). Failover is automatic on active node failure; RPO is near-zero, RTO is typically under 60 seconds.

```
Active VCSA ──── HA network ────▶ Passive VCSA
       │                               │
       └──────── Witness VCSA ─────────┘
```

## Key Ports and Connectivity

| Port | Protocol | Purpose |
|---|---|---|
| 443 | TCP | vSphere Client, API, SSO |
| 902 | TCP/UDP | ESXi host agent (heartbeat) |
| 9443 | TCP | vSphere Web Client (legacy, ≤ vSphere 6.7) |
| 5480 | TCP | VCSA VAMI (appliance management) |
| 8443 | TCP | vCenter HA replication |
| 389 | TCP | LDAP (SSO) |
| 636 | TCP | LDAPS (SSO) |

All ESXi hosts must reach vCenter on 443 and vCenter must reach ESXi on 902.

## Sizing

| Deployment Size | Max Hosts | Max VMs | vCPU | RAM | Disk (OS + DB) |
|---|---|---|---|---|---|
| Tiny (lab) | 10 | 100 | 2 | 12 GB | 415 GB |
| Small | 100 | 1,000 | 4 | 19 GB | 480 GB |
| Medium | 400 | 4,000 | 8 | 28 GB | 700 GB |
| Large | 1,000 | 10,000 | 16 | 37 GB | 1,065 GB |
| X-Large | 2,000 | 35,000 | 24 | 56 GB | 1,805 GB |

Sizing is set at deploy time and can be changed by modifying vCPU/RAM after deployment (requires reboot). Disk partitions can be expanded online.

## Logical Hierarchy

```
vCenter Server
└── Datacenter (DC-<site>)
    ├── Cluster (CL-<site>-<function>)
    │   ├── ESXi Host (esxi-01.<domain>)
    │   │   └── VMs
    │   └── vSAN Datastore / VMFS / NFS
    └── Standalone Host (uncommon in production)
```

Resource pools, vSphere tags, and content libraries are vCenter-level constructs applied within this hierarchy.

## High-Level Failure Domains

- **vCenter failure** — hosts and VMs continue running; HA/DRS stop working; no management plane until vCenter recovers
- **PSC/SSO failure** — authentication failures; vSphere Client inaccessible; hosts in lockdown mode become inaccessible via API
- **Database failure** — vCenter services crash; restore from last backup required
- **VCHA passive failure** — no impact to active; witness still provides quorum; repair passive before next failover test
