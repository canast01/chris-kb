# Aria Operations — Initial Deployment

<div class="kb-summary">
Step-by-step guide to deploying VMware Aria Operations from OVA through to a fully configured monitoring cluster with adapters, alerting, and dashboards.
</div>

## Prerequisites

Before deploying Aria Operations, verify the following are in place.

**vCenter:**

- vCenter 7.0 U3 or later (vCenter 8.x recommended for Aria Ops 8.x)
- Service account with permissions: read-only + deploy VM + push metrics
- Datastore with at least 512 GB free for the primary node

**DNS:**

- Forward (A) and reverse (PTR) records created for every node before OVA deployment
- Nodes must resolve each other by FQDN — do not use IP-only deployments

**NTP:**

- All Aria Ops nodes must sync to the same NTP source as vCenter
- Confirm NTP reachability before deploying: `ntpdate -q <ntp-server>`

**Sizing — minimum 4-node cluster:**

| Node role | vCPU | RAM | Disk |
|---|---|---|---|
| Primary (master) | 8 | 32 GB | 512 GB |
| Replica | 8 | 32 GB | 512 GB |
| Collector node (x2) | 4 | 16 GB | 256 GB |

**Ports to open:**

- 443/TCP — HTTPS UI and adapter communication
- 514/UDP — syslog ingest (optional)
- 22/TCP — SSH management access

**Licensing:** Obtain Aria Operations Advanced or Enterprise licence key from VMware Customer Connect before starting.

---

## Deploy Primary Node OVA

1. Download the Aria Operations OVA from VMware Customer Connect.
2. In the vSphere Client, right-click the target cluster and select **Deploy OVF Template**.
3. Select the OVA file and click **Next**.
4. On the **Select a name and folder** screen, set the VM name (e.g. `aria-ops-primary`) and target datacenter.
5. On **Select a compute resource**, choose the destination cluster or host.
6. On **Configuration**, select the deployment size (Small / Medium / Large) matching the sizing table above.
7. On **Select storage**, choose the target datastore and set disk format to **Thick Provision Lazy Zeroed**.
8. On **Select networks**, map the OVA network to the correct management portgroup.
9. On **Customize template**, complete all fields:
   - Hostname (must match DNS A record)
   - IP address, subnet mask, default gateway
   - DNS server IPs
   - NTP server address
   - Timezone
10. Review the summary and click **Finish**.
11. Power on the VM and wait approximately 15–20 minutes for first-boot initialisation.

---

## Configure Initial Setup

1. Open a browser to `https://<primary-node-ip>` and accept the self-signed certificate.
2. The setup wizard opens automatically on first access.
3. Set the **admin** password (minimum 12 characters, mix of upper/lower/digit/symbol).
4. Accept the End User Licence Agreement.
5. On the **Activate Licence** screen, paste the Aria Operations licence key and click **Validate**.
6. Wait for the primary node to reach **Running** status — shown at **Administration → Cluster Management**.
7. Verify the node shows **Online** and the analytics engine shows **Active** before proceeding.

**Post-setup:**

- Configure an SMTP notification plugin: **Administration → Outbound Settings → Email (SMTP)**.
- Set the system timezone: **Administration → Global Settings → Time Settings**.

---

## Add vCenter Adapter

1. Navigate to **Data Sources → Integrations → Add Account**.
2. Select **VMware vSphere** from the adapter type list.
3. Enter the vCenter FQDN (not IP) and the service account credentials.
4. Set **Collector/Group** to the default collector or a remote collector if the vCenter is at a remote site.
5. Click **Validate Connection** — the status must show **Connection Successful** before saving.
6. Click **Add**.
7. Wait 15–30 minutes for the initial inventory walk to complete.
8. Verify objects appear: **Environment → Object Browser** should list hosts, clusters, VMs, and datastores.

**Additional adapters to add following the same flow:**

- NSX-T: select adapter type **VMware NSX-T**
- vSAN: auto-collected via the vCenter adapter; confirm under **Environment → vSAN**
- Storage arrays: install management packs from **Administration → Repository** before adding adapter instances

---

## Add Replica Nodes

Replica nodes provide HA for the master analytics and UI functions.

1. Deploy an additional Aria Operations OVA following the same process as the primary node.
2. On the **Customize template** screen, set the **Node Role** to **Data** (this applies to both replica and analytics/data nodes in OVA v8.x).
3. In the **Primary Node FQDN** field, enter the FQDN of the primary node deployed earlier.
4. Power on the replica node — it will self-register to the primary.
5. In the primary node UI, navigate to **Administration → Cluster Management** and confirm the new node appears with status **Joining**, then transitions to **Online**.
6. Repeat for each additional replica or analytics node required.

**Minimum HA cluster:** 1 primary + 1 replica = 2-node cluster. For >500 VMs, deploy a 4-node cluster (1 primary, 1 replica, 2 data nodes).

---

## Add Remote Collectors

Remote collectors reduce WAN load by collecting data locally and forwarding processed metrics to the primary cluster.

1. Download the Remote Collector OVA — this is a separate, smaller OVA available on Customer Connect.
2. Deploy it to the remote site vCenter using the same OVF deploy process.
3. On **Customize template**, set the **Collector Type** to **Remote Collector** and enter the primary node FQDN and the shared registration key.
4. The shared key is found at **Administration → Remote Collectors → Actions → Show Registration Key**.
5. Power on the remote collector VM.
6. In the primary node UI, navigate to **Administration → Remote Collectors** and confirm the collector appears as **Online**.
7. Assign adapters to the remote collector: when adding or editing an adapter instance, set **Collector/Group** to the newly registered remote collector.

---

## Configure Alerting and Dashboards

**Alerting:**

1. Navigate to **Alerts → Alert Settings** and review the default alert definitions for the vSphere management pack.
2. Enable alert definitions relevant to the environment (CPU, memory, datastore latency, vSAN health).
3. Suppress known environment deviations to reduce noise: **Alerts → Alert Settings → Suspend** on specific definitions.
4. Configure notification plugins:
   - SMTP: **Administration → Outbound Settings → Email**
   - ServiceNow: install the ServiceNow management pack, then configure under **Administration → Outbound Settings**
   - Webhook (Slack, PagerDuty): **Administration → Outbound Settings → Webhook**
5. Create notification rules: **Alerts → Notification Rules → Add** — map alert criticalities to outbound plugins.

**Dashboards:**

1. Navigate to **Visualise → Dashboards** and click **Create**.
2. Recommended starter dashboards:
   - vSAN cluster health (widgets: vSAN capacity, congestion, disk group health)
   - Cluster capacity (widgets: CPU/memory/storage trend, capacity remaining days)
   - VM rightsizing (use the built-in Rightsizing dashboard from the content pack)
3. Import the VMware default content: **Administration → Repository → Content → Import** — select the vSphere management pack views and dashboards.
4. Share dashboards with other users: click the dashboard kebab menu → **Share → Set Visibility to Everyone**.

---

## Validate Deployment

Run through the following checks before declaring the deployment complete.

**Cluster health:**

- **Administration → Cluster Management** — all nodes show **Online**, analytics engine **Active**
- **Administration → Remote Collectors** — all remote collectors show **Online**

**Data collection:**

- **Data Sources → Integrations** — all adapter instances show **Collection State: Collecting**
- **Environment → Object Browser** — confirm hosts, VMs, datastores, and networks are visible
- Allow 30 minutes after adding adapters before expecting full inventory

**Alerting:**

- Trigger a test alert by temporarily lowering a CPU threshold below current usage, confirm notification email is received, then restore the threshold
- Verify **Alerts → Active Alerts** shows expected alerts for the environment

**Dashboards:**

- Open each dashboard and confirm widgets populate with live data
- Check that capacity trend charts show historical data (may take 24 hours for trending charts)

**Licence:**

- **Administration → Licences** — licence key is active, object count is within licensed limit
