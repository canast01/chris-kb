# ESXi — Architecture Overview

## Hypervisor Overview

ESXi is a Type-1 (bare-metal) hypervisor built around the **VMkernel** — a purpose-built OS that directly manages CPU, memory, storage, and network resources on the physical host. ESXi has no general-purpose OS underneath it.

Key design principles:
- **Thin footprint**: ESXi runs from a USB/SD card or M.2 boot device (< 1 GB)
- **In-memory configuration**: most host config is held in memory and persisted to a config store
- **Direct hardware access**: VMkernel drivers communicate directly with hardware via VIBs (vSphere Installation Bundles)

## Management Interfaces

| Interface | Access | Purpose |
|---|---|---|
| DCUI | Physical console (or IPMI/iDRAC KVM) | Emergency management, IP config, lockdown mode |
| ESXi Shell | SSH or local console | Advanced diagnostics; disable when not in use |
| vSphere Client | Via vCenter | Primary day-to-day management |
| ESXi Embedded Host Client | `https://<host>/ui` | Direct host management when vCenter unavailable |
| REST API | `https://<host>/api` | Automation and programmatic access |

## High Availability at Host Level

ESXi hosts do not provide HA themselves — HA is orchestrated by vCenter through the **HA cluster**. When a host fails:

1. vCenter HA master detects host failure (network isolation or host failure)
2. HA master elects which surviving host will restart failed VMs
3. VMs are restarted based on restart priority and available capacity (admission control)

**Host Profiles** enforce consistent configuration across cluster hosts. Applied from vCenter; any host that drifts from profile is flagged as non-compliant.
