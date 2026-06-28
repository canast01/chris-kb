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

```mermaid
graph TD
    S([What is the symptom?]) --> B1[Replication paused or stopped]
    S --> B2[RPO violation amber or red]
    S --> B3[Connection refused or initial sync stalled]
    S --> B4[Site pair disconnected]
    S --> B5[No datastore available for target]
    S --> B6[Certificate mismatch between sites]

    B1 --> D1{VRA appliance\nreachable?}
    D1 -->|No| R1[Start HMS/VRMS Services · Check TCP 44046\n→ Replication Fails]
    D1 -->|Yes| R2[Check Cert Thumbprints · Re-pair Sites\n→ Replication Fails]

    B2 --> D2{WAN bandwidth\nsaturated?}
    D2 -->|Yes| R3[Apply QoS · Raise RPO Value\n→ RPO Violation]
    D2 -->|No| R4[Check ESXi CPU Ready · VRA Disk Full\n→ RPO Violation]

    B3 --> R5[Check TCP 31031 · Route to VRA · Seed Pre-copy\n→ Replication Fails with Connection Refused]

    B4 --> R6[Check VRA Services · Port 44046 · Cert Thumbprints\n→ Site Pair Disconnected]

    B5 --> R7[Mount Target Datastore · Free Space\n→ No Datastore Available]

    B6 --> R8[Refresh Thumbprints in vCenter · Re-register VRMS\n→ Site Pair Disconnected]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class D1,D2 decision
    class S start
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

- [vSphere Replication — Diagnostics](diagnostics/)
- [vSphere Replication — Escalation](escalation/)
- [vSphere Replication — Health Checks](../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
