# Operations

> Part of the [RecoverPoint](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] All Consistency Groups (CGs) are in ACTIVE replication state |  | none suspended, in error, or paused without a corresponding change ticket |
| [ ] All RPA nodes are online and clustered |  | no degraded or faulted RPA |
| [ ] Journal capacity |  |  |
| [ ] Replication lag / RPO is within the acceptable threshold (typicall |  |  |
| [ ] No image access sessions are left enabled from a previous DR test |  |  |
| [ ] Confirm both production and DR site RecoverPoint clusters are reac |  |  |

## Health Check

```bash
# SSH to the RPA management IP
ssh admin@<rpa_cluster_ip>

# Show overall system status (RPA nodes, cluster state)
system status

# Show all Consistency Group states (expect ACTIVE for all production CGs)
groups status

# Show detailed CG status including RPO and journal utilization
groups status detail

# Show RPA alarms (any active hardware or software alarms)
alarms list

# Show journal capacity for all CGs
journals list

# Show replication link statistics (latency, bandwidth)
links statistics

# REST API: get cluster summary (run from automation host)
RPAPI="https://<rpa_mgmt_ip>/rest/v1"
RP_TOKEN="<base64_encoded_credentials>"

curl -s -k -H "Authorization: Basic ${RP_TOKEN}" \
  "${RPAPI}/clusters" | jq '.clusters[] | {name: .name, health: .healthState}'

# REST API: list all CGs and their replication state
curl -s -k -H "Authorization: Basic ${RP_TOKEN}" \
  "${RPAPI}/groups" | jq '.innerSets[] | {name: .name, state: .replicationState, rpo: .RPO}'
```

## Change Readiness

- [ ] All CGs are in a Consistent state before beginning any storage-side or server-side maintenance
- [ ] Current RPO for each production CG has been noted as a pre-change baseline
- [ ] Journal capacity has sufficient headroom to absorb the expected I/O during the maintenance window (rule of thumb: journal should be < 50% at start of window)
- [ ] RecoverPoint CLI access (SSH to RPA) is confirmed and credentials are available
- [ ] DR site RecoverPoint cluster is reachable and healthy
- [ ] Maintenance window duration has been agreed and does not exceed the journal protection window

| Item | Status | Notes |
|---|---|---|
| All CGs in Consistent state | | |
| Pre-change RPO baseline recorded | | |
| Journal headroom sufficient (< 50% at window start) | | |
| RPA CLI access confirmed | | |
| DR site cluster healthy and reachable | | |
| Window duration within journal protection window | | |

## Incident Triage

**On alert or issue:**
1. SSH to the RPA cluster and run `groups status detail` to identify which CGs are not replicating and their current error state
2. Run `alarms list` to check for active hardware or software alarms on the RPA nodes
3. Run `links statistics` to check for inter-site network issues (high latency, packet loss, zero bandwidth)
4. If a journal is full (`journals list`), the CG replication will be paused — immediately reduce I/O to the protected volumes or increase journal allocation
5. If image access is left on from a previous DR test, disable it immediately: `group disable-image-access --gname <cg_name>`
6. If an RPA node is down, check the RPA hardware health and the underlying network/storage connectivity for that node

| Symptom | Likely Cause | Action |
|---|---|---|
| CG in ERROR or PAUSED state (not manually paused) | Journal full, network failure, or storage issue | Run `journals list` to check journal; run `links statistics` to check network; check RPA alarms |
| Journal above 80% | Write rate exceeding journal drain rate or link down | Check link bandwidth with `links statistics`, reduce write I/O if possible, expand journal allocation |
| RPO breach alert (lag > SLA threshold) | Link congestion or insufficient bandwidth | Check `links statistics`, check WAN QoS for RP replication traffic on port 4460 |
| Image access left active after DR test | DR test was not properly cleaned up | Run `group disable-image-access --gname <cg_name>` immediately, then verify CG returns to ACTIVE |
| RPA node down | Hardware failure or network issue | Check RPA hardware state with `system status`, check physical/VM health, open Dell support case |
| CG in MIXED state | Partial subset of volumes replicating | Run `groups status detail` to identify affected volumes, check initiator zones and storage connectivity |

## Maintenance Window

**Pausing replication for a storage or server maintenance window:**

1. Confirm all CGs are in Consistent state before pausing
2. Pause the relevant CGs:
   ```bash
   # Pause a specific CG
   group disable-replication --gname <cg_name>

   # Or pause all CGs in a group set
   groups disable-replication
   ```
3. Perform the maintenance on the protected storage or servers
4. Resume replication after maintenance is complete:
   ```bash
   group enable-replication --gname <cg_name>
   ```
5. Monitor replication resync — watch `groups status detail` until all CGs return to ACTIVE/Consistent state
6. Confirm RPO returns to within SLA after resync

**DR test image access procedure:**

1. Enable image access on the target copy at the desired point-in-time bookmark:
   ```bash
   group enable-image-access --gname <cg_name> --copy DR --image <bookmark_or_timestamp>
   ```
2. Perform DR test workload validation
3. Disable image access immediately after testing is complete:
   ```bash
   group disable-image-access --gname <cg_name>
   ```
4. Confirm CG returns to ACTIVE replication state

## Post-Change Validation

- [ ] All CGs have returned to ACTIVE replication state (`groups status`)
- [ ] RPO for all production CGs is back within SLA threshold (typically < 15 minutes)
- [ ] Journal consumption has returned to the pre-change baseline (`journals list`)
- [ ] No image access sessions are active
- [ ] `alarms list` shows no new active alarms
- [ ] DR site cluster is healthy and reachable
