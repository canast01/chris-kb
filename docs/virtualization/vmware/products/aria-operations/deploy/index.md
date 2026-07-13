---
tags:
  - aria-operations
  - deployment
  - vmware
search:
  boost: 1.5
description: "End-to-end deployment guide for VMware Aria Operations (vROps). Covers prerequisites, master node OVA deployment, cluster expansion, vCenter adapter..."
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

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: HOW TO: Install, Configure and Manage VMware Aria Operations 8.17](https://www.youtube.com/watch?v=R-KfLZ4B4pc){ .md-button }
<!-- /video-link -->

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


```text title="Expected output"
Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	vrops-master.example.local
Address: 192.168.100.45

Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	192.168.100.45
Address:	vrops-master.example.local

Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	vrops-replica.example.local
Address: 192.168.100.46

Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	vrops-rc-site2.example.local
Address: 192.168.100.47

polling server 10.0.1.100
server 10.0.1.100, stratum 2, offset 0.012345, delay 0.04567
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `** nslookup: can't resolve 'vrops-master.example.local': Non-existent domain` | Verify DNS zone contains the FQDN record and confirm the correct DNS server IP is configured on the management workstation. |
    | `** nslookup: can't resolve '<planned-master-ip>': Non-existent domain` | Ensure a PTR (reverse DNS) record exists for the IP address in the DNS server's reverse zone. |
    | `** ntpdate[12345]: the NTP socket is in use, exiting` | Stop the ntpd or chronyd service with `systemctl stop ntpd` before running ntpdate, or use `chronyc waitsync` instead if using chrony. |
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


```text title="Expected output"
root@vrops-master:~# service vmware-vcops-analytics status
● vmware-vcops-analytics.service - VMware vRealize Operations Analytics Service
     Loaded: loaded (/etc/systemd/system/vmware-vcops-analytics.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 09:42:18 UTC; 2 days ago
   Main PID: 4521 (java)
      Tasks: 47 (limit: 4096)
     Memory: 2.8G
root@vrops-master:~# service vmware-vcops-collector status
● vmware-vcops-collector.service - VMware vRealize Operations Collector Service
     Loaded: loaded (/etc/systemd/system/vmware-vcops-collector.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 09:43:52 UTC; 2 days ago
   Main PID: 5847 (java)
      Tasks: 52 (limit: 4096)
     Memory: 3.1G
root@vrops-master:~# service vmware-casa status
● vmware-casa.service - VMware CASA Service
     Loaded: loaded (/etc/systemd/system/vmware-casa.service; enabled; vendor preset: disabled)
     Active: active (running) since Mon 2024-01-15 09:44:31 UTC; 2 days ago
   Main PID: 6123 (java)
      Tasks: 38 (limit: 4096)
     Memory: 1.9G
root@vrops-master:~# /usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
Cluster Status Report
=====================
Master Node: vrops-master.example.local (192.168.1.45)
Status: HEALTHY
Cluster Mode: Active-Active
Nodes in Cluster: 3
  - vrops-master.example.local (192.168.1.45) - ONLINE
  - vrops-replica1.example.local (192.168.1.46) - ONLINE
  - vrops-replica2.example.local (192.168.1.47) - ONLINE
Database Replication: SYNCHRONIZED
Last Sync: 2024-01-17 14:32:15 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused` | Verify SSH connectivity and that the vROps master node is reachable on port 22. |
    | `vcops-cli.sh: command not found` | Confirm the vRealize Operations suite is installed in `/usr/lib/vmware-vcopssuite/` and the utilities package is present. |
    | `● vmware-vcops-analytics.service - VMware vRealize Operations Analytics Service ... Active: inactive (dead)` | Start the service with `systemctl start vmware-vcops-analytics` and check logs with `journalctl -u vmware-vcops-analytics -n 50` for startup errors. |
---

## Phase 3 — Cluster Expansion

**Exit criterion:** All cluster nodes are Online in the Cluster Management UI. Remote collectors are registered and assigned to collector groups.

Deploy replica and data node OVAs using the same process as Phase 2, but select **Existing Installation → Join Cluster** in the setup wizard. Provide the master IP and admin credentials.

```bash
# Confirm all nodes Online from master
/usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
# All nodes: Online
```


```text title="Expected output"
Cluster Status Report
=====================
Node Name                    Status      Role            Version
master-aria-ops-01          Online      Master          8.10.2.0-21567890
worker-aria-ops-02          Online      Worker          8.10.2.0-21567890
worker-aria-ops-03          Online      Worker          8.10.2.0-21567890
analytics-aria-ops-04       Online      Analytics       8.10.2.0-21567890

Cluster Health: HEALTHY
Last Updated: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Command not found: /usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh` | Verify Aria Operations is installed on this node and the installation path is correct. |
    | `Error: Unable to connect to cluster database` | Ensure the master node is running and network connectivity exists between all cluster nodes. |
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


```text title="Expected output"
Extracting installer...
Verifying digital signature...
Installing VMware Aria Operations Agent v8.12.1...
Creating user 'epops'...
Configuring agent group: Linux-Prod
Installation completed successfully.
Agent registered with server: vrops-master.example.local:443
Waiting for agent startup...

Agent Status:
  Process ID: 4782
  Status: RUNNING
  Version: 8.12.1.21847392
  Server: vrops-master.example.local
  Last Heartbeat: 2024-01-15 14:32:18 UTC
  Memory Usage: 287 MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `./vrops-agent-install.bin: Permission denied` | Run `chmod +x vrops-agent-install.bin` before executing the installer. |
    | `Error: Unable to connect to server vrops-master.example.local:443` | Verify network connectivity and that the Aria Operations master server hostname/IP is correct and reachable on port 443. |
    | `Agent Status: NOT_RUNNING - Failed to start epops-agent service` | Check `/opt/vmware/epops-agent/log/wrapper.log` for startup errors and ensure the system has sufficient memory and disk space. |
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


```text title="Expected output"
root@vrops-master:~# /usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh cluster-status
Cluster Status Report
=====================
Node: vrops-master.example.local     Status: Online
Node: vrops-replica-1.example.local  Status: Online
Node: vrops-replica-2.example.local  Status: Online

All nodes: Online

root@vrops-master:~# service vmware-vcops-cassandra status
● vmware-vcops-cassandra.service - VMware vRealize Operations Cassandra
   Loaded: loaded (/etc/systemd/system/vmware-vcops-cassandra.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2 days ago

root@vrops-master:~# service vmware-vcops-gemfire status
● vmware-vcops-gemfire.service - VMware vRealize Operations GemFire
   Loaded: loaded (/etc/systemd/system/vmware-vcops-gemfire.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-01-17 14:33:05 UTC; 2 days ago

root@vrops-master:~# service vmware-vcops-postgres status
● vmware-vcops-postgres.service - VMware vRealize Operations PostgreSQL
   Loaded: loaded (/etc/systemd/system/vmware-vcops-postgres.service; enabled; vendor preset: disabled)
   Active: active (running) since Wed 2024-01-17 14:33:42 UTC; 2 days ago

root@vrops-master:~# /usr/lib/vmware-vcopssuite/utilities/bin/vcops-cli.sh adapter-status
Adapter Status Report
=====================
vSphere Adapter Instance 1:     Status: Collecting
vSphere Adapter Instance 2:     Status: Collecting
NSX-T Adapter Instance 1:       Status: Collecting
Kubernetes Adapter Instance 1:  Status: Collecting

All adapters: Collecting
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused` | Verify SSH connectivity and that the vrops-master hostname resolves correctly with `nslookup vrops-master.example.local`. |
    | `vcops-cli.sh: command not found` | Confirm the vRealize Operations Suite is installed and the utilities path exists with `ls -la /usr/lib/vmware-vcopssuite/utilities/bin/`. |
    | `Job for vmware-vcops-cassandra.service failed because the control process exited with error code` | Restart the failed service with `service vmware-vcops-cassandra restart` and check logs via `journalctl -u vmware-vcops-cassandra -n 50`. |
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
