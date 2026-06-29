---
tags:
  - troubleshooting
  - vmware
  - vxrail
search:
  boost: 1.5
---
# VxRail — Diagnostics

<div class="kb-summary">
VxRail diagnostic commands: tail VxRail Manager mystic.log and lcm.log, grep ESXi vmkernel.log for vSAN LSOM/DOM errors, collect iDRAC SEL hardware event logs with racadm, and generate the Dell VxRail support bundle via the plugin UI or REST API.

*Applies to: VxRail 7.x / 8.x*
</div>
![VxRail — Diagnostics](../../../../assets/virtualization-vmware-vxrail-troubleshooting-diagnostics.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "SSH mystic@vxrail-manager\nsudo tail -f /var/log/mystic/mystic.log" {shape: rectangle}
D: "sudo tail lcm.log grep error\nCheck upgrade phase: PRECHECK DOWNLOAD STAGING UPGRADE" {shape: rectangle}
E: "vmkernel.log grep LSOM DOM on ESXi\nvSAN Health UI in vCenter" {shape: rectangle}
F: "vmkernel.log grep APD PDL NMP on ESXi\nesxcli storage core path list" {shape: rectangle}
G: "racadm getsel filter critical warning\nracadm getsysinfo filter fault" {shape: rectangle}
H: "hostd.log grep vpxd connect fail\nPing vCenter FQDN from ESXi" {shape: rectangle}
I: "I" {shape: rectangle}
J: "Verify VxRail Manager can reach vCenter: ping vcenter-fqdn\nCheck VxRail Manager service: systemctl status mystic" {shape: rectangle}
K: "Re-register VxRail plugin in vCenter\nCheck VxRail Manager vCenter credentials" {shape: rectangle}
L: "L" {shape: rectangle}
M: "Check failing check name in lcm.log\nResolve pre-check issue and retry LCM" {shape: rectangle}
N: "Check TIMEOUT entries in lcm.log\nVerify iDRAC and ESXi host reachability" {shape: rectangle}
O: "esxcli vsan debug object list on ESXi\nCheck which node hosts the absent component" {shape: rectangle}
P: "esxcli storage core path list for APD paths\nCheck vmnic link status: esxcli network nic list" {shape: rectangle}
Q: "racadm getsel tail 50 for SEL history\nracadm storage get pdisks for disk health" {shape: rectangle}
R: "grep connect refuse /var/log/hostd.log\nCheck management vmk0 IP and gateway" {shape: rectangle}
S: "Generate Dell VxRail support bundle\nOpen Dell support case" {shape: rectangle}
T: "VxRail plugin: Support > Generate Support Bundle\nor REST API: POST /rest/vxm/v1/support/bundle" {shape: rectangle}
A: "VxRail Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
L -> M
L -> N
E -> O
F -> P
G -> Q
H -> R
J -> S
K -> S
M -> S
N -> S
O -> S
P -> S
Q -> S
R -> S
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_vxrail_manager_logs: "Step 1 — Check VxRail Manager logs" {shape: rectangle}
step_2_check_esxi_host_logs: "Step 2 — Check ESXi host logs" {shape: rectangle}
step_3_check_idrac_for_hardware_faul: "Step 3 — Check iDRAC for hardware faults" {shape: rectangle}
step_4_collect_vmsupport_esxi_bundle: "Step 4 — Collect vm-support ESXi bundle" {shape: rectangle}
step_5_generate_dell_vxrail_support_: "Step 5 — Generate Dell VxRail support bundle" {shape: rectangle}
log_locations: "Log locations" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_vxrail_manager_logs: investigate
symptom -> step_2_check_esxi_host_logs: investigate
symptom -> step_3_check_idrac_for_hardware_faul: investigate
symptom -> step_4_collect_vmsupport_esxi_bundle: investigate
symptom -> step_5_generate_dell_vxrail_support_: investigate
symptom -> log_locations: investigate
step_1_check_vxrail_manager_logs -> resolution
step_2_check_esxi_host_logs -> resolution
step_3_check_idrac_for_hardware_faul -> resolution
step_4_collect_vmsupport_esxi_bundle -> resolution
step_5_generate_dell_vxrail_support_ -> resolution
log_locations -> resolution
```

## Before you begin

- **Access:** SSH to VxRail Manager (`mystic@<vxrail-manager-ip>`); ESXi root SSH access; iDRAC SSH or racadm remote access; vCenter admin credentials
- **Gather first:** the specific symptom (plugin error, LCM pre-check name, vSAN health alarm, iDRAC hardware alert), the affected node IP or service tag, and when the issue started
- **Scope:** confirm whether the issue affects one node, one VxRail cluster, or the vCenter-VxRail integration layer

---

## Step 1 — Check VxRail Manager logs

```bash
# SSH to VxRail Manager
ssh mystic@<vxrail-manager-ip>

# List all log files with sizes
sudo ls -lh /var/log/mystic/

# mystic.log — Main VxRail Manager daemon log
sudo tail -500 /var/log/mystic/mystic.log
sudo tail -500 /var/log/mystic/mystic.log | grep -i "error\|exception\|critical\|fail"

# Watch live during active troubleshooting
sudo tail -f /var/log/mystic/mystic.log

# lcm.log — LCM upgrade operations
sudo tail -200 /var/log/mystic/lcm.log | grep -i "error\|fail\|exception\|timeout"

# Find a specific upgrade run by date
sudo grep "2026-06-15" /var/log/mystic/lcm.log | grep -i "error\|fail"

# access.log — REST API call history and error codes
sudo grep " 5[0-9][0-9] " /var/log/mystic/access.log | tail -50   # server errors
sudo grep " 401 " /var/log/mystic/access.log | tail -20            # auth failures
```

LCM phase sequence to check in lcm.log:

| Phase | What to look for |
|---|---|
| PRECHECK | `precheck.*FAIL` — check name tells you what to fix |
| DOWNLOAD | `download.*fail\|bundle.*error` — depot/proxy issue |
| STAGING | `TIMEOUT` — iDRAC or ESXi unreachable during staging |
| UPGRADE | `stage.*failed` — check the specific failing component |
| POSTCHECKS | `postcheck.*fail` — verify node health after upgrade |

---

## Step 2 — Check ESXi host logs

```bash
# SSH to the affected ESXi host
ssh root@<esxi-host-ip>

# vmkernel.log — vSAN storage layer and network errors
tail -200 /var/log/vmkernel.log | grep -i "vsan\|LSOM\|DOM"
tail -200 /var/log/vmkernel.log | grep -i "APD\|PDL\|NMP\|path"
tail -200 /var/log/vmkernel.log | grep -i "vmnic\|uplink\|link down"

# Wider search window
grep -i "LSOM\|error" /var/log/vmkernel.log | tail -200

# hostd.log — Host management and vCenter connection
tail -200 /var/log/hostd.log | grep -i "error\|fail"
grep -i "vpxd\|vCenter\|connect" /var/log/hostd.log | tail -50

# Storage path status
esxcli storage core path list | grep -v "Active"
# Expected: all paths Active; problem: Dead, Standby (unexpected)

# vSAN object list on this host
esxcli vsan debug object list 2>/dev/null | head -30
```

vmkernel.log patterns:

| Pattern | Meaning |
|---|---|
| `LSOM: disk ... failed` | Local disk failure — check iDRAC SEL |
| `DOM: component ... absent` | vSAN object component absent; node may be offline |
| `NMP: no more paths` | All paths dead — PDL condition |
| `APD START` | All Paths Down — storage temporarily unreachable |
| `vmnic ... link state changed to down` | NIC link dropped — check cable or switch port |
| `VSAN: network partition` | Nodes cannot communicate on vSAN vmkernel network |

---

## Step 3 — Check iDRAC for hardware faults

```bash
# SSH to node iDRAC
ssh root@<node-idrac-ip>

# Or use racadm remotely from a management host
racadm -r <idrac-ip> -u root -p <password> getsel

# System Event Log — primary hardware fault source
racadm getsel | tail -50
racadm getsel | grep -i "critical\|warning\|fault"

# Full system summary
racadm getsysinfo | grep -i "fault\|warning\|critical"

# Power supply status
racadm getsysinfo -t pwrsupply

# Fan status (failure causes thermal shutdown)
racadm getsysinfo -t fan

# Disk and RAID controller health
racadm storage get pdisks -o -p State,PredictiveFailureState,MediaType
racadm storage get controllers -o

# NIC link status
racadm getniccfg -n NIC.Integrated.1-1

# Temperature readings
racadm getsysinfo -t temp

# Quick hardware diagnostic test
racadm diagnostics run -t QuickTest
```

SEL patterns to look for:

| SEL Entry | Meaning |
|---|---|
| `Physical Disk ... Predictive Failure` | Disk imminent failure — plan replacement |
| `Physical Disk ... Failed` | Disk has failed — replace immediately |
| `Power Supply ... Failure` | PSU failed — check and replace |
| `Memory ... Correctable ECC` | Single-bit memory error — monitor |
| `Memory ... Uncorrectable ECC` | Multi-bit error — DIMM replacement required |
| `Network interface ... link down` | NIC link lost — check cable and switch |

---

## Step 4 — Collect vm-support ESXi bundle

```bash
# Collect full ESXi diagnostic bundle (does not impact running VMs)
ssh root@<esxi-host-ip>
vm-support -n -w /tmp/
# Duration: 2-5 minutes

# List the generated bundle file
ls -lh /tmp/*.tgz

# SCP to management workstation
scp root@<esxi-host-ip>:/tmp/esx-<hostname>-<timestamp>.tgz ./
```

The vm-support bundle includes: vmkernel.log, hostd.log, vpxa.log, network config, storage config, and running process state.

---

## Step 5 — Generate Dell VxRail support bundle

### Via VxRail plugin (UI path)

Navigate to: **VxRail Plugin → Support → Generate Support Bundle**

Bundle generation takes 10–20 minutes. The download link appears when complete. Contents: VxRail Manager logs, node health data, iDRAC logs, and ESXi log excerpts from all nodes.

### Via VxRail Manager API

```bash
# SSH to VxRail Manager
ssh mystic@<vxrail-manager-ip>

# Trigger bundle generation
curl -sk -X POST \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  -H "Content-Type: application/json" \
  "https://localhost/rest/vxm/v1/support/bundle"
# Returns: JSON with job_id

# Poll job status
curl -sk \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://localhost/rest/vxm/v1/requests/<job-id>" | python3 -m json.tool

# When status = COMPLETED, download the bundle
curl -sk -O \
  -H "Authorization: Basic $(echo -n 'mystic:password' | base64)" \
  "https://localhost/rest/vxm/v1/support/bundle/download"
```

---

## Log locations

| Log Source | Best For | Path / Command |
|---|---|---|
| mystic.log | Plugin errors, API failures | `/var/log/mystic/mystic.log` on VxRail Manager |
| lcm.log | LCM pre-check and upgrade stage failures | `/var/log/mystic/lcm.log` on VxRail Manager |
| access.log | REST API call history | `/var/log/mystic/access.log` on VxRail Manager |
| vmkernel.log | vSAN I/O errors, disk failures, network drops | `/var/log/vmkernel.log` on ESXi host |
| hostd.log | vCenter connectivity, VM operations | `/var/log/hostd.log` on ESXi host |
| iDRAC SEL | Hardware fault timeline | `racadm getsel` against node iDRAC |
| vm-support bundle | Full ESXi snapshot | `vm-support -n -w /tmp/` on ESXi host |
| VxRail support bundle | Full cluster snapshot | VxRail plugin → Support → Generate Support Bundle |

---

## See also

- [VxRail — Common Issues](../common-issues/)
- [VxRail — Escalation](../escalation/)

## Verify resolution

- VxRail plugin loads in vCenter without error; node health shows green in VxRail Manager
- `sudo tail -50 /var/log/mystic/mystic.log` shows no new ERROR entries after the fix
- LCM operation completes: upgrade phases reach POSTCHECKS with no FAIL entries in lcm.log
- `grep -i "LSOM\|DOM\|APD\|PDL" /var/log/vmkernel.log | tail -10` shows no new error events
- iDRAC SEL shows no new Critical events: `racadm getsel | grep -i critical`
- vSAN health UI in vCenter shows all checks green with no warnings
