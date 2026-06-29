---
tags:
  - aria-operations
  - deployment
  - vmware
search:
  boost: 1.5
---
# Aria Operations — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Aria Operations (vROps). Covers prerequisites, master node OVA deployment, cluster expansion, vCenter adapter configuration, management pack installation, and end-to-end validation.

*Applies to: Aria Ops 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_predeployment_prerequisites: "Phase 1 — Pre-Deployment Prerequisites" {shape: rectangle}
phase_2_master_node_deployment: "Phase 2 — Master Node Deployment" {shape: rectangle}
phase_3_cluster_expansion: "Phase 3 — Cluster Expansion" {shape: rectangle}
phase_4_vcenter_adapter_and_data_sou: "Phase 4 — vCenter Adapter and Data Sources" {shape: rectangle}
phase_5_management_packs_and_alert_n: "Phase 5 — Management Packs and Alert Notifications" {shape: rectangle}
phase_6_endtoend_validation: "Phase 6 — End-to-End Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_predeployment_prerequisites
phase_1_predeployment_prerequisites -> phase_2_master_node_deployment
phase_2_master_node_deployment -> phase_3_cluster_expansion
phase_3_cluster_expansion -> phase_4_vcenter_adapter_and_data_sou
phase_4_vcenter_adapter_and_data_sou -> phase_5_management_packs_and_alert_n
phase_5_management_packs_and_alert_n -> phase_6_endtoend_validation
phase_6_endtoend_validation -> validate
```

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Pre-Deployment Prerequisites

**Exit criterion:** DNS resolves with PTR records, NTP is confirmed, datastore is sized, and the vCenter service account is created.

```bash
# Verify forward and reverse DNS from management workstation
nslookup vrops-master.example.local && nslookup <planned-master-ip>
nslookup vrops-replica.example.local && nslookup vrops-rc-site2.example.local
# NTP — drift > 1s causes cluster communication failures
ntpdate -q ntp.example.local
```

vCenter service account minimum permissions:

| Scope | Required Role |
|---|---|
| vCenter global | Read-Only |
| vSAN cluster monitoring | vSAN.NoAction on cluster |
| NSX adapter | NSX Manager read-only API user |

Sizing quick reference:

| Size | Nodes | vCPUs / RAM | /storage/db | Objects |
|---|---|---|---|---|
| Small | Primary only | 8 / 32 GB | 300 GB | ≤ 1,500 |
| Medium | Primary + Replica | 16 / 48 GB each | 500 GB each | ≤ 3,500 |
| Large | Primary + Replica + 2 Data | 16 / 48 GB each | 500 GB each | ≤ 10,000 |

---

## Phase 2 — Master Node Deployment

**Exit criterion:** Master node is in Running state; the initial setup wizard is complete and services are active.

```text
vSphere Client → Deploy OVF Template → select Aria Operations OVA
→ Target: cluster → SSD-backed datastore
→ Customise:
    Hostname: vrops-master.example.local  ·  IP: 10.0.1.20/24
    Gateway: 10.0.1.1  ·  DNS: 10.0.1.5  ·  NTP: ntp.example.local
→ Power on (first-boot takes 5–10 min)
```

Setup wizard at `https://vrops-master.example.local`:

1. Accept EULA → enter licence key.
2. Deployment type: **New Installation** → Cluster role: **Master** (Primary).
3. Set admin password → cluster initialises → master enters **Running** state.

```bash
ssh root@vrops-master.example.local
service vmware-vcops-analytics status   # Active (running)
service vmware-vcops-collector status   # Active (running)
service vmware-casa status              # Active (running)
/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
```

---

## Phase 3 — Cluster Expansion

**Exit criterion:** All cluster nodes are Online in the Cluster Management UI. Remote collectors are registered and assigned to collector groups.

Deploy replica and data node OVAs using the same process as Phase 2, but select **Existing Installation → Join Cluster** in the setup wizard. Provide the master IP and admin credentials.

```bash
# Confirm all nodes Online from master
/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
# All nodes: Online
```

Remote collectors for branch sites or DMZs — deploy a lightweight collector OVA:

```text
Setup wizard → Existing Installation → Join Cluster (Remote Collector)
→ Master FQDN: vrops-master.example.local  ·  Admin credentials
```

```text
Administration → Collector Groups → New Group
→ Name: CG-Site2-DC → assign collector: vrops-rc-site2.example.local
(adapters assigned to this group run on the remote collector)
```

---

## Phase 4 — vCenter Adapter and Data Sources

**Exit criterion:** vCenter adapter shows Collecting; hosts, clusters, and VMs are visible in Environment → Object Browser.

```text
Data Sources → Cloud Accounts → Add Cloud Account → vCenter
→ Display Name: vCenter-Prod
→ FQDN: vcenter.example.local
→ Credentials: svc-vrops@example.local / <password>
→ Accept thumbprint  ·  Collection interval: 5 min
→ Enable continuous discovery: Yes
→ Save
```

```bash
# Confirm adapter collecting (run after first 5-minute cycle)
/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh adapter-status
# vCenter-Prod: Collecting
```

```text
Environment → Object Browser → vCenter-Prod
→ Hosts, clusters, VMs, datastores visible
→ Any VM → Metrics tab: CPU and memory data present
```

---

## Phase 5 — Management Packs and Alert Notifications

**Exit criterion:** NSX and vSAN adapters are collecting. Alert notification plugins are configured and tested.

Add the NSX adapter:

```text
Data Sources → Cloud Accounts → Add Cloud Account → NSX-T Manager
→ FQDN: nsx-mgr.example.local  ·  Credentials: svc-vrops-nsx@example.local
→ Collection interval: 5 min  ·  Collector group: Default
```

The vSAN adapter activates automatically from the vSphere management pack once vSAN clusters are discovered via vCenter — no separate configuration needed.

OS in-guest agents (for application-layer metrics):

```bash
# Download agent: Administration → Agents → Download Agent
chmod +x vrops-agent-install.bin
./vrops-agent-install.bin -- --server vrops-master.example.local \
  --serverPort 443 --agentGroup Linux-Prod
/opt/vmware/epops-agent/bin/epops-agent status
```

Configure notification plugins:

```text
Administration → Notifications → Outbound Plugins
→ Email: SMTP host smtp.example.local:25 · From: vrops-alerts@example.local
→ Webhook: https://hooks.slack.com/services/<token>  (POST, application/json)
→ ServiceNow REST: https://company.service-now.com/api/now/table/incident
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All checks pass. CaSA backup completed. Runbook updated. Hand off to operations.

```bash
ssh root@vrops-master.example.local
/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
# All nodes: Online

service vmware-vcops-cassandra status   # Active (running)
service vmware-vcops-gemfire status     # Active (running)
service vmware-vcops-postgres status    # Active (running)

/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh adapter-status
# All adapters: Collecting
```

Take CaSA backup before handing to operations:

```text
Administration → Backup and Restore → Backup Now
→ Destination: NFS share or SFTP  ·  Confirm completes without error
```

| Check | Location / Command | Expected |
|---|---|---|
| All nodes Online | Cluster Management UI | Online for every node |
| All adapters Collecting | `vcops-cli.sh adapter-status` | Collecting |
| vSphere inventory visible | Environment → Object Browser | All VMs and hosts present |
| Metrics populating | Any VM → Metrics tab | CPU/memory data present |
| vSAN metrics visible | vSAN cluster → Monitor | Health metrics present |
| NSX metrics visible | NSX objects → Metrics | Transport node metrics |
| Alert notifications tested | Notifications → Test | Delivery confirmed |
| Dashboards showing data | Dashboards → vSphere Health | Widgets populated |
| Cassandra running | `service vmware-vcops-cassandra status` | Active (running) |
| CaSA backup completed | Administration → Backup | Last backup fresh |
| Capacity forecasts available | Environment → Capacity | Forecasts shown (after 24h) |

---

## See also

- [Aria Operations — How It Works](../architecture/how-it-works/)
- [Aria Operations Health Checks](../operations/health-checks/)
- [Aria Operations Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
