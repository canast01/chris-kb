---
tags:
  - troubleshooting
  - vmware
  - vsphere-replication
search:
  boost: 1.5
---
# vSphere Replication — Common Issues
![vSphere Replication — Common Issues](../../../../assets/virtualization-vmware-vsphere-replication-troubleshooting-co.svg)

```text
   Configure Replication → Step 4: Seeds → Use existing data
   ```

3. **Schedule full sync during low-traffic window**: VR throttles to available bandwidth

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
replication_fails_with_connection_re: "Replication Fails with 'Connection Refused' / 'Connection Ti" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> replication_fails_with_connection_re: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
replication_fails_with_connection_re -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
B1: "Replication paused or stopped" {shape: rectangle}
B2: "RPO violation amber or red" {shape: rectangle}
B3: "Connection refused or initial sync stalled" {shape: rectangle}
B4: "Site pair disconnected" {shape: rectangle}
B5: "No datastore available for target" {shape: rectangle}
B6: "Certificate mismatch between sites" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Start HMS/VRMS Services · Check TCP 44046\n→ Replication Fails" {shape: rectangle}
R2: "Check Cert Thumbprints · Re-pair Sites\n→ Replication Fails" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Apply QoS · Raise RPO Value\n→ RPO Violation" {shape: rectangle}
R4: "Check ESXi CPU Ready · VRA Disk Full\n→ RPO Violation" {shape: rectangle}
R5: "Check TCP 31031 · Route to VRA · Seed Pre-copy\n→ Replication Fails with Connection Refused" {shape: rectangle}
R6: "Check VRA Services · Port 44046 · Cert Thumbprints\n→ Site Pair Disconnected" {shape: rectangle}
R7: "Mount Target Datastore · Free Space\n→ No Datastore Available" {shape: rectangle}
R8: "Refresh Thumbprints in vCenter · Re-register VRMS\n→ Site Pair Disconnected" {shape: rectangle}

S -> B1
S -> B2
S -> B3
S -> B4
S -> B5
S -> B6
D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
B3 -> R5
B4 -> R6
B5 -> R7
B6 -> R8
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Replication Fails with "Connection Refused" / "Connection Timeout"

**Symptoms:** Replication status error: network connectivity to target VRA

```bash
# From source ESXi host shell:
nc -vz vra-amsterdam.example.local 31031
# If connection refused → firewall blocking TCP 31031
# If timeout → no route to target VRA

# Verify from ESXi:
vmkping -I vmk0 <target-VRA-IP>
```
```bash
ssh admin@vra-london.example.local
df -h
# Check /opt partition — VRA appliance partition

# Clear old log files if disk is full:
sudo find /opt/vmware/logs -name "*.log" -mtime +30 -delete
sudo journalctl --vacuum-size=500M
```
```bash
vCenter → [VRA VM] → Edit Settings → Disk → increase size
Then expand filesystem inside VRA:
  sudo growpart /dev/sda 1
  sudo resize2fs /dev/sda1
```

---

## See also

- [vSphere Replication — Diagnostics](../diagnostics/)
- [vSphere Replication — Escalation](../escalation/)
- [vSphere Replication — Health Checks](../../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
