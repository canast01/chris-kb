---
tags:
  - incident-response
  - operations
  - troubleshooting
---
# Incident Response Playbooks

<div class="kb-summary">
Structured response playbooks for the most common infrastructure incidents. Each playbook follows the same Triage → Isolate → Diagnose → Fix → Verify → Document structure.
</div>

<div class="kb-grid">
<a class="kb-card" href="vcenter-unreachable/">
<strong>INC-001: vCenter Server Unreachable</strong><br>
P1 — vCenter is not responding to client connections. Covers service restart, VM recovery, and backup restore paths.
</a>
<a class="kb-card" href="storage-array-full/">
<strong>INC-002: Storage Array / Datastore Full</strong><br>
P1/P2 — Datastore or array at capacity, VMs pausing or failing writes. Covers ONTAP, vSAN, and PowerCLI remediation.
</a>
<a class="kb-card" href="ransomware-detection/">
<strong>INC-003: Ransomware / Crypto Attack Detected</strong><br>
P0 — Active encryption attack in progress. Covers network isolation, evidence preservation, and immutable backup recovery.
</a>
<a class="kb-card" href="replication-lag-alert/">
<strong>INC-004: Replication Lag / DR Gap Alert</strong><br>
P2/P1 — SnapMirror or RecoverPoint lag exceeds RPO target. Covers ONTAP SnapMirror diagnosis and forced update.
</a>
<a class="kb-card" href="host-disconnected/">
<strong>INC-005: ESXi Host Disconnected from vCenter</strong><br>
P1/P2 — ESXi host shows Not Responding in vCenter. Covers management agent restart, VM evacuation, and HA verification.
</a>
</div>
