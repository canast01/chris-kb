# Nexus Dashboard — Initial Deployment

```text
┌───────────────────────────── Cisco Nexus Dashboard — Deployment Overview ─────────────────────────────┐
│                                                                                                       │
│   Nexus Dashboard is a 3-node cluster hosting NDFC (fabric management) and NDI (telemetry) services   │
│   Minimum production deployment: 3 nodes; single-node is lab-only                                     │
│   Two networks required: management (eth0) for switch MGMT0 reach, data (eth1) for fabric programming │
│                                                                                                       │
│   Node requirements                                                                                   │
│   16 vCPU, 64 GB RAM, 500 GB thick-provisioned disk per node; ESXi 7.0 U2+ or bare-metal RHEL         │
│   Node latency: <10ms round-trip between all three nodes (required for cluster consensus)             │
│   IPs needed: 3× management, 1× management VIP, 3× data, 1× data VIP                                  │
│                                                                                                       │
│   Deployment sequence                                                                                 │
│   Step 1: deploy OVA three times (one per node); set management IP, data IP, admin password per node  │
│   Step 2: browse to Node 1 management IP; run Initial Setup wizard to form the cluster                │
│   Step 3: add nodes 2 and 3 via wizard; enter management IPs; cluster formation takes 10-20 minutes   │
│   Step 4: redirect to cluster management VIP; verify all three nodes show Healthy                     │
│                                                                                                       │
│   Service installation                                                                                │
│   Install NDFC: Admin > Services > Service Catalog > Nexus Dashboard Fabric Controller > Install      │
│   Install NDI (optional): same catalog; provides telemetry, flow analytics, and anomaly detection     │
│   Verify: SSH to any node; run acs services status — all services should show Running                 │
│                                                                                                       │
│   Site onboarding                                                                                     │
│   Admin > Sites > Add Site: select NDFC or ACI as site type; enter controller URL and credentials     │
│   Or: create fabric directly in NDFC service — it auto-registers as a Nexus Dashboard site            │
│   Validate: Sites view shows Connectivity: Reachable; NDFC Switches shows Config Status: In Sync      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   NDFC       = Nexus Dashboard Fabric Controller; manages Nexus and MDS fabrics (formerly DCNM)       │
│   NDI        = Nexus Dashboard Insights; telemetry, flow data, and advisory analysis                  │
│   Cluster VIP = virtual IP address shared across all three nodes; used for browser and switch access  │
│   acs        = Nexus Dashboard CLI tool; acs health checks cluster, acs services status checks apps   │
│   Site       = a managed fabric registered in Nexus Dashboard (NDFC, ACI, or standalone)              │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

This guide covers deploying Cisco Nexus Dashboard (ND) from OVA to a validated 3-node cluster with NDFC and/or NDI services installed and a first site connected. Nexus Dashboard is the unified platform that hosts Cisco's NDFC (formerly DCNM), NDI (Network Insights), and other data center management services.

---

## Prerequisites

**Cluster requirements:**

- Nexus Dashboard requires a minimum 3-node cluster for production deployments (single-node is supported for lab use only)
- Each node VM:
  - 16 vCPU, 64 GB RAM, 500 GB SSD-backed disk
  - Two network interfaces:
    - `eth0` (Management Network): reaches switch MGMT0 interfaces, DNS, NTP, LDAP
    - `eth1` (Data Network): reaches in-band fabric interfaces, required for NDFC fabric programming
  - VMware ESXi 7.0 U2 or later, or bare-metal RHEL for physical node deployment

**IP address plan (3-node cluster example):**

| Component               | IP           |
|-------------------------|--------------|
| ND Node 1 management    | 10.0.0.40    |
| ND Node 2 management    | 10.0.0.41    |
| ND Node 3 management    | 10.0.0.42    |
| Cluster management VIP  | 10.0.0.45    |
| ND Node 1 data          | 10.0.10.40   |
| ND Node 2 data          | 10.0.10.41   |
| ND Node 3 data          | 10.0.10.42   |
| Cluster data VIP        | 10.0.10.45   |

**Network connectivity:**

- All three management IPs and the management VIP must be on the same subnet
- All three data IPs and the data VIP must be on the same subnet
- Latency between nodes: less than 10ms round-trip (required for cluster consensus)
- TCP 443 open between ND management VIP and all managed switches' management interfaces

**Cisco switch requirements:**

- Nexus 9000 series running NX-OS 9.3(3) or later for NDFC-managed fabrics
- MDS 9000 running NX-OS 8.4(1) or later for SAN fabric management
- All switches must have mgmt0 reachable from the ND management VIP

---

## Deploy ND OVA (3-Node Cluster)

Deploy the OVA three times — once per node.

1. Download the Nexus Dashboard OVA from Cisco Software Download (search "Nexus Dashboard").
2. In vSphere Client, deploy the OVA via **Actions > Deploy OVF Template**:
   - Select the OVA file.
   - On the network mapping page:
     - Map `Management Network` to your OOB management port group.
     - Map `Data Network` to your in-band fabric port group.
   - On the **Customize template** page:
     - Set the node's management IP, subnet, and gateway.
     - Set the data network IP, subnet, and gateway.
     - Set the admin password.
   - Set disk provisioning to **Thick Provision Lazy Zeroed** (required — thin provisioning is not supported).
3. Repeat the OVA deployment for nodes 2 and 3, adjusting the IP addresses per node.
4. Power on all three VMs. Allow 15–20 minutes for each node to complete initial boot.

---

## Cluster Formation

Cluster formation is initiated from the first node's UI.

**Step 1 — Access Node 1 initial setup:**

1. Browse to `https://<node1_management_ip>`.
2. Log in with `admin` and the password set during OVA deployment.
3. The **Initial Setup** wizard opens.

**Step 2 — Configure the first node:**

1. **Cluster name:** Enter a name (e.g., `nd-prod-cluster`).
2. **Management network:** Confirm the management IP, subnet, gateway, DNS servers, and NTP server.
3. **Data network:** Confirm the data IP and subnet.
4. **Cluster VIPs:** Enter the management VIP (`10.0.0.45`) and data VIP (`10.0.10.45`). These are the addresses all users and switches will connect to after cluster formation.
5. Click **Next**.

**Step 3 — Add nodes 2 and 3:**

1. On the "Add Nodes" screen, click **Add Node**.
2. Enter Node 2's management IP and credentials.
3. Nexus Dashboard contacts Node 2, retrieves its configuration, and adds it to the cluster.
4. Repeat for Node 3.
5. Click **Finish**. Cluster formation begins.

**Monitor cluster formation:**

Cluster formation takes 10–20 minutes. The UI redirects to `https://<cluster_management_vip>`. Wait until the cluster overview page shows all three nodes as **Healthy**.

```bash
# SSH to any node and check cluster status:
acs health
# All three nodes should show health: "healthy"
```

---

## Install NDFC/NDI Services

Nexus Dashboard hosts management services as containerized applications called "services." Install NDFC for fabric management and NDI for analytics.

1. Log in to Nexus Dashboard at `https://<cluster_vip>`.
2. Navigate to **Admin > Services > Service Catalog**.
3. Find **Nexus Dashboard Fabric Controller (NDFC)**:
   - Click **Install**.
   - Select the version compatible with your NX-OS version (check Cisco's Compatibility Matrix).
   - Click **Install** and confirm. The installation downloads and deploys NDFC containers to the cluster. This takes 15–25 minutes.
4. Find **Nexus Dashboard Insights (NDI)** (optional — for telemetry and flow analytics):
   - Click **Install** and follow the same process.
5. After installation, services appear in the **Services** dropdown in the top navigation bar.

**Verify services are running:**

```bash
# SSH to any ND node:
acs services status
# NDFC and NDI should show Running
```

**Access NDFC:**

Navigate to **Services > Nexus Dashboard Fabric Controller**. The NDFC interface opens within Nexus Dashboard. First launch may take 2–3 minutes while NDFC initializes its internal database.

---

## Add First Site

A "site" in Nexus Dashboard is a managed fabric (a group of Cisco switches). Sites can be Nexus 9000 LAN fabrics, MDS SAN fabrics, or ACI fabrics.

**Add a Nexus LAN fabric as a site:**

1. Navigate to **Admin > Sites > Add Site**.
2. Select **NDFC** as the site type (the site will be managed by the NDFC service).
3. Enter:
   - **Site name:** (e.g., `dc1_leaf_spine`)
   - **Controller URL:** This is the NDFC internal endpoint — use `https://localhost` if NDFC is co-hosted on the same ND cluster
   - **Username/Password:** NDFC admin credentials
4. Click **Add**. Nexus Dashboard registers the NDFC-managed fabric as a site.

**Alternatively, onboard a fabric directly in NDFC:**

1. Open the NDFC service from **Services > NDFC**.
2. Navigate to **LAN > Fabrics > Create Fabric** and follow the fabric creation wizard (see the Cisco DCNM deployment guide for fabric creation details).
3. After fabric creation in NDFC, the fabric appears automatically as a site in Nexus Dashboard.

**For ACI fabrics (APIC-managed):**

1. Navigate to **Admin > Sites > Add Site**.
2. Select **ACI** as site type.
3. Enter the APIC management IP and credentials.
4. Nexus Dashboard connects to the APIC and imports the fabric.

---

## Validate

**Cluster health:**

1. Navigate to **Admin > System Status**. All three nodes should show CPU and memory usage well within limits and no critical alerts.
2. Navigate to **Admin > Sites**. The site added above should show **Connectivity: Reachable**.

**Service health:**

```bash
acs services status
# All installed services should show "Running" with no restarts
```

**NDFC fabric connectivity:**

1. Open **Services > NDFC**.
2. Navigate to **LAN > Switches** (for LAN fabrics) or **SAN > Switches** (for SAN fabrics).
3. All managed switches should show **Reachability: Reachable** and **Config Status: In Sync**.

**NDI telemetry validation (if installed):**

1. Open **Services > Nexus Dashboard Insights**.
2. Navigate to **Browse > Flows**. If telemetry is configured on the switches, flow data should begin appearing within 5 minutes.
3. Navigate to **Analyze > Advisories**. Any misconfigurations or anomalies detected by NDI are listed here with remediation suggestions.

**Certificate validation:**

The default self-signed certificate should be replaced for production use:

1. Navigate to **Admin > Security > Certificates > Replace Certificate**.
2. Upload a PEM-encoded certificate and private key signed by your internal CA.
3. Apply and confirm that browsing to the cluster VIP no longer shows a certificate warning.
