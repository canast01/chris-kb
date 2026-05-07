# Dell PowerMax

<div class="kb-grid kb-grid-15">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>HA topology, components, connectivity, and sizing.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Naming conventions, build baseline, and configuration checklist.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Command reference by category with syntax and examples.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for daily checks, health, incident triage, and validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic commands, log locations, and error codes.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>VMware, backup tools, monitoring, authentication, and API integration.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span>
</a>

<a class="kb-card" href="vendor-support/">
  <strong>Vendor Support</strong>
  <span>Opening a case, information to collect, support portal, and SLA tiers.</span>
</a>


<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Health check procedures and validation steps.</span>
</a>

<a class="kb-card" href="masking-views/">
  <strong>Masking Views</strong>
  <span>Masking Views notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="performance/">
  <strong>Performance</strong>
  <span>Performance monitoring, tuning, and baselining.</span>
</a>

<a class="kb-card" href="provisioning/">
  <strong>Provisioning</strong>
  <span>Provisioning notes, checks, commands, and references.</span>
</a>

<a class="kb-card" href="srdf/">
  <strong>Srdf</strong>
  <span>Srdf notes, checks, commands, and references.</span>
</a>
</div>

## PowerMax Architecture

```
  ┌──────────────────────────────────────────────────────────────────────┐
  │                     PowerMax 8000 Array                              │
  │                                                                      │
  │  ┌──────────────────────────────────────────────────────────────┐    │
  │  │             Director Layer (active-active)                    │    │
  │  │  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐ │    │
  │  │  │  FA Dir   │  │  FA Dir   │  │  SRDF Dir │  │  SRDF Dir │ │    │
  │  │  │ (FC/NVMe) │  │ (FC/NVMe) │  │(replication│  │(replication│ │    │
  │  │  │  ports)   │  │  ports)   │  │  ports)   │  │  ports)   │ │    │
  │  │  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └─────┬─────┘ │    │
  │  └────────┼──────────────┼──────────────┼──────────────┼────────┘    │
  │           │              │              │              │             │
  │  ┌────────▼──────────────▼──────────────▼──────────────▼────────┐    │
  │  │              Crossbar Interconnect (low-latency)              │    │
  │  └───────────────────────────┬───────────────────────────────────┘    │
  │                              │                                        │
  │  ┌───────────────────────────▼───────────────────────────────────┐    │
  │  │              NVMe Flash Drives (NVMe-SCM / eTLC)              │    │
  │  │           (data + FAST VP tiering, SnapVX metadata)           │    │
  │  └───────────────────────────────────────────────────────────────┘    │
  └─────────────────────┬─────────────────────┬────────────────────────── ┘
                        │  FC / NVMe-oF        │ SRDF replication
           ┌────────────▼──────────┐   ┌───────▼───────────────────┐
           │    SAN Fabric          │   │   Remote PowerMax Array   │
           │  (Brocade / Cisco MDS) │   │   (SRDF/S or SRDF/A)      │
           └────────────┬──────────┘   └───────────────────────────┘
                        │
           ┌────────────▼──────────────────────────┐
           │  Hosts (MPIO / PowerPath)              │
           │  Oracle RAC / SQL Server / SAP HANA    │
           └───────────────────────────────────────┘
```

## Overview

Dell PowerMax is an enterprise NVMe-oF all-flash array available in the PowerMax 2000 and 8000 models, designed for mission-critical workloads requiring sub-millisecond latency and continuous availability. It is managed via Unisphere for PowerMax (GUI) or SYMCLI (Solutions Enabler). PowerMax provides synchronous and asynchronous remote replication through SRDF (Symmetrix Remote Data Facility), local snapshots via SnapVX (up to 256 snapshots per device), and automated storage tiering with FAST VP.

## Where It Fits


| Use Case |
|---|
| Primary block storage for tier-1 databases (Oracle, SQL Server, SAP HANA) requiring consistent sub-millisecond latency |
| Synchronous DR replication with SRDF/S for zero RPO between data centres |
| Asynchronous DR replication with SRDF/A for longer-distance sites where synchronous distance is impractical |
| Local point-in-time snapshots with SnapVX for application-consistent backups, dev/test clones, and fast recovery |
| Multi-host SAN environments — storage groups, masking views, and port groups control LUN presentation |
| Automated storage tiering with FAST VP to move data between NVMe, SAS, and NL-SAS tiers based on activity |

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Open Unisphere for PowerMax and review the Dashboard for active alerts |  |  |
| Run `symcfg -sid <SID> show` to confirm array-level health and directo | `symcfg -sid <SID> show` |  |
| Run `symdf list -sid <SID>` to check SRDF pair states | `symdf list -sid <SID>` | all R1 pairs should be `Synchronized` (SRDF/S) or `Consistent` (SRDF/A) |
| Review `sympd list -sid <SID>` to confirm no physical drives are in a | `sympd list -sid <SID>` |  |
| Check storage group thin device pool utilisation via Unisphere or `sym | `symsg list -sid <SID>` |  |
| Confirm any SnapVX sessions that are no longer needed have been termin |  |  |
| Review Unisphere → Performance → Array to check I/O response time and |  |  |

## Health Commands

~~~bash
# List all Symmetrix arrays visible to Solutions Enabler
symcfg list

# Show full array configuration and health for a specific SID
symcfg -sid <SID> show

# List SRDF groups (RDF groups) for the array
symdf list -sid <SID>

# Show SRDF pair state for a specific RDF group
symrdf -sid <SID> -rdfg <group> query

# List all storage groups
symsg list -sid <SID>

# List all device groups
symdg list -sid <SID>

# List all physical drives and their state
sympd list -sid <SID>

# List SnapVX snapshots for a storage group
symsnap list -sid <SID> -sg <storage-group>

# Show real-time I/O statistics (R2 side)
symstat -sid <SID> -type r2

# Show replication sessions (SRDF and SnapVX)
symreplicate list -sid <SID>
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| SRDF pair in `R1 Updated` or `Transmit Idle` state | Link failure, R2 array unreachable, or SRDF director port error | Run `symrdf -sid <SID> -rdfg <group> query`; check director port with `symcfg -sid <SID> show`; investigate WAN link and RDF port health |
| SRDF pair in `Suspended` state | Manual suspend or automatic suspend triggered by I/O error | Confirm cause; if intentional verify R2 is consistent; resume with `symrdf -sid <SID> -rdfg <group> resume` |
| SnapVX session quota exceeded (256 per device limit) | Accumulated snapshots not being expired or unlinked | Run `symsnap list -sid <SID>` to identify stale sessions; terminate or expire unneeded snaps with `symsnap -sid <SID> terminate` |
| Storage group thin device at capacity warning threshold | Thin device allocated capacity approaching the pool limit | Increase thin pool allocation via Unisphere; or expand the storage group device with `symdev -sid <SID> modify` |
| Director port errors or I/O latency spike | SAN fabric event, host HBA issue, or director port degraded | Check `symcfg -sid <SID> show` for port status; review fabric zoning and host multipathing |
| Unisphere certificate expired, GUI inaccessible | TLS certificate for Unisphere web service has lapsed | Replace the certificate via the Solutions Enabler configuration; restart the Unisphere service after renewal |

## Operational Tasks


| Task | Command |
|---|---|
| Create a new storage group with `symsg -sid <SID> create <sg-name>` and add thin |  |
| Create a masking view to present a storage group to a host | `symmask` |
| Create a SnapVX snapshot | `symsnap -sid <SID> create -sg <sg-name> -name <snap-name>` |
| Link a SnapVX snapshot to a target storage group for dev/test or restore |  |
| Establish an SRDF pair | `symrdf -sid <SID> createpair` |
| Change SRDF mode between synchronous and asynchronous via `symrdf -sid <SID> -rd |  |
| Perform a planned SRDF failover (split) and failback via `symrdf split` and `sym |  |
| Expand a thin pool by adding devices via Unisphere → Storage → Thin Pools → Modi |  |

## Upgrade Notes


| Step | Action |
|---|---|
| 1 | Record the current PowerMaxOS and Solutions Enabler version from `symcfg list` and the Unisphere About page |
| 2 | Check the Dell Simple Support Matrix to confirm the target PowerMaxOS version is compatible with all connected host agent and Unisphere versions |
| 3 | Confirm all SRDF pairs are in `Synchronized` or `Consistent` state before upgrade; suspend replication if advised by release notes |
| 4 | Back up the Solutions Enabler database and Unisphere configuration files to an external location |
| 5 | Upgrade Solutions Enabler and Unisphere on management hosts before upgrading the array firmware, following the order specified in the release notes |
| 6 | Apply the PowerMaxOS code upgrade via Unisphere → System → Upgrade; upgrades are non-disruptive and applied as a rolling microcode push |
| 7 | After the upgrade completes, run `symcfg list`, `symdf list -sid <SID>`, and check Unisphere alerts to confirm all directors, ports, and SRDF pairs are healthy |

## Best Practices


| Recommendation | Detail |
|---|---|
| Use SRDF/A with write-order consistency groups (`symcg`) | Use SRDF/A with write-order consistency groups (`symcg`) for multi-volume application workloads to ensure crash-consistent recovery at the DR site |
| Implement FAST VP policies to automate data tiering between NVMe and capacity tiers based on observed I/O patterns | review tier placement quarterly |
| Set I/O limit SLOs (Service Level Objectives) on storage | Set I/O limit SLOs (Service Level Objectives) on storage groups via Unisphere to enforce per-workload latency and bandwidth caps and prevent noisy-neighbour problems |
| Document Symmetrix device IDs, storage group names, and masking view mappings in a CMDB or equivalent | SYMCLI device IDs are array-specific and not portable |
| Never exceed 256 SnapVX snapshots per device | implement automated snap expiry policies in backup software or scripted `symsnap terminate` jobs to stay within limits |
| Use Unisphere Performance → Thresholds to set alert | Use Unisphere Performance → Thresholds to set alert thresholds on response time and port utilisation so issues are caught before they affect hosts |
| Test SRDF failover and failback procedures at least annually | document the exact SYMCLI sequence and validate host I/O resumes on R2 within the target RTO |
| Keep Solutions Enabler and Unisphere at the same major | Keep Solutions Enabler and Unisphere at the same major version as PowerMaxOS to avoid CLI and API incompatibilities |
