# Dell VPLEX

<div class="kb-summary">
Storage federation and virtualization platform — active-active LUN access (VPLEX Local), synchronous metro mirroring (VPLEX Metro), and data mobility across heterogeneous arrays without host disruption.
</div>

```
┌──────────────────────────────────── Dell VPLEX Storage Federation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        VPLEX: Dell storage virtualization/federation; presents virtual volumes to hosts       │   │
│   │        VPLEX Local: single cluster; virtualizes back-end arrays; pooling and migration        │   │
│   │        VPLEX Metro: two clusters linked via WAN; distributed volumes for active-active        │   │
│   │       GeoSynchrony OS: VPLEX management; directors (I/O and Storage); witness for Metro       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host → I/O Director → virtual volume → Storage Director → back-end array LUN                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │          Metro / HA         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         I/O Director        │  │          VPLEX CLI          │  │       Distributed vol       │   │
│   │       Storage Director      │  │       Virtual vol prov      │  │          Witness VM         │   │
│   │       GeoSynchrony OS       │  │        CG management        │  │        WAN link <5ms        │   │
│   │       DRAM write cache      │  │         Storage view        │  │       Split-brain prot      │   │
│   │       Back-end arrays       │  │       Director health       │  │        Metro failover       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    I/O director receives host write → DRAM cache → Storage Director → back-end array                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Mode       │   VPLEX Local    │    VPLEX Metro    │     Protocol     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Clusters     │    1 cluster     │     2 clusters    │     FC host      │  iSCSI optional  │   │
│   │   Volume type    │   Virtual vol    │  Distributed vol  │   FC back-end    │  Array-agnostic  │   │
│   │       RPO        │    N/A local     │    Zero (sync)    │   WAN IP link    │  <5ms RTT req.   │   │
│   │     Witness      │   Not required   │      Required     │        —         │  Tie-breaker VM  │   │
│                                                                                                       │
│    Physical: VPLEX chassis with director blades; FC fabric to hosts and back-end arrays               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    I/O Director   = Front-end VPLEX blade; handles host FC connections and virtual volume I/O         │
│    Storage Director= Back-end VPLEX blade; connects to physical array FC ports                        │
│    Virtual volume = Logical volume presented to host; backed by one or more array LUNs                │
│    Distributed vol= Metro volume visible and writable from both VPLEX clusters simultaneously         │
│    GeoSynchrony   = VPLEX management OS; configuration, CLI access, director orchestration            │
│    Storage view   = VPLEX host access control; maps virtual volumes to initiator ports                │
│    DRAM cache     = Write cache in director; coalesces writes before committing to array              │
│    Witness VM     = Third-site VM; breaks tie in Metro split-brain; must be on neutral site           │
│    Split-brain    = Both clusters lose WAN; each thinks it is the only survivor; witness decides      │
│    Metro failover = One cluster takes full I/O after site loss; witness determines survivor           │
│    CG             = Consistency Group; set of distributed volumes with write-order fidelity           │
│    VPLEX CLI      = vplex-shell; management console on GeoSynchrony for all VPLEX config              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────── Dell VPLEX Storage Federation ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        VPLEX: Dell storage virtualization/federation; presents virtual volumes to hosts       │   │
│   │        VPLEX Local: single cluster; virtualizes back-end arrays; pooling and migration        │   │
│   │        VPLEX Metro: two clusters linked via WAN; distributed volumes for active-active        │   │
│   │       GeoSynchrony OS: VPLEX management; directors (I/O and Storage); witness for Metro       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host → I/O Director → virtual volume → Storage Director → back-end array LUN                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │          Metro / HA         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │         I/O Director        │  │          VPLEX CLI          │  │       Distributed vol       │   │
│   │       Storage Director      │  │       Virtual vol prov      │  │          Witness VM         │   │
│   │       GeoSynchrony OS       │  │        CG management        │  │        WAN link <5ms        │   │
│   │       DRAM write cache      │  │         Storage view        │  │       Split-brain prot      │   │
│   │       Back-end arrays       │  │       Director health       │  │        Metro failover       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    I/O director receives host write → DRAM cache → Storage Director → back-end array                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Mode       │   VPLEX Local    │    VPLEX Metro    │     Protocol     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Clusters     │    1 cluster     │     2 clusters    │     FC host      │  iSCSI optional  │   │
│   │   Volume type    │   Virtual vol    │  Distributed vol  │   FC back-end    │  Array-agnostic  │   │
│   │       RPO        │    N/A local     │    Zero (sync)    │   WAN IP link    │  <5ms RTT req.   │   │
│   │     Witness      │   Not required   │      Required     │        —         │  Tie-breaker VM  │   │
│                                                                                                       │
│    Physical: VPLEX chassis with director blades; FC fabric to hosts and back-end arrays               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    I/O Director   = Front-end VPLEX blade; handles host FC connections and virtual volume I/O         │
│    Storage Director= Back-end VPLEX blade; connects to physical array FC ports                        │
│    Virtual volume = Logical volume presented to host; backed by one or more array LUNs                │
│    Distributed vol= Metro volume visible and writable from both VPLEX clusters simultaneously         │
│    GeoSynchrony   = VPLEX management OS; configuration, CLI access, director orchestration            │
│    Storage view   = VPLEX host access control; maps virtual volumes to initiator ports                │
│    DRAM cache     = Write cache in director; coalesces writes before committing to array              │
│    Witness VM     = Third-site VM; breaks tie in Metro split-brain; must be on neutral site           │
│    Split-brain    = Both clusters lose WAN; each thinks it is the only survivor; witness decides      │
│    Metro failover = One cluster takes full I/O after site loss; witness determines survivor           │
│    CG             = Consistency Group; set of distributed volumes with write-order fidelity           │
│    VPLEX CLI      = vplex-shell; management console on GeoSynchrony for all VPLEX config              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
