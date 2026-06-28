---
tags:
  - operations
  - san
---
# Cisco Nexus Dashboard — Operations Common Issues
![Cisco Nexus Dashboard — Operations Common Issues](../../../../assets/san-cisco-nexus-dashboard-operations-common-issues.svg)


```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check cluster health
acs health

# Show node detail
acs nodes list

# Check if Kubernetes agrees with ND's view
kubectl get nodes
# Expected: all nodes Ready

# Check failing pods on the affected node
kubectl get pods --all-namespaces --field-selector spec.nodeName=<node-hostname> | grep -v Running
```

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Test remote backup connectivity
acs backup remote test

# Check backup status and last error
acs backup status

# Check backup logs
acs system logs --component backup --tail 50
```

```d2
direction: right

hub: "Nexus Dashboard\nOperations" {shape: hexagon}
verify: "Verify" {shape: rectangle}

hub -> verify
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Nexus Dashboard: Fabric Alerts, Severity, Acknowledgement, and Notification Policies](alerts.md)
- [Cisco Nexus Dashboard — Operations Backup & Restore](backup-restore.md)
- [Cisco Nexus Dashboard — Operations CLI Reference](cli-reference.md)
- [Nexus Dashboard — Operations](index.md)
- [Nexus Dashboard — Architecture](../architecture/)
- [Nexus Dashboard — Initial Deployment](../deploy/)
- [Nexus Dashboard — Security](../security/)
- [Cisco Nexus Dashboard — Troubleshooting](../troubleshooting/)
