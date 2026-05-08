# Nexus Dashboard — Common Issues

> Part of the [Nexus Dashboard](../../) reference. For deeper diagnosis, see [Troubleshooting > Common Issues](../../troubleshooting/common-issues/).

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

**Common causes:**

| Cause | Fix |
|---|---|
| Node VM has insufficient memory | Increase VM RAM; check for memory overcommit on hypervisor |
| Cluster internal network (app0) unreachable | Verify L2 connectivity on the cluster VLAN between nodes |
| etcd quorum lost (2 of 3 nodes down) | Restore at least 2 nodes; contact Cisco TAC if etcd is corrupted |
| Pod stuck in CrashLoopBackOff | `kubectl logs -n <ns> <pod> --previous` to view crash reason |
| Disk full on node | `df -h` on the node; purge old logs or expand storage |

---

## NDFC Cannot Discover Switches

**Symptom:** After adding a seed switch in NDFC, the fabric shows only the seed switch or no switches at all.

**Resolution:**

1. Verify SSH from the ND data network to the switch management IP:
   ```bash
   ssh ndadmin@nd-dc1-1.corp.example.com
   acs network test --host <switch-ip> --port 22
   # If this fails: routing or firewall issue on the data network
   ```
2. Verify the `ndfc_mgmt` account has `network-admin` role on the switch:
   ```bash
   # On the MDS switch (NX-OS CLI)
   show user-account ndfc_mgmt
   ```
3. Verify SNMPv3 credentials match:
   ```bash
   # On the MDS switch
   show snmp user
   # Confirm dcnm_poll (or ndfc_poll) user is present with correct auth/priv protocols
   ```
4. Check NDFC discovery logs:
   ```bash
   kubectl logs -n ndfc deployment/ndfc-discovery-manager --tail=200 | grep -i "error\|fail\|<switch-ip>"
   ```

---

## Zone Activation Fails in NDFC

**Symptom:** Zone set activation from NDFC returns an error or the zone set does not propagate to all switches.

**Resolution:**

1. Navigate to **NDFC > Fabrics > [Fabric] > Zoning > Zone Status** — check for merge conflicts.
2. Check on the principal MDS switch:
   ```bash
   show zone status vsan <vsan-id>
   # Check: Mode, Default-zone, Merge Status
   show zone merge-failure vsan <vsan-id>
   ```
3. If a merge conflict is reported:
   - Identify the switch with the conflicting zone database
   - Trigger a zone re-sync from NDFC: **Fabrics > [Fabric] > Deploy All** to re-push the NDFC zone set
4. Verify the `ndfc_mgmt` account has `network-admin` role (required for zone operations)

---

## NDFC Performance Data Missing

**Symptom:** **NDFC > Monitor > Performance** shows no data or stale data.

**Resolution:**

```bash
# Check Performance Manager pod status
kubectl get pods -n ndfc | grep pm
# Should be Running

# Check PM logs for polling errors
kubectl logs -n ndfc deployment/ndfc-pm --tail=100 | grep -i "error\|timeout\|fail"

# Restart PM pod
kubectl rollout restart deployment/ndfc-pm -n ndfc
kubectl rollout status deployment/ndfc-pm -n ndfc
```

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
