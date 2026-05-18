# vSphere Replication — Common Issues

```
  VR Triage Decision Tree
┌─────────────────────────────────────────────────────────────────┐
│  Symptom                  Check                  Fix            │
│  ┌─────────────────┐      ┌──────────────────┐                  │
│  │ RPO Violation   │─────►│ Bandwidth?        │─► QoS / raise   │
│  │ (amber/red)     │      │ ESXi CPU ready %? │   RPO value     │
│  │                 │      │ VRA disk full?    │─► expand VMDK   │
│  └─────────────────┘      └──────────────────┘                  │
│  ┌─────────────────┐      ┌──────────────────┐                  │
│  │ Site Pair       │─────►│ VRA services up?  │─► start hms/   │
│  │ Disconnected    │      │ TCP 44046 open?   │   vrms          │
│  │                 │      │ Cert expired?     │─► refresh       │
│  └─────────────────┘      └──────────────────┘   thumbprints   │
│  ┌─────────────────┐      ┌──────────────────┐                  │
│  │ Conn Refused /  │─────►│ TCP 31031 open?   │─► firewall      │
│  │ Initial Sync    │      │ Route to VRA?     │   rule / seed   │
│  │ Stalled         │      │ Seed available?   │   pre-copy      │
│  └─────────────────┘      └──────────────────┘                  │
│  ┌─────────────────┐      ┌──────────────────┐                  │
│  │ No Datastore    │─────►│ Target datastore  │─► mount DS /    │
│  │ Available       │      │ mounted? space?   │   free space    │
│  └─────────────────┘      └──────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## VM Stuck in RPO Violation

**Symptoms:** VM shows amber or red in vCenter → Site Recovery → Replications; replication lag exceeds RPO

1. **Insufficient network bandwidth**: Check WAN link utilization
   ```bash
   # On ESXi source host — check replication traffic
   esxtop → n (network) → filter for vmkernel adapter carrying replication traffic
   # Or monitor from network device: check utilization on WAN link
   ```
   Fix: increase RPO to reduce required bandwidth, or prioritize replication traffic via QoS

2. **Source datastore I/O saturation**: High I/O on source datastore causes CBT tracking to slow down
   ```
   vCenter → [VM datastore] → Monitor → Performance → check IOPS and latency
   ```

3. **Source ESXi host CPU saturation**:
   ```
   vCenter → [ESXi host] → Monitor → Performance → CPU ready %
   # If >5%, ESXi is CPU-constrained — replication competes for CPU
   ```

4. **VRA disk full at target site**:
   ```bash
   ssh admin@vra-amsterdam.corp.local
   df -h  # Check /opt and /tmp
   ```

---

## Initial Sync Taking Too Long

**Symptoms:** Newly configured replication stuck in "Syncing" state for days

Initial sync is a full copy of all VM disks — large VMs (1+ TB) naturally take a long time.

1. **Check if sync is actually progressing** (not stalled):
   ```
   Site Recovery → Replications → [VM] → check "Transferred" bytes — should increase over time
   ```
   If bytes transferred is not increasing for >1 hour → stalled

2. **Use a seed** (pre-copy VM disks to target site via another method, then configure VR pointing to the seed):
   ```
   Configure Replication → Step 4: Seeds → Use existing data
   ```

3. **Schedule full sync during low-traffic window**: VR throttles to available bandwidth

---

## Replication Fails with "Connection Refused" / "Connection Timeout"

**Symptoms:** Replication status error: network connectivity to target VRA

```bash
# From source ESXi host shell:
nc -vz vra-amsterdam.corp.local 31031
# If connection refused → firewall blocking TCP 31031
# If timeout → no route to target VRA

# Verify from ESXi:
vmkping -I vmk0 <target-VRA-IP>
```

Fix: open TCP 31031 from source ESXi management IPs to target VRA IP in firewall.

---

## VRA Shows Disconnected / Site Pair Broken

**Symptoms:** Site Recovery → Sites shows "Not Connected"; replications may still be running but management plane is broken

1. **VRA certificate expired or replaced**:
   ```bash
   echo | openssl s_client -connect vra-amsterdam.corp.local:443 2>/dev/null \
     | openssl x509 -noout -dates -subject
   # If expired: deploy new VRA OVA with same IP, re-register
   ```

2. **VRA service stopped**:
   ```bash
   ssh admin@vra-amsterdam.corp.local
   systemctl status hms vrms
   systemctl start hms vrms
   ```

3. **Network interruption between VRAs** (TCP 44046):
   ```bash
   nc -vz vra-amsterdam.corp.local 44046
   ```

4. **Site pair thumbprint mismatch** (cert was replaced):
   ```
   Site Recovery → Sites → [pair] → Edit → Refresh Thumbprints
   ```

---

## "No Compatible Datastore" Error When Configuring Replication

**Symptoms:** Configure Replication wizard shows no available datastores at target site

1. **Target datastore not accessible from target host**: VRA's associated vCenter must see the datastore
2. **Insufficient space**: Target datastore does not meet minimum space requirement for replica
3. **Unsupported datastore type**: VR does not support tape or CDROM-backed datastores

Fix: verify target datastore is mounted and accessible at target vCenter, and has adequate free space.

---

## VRA Running Out of Disk Space

**Symptoms:** VRA VAMI shows disk warning; replications may start failing

```bash
ssh admin@vra-london.corp.local
df -h
# Check /opt partition — VRA appliance partition

# Clear old log files if disk is full:
sudo find /opt/vmware/logs -name "*.log" -mtime +30 -delete
sudo journalctl --vacuum-size=500M
```

VRA appliance disk should be on a thin-provisioned VMDK — expand via vCenter if needed:
```
vCenter → [VRA VM] → Edit Settings → Disk → increase size
Then expand filesystem inside VRA:
  sudo growpart /dev/sda 1
  sudo resize2fs /dev/sda1
```
