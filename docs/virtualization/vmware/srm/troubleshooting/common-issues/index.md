# SRM — Common Issues

```
┌───────────────────────────────────── VMware SRM — Common Issues ──────────────────────────────────────┐
│                                                                                                       │
│  Common SRM issues: site pair disconnected, replication lag exceeded RPO, plan test                   │
│  failure, IP customisation not applied, and cleanup stuck after test.                                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Site Pair Issues               │  │              Replication Issues             │   │
│   │         Pair disconnected: check net         │  │           Lag > RPO: check WAN BW           │   │
│   │            Cert expired: re-pair             │  │          vSR error: check vRAM host         │   │
│   │          vCenter unreachable: check          │  │          ABR error: check SRA logs          │   │
│   │          Port 9086: check firewall           │  │          Disk full: clear vSR logs          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cert expiry is the most common site pair disconnection cause; monitor 30+ days ahead.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Plan Test Failures              │  │               Post-Test Issues              │   │
│   │         VM fail to power on: vSphere         │  │             Cleanup stuck: force            │   │
│   │          IP script error: check log          │  │             Test VMs not deleted            │   │
│   │          Network mapping wrong: fix          │  │           Snapshots remain: purge           │   │
│   │           Script timeout: increase           │  │           Re-run cleanup in SRM UI          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Most issues: WAN bandwidth (lag), network mapping (IP/VLAN), cert expiry (pair),                     │
│  or vCenter connectivity; check all four before deep investigation.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Site pair disconnected= SRM Servers lost TCP connectivity                                            │
│  Port 9086     = SRM inter-site communication; must be open in FW                                     │
│  Cert expired  = site pair uses TLS certs; expiry breaks connection                                   │
│  Re-pair       = re-establish site trust after cert or config change                                  │
│  vSR host      = vSphere Replication Server appliance; check logs                                     │
│  SRA logs      = Storage Replication Adapter log; array errors here                                   │
│  IP script     = customisation script; failure blocks VM connectivity                                 │
│  Network mapping= maps protected-site portgroup to recovery portgroup                                 │
│  Cleanup stuck = SRM cleanup task hung; force via SRM UI                                              │
│  Force cleanup = right-click plan > Cleanup in SRM UI                                                 │
│  WAN BW        = insufficient bandwidth causes replication lag                                        │
│  Snapshot purge= manual delete of orphan snapshots after stuck cleanup                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
  Triage Decision Tree
┌──────────────────────────────────────────────────────────────┐
│  Site pairing broken?         Replication lag?               │
│  ┌──────────────────┐         ┌──────────────────────────┐   │
│  │ Cert thumbprint  │         │ Network bandwidth?        │   │
│  │  mismatch?       │         │ Source datastore I/O?    │   │
│  │ TCP 9086 blocked?│         │ VRA unreachable?         │   │
│  │ SRM service down?│         └──────────────────────────┘   │
│  └──────────────────┘                                        │
│                                                              │
│  Recovery Plan stuck?         Test failover: VMs fail on?    │
│  ┌──────────────────┐         ┌──────────────────────────┐   │
│  │ Manual step wait │         │ Network mapping missing? │   │
│  │  for approval?   │         │ Placeholder VM stale?    │   │
│  │ VM power-on      │         │ Recovery site resources  │   │
│  │  timeout?        │         │  insufficient?           │   │
│  └──────────────────┘         └──────────────────────────┘   │
│                                                              │
│  Failback fails?                                             │
│  ┌──────────────────┐                                        │
│  │ Reprotect first! │                                        │
│  │ Protected site   │                                        │
│  │ vCenter up?      │                                        │
│  └──────────────────┘                                        │
└──────────────────────────────────────────────────────────────┘
```

---

## Site Pairing Fails / Shows Disconnected

**Symptoms:** Site Recovery Summary shows remote site as "Not Connected"

1. **Certificate thumbprint mismatch** (cert replaced without updating pairing):
   ```bash
   # Get current remote SRM cert thumbprint:
   echo | openssl s_client -connect srm-recovery.example.local:9086 2>/dev/null \
     | openssl x509 -fingerprint -sha1 -noout
   # Compare to thumbprint stored in site pair
   # Site Recovery → Site Pair → Edit → update thumbprint
   ```

2. **Network / firewall**: TCP 9086 blocked between SRM Servers
   ```bash
   nc -vz srm-recovery.example.local 9086
   # If connection refused or timeout: firewall rule missing
   ```

3. **SRM service stopped on remote site**:
   ```powershell
   Get-Service -ComputerName srm-recovery.example.local -Name "VMware vCenter Site Recovery Manager"
   Start-Service -ComputerName srm-recovery.example.local -Name "VMware vCenter Site Recovery Manager"
   ```

---

## SRA Not Found / Discovery Fails

**Symptoms:** "No Storage Replication Adapters found" or discovery returns empty

1. **SRA service stopped on SRM Server**:
   ```powershell
   Get-Service -ComputerName srm-protected.example.local -Name "*SRA*"
   # Restart if stopped
   ```

2. **Wrong array credentials**:
   ```
   Site Recovery → Storage → Array Pairs → [pair] → Configure Adapter
   Test credentials against array directly:
   curl -sk -H "x-auth-token: <api-token>" https://<flasharray-ip>/api/2.0/array
   # Should return 200 OK
   ```

3. **Network connectivity from SRM Server to array management IP**:
   ```
   Test-NetConnection <flasharray-ip> -Port 443
   ```

---

## Recovery Plan Stuck in "Running"

**Symptoms:** Recovery Plan is running but no progress for >10 minutes; one step shows in-progress indefinitely

1. **Manual step timeout**: Recovery Plan has a manual approval step that no one has approved
   ```
   Site Recovery → Recovery Plans → [plan] → [current run] → Steps
   Find the step waiting for input → click to complete/skip
   ```

2. **VM power-on timeout**: VM at recovery site taking too long to power on (resource contention)
   ```
   vCenter (Recovery) → Recent Tasks → look for power-on task on the stuck VM
   Check ESXi host resources at recovery site
   ```

3. **Force cancel if stuck >30 minutes**:
   ```
   Site Recovery → Recovery Plans → [plan] → Cancel
   Note: cancellation may leave partial state — check VMs manually
   ```

---

## Protection Group Shows Error

**Symptoms:** Protection Group status is "Error" or "Warning"

1. **RPO lag exceeds configured RPO**: Replication is not keeping up
   ```
   Site Recovery → Replication → vSphere Replication
   Find the VMs in the PG → check "Lag" column
   Investigate: network bandwidth, ESXi CPU on source host, source datastore I/O
   ```

2. **VM snapshot inconsistency** (for ABR protection groups):
   ```
   Check storage array — verify snapshot exists for the replication group
   SRA may need to re-discover: Site Recovery → Storage → Array Pairs → Discover Devices
   ```

3. **vSphere Replication appliance unreachable**:
   ```bash
   nc -vz vra-protected.example.local 31031
   nc -vz vra-protected.example.local 44046
   # Both should be open
   ```

---

## Test Failover: VMs Fail to Power On

**Symptoms:** Test recovery starts but VMs in isolated network fail to power on or get wrong IP

1. **Network mapping missing**: The test network not mapped to an isolated portgroup
   ```
   Site Recovery → Recovery Plans → [plan] → Test Networks
   Map each protected network to an isolated portgroup at recovery site
   ```

2. **Placeholder VM stale**: Placeholder VM at recovery site has incorrect config
   ```
   # Delete placeholder VM from recovery site vCenter
   # Site Recovery → Protection → [PG] → Configure → adds placeholder VMs back automatically
   ```

3. **Resource pool or datastore insufficient at recovery site**:
   ```
   Check recovery site CPU/RAM/storage capacity before running test
   Verify resource mappings in Site Recovery → Site Pair → Inventory Mappings
   ```

---

## Failback Fails

**Symptoms:** After recovery, re-protect or planned migration back fails

1. **VM not re-protected**: Must run "Reprotect" after DR before failback
   ```
   Site Recovery → Protection → [PG] → Reprotect
   Wait for initial sync to complete (status: OK)
   Then run Planned Migration back to protected site
   ```

2. **Protected site not fully restored**: Protected site vCenter or SRM not running
   ```
   Verify: vCenter at protected site is operational
   Verify: SRM service running at protected site
   Verify: site pairing is Connected
   ```
