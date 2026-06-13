---
tags:
  - nutanix
  - troubleshooting
  - ncc
  - cvm
search:
  boost: 1.5
---
# Nutanix — Common Issues

<div class="kb-summary">
Troubleshooting guide for the most frequent Nutanix problems: CVM down or unreachable, NCC failures, storage degraded/critical, network connectivity issues, cluster full, VM stuck power states, and replication failures.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** CVM SSH (nutanix) and Prism Element admin; AHV host root access may be needed for deep issues
- **Baseline:** Run `ncc --health_checks run_all` as first step for any alert — it identifies the majority of issues automatically

---

## CVM Down / Unreachable

**Symptoms:** `allssh` times out on one CVM; NCC reports `cluster_services_status_check FAIL`; Prism shows one node missing from Hardware view.

**Triage:**
```bash
# From another CVM — can you ping the affected CVM?
ping <cvm-ip>

# If reachable, try SSH
ssh nutanix@<cvm-ip>
genesis status

# If not reachable — check via AHV hypervisor console
# Log into the AHV host directly and check CVM VM state:
virsh list --all | grep CVM
virsh console CVM    # (AHV) connect to CVM console
```

**Common causes and fixes:**

| Cause | Fix |
|---|---|
| CVM powered off | Start CVM: `virsh start CVM` on the AHV host |
| Network issue | Verify CVM IP config on AHV: `ip addr show` on CVM |
| Genesis crashed | SSH to CVM → `genesis restart` |
| Hardware fault | Check AHV host IPMI for memory/disk errors |
| Out of disk space | `df -h /` on CVM — free space in `/home/nutanix` |

```bash
# Restart genesis (recovers most service crashes)
genesis restart

# If genesis won't start — reboot the CVM
sudo reboot   # or via Prism → Hardware → host → reboot CVM
```

---

## NCC Health Check Failures

**Triage:**
```bash
# Run NCC and capture output
ncc --health_checks run_all 2>&1 | tee /tmp/ncc-$(date +%Y%m%d).txt

# Show only failures and warnings
grep -E "^FAIL|^WARN" /tmp/ncc-$(date +%Y%m%d).txt

# Get details for a specific failed check
ncc --health_checks <check_name> 2>&1
```

**Common NCC failures:**

| NCC Check | Common cause | Fix |
|---|---|---|
| `ntp_synchronization_check` | NTP server unreachable | Verify NTP config: `ncli cluster edit-params ntp-server-ip-address-list=<ntp>` |
| `dns_server_check` | DNS unreachable | `ncli cluster edit-params dns-server-ip-address-list=<dns>` |
| `disk_usage_check` | Container over 70% | Expand cluster, delete unused VMs/snapshots |
| `cvm_memory_check` | CVM OOM | Check CVM memory allocation; restart memory-leaking service |
| `cluster_services_status_check` | Service down on a CVM | `genesis status` → restart failing service |
| `cassandra_ring_check` | Node dropped from ring | Check `nodetool status`; restart cassandra: `genesis restart` |
| `data_resiliency_status_check` | Degraded objects | Wait for rebuild; check disk health |

---

## Storage Degraded or Critical

**Symptoms:** Prism alerts "Data Resiliency Status: Critical"; VMs may go read-only or pause if cluster capacity is exhausted.

```bash
# Check cluster resilience
ncli cluster get-domain-fault-tolerance-status type=node

# Check storage usage
ncli ctr list | grep -E "name|used|capacity"

# Check for degraded objects
ncli cluster get-domain-fault-tolerance-status type=disk

# Check data rebuild progress
curator_cli display_curator_tasks | grep -i "rebuild\|resync"
```

**Common causes:**

| Cause | Indicator | Fix |
|---|---|---|
| Disk failure | `ncli disk list` shows non-NORMAL disk | Replace failed disk; curator re-rebuilds automatically |
| Node failure | Resilience = 0 | Restore CVM; if HW failure escalate to Nutanix support |
| Container over-provisioned | Used > 80% | Delete VMs/snapshots, add nodes, or increase container capacity limit |
| Snapshots consuming space | Many old snapshots | `ncli pd ls-snapshots` → delete old ones |

---

## VM Stuck Powering On/Off

**Symptoms:** VM stays in `Transitioning` state; power operation never completes.

```bash
# Check what state the VM is in
acli vm.get <vm-name> | grep -i "power\|state"

# Force reset (if graceful off didn't work)
acli vm.reset <vm-name>

# If reset also hangs, force the VM off at the AHV level:
ssh root@<ahv-host-ip>
virsh list --all | grep <vm-name>
virsh destroy <vm-name>     # hard kill (like pulling power cord)
```

---

## VM Cannot Connect to Network

**Symptoms:** VM boots but has no network; NIC shows no IP.

```bash
# Check VM NIC config
acli vm.nic_list <vm-name>

# Verify the network exists
acli net.list | grep <network-name>

# Remove and re-add NIC (if MAC address issue)
acli vm.nic_delete <vm-name> mac_address=<mac>
acli vm.nic_create <vm-name> network=<network-name>
```

Inside the VM:
```bash
# Reset network interface
ip link set eth0 down && ip link set eth0 up
dhclient eth0   # re-request DHCP
```

---

## Cluster Full — Storage Exhausted

**Symptoms:** VMs failing to write disk; Prism shows "Cluster storage critically full"; containers may go into read-only mode at ~95%.

**Immediate actions (in order):**

1. Delete unused snapshots:
```bash
# List all VMs and their snapshots
for vm in $(acli vm.list | tail -n +2 | awk '{print $1}'); do
    snaps=$(acli vm.snapshot_list "$vm" 2>/dev/null | wc -l)
    [[ $snaps -gt 1 ]] && echo "$vm: $snaps snapshots"
done

# Delete specific snapshot
acli vm.snapshot_delete <vm-name> snapshot_name=<snap-name>
```

2. Delete Protection Domain old snapshots:
```bash
ncli pd ls-snapshots name=<pd-name>
# Delete oldest snapshots manually via Prism Element
```

3. Power off non-critical VMs

4. If still critical — Nutanix support for emergency capacity expansion

---

## Replication Failures (Protection Domain)

**Symptoms:** Replication lag growing; alerts about "Replication link broken" or "Protection domain replication delayed".

```bash
# Check PD replication status
ncli pd get name=<pd-name>

# Check remote site connectivity
ncli remote-site ping name=<dr-site-name>

# Restart replication manually
ncli pd disable-replication name=<pd-name>
ncli pd enable-replication name=<pd-name>

# Check bandwidth to remote site
allssh "iperf3 -c <remote-cvm-ip> -t 10"  # iperf3 must be available
```

---

## Prism UI Inaccessible

**Symptoms:** Cannot reach `https://<cluster-vip>:9440`

```bash
# Check cluster VIP is assigned
ncli cluster info | grep "External IP"

# Ping the VIP
ping <cluster-vip>

# VIP is managed by "cluster" service — restart it:
# (on any CVM)
allssh "genesis status | grep cluster"
# If "cluster" service is DOWN:
genesis restart
```

---



---

## Verify

- The original symptom is resolved — CVM is reachable, storage is healthy, VM has power
- `ncc --health_checks run_all` returns no failures related to the resolved issue
- Prism alert for the issue is cleared or acknowledged
- If a permanent fix was applied (config change, re-registration), record it in the change ticket


---

## See also

- [Nutanix — Diagnostics](diagnostics/)
- [Nutanix — Escalation](escalation/)
- [Nutanix — Health Checks](../operations/health-checks/)
