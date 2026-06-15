---
tags:
  - internals
  - vmware
---
# vCenter HA Internals

<div class="kb-summary">
vCenter High Availability (VCHA) deploys three vCenter instances — active, passive, and witness — with database replication over a private HA network. Failover is automatic (~4 min RTO) with split-brain prevention via the witness tie-breaker.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌─────────────────────────────── vCenter HA (VCHA) — Three-Node Topology ───────────────────────────────┐
│                                                                                                       │
│  VCHA deploys three vCenter instances — active, passive, and witness — with                           │
│  Postgres streaming replication; witness prevents split-brain; RTO ~4 min.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                VCHA Topology                 │  │              Failover Behaviour             │   │
│   │        Active: primary vCenter (R/W)         │  │        Witness + passive detect loss        │   │
│   │       Passive: standby; Postgres sync        │  │          Quorum: 2 of 3 nodes agree         │   │
│   │        Witness: tie-breaker (1 vCPU)         │  │          Failover time: ~4 min RTO          │   │
│   │          HA network: private 1 GbE           │  │        Split-brain: witness prevents        │   │
│   │       Replication: Postgres streaming        │  │        Manual failover: VCHA admin UI       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VCHA is HA only — it does not replace VCSA file-based backup for DR.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Network Requirements             │  │            Maintenance and Backup           │   │
│   │        HA network: /24 dedicated VLAN        │  │           VCHA != backup: HA only           │   │
│   │        Mgmt IP: all 3 on same subnet         │  │        File-based backup: daily SFTP        │   │
│   │       Witness: can be on WAN (low BW)        │  │          Restore: backup + new VCSA         │   │
│   │       Maintenance: disable VCHA first        │  │          Rebuild VCHA after restore         │   │
│   │        All 3 nodes: must match build         │  │       Patch: active -> passive -> wit       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Three VCSA VMs on separate hosts/clusters for fault isolation; HA network                            │
│  on isolated VLAN; witness can be on remote ESXi or vCenter-managed host.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCHA         = vCenter High Availability; 3-node active/passive/witness                              │
│  Active node  = runs vCenter services and responds to all requests                                    │
│  Passive node = warm standby; Postgres replica; takes over on failover                                │
│  Witness node = tie-breaker only; no vCenter services; 1 vCPU/1 GB                                    │
│  Postgres     = vCenter internal database; streamed from active to passive                            │
│  RTO          = Recovery Time Objective; ~4 min for VCHA automatic failover                           │
│  Split-brain  = both active and passive believe they are primary; prevented by witness                │
│  Quorum       = 2 of 3 VCHA nodes must agree before promoting passive                                 │
│  HA network   = private /24 VLAN for replication; not management network                              │
│  File-based backup= VCSA backup via SFTP/NFS/SMB; separate from VCHA                                  │
│  Build match  = all 3 VCHA nodes must run identical vCenter build number                              │
│  Maintenance  = disable VCHA before patching; re-enable after all 3 updated                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
    classDef active fill:#2563eb,color:#fff,stroke:none
    classDef passive fill:#15803d,color:#fff,stroke:none
    classDef witness fill:#b45309,color:#fff,stroke:none
    classDef net fill:#1e3a5f,color:#fff,stroke:none

    A[Active vCenter]:::active
    P[Passive vCenter]:::passive
    W[Witness Node]:::witness
    HN[HA Network\n192.168.10.0/24\nport 8095]:::net

    A -->|DB replication\nDRBD filesystem sync| HN
    HN -->|continuous sync| P
    A -->|heartbeat| HN
    HN -->|heartbeat| W
    P -->|quorum check| W
```
## 3-Node Topology

VCHA requires exactly three participants. Each runs as a separate VCSA VM.

| Node | Role | NIC requirement |
|------|------|-----------------|
| Active | Serves all management traffic; vCenter API and UI | Management NIC + HA NIC |
| Passive | Receives continuous DB replication; takes over on active failure | Management NIC + HA NIC |
| Witness | Provides quorum only; holds no vCenter state | HA NIC only (1 vCPU, 8 GB RAM minimum) |

The three nodes share the same vCenter IP/FQDN via a virtual IP (cluster IP) owned by the active node. On failover, the passive node assumes this cluster IP.

## State Synchronisation

Two independent replication channels run continuously over the private HA network:

**Database replication — port 8095**
- vPostgres streaming replication (WAL shipping) from active to passive.
- Synchronous by default; passive must acknowledge each WAL segment before active commits.
- Replication lag is monitored; UI shows "In Sync / Out of Sync" under vCenter HA configuration.

**Filesystem sync — DRBD**
- DRBD (Distributed Replicated Block Device) replicates the VCSA `/storage` filesystem partitions.
- Covers configuration files, certificate stores (VECS), and STS LDAP data that live outside vPostgres.
- DRBD protocol C (synchronous) ensures no write is acknowledged until the passive disk confirms receipt.

**Private HA network requirements:**
- Dedicated VLAN or dedicated port group; must not traverse a WAN link.
- Minimum 1 GbE; 10 GbE recommended for large inventories.
- Latency must be < 10 ms RTT between active and passive.

## Failover Trigger and Sequence

The FDM (Fault Domain Manager) agent on the passive node monitors active node heartbeats on the HA network.

**Default timing parameters:**

| Parameter | Default | Notes |
|-----------|---------|-------|
| Heartbeat interval | 10 s | Configurable via advanced VCHA settings |
| Failure count before promotion | 3 | Consecutive missed heartbeats |
| Effective dead-time before action | 30 s | 3 × 10 s |
| DB sync completion wait | Variable | Passive waits until replication lag = 0 |
| Total RTO (typical) | ~4 min | Includes OS boot of services on passive |

**Failover sequence:**

1. Passive FDM detects three consecutive missed heartbeats from active.
2. Passive queries witness: "Is active reachable from your vantage point?"
3. Witness confirms active is unreachable → quorum achieved.
4. Passive confirms DB replication lag is 0 (all WAL applied).
5. Passive promotes: acquires cluster IP, starts all vCenter services.
6. vSphere Client and API calls resume on the new active node.
7. Original active (if recovered) rejoins as the new passive in standby.

## Split-Brain Prevention

The witness is the sole tie-breaker. Split-brain scenarios:

| Scenario | Outcome |
|----------|---------|
| Active unreachable, witness confirms → quorum | Passive promotes |
| Active unreachable, witness also unreachable | Passive does NOT promote; cluster goes read-only |
| Network partition: passive cannot reach active but witness sees active alive | Passive does NOT promote |
| Active and passive both claim active role | Witness vote determines the true active; loser powers off vCenter services |

This design prevents a split where both passive and original active serve API traffic simultaneously.

## vCenter HA vs Recovery Options

| Capability | VCHA | vCenter restore from backup |
|------------|------|-----------------------------|
| RTO | ~4 min automated | Hours (manual restore) |
| RPO | Near-zero (synchronous replication) | Age of last backup |
| Topology | 3 VMs, dedicated HA network | Single VCSA |
| PSC model | Embedded PSC (vSphere 7+); separate PSC in 6.x required careful HA config | N/A |
| Use case | Active/passive HA for management plane | DR site recovery or full rebuild |

In vSphere 7.0+, the PSC is embedded in VCSA. In 6.x, VCHA required the PSC to be separately deployed and did not protect the PSC itself — a significant limitation removed in 7.0.

## VCHA Requirements

| Requirement | Specification |
|-------------|--------------|
| vCenter edition | Standard or higher (not Foundation/Essentials) |
| HA network | Dedicated port group; same vDS or separate vSS; not routed WAN |
| HA network bandwidth | 1 GbE minimum; 10 GbE recommended |
| Cluster placement | All 3 nodes can be on same ESXi cluster or cross-cluster (not cross-site for HA network) |
| Witness resource | 1 vCPU, 8 GB RAM, 1 NIC (HA network only) |
| Active/Passive resource | Same sizing as standalone vCenter (size based on inventory) |
| vSphere version | 6.5+ for initial VCHA; 7.0+ for embedded PSC support |
| Storage | Active and passive need same datastore access; witness needs separate datastore |

## Procedure: Initiate Manual Failover

**Via vSphere Client UI:**

1. Log in to the active vCenter as an SSO administrator.
2. Navigate to **Menu → Administration → vCenter HA**.
3. Confirm status shows "Healthy" with passive "In Sync".
4. Click **Initiate Failover**.
5. Confirm the dialog warning that management plane will be briefly unavailable.
6. Passive promotes; reconnect vSphere Client to the same cluster IP after ~4 min.

**Via REST API:**

```bash
# Trigger failover using vCenter REST API (authenticate first to get session token)
curl -X POST \
  -H "vmware-api-session-id: <SESSION_TOKEN>" \
  "https://<VCENTER_FQDN>/api/vcenter/vcha/cluster?action=failover_vcha"
```

The `vcha.failover` operation is idempotent if passive is already active; returns HTTP 204 on success.

**Post-failover validation:**

1. Verify vSphere Client accessible on cluster IP.
2. Check **Administration → vCenter HA** — original active should show as new passive.
3. Confirm DB replication status returns to "In Sync" (within 5–10 min after original active recovers).
4. Run `vCenter Server → Monitor → Tasks` to confirm no stuck tasks from the failover window.

---

## See also

- [Scenarios — vCenter HA Failover](../../topics/scenarios/vcenter-ha-failover/)
- [vCenter — Operations](../../vcenter/operations/)
- [HA Deep Dive — Internals](../ha-deep-dive/)
