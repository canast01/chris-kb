# PowerPath — Components

## Core Components

| Component | Role |
|---|---|
| PowerPath kernel module | Loaded at boot; intercepts block I/O and routes it across physical paths |
| Pseudo device | Virtual block device presented to the OS per LUN (e.g., `/dev/emcpowera` on Linux) |
| `powermt` CLI | Management tool for viewing path state, changing policies, and performing configuration operations |
| PowerPath license (registration key) | Entitlement applied per host; required for paths to be managed (unlicensed paths show as `unlic`) |
| PowerPath configuration file | Persists path policy and device settings across reboots; saved with `powermt save` |
| PowerPath daemon (`PowerPath` service) | Userspace service that monitors path health and triggers failover/restore events |

## Connectivity and Integration Points

| Layer | Protocol / Interface | Notes |
|---|---|---|
| Fibre Channel | FC HBA → FC switch → array FA port | Most common in enterprise environments |
| iSCSI | iSCSI initiator → IP network → array iSCSI port | Requires iSCSI initiator configured before PowerPath |
| Host OS | Linux (RHEL, SLES, OEL), Windows Server, AIX, HP-UX, Solaris | Platform-specific PowerPath packages; refer to support matrix |
| Array side | PowerMax, VMAX, Unity, CLARiiON, VNX, PowerStore | PowerPath CLAROpt policy works with ALUA on these platforms |
| VMware | PowerPath/VE for ESXi | Separate product for ESXi; integrates with VAAI for offloaded operations |

## Path States

| State | Meaning | Action |
|---|---|---|
| `alive` | Path healthy and eligible for I/O | None |
| `dead` | Path has failed I/O tests; excluded from routing | Investigate HBA/SAN |
| `unlic` | Path not licensed; I/O not sent over this path | Check license registration |
| `standby` | Path in standby (failover ready) | Normal for some policies |
| `degraded` | Partial path issue | Investigate urgently |

## Load Balancing Policies

| Policy | Code | Description |
|---|---|---|
| CLARiiON Optimized | `co` | Dell/EMC optimised; ALUA-aware; sends I/O over optimised paths first |
| RoundRobin | `rr` | Distributes I/O evenly across all paths regardless of ALUA state |
| BasicFailover | `bf` | Uses one path, fails over on failure; no load balancing |
| Adaptive | `ad` | Load-based selection — switches to least-loaded path |
| No Redirect | `nr` | Uses first active path only (no load balancing) |
| Single Initiator | `si` | Pins I/O to a single HBA port |
