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
┌─────────────────────────── Aria Operations for Logs — Install and Upgrade ────────────────────────────┐
│                                                                                                       │
│  vRLI is installed via OVA in vCenter; upgrades use PAK file uploaded to VAMI or LCM.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Pre-Install Requirements           │  │                Install Steps                │   │
│   │          DNS: FQDN fwd+rev for vRLI          │  │            Deploy OVA in vCenter            │   │
│   │          NTP: appliance time synced          │  │       VAMI first-boot: set IP/FQDN/NTP      │   │
│   │         Storage: 1 TB+ for log data          │  │          License: activate in VAMI          │   │
│   │       Firewall: 514/6514/443/9543 open       │  │       vSphere integration: add vCenter      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Upgrade via PAK file in VAMI or managed by LCM; take VM snapshot before upgrading.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Upgrade Process                │  │           Post-Upgrade Validation           │   │
│   │       1. Snapshot master (and workers)       │  │           Cluster: all nodes green          │   │
│   │       2. Upload PAK to VAMI or use LCM       │  │        Ingestion: events/sec resumed        │   │
│   │    3. Upgrade master first, then workers     │  │        Alerts: all enabled and firing       │   │
│   │       4. Monitor VAMI upgrade progress       │  │       SSO and forwarding: verified OK       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRLI OVA/PAK · vCenter · datastore ≥1 TB · DNS/NTP · LCM (optional managed upgrade)                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA               = Open Virtual Appliance; initial install format for vRLI                          │
│  PAK file          = vRLI upgrade package; upload to VAMI Administration → Upgrade                    │
│  VAMI              = Virtual Appliance Management Interface; configure vRLI at :9543                  │
│  LCM managed       = Aria Suite LCM can install and upgrade vRLI in managed environments              │
│  vSphere integration= Add vCenter to vRLI; auto-deploys vSphere agent to ESXi hosts                   │
│  Syslog ports      = UDP/TCP 514 (plaintext) and TCP 6514 (TLS); must be open in firewall             │
│  Upgrade sequence  = Master upgraded first; workers must be on same version as master                 │
│  VM snapshot       = Pre-upgrade rollback point; delete after 48h if upgrade successful               │
│  License           = vRLI license activated in VAMI; free tier: 25 OSI included                       │
│  Post-upgrade check= Verify cluster, ingestion, alerts, and forwarding all functional                 │
│  Worker join       = Worker nodes re-join cluster automatically after upgrade                         │
│  OSI               = Operationally Significant Instance; licensed unit in vRLI                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

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
