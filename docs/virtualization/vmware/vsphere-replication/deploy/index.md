---
tags:
  - deployment
  - vmware
  - vsphere-replication
search:
  boost: 1.5
---
# vSphere Replication — Deploy

<div class="kb-summary">
End-to-end deployment guide for vSphere Replication. Covers VRA OVA deployment at source and target sites, vCenter registration, site pairing, per-VM replication configuration with RPO and MPIT settings, and RPO compliance validation.

*Applies to: vSphere Replication 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_predeployment_checks: "Phase 1 — Pre-Deployment Checks" {shape: rectangle}
phase_2_vra_deployment_source_site: "Phase 2 — VRA Deployment: Source Site" {shape: rectangle}
phase_3_vra_deployment_target_site_a: "Phase 3 — VRA Deployment: Target Site and Site Pairing" {shape: rectangle}
phase_4_configure_vm_replication: "Phase 4 — Configure VM Replication" {shape: rectangle}
phase_5_monitor_rpo_compliance: "Phase 5 — Monitor RPO Compliance" {shape: rectangle}
phase_6_endtoend_validation: "Phase 6 — End-to-End Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_predeployment_checks
phase_1_predeployment_checks -> phase_2_vra_deployment_source_site
phase_2_vra_deployment_source_site -> phase_3_vra_deployment_target_site_a
phase_3_vra_deployment_target_site_a -> phase_4_configure_vm_replication
phase_4_configure_vm_replication -> phase_5_monitor_rpo_compliance
phase_5_monitor_rpo_compliance -> phase_6_endtoend_validation
phase_6_endtoend_validation -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Pre-Deployment Checks

**Exit criterion:** Network ports verified, DNS confirmed, NTP synchronized, target datastore capacity assessed, inter-site latency measured.

### Network Port Validation

vSphere Replication requires the following ports between sites. Confirm with your firewall team before deployment.

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 31031 | TCP | Source ESXi hosts → Target VRA | Replication data stream (hbrsvc → HMS) |
| 44046 | TCP | VRA ↔ VRA (both directions) | VRA-to-VRA management and site pairing |
| 443 | HTTPS | VRA → vCenter (both sites) | VRA registration and vCenter API |
| 8043 | HTTPS | vCenter → VRA (both sites) | vCenter plugin calling VR management API |
| 5480 | HTTPS | Admin → VRA | VAMI appliance management UI |

```bash
# Test port 31031 from source ESXi host to target VRA IP (after VRA deployed)
# Run from source ESXi host SSH session:
nc -zv <target-VRA-IP> 31031

# Test VRA pairing port 44046
nc -zv <remote-VRA-IP> 44046

# Test from management workstation (pre-VRA deployment)
# Use a temporary test host to verify firewall rules are open
nc -zv <target-site-management-IP> 443
```


```text title="Expected output"
Connection to 192.168.100.45 31031 port [tcp/*] succeeded!
Connection to 192.168.100.46 44046 port [tcp/*] succeeded!
Connection to 10.50.12.8 443 port [tcp/*] succeeded!
```

!!! warning "Common errors"
    **`nc: connect to 192.168.100.45 port 31031 (tcp) failed: Connection refused`** — Verify the VRA is fully deployed and the vSphere Replication service is running on the target host.
    **`nc: connect to 192.168.100.45 port 31031 (tcp) failed: Connection timed out`** — Check that firewall rules allow port 31031 between source and target ESXi hosts, and that the target IP is reachable.
    **`command not found: nc`** — Install netcat using `esxcli software vib install -v /tmp/netcat.vib` or use `telnet <IP> <port>` as an alternative connectivity test.
### DNS Validation

```bash
# VRA FQDNs must resolve from both sites before deployment
nslookup vra-siteA.example.local
nslookup vra-siteB.example.local

# Verify PTR records also exist
nslookup <planned VRA site-A IP>
nslookup <planned VRA site-B IP>
```


```text title="Expected output"
Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	vra-siteA.example.local
Address: 192.168.10.45

Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	vra-siteB.example.local
Address: 192.168.20.48

Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	host-vra-siteA.example.local
Address: 192.168.10.45

Server:		10.0.1.10
Address:	10.0.1.10#53

Name:	host-vra-siteB.example.local
Address: 192.168.20.48
```

!!! warning "Common errors"
    **`** server can't find vra-siteA.example.local: NXDOMAIN`** — Add the VRA FQDNs to your DNS zone file or create A records in your DNS server before proceeding.
    **`** server can't find 192.168.10.45.in-addr.arpa: NXDOMAIN`** — Configure reverse DNS (PTR) records for both VRA IP addresses in your DNS reverse zone.
    **`connection timed out; try again`** — Verify DNS server 10.0.1.10 is reachable and responding; check firewall rules blocking UDP port 53.
### Inter-Site Latency Check

```bash
# Measure round-trip latency between sites (must be ≤ 200 ms for stable replication)
# Run from source ESXi host to target site management IP
ping -c 20 <target-site-gateway-or-host-IP>
# Maximum acceptable: 200 ms average RTT; excessive jitter causes RPO violations
```


```text title="Expected output"
PING 10.50.12.1 (10.50.12.1) 56(84) bytes of data.
64 bytes from 10.50.12.1: icmp_seq=1 ttl=64 time=45.2 ms
64 bytes from 10.50.12.1: icmp_seq=2 ttl=64 time=46.1 ms
64 bytes from 10.50.12.1: icmp_seq=3 ttl=64 time=45.8 ms
64 bytes from 10.50.12.1: icmp_seq=4 ttl=64 time=47.3 ms
64 bytes from 10.50.12.1: icmp_seq=5 ttl=64 time=45.9 ms
64 bytes from 10.50.12.1: icmp_seq=6 ttl=64 time=48.2 ms
64 bytes from 10.50.12.1: icmp_seq=7 ttl=64 time=46.5 ms
64 bytes from 10.50.12.1: icmp_seq=8 ttl=64 time=49.1 ms
...
64 bytes from 10.50.12.1: icmp_seq=20 ttl=64 time=46.8 ms

--- 10.50.12.1 statistics ---
20 packets transmitted, 20 received, 0% packet loss, time 19234ms
rtt min/avg/max/stddev = 45.2/46.8/49.1/1.2 ms
```

!!! warning "Common errors"
    **`ping: unknown host <target-site-gateway-or-host-IP>`** — Replace the placeholder with an actual IP address or resolvable hostname (e.g., `10.50.12.1` or `dr-gateway.corp.local`).
    **`100% packet loss`** — Verify network connectivity between sites, check firewall rules allow ICMP, and confirm the target IP is reachable from the source ESXi host.
    **`rtt min/avg/max/stddev = .../250.5/...`** — Average RTT exceeds 200 ms threshold; investigate WAN link congestion, increase bandwidth, or optimize routing before deploying replication.
### Target Datastore Capacity Estimate

Estimate target storage required:

```text
Per replicated VM:
  - Base replica disk: same size as source VMDK
  - MPIT delta disks: (write rate × RPO × MPIT count)
  
Example (3 VMs, 200 GB each, 1 hr RPO, 3 MPIT):
  Base:   3 × 200 GB = 600 GB
  Deltas: 3 × (avg 5 GB per cycle × 3 instances) = 45 GB
  Total:  ~650 GB minimum; add 20% safety margin
```

---

## Phase 2 — VRA Deployment: Source Site

**Exit criterion:** Source site VRA deployed, registered with source vCenter, and VR plugin visible in vSphere Client.

### Deploy VRA OVA at Source Site

```text
vCenter (source site) → Deploy OVF Template
  Source: VMware-vSphere-Replication-<version>.ovf

  Step 1: VM name and folder
    Name: vra-siteA
    Folder: Infrastructure VMs

  Step 2: Compute resource
    Select: host or cluster for the VRA VM

  Step 3: Storage
    Storage policy: default
    Datastore: management datastore (≥ 20 GB free)

  Step 4: Network
    Network: Management portgroup

  Step 5: Customize template
    Hostname: vra-siteA.example.local
    IP Address: 10.10.10.50
    Subnet Mask: 255.255.255.0
    Default Gateway: 10.10.10.1
    DNS Server: 10.10.10.53
    NTP Server: ntp.example.local
    Admin password: <strong password>
    Root password: <strong password>
    → Deploy (~5 minutes)
```

### Register VRA with Source vCenter

```text
VRA VAMI: https://vra-siteA.example.local:5480
  Login: admin / <password>
  Configuration → vCenter Server
    vCenter Address: vcenter-siteA.example.local
    vCenter Port: 443
    SSO Admin Username: administrator@vsphere.local
    SSO Admin Password: <password>
    → Register
    Accept vCenter certificate thumbprint → OK
```

### Verify Registration

```bash
# Verify VR plugin is active in vSphere Client
# vSphere Client → Menu → Site Recovery
# VRA should appear as a Replication Appliance

# Verify HMS and VRMS services on VRA
ssh admin@vra-siteA.example.local
systemctl status hms
systemctl status vrms
# Both should show: active (running)
```


```text title="Expected output"
admin@vra-siteA.example.local's password: 
● hms.service - HMS Service
     Loaded: loaded (/etc/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 45min ago
       Docs: https://docs.vmware.com/en/vSphere-Replication
    Process: 2847 ExecStart=/opt/vmware/hms/bin/hms.sh start (code=exited, status=0/SUCCESS)
   Main PID: 2891 (java)
      Tasks: 28 (limit: 4915)
     Memory: 512.3M
        CPU: 2min 14.328s
     CGroup: /system.slice/hms.service
             └─2891 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java -Xmx1024m

● vrms.service - VRMS Service
     Loaded: loaded (/etc/systemd/system/vrms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:33:05 UTC; 2h 44min ago
       Docs: https://docs.vmware.com/en/vSphere-Replication
    Process: 2956 ExecStart=/opt/vmware/vrms/bin/vrms.sh start (code=exited, status=0/SUCCESS)
   Main PID: 3012 (java)
      Tasks: 31 (limit: 4915)
     Memory: 768.1M
        CPU: 3min 42.891s
     CGroup: /system.slice/vrms.service
             └─3012 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java -Xmx2048m
```

!!! warning "Common errors"
    **`Unit hms.service could not be found.`** — Verify VRA was deployed correctly by checking `/opt/vmware/hms/` exists; if missing, redeploy the VRA OVA.
    **`Connection refused`** — Ensure SSH is enabled on the VRA and the hostname/IP is reachable; verify network connectivity with `ping vra-siteA.example.local` first.
    **`Active: inactive (dead)`** — Restart the service with `systemctl restart hms` and check logs via `journalctl -u hms -n 50` to identify the root cause.
---

## Phase 3 — VRA Deployment: Target Site and Site Pairing

**Exit criterion:** Target site VRA deployed and registered; site pair established between both VRAs; both sites visible in vSphere Client Site Recovery.

### Deploy VRA OVA at Target Site

Deploy using the same procedure as Phase 2 but targeting the recovery site:

```text
VRA name: vra-siteB
IP: 10.20.10.50 (example target site IP)
vCenter to register with: vcenter-siteB.example.local
```

```bash
# Verify target VRA services
ssh admin@vra-siteB.example.local
systemctl status hms
systemctl status vrms
```


```text title="Expected output"
admin@vra-siteB.example.local's password: 
● hms.service - vSphere Replication Management Service
     Loaded: loaded (/etc/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2h 45min ago
       Docs: https://docs.vmware.com/en/vSphere-Replication/
    Process: 2847 ExecStart=/opt/vmware/hms/bin/hms.sh start (code=exited, status=0/SUCCESS)
   Main PID: 2891 (java)
      Tasks: 28 (limit: 4915)
     Memory: 512.3M
        CPU: 2min 34.821s
     CGroup: /system.slice/hms.service
             └─2891 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java -Xmx1024m...

● vrms.service - vSphere Replication Management Server
     Loaded: loaded (/etc/systemd/system/vrms.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:33:02 UTC; 2h 44min ago
       Docs: https://docs.vmware.com/en/vSphere-Replication/
    Process: 3156 ExecStart=/opt/vmware/vrms/bin/vrms.sh start (code=exited, status=0/SUCCESS)
   Main PID: 3201 (java)
      Tasks: 42 (limit: 4915)
     Memory: 1.2G
        CPU: 5min 12.340s
     CGroup: /system.slice/vrms.service
             └─3201 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java -Xmx2048m...
```

!!! warning "Common errors"
    **`Unit hms.service could not be found.`** — Verify VRA is installed on this host by checking `/opt/vmware/hms/` exists, or confirm you are connecting to the correct VRA appliance.
    **`Connection refused`** — Ensure SSH is enabled on the VRA appliance and the admin account credentials are correct; check network connectivity to vra-siteB.example.local.
    **`● hms.service - vSphere Replication Management Service ... Active: inactive (dead)`** — Restart the service with `sudo systemctl restart hms` and check logs via `sudo journalctl -u hms -n 50` for startup errors.
### Pair the Sites

```text
vCenter (source site) → Menu → Site Recovery → New Site Pair

  Step 1: Site pair details
    PSC / vCenter Server of remote site: vcenter-siteB.example.local
    SSO username: administrator@vsphere.local
    SSO password: <remote vCenter SSO password>

  Step 2: Remote site services
    Select VRA: vra-siteB.example.local
    Accept certificate thumbprints for:
      - Remote vCenter
      - Remote VRA (vra-siteB)
    → Pair

  Pairing completes in ~2 minutes
```

### Verify Site Pair

```bash
# Check pairing status via VRA API
curl -sk -u admin:<password> \
  https://vra-siteA.example.local:8043/api/sites \
  | python3 -m json.tool | grep -E '"name"|"status"'
# Expected: both sites listed, status Connected

# In vSphere Client: Site Recovery → Sites
# Both sites should show: Connected
```


```text title="Expected output"
{
  "name": "Site-A",
  "status": "Connected"
}
{
  "name": "Site-B",
  "status": "Connected"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the VRA's CA certificate into your system trust store.
    **`curl: (7) Failed to connect to vra-siteA.example.local port 8043: Connection refused`** — Verify the VRA appliance is running, the hostname resolves correctly, and port 8043 is accessible from your client (check firewall rules and VRA service status).
---

## Phase 4 — Configure VM Replication

**Exit criterion:** At least one test VM fully configured for replication; initial sync completed; status shows Syncing or OK.

### Configure Replication on a VM

```text
vSphere Client → [source VM] → right-click → Configure Replication
  (or: Site Recovery → Replications → New Replication)

  Step 1: Target site
    Replication type: vSphere Replication
    Target site: siteB (paired site)

  Step 2: Target location
    Target datastore: ds-siteB-replica (target datastore)
    Target folder: Replicas (optional subfolder)

  Step 3: Replication settings
    RPO: 1 hour  (minimum 5 minutes; maximum 24 hours)
    Enable multiple point in time (MPIT): Yes
    Instances: 3  (range 1–24)
    Quiesce: Yes (requires VMware Tools — application-consistent)
    Network compression: Yes (recommended for WAN links)

  Step 4: Recovery settings
    Network mapping: leave default or specify target portgroup

  Step 5: Review → Finish
```

### Monitor Initial Full Sync

```bash
# vSphere Client → Site Recovery → Replications
# Status: "Initial Full Sync" → progress percentage shown
# Large disks may take hours over WAN; can seed from backup media to reduce transfer

# Check hbrsvc on source ESXi host (SSH to ESXi)
esxcli hbr replication list
# Expected: VM listed with state "SYNCING"

esxcli hbr replication getstate
# Shows per-VM replication stats including bytes transferred
```


```text title="Expected output"
Virtual Machine: vm-prod-db-01
State: SYNCING
RPO: 3600
Source: 192.168.1.45
Target: 192.168.2.50
Replication Rate: 45.2 MB/s

Virtual Machine: vm-web-frontend
State: SYNCING
RPO: 1800
Source: 192.168.1.46
Target: 192.168.2.51
Replication Rate: 12.8 MB/s

VM Name: vm-prod-db-01
Bytes Transferred: 847362891776
Bytes Remaining: 1253698541056
Percentage Complete: 40.3%
Elapsed Time: 14h 22m
Estimated Time Remaining: 21h 15m
```

!!! warning "Common errors"
    **`Error: Unable to connect to hbrsvc`** — Verify the vSphere Replication appliance is running and network connectivity exists between source and target sites.
    **`Error: No replication found for VM`** — Confirm the replication was successfully configured in vSphere Client under Site Recovery and the VM is powered on.
### Configure Multiple VMs (Batch)

```powershell
# PowerCLI: configure replication for all VMs in a folder
Connect-VIServer vcenter-siteA.example.local
$vms = Get-VM -Location (Get-Folder "Production-VMs")
foreach ($vm in $vms) {
    $vm | Get-VmReplication  # check if already configured
    # Use vSphere Replication API or Site Recovery UI for batch config
}
```

---

## Phase 5 — Monitor RPO Compliance

**Exit criterion:** All configured VMs showing RPO status OK (green); no persistent violations; bandwidth usage within capacity.

### Check RPO Status

```bash
# vSphere Client → Site Recovery → Replications
# Each VM shows RPO status:
#   Green (OK):     last sync within configured RPO window
#   Yellow (Warn):  >80% of RPO elapsed since last sync
#   Red (Error):    RPO violated — most recent recovery point is stale

# Check VRMS logs for replication errors
ssh admin@vra-siteA.example.local
tail -100 /var/log/vmware/vrms/vrms.log | grep -i "error\|warn\|violation"

# Check HMS logs (data reception at target)
ssh admin@vra-siteB.example.local
tail -100 /var/log/vmware/hms/hms.log | grep -i "error\|warn"
```


```text title="Expected output"
admin@vra-siteA.example.local's password: 
2024-01-15 14:32:18.456 [VRMS] WARNING: Replication lag detected for VM 'prod-db-01' — 45 minutes elapsed, RPO target 30 minutes
2024-01-15 14:28:03.122 [VRMS] ERROR: Failed to send checkpoint for VM 'web-app-03' to target site — network timeout after 120s
2024-01-15 14:15:47.891 [VRMS] WARNING: Bandwidth throttling active — replication queue depth at 87% capacity
2024-01-15 13:52:14.334 [VRMS] ERROR: Snapshot consolidation failed on VM 'backup-srv-02' — insufficient storage on replica datastore
2024-01-15 13:41:09.567 [VRMS] WARNING: RPO violation imminent for VM 'mail-exchange' — 28 of 30 minute window consumed

admin@vra-siteB.example.local's password: 
2024-01-15 14:33:52.789 [HMS] WARNING: Received out-of-order checkpoint sequence for VM 'prod-db-01' — reordering buffer engaged
2024-01-15 14:29:15.445 [HMS] ERROR: Disk write failed on replica VM 'web-app-03' — target datastore 'ds-replica-02' at 94% capacity
2024-01-15 14:18:33.221 [HMS] WARNING: Network latency spike detected — 250ms RTT to source site
2024-01-15 14:05:47.612 [HMS] ERROR: Failed to apply snapshot for VM 'backup-srv-02' — quiesced snapshot timed out after 180s
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Verify SSH credentials and ensure the vRA appliance user account is enabled; check `/etc/ssh/sshd_config` for PasswordAuthentication setting.
    **`tail: cannot open '/var/log/vmware/vrms/vrms.log' for reading: No such file or directory`** — Confirm the vSphere Replication Management Server is running with `systemctl status vmware-vrms` and check actual log path with `find /var/log -name '*vrms*'`.
    **`grep: (standard input): Permission denied`** — Run the command with `sudo` or ensure the admin user has read permissions on `/var/log/vmware/*/` directories via `sudo usermod -aG adm admin`.
### Verify hbrsvc on Source ESXi Hosts

```bash
# SSH to a source ESXi host
ssh root@esxi-siteA-01.example.local

# List active replications
esxcli hbr replication list

# Show detailed state (including last sync time and next expected sync)
esxcli hbr replication getstate

# Check hbr kernel module is loaded
vmkload_mod -l | grep hbr
# Expected: hbr module present

# View hbr log
tail -50 /var/log/hbr.log | grep -i "error\|warn"
```


```text title="Expected output"
root@esxi-siteA-01.example.local:~]
esxcli hbr replication list
VM Name                          State      RPO Status
-------------------------------- ---------- -----------
prod-web-01                      Syncing    On Schedule
prod-db-02                       Syncing    On Schedule
dev-app-03                       Idle       On Schedule

esxcli hbr replication getstate
VM: prod-web-01
  State: Syncing
  Last Sync Time: 2024-01-15 14:32:18 UTC
  Next Expected Sync: 2024-01-15 14:37:18 UTC
  Data Transferred: 2.3 GB
  Sync Duration: 4m 22s

vmkload_mod -l | grep hbr
hbr                                 1  0x4200000000 0x1000000 /usr/lib/vmkmod/hbr

tail -50 /var/log/hbr.log | grep -i "error\|warn"
2024-01-15T14:31:02Z warn: Replication lag detected for prod-web-01: 45 seconds
2024-01-15T14:25:14Z warn: Network bandwidth throttled to 50 Mbps
```

!!! warning "Common errors"
    **`esxcli hbr replication list: Unknown command or namespace hbr`** — Verify vSphere Replication is installed on the ESXi host by checking `/etc/vmware/vpx/vpxa.cfg` or reinstall the VR agent.
    **`vmkload_mod: Command not found`** — Use the correct command `vmkload_mod -l` or check the ESXi version; on some versions use `esxcli system module list | grep hbr` instead.
    **`tail: /var/log/hbr.log: No such file or directory`** — Confirm vSphere Replication services are running with `service hbrsrv status` and check `/var/log/vmkernel.log` for initialization errors.
### Configure Replication Alerts

```text
vSphere Client → [VM] → Monitor → vSphere Replication → Manage Notifications
  Add email notification for: RPO violation, replication error, full sync triggered
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All replication health checks pass. RPO met. MPIT snapshots present. Sign off.

### Verify All VM RPO Status

```bash
# All replicated VMs should show green RPO status
# vSphere Client → Site Recovery → Replications
# Filter: Status = Error or Warning → resolve before sign-off

# Check replication lag via VRA API
curl -sk -u admin:<password> \
  https://vra-siteA.example.local:8043/api/vms \
  | python3 -m json.tool | grep -E '"vmName"|"rpoStatus"|"lastReplicationTime"'
```


```text title="Expected output"
{
  "vmName": "prod-db-01",
  "rpoStatus": "Green",
  "lastReplicationTime": "2024-01-15T14:32:18Z"
}
{
  "vmName": "prod-web-02",
  "rpoStatus": "Green",
  "lastReplicationTime": "2024-01-15T14:31:45Z"
}
{
  "vmName": "prod-app-03",
  "rpoStatus": "Yellow",
  "lastReplicationTime": "2024-01-15T14:15:22Z"
}
{
  "vmName": "prod-cache-04",
  "rpoStatus": "Green",
  "lastReplicationTime": "2024-01-15T14:33:01Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example; if error persists, verify VRA hostname matches certificate CN).
    **`curl: (7) Failed to connect to vra-siteA.example.local port 8043: Name or service not known`** — Confirm VRA hostname is resolvable and port 8043 is accessible from your network location using `nslookup vra-siteA.example.local` and `telnet vra-siteA.example.local 8043`.
    **`jq: parse error: Invalid JSON text at line 1`** — Verify API authentication credentials are correct and the VRA service is running; test with `curl -sk -u admin:<password> https://vra-siteA.example.local:8043/api/health` first.
### Verify MPIT Recovery Points

```bash
# Verify MPIT snapshots captured at target site
# vSphere Client → Site Recovery → Replications → [VM] → Recovery Points
# Multiple instances should be listed (matching configured MPIT count)

# Check target datastore for replica VMDK structure
# Target datastore should contain:
#   <vm-name>.vmdk         (base replica)
#   <vm-name>-000001.vmdk  (delta disk for recovery point 1)
#   <vm-name>-000002.vmdk  (delta disk for recovery point 2)
```

### Test Planned Migration (Non-Destructive)

```bash
# Test recovery using a test VM (not production) before sign-off
# vSphere Client → Site Recovery → Replications → [test VM] → Migrate

# Planned migration (graceful):
#   1. Source VM quiesced and final sync triggered
#   2. VM powered off at source
#   3. Replica promoted to running VM at target
#   4. Verify VM boots and application responds

# After test: reprotect VM to resume replication
# vSphere Client → [migrated VM at target] → Configure Replication (back to source)
```

### VRA Service Health

```bash
# Both site VRAs: verify HMS and VRMS healthy
ssh admin@vra-siteA.example.local
systemctl status hms vrms
# Both: active (running)

ssh admin@vra-siteB.example.local
systemctl status hms vrms
# Both: active (running)

# Verify VRA API health endpoint
curl -sk https://vra-siteA.example.local/api/rest/vr/health
curl -sk https://vra-siteB.example.local/api/rest/vr/health
# Expected: {"status":"OK"} or equivalent healthy response
```


```text title="Expected output"
● hms.service - Hybrid Management Service
     Loaded: loaded (/usr/lib/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 8 days ago
   Main PID: 2847 (java)
      Tasks: 47 (limit: 4915)
     Memory: 512.3M
     CGroup: /system.slice/hms.service
             └─2847 /usr/lib/jvm/java-11-openjdk-11.0.18.10-1.el7_9.x86_64/bin/java

● vrms.service - vSphere Replication Management Service
     Loaded: loaded (/usr/lib/systemd/system/vrms.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:33:05 UTC; 8 days ago
   Main PID: 3156 (java)
      Tasks: 52 (limit: 4915)
     Memory: 768.1M

● hms.service - Hybrid Management Service
     Loaded: loaded (/usr/lib/systemd/system/hms.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 09:15:42 UTC; 7 days ago
   Main PID: 4521 (java)
      Tasks: 48 (limit: 4915)
     Memory: 501.7M

● vrms.service - vSphere Replication Management Service
     Loaded: loaded (/usr/lib/systemd/system/vrms.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2024-01-18 09:16:11 UTC; 7 days ago
   Main PID: 4892 (java)
      Tasks: 51 (limit: 4915)
     Memory: 755.4M

{"status":"OK","version":"8.7.0.1","build":"21457896","timestamp":"2024-01-25T10:42:33.847Z"}
{"status":"OK","version":"8.7.0.1","build":"21457896","timestamp":"2024-01-25T10:42:34.102Z"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, but ensure it's included if removed).
    **`Connection refused`** — Verify the VRA API service is listening on port 443 by running `netstat -tlnp | grep 443` and restart vrms if needed with `systemctl restart vrms`.
    **`Active: inactive (dead)`** — Start the service with `systemctl start hms vrms` and check logs with `journalctl -u hms -n 50` to diagnose startup failures.
### Post-Deployment Checklist

| Item | Check |
|---|---|
| Source VRA | Registered with source vCenter; VRMS running |
| Target VRA | Registered with target vCenter; HMS and VRMS running |
| Site pair | Both sites show Connected in Site Recovery |
| Ports 31031/44046 | Open between sites; confirmed with nc tests |
| Inter-site latency | < 200 ms average RTT |
| Initial sync | All configured VMs completed initial full sync |
| RPO compliance | All VMs green (OK) RPO status |
| MPIT snapshots | Recovery point instances present at target |
| DNS | VRA FQDNs resolve from both sites forward and reverse |
| NTP | VRA appliances and vCenter drift < 5 seconds |
| Alerts | Email notifications configured for RPO violations |
| Target datastore | Adequate free space; < 70% used |
| Recovery test | Planned migration test completed on test VM |

---

## See also

- [vSphere Replication — How It Works](../architecture/how-it-works/)
- [vSphere Replication — Health Checks](../operations/health-checks/)
- [vSphere Replication — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
