# Dell VPLEX — Operations

<div class="kb-summary">
Dell VPLEX — Operations reference: Health Checks, Procedures, CLI Reference, Install & Upgrade, and 2 more.
</div>

```
┌──────────────────────────────────────── Dell VPLEX Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Day-2 ops: virtual volume provisioning, CG operations, Metro volume health, WAN monitoring  │   │
│   │     Provision: claim back-end LUN → create storage volume → virtual volume → storage view     │   │
│   │      Metro ops: check distributed volume state, WAN link health, and witness connectivity     │   │
│   │         Health: director status, cache utilization, back-end path health via VPLEX CLI        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Back-end LUN claimed → virtual volume created → CG added → storage view updated → host sees        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Provisioning        │  │          Metro Ops          │  │            Health           │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Claim back-end       │  │        Dist vol state       │  │       Director status       │   │
│   │       Create virt vol       │  │       WAN link health       │  │         Cache stats         │   │
│   │          Add to CG          │  │        Witness check        │  │        BE path check        │   │
│   │         Storage view        │  │        Metro failover       │  │          Event log          │   │
│   │         Host rescan         │  │        Metro failback       │  │         Alert review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Director health → WAN link state → distributed volume check → storage view audit                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │   CLI context    │      Command      │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │ Director health  │     engines      │    ls directors   │      Daily       │   Any degraded   │   │
│   │    Vol state     │ virtual-volumes  │       ls -t       │      Daily       │  Check detached  │   │
│   │     WAN link     │     clusters     │   ls comm-links   │  Daily (Metro)   │  Check latency   │   │
│   │     Witness      │     clusters     │    ls witnesses   │      Weekly      │Must be reachable │   │
│                                                                                                       │
│    Physical: VPLEX chassis FC ports to SAN fabric; IP WAN ports for Metro cluster link                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Claim back-end = VPLEX takes ownership of an array LUN for use as a storage volume                 │
│    Storage volume = VPLEX internal representation of a claimed back-end LUN                           │
│    Virtual volume = External-facing volume presented to hosts via VPLEX storage view                  │
│    Storage view   = Maps virtual volumes to host initiator ports; VPLEX access control                │
│    Distributed vol= Metro volume type; accessible from both clusters simultaneously                   │
│    WAN comm-link  = IP link between two VPLEX Metro clusters; must be <5ms RTT                        │
│    Witness        = Third-site VM; provides quorum for Metro split decisions                          │
│    Detached vol   = Virtual volume not currently accessible due to director or BE fault               │
│    Metro failover = One cluster takes full write ownership after WAN loss; witness arbitrates         │
│    Metro failback = After site recovery, resync cluster and restore distributed volume state          │
│    ls directors   = VPLEX CLI: list all directors and their operational state                         │
│    ls comm-links  = VPLEX CLI: list Metro WAN communication links and latency stats                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── Dell VPLEX Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Day-2 ops: virtual volume provisioning, CG operations, Metro volume health, WAN monitoring  │   │
│   │     Provision: claim back-end LUN → create storage volume → virtual volume → storage view     │   │
│   │      Metro ops: check distributed volume state, WAN link health, and witness connectivity     │   │
│   │         Health: director status, cache utilization, back-end path health via VPLEX CLI        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Back-end LUN claimed → virtual volume created → CG added → storage view updated → host sees        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Provisioning        │  │          Metro Ops          │  │            Health           │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        Claim back-end       │  │        Dist vol state       │  │       Director status       │   │
│   │       Create virt vol       │  │       WAN link health       │  │         Cache stats         │   │
│   │          Add to CG          │  │        Witness check        │  │        BE path check        │   │
│   │         Storage view        │  │        Metro failover       │  │          Event log          │   │
│   │         Host rescan         │  │        Metro failback       │  │         Alert review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Director health → WAN link state → distributed volume check → storage view audit                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │   CLI context    │      Command      │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │ Director health  │     engines      │    ls directors   │      Daily       │   Any degraded   │   │
│   │    Vol state     │ virtual-volumes  │       ls -t       │      Daily       │  Check detached  │   │
│   │     WAN link     │     clusters     │   ls comm-links   │  Daily (Metro)   │  Check latency   │   │
│   │     Witness      │     clusters     │    ls witnesses   │      Weekly      │Must be reachable │   │
│                                                                                                       │
│    Physical: VPLEX chassis FC ports to SAN fabric; IP WAN ports for Metro cluster link                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Claim back-end = VPLEX takes ownership of an array LUN for use as a storage volume                 │
│    Storage volume = VPLEX internal representation of a claimed back-end LUN                           │
│    Virtual volume = External-facing volume presented to hosts via VPLEX storage view                  │
│    Storage view   = Maps virtual volumes to host initiator ports; VPLEX access control                │
│    Distributed vol= Metro volume type; accessible from both clusters simultaneously                   │
│    WAN comm-link  = IP link between two VPLEX Metro clusters; must be <5ms RTT                        │
│    Witness        = Third-site VM; provides quorum for Metro split decisions                          │
│    Detached vol   = Virtual volume not currently accessible due to director or BE fault               │
│    Metro failover = One cluster takes full write ownership after WAN loss; witness arbitrates         │
│    Metro failback = After site recovery, resync cluster and restore distributed volume state          │
│    ls directors   = VPLEX CLI: list all directors and their operational state                         │
│    ls comm-links  = VPLEX CLI: list Metro WAN communication links and latency stats                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>
