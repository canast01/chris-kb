# Active Directory — Architecture Overview

## Forest and Domain Hierarchy

Active Directory is organised in a Forest → Domain → OU hierarchy:

```mermaid
graph TB
  FOREST["AD Forest\n(security boundary)"] --> ROOT["Forest Root Domain\ncorp.example.com"]
  ROOT --> DC1["DC-01 Site A\nPDC · RID · Infra Master"]
  ROOT --> DC2["DC-02 Site A\nGlobal Catalog"]
  ROOT -->|"AD replication"| DC3["DC-03 · DC-04\nSite B — replica DCs"]
  ROOT --> CHILD["Child Domain\ndivision.corp.example.com"]
  CHILD --> CDC["Child DC"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class DC1,DC2,DC3,CDC ctrl
  class FOREST,ROOT,CHILD mgmt
```

The forest is the ultimate security boundary — Kerberos trust does not cross forest boundaries by default. Child domains share the forest schema and global catalog but have separate administrative boundaries.


## Forest and Domain Topology

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                         AD Forest                                        │
  │                                                                          │
  │  ┌────────────────────────────────────────────────────────────────┐     │
  │  │  Forest Root Domain  (corp.example.com)                        │     │
  │  │  ┌────────────────────────────────────────────────────────┐   │     │
  │  │  │  Schema Master  Domain Naming Master  Global Catalogue  │   │     │
  │  │  └────────────────────────────────────────────────────────┘   │     │
  │  │                                                                │     │
  │  │  ┌─────────────────────┐  ┌─────────────────────────────┐    │     │
  │  │  │  DC-01 (Site A PDC) │  │  DC-02 (Site A)             │    │     │
  │  │  │  RID / PDC Emulator │  │  Global Catalogue           │    │     │
  │  │  │  Infra Master       │  │                             │    │     │
  │  │  └────────┬────────────┘  └─────────────────────────────┘    │     │
  │  │           │ AD replication (inter-site: IP / SMTP)            │     │
  │  │  ┌────────▼──────────────────────────────────────────────┐   │     │
  │  │  │  DC-03 (Site B)  DC-04 (Site B)  — replica DCs        │   │     │
  │  │  └────────────────────────────────────────────────────────┘   │     │
  │  └────────────────────────────────────────────────────────────────┘     │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Child Domains (if used)                                        │    │
  │  │  eu.corp.example.com    apac.corp.example.com                   │    │
  │  │  (trust is automatic within forest — transitive two-way)        │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────┘
  DNS: every DC is also a DNS server; AD relies entirely on DNS SRV records
```

## Core Components

| Component | Role |
|---|---|
| Forest Root Domain | Schema master, Enterprise Admins, trust anchor |
| Regional Domains | Administrative boundary per region or business unit |
| Domain Controller (DC) | Hosts AD database (NTDS.DIT), DNS, KDC, SYSVOL |
| Global Catalog (GC) | Partial attribute replica + universal group membership cache |
| FSMO Roles | Five single-master operations (see below) |
| Sites & Site Links | Control replication topology and DC/KDC selection |
| SYSVOL | Shared folder replicated via DFSR; holds GPO templates and logon scripts |

## FSMO Role Placement

| FSMO Role | Scope | Recommended DC |
|---|---|---|
| Schema Master | Forest-wide | Forest root DC 1 |
| Domain Naming Master | Forest-wide | Forest root DC 1 |
| PDC Emulator | Per domain | Most capable DC; close to users (time source) |
| RID Master | Per domain | Same site as PDC Emulator preferred |
| Infrastructure Master | Per domain | Not a GC DC (if single-domain, can be GC) |

Verify current FSMO holders:
```powershell
netdom query fsmo /domain:corp.local
# Or:
Get-ADDomain | Select-Object InfrastructureMaster, RIDMaster, PDCEmulator
Get-ADForest | Select-Object SchemaMaster, DomainNamingMaster
```

## Key Services and Ports

| Service | Port | Protocol | Purpose |
|---|---|---|---|
| LDAP | 389 | TCP/UDP | Directory queries |
| LDAPS | 636 | TCP | Encrypted directory queries |
| Global Catalog | 3268 | TCP | Universal group membership |
| Global Catalog SSL | 3269 | TCP | Encrypted GC queries |
| Kerberos | 88 | TCP/UDP | Authentication tickets |
| DNS | 53 | TCP/UDP | Name resolution (AD-integrated DNS) |
| RPC (replication) | 135 + dynamic | TCP | DC-to-DC replication |
| SMB (SYSVOL) | 445 | TCP | SYSVOL/DFSR replication |
| WinRM | 5985/5986 | TCP | Remote management |

## Replication Topology (KCC-Generated)

```mermaid
graph TD
    siteA["Site A — London"]
    siteB["Site B — New York"]
    siteC["Site C — Singapore"]

    dc01["DC-01\nPDC Emulator\nRID Master"]
    dc02["DC-02\nGlobal Catalog"]
    dc03["DC-03\nSite A replica"]
    dc04["DC-04\nGlobal Catalog"]
    dc05["DC-05\nSite B replica"]
    dc06["DC-06\nSite C GC"]

    siteA --> dc01
    siteA --> dc02
    siteA --> dc03
    siteB --> dc04
    siteB --> dc05
    siteC --> dc06

    dc01 <-->|"intra-site\nRPC — frequent"| dc02
    dc01 <-->|"intra-site\nRPC — frequent"| dc03
    dc04 <-->|"intra-site"| dc05

    dc01 <-->|"inter-site link\nscheduled interval"| dc04
    dc01 <-->|"inter-site link\nscheduled interval"| dc06
    dc04 <-->|"inter-site link"| dc06
```

## Sites and Replication

Sites define physical network boundaries for efficient replication and logon:

```powershell
# List sites
Get-ADReplicationSite -Filter *

# List site links
Get-ADReplicationSiteLink -Filter *

# Check replication health
repadmin /showrepl
repadmin /replsummary   # Summary of replication success/failure
dcdiag /test:replications /v
```

AD replicates via multi-master within a site (frequent, fast) and between sites via site links (scheduled, based on link interval).

## DC High Availability Design

Minimum two Domain Controllers per site:
- DC1: PDC Emulator, RID Master for the site's domain
- DC2: Infrastructure Master, GC (if only one domain — GC on both)
- Both DCs act as DNS servers for the site

In the event DC1 fails: DC2 handles all authentication and DNS. FSMO roles should be seized only if DC1 cannot be restored within 24 hours.

## Active Directory Database

The AD database file is `NTDS.DIT`:
```
Location: C:\Windows\NTDS\NTDS.DIT
Log files: C:\Windows\NTDS\*.log (EDB transaction logs)
SYSVOL: C:\Windows\SYSVOL\sysvol\<domain>\
```

Back up via Windows Server Backup (System State backup) or bare-metal backup:
```powershell
# System State backup includes NTDS.DIT
wbadmin start systemstatebackup -backupTarget:D:
```

## Kerberos Authentication Sequence

```mermaid
sequenceDiagram
    participant client as Client
    participant kdc as KDC (Domain Controller)
    participant svc as Application Server

    client->>kdc: AS-REQ (username + encrypted timestamp)
    kdc-->>client: AS-REP — TGT (encrypted with krbtgt key)
    note over client: Client caches TGT (valid 10 hours)
    client->>kdc: TGS-REQ (TGT + service SPN)
    kdc-->>client: TGS-REP — Service Ticket (encrypted with service key)
    client->>svc: AP-REQ (Service Ticket + authenticator)
    svc-->>client: AP-REP (mutual auth confirmation)
    note over client,svc: Secure session established
```

## Kerberos Authentication Flow

```
  Client                  KDC (DC)                  Application Server
    │                        │                               │
    │── AS-REQ (username) ──►│                               │
    │   (pre-auth: enc TS)   │                               │
    │◄── AS-REP (TGT) ───────│                               │
    │    enc with krbtgt key  │                               │
    │                        │                               │
    │── TGS-REQ (TGT) ──────►│                               │
    │   (request: service SPN)│                               │
    │◄── TGS-REP (ST) ───────│                               │
    │    enc with svc key     │                               │
    │                        │                               │
    │── AP-REQ (ST + auth) ──────────────────────────────►  │
    │   (mutual auth option)  │                               │
    │◄── AP-REP ─────────────────────────────────────────── │
    │                        │                               │
    │           [Session established — Kerberos ticket valid]│
    │                        │                               │
    │── Resource Access ─────────────────────────────────►  │
    │◄── Response ────────────────────────────────────────── │
```

## LDAP Bind Flow

```
  Client                         Active Directory (LDAP)
    │                                      │
    │── TCP SYN ──────────────────────────►│  (port 389 / 636)
    │◄── TCP SYN-ACK ─────────────────────│
    │── LDAP Bind Request (DN + password) ►│
    │◄── Bind Response (success / error) ──│
    │                                      │
    │── Search Request (filter + scope) ──►│
    │◄── Search Entries ───────────────────│
    │◄── Search Done ──────────────────────│
    │                                      │
    │── Unbind ───────────────────────────►│
    │── TCP FIN ──────────────────────────►│
```

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
