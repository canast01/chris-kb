# Nexus Dashboard — Known Issues

> Part of the [Nexus Dashboard](../../index.md) reference. For deeper diagnosis, see [Troubleshooting > Common Issues](../../troubleshooting/common-issues/index.md).

---

## Overview

Quick reference for operational issues encountered during Nexus Dashboard and NDFC day-to-day management.

---

## ND Cluster Node Shows Unhealthy

**Symptom:** One or more nodes in **Admin Console > Infrastructure > Nodes** shows **Degraded**, **Unavailable**, or **Unknown**.

**Diagnosis:**

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
┌────────────────────────── Cisco Nexus Dashboard — Operations Common Issues ───────────────────────────┐
│                                                                                                       │
│  Frequent ND operational issues: cluster quorum loss, app failures, site disconnects.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Cluster Issues                │  │                 App Failures                │   │
│   │          Quorum lost: 2 nodes down           │  │            NDFC pod crash-looping           │   │
│   │       etcd split-brain: net partition        │  │         NDI no telemetry: gRPC down         │   │
│   │        Node offline: NIC/cable fault         │  │         NDO deploy stuck: APIC busy         │   │
│   │        Disk full: log or data volume         │  │           OOM: pod evicted by K8s           │   │
│   │       NTP drift: cert validation fail        │  │          App upgrade failed: retry          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Cluster health checked first; then app-level pod logs for targeted troubleshooting                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Site Connectivity Issues           │  │               Resolution Steps              │   │
│   │        Site unreachable: REST timeout        │  │          acs health: cluster state          │   │
│   │         Cred expired: 401 from APIC          │  │         acs logs: pod error messages        │   │
│   │         SSL cert expired: handshake          │  │         kubectl describe pod detail         │   │
│   │          Firewall: port 443 blocked          │  │          Renew cert or rotate creds         │   │
│   │        Version mismatch: app incompat        │  │         TAC: if quorum unrecoverable        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · management switches · APIC cluster · NTP server · firewall                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Quorum         = Minimum node count for cluster consensus; loss stops all writes                     │
│  etcd           = K8s state store; split-brain means two halves disagree on state                     │
│  Split-brain    = Network partition causing cluster halves to diverge independently                   │
│  Crash-loop     = Pod repeatedly starting and failing; check logs for root cause                      │
│  OOM            = Out Of Memory; Kubernetes evicts pod when node memory exhausted                     │
│  gRPC           = Streaming protocol; NDI telemetry stops if gRPC session drops                       │
│  NDO deploy     = Pushing policy templates to remote APIC; can time out if APIC busy                  │
│  NTP drift      = Time skew between nodes breaks TLS cert validation                                  │
│  401 error      = HTTP Unauthorized; credentials rejected by APIC REST API                            │
│  Version mismatch= ND app version incompatible with connected fabric controller                       │
│  kubectl describe= Kubernetes command showing pod events and failure reason                           │
│  TAC            = Cisco Technical Assistance Center; escalate unrecoverable faults                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Common causes:
- SNMP credentials changed on switches: update in NDFC fabric settings
- Switch SNMP ACL blocking ND data IP: update switch ACL
- PM database full: navigate to **NDFC > Settings > Data Retention** and reduce retention

---

## NDI Not Receiving Telemetry

**Symptom:** NDI dashboard shows no flow data or anomaly data is stale (> 30 minutes).

**Resolution:**

1. Verify the streaming telemetry connection from managed switches to ND:
   - For MDS (SAN Insights): telemetry is pulled via NDFC, not streamed directly; verify NDFC-to-switch connectivity
   - For ACI: verify APIC connectivity to ND

2. Check NDI flow collector pods:
   ```bash
   kubectl get pods -n ndi | grep collector
   kubectl logs -n ndi deployment/ndi-flow-collector --tail=100 | grep -i "error"
   ```

3. Verify the NDI license is applied:
   - Navigate to **Admin Console > System > Licensing** — confirm NDI Insights license is valid

4. For ACI sites: verify the APIC is registered in NDI:
   - Navigate to **NDI > Manage > Sites** — confirm site status is **Online**

---

## ND UI Certificate Warning After Upgrade

**Symptom:** After an ND upgrade, browsers show a certificate warning on the ND management URL.

**Cause:** ND upgrades may reset the TLS certificate to a self-signed default in some versions.

**Resolution:**

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check the current active certificate
acs certificates show
# If it shows the ND self-signed cert: the custom cert was lost

# Re-import the corporate CA certificate
acs certificates import \
  --key /tmp/nd.key \
  --cert /tmp/nd-bundle.crt \
  --name nd-dc1-cert

# Activate the certificate
acs certificates activate --name nd-dc1-cert
```

Maintain copies of the ND certificate key and signed certificate on a secure file share or vault. They are needed after every major ND upgrade if the cert is not preserved.

---

## ND Backup Failing

**Symptom:** Scheduled backup does not complete; backup history shows errors.

**Resolution:**

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Test remote backup connectivity
acs backup remote test

# Check backup status and last error
acs backup status

# Check backup logs
acs system logs --component backup --tail 50
```

Common causes:

| Cause | Fix |
|---|---|
| SSH key authentication to backup server expired | Rotate SSH key; update in backup configuration |
| Remote backup path does not exist | Create the path on the backup server |
| Remote backup disk full | Free space on the backup server or reduce ND retention count |
| ND data volume full | `kubectl exec` into a pod to check `/data` usage; purge NDI telemetry |

---

## LDAP Users Cannot Log In

**Symptom:** Users get "Invalid credentials" with AD accounts; local accounts work.

**Resolution:**

1. Navigate to **Admin Console > Security > Authentication > Login Domains > [LDAP domain] > Test**.
2. Enter an AD username and password to test.
3. Review the test output for the specific error.

Common errors:

| Error | Cause | Fix |
|---|---|---|
| Connection refused / timeout | Port 636 blocked | Open firewall from ND mgmt to LDAP server |
| Invalid bind credentials | Bind DN password changed | Update in ND LDAP configuration |
| User not found | Wrong search base or filter | Verify OU and user attribute setting |
| SSL handshake failed | CA cert not imported | Import CA cert into ND via `acs certificates` or Admin Console |
| Group not mapped | AD group not in role mapping table | Add group under **Security > Roles** |
