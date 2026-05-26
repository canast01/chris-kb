# Aria Ops for Logs — Install & Upgrade

## Initial Deployment

Aria Operations for Logs is deployed as a Linux-based virtual appliance (OVA). For LCM-managed environments, use LCM to deploy and upgrade. For standalone deployments, use the manual OVA process below.

### Pre-Deployment Requirements

- DNS A and PTR records created for all node FQDNs
- Static IPs reserved in IPAM
- NTP accessible from the appliance network
- Sufficient datastore space (minimum 500 GB per node for production)
- vCenter with target cluster, datastore, and port group identified
- CA-signed certificate prepared (or plan to replace self-signed post-deployment)

### OVA Deployment via vSphere Client

1. **vSphere Client → Actions → Deploy OVF Template**
2. Select the Aria Ops for Logs OVA file
3. Accept the license agreement
4. Select target: datacenter, cluster, datastore
5. Select the VM network (management network port group)
6. Customise the template:
   - **Hostname**: `vrli-prod-01.example.local`
   - **IP address**: `10.0.1.30`
   - **Netmask**: `255.255.255.0`
   - **Gateway**: `10.0.1.1`
   - **DNS**: `10.0.1.5`
   - **NTP**: `ntp.example.local`
   - **Root password**: set a strong password
7. Power on the VM — first-boot configuration takes 5–10 minutes
8. Navigate to `https://vrli-prod-01.example.local` and complete the setup wizard

### Setup Wizard Steps

1. Accept the EULA
2. Set the admin password
3. Configure the email for the admin account
4. Choose deployment type: **New Deployment** (for the first node) or **Join Cluster** (for worker nodes)
5. For production: select the appropriate licence (OSS / Standard / Advanced / Enterprise)
6. Complete the wizard — Aria Ops for Logs is ready for configuration

---

## Adding Worker Nodes to the Cluster

1. Deploy additional OVAs using the same procedure, but in step 4 of the setup wizard, select **Join Cluster**
2. Provide the master node IP and admin credentials
3. The worker joins the cluster automatically — verify in **Administration → Cluster**

```bash
# From master node — confirm all cluster members
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, role: .role}'
```

---

## Upgrade — LCM-Managed Deployments

When deployed via LCM:

1. LCM → Lifecycle Operations → Environments → locate Aria Ops for Logs product card
2. Click **Upgrade** — LCM shows compatible target versions
3. Review and resolve any pre-check failures
4. Take VM snapshots (LCM does this automatically as part of the workflow)
5. Click **Start Upgrade** — monitor via **Lifecycle Operations → Requests**

LCM upgrades worker nodes sequentially after the master — the cluster remains available during the upgrade (rolling upgrade). Ingestion may briefly slow but should not stop.

---

## Upgrade — Standalone Deployment (PAK File)

For environments not managed by LCM, upgrades use a `.pak` upgrade bundle.

**Pre-upgrade checklist:**

- [ ] Current version and target version compatibility confirmed in Broadcom Release Notes
- [ ] VM snapshot taken for all cluster nodes
- [ ] Disk usage on all nodes < 70%
- [ ] All nodes ACTIVE in cluster view
- [ ] PAK file SHA256 verified against Broadcom portal

**Upgrade via UI:**

```text
Administration → Cluster → Upgrade → Upload PAK file
```

Upload the PAK file. Aria Ops for Logs validates the file and presents a pre-upgrade compatibility check. If all checks pass, click **Upgrade**.

**Upgrade via CLI (scripted):**

```bash
# Upload PAK file to master node
scp VMware-vRealize-Log-Insight-*.pak admin@vrli-prod-01.example.local:/tmp/

# Initiate upgrade via API
curl -sk -u 'admin:<password>' -X POST \
  "https://vrli-prod-01.example.local/api/v2/upgrade/upload" \
  -F "pakFile=@/tmp/VMware-vRealize-Log-Insight-*.pak"

# Monitor upgrade status
watch -n 30 'curl -sk -u "admin:<password>" \
  "https://vrli-prod-01.example.local/api/v2/upgrade/status" | jq .'
```

---

## Post-Upgrade Validation

```bash
# Confirm version
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/version" | jq '.version'

# Confirm cluster health
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/nodes" | \
  jq '.nodes[] | {host: .hostname, state: .state, version: .version}'

# Confirm ingestion is running
curl -sk -u 'admin:<password>' \
  "https://vrli-prod-01.example.local/api/v2/cluster/stats" | \
  jq '.eventsIngested'
```

Post-upgrade checks:
- [ ] All nodes on the same version
- [ ] All nodes ACTIVE
- [ ] Log ingestion rate non-zero
- [ ] Alert definitions still enabled
- [ ] Content packs still installed and active
- [ ] Notification channels functional (send a test notification)
- [ ] Aria Operations integration still connected (if configured)
- [ ] Remove VM snapshots within 48 hours of successful upgrade
