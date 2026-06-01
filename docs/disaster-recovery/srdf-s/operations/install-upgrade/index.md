# SRDF/S — Install & Upgrade


<div class="kb-summary">
> Part of the [SRDF/S Operations](../index.md) reference.
</div>

---

## HYPERMAX OS Version Compatibility

SRDF/S pairs require compatible HYPERMAX OS versions on both arrays. Always check the Dell interoperability matrix before mixed-version pairing.

| Source Array | Target Array | Supported? | Why |
|---|---|---|---|
| PowerMax 2500 (10.0.x) | PowerMax 2500 (10.0.x) | Yes (same version) | Identical microcode level — full SRDF/S feature parity |
| PowerMax 2500 (10.0.x) | PowerMax 8500 (10.0.x) | Yes (same major) | Same major release supports cross-model pairing |
| PowerMax (10.0.x) | VMAX All Flash (8.4.x) | Check matrix — limited | Different product generations; some SRDF/S features unavailable |
| PowerMax (10.1.x) | PowerMax (10.0.x) | Check matrix — N-1 typically supported | N-1 is generally allowed but verify specific feature requirements |

Verify current version:
```bash
symcfg list -v | grep "Microcode"
```
┌───────────────────────────────────── SRDF/S — Install & Upgrade ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              SRDF/S — Installation Prerequisites                              │   │
│   │             OS: supported Linux or Windows Server (see vendor compatibility matrix)           │   │
│   │      Network: Dark fiber FC (< 5 ms RTT) · DWDM long-haul FC — ensure firewall allows these   │   │
│   │        Auth: Symmetrix admin credentials; Solutions Enabler; Unisphere role-based access      │   │
│   │        Storage: Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency (< 200 km)      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Install Sequence                                       │   │
│   │                  1  Deploy control plane component and configure network access               │   │
│   │                          2  Configure storage and network connectivity                        │   │
│   │                        3  Install agent/proxy/splitter on protected hosts                     │   │
│   │                      4  Register sources and configure protection policies                    │   │
│   │                        5  Run first job; verify completion; test restore                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Upgrade Sequence                                       │   │
│   │                 1  Review release notes and compatibility matrix before upgrade               │   │
│   │                   2  Snapshot or backup the control plane VM before upgrading                 │   │
│   │                  3  Upgrade control plane first, then proxies/agents/appliances               │   │
│   │                       4  Validate jobs resume automatically after upgrade                     │   │
│   │                        5  Document version change and update CMDB record                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Two PowerMax arrays · Dark fiber / DWDM FC link · Low-latency network (< 200 km) · RF director ports │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SRDF/S        = Synchronous SRDF; every R1 write is mirrored to R2 before host acknowledgment        │
│  R1            = source volume; write is held pending R2 confirmation — adds WAN RTT to latency       │
│  R2            = target volume; must acknowledge each write; acts as synchronous mirror               │
│  RTT           = Round-Trip Time between R1 and R2 arrays; directly added to host write latency       │
│  RPO=0         = zero recovery point objective; no data loss possible under normal operation          │
│  RTO           = Recovery Time Objective; SRDF/S failover typically < 5 minutes manual, < 1 min       │
│  symrdf        = CLI for all SRDF operations: establish, split, suspend, failover, restore, ver       │
│  Pair State    = Synchronized | Consistent | Suspended | Failed Over | Split                          │
│  Consistent    = transient state where R1 write is in transit but not yet confirmed on R2             │
│  Failover      = makes R2 read-write; production continues from DR site after R1 failure              │
│  Restore       = re-synchronises after failover; direction is reversed until R1 catches up            │
│  RDFG          = RDF Group: logical grouping of SRDF pairs sharing same link and parameters           │
│  FA Port       = Front-End Adapter port on PowerMax; used for host connectivity (non-SRDF)            │
│  RF Port       = Remote Fabric port on PowerMax; used exclusively for SRDF replication traffic        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

---

## License Lifecycle

SRDF licenses are array-bound per PowerMax array. Track:

| Item | Action | Why |
|---|---|---|
| License expiry dates | Annual review; alert 90 days before expiry | Expired license disables SRDF operations — potential production outage |
| SRDF/S vs SRDF/A licences | Separate SKUs; verify correct licence type is applied | Wrong license type results in replication mode mismatch at establish time |
| SRDF/E (encryption) | Optional add-on — track separately | Required for compliance frameworks mandating data-in-transit encryption |
| License compliance | Compare licensed pairs vs. `symcfg list -rdfg` output | Over-deployed pairs may fail to establish if license count is exceeded |

## NDU Firmware Upgrade Sequence

```mermaid
flowchart TD
    preCheck["Verify All Pairs Synchronized\nsymrdf -g rdfg query | grep -v Synchronized"]
    notifyApps["Notify Application Teams\nTemporary RPO degradation during window"]
    convertAsync["Convert to SRDF/A\nsymrdf -g rdfg set mode async"]
    nduSource["NDU on Source Array\n(Dell NDU runbook)"]
    nduTarget["NDU on Target Array"]
    convertSync["Re-establish Synchronous Mode\nsymrdf -g rdfg set mode sync"]
    waitResync["Wait for Synchronized State\n(SyncInProg expected)"]
    postValidate["Post-Upgrade Validation\nAll pairs Synchronized within 30 min"]
    closeChange["Close Change Ticket"]

    preCheck --> notifyApps
    notifyApps --> convertAsync
    convertAsync --> nduSource
    nduSource --> nduTarget
    nduTarget --> convertSync
    convertSync --> waitResync
    waitResync --> postValidate
    postValidate --> closeChange

    style preCheck fill:#7c3aed,color:#fff
    style convertAsync fill:#b45309,color:#fff
    style convertSync fill:#2563eb,color:#fff
    style closeChange fill:#15803d,color:#fff
```
