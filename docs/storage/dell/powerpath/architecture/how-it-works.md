---
tags:
  - architecture
  - dell
---
# PowerPath — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Host-Side MPIO Stack, Path States, Load-Balancing Policies, Failover and Recovery and 2 more sections.

*Applies to: PowerPath*
</div>
![PowerPath — How It Works](../../../../assets/storage-dell-powerpath-architecture-how-it-works.svg)




```d2
direction: right

center: "PowerPath" {shape: hexagon}
hostside_mpio_stack: "Host-Side MPIO Stack" {shape: rectangle}
path_states: "Path States" {shape: rectangle}
loadbalancing_policies: "Load-Balancing Policies" {shape: rectangle}
failover_and_recovery: "Failover and Recovery" {shape: rectangle}
supported_platforms: "Supported Platforms" {shape: rectangle}
key_commands: "Key Commands" {shape: rectangle}

center -> hostside_mpio_stack
center -> path_states
center -> loadbalancing_policies
center -> failover_and_recovery
center -> supported_platforms
center -> key_commands
```

## Overview

Dell PowerPath is a host-side multipath I/O driver that sits between the OS block device layer and the physical HBA/iSCSI initiator layer. It intercepts I/O destined for storage LUNs and distributes it across all available physical paths, providing automatic failover on path loss and load balancing across healthy paths. PowerPath presents a single virtual (pseudo) device per LUN to the OS regardless of how many physical paths exist.

## Host-Side MPIO Stack

```mermaid
graph LR
  HOST(["Host — Linux / Windows / VMware"]) --> PP["PowerPath\n(MPIO driver)"]
  PP --> P1["HBA0 → Fabric A → SP-A"]
  PP --> P2["HBA0 → Fabric A → SP-B"]
  PP --> P3["HBA1 → Fabric B → SP-A"]
  PP --> P4["HBA1 → Fabric B → SP-B"]
  P1 & P2 & P3 & P4 --> ARRAY["Storage Array\nPowerMax / Unity"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PP net
  class P1,P2,P3,P4 net
  class HOST host
  class ARRAY ctrl
```

## Path States

On startup, PowerPath discovers all LUNs visible across all HBA ports and groups paths to the same LUN into a single pseudo device.

| State | Meaning |
|---|---|
| `alive` | Path is healthy and eligible for I/O |
| `dead` | Path has failed I/O tests; excluded from routing |
| `unlic` | Path is not licensed; I/O will not be sent over this path |

## Load-Balancing Policies

| Policy | Code | Description |
|---|---|---|
| CLAROpt | `co` | Dell/EMC optimised — ALUA-aware; prefers active-optimised paths on PowerMax, Unity |
| RoundRobin | `rr` | Even distribution across all paths regardless of ALUA state (not recommended for Dell arrays) |
| BasicFailover | `bf` | Uses one path; fails over to another on failure; no load balancing |

CLAROpt is the recommended policy for all Dell/EMC arrays. It respects ALUA path preferences and avoids non-optimised paths under normal conditions.

## Failover and Recovery

On path failure, PowerPath automatically marks the path `dead` and re-routes I/O to remaining `alive` paths within milliseconds. Path restoration is automatic — when a failed path recovers, `powermt restore` (run periodically by the daemon or manually) retests dead paths and promotes them back to `alive`.

## Supported Platforms

| OS | Notes |
|---|---|
| Linux (RHEL, SLES, Ubuntu) | RPM/DEB package; integrates with dm-multipath (replaces it) |
| Windows Server | MSI installer; presents pseudo devices as disk objects |
| VMware ESXi | vSphere plug-in; used with PowerMax and Unity |
| AIX, HP-UX, Solaris | Legacy OS support — check PowerPath compatibility matrix |

## Key Commands

```bash
powermt display              # show all pseudo devices and path states
powermt display dev=all      # verbose path detail per device
powermt restore              # retest dead paths and restore alive
powermt check_registration   # verify PowerPath license is registered
```

---

## See also

- [Powerpath — Design Standards](design-standards/)
- [Powerpath — Integrations](integrations/)
