#!/usr/bin/env python3
"""Generate FAQ stubs — batch 4: virtualization."""

import os
import xml.etree.ElementTree as ET

BASE = "/Users/chrisanastasiadis/chris-kb/docs"
ASSETS = "/Users/chrisanastasiadis/chris-kb/docs/assets"

PRODUCTS = [
    ("virtualization/nutanix/operations", "nutanix", "Nutanix AOS", {
        "version_check": ("What AOS version is recommended for new Nutanix deployments?",
            "AOS 6.8.x LTS is the current recommendation. Check via Prism Central → Settings → Cluster Details or `ncli cluster version` on a CVM. Always check the Nutanix compatibility matrix before upgrading."),
        "version_cmd": "ncli cluster version",
        "default_setting": ("What is the default data resiliency factor and when should it change?",
            "Replication Factor 2 (RF2) is the default — tolerates one node failure. Use RF3 for mission-critical workloads or clusters with fewer than 5 nodes where RF2 provides inadequate protection."),
        "enable_feature": ("How do I enable Nutanix Flow microsegmentation?",
            "Flow is enabled per cluster in Prism Central → Settings → Flow → Enable. Requires AOS 5.17+ and PC 5.17+. Create Security Policies under Policies → Security Policies. Flow uses VM categories for policy targeting."),
        "rolling_upgrade": ("How do I perform a rolling upgrade of AOS without downtime?",
            "Use Life Cycle Manager (LCM): Prism Central → LCM → Inventory → Update. LCM upgrades one node at a time, migrating VMs before patching each node. Verify cluster health before each node upgrade."),
        "add_resource": ("What is the correct procedure to add a new node to a Nutanix cluster?",
            "Rack and cable the node. From Prism Element → Settings → Expand Cluster → enter the node serial or IP. Nutanix Foundation handles the remaining discovery and join process. Cluster rebalances data automatically."),
        "warning": ("Prism shows 'Cluster health critical — node is down'. What does it mean?",
            "A node has left the cluster. If a CVM is down: SSH to another CVM and check `cluster status`. If a hypervisor is down: check iDRAC/IPMI. Nutanix automatically re-replicates data to surviving nodes for RF2 clusters."),
        "perf": ("VM performance is degraded on Nutanix — where do I start?",
            "Check Prism → Analysis → Performance for the VM. Review storage controller (CVM) CPU and memory. Check for noisy-neighbour VMs using the same storage tier. Verify SSD tier has not been fully consumed with `ncli cluster get-storage-pool`."),
        "backup_freq": ("How often should I back up Nutanix Prism configuration?",
            "Enable automated Prism Central backup: PC → Settings → Backup. Daily backup to an external server. For Prism Element, export configuration weekly. Test restore to a lab cluster quarterly."),
        "restore": ("Can I restore a single VM from a Nutanix snapshot without restoring the whole cluster?",
            "Yes — Prism Element → VM → Snapshots → Restore. This restores only that VM. For application-consistent recovery across multiple VMs, use Nutanix Protection Domains or a third-party backup tool (Veeam, Commvault)."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("virtualization/openshift/operations", "openshift", "Red Hat OpenShift", {
        "version_check": ("What OpenShift version is recommended for new deployments?",
            "OpenShift 4.15.x or the latest EUS (Extended Update Support) release. Check: `oc version`. Red Hat supports N and N-1 minor versions. Plan upgrades to stay within the support window."),
        "version_cmd": "oc version",
        "default_setting": ("What is the default node autoscaling configuration?",
            "Autoscaling is disabled by default. Enable with a MachineAutoscaler: `oc apply -f machine-autoscaler.yaml`. Set `minReplicas` and `maxReplicas` per MachineSet. ClusterAutoscaler must also be enabled."),
        "enable_feature": ("How do I enable OpenShift GitOps (ArgoCD) for application delivery?",
            "Install the OpenShift GitOps operator from OperatorHub. After installation, ArgoCD is deployed in the `openshift-gitops` namespace. Access the ArgoCD UI via the Route: `oc get route -n openshift-gitops`."),
        "rolling_upgrade": ("How do I upgrade OpenShift without disrupting workloads?",
            "Upgrades are rolling and managed by the Cluster Version Operator (CVO). Initiate via `oc adm upgrade --to=<version>`. Control plane upgrades first, then worker nodes one at a time. Monitor: `oc get clusterversion`."),
        "add_resource": ("What is the correct procedure to add a new worker node?",
            "Scale the MachineSet: `oc scale machineset <name> -n openshift-machine-api --replicas=<n>`. For bare-metal, use the Assisted Installer or add the host manually via the BMC/IPMI and approve the CSR: `oc get csr | grep Pending`."),
        "warning": ("OpenShift shows 'ClusterOperator degraded'. What does it mean?",
            "A core cluster operator is not healthy. Check: `oc get co` and `oc describe co <name>` for the degraded operator. Common causes: network connectivity issues, etcd quorum loss, or resource exhaustion. Address immediately."),
        "perf": ("Pod scheduling latency is high — where do I start?",
            "Check scheduler logs: `oc logs -n openshift-kube-scheduler`. Review node resource pressure: `oc describe nodes | grep -A5 Conditions`. Check for pending PVCs blocking pod start. Review resource quotas and limit ranges."),
        "backup_freq": ("How often should I back up OpenShift etcd?",
            "Daily etcd snapshots via the OpenShift etcd backup procedure: `oc exec -n openshift-etcd etcd-<master> -- /usr/local/bin/cluster-backup.sh /home/core/`. Backup includes all cluster state. Test restore quarterly."),
        "restore": ("Can I restore a single namespace from an etcd backup?",
            "Not directly — etcd restores are full cluster restores. For namespace-level recovery, use Velero (OADP operator) which supports namespace-scoped backup and restore. Always test Velero restores before incidents occur."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/aria-automation/operations", "aria-automation", "VMware Aria Automation", {
        "version_check": ("What Aria Automation version is recommended?",
            "Aria Automation 8.16.x is the current recommendation. Check via Aria Automation UI → Help → About. Aria Suite Lifecycle Manager (LCM) is the recommended upgrade mechanism."),
        "version_cmd": "Aria Automation UI → Help → About",
        "default_setting": ("What is the default cloud zone configuration and when should it change?",
            "Cloud zones are empty by default — you must configure them for each connected vCenter/cloud account. Assign datastores, compute clusters, and networks. Use placement policies (must, should) to control where workloads are provisioned."),
        "enable_feature": ("How do I enable Aria Automation Orchestrator integration?",
            "In Aria Automation, go to Infrastructure → Integrations → Orchestrator. Add the vRO endpoint (embedded or external). Once connected, vRO workflows appear as extensibility actions in blueprints."),
        "rolling_upgrade": ("How do I upgrade Aria Automation using Aria Suite Lifecycle Manager?",
            "In LCM → Lifecycle Operations → Environment → select the Aria Automation instance → Upgrade. LCM handles the upgrade sequence. For clustered deployments, nodes upgrade sequentially. Typical upgrade time: 2-3 hours."),
        "add_resource": ("What is the correct procedure to add a new vCenter cloud account?",
            "Aria Automation → Infrastructure → Cloud Accounts → Add Account → vCenter. Provide vCenter FQDN and credentials. After connection, configure cloud zones and network/storage profiles."),
        "warning": ("Aria Automation shows 'Deployment failed — resource not available'. What does it mean?",
            "The placement engine could not find a suitable compute, storage, or network resource matching the blueprint constraints. Check cloud zone capacity, placement policies, and network profile assignments. Review the deployment request details for specific constraints."),
        "perf": ("Aria Automation deployments are slow to complete — where do I start?",
            "Check vRO workflow execution logs for bottlenecks. Review NSX segment creation time if networking is involved. Check vCenter task queue for concurrent provisioning load. Verify Aria Automation appliance CPU/memory is within spec."),
        "backup_freq": ("How often should I back up Aria Automation?",
            "Daily via LCM → Lifecycle Operations → Environment → Backup. Backup includes all service content (blueprints, cloud accounts, deployments). Store off-appliance. Test restore to a lab environment quarterly."),
        "restore": ("Can I restore a single blueprint without a full Aria Automation restore?",
            "Yes — export the blueprint to YAML (Cloud Template → Export). Re-import via Content Sources or directly via the Aria Automation API. Blueprint content is separate from the platform data and can be restored independently."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/aria-operations-for-logs/operations", "aria-ops-logs", "VMware Aria Operations for Logs", {
        "version_check": ("What Aria Operations for Logs version is recommended?",
            "Aria Operations for Logs 8.14.x is the current recommendation. Check via Admin UI → System → About."),
        "version_cmd": "Admin UI → System → About",
        "default_setting": ("What is the default log retention period?",
            "Default retention is 30 days. Increase to 90 days for compliance (PCI-DSS, ISO 27001). For SOX, 12 months minimum. Configure under Admin → General Configuration → Data Retention."),
        "enable_feature": ("How do I enable Aria Operations for Logs integration with Aria Operations?",
            "Admin → Integration → VMware Aria Operations → Add. Provide Aria Operations URL and credentials. Once connected, log events can trigger alerts in Aria Operations and VMs in Aria Ops link to their logs."),
        "rolling_upgrade": ("How do I upgrade Aria Operations for Logs without losing log data?",
            "Log data persists on the virtual disk during upgrade. Use LCM for the upgrade. For clustered deployments, the master node upgrades first, then worker nodes. Log ingestion pauses briefly during each node upgrade."),
        "add_resource": ("What is the correct procedure to add a new syslog source?",
            "Configure the source device to forward syslog to the Aria Logs VIP (UDP/TCP 514 or 1514). In Aria Logs, create a content pack or custom alert for the new source. Verify log ingestion in Live Log View."),
        "warning": ("Aria Logs shows 'Disk usage above 80%'. What does it mean?",
            "Log storage is nearing capacity. Either expand the storage partition or reduce retention period. If retention cannot be reduced, add worker nodes to the cluster to distribute storage. Logs will be dropped if disk reaches 100%."),
        "perf": ("Log ingestion rate is dropping — where do I start?",
            "Check Admin → System → Cluster Status for node health. Review ingestion rate in Admin → General Configuration. High ingestion rates may require additional worker nodes. Check network bandwidth between log sources and Aria Logs VIP."),
        "backup_freq": ("How often should I back up Aria Operations for Logs configuration?",
            "Weekly via Admin → System → Export Configuration. Log data itself is not backed up (it is telemetry). Configuration backup includes content packs, alerts, and dashboards. Store off-appliance."),
        "restore": ("Can I restore historical logs after an Aria Logs rebuild?",
            "No — historical logs cannot be recovered after a rebuild unless you have a full VM snapshot (which includes the log data disk). This is why retention period and disk expansion are critical — lost logs cannot be re-ingested."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/aria-operations-for-networks/operations", "aria-ops-networks", "VMware Aria Operations for Networks", {
        "version_check": ("What Aria Operations for Networks version is recommended?",
            "Aria Operations for Networks 6.12.x is the current recommendation. Check via Administration → Overview → Product Version."),
        "version_cmd": "Administration → Overview → Product Version",
        "default_setting": ("What is the default flow data collection interval?",
            "IPFIX flow data is collected every 60 seconds by default. Reduce to 30 seconds for faster anomaly detection. Increase to 120 seconds for large environments where 60-second polling causes performance overhead."),
        "enable_feature": ("How do I enable NSX Intelligence integration with Aria Operations for Networks?",
            "Administration → Data Sources → Add NSX-T Manager. Enable flow collection. Also enable NSX Intelligence (separate licence) for ML-based anomaly detection. Both sources appear as separate data streams in the UI."),
        "rolling_upgrade": ("How do I upgrade Aria Operations for Networks without losing flow history?",
            "Flow history is stored on the appliance data disk which persists through upgrades. Use the UI-based upgrade: Administration → Overview → Update. Platform node upgrades first, then collector nodes."),
        "add_resource": ("What is the correct procedure to add a new vCenter as a data source?",
            "Administration → Data Sources → Add vCenter Server. Provide FQDN and read-only credentials. Aria OpN discovers all VMs, hosts, and port groups. Flow data begins appearing within 10 minutes if IPFIX is configured on vSphere Distributed Switches."),
        "warning": ("Aria Operations for Networks shows 'Flow data missing for entity X'. What does it mean?",
            "IPFIX flow export is not configured or has stopped for the VDS associated with the entity. Check the VDS IPFIX configuration in vCenter → Distributed Switch → Edit Settings → IPFIX → verify collector IP matches the Aria OpN collector."),
        "perf": ("Aria Operations for Networks UI is slow when querying large time ranges — where do I start?",
            "Reduce query time range. Use the search filters to narrow scope (specific VMs or flows). For bulk queries, use the REST API with pagination. Consider adding a dedicated collector node for high-volume environments."),
        "backup_freq": ("How often should I back up Aria Operations for Networks?",
            "Weekly configuration export (Administration → System → Backup). Flow data is telemetry and not typically backed up. Configuration backup includes data sources, dashboards, and alert definitions."),
        "restore": ("Can I recover flow data from before an Aria Operations for Networks rebuild?",
            "No — flow data stored on the appliance is lost if the appliance is rebuilt. Take VM-level snapshots before upgrades if historical flow data preservation is critical. Flow data is regenerated from IPFIX sources going forward."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/aria-operations/operations", "aria-operations", "VMware Aria Operations", {
        "version_check": ("What Aria Operations version is recommended?",
            "Aria Operations 8.16.x is the current recommendation. Check via Administration → Support → About."),
        "version_cmd": "Administration → Support → About",
        "default_setting": ("What is the default collection interval for metrics?",
            "5 minutes is the default collection interval. Reduce to 1 minute for high-frequency monitoring of critical VMs (increases storage). Aria Operations retains high-resolution data for 6 months, then rolls up to daily."),
        "enable_feature": ("How do I enable Aria Operations Workload Optimization?",
            "Go to Optimize → Workload Optimization → Enable. Configure automation policies (Manual, Automated). Start with Manual mode to review recommendations before applying. Workload Optimization rebalances VMs across hosts based on capacity."),
        "rolling_upgrade": ("How do I upgrade Aria Operations without downtime?",
            "Aria Operations supports rolling upgrades for clustered deployments. Use LCM or the PAK-based upgrade via Administration → Software Update. The primary node upgrades first, then data nodes one at a time."),
        "add_resource": ("What is the correct procedure to add a new vCenter adapter?",
            "Administration → Solutions → vCenter Server → Add New. Provide vCenter FQDN and credentials. Aria Operations discovers all inventory (VMs, hosts, clusters) within the first collection cycle (5 minutes)."),
        "warning": ("Aria Operations shows a VM with 'Anomalous Metrics'. What does it mean?",
            "Aria Operations' ML engine has detected metric values outside the normal baseline for that VM (CPU, memory, latency, etc.). Investigate whether this is expected load change or a problem. Check the 'What Changed' context in the alert details."),
        "perf": ("Aria Operations is slow and collectors are lagging — where do I start?",
            "Check Administration → Collector Groups for overloaded collectors. Balance object count across collectors. Check data node disk usage under Administration → Environment → Cluster Management. Consider adding data nodes for large environments."),
        "backup_freq": ("How often should I back up Aria Operations?",
            "Daily via LCM or Administration → Administration → Global Settings → Scheduled Backup. Backup includes all dashboards, alerts, policies, and custom metrics. Store off-appliance."),
        "restore": ("Can I restore a single dashboard without a full Aria Operations restore?",
            "Yes — dashboards can be exported to JSON (Dashboard → Export) and re-imported. Super Metrics and custom groups can also be exported individually. Full restore is needed only for system-level configuration recovery."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/aria-suite-lifecycle/operations", "aria-suite-lifecycle", "VMware Aria Suite Lifecycle Manager", {
        "version_check": ("What Aria Suite Lifecycle Manager version is recommended?",
            "LCM 8.16.x is the current recommendation — it must be upgraded first before any Aria Suite products. Check via Administration → System Details → Product Version."),
        "version_cmd": "Administration → System Details → Product Version",
        "default_setting": ("What is the default certificate management approach in LCM?",
            "LCM uses its own internal CA by default for Aria Suite product certificates. For production, integrate with your enterprise CA under Lifecycle Operations → Certificate Management → Request Certificate. This avoids browser certificate warnings."),
        "enable_feature": ("How do I enable LCM integration with vRealize Easy Installer for greenfield deployments?",
            "Download the Aria Suite Easy Installer OVA from VMware Customer Connect. Deploy it and run the installer wizard, which deploys and configures LCM, Identity Manager, and selected Aria Suite products in the correct order."),
        "rolling_upgrade": ("What is the correct upgrade order for Aria Suite products via LCM?",
            "Always upgrade in this order: 1) LCM itself, 2) VMware Identity Manager (Workspace ONE Access), 3) Aria Operations for Logs, 4) Aria Operations, 5) Aria Operations for Networks, 6) Aria Automation. Never skip this sequence."),
        "add_resource": ("What is the correct procedure to add a new environment to LCM?",
            "LCM → Lifecycle Operations → Create Environment. Specify datacenter and vCenter. Add product installers to the binary mapping. LCM will deploy and configure the product within the environment."),
        "warning": ("LCM shows 'Precheck failed: certificate validation error'. What does it mean?",
            "LCM cannot validate SSL certificates for connected products — usually caused by certificate expiry or a CA mismatch. Renew the certificate via LCM → Locker → Certificates before retrying the upgrade."),
        "perf": ("LCM upgrades are timing out mid-way — where do I start?",
            "Check LCM appliance resources (CPU, memory, disk). Verify network connectivity to all product appliances. Review LCM logs: `tail -f /var/log/vlcm/vlcm-app.log`. Increase LCM VM memory if running multiple product upgrades simultaneously."),
        "backup_freq": ("How often should I back up LCM?",
            "Weekly LCM backup via Administration → System Details → Request Backup. LCM backup includes all product mappings, environments, and locker content (certificates, passwords). Store off-appliance."),
        "restore": ("Can I restore LCM without restoring all managed Aria Suite products?",
            "Yes — LCM restore only restores the LCM management plane (inventory, mappings, locker). The Aria Suite products themselves are unaffected by an LCM restore. Reconnect products to the restored LCM after restore."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/esxi/operations", "esxi", "VMware ESXi", {
        "version_check": ("What ESXi version is recommended for new deployments?",
            "ESXi 8.0 Update 3 is the current recommendation. Check: `vmware -v` from ESXi shell or vCenter → Host → Summary → ESXi Version. Always align with the vCenter compatibility matrix."),
        "version_cmd": "vmware -v",
        "default_setting": ("What is the default SSH service configuration and when should it change?",
            "SSH is disabled by default on ESXi. Enable only for troubleshooting: Host → Configuration → Security Profile → SSH → Start. Disable immediately after use. Use host profiles to enforce this policy fleet-wide."),
        "enable_feature": ("How do I enable ESXi host profiles for configuration compliance?",
            "In vCenter, create a host profile from a reference host: Host Profiles → Extract Profile. Attach the profile to target hosts. Run compliance check. Remediate non-compliant hosts (requires maintenance mode for some settings)."),
        "rolling_upgrade": ("How do I patch ESXi hosts in a cluster without downtime?",
            "Use vSphere Lifecycle Manager (vLCM): Cluster → Updates → Remediate All. vLCM puts each host into maintenance mode (migrating VMs via vMotion), applies patches, and reboots. Process repeats per host. Requires DRS enabled."),
        "add_resource": ("What is the correct procedure to add a new host to a vSphere cluster?",
            "vCenter → Datacenter → Add Host. Enter the host FQDN/IP and root credentials. Add to the target cluster. vCenter validates the host, applies the cluster's host profile, and makes it available for VM placement."),
        "warning": ("ESXi shows 'Host in disconnected state' in vCenter. What does it mean?",
            "vCenter cannot communicate with the host's management agent (hostd). SSH to the host directly and run `service.sh restart`. If SSH is unavailable, reboot via iDRAC/IPMI. Check management network connectivity and firewall rules."),
        "perf": ("VM CPU ready time is high on a specific ESXi host — where do I start?",
            "Check host CPU utilisation in vCenter → Host → Monitor → Performance. High CPU ready indicates overcommitment. Use DRS to migrate VMs to less-loaded hosts. Review NUMA topology — cross-NUMA memory access adds latency."),
        "backup_freq": ("How often should I back up ESXi host configuration?",
            "Weekly via PowerCLI: `Get-VMHostFirmware -VMHost <host> -BackupConfiguration -DestinationPath ./`. Or via host profile compliance. Back up before any patch or upgrade. Store configs in version control."),
        "restore": ("Can I restore a single ESXi host configuration without rebuilding?",
            "Yes — restore from firmware backup: `Set-VMHostFirmware -VMHost <host> -Restore -SourcePath ./configBundle.tgz`. This restores network, storage, and firewall config. Test on a spare host first."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/horizon/operations", "horizon", "VMware Horizon", {
        "version_check": ("What Horizon version is recommended for new deployments?",
            "Horizon 8 (2312 or latest CR) is recommended. Check via Horizon Administrator console → Help → About. Connection Server and Agents should be on matching major versions."),
        "version_cmd": "Horizon Administrator → Help → About",
        "default_setting": ("What is the default session timeout and when should it change?",
            "Default idle session timeout is 10 minutes. Adjust per security policy: Global Settings → Global Policies → Session Timeout. For VDI desktops, 30-60 minutes is typical. For RDSH apps, 15 minutes is more appropriate."),
        "enable_feature": ("How do I enable Horizon Smart Policies for per-user peripheral control?",
            "Install Horizon Dynamic Environment Manager (DEM). Create Smart Policies in DEM → Smart Policies. Policies can control USB redirection, clipboard, printing, and audio per AD group or condition."),
        "rolling_upgrade": ("How do I upgrade Horizon Connection Servers without user disruption?",
            "Upgrade Connection Servers one at a time. Horizon supports mixed-version Connection Server pods temporarily. Upgrade the replica servers first, then the primary. Users connected to the upgraded server are not disconnected."),
        "add_resource": ("What is the correct procedure to add a new desktop pool?",
            "Horizon Administrator → Catalog → Desktop Pools → Add. Select pool type (Automated, Manual, or RDS). Configure the vCenter template, network, datastore, and desktop policy. Entitle the pool to AD groups."),
        "warning": ("Horizon shows 'Agent Unreachable' for a desktop pool. What does it mean?",
            "Connection Servers cannot reach the Horizon Agent on the desktop VMs. Check VM power state. Verify Horizon Agent service is running. Check network connectivity from Connection Server to the desktop network. Review firewall rules for ports 4001, 4002, 443."),
        "perf": ("User desktop performance is poor — where do I start?",
            "Check vSphere host CPU ready and memory balloon on the hosting ESXi. Review Blast display protocol settings (reduce quality for bandwidth-limited clients). Check storage latency for the desktop datastore (IOPS-intensive VDI workloads)."),
        "backup_freq": ("How often should I back up Horizon Connection Server configuration?",
            "Daily LDAP backup: `vdmexport.exe -f backup.ldf` on the Connection Server. This exports the entire Horizon configuration. Store off-server. Test restore to a lab Connection Server quarterly."),
        "restore": ("Can I restore a single desktop pool configuration without a full Horizon restore?",
            "Not directly — Horizon configuration is stored in an ADAM (Active Directory Application Mode) database. Restore requires the full LDAP export. Individual pool settings can be reconfigured manually if the pool metadata is lost."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/nsx/operations", "nsx", "VMware NSX", {
        "version_check": ("What NSX version is recommended for new deployments?",
            "NSX 4.1.x or 4.2.x is the current recommendation. Check: NSX Manager → System → Overview → Version. Always align NSX version with vCenter and ESXi compatibility matrix."),
        "version_cmd": "NSX Manager → System → Overview → Version",
        "default_setting": ("What is the default MTU requirement for NSX GENEVE overlay and when must it change?",
            "GENEVE encapsulation adds 50-54 bytes overhead. Physical network MTU must be at least 1600 bytes (recommended 9000 for jumbo frames). Configure uplink profiles accordingly. Failure to set MTU causes silent packet drops for large frames."),
        "enable_feature": ("How do I enable NSX Distributed Firewall for east-west microsegmentation?",
            "DFW is enabled by default once NSX is installed. Create security groups (Inventory → Groups) using VM tags, OS type, or AD groups. Create DFW policies (Security → Distributed Firewall → Add Policy). Apply default-deny with explicit allow rules."),
        "rolling_upgrade": ("How do I upgrade NSX without disrupting workload networking?",
            "Upgrade NSX Manager appliances first (N+1 rolling within the cluster). Then upgrade Edge clusters. Then upgrade host transport nodes one at a time (hosts remain in the fabric during upgrade — only the upgrade itself causes a brief disruption per host)."),
        "add_resource": ("What is the correct procedure to add a new T1 gateway and segment?",
            "NSX Manager → Networking → Tier-1 Gateways → Add. Link to existing T0. Create Segment: Networking → Segments → Add → connect to the T1. Set the subnet gateway address. Assign to VMs via vCenter port group."),
        "warning": ("NSX shows 'Edge node tunnel is down'. What does it mean?",
            "The GENEVE tunnel between the Edge node and transport nodes is failing. Check TEP IP reachability, MTU, and the uplink profile. Verify physical switch ports carrying the TEP VLAN are up. Review `get tunnel-port` from the Edge node CLI."),
        "perf": ("North-south throughput through NSX Edge is below expected — where do I start?",
            "Check Edge node CPU utilisation (DPDKs are single-threaded per core). Verify ECMP is configured across multiple Edge uplinks. Review DPDK queue statistics via Edge node CLI: `get dataplane l2fwd`. Add Edge nodes if throughput is near the per-node limit."),
        "backup_freq": ("How often should I back up NSX configuration?",
            "Daily automated backup: NSX Manager → System → Backup → Schedule. Store on a remote SFTP server. Backup includes all logical networking, security policies, and certificates. Test restore to a lab environment quarterly."),
        "restore": ("Can I restore a single DFW policy without a full NSX restore?",
            "Not natively. DFW policies are part of the NSX configuration database. Export policies to CSV/XML for documentation, but restoration requires the full NSX backup. Use NSX API (`GET /policy/api/v1/infra`) to export policy state for manual reconstruction."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/operations", "vmware", "VMware vSphere", {
        "version_check": ("How do I get a consolidated version view across a vSphere environment?",
            "vCenter → Menu → Lifecycle Manager → Cluster Compliance shows all host patch levels. For vCenter itself: vCenter → Administration → Deployment → System Configuration → Nodes → Software Version."),
        "version_cmd": "vCenter → Administration → Deployment → System Configuration → Software Version",
        "default_setting": ("What is the default DRS automation level and when should it change?",
            "DRS defaults to 'Fully Automated' for new clusters. Use 'Partially Automated' for production clusters where you want to approve vMotion recommendations before execution. Use 'Manual' only for troubleshooting."),
        "enable_feature": ("How do I enable vSphere Tanzu (Workload Management) on a cluster?",
            "vCenter → Workload Management → Enable. Select the cluster, configure the supervisor network (NSX or VDS-based), and Kubernetes API endpoint. Requires vSphere 7.0+ with Enterprise Plus licence and NSX or VDS-based networking."),
        "rolling_upgrade": ("How do I plan and execute a vSphere upgrade from 7.x to 8.x?",
            "Upgrade order: vCenter first, then ESXi hosts. Check compatibility matrix (HCL, guest OS, solutions). Use vLCM for ESXi upgrades. Upgrade one cluster at a time. Test VMs on upgraded hosts before decommissioning old hosts."),
        "add_resource": ("What is the correct procedure to add a new cluster to vCenter?",
            "vCenter → Datacenter → New Cluster. Configure DRS, HA, and vSAN settings. Add hosts. Apply cluster host profile. Configure storage and networking. Run cluster quickstart for guided setup."),
        "warning": ("vCenter shows 'HA host isolated'. What does it mean?",
            "The host cannot reach the HA management network. vSphere HA isolation response may restart VMs on the isolated host on other hosts. Check management network connectivity. Configure isolation addresses (isolation.address) to reduce false positives."),
        "perf": ("vCenter performance degraded after a large environment expansion — where do I start?",
            "Check VCSA resource utilisation (vcenter-cli shell: `df -h`, `top`). Consider upgrading VCSA hardware profile for large environments (25K+ VMs requires Large or X-Large deployment). Review vCenter statistics level — level 3/4 increases DB load."),
        "backup_freq": ("How often should I back up vCenter?",
            "Daily file-based backup: VCSA Management UI → Backup. Include database and seat data. Store remote (NFS/SFTP). Test restore quarterly using the VCSA restore wizard. Never use VM snapshots as the sole vCenter backup method."),
        "restore": ("Can I restore vCenter without restoring the ESXi hosts?",
            "Yes — VCSA restore is independent of ESXi hosts. Restore VCSA to a new appliance; it reconnects to existing ESXi hosts automatically. VMs continue running on ESXi during vCenter restore (EVC mode may need re-verification)."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/powercli/operations", "powercli", "VMware PowerCLI", {
        "version_check": ("What PowerCLI version is recommended?",
            "PowerCLI 13.x is the current recommendation. Check: `Get-Module VMware.PowerCLI -ListAvailable | Select Version`. Update: `Update-Module VMware.PowerCLI`."),
        "version_cmd": "Get-Module VMware.PowerCLI -ListAvailable | Select Version",
        "default_setting": ("What is the default certificate handling and when should it change?",
            "PowerCLI warns on self-signed certificates by default. Set `Set-PowerCLIConfiguration -InvalidCertificateAction Ignore` for lab environments only. In production, use valid certificates on vCenter and set to `Warn` or `Fail`."),
        "enable_feature": ("How do I enable PowerCLI to manage multiple vCenters simultaneously?",
            "Connect to multiple vCenters: `Connect-VIServer -Server vc1,vc2`. Use `$global:DefaultVIServers` to see all connections. Target specific servers: `Get-VM -Server vc1`. Disconnect individually: `Disconnect-VIServer -Server vc1`."),
        "rolling_upgrade": ("How do I use PowerCLI to automate ESXi patch remediation?",
            "Use `Install-VMHostPatch` or the newer vLCM API via `Invoke-VsanCommand`. For staged remediation: `Get-VMHost | where State -eq 'Connected' | ForEach { Set-VMHost $_ -State Maintenance; Install-VMHostPatch ...; Set-VMHost $_ -State Connected }`."),
        "add_resource": ("What is the correct procedure to bulk-add VMs to a folder using PowerCLI?",
            "`$folder = Get-Folder 'Production'; Get-VM | where Name -match 'prod-' | Move-VM -Destination $folder`. Verify with `Get-VM -Location $folder`. Use `-WhatIf` parameter first to preview changes before execution."),
        "warning": ("PowerCLI shows 'Server certificate validation error'. What does it mean?",
            "The vCenter certificate is not trusted by the PowerCLI client. Either set `Set-PowerCLIConfiguration -InvalidCertificateAction Ignore` (lab only) or import the vCenter CA certificate into the Windows certificate store."),
        "perf": ("Large PowerCLI scripts run slowly against big vCenter inventories — where do I start?",
            "Use `Get-View` instead of `Get-VM` for bulk queries — it uses direct API calls without object wrapping. Filter server-side: `Get-View -ViewType VirtualMachine -Filter @{Name='prod-*'}`. Avoid `Get-VM | where` which retrieves all VMs first."),
        "backup_freq": ("How do I back up PowerCLI scripts and modules?",
            "Store all PowerCLI scripts in Git. Pin module versions in a `requirements.psd1`. For DSC-based automation, version-control the configuration files. Use a private PowerShell repository (Azure Artifacts, Nexus) for internal modules."),
        "restore": ("Can I recover a deleted VM configuration using PowerCLI?",
            "If the VM was removed from inventory (not deleted from disk), re-register: `New-VM -VMFilePath '[datastore] vm/vm.vmx' -ResourcePool <pool>`. If deleted from disk, restore from backup using your backup tool's PowerShell cmdlets."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/srm/operations", "srm", "VMware Site Recovery Manager", {
        "version_check": ("What SRM version is recommended?",
            "SRM 8.8.x is the current recommendation. Check: SRM UI → Help → About. SRM version must be compatible with the paired vCenter versions. Check the VMware Product Interoperability Matrix."),
        "version_cmd": "SRM UI → Help → About",
        "default_setting": ("What are the protection group types and when to use each?",
            "Two types: vSphere Replication (RPO: 5 minutes to 24 hours, no shared storage needed) and Array-Based Replication (RPO depends on array, requires supported storage array). Use array-based for zero or near-zero RPO; vSphere Replication for cost-effective DR."),
        "enable_feature": ("How do I enable IP customisation rules for network reconfiguration during failover?",
            "In SRM, go to Recovery Plans → select plan → IP Customization Rules. Map source-site IP ranges to recovery-site ranges. SRM applies these rules automatically during failover to update guest IP addresses using VMware Tools."),
        "rolling_upgrade": ("How do I upgrade SRM without breaking existing protection groups?",
            "Upgrade the recovery site SRM first, then the protected site. Protection groups and recovery plans persist through upgrades. After upgrade, verify all protection groups show 'OK' status in SRM UI."),
        "add_resource": ("What is the correct procedure to add a new VM to an SRM protection group?",
            "In SRM → Protection Groups → select group → VMs → Add VMs. Select the VM. SRM begins replication (vSphere Replication) or verifies array replication is active. Run a test failover after adding the VM to validate."),
        "warning": ("SRM shows 'RPO Violation' for a protected VM. What does it mean?",
            "Replication has fallen behind the configured RPO target. For vSphere Replication: check network bandwidth between sites. For array-based: check array replication status. Resolve the underlying replication issue before the next planned or test failover."),
        "perf": ("SRM test failover is taking longer than expected — where do I start?",
            "Review recovery plan step timing in the SRM recovery history. Long times are usually due to: VM power-on ordering, IP customisation scripts, or storage snapshot presentation. Optimise recovery plan step sequencing."),
        "backup_freq": ("How often should I test SRM recovery plans?",
            "Test failover quarterly minimum. Use SRM's 'Test' mode — it creates isolated snapshots and does not affect production. Document test results and resolve any errors before the next test. Full planned failover test annually."),
        "restore": ("What is the difference between Test Failover, Planned Failover, and Disaster Recovery failover in SRM?",
            "Test: isolated test (production unaffected). Planned Failover: orderly migration to recovery site (both sites available). Disaster Recovery: emergency failover when protected site is unavailable. Only DR failover is one-way without automatic failback."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/tanzu/operations", "tanzu", "VMware Tanzu", {
        "version_check": ("What Tanzu Kubernetes Grid version is recommended?",
            "TKG 2.4.x or the Supervisor-embedded Kubernetes version tied to your vSphere version. Check: `tanzu version` (CLI) or vCenter → Workload Management → Supervisors → Kubernetes version."),
        "version_cmd": "tanzu version",
        "default_setting": ("What is the default node size for Tanzu Kubernetes clusters?",
            "Default is 2 vCPU / 4 GB RAM per worker node (small). Use medium (2 vCPU / 8 GB) or large (4 vCPU / 16 GB) for production workloads. Set in the TanzuKubernetesCluster spec under `nodePools[].vmClass`."),
        "enable_feature": ("How do I enable Tanzu Service Mesh (TSM) for inter-cluster networking?",
            "TSM is a separate SaaS service (console.cloud.vmware.com). Onboard clusters by deploying the TSM agent: `kubectl apply -f tsm-agent.yaml`. Configure global namespaces for cross-cluster service discovery."),
        "rolling_upgrade": ("How do I upgrade Tanzu Kubernetes clusters without downtime?",
            "Update the TanzuKubernetesCluster spec to the new Kubernetes version. The supervisor performs rolling node replacement. Control plane nodes update first, then workers one at a time. Monitor with `kubectl get nodes -w`."),
        "add_resource": ("What is the correct procedure to provision a new Tanzu Kubernetes cluster?",
            "kubectl apply a `TanzuKubernetesCluster` CR in the vSphere namespace. Specify control plane and worker node count, VM class, and storage class. The Supervisor creates the cluster within 10-20 minutes."),
        "warning": ("Tanzu Kubernetes cluster shows 'NodeNotReady'. What does it mean?",
            "A cluster node cannot communicate with the API server or its kubelet is unhealthy. Check the node VM in vCenter. SSH to the node and check `systemctl status kubelet`. Common causes: disk pressure, network misconfiguration, or failed CNI plugin."),
        "perf": ("Pods on Tanzu clusters have high scheduling latency — where do I start?",
            "Check node resource utilisation: `kubectl describe nodes | grep -A5 Allocated`. Review scheduler events: `kubectl get events --sort-by=.metadata.creationTimestamp`. Check storage class provisioning time — slow PVC creation delays pod starts."),
        "backup_freq": ("How often should I back up Tanzu cluster configuration?",
            "Store all TanzuKubernetesCluster manifests in Git. Use Velero (installed via Tanzu Mission Control) for application-level namespace backup. Back up the Supervisor etcd as part of vCenter backup."),
        "restore": ("Can I restore a deleted Tanzu namespace without a full cluster restore?",
            "If Velero backups were configured, restore the namespace: `velero restore create --from-backup <backup-name> --include-namespaces <ns>`. Without Velero, the namespace content is lost — only the TanzuKubernetesCluster CR (stored in vCenter) is recoverable."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/vcenter/operations", "vcenter", "VMware vCenter", {
        "version_check": ("What vCenter version is recommended for new deployments?",
            "vCenter 8.0 Update 3 is the current recommendation. Check: VCSA VAMI (https://vcenter:5480) → Summary → Version. vCenter must be at least equal to or newer than all managed ESXi hosts."),
        "version_cmd": "https://<vcenter>:5480 → Summary → Version",
        "default_setting": ("What is the default SSO lockout policy and when should it change?",
            "Default SSO lockout is 5 failed attempts in 3 minutes, locked for 5 minutes. Align with your corporate password policy. Adjust via vCenter → Administration → Single Sign On → Configuration → Lockout Policy."),
        "enable_feature": ("How do I enable vCenter HA for management plane redundancy?",
            "vCenter → Administration → vCenter HA → Set Up vCenter HA. Requires a dedicated HA network between active, passive, and witness nodes. VCHA provides automatic failover of vCenter with sub-minute RTO."),
        "rolling_upgrade": ("What is the correct upgrade order when upgrading vCenter and ESXi?",
            "Always upgrade vCenter before ESXi hosts. vCenter N supports ESXi N-2, but not the reverse. After upgrading vCenter, upgrade hosts via vLCM. Test a single host first. Upgrade clusters one at a time."),
        "add_resource": ("What is the correct procedure to add a new PSC (legacy) or renew SSO after a cert change?",
            "For embedded VCSA (8.x): re-run `certificate-manager` (option 4 or 6). For vCenter HA, certificate renewal must be coordinated across all VCHA nodes. Refer to KB 2112283 for the certificate renewal order."),
        "warning": ("vCenter shows 'SSL certificate will expire in 30 days'. What does it mean?",
            "The machine SSL certificate (used for vCenter API/HTTPS) is nearing expiry. Renew via VCSA VAMI → Certificate Management → Machine SSL Certificate → Renew. Schedule renewal during a maintenance window — vCenter services restart."),
        "perf": ("vCenter is slow and the vSphere Client takes a long time to load — where do I start?",
            "SSH to VCSA and check `top` for CPU/memory. Check disk space: `df -h`. Review vpxd logs: `tail -f /var/log/vmware/vpx/vpxd.log`. Check database health: `service-control --status vmware-vpostgres`. Large inventories may require VCSA large/xlarge sizing."),
        "backup_freq": ("How often should I back up vCenter?",
            "Daily file-based backup via VCSA VAMI → Backup → Schedule. Remote SFTP/FTP/HTTP destination. Backup includes: database, config, and seat data. Test restore quarterly. Retain at least 7 daily backups."),
        "restore": ("Can I restore vCenter while VMs continue running on ESXi hosts?",
            "Yes — restore VCSA to a new appliance. VMs continue running on ESXi hosts independently. After restore, vCenter reconnects to ESXi hosts and discovers running VMs. Check vCenter HA config after restore if VCHA was in use."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/vmware-cloud-foundation/operations", "vcf", "VMware Cloud Foundation", {
        "version_check": ("What VCF version is recommended for new deployments?",
            "VCF 5.1.x or 5.2.x is the current recommendation. Check: SDDC Manager → Settings → System Configuration → Version. VCF version determines the compatible versions of all bundled components."),
        "version_cmd": "SDDC Manager → Settings → System Configuration → Version",
        "default_setting": ("What is the default workload domain configuration?",
            "The Management Domain is created during VCF bringup and hosts management components. Create additional VI Workload Domains for production workloads. Never run production VMs in the Management Domain."),
        "enable_feature": ("How do I enable VCF+ for cloud-connected management?",
            "In SDDC Manager → Administration → VCF+ → Activate. Requires a My VMware account linked to the VCF licence. VCF+ enables Skyline health checks, cloud-based inventory, and enhanced lifecycle management."),
        "rolling_upgrade": ("How do I upgrade VCF using the SDDC Manager lifecycle workflow?",
            "SDDC Manager → Lifecycle Management → Software Updates → check for updates → Download → Schedule. SDDC Manager orchestrates the upgrade sequence: SDDC Manager → NSX → vCenter → ESXi hosts. Upgrade the Management Domain first, then Workload Domains."),
        "add_resource": ("What is the correct procedure to expand a VCF Workload Domain with new hosts?",
            "Commission hosts via SDDC Manager → Inventory → Hosts → Commission Hosts. Then expand the Workload Domain: SDDC Manager → Workload Domains → select domain → Add Hosts. SDDC Manager configures networking, storage, and vSphere automatically."),
        "warning": ("SDDC Manager shows 'Component health check failed'. What does it mean?",
            "SDDC Manager's health check detected an issue with a VCF component (vCenter, NSX, ESXi, vSAN). Go to SDDC Manager → Health → view the failing check. Address the underlying component issue before proceeding with any lifecycle operations."),
        "perf": ("VCF lifecycle operations are slow — where do I start?",
            "Check SDDC Manager appliance resources. Verify inter-component network connectivity. Review bundle download speed — pre-stage bundles during off-peak hours. For large environments, check NSX manager health before upgrades."),
        "backup_freq": ("How often should I back up VCF SDDC Manager?",
            "Daily via SDDC Manager → Administration → Backup and Restore → Configure Backup. Backup includes all workload domain configurations, commission data, and licence information. Store on external SFTP. Also back up all component products (vCenter, NSX) individually."),
        "restore": ("Can I restore a single Workload Domain configuration without a full SDDC Manager restore?",
            "Not independently — VCF configuration is holistic within SDDC Manager. For component-level recovery, restore vCenter or NSX individually. SDDC Manager restore is needed only when SDDC Manager itself is lost."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/vsan/operations", "vsan", "VMware vSAN", {
        "version_check": ("What vSAN version is recommended?",
            "vSAN ships with vSphere — use the version matching your vCenter/ESXi 8.0 Update 3 deployment. Check: vCenter → Cluster → Configure → vSAN → General → vSAN Version."),
        "version_cmd": "vCenter → Cluster → Configure → vSAN → General → vSAN Version",
        "default_setting": ("What is the default storage policy and when should it change?",
            "Default is FTT=1 (RAID-1), meaning data is mirrored across 2 hosts. Increase to FTT=2 for mission-critical VMs (tolerates 2 host failures, requires 5+ hosts for RAID-6). Use RAID-5/6 erasure coding for space efficiency over 4+ hosts."),
        "enable_feature": ("How do I enable vSAN deduplication and compression?",
            "Cluster → Configure → vSAN → Services → Deduplication and Compression → Enable. All-flash only. Services apply cluster-wide (per disk group). Expect 1.5-2x space savings for typical VDI workloads; variable for databases."),
        "rolling_upgrade": ("How do I patch vSAN hosts without downtime?",
            "Use vLCM with cluster remediation. vLCM puts one host into maintenance mode at a time (evacuating vSAN components), patches it, reboots, and waits for vSAN resync before moving to the next host. Never patch more than 1 host at a time in a 4-node cluster."),
        "add_resource": ("What is the correct procedure to add a new disk group to a vSAN host?",
            "Ensure the drives are unclaimed. vCenter → Host → Configure → vSAN → Disk Management → Claim Disks. Select the cache and capacity drives. vSAN builds the disk group and rebalances automatically."),
        "warning": ("vSAN health shows yellow 'Performance service'. What does it mean?",
            "The vSAN performance service (stats collection) is degraded or disabled. Enable it: Cluster → Monitor → vSAN → Performance → Enable vSAN Performance Service. Yellow is non-critical — storage continues to function normally."),
        "perf": ("vSAN storage latency is elevated — where do I start?",
            "Check vSAN performance service: Cluster → Monitor → vSAN → Performance → Backend. Review disk group cache hit ratio. Check for rebalancing activity (`resync` operations). Verify physical disk health with `esxcli vsan storage list`."),
        "backup_freq": ("How often should I back up vSAN configuration?",
            "vSAN configuration is part of the vCenter/cluster config — back up vCenter daily. For vSAN stretched cluster witness VM, back it up separately. Storage policies are in vCenter — they are included in the vCenter backup."),
        "restore": ("Can I recover from a disk failure in a vSAN cluster?",
            "vSAN automatically re-replicates data after a disk or host failure, as long as the cluster remains above the FTT threshold. Replace the failed disk. vSAN rebuilds the component on the new disk. Monitor with `esxcli vsan debug object list`."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/vsphere-replication/operations", "vsphere-replication", "VMware vSphere Replication", {
        "version_check": ("What vSphere Replication version is recommended?",
            "vSphere Replication 8.8.x is the current recommendation. Check: vSphere Replication appliance web UI (https://vr-appliance:5480) → Summary → Version."),
        "version_cmd": "https://<vr-appliance>:5480 → Summary → Version",
        "default_setting": ("What is the minimum RPO for vSphere Replication?",
            "Minimum RPO is 5 minutes. This is not suitable for zero-RPO requirements — use array-based replication (SRDF, SnapMirror) for near-zero RPO. vSphere Replication suits RPO of 15 minutes to 24 hours for most use cases."),
        "enable_feature": ("How do I enable multi-point-in-time (MPIT) recovery for vSphere Replication?",
            "When configuring replication, enable 'Enable multiple point in time instances'. Set the number of instances (up to 24). MPIT retains multiple recovery points at the target, allowing recovery to a specific point before ransomware or corruption."),
        "rolling_upgrade": ("How do I upgrade vSphere Replication without breaking active replications?",
            "Active replications pause briefly during upgrade but resume automatically. Upgrade the vSphere Replication appliance via its VAMI (5480 port). Do not reconfigure replications during upgrade. Verify all replications resume within 30 minutes post-upgrade."),
        "add_resource": ("What is the correct procedure to configure replication for a new VM?",
            "vCenter → VM → Actions → All vSphere Replication Actions → Configure Replication. Select the target site VR server and datastore. Set RPO. Initial full sync begins immediately — monitor progress in vCenter → Monitor → vSphere Replication."),
        "warning": ("vSphere Replication shows 'RPO violation' for a VM. What does it mean?",
            "The last successful replication sync exceeded the configured RPO window. Check vSphere Replication appliance health. Verify network bandwidth between sites. Check if the source VM has high change rate. Review vSphere Replication logs for error details."),
        "perf": ("Replication bandwidth is saturating the WAN link — where do I start?",
            "Configure bandwidth throttling: vSphere Replication → Site → Bandwidth Throttling. Stagger replication schedules to avoid concurrent syncs. Enable compression (vSphere Replication compresses data in transit by default)."),
        "backup_freq": ("How often should I test vSphere Replication recovery?",
            "Use SRM test failover quarterly (if SRM is in use). For standalone vSphere Replication, perform a manual test recovery to an isolated network annually. Verify application consistency of recovered VMs."),
        "restore": ("How do I recover a VM using vSphere Replication when the source site is unavailable?",
            "At the recovery site, vCenter → Monitor → vSphere Replication → Incoming Replications → select VM → Recover. The VM is powered on from the latest replica. For MPIT, select the desired recovery point before recovering."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("virtualization/vmware/vxrail/operations", "vxrail", "Dell VxRail", {
        "version_check": ("What VxRail software bundle version is recommended?",
            "VxRail 8.0.2xx or the latest validated bundle for your hardware generation. Check: VxRail Manager UI → Settings → Software → Installed Version. VxRail Manager also shows available upgrade packages."),
        "version_cmd": "VxRail Manager UI → Settings → Software → Installed Version",
        "default_setting": ("What is the default VxRail vSAN storage policy?",
            "Default is FTT=1 RAID-1 (2-node mirror). For VxRail clusters with 5+ nodes, consider FTT=2 RAID-6 for better space efficiency. Storage policies are managed in vCenter — VxRail Manager uses the same vSAN policy framework."),
        "enable_feature": ("How do I enable VxRail automated HCI System Software upgrades?",
            "VxRail Manager → LCM → Software Update. VxRail packages all component updates (vSphere, vSAN, VxRail Manager, Dell firmware) into a single validated bundle. Enable the update in VxRail Manager and it orchestrates the full rolling upgrade."),
        "rolling_upgrade": ("How does VxRail LCM perform a rolling cluster upgrade?",
            "VxRail LCM puts one node into maintenance mode (migrating VMs via vMotion and vSAN data), applies the firmware and software bundle, reboots, waits for vSAN resync, then proceeds to the next node. Typically 30-60 minutes per node."),
        "add_resource": ("What is the correct procedure to add a new node to a VxRail cluster?",
            "Rack and cable the new node. Power on. In VxRail Manager → Cluster → Add Node. VxRail Manager discovers the node, validates hardware compatibility, and joins it to the cluster. Data rebalancing begins automatically."),
        "warning": ("VxRail Manager shows 'Node health critical'. What does it mean?",
            "A hardware component (drive, NIC, PSU) in a node has failed or is degraded. VxRail Manager creates a SupportAssist case with Dell automatically for hardware issues. Log into iDRAC for the specific node to see the hardware error details."),
        "perf": ("VxRail VM performance is below expectations after adding workloads — where do I start?",
            "Check vSAN performance in vCenter → Cluster → Monitor → vSAN → Performance. Review vSAN cache hit ratio. Verify VxRail nodes have adequate CPU and memory headroom. Check that new workloads are not exceeding the vSAN all-flash write buffer."),
        "backup_freq": ("How often should I back up VxRail configuration?",
            "VxRail Manager configuration is backed up as part of the vCenter backup (VxRail Manager runs as a VM). Additionally, export the VxRail appliance config from VxRail Manager → Settings → System → Export Configuration weekly."),
        "restore": ("Can I recover a failed VxRail node without losing data?",
            "If one node fails, vSAN reprotects data to remaining nodes (for FTT=1 clusters). Replace the failed node and VxRail Manager guides the replacement process (node must match hardware model). Data is rebuilt on the replacement node automatically."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
]

def make_svg(slug):
    boxes = ["Identify Question", "Find Answer", "Verify Context", "Apply Solution", "✓ Issue Resolved"]
    w, h = 820, 200
    box_w, box_h = 130, 60
    gap = 15
    total = len(boxes) * box_w + (len(boxes) - 1) * gap
    start_x = (w - total) // 2
    y_center = h // 2

    svg = ET.Element("svg", xmlns="http://www.w3.org/2000/svg", width=str(w), height=str(h))
    defs = ET.SubElement(svg, "defs")
    grad = ET.SubElement(defs, "linearGradient", id="hdr", x1="0", y1="0", x2="1", y2="0")
    ET.SubElement(grad, "stop", offset="0%", style="stop-color:#1a2744")
    ET.SubElement(grad, "stop", offset="100%", style="stop-color:#2a3f6f")

    ET.SubElement(svg, "rect", width=str(w), height=str(h), fill="#f8f9fa")
    ET.SubElement(svg, "rect", width=str(w), height="32", fill="url(#hdr)")
    title = ET.SubElement(svg, "text", x=str(w // 2), y="21",
                           fill="white", **{"font-family": "sans-serif", "font-size": "13",
                                            "font-weight": "bold", "text-anchor": "middle"})
    title.text = "FAQ — Operations Guide"

    colors = ["#1a2744", "#1e3a5f", "#155e75", "#065f46", "#14532d"]
    for i, (label, color) in enumerate(zip(boxes, colors)):
        x = start_x + i * (box_w + gap)
        y = y_center - box_h // 2
        ET.SubElement(svg, "rect", x=str(x), y=str(y), width=str(box_w), height=str(box_h),
                       rx="6", fill=color)
        lines = label.split()
        mid = len(lines) // 2
        for j, word in enumerate(lines):
            dy = (j - mid) * 16 + (8 if len(lines) == 1 else 0)
            t = ET.SubElement(svg, "text",
                               x=str(x + box_w // 2), y=str(y_center + dy),
                               fill="white", **{"font-family": "sans-serif", "font-size": "11",
                                                "text-anchor": "middle"})
            t.text = word
        if i < len(boxes) - 1:
            ax = x + box_w + 2
            ay = y_center
            ET.SubElement(svg, "polygon",
                           points=f"{ax},{ay-5} {ax+gap-4},{ay} {ax},{ay+5}",
                           fill="#94a3b8")

    return ET.tostring(svg, encoding="unicode")

def depth_prefix(path_from_docs):
    parts = path_from_docs.rstrip("/").split("/")
    return "../" * len(parts)

def slug_from_path(path_from_docs):
    parts = path_from_docs.rstrip("/").split("/")
    return "-".join(parts) + "-faq"

created_files = []
created_svgs = []

for path_from_docs, tag, product_name, qa in PRODUCTS:
    full_dir = os.path.join(BASE, path_from_docs)
    faq_path = os.path.join(full_dir, "faq.md")
    if os.path.exists(faq_path):
        print(f"SKIP: {faq_path}")
        continue

    slug = slug_from_path(path_from_docs)
    prefix = depth_prefix(path_from_docs)
    svg_rel = f"{prefix}assets/{slug}.svg"

    content = f"""---
tags:
  - {tag}
  - faq
  - operations
---
# {product_name} — Frequently Asked Questions

<div class="kb-summary">
Common questions about {product_name} operations, configuration, and troubleshooting. For step-by-step procedures, see the <a href="index.md">Operations</a> section.
</div>

![{product_name} FAQ]({svg_rel})

## General

**Q: {qa['version_check'][0]}**
A: {qa['version_check'][1]}

**Q: How do I check the current {product_name} version?**
A: `{qa['version_cmd']}`

## Configuration

**Q: {qa['default_setting'][0]}**
A: {qa['default_setting'][1]}

**Q: {qa['enable_feature'][0]}**
A: {qa['enable_feature'][1]}

## Operations

**Q: {qa['rolling_upgrade'][0]}**
A: {qa['rolling_upgrade'][1]}

**Q: {qa['add_resource'][0]}**
A: {qa['add_resource'][1]}

## Troubleshooting

**Q: {qa['warning'][0]}**
A: {qa['warning'][1]}

**Q: {qa['perf'][0]}**
A: {qa['perf'][1]}

## Backup and Recovery

**Q: {qa['backup_freq'][0]}**
A: {qa['backup_freq'][1]}

**Q: {qa['restore'][0]}**
A: {qa['restore'][1]}

## See Also

- [{product_name} Operations](index.md)
- [{product_name} Troubleshooting]({qa['ts_link']})
"""
    os.makedirs(full_dir, exist_ok=True)
    with open(faq_path, "w") as f:
        f.write(content)
    created_files.append(faq_path)

    svg_path = os.path.join(ASSETS, f"{slug}.svg")
    if not os.path.exists(svg_path):
        svg_content = make_svg(slug)
        ET.fromstring(svg_content)
        with open(svg_path, "w") as f:
            f.write(svg_content)
        created_svgs.append(svg_path)

print(f"Created {len(created_files)} FAQ files, {len(created_svgs)} SVGs (batch 4)")
