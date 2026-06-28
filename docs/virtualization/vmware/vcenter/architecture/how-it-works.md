---
tags:
  - architecture
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter — How It Works


<div class="kb-summary">
How It Works reference covering Deployment Model, Core Services, Main Dependencies, vCenter HA (VCHA), Service Startup Order and 7 more sections.

*Applies to: vSphere 7.x · 8.x*
</div>
![vCenter — How It Works](../../../../assets/virtualization-vmware-vcenter-architecture-how-it-works.svg)

```d2
direction: right

vcenter: vCenter Server (VCSA) {
  shape: hexagon
}

clients: vSphere Clients {shape: person}
ad: Active Directory {shape: rectangle}
dns: DNS {shape: rectangle}
ntp: NTP {shape: rectangle}
esxi: ESXi Hosts {shape: rectangle}
vsan: vSAN Datastore {shape: cylinder}
nsx: NSX Manager {shape: rectangle}
backup: Backup Target {shape: cylinder}

clients -> vcenter: HTTPS 443
vcenter -> ad: LDAP/S 389·636
vcenter -> dns: UDP 53
vcenter -> ntp: UDP 123
vcenter -> esxi: TCP 443·902
esxi -> vsan: vSAN traffic
vcenter -> nsx: REST API 443
vcenter -> backup: SCP·SFTP
```

## Deployment Model

vCenter Server is delivered as the **vCenter Server Appliance (VCSA)** — a Photon OS-based virtual appliance. Since vCenter 7.0, the Platform Services Controller (PSC) is embedded directly in the appliance (external PSC is deprecated). The embedded database is PostgreSQL.

A single VCSA manages the full vSphere inventory: datacenters, clusters, hosts, VMs, datastores, networks, and policies.

## Core Services

| Service | Description |
|---|---|
| vCenter Server Appliance (VCSA) | The main management appliance; Photon OS-based |
| vpxd | Core vCenter daemon — inventory, scheduling, HA/DRS orchestration |
| vSphere Client | HTML5 web UI at `https://<vcenter>/ui` |
| Embedded PSC / SSO | Authentication, SSO domain, VMCA certificate authority, licensing |
| vPostgres (PostgreSQL) | Embedded database — vCenter inventory, events, tasks |
| vAPI Endpoint | Modern REST API at `https://<vcenter>/api` |
| Lookup Service | Service registry for all vCenter components |
| Certificate Manager (VMCA) | Issues and renews certificates for VCSA and ESXi hosts |
| Backup Scheduler | Built-in file-based backup via VAMI |

## Main Dependencies

| Dependency | Notes |
|---|---|
| DNS | Forward and reverse resolution required for VCSA FQDN and all ESXi hosts |
| NTP | Time sync mandatory; skew > 5 minutes breaks Kerberos and SSO |
| Authentication Source | AD/LDAP identity source for user authentication |
| Management Network | VCSA must be reachable from all ESXi hosts on port 443; hosts reachable on 902 |
| Storage | VCSA runs as a VM; requires reliable datastore access |
| Certificate Trust | All services use TLS; expired certificates cascade into auth failures |

---

## vCenter HA (VCHA)

VCHA provides active/passive failover for the VCSA itself. Three nodes required:

- **Active** — serves all management traffic
- **Passive** — hot standby, continuously replicates from active
- **Witness** — tie-breaker for split-brain; can be a small VM (2 vCPU / 1 GB RAM)

Shared storage is **not** required — replication is network-based over a dedicated HA network. Failover is automatic on active node failure; RPO is near-zero, RTO is typically under 60 seconds.

```mermaid
graph LR
    clients["vSphere Clients\n& API consumers"]
    active["Active VCSA\n(serves all traffic)"]
    passive["Passive VCSA\n(hot standby)"]
    witness["Witness VCSA\n(2 vCPU / 1 GB — tie-breaker)"]

    clients -->|"port 443"| active
    active -->|"continuous replication\n(HA network)"| passive
    active -.->|"heartbeat"| witness
    passive -.->|"heartbeat"| witness

    classDef active fill:#15803d,stroke:#166534,color:#fff
    classDef standby fill:#b45309,stroke:#92400e,color:#fff
    classDef witness fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef client fill:#2563eb,stroke:#1d4ed8,color:#fff

    class active active
    class passive standby
    class witness witness
    class clients client
```


---

## Service Startup Order

Services must start in the correct dependency order or vpxd will fail to initialise:

```mermaid
graph TD
    vpostgres["vmware-vpostgres\n(PostgreSQL database)"]
    stsd["vmware-stsd\n(SSO token service)"]
    idmd["vmware-sts-idmd\n(identity management)"]
    vpxd["vpxd\n(core vCenter daemon)"]
    ui["vsphere-ui\n(HTML5 Client)"]
    eam["vmware-eam\n(ESX Agent Manager)"]

    vpostgres --> stsd
    stsd --> idmd
    idmd --> vpxd
    vpxd --> ui
    vpxd --> eam

    classDef db fill:#1d4ed8,stroke:#1e40af,color:#fff
    classDef sso fill:#7c3aed,stroke:#6d28d9,color:#fff
    classDef core fill:#b45309,stroke:#92400e,color:#fff
    classDef svc fill:#15803d,stroke:#166534,color:#fff

    class vpostgres db
    class stsd,idmd sso
    class vpxd core
    class ui,eam svc
```

```bash
# Manual restart in dependency order
service-control --stop --all
service-control --start vmware-vpostgres
service-control --start vmware-stsd
service-control --start vmware-sts-idmd
service-control --start vpxd
service-control --start --all

# Verify
service-control --status --all
```

---

## Sizing

| Deployment Size | Max Hosts | Max VMs | vCPU | RAM | Disk (OS + DB) |
|---|---|---|---|---|---|
| Tiny (lab) | 10 | 100 | 2 | 12 GB | 415 GB |
| Small | 100 | 1,000 | 4 | 19 GB | 480 GB |
| Medium | 400 | 4,000 | 8 | 28 GB | 700 GB |
| Large | 1,000 | 10,000 | 16 | 37 GB | 1,065 GB |
| X-Large | 2,000 | 35,000 | 24 | 56 GB | 1,805 GB |

Sizing is set at deploy time and can be changed by modifying vCPU/RAM after deployment (requires reboot). Disk partitions can be expanded online.

```vegalite
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": "vCenter Sizing — Maximum VMs by Deployment Size",
  "width": 400,
  "height": 200,
  "data": {
    "values": [
      {"size": "Tiny",    "max_vms": 100,   "max_hosts": 10},
      {"size": "Small",   "max_vms": 1000,  "max_hosts": 100},
      {"size": "Medium",  "max_vms": 4000,  "max_hosts": 400},
      {"size": "Large",   "max_vms": 10000, "max_hosts": 1000},
      {"size": "X-Large", "max_vms": 35000, "max_hosts": 2000}
    ]
  },
  "layer": [
    {
      "mark": {"type": "bar", "tooltip": true},
      "encoding": {
        "x": {
          "field": "size",
          "type": "ordinal",
          "sort": ["Tiny", "Small", "Medium", "Large", "X-Large"],
          "title": "Deployment Size"
        },
        "y": {"field": "max_vms", "type": "quantitative", "title": "Max VMs"},
        "color": {
          "field": "size",
          "type": "nominal",
          "legend": null,
          "scale": {"range": ["#64b5f6","#42a5f5","#2196f3","#1e88e5","#1565c0"]}
        }
      }
    },
    {
      "mark": {"type": "text", "dy": -6, "fontSize": 11},
      "encoding": {
        "x": {
          "field": "size",
          "type": "ordinal",
          "sort": ["Tiny", "Small", "Medium", "Large", "X-Large"]
        },
        "y": {"field": "max_vms", "type": "quantitative"},
        "text": {"field": "max_vms", "type": "quantitative"}
      }
    }
  ]
}
```

---

## Failure Domains

| Failure | Impact | Recovery |
|---|---|---|
| vCenter failure | Hosts and VMs continue running; HA/DRS stop; no management plane | Restore VCSA from backup or VCHA failover |
| PSC/SSO failure | Authentication failures; vSphere Client inaccessible | Restart SSO services; fix identity source |
| Database failure | vCenter services crash | Restore from last backup |
| VCHA passive failure | No impact to active; witness still provides quorum | Repair passive before next failover |
| Partition full (`/storage/log`) | vCenter services may crash or stop logging | Free space; rotate/archive logs |

---

## Ports and Protocols

| Use | Protocol | Port |
|---|---|---|
| vSphere Client / API | HTTPS | 443 |
| ESXi host agent heartbeat | TCP/UDP | 902 |
| VCSA VAMI (appliance management) | HTTPS | 5480 |
| vCenter HA replication | TCP | 8443 |
| LDAP | TCP | 389 |
| LDAPS | TCP | 636 |
| Syslog | UDP/TCP | 514 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

---

## Key Logs

| Component | Log Path |
|---|---|
| vpxd (core service) | `/var/log/vmware/vpxd/vpxd.log` |
| vSphere Client | `/var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log` |
| SSO / identity | `/var/log/vmware/sso/vmware-sts-idmd.log` |
| SSO admin server | `/var/log/vmware/sso/ssoAdminServer.log` |
| VAMI | `/var/log/vmware/applmgmt/applmgmt.log` |
| Upgrade / patch | `/var/log/vmware/applmgmt/software-packages.log` |
| Certificate manager | `/var/log/vmware/vmcad/certificate-manager.log` |
| Postgres DB | `/var/log/vmware/vpostgres/postgresql-*.log` |

---

## Useful Commands

```bash
# Service status
service-control --status --all

# Disk usage
df -h

# VECS certificate store — check expiry
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT --text | grep -E "Alias|Not After"

# SSO domain info
/usr/lib/vmware-vmafd/bin/vmafd-cli get-domain-name --server-name localhost

# System resource usage
top
vmstat 1 5

# Network — open listening ports
ss -tlnp

# Photon OS version
cat /etc/photon-release
```

---

## Database Operations

```bash
# Connect to embedded PostgreSQL
/opt/vmware/vpostgres/current/bin/psql -U postgres -d VCDB

# Inside psql
\dt                                          # list tables
SELECT pg_size_pretty(pg_database_size('VCDB'));  # check DB size
SELECT COUNT(*) FROM vc_event;               # verify DB is intact
\q
```

Do not modify the vCenter database directly unless directed by VMware Support.

---

## REST API Quick Reference

```bash
# Authenticate
TOKEN=$(curl -sk -u 'administrator@vsphere.local:<password>' \
    -X POST https://vcenter.example.local/api/session | tr -d '"')

# Host inventory
curl -sk -H "vmware-api-session-id: $TOKEN" \
    "https://vcenter.example.local/api/vcenter/host" | python3 -m json.tool

# VM inventory
curl -sk -H "vmware-api-session-id: $TOKEN" \
    "https://vcenter.example.local/api/vcenter/vm" | python3 -m json.tool

# System health
curl -sk -H "vmware-api-session-id: $TOKEN" \
    "https://vcenter.example.local/api/vcenter/health/system"

# Delete session
curl -sk -H "vmware-api-session-id: $TOKEN" \
    -X DELETE https://vcenter.example.local/api/session
```

Swagger UI: `https://<vcenter>/apiexplorer`


---

## vCenter HA (VCHA) — Topology


---

## Identity Federation (vSphere 8)

vSphere 8 supports Active Directory Federation Services (AD FS) as an external identity provider via OIDC, replacing the older LDAP bind model. The flow below shows how vSphere Client authenticates a user through an external IdP.

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor Admin
participant "vSphere Client" as UI
participant "vCenter SSO\n(STSD)" as SSO
participant "AD FS / IdP\n(OIDC)" as IDP
participant "Active Directory" as AD

Admin -> UI: Open https://vcenter/ui
UI -> SSO: GET /ui — unauthenticated
SSO --> UI: Redirect → IdP authorization endpoint
UI -> IDP: Authorization request (OIDC code flow)
IDP --> Admin: IdP login page
Admin -> IDP: Credentials (AD UPN format)
IDP -> AD: Kerberos / LDAP credential validation
AD --> IDP: Auth OK + group membership
IDP --> UI: Authorization code
UI -> SSO: Exchange code → SSO token
SSO -> IDP: Token introspection / JWKS verification
IDP --> SSO: ID token claims (UPN, groups)
SSO --> UI: vCenter session established
UI --> Admin: vSphere Client dashboard (roles from group mapping)
@enduml
```

---

## VM Encryption — Key Hierarchy


---

## Content Library — Publish & Subscribe



---

## Resource Pools — Shares, Limits & Reservations



---

## vMotion Types — Comparison



---

## DRS — Placement & Balancing Logic



## See also

- [vCenter — Design Standards](../design-standards/)
- [vCenter — Deploy](../deploy/)
- [vCenter — Integrations](../integrations/)
