# Nexus Dashboard — Common Issues


<div class="kb-summary">
> Part of the [Nexus Dashboard](../../index.md) reference.
</div>

---

## ND Cluster Node Not Healthy

**Symptom:** One or more nodes shows **Degraded** or **Unavailable** in **Admin Console > Infrastructure > Nodes**.

**Diagnosis:**

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Overall cluster health
acs health

# Detailed node status
acs nodes list

# Check Kubernetes node status
kubectl get nodes
# If a node shows NotReady: investigate the node-specific issue below
```
┌──────────────────────── Cisco Nexus Dashboard — Troubleshooting Common Issues ────────────────────────┐
│                                                                                                       │
│  Most frequent ND issues: cluster quorum, app failures, site disconnects, auth errors.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Cluster Problems               │  │           Authentication Failures           │   │
│   │         Node unreachable: NIC/cable          │  │         Login fail: AAA unreachable         │   │
│   │          Quorum lost: 2+ nodes down          │  │          SAML error: cert mismatch          │   │
│   │         Disk full: Elasticsearch log         │  │          Token expired: re-auth API         │   │
│   │         NTP drift: TLS cert failure          │  │             LDAP: bind DN wrong             │   │
│   │          etcd crash: restore backup          │  │           401 REST: creds rotated           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check acs health first; auth issues need AAA server reachability confirmed                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Site and App Issues              │  │               Resolution Steps              │   │
│   │          Site offline: REST timeout          │  │           acs health: check nodes           │   │
│   │           NDFC: pod crash-looping            │  │          acs logs <app>: pod errors         │   │
│   │            NDI: no telemetry data            │  │            Renew cert or fix NTP            │   │
│   │          NDO: deploy stuck/timeout           │  │           Restart app: acs restart          │   │
│   │         SSL cert expired: 503 error          │  │          TAC: quorum unrecoverable          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · management switch · NTP · AAA server · APIC · firewall                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  acs health     = ND CLI command; shows cluster node and service health at a glance                   │
│  Quorum         = Requires 2 of 3 nodes; loss makes cluster read-only                                 │
│  etcd crash     = State-store failure; requires cluster restore from backup                           │
│  Disk full      = Elasticsearch retains telemetry; purge old data or expand volume                    │
│  NTP drift      = Clock skew breaks TLS validation and JWT expiry calculations                        │
│  Crash-loop     = Pod restarting repeatedly; acs logs shows root cause                                │
│  503 error      = HTTP Service Unavailable; typically expired TLS cert on ND                          │
│  401 error      = HTTP Unauthorized; API credentials rotated but not updated in ND                    │
│  Bind DN        = LDAP distinguished name ND uses to connect; fails if password changed               │
│  SAML cert mismatch= IdP signing cert changed but not updated in ND SP config                         │
│  acs restart    = ND CLI command to restart a specific app service gracefully                         │
│  TAC            = Cisco TAC; escalate cluster quorum loss or etcd corruption                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## Zone Activation Partially Propagates (Some Switches Updated, Others Not)

**Symptom:** After activating a zone set in NDFC, the zone change is present on some switches but not all.

**Diagnosis:**

```bash
# On each MDS switch — verify active zone set version
show zoneset active vsan <vsan-id> | include name
# Compare timestamps across switches — the lagging switch shows an older timestamp

# Check for zone merge failures
show zone merge-failure vsan <vsan-id>
```

**Resolution:**

1. In NDFC: navigate to **Fabrics > [Fabric] > Zoning > Deploy** to force a zone push to all switches.
2. If a specific switch is repeatedly failing: verify SSH connectivity and that the `ndfc_mgmt` account has `network-admin` role on that switch.
3. If the zone database is significantly out of sync on one switch: from NDFC, select the switch and use **Re-sync Zone Database** to replace the switch zone DB with NDFC's authoritative copy.

---

## NDI Anomalies Showing Stale Data

**Symptom:** NDI dashboard shows anomalies with timestamps > 1 hour old; no new anomalies are appearing despite known issues in the fabric.

**Diagnosis:**

```bash
# Check NDI pods
kubectl get pods -n ndi
# All should be Running

# Check flow collector logs
kubectl logs -n ndi deployment/ndi-flow-collector --tail=100 | grep -i "error\|drop\|overflow"

# Check disk usage for NDI data
kubectl exec -n ndi deployment/ndi-elasticsearch -- df -h /usr/share/elasticsearch/data
# If > 85% full: NDI stops writing new data (Elasticsearch circuit breaker)
```

**Resolution for disk full:**

1. Navigate to **NDI > Admin > Data Retention** and reduce the telemetry retention period (e.g., from 30 to 14 days).
2. NDI will purge older data over the next few hours.
3. Consider expanding the persistent volume or adding ND cluster storage.

---

## ND Backup Fails with Authentication Error

**Symptom:** Backup job fails; error message indicates authentication failure to the remote SCP/SFTP server.

**Diagnosis and Resolution:**

```bash
# Test remote backup connectivity
ssh ndadmin@nd-dc1-1.corp.example.com
acs backup remote test
# Review output for the specific error

# If SSH key authentication: check if key is still authorized on backup server
# Update the backup configuration if credentials changed:
acs backup remote update \
  --server backup-server.corp.example.com \
  --user nd-bkp \
  --key-file /home/ndadmin/.ssh/nd-backup-key
```

Common causes:
- SSH key was rotated on the backup server without updating ND configuration
- Remote backup path does not exist or write permissions changed
- Backup server IP/hostname changed

---

## SAML SSO Login Redirects but Fails to Return to ND

**Symptom:** Clicking the SSO button redirects to the IdP login page, authentication completes, but the user is not redirected back to ND (or returns to ND with an error).

**Common Causes:**

| Symptom | Cause | Fix |
|---|---|---|
| "Audience URI mismatch" | ND Service Provider Entity ID in IdP does not match ND's expected value | Update Entity ID in IdP to match ND metadata |
| "Signature validation failed" | IdP signing certificate has changed | Re-import IdP metadata into ND |
| "No role assigned" | User's IdP role attribute is not mapped in ND | Add the role to ND SAML role mapping |
| Loop back to IdP login | ND cannot reach the IdP ACS URL | Check firewall between ND mgmt network and IdP |

```bash
# Check ND authentication service logs for SAML errors
kubectl logs -n nd-platform deployment/nd-keycloak --tail=100 | grep -i "saml\|assertion\|redirect"
```

---

## Cisco Intersight Connection Fails

**Symptom:** ND cannot claim to Intersight; the claim process times out or returns an error.

**Resolution:**

1. Verify outbound HTTPS from ND management network to `api.intersight.com`:
   ```bash
   acs network test --host api.intersight.com --port 443
   ```
2. If proxy is required: configure the HTTP proxy in ND:
   - Navigate to **Admin Console > System > Proxy Settings**
   - Enter the proxy address and credentials
3. Re-attempt the claim process: generate a new claim code in ND and redeem it in Intersight.
4. If the Intersight connection was previously working and suddenly stopped: check if the Intersight device connector was reset during an ND upgrade. Re-claim if necessary.

---

## Application (NDFC or NDI) Stuck in "Installing" or "Error" State

**Symptom:** After uploading a new app image, the app shows **Installing** or **Error** state indefinitely.

**Resolution:**

```bash
ssh ndadmin@nd-dc1-1.corp.example.com

# Check app status
acs apps status

# Check for pods stuck in Init or Error states
kubectl get pods --all-namespaces | grep -Ev "Running|Completed"

# Describe a stuck pod
kubectl describe pod -n ndfc <pod-name>
# Check Events section for resource constraints, image pull errors, etc.

# Check node resource availability
acs system resources
# If nodes are at memory/CPU limit: scale down other apps or add resources

# If the install image is corrupt:
acs apps remove-image <app> <version>
# Re-upload the image from a fresh download
```

---

## Time Skew Between ND Nodes

**Symptom:** acs health warns about time synchronization issues; Kubernetes etcd logs show time-related warnings; cluster becomes unstable.

**Resolution:**

```bash
# Check NTP on all nodes
acs system ntp show

# If NTP is not synchronised, re-add NTP servers:
acs system ntp add --server 10.10.0.10 --prefer
acs system ntp add --server 10.10.0.11

# Wait 2-3 minutes and check again
acs system ntp show
# Expected offset: < 100ms

# If offset is large and nodes cannot sync (isolated network):
# Use chronyc on the node OS to force a step correction:
sudo chronyc makestep
```

etcd requires all cluster nodes to have time within 1 second of each other. Large time skew causes leader election failures and cluster instability.
