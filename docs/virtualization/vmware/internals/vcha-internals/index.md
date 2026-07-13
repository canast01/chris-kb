---
tags:
  - internals
  - vmware
description: "vCenter High Availability (VCHA) deploys three vCenter instances — active, passive, and witness — with database replication over a private HA network..."
---
# vCenter HA Internals

<div class="kb-summary">
vCenter High Availability (VCHA) deploys three vCenter instances — active, passive, and witness — with database replication over a private HA network. Failover is automatic (~4 min RTO) with split-brain prevention via the witness tie-breaker.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

A: "A" {shape: rectangle}
HN: "HN" {shape: rectangle}
P: "P" {shape: rectangle}
W: "W" {shape: rectangle}

A -> HN
HN -> P
HN -> W
P -> W
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


```text title="Expected output"
{"value":null}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the vCenter certificate into your system trust store.
    **`{"type":"com.vmware.vapi.std.errors.unauthenticated","value":{"messages":[]}}`** — Ensure the SESSION_TOKEN is valid and not expired; obtain a fresh token by authenticating with `/api/session` endpoint first.
    **`curl: (7) Failed to connect to <VCENTER_FQDN> port 443: Connection refused`** — Verify the vCenter FQDN is correct and resolvable, and that the vCenter API service is running and accessible on port 443.
The `vcha.failover` operation is idempotent if passive is already active; returns HTTP 204 on success.

**Post-failover validation:**

1. Verify vSphere Client accessible on cluster IP.
2. Check **Administration → vCenter HA** — original active should show as new passive.
3. Confirm DB replication status returns to "In Sync" (within 5–10 min after original active recovers).
4. Run `vCenter Server → Monitor → Tasks` to confirm no stuck tasks from the failover window.

---

## See also

- [Scenarios — vCenter HA Failover](../../topics/scenarios/vcenter-ha-failover/)
- [vCenter — Operations](../../products/vcenter/operations/)
- [HA Deep Dive — Internals](../ha-deep-dive/)
