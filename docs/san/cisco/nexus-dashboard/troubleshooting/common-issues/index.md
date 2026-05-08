# Nexus Dashboard — Common Issues

> Part of the [Nexus Dashboard](../../) reference.

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

**Resolution by cause:**

| Cause | Indicator | Fix |
|---|---|---|
| VM resource exhaustion (RAM/CPU) | High usage in acs system resources | Increase VM resources or reduce app workload |
| Cluster network (app0) disruption | Nodes cannot reach each other | Verify L2 connectivity on cluster VLAN; check vSwitch/port group |
| etcd quorum lost | acs health shows etcd warnings | Restore lost nodes; if etcd is corrupted, restore from backup |
| Kubernetes pod crash loop | `kubectl get pods --all-namespaces \| grep -v Running` | `kubectl logs -n <ns> <pod> --previous` for crash reason |
| Disk full on node | df shows /data > 90% | Purge NDI telemetry data; expand PV |
| NTP drift > 100ms | acs system ntp show | Fix NTP on affected node; etcd requires tight time sync |

---

## NDFC Fabric Shows All Switches as Unmanageable After ND Upgrade

**Symptom:** After upgrading ND or NDFC, all fabric switches show Unmanageable.

**Cause:** NDFC credential keys or service account passwords may need re-entry after a major upgrade; or NDFC pods may not have fully restarted.

**Resolution:**

```bash
# Check NDFC pod health
kubectl get pods -n ndfc

# If pods are not all Running after 10 minutes:
kubectl rollout restart deployment -n ndfc

# Wait for pods to restart
kubectl rollout status deployment/ndfc-server -n ndfc

# If pods are Running but switches still show Unmanageable:
# Test SSH from the ND data network to a managed switch
acs network test --host <switch-ip> --port 22

# If connectivity is OK: re-enter switch credentials in NDFC
# NDFC > Fabrics > [Fabric] > Edit Credentials
```

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
