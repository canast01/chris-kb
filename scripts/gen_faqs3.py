#!/usr/bin/env python3
"""Generate FAQ stubs — batch 3: storage (Dell, NetApp, Pure, Ceph)."""

import os
import xml.etree.ElementTree as ET

BASE = "/Users/chrisanastasiadis/chris-kb/docs"
ASSETS = "/Users/chrisanastasiadis/chris-kb/docs/assets"

PRODUCTS = [
    ("storage/ceph/operations", "ceph", "Ceph", {
        "version_check": ("What Ceph version is recommended for new deployments?",
            "Ceph Reef (18.x) is the current LTS. Check with `ceph version` on any monitor node. Avoid releases older than Quincy (17.x) for new deployments."),
        "version_cmd": "ceph version",
        "default_setting": ("What is the default replication factor and when should it change?",
            "Default pool size is 3 replicas (`osd_pool_default_size = 3`). Reduce to 2 only for non-critical data with adequate OSD count. Never run `size=1` in production — a single OSD failure causes data loss."),
        "enable_feature": ("How do I enable Ceph Dashboard for cluster monitoring?",
            "Enable the dashboard module: `ceph mgr module enable dashboard`. Set credentials: `ceph dashboard create-self-signed-cert; ceph dashboard ac-user-create admin -i <password_file> administrator`. Access at `https://<mgr-host>:8443`."),
        "rolling_upgrade": ("How do I perform a rolling Ceph upgrade without downtime?",
            "Upgrade monitors first (one at a time), then managers, then OSDs. Use `ceph orch upgrade start --ceph-version <version>` with cephadm. Monitor progress with `ceph orch upgrade status`. Set `noout` flag before OSD upgrades: `ceph osd set noout`."),
        "add_resource": ("What is the correct procedure to add a new OSD node?",
            "Add the node to cephadm: `ceph orch host add <hostname> <ip>`. Deploy OSDs: `ceph orch daemon add osd <hostname>:/dev/sdX`. Verify OSD joins the cluster: `ceph osd tree`. Remove `noout` flag if set."),
        "warning": ("Ceph health shows 'HEALTH_WARN: X pgs degraded'. What does it mean?",
            "Some placement groups have fewer than the required replica count. Usually caused by a downed OSD. Check `ceph osd stat` and `ceph osd tree` for down OSDs. Recovery begins automatically when the OSD comes back or is replaced."),
        "perf": ("Ceph cluster throughput is below expectations — where do I start?",
            "Check `ceph osd perf` for per-OSD latency. Verify network bandwidth between OSDs (cluster network). Check `ceph df` for near-full OSDs (>85% triggers backpressure). Review `ceph pg stat` for scrubbing activity."),
        "backup_freq": ("How often should I back up Ceph cluster configuration?",
            "Back up monitor config: `ceph config-key dump > ceph-config-backup.json` weekly. With cephadm, back up `/etc/ceph/` and the cephadm spec files. Test restore to a lab cluster annually."),
        "restore": ("Can I recover a single lost OSD's data without full cluster restore?",
            "If replication factor >= 2 and the remaining OSDs are healthy, Ceph automatically re-replicates lost data to surviving OSDs. Simply replace the failed OSD and Ceph backfills it. No manual restore needed for single-OSD failures."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("storage/dell/apex-storage-as-a-service/operations", "dell-apex-saas", "Dell APEX Storage as a Service", {
        "version_check": ("How do I check the current APEX Storage firmware version?",
            "Log in to the APEX Console at console.apex.dell.com. Navigate to your storage service → Details → Software Version. Dell manages firmware updates automatically for APEX services."),
        "version_cmd": "APEX Console → Storage Service → Details → Software Version",
        "default_setting": ("What is the default performance tier for new APEX Storage volumes?",
            "Performance tier is selected during service configuration. For most workloads, select 'Performance' (NVMe-backed). Use 'Standard' only for archival or low-IOPS workloads. Tier changes require a service reconfiguration request."),
        "enable_feature": ("How do I enable data-at-rest encryption for an APEX Storage service?",
            "Encryption is enabled by default for all APEX Storage services. Dell manages the encryption keys unless you configure Customer-Managed Keys (CMK) via the APEX Console → Security → Encryption Settings."),
        "rolling_upgrade": ("How does Dell handle firmware upgrades for APEX Storage?",
            "Dell handles all firmware upgrades as part of the APEX managed service. You receive advance notification of planned maintenance windows. APEX upgrades are non-disruptive for supported configurations. You cannot manually trigger or defer upgrades."),
        "add_resource": ("What is the correct procedure to expand APEX Storage capacity?",
            "In APEX Console, navigate to your service → Manage → Expand. Select additional capacity increment. Expansion is elastic — no hardware intervention required. Capacity is available within minutes for all-flash tiers."),
        "warning": ("APEX Console shows 'Service Health: Degraded'. What does it mean?",
            "One or more components of your APEX service have reduced redundancy. Dell Support is automatically notified and a case is created. Review the alert details for estimated resolution time. Contact Dell Support if no case appears within 30 minutes."),
        "perf": ("APEX Storage performance is below contracted SLA — where do I start?",
            "Review APEX Console performance metrics. If below SLA, open a support case via the APEX Console — Dell will investigate infrastructure health. Review host-side I/O patterns (queue depth, block size) that may be limiting throughput."),
        "backup_freq": ("How is APEX Storage data protected?",
            "APEX Storage includes built-in redundancy (RAID/erasure coding). For backup, you configure your own solution (Veeam, Commvault) targeting the APEX volumes. Dell does not manage application-level backups within the APEX service."),
        "restore": ("Can I request a point-in-time restore for APEX Storage?",
            "APEX Storage supports native snapshots (configure via APEX Console or REST API). Restore from a snapshot via the APEX Console → Storage → Snapshots → Restore. Restores are volume-level, not file-level."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/cloudiq/operations", "dell-cloudiq", "Dell CloudIQ", {
        "version_check": ("How do I check the CloudIQ version?",
            "CloudIQ is a SaaS platform — Dell manages versioning. Check the current release notes at dell.com/support. The platform version is shown in CloudIQ UI → Help → About."),
        "version_cmd": "CloudIQ UI → Help → About",
        "default_setting": ("What is the default health score threshold for alerts?",
            "CloudIQ generates alerts when health score drops below 80 (default). Customise thresholds per system type under Settings → Alerting. Set email or webhook notifications for score drops below your defined threshold."),
        "enable_feature": ("How do I enable CloudIQ for a new Dell storage system?",
            "Ensure SupportAssist (formerly Secure Remote Services) is active on the system. In CloudIQ, go to Settings → Connected Systems → Add. The system must have outbound HTTPS (443) connectivity to CloudIQ SaaS endpoints."),
        "rolling_upgrade": ("How does CloudIQ handle new feature rollouts?",
            "CloudIQ is a SaaS platform — Dell rolls out new features automatically. No action required. Check the CloudIQ What's New page monthly for feature updates. New features may require opt-in for preview."),
        "add_resource": ("What is the correct procedure to add a new storage system to CloudIQ?",
            "Register the system with SupportAssist (CloudIQ ingests data automatically once SupportAssist is active). Verify in CloudIQ → Systems within 24 hours. Configure notification recipients and thresholds for the new system."),
        "warning": ("CloudIQ shows 'Connectivity Lost' for a system. What does it mean?",
            "The system has not sent telemetry to CloudIQ for more than the expected interval. Check the system's SupportAssist connectivity. Verify the proxy configuration if the system routes outbound traffic via proxy. Check for firewall rule changes."),
        "perf": ("CloudIQ performance prediction shows an upcoming capacity breach — where do I start?",
            "Review the capacity trend chart. If breach is within 90 days, initiate capacity expansion planning. Use CloudIQ's 'What-if' analysis to model the impact of adding drives or volumes. Engage Dell account team for procurement lead times."),
        "backup_freq": ("Should I back up CloudIQ data?",
            "CloudIQ is a SaaS platform — Dell manages data retention and backup. Historical performance and capacity data is retained per the CloudIQ data retention policy (typically 90 days hot, longer for trend analysis). No customer action required."),
        "restore": ("Can I recover CloudIQ historical data if my system was offline?",
            "Data collected while the system was offline is lost — CloudIQ only ingests live telemetry. Historical trends show a gap for the offline period. If the system was online but connectivity was interrupted, some data may be buffered and uploaded when connectivity restores."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/cod/operations", "dell-cod", "Dell Capacity on Demand", {
        "version_check": ("How do I check which CoD licences are active on a Dell array?",
            "For PowerMax: Unisphere → System → Licences → CoD. For PowerStore: PowerStore Manager → Settings → Licences. For Unity: Unisphere for Unity → System → Licences."),
        "version_cmd": "Unisphere → System → Licences → Capacity on Demand",
        "default_setting": ("What is the default CoD capacity increment?",
            "CoD increments are defined in the purchase agreement and vary by array model. Typical increments: PowerMax 2500: 5 TB raw per increment. Confirm your entitlement in the CoD order documentation or Dell account portal."),
        "enable_feature": ("How do I activate a CoD capacity increment?",
            "Log a request with Dell Support providing the array serial number and desired increment. Dell remotely activates the capacity increment and provides a licence key. Apply the key in Unisphere under System → Licences → Apply Licence."),
        "rolling_upgrade": ("How do I plan for CoD capacity without disrupting production?",
            "Monitor utilisation trends in CloudIQ. Request CoD activation when utilisation reaches 75%. CoD activation is non-disruptive — no downtime required. The new capacity is available immediately after key application."),
        "add_resource": ("What is the correct procedure to request a CoD increment?",
            "Contact Dell Support or your account team with: array serial number, requested capacity increment, and current utilisation. Dell validates entitlement and activates within 1 business day for standard requests."),
        "warning": ("Array shows 'CoD capacity nearing maximum entitlement'. What does it mean?",
            "You are approaching the maximum pre-purchased CoD capacity. You must purchase additional CoD entitlement or plan for hardware expansion before the limit is reached. Contact your Dell account team immediately."),
        "perf": ("Adding CoD capacity did not improve performance — where do I start?",
            "CoD adds raw capacity, not additional back-end drives or controllers. If performance is the constraint (IOPS/throughput), you may need additional drive groups or a controller upgrade rather than CoD. Review CloudIQ performance metrics."),
        "backup_freq": ("Should I back up CoD licence keys?",
            "Yes — store CoD licence keys in a secure location (password manager or secrets vault). Dell can reissue keys if lost, but this may take 1-2 business days. Back up the array configuration which includes the licence record."),
        "restore": ("If I restore an array to a previous configuration, do I lose CoD capacity?",
            "The CoD licence is applied at the array level and persists through configuration restores. Capacity availability depends on the licence key being applied. Contact Dell Support if capacity appears missing after a restore."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/data-domain/operations", "dell-data-domain", "Dell Data Domain", {
        "version_check": ("What DD OS version is recommended for new Data Domain deployments?",
            "DD OS 7.13.x is the current recommendation. Check with `system show version` on the CLI. Always review the Dell Data Domain Compatibility Guide before upgrading."),
        "version_cmd": "system show version",
        "default_setting": ("What is the default deduplication scope and when should it change?",
            "Global deduplication across all MTrees is the default and recommended setting. Do not disable deduplication — it is the core value of Data Domain and cannot be meaningfully turned off for individual MTrees in production."),
        "enable_feature": ("How do I enable DD Replicator for off-site disaster recovery?",
            "Configure replication context: `replication add source mtree://<local-mtree> destination ddboost://<remote-dd>/mtree`. Verify connectivity and credentials. Monitor with `replication show all`. Ensure bandwidth throttle is configured for WAN links."),
        "rolling_upgrade": ("How do I upgrade DD OS without disrupting backup jobs?",
            "Download the upgrade package from Dell Support. Use `system upgrade` command. Non-disruptive upgrade (NDU) is supported on DD6xxx and above — backup jobs continue during most of the upgrade. Schedule during low-activity window for the reboot phase."),
        "add_resource": ("What is the correct procedure to add a new MTree for a new backup application?",
            "Create MTree: `mtree create /data/col1/newapp`. Set quota if needed: `mtree modify /data/col1/newapp quota-hard 10 TiB`. Configure DDBoost user or NFS/CIFS access for the backup application."),
        "warning": ("Data Domain shows 'ALERT: file system usage > 80%'. What does it mean?",
            "Usable space after deduplication is above 80%. Dedup ratio may be declining (more unique data arriving). Review backup retention policies. Clean up expired data: `filesys clean start`. Consider capacity expansion or tiering to DD Cloud Tier."),
        "perf": ("Backup throughput to Data Domain is lower than expected — where do I start?",
            "Check `performance show` for per-interface throughput. Verify DDBoost is enabled (provides 50%+ throughput improvement over NFS). Check network bandwidth. Review `disk show performance` for backend disk I/O."),
        "backup_freq": ("How often should I back up the Data Domain configuration?",
            "Weekly: `config backup <remote-path>`. Includes system configuration, network settings, and MTree configuration. Store off-appliance. Data Domain does not back up its own deduplicated data — that is your backup application's responsibility."),
        "restore": ("Can I recover individual files from a Data Domain MTree?",
            "Data Domain is a backup target, not a source for file-level restore. Restore files through the backup application (Veeam, NetBackup, Commvault) that wrote to the MTree. Data Domain does not provide file-level access to backup data directly."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/dell-aiops/operations", "dell-aiops", "Dell AIOps", {
        "version_check": ("How do I check the Dell AIOps platform version?",
            "Dell AIOps is delivered as a SaaS or integrated component of CloudIQ. Check the version in the AIOps UI → Help → About, or in the CloudIQ platform release notes."),
        "version_cmd": "Dell AIOps UI → Help → About",
        "default_setting": ("What is the default anomaly detection sensitivity?",
            "Medium sensitivity is the default — balances alert volume with detection coverage. Increase to High for critical arrays where even minor anomalies warrant investigation. Reduce for stable, predictable environments to reduce noise."),
        "enable_feature": ("How do I enable predictive failure alerts in Dell AIOps?",
            "Ensure SupportAssist is active on all monitored systems. In AIOps/CloudIQ, enable Predictive Recommendations under Settings → Analytics. Dell's ML models analyse telemetry and generate predictions based on fleet-wide failure patterns."),
        "rolling_upgrade": ("How does Dell AIOps update its ML models?",
            "Dell updates AIOps ML models automatically as a SaaS service. New model versions are trained on aggregated (anonymised) fleet telemetry. No customer action required. Prediction accuracy improves over time as more data is collected."),
        "add_resource": ("What is the correct procedure to add a new system to AIOps monitoring?",
            "Register the system with SupportAssist. AIOps automatically discovers newly connected systems within 24 hours. Configure alert recipients for the new system under AIOps Settings → Notifications."),
        "warning": ("AIOps shows 'Predicted Failure: Drive X within 14 days'. What does it mean?",
            "AIOps ML models have detected patterns consistent with imminent drive failure based on SMART data and error patterns. Contact Dell Support immediately to arrange a preventive drive replacement before data loss or performance impact occurs."),
        "perf": ("AIOps recommendations are generating too many low-priority alerts — where do I start?",
            "Tune alert thresholds in AIOps Settings → Alert Configuration. Suppress known-benign recommendations using the 'Acknowledge' workflow. Review suppressed alerts monthly to ensure no real issues are being masked."),
        "backup_freq": ("Is AIOps data backed up?",
            "AIOps is a SaaS platform — Dell manages all data retention and backup. Historical telemetry, model outputs, and alert history are retained per Dell's SaaS data retention policy. No customer backup action required."),
        "restore": ("What happens to AIOps data if I replace an array?",
            "AIOps historical data is linked to the system serial number. After replacement, the new array builds its own telemetry history. Dell Support can link the new serial to the old data for continuity if needed."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/ecs/operations", "dell-ecs", "Dell ECS (Elastic Cloud Storage)", {
        "version_check": ("What ECS version is recommended for new deployments?",
            "ECS 3.8.x is the current recommendation. Check with `ecs version` CLI or via ECS Management Portal → System → Software Version."),
        "version_cmd": "ecs version",
        "default_setting": ("What is the default replication factor for ECS object storage?",
            "ECS uses erasure coding rather than replication. Default is EC 12+4 for large objects, 2+1 replication for small objects (< 1 MB). Increase parity shards for higher durability requirements; this increases raw storage overhead."),
        "enable_feature": ("How do I enable S3 versioning on an ECS bucket?",
            "Use the S3 API or ECS Management Portal: Bucket → Properties → Versioning → Enable. Versioning allows recovery of overwritten or deleted objects. Note: versioned objects consume additional capacity."),
        "rolling_upgrade": ("How do I upgrade ECS without disrupting object storage access?",
            "ECS supports rolling upgrades — nodes upgrade one at a time. Use the ECS Management Portal → Upgrade to initiate. Data access continues throughout. Schedule during low-activity periods for reduced client impact."),
        "add_resource": ("What is the correct procedure to add a new ECS node to an existing site?",
            "Add the node hardware, configure networking and hostname. In ECS Management Portal → Nodes → Add Node. ECS rebalances data across the expanded node count automatically. Rebalancing can take hours for large clusters."),
        "warning": ("ECS shows 'Storage Pool capacity > 80%'. What does it mean?",
            "The storage pool is nearing full. ECS performance degrades above 85% utilisation. Plan capacity expansion immediately. Review bucket quotas and lifecycle policies to reduce unnecessary data retention."),
        "perf": ("ECS object PUT/GET performance is degraded — where do I start?",
            "Check ECS Management Portal → Performance for per-node metrics. Review network bandwidth. Check for rebalancing activity (reduces available IOPS during rebalance). Verify client-side connection pooling is configured."),
        "backup_freq": ("How do I protect ECS metadata?",
            "ECS metadata is replicated across nodes within the cluster. For disaster recovery, configure geo-replication to a second ECS site. Back up ECS system configuration weekly via Management Portal → System → Export Configuration."),
        "restore": ("Can I restore a specific object version in ECS?",
            "Yes — with versioning enabled, use the S3 API: `aws s3api get-object --bucket <name> --key <key> --version-id <vid> output.file`. In ECS Management Portal, browse bucket versions and restore via UI."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/fod/operations", "dell-fod", "Dell Features on Demand", {
        "version_check": ("How do I check which FoD licences are active on a Dell array?",
            "For PowerStore: PowerStore Manager → Settings → Licences. For Unity: Unisphere for Unity → System → Licences. For PowerMax: Unisphere → System → Licences. Active FoD features are listed with their entitlement status."),
        "version_cmd": "Unisphere → System → Licences → Features on Demand",
        "default_setting": ("What features are included in the base array licence vs FoD?",
            "Base licences include core block/file functionality. FoD unlocks advanced features: synchronous replication, data reduction, cloud tiering, and analytics. Review the Dell FoD catalogue for your specific array model."),
        "enable_feature": ("How do I activate a new FoD feature licence?",
            "Obtain the licence key from Dell (via Support portal or account team). Apply in the array management UI: System → Licences → Apply Key. Most features activate immediately without downtime."),
        "rolling_upgrade": ("How do I plan a FoD feature rollout across multiple arrays?",
            "Activate on a test array first. Validate the feature works as expected. Roll out to production arrays one at a time. For replication features, activate on both source and target arrays before configuring replication."),
        "add_resource": ("What is the correct procedure to request a new FoD trial licence?",
            "Contact Dell Support or your account team. Specify the array serial number and the feature to trial. Dell provides a 90-day trial key. Permanent licensing requires a purchase order."),
        "warning": ("Array shows 'FoD Licence Expiring in 30 Days'. What does it mean?",
            "A trial or term licence for a feature is expiring. If you are using the feature in production, contact Dell immediately to purchase a permanent licence. The feature will be disabled when the licence expires."),
        "perf": ("Activating a FoD feature caused unexpected performance impact — where do I start?",
            "Some FoD features (deduplication, compression, encryption) have CPU overhead. Review CloudIQ performance metrics. Contact Dell Support if the impact exceeds expected levels for your configuration."),
        "backup_freq": ("Should I back up FoD licence keys?",
            "Yes — store all FoD licence keys in a secure credential store. Dell can reissue keys but this takes 1-2 business days. Document the array serial number and associated FoD features in your CMDB."),
        "restore": ("If I rebuild an array, are FoD licences automatically re-applied?",
            "No — you must re-apply FoD licence keys after a factory reset or rebuild. Ensure keys are stored securely and retrievable before initiating any destructive operation on the array."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/powermax/operations", "dell-powermax", "Dell PowerMax", {
        "version_check": ("What PowerMaxOS version is recommended?",
            "PowerMaxOS 10.1.x (5978.x) is the current recommendation for PowerMax 2500/8500. Check via Unisphere: System → System Overview → Microcode Version."),
        "version_cmd": "Unisphere → System → System Overview → Microcode Version",
        "default_setting": ("What is the default Service Level Objective (SLO) for new storage groups?",
            "Diamond SLO is the default for PowerMax — targets <1ms response time. Use lower SLOs (Platinum, Gold) only for workloads with relaxed latency requirements to avoid over-provisioning NVMe cache."),
        "enable_feature": ("How do I enable SRDF/A (asynchronous replication) on PowerMax?",
            "Create SRDF/A group via Unisphere: Storage → SRDF → Create SRDF Group, select Asynchronous mode. Assign storage groups. Configure cycle time (minimum 30 seconds). Requires SRDF FoD licence on both arrays."),
        "rolling_upgrade": ("How do I upgrade PowerMaxOS without disrupting production workloads?",
            "PowerMaxOS upgrades are non-disruptive (NDU). Use Unisphere: System → Upgrade. The upgrade rolls across directors sequentially. No host-side changes required. Schedule during low-activity window for reduced risk."),
        "add_resource": ("What is the correct procedure to provision a new LUN on PowerMax?",
            "Create storage group, add volumes, add host/initiator group, create masking view. Via Unisphere or SYMCLI: `symconfigure -sid <sid> -cmd 'create dev count=1, size=100 GB, emulation=FBA, config=TDEV;' commit`. Verify with `symdev list -sid <sid>`."),
        "warning": ("PowerMax shows 'Alert: SLO Compliance < 95%'. What does it mean?",
            "Workloads are not meeting their target SLO. Check CloudIQ for hot volumes. Review if workload has grown beyond what the SLO tier can serve. Promote volumes to a higher SLO or rebalance across storage groups."),
        "perf": ("PowerMax latency increased after a workload migration — where do I start?",
            "Check Unisphere Performance tab for the affected storage group. Review front-end port utilisation. Verify SLO is correctly assigned. Check cache hit ratio — low cache hits indicate working set exceeds NVMe cache. Contact Dell if performance is unexpected."),
        "backup_freq": ("How often should I back up PowerMax configuration?",
            "Weekly SYMCLI configuration export: `symconfigure -sid <sid> -f config_backup.txt list`. Also enable Unisphere scheduled config backup under System → Backup Configuration. Store off-array."),
        "restore": ("Can I restore a single storage group's masking view without a full config restore?",
            "Yes — recreate the masking view via Unisphere or SYMCLI using the backed-up configuration. Masking view components (storage group, host group, port group) are independent objects and can be recreated individually."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/powerpath/operations", "dell-powerpath", "Dell PowerPath", {
        "version_check": ("What PowerPath version is recommended?",
            "PowerPath 6.4.x for Windows, 6.2.x for Linux are current. Check with `powermt version` on the host. Always align PowerPath version with the array support matrix."),
        "version_cmd": "powermt version",
        "default_setting": ("What is the default load balancing policy and when should it change?",
            "Adaptive load balancing (`adap`) is the default for PowerMax and VMAX arrays. For all-active arrays (PowerStore, Unity), use `round-robin` or `least-queue-depth`. Check with `powermt display dev=all`."),
        "enable_feature": ("How do I enable PowerPath pseudo device persistence after host reboot?",
            "PowerPath pseudo device names persist by default if properly configured. Verify `powermt save` is called after any configuration change. On Linux, ensure `powervt` daemon is enabled: `systemctl enable powermt`."),
        "rolling_upgrade": ("How do I upgrade PowerPath on a host with active I/O?",
            "PowerPath upgrades require host downtime or migration of workloads. For VMware: use PowerPath/VE, which supports online upgrades. For bare-metal, schedule a maintenance window, stop I/O, upgrade, reboot, verify paths with `powermt display dev=all`."),
        "add_resource": ("What is the correct procedure to add a new storage path to PowerPath?",
            "Zone the new path in the SAN fabric. Rescan the HBA: `echo '- - -' > /sys/class/scsi_host/hostX/scan`. Run `powermt config` to detect new paths. Verify with `powermt display dev=all`. Save config: `powermt save`."),
        "warning": ("PowerPath shows 'path degraded' for a device. What does it mean?",
            "One or more paths to a LUN are unavailable. I/O continues on remaining paths. Check the HBA, SAN zoning, and storage port. Run `powermt display dev=<dev>` for path details. Resolve the path failure before another path goes down."),
        "perf": ("I/O throughput is unevenly distributed across paths — where do I start?",
            "Check `powermt display dev=all` for per-path I/O statistics. If load is uneven, verify the load balancing policy is set correctly for your array type. For persistent path preference, switch to `rr` (round-robin) policy."),
        "backup_freq": ("How often should I back up PowerPath configuration?",
            "Run `powermt save` after every configuration change. The saved config file (`/etc/powermt.custom` on Linux) should be included in host configuration backup. Back up before any PowerPath upgrade."),
        "restore": ("Can I restore PowerPath configuration after a host rebuild?",
            "Yes — install PowerPath, copy `/etc/powermt.custom` from backup, then run `powermt restore`. This restores device aliases and policy settings. Verify paths with `powermt display dev=all` after restore."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/powerscale/operations", "dell-powerscale", "Dell PowerScale (Isilon)", {
        "version_check": ("What OneFS version is recommended for new deployments?",
            "OneFS 9.7.x is the current recommendation. Check with `isi version` on a node CLI or Isilon Management Interface (IMI) → Help → About."),
        "version_cmd": "isi version",
        "default_setting": ("What is the default protection level and when should it change?",
            "Default protection is +2d:1n (survive 2 drive failures or 1 node failure). Increase to +3d:1n1d or +2n for mission-critical data. Review with `isi storagepool list`."),
        "enable_feature": ("How do I enable SmartQuotas for per-directory capacity limits?",
            "Enable the SmartQuotas licence and module. Create a quota: `isi quota quotas create /ifs/data/dept type=directory hard-threshold=1T`. Monitor with `isi quota quotas list`."),
        "rolling_upgrade": ("How do I upgrade OneFS without disrupting NFS/SMB clients?",
            "OneFS rolling upgrades are supported: `isi upgrade cluster start --release <ver>`. Nodes upgrade one at a time; clients reconnect automatically. Verify cluster health before each node upgrade with `isi status`."),
        "add_resource": ("What is the correct procedure to add a new node to a PowerScale cluster?",
            "Rack and cable the node, power on, join via the join wizard or `isi devices node add`. OneFS rebalances data across the expanded cluster automatically. Monitor with `isi rebalance status`."),
        "warning": ("PowerScale shows 'Node is in a degraded state'. What does it mean?",
            "A drive or network component in the node is failed or degraded. Check `isi status` for details. If a drive has failed, OneFS automatically reprotects data. If network is degraded, check InfiniBand/Ethernet back-end connections."),
        "perf": ("NFS throughput is below expectations — where do I start?",
            "Check `isi statistics client` for per-client throughput. Verify NIC bonding and MTU (jumbo frames recommended). Review SmartPools tiering — data may have migrated to slower HDD tiers. Check for heavy metadata operations with `isi statistics system`."),
        "backup_freq": ("How often should I back up PowerScale configuration?",
            "Weekly configuration backup via `isi_gather_info --upload`. For DR, configure SyncIQ replication to a second cluster. Test SyncIQ failover quarterly."),
        "restore": ("Can I restore a single directory from a SyncIQ replica?",
            "Yes — with SyncIQ, perform a selective recovery: `isi sync policies edit --target-compare-initial-sync true`. For SnapshotIQ, restore a directory: `isi snapshot restore <snapshot> /ifs/data/dir`."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/powerstore/operations", "dell-powerstore", "Dell PowerStore", {
        "version_check": ("What PowerStore OS version is recommended?",
            "PowerStore OS 3.5.x is the current recommendation. Check in PowerStore Manager: Settings → Software → Installed Software Version."),
        "version_cmd": "PowerStore Manager → Settings → Software → Installed Version",
        "default_setting": ("What is the default storage policy and when should it change?",
            "PowerStore uses a flat storage pool — no tiering policy to set. Inline deduplication and compression are enabled by default. Disable only for workloads with already-compressed data (e.g., encrypted backups, video)."),
        "enable_feature": ("How do I enable PowerStore Metro Volume for zero-RPO synchronous replication?",
            "Configure Metro Volume via PowerStore Manager: Protection → Replication → Add Metro Rule. Assign to volumes. Requires two PowerStore arrays at <5ms RTT. Requires Metro licence on both arrays."),
        "rolling_upgrade": ("How do I upgrade PowerStore OS without downtime?",
            "Upgrades are non-disruptive on PowerStore appliances. Initiate via PowerStore Manager → Settings → Software → Upgrade. The upgrade is applied node-by-node with automatic I/O failover. Schedule during low-activity period."),
        "add_resource": ("What is the correct procedure to provision a new volume on PowerStore?",
            "PowerStore Manager → Storage → Volumes → Create. Set name, size, host mapping, and performance policy. For VMware, use the vSphere plugin for automated VMFS datastore creation."),
        "warning": ("PowerStore shows 'Appliance node is in service mode'. What does it mean?",
            "One node of the PowerStore appliance has failed over. I/O continues on the surviving node. Contact Dell Support immediately — this is a degraded state. Do not reboot the appliance without Dell guidance."),
        "perf": ("PowerStore latency spiked — where do I start?",
            "Check PowerStore Manager → Performance for per-volume and per-appliance metrics. Review front-end port utilisation. Check dedup/compression saving ratio — low ratios may indicate working set exceeds NVMe capacity."),
        "backup_freq": ("How often should I back up PowerStore configuration?",
            "Weekly via PowerStore Manager → Settings → System → Export Configuration. Include in off-site backup. Also configure Protection Policies with snapshots for data recovery."),
        "restore": ("Can I recover a deleted volume's snapshot on PowerStore?",
            "Yes — snapshots persist independently of volume deletion if the snapshot is not manually deleted. In PowerStore Manager → Storage → Snapshots, locate the snapshot and restore or create a new volume from it."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/recoverpoint/operations", "dell-recoverpoint", "Dell RecoverPoint", {
        "version_check": ("What RecoverPoint version is recommended?",
            "RecoverPoint 5.3.x is the current recommendation. Check via RecoverPoint Management Application (RPMA) → System → About."),
        "version_cmd": "RPMA → System → About",
        "default_setting": ("What is the default journal size and when should it change?",
            "Default journal size is 10% of protected volume size. Increase for longer RPO windows or high-change-rate workloads. Under-sized journals cause journal overflow, which forces a full sweep (similar to a full resync)."),
        "enable_feature": ("How do I enable bookmark-based recovery in RecoverPoint?",
            "Create a bookmark via RPMA: Consistency Group → Bookmarks → Add Bookmark. Bookmarks mark a specific point in time for recovery. Enable auto-bookmarks on a schedule for regular recovery points."),
        "rolling_upgrade": ("How do I upgrade RecoverPoint Appliances without disrupting replication?",
            "RecoverPoint upgrades are non-disruptive for most versions. Use RPMA → System → Upgrade. Splitters continue to protect volumes during upgrade. Test failback after upgrade. Schedule during low I/O periods."),
        "add_resource": ("What is the correct procedure to add a new volume to an existing consistency group?",
            "In RPMA: select the Consistency Group → Volumes → Add Volume. Map source and replica volumes. RecoverPoint begins initial copy (sweep). Monitor sweep progress via RPMA → Consistency Groups → Policies."),
        "warning": ("RecoverPoint shows 'Journal overflow'. What does it mean?",
            "The journal volume is full — incoming writes exceed journal capacity faster than they can be applied to the replica. Increase journal size, reduce protected volume write rate, or reduce RPO target. Overflow forces a full resync."),
        "perf": ("Replication lag is increasing — where do I start?",
            "Check WAN bandwidth between RPA clusters. Review journal utilisation. Check RPA CPU and memory. Reduce replication traffic with compression (enabled by default). Throttle non-critical CGs during peak hours."),
        "backup_freq": ("How often should I back up RecoverPoint configuration?",
            "Weekly via RPMA → System → Export Configuration. Back up before any upgrade. Include RPA network configuration in your runbook. Configuration restore requires matching software version."),
        "restore": ("Can I perform a partial failover for a single volume in a consistency group?",
            "RecoverPoint fails over consistency groups as a unit to maintain write-order fidelity. To fail over a single volume, it must be in its own consistency group. Review CG design before incident — splitting CGs later requires a full resync."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/secure-connect-gateway/operations", "dell-scg", "Dell Secure Connect Gateway", {
        "version_check": ("What Secure Connect Gateway version is recommended?",
            "SCG 5.24.x is the current recommendation. Check via SCG web interface → Administration → About. SCG replaces the legacy SupportAssist Enterprise and EMC Secure Remote Services (ESRS)."),
        "version_cmd": "SCG UI → Administration → About",
        "default_setting": ("What is the default connectivity mode for SCG?",
            "Direct connectivity to Dell (HTTPS outbound, port 443) is the default. Configure proxy if required: SCG → Network → Proxy Settings. Use access list to control which devices connect through SCG."),
        "enable_feature": ("How do I enable remote diagnostics collection for a new Dell array via SCG?",
            "Register the array in SCG: Devices → Add Device. Provide the array management IP and credentials. SCG establishes connectivity and begins collecting telemetry for CloudIQ and SupportAssist."),
        "rolling_upgrade": ("How do I upgrade SCG without interrupting device monitoring?",
            "Download SCG update from dell.com/support. Apply via SCG → Administration → Update. SCG restarts during upgrade (5-10 minutes). Device connections resume automatically after restart. Monitor reconnection in SCG → Devices."),
        "add_resource": ("What is the correct procedure to add a new server to SCG?",
            "Install the iDRAC Service Module (iSM) or SupportAssist agent on the server. In SCG, go to Devices → Add Device → Server. Provide iDRAC or agent credentials. Verify telemetry appears in CloudIQ within 24 hours."),
        "warning": ("SCG shows 'Device Not Responding'. What does it mean?",
            "SCG cannot collect telemetry from the device. Check device management IP reachability from the SCG server. Verify credentials have not expired. Check firewall rules between SCG and the device management network."),
        "perf": ("SCG is slow to respond to the UI — where do I start?",
            "Check SCG server resources (CPU, memory, disk). SCG is Java-based — increase JVM heap if under-allocated. Review the number of registered devices — very large deployments may need a second SCG instance."),
        "backup_freq": ("How often should I back up SCG configuration?",
            "Weekly via SCG → Administration → Backup. Backup includes all device registrations and settings. Store off-SCG. Restore requires matching SCG version."),
        "restore": ("Can I restore SCG device registrations after a server failure?",
            "Yes — restore from the SCG backup file via the SCG installer's restore mode. Device registrations, credentials, and network settings are all restored. Re-verify device connectivity after restore."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/srdf-a/operations", "dell-srdf-a", "Dell SRDF/A (Asynchronous Replication)", {
        "version_check": ("How do I check the SRDF/A replication status on PowerMax?",
            "Via Unisphere: Storage → SRDF → SRDF Groups. Check pair state (Synchronized, SyncInProg, Suspended). Via SYMCLI: `symrdf -g <rdf_group> query`. Current lag is shown as RPO in seconds."),
        "version_cmd": "symrdf -g <rdf_group> query",
        "default_setting": ("What is the default SRDF/A cycle time and when should it change?",
            "Default cycle time is 30 seconds (minimum). Increase to 60-300 seconds for WAN links with limited bandwidth — longer cycles allow more compression before transmission. Shorter cycles reduce RPO but increase bandwidth consumption."),
        "enable_feature": ("How do I enable SRDF/A STAR (Three-Site Replication)?",
            "Configure a three-hop SRDF group (SRDF/S from site A to site B, SRDF/A from site B to site C). Requires SRDF STAR licence. Configure via Unisphere or SYMCLI. All three arrays must be registered in Unisphere."),
        "rolling_upgrade": ("How do I suspend and resume SRDF/A replication during array maintenance?",
            "Suspend: `symrdf -g <rdf_group> suspend`. Perform maintenance. Resume: `symrdf -g <rdf_group> resume`. During suspension, the journal accumulates changes. Monitor journal capacity — if full during suspend, a full copy is needed on resume."),
        "add_resource": ("What is the correct procedure to add a new volume to an existing SRDF/A group?",
            "Add volume to the storage group. In SYMCLI: `symrdf -g <rdf_group> addpair -dev <devid> -rdfg <rdf_group> -type async`. Initial copy begins automatically. Monitor with `symrdf -g <rdf_group> query`."),
        "warning": ("SRDF/A shows 'R2 out of sync'. What does it mean?",
            "The replica (R2) is not receiving updates from the source (R1). Check WAN connectivity and SRDF port health with `symrdf -g <rdf_group> verify`. If the link is restored, SRDF/A will automatically re-sync within the journal window."),
        "perf": ("SRDF/A RPO is consistently above target — where do I start?",
            "Check WAN bandwidth utilisation. Enable SRDF/A compression if not already enabled. Increase cycle time to reduce overhead. Review which volumes are generating the most delta using `symrdf -g <rdf_group> list -v`."),
        "backup_freq": ("How often should I back up SRDF/A configuration?",
            "Weekly SYMCLI export of RDF group configuration. Back up before any microcode upgrade or RDF group modification. Configuration restore requires both source and target arrays to be available."),
        "restore": ("Can I perform a partial failover of selected volumes in an SRDF/A group?",
            "Yes — use consistent failover per device: `symrdf -g <rdf_group> -dev <devlist> failover`. However, for transactionally consistent recovery, fail over the entire consistency group rather than individual volumes."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/srdf-s/operations", "dell-srdf-s", "Dell SRDF/S (Synchronous Replication)", {
        "version_check": ("How do I verify SRDF/S replication is synchronised?",
            "Via Unisphere: Storage → SRDF → SRDF Groups → check pair state is 'Synchronized'. Via SYMCLI: `symrdf -g <rdf_group> query` — R1 and R2 should show '==' (synchronized). Any other state indicates a problem."),
        "version_cmd": "symrdf -g <rdf_group> query",
        "default_setting": ("What is the maximum recommended RTT for SRDF/S and when should SRDF/A be used instead?",
            "SRDF/S requires RTT < 10ms for acceptable host I/O latency (every write waits for R2 acknowledgement). For RTT > 10ms, use SRDF/A (asynchronous) instead. Use `ping -c 100 <R2-ip>` to measure RTT."),
        "enable_feature": ("How do I enable SRDF/S Adaptive Copy mode for planned maintenance?",
            "Switch to Adaptive Copy: `symrdf -g <rdf_group> set mode adaptivecopy`. This allows R2 to fall slightly behind R1 during heavy write activity. Switch back to Synchronous: `symrdf -g <rdf_group> set mode sync` when complete."),
        "rolling_upgrade": ("How do I suspend SRDF/S for array maintenance without data loss?",
            "Switch to SRDF/A mode temporarily: `symrdf -g <rdf_group> set mode async`. Perform maintenance. Switch back: `symrdf -g <rdf_group> set mode sync`. Verify synchronisation before switching back."),
        "add_resource": ("What is the correct procedure to add new volumes to an SRDF/S group?",
            "Create the R2 device on the target array. Add pair to the RDF group: `symrdf -g <rdf_group> addpair -dev <devid> -rdfg <rdf_group> -type sync`. Monitor initial copy with `symrdf -g <rdf_group> query`."),
        "warning": ("SRDF/S shows 'R2 Not Ready'. What does it mean?",
            "The R2 volume is not accepting host I/O (expected in normal operation — R2 is write-protected). If this appears during a failover scenario, run `symrdf -g <rdf_group> failover` to make R2 read/write. Do not force-write to R2 without failing over."),
        "perf": ("SRDF/S is adding significant write latency — where do I start?",
            "Measure RTT to the R2 array (`ping`). SRDF/S adds approximately 2x RTT to every write. If RTT is >5ms, consider switching to SRDF/A. Check RDF port utilisation — congested ports increase latency. Review WAN QoS configuration."),
        "backup_freq": ("How often should I back up SRDF/S RDF group configuration?",
            "Weekly SYMCLI export. The R2 array itself serves as a synchronous copy — it is both the DR target and effectively a real-time backup for recent changes. Supplement with application-consistent snapshots on R2."),
        "restore": ("How do I perform a planned failover to the SRDF/S replica site?",
            "1) Quiesce applications. 2) `symrdf -g <rdf_group> failover`. 3) Mount R2 volumes on target hosts. 4) Start applications on target site. For failback: `symrdf -g <rdf_group> failback` after re-synchronisation."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/unity/operations", "dell-unity", "Dell Unity", {
        "version_check": ("What Unity OS version is recommended?",
            "Unity OS 5.4.x is the current recommendation. Check via Unisphere for Unity: System → Software. Apply the latest OE (Operating Environment) patch before any production deployment."),
        "version_cmd": "Unisphere for Unity → System → Software",
        "default_setting": ("What is the default snapshot schedule and when should it change?",
            "No default snapshot schedule is configured. Create protection schedules under Protection → Snapshots → Schedule. Minimum recommended: hourly snapshots retained for 24 hours, daily for 7 days, weekly for 4 weeks."),
        "enable_feature": ("How do I enable Unity Metro Sync for synchronous replication?",
            "Requires two Unity arrays and a Metro Sync licence. Configure via Unisphere: Protection → Replication → Add Replication Session. Select Synchronous mode. Ensure RTT < 5ms between arrays for acceptable performance."),
        "rolling_upgrade": ("How do I upgrade Unity OS without downtime?",
            "Unity supports non-disruptive upgrades (NDU). Via Unisphere: System → Software → Upgrade. Storage processors upgrade sequentially; I/O fails over to the peer SP during each SP's upgrade. Typically completes in 30-60 minutes."),
        "add_resource": ("What is the correct procedure to provision a new LUN on Unity?",
            "Unisphere: Storage → Block → LUNs → Create LUN. Set name, pool, size, and host access. For thin provisioning, select 'Thin' and set the size limit. Assign the LUN to a host via the Access tab."),
        "warning": ("Unity shows 'Storage Pool nearly full'. What does it mean?",
            "Usable pool capacity is above 85%. Thin-provisioned LUNs may fail writes if the pool reaches 100%. Add drives to the pool (Unisphere: Storage → Pools → Add Capacity) or delete unnecessary data/snapshots."),
        "perf": ("Unity I/O latency increased — where do I start?",
            "Check Unisphere Performance tab for per-LUN and per-pool metrics. Review cache utilisation (SSD cache should be >50% hit rate). Check for heavy snapshot operations. Review host queue depth settings."),
        "backup_freq": ("How often should I back up Unity configuration?",
            "Weekly via Unisphere: System → Service → Export Configuration. Back up before any OE upgrade or configuration change. Store off-array."),
        "restore": ("Can I restore a single LUN from a Unity snapshot?",
            "Yes — Unisphere: Protection → Snapshots → select snapshot → Restore (restores in-place) or Create LUN from Snapshot (creates a new LUN from the snapshot). Restoring in-place overwrites current data."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/dell/vplex/operations", "dell-vplex", "Dell VPLEX", {
        "version_check": ("What VPLEX OS version is recommended?",
            "VPLEX GeoSynchrony 6.2.x is the current recommendation. Check via Management Console: System → About VPLEX."),
        "version_cmd": "Management Console → System → About VPLEX",
        "default_setting": ("What is the default cache mode for VPLEX volumes?",
            "Write-back cache is the default for optimal performance. Write-through mode is available for compliance environments where data must be committed to back-end storage before acknowledgement. Configure per virtual volume."),
        "enable_feature": ("How do I enable VPLEX Metro for active-active stretched clustering?",
            "Configure a VPLEX Metro cluster with two VPLEX clusters connected via synchronous WAN link (<10ms RTT). Create distributed devices and distributed virtual volumes. Requires VPLEX Metro licence. Zoning is required on both fabrics."),
        "rolling_upgrade": ("How do I upgrade VPLEX OS without disrupting host I/O?",
            "VPLEX NDU upgrades directors one at a time. I/O fails over to remaining directors during each director's upgrade. Use Management Console → System → Software → Upgrade. Schedule during low-activity window."),
        "add_resource": ("What is the correct procedure to add a new back-end storage volume to VPLEX?",
            "Zone the new back-end LUN to the VPLEX initiators. Run discovery: `management-server/devices> ll` to see new storage views. Create a storage volume in VPLEX and build an extent, device, and virtual volume on top of it."),
        "warning": ("VPLEX shows 'Director communication loss'. What does it mean?",
            "Two VPLEX directors cannot communicate — potential split-brain risk in Metro configurations. Check inter-director network. If one director is truly offline, ensure the surviving director has quorum before allowing host writes. Contact Dell Support immediately."),
        "perf": ("VPLEX cache hit rate is low — where do I start?",
            "Check Management Console Performance tab for cache statistics. Low hit rate indicates working set exceeds VPLEX cache. Review which virtual volumes have the most misses. Consider adding VPLEX cache expansion if available for your model."),
        "backup_freq": ("How often should I back up VPLEX configuration?",
            "Weekly: `management-server> configuration backup create`. Store off-VPLEX. Back up before any upgrade or major configuration change. VPLEX configuration backup includes all virtual volume definitions and cluster settings."),
        "restore": ("Can I recover a corrupted VPLEX distributed device without data loss?",
            "Contact Dell Support immediately for distributed device issues — recovery requires expert guidance. For Metro configurations, ensure the surviving site has consistent data before any recovery attempt. Do not force-rebuild without Dell guidance."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    # NetApp
    ("storage/netapp/insightiq/operations", "netapp-insightiq", "NetApp InsightIQ", {
        "version_check": ("What InsightIQ version is recommended?",
            "InsightIQ 4.2.x is the latest release. Check via InsightIQ UI → Administration → About. Note: InsightIQ is specific to NetApp PowerScale (Isilon) performance monitoring."),
        "version_cmd": "InsightIQ UI → Administration → About",
        "default_setting": ("What is the default data collection interval?",
            "InsightIQ collects performance data every 30 seconds by default. Reduce to 10 seconds for high-resolution troubleshooting (increases database growth). Increase to 60 seconds for capacity planning at scale."),
        "enable_feature": ("How do I enable InsightIQ dashboards for NFS client analytics?",
            "In InsightIQ, go to Analytics → Client Analytics → enable NFS client tracking. This requires OneFS 8.1+ on the cluster. Client-level analytics show per-client throughput and latency breakdown."),
        "rolling_upgrade": ("How do I upgrade InsightIQ without losing historical data?",
            "InsightIQ stores data in a local PostgreSQL database. Back up before upgrade: `pg_dump insightiq > insightiq_backup.sql`. Apply the upgrade package. Verify data continuity in dashboards post-upgrade."),
        "add_resource": ("What is the correct procedure to add a new PowerScale cluster to InsightIQ?",
            "In InsightIQ: Clusters → Add Cluster. Provide the cluster management IP and credentials (read-only API user recommended). InsightIQ begins collecting data within 5 minutes."),
        "warning": ("InsightIQ shows 'Data collection paused for cluster X'. What does it mean?",
            "InsightIQ cannot reach the cluster API. Check network connectivity, API credentials, and OneFS version compatibility. If InsightIQ misses more than 24 hours of data, historical trend charts will show a gap."),
        "perf": ("InsightIQ UI is slow to load dashboard data — where do I start?",
            "Check InsightIQ server disk and memory. The PostgreSQL database grows continuously — consider purging data older than 90 days: InsightIQ → Administration → Data Retention. Reduce the number of open dashboards."),
        "backup_freq": ("How often should I back up InsightIQ data?",
            "Weekly PostgreSQL dump. InsightIQ data is performance telemetry — not business-critical, but useful for trending. The InsightIQ configuration (cluster list, dashboard definitions) is more important to back up."),
        "restore": ("Can I restore a specific time range of missing performance data?",
            "No — InsightIQ can only display data it has collected. Gaps caused by collection outages cannot be retroactively filled. Use the PowerScale native `isi statistics` CLI for recent data if InsightIQ has a gap."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/netapp/keystone/operations", "netapp-keystone", "NetApp Keystone", {
        "version_check": ("How do I check my Keystone subscription status and committed capacity?",
            "Log in to NetApp BlueXP (console.bluexp.netapp.com) → Keystone → Subscriptions. View committed capacity, consumed capacity, and burst usage by service level."),
        "version_cmd": "BlueXP → Keystone → Subscriptions → View Details",
        "default_setting": ("What is the default burst tolerance for Keystone subscriptions?",
            "Keystone allows burst up to 20% above committed capacity. Burst usage is billed at a higher rate. Monitor burst consumption in BlueXP → Keystone → Capacity Trend to avoid unexpected charges."),
        "enable_feature": ("How do I enable Keystone capacity reporting alerts?",
            "In BlueXP → Keystone → Alerts, configure capacity threshold notifications (e.g., alert at 80% of committed capacity). Alerts are sent via email. Set up early warnings to allow time for subscription adjustment."),
        "rolling_upgrade": ("How does Keystone handle service level upgrades mid-subscription?",
            "Contact NetApp to modify the subscription. Service level changes (e.g., Extreme to Premium) take effect at the next billing period. Capacity committed at the new level is immediately available after order processing."),
        "add_resource": ("What is the correct procedure to add capacity to a Keystone subscription?",
            "Submit a request via BlueXP → Keystone → Manage Subscription → Add Capacity, or contact your NetApp account team. Additional committed capacity is typically provisioned within 2 business days."),
        "warning": ("Keystone shows 'Burst threshold exceeded'. What does it mean?",
            "Consumed capacity exceeds the committed + 20% burst threshold. Additional burst may be denied or billed at overage rates per your contract. Review which workloads are consuming excess capacity and either expand the subscription or reduce consumption."),
        "perf": ("Keystone storage performance is below committed SLA — where do I start?",
            "Check BlueXP performance dashboards. If below contracted SLA, raise a support case with NetApp. Keystone SLAs are contractually backed — NetApp is obligated to investigate and remediate."),
        "backup_freq": ("How is Keystone data protected?",
            "Keystone includes built-in redundancy. Application-level backup (SnapCenter, Veeam) is the customer's responsibility. Review your Keystone contract for data protection responsibilities and included snapshot features."),
        "restore": ("Can I restore data from a Keystone snapshot?",
            "Yes — Keystone services include snapshot capabilities. Restore via the array management interface (ONTAP System Manager for Keystone ONTAP services) or via the backup application (SnapCenter)."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/netapp/ontap/operations", "netapp-ontap", "NetApp ONTAP", {
        "version_check": ("What ONTAP version is recommended for new deployments?",
            "ONTAP 9.14.1 or 9.15.1 (latest P-releases) are recommended. Check with `version` from ONTAP CLI or System Manager → Cluster → Software. Always apply the latest patch release."),
        "version_cmd": "version",
        "default_setting": ("What is the default volume guarantee and when should it change?",
            "Default is `volume` guarantee (thick provisioning). Switch to `none` (thin provisioning) to allow overcommitment: `volume modify -volume vol1 -space-guarantee none`. Monitor aggregate space carefully when thin provisioning."),
        "enable_feature": ("How do I enable ONTAP inline deduplication and compression?",
            "`volume efficiency on -volume vol1` enables inline dedup and compression. Verify: `volume efficiency show -volume vol1`. For AFF arrays, both are enabled by default. Expected savings: 2-5x for typical workloads."),
        "rolling_upgrade": ("How do I perform an ONTAP rolling upgrade without downtime?",
            "Use ONTAP automatic non-disruptive upgrade (ANDU): `system image update -package <url> -replace-package true`. ANDU upgrades nodes one at a time, taking over and giving back storage. Verify with `cluster image show`."),
        "add_resource": ("What is the correct procedure to create a new SVM and NFS export?",
            "`vserver create -vserver nfs_svm -rootvolume root -rootvolume-security-style unix`. Add data LIF. Create volume. Add export policy. Verify: `vserver show -vserver nfs_svm`. Test mount from a client."),
        "warning": ("ONTAP shows 'Aggregate is nearly full'. What does it mean?",
            "Aggregate space usage is above 90%. ONTAP restricts new volume creation and thin-provisioned writes above 98%. Add drives, move volumes to another aggregate, or delete snapshots to reclaim space immediately."),
        "perf": ("NFS/iSCSI latency increased — where do I start?",
            "Check `qos statistics performance show` for workload latency breakdown. Review `statistics show -object volume` for per-volume IOPS. Check aggregate disk busy % with `aggr show-space`. Review network with `network interface show`."),
        "backup_freq": ("How often should I back up ONTAP configuration?",
            "ONTAP automatically backs up configuration to all nodes. Manual export: `system configuration backup upload`. For disaster recovery, configure SnapMirror for data and MetroCluster for HA. Test failover quarterly."),
        "restore": ("Can I restore a single file from an ONTAP snapshot?",
            "Yes — access the `.snapshot` directory in any NFS mount (`ls /mnt/vol1/.snapshot`). Copy the file directly from the snapshot directory. For block (iSCSI/FC), use SnapRestore: `volume snapshot restore-file -volume vol -snapshot snap -path /file`."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/netapp/operations", "netapp", "NetApp", {
        "version_check": ("How do I determine which NetApp products are deployed and their versions?",
            "Use BlueXP (console.bluexp.netapp.com) → Inventory for a unified view. For ONTAP: `version` CLI. For StorageGRID: Grid Manager → Nodes → Software Version. For E-Series: SANtricity System Manager → About."),
        "version_cmd": "BlueXP → Inventory → Software Versions",
        "default_setting": ("What is the default AutoSupport configuration and when should it change?",
            "AutoSupport sends telemetry to NetApp and your support team. Default is HTTPS to NetApp. Enable email notifications for your team: `autosupport modify -mail-hosts <smtp> -to <team@company.com>`. Never disable AutoSupport in production."),
        "enable_feature": ("How do I enable BlueXP data tiering to object storage?",
            "In BlueXP → Tiering, connect your ONTAP cluster. Select the volumes to tier. Choose S3, Azure Blob, or StorageGRID as the target. BlueXP automatically moves cold data (configurable cooldown period) to object storage."),
        "rolling_upgrade": ("How do I plan a NetApp portfolio upgrade across multiple product generations?",
            "Upgrade ONTAP first (it provides the most compatibility guarantees). Then upgrade SnapCenter. Finally upgrade monitoring tools (InsightIQ, Active IQ). Review the NetApp Interoperability Matrix (IMT) before each upgrade."),
        "add_resource": ("What is the correct procedure to add a new NetApp system to BlueXP?",
            "BlueXP → Add Working Environment. Select NetApp ONTAP, E-Series, or StorageGRID. Provide management IP and credentials. BlueXP discovers the system and adds it to the dashboard within 5 minutes."),
        "warning": ("BlueXP shows 'System at Risk' for a cluster. What does it mean?",
            "NetApp Active IQ has identified a risk (hardware vulnerability, software bug, configuration issue). Click through to see the specific risk and recommended action. Address Critical risks within 30 days; High within 90 days."),
        "perf": ("NetApp Active IQ shows a performance risk — where do I start?",
            "Review the specific recommendation in Active IQ. Common causes: volume move needed, aggregate rebalancing, protocol contention. Follow the recommended action in the Active IQ advisory. Contact NetApp Support if unclear."),
        "backup_freq": ("How often should I audit NetApp configuration across the portfolio?",
            "Monthly review of Active IQ recommendations. Quarterly review of SnapMirror health and SnapCenter backup success rates. Annual review of licence compliance and support contract renewals."),
        "restore": ("Can I use NetApp BlueXP to initiate a disaster recovery failover?",
            "Yes — BlueXP DR (preview) supports policy-based DR failover for ONTAP. For production DR, use SnapCenter or manual SnapMirror break/resync procedures. Test DR failover quarterly in an isolated environment."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("storage/netapp/snapcenter/operations", "netapp-snapcenter", "NetApp SnapCenter", {
        "version_check": ("What SnapCenter version is recommended?",
            "SnapCenter 6.0.x is the current recommendation. Check via SnapCenter UI → Settings → Software. Keep SnapCenter within 1 major version of your ONTAP version for full compatibility."),
        "version_cmd": "SnapCenter UI → Settings → Software → Version",
        "default_setting": ("What is the default retention policy and when should it change?",
            "Default is 3 snapshots (hourly). Increase for critical workloads: hourly × 24, daily × 7, weekly × 4 is a common production baseline. Define retention policies per resource group to match recovery objectives."),
        "enable_feature": ("How do I enable SnapCenter application-consistent backups for SQL Server?",
            "Install the SnapCenter Plug-in for Microsoft SQL Server on the SQL hosts. In SnapCenter, add the SQL host under Hosts → Add. Create a resource group selecting the SQL databases. Enable VSS quiescing for application consistency."),
        "rolling_upgrade": ("How do I upgrade SnapCenter without disrupting scheduled backups?",
            "SnapCenter upgrades require a brief maintenance window (UI unavailable during upgrade). Scheduled jobs that trigger during upgrade will fail and retry. Upgrade the SnapCenter server first, then push plug-in updates to hosts."),
        "add_resource": ("What is the correct procedure to add a new host to SnapCenter?",
            "SnapCenter UI → Hosts → Add Host. Provide the hostname, OS type, and credentials. SnapCenter installs the appropriate plug-in automatically. Verify the host appears with a green status before creating resource groups."),
        "warning": ("SnapCenter job fails with 'Snapshot operation not allowed while volume move is in progress'. What does it mean?",
            "ONTAP is moving the volume to another aggregate. SnapCenter snapshot operations are blocked during volume move. Wait for the move to complete (`volume move show`) then retry the backup job."),
        "perf": ("SnapCenter backup jobs are slow — where do I start?",
            "Check ONTAP aggregate performance during backup windows. Review concurrent job count — reduce parallelism if ONTAP is saturated. For SQL, check VSS quiesce time. Enable SnapCenter logging for detailed timing analysis."),
        "backup_freq": ("How often should I back up SnapCenter configuration?",
            "Weekly via SnapCenter → Settings → Settings → Backup SnapCenter Server. Includes all policies, resource groups, and credentials. Store off-server. Test restore annually."),
        "restore": ("Can I restore a single file from a SnapCenter backup?",
            "Yes — SnapCenter supports file-level restore for Windows (via SnapCenter Plug-in for Windows), Oracle, and SQL. For VMware VMs, use SnapCenter Plug-in for VMware → File Restore → browse the mounted backup."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/netapp/snapmirror/operations", "netapp-snapmirror", "NetApp SnapMirror", {
        "version_check": ("How do I check SnapMirror relationship status across all volumes?",
            "`snapmirror show -fields state,lag-time,health` from ONTAP CLI. Use SnapCenter or BlueXP for a GUI view. All relationships should show `Snapmirrored` state with lag below the RPO target."),
        "version_cmd": "snapmirror show -fields state,lag-time,health",
        "default_setting": ("What is the default SnapMirror schedule and when should it change?",
            "No default schedule is set — you define the schedule per relationship. Typical baseline: hourly for critical volumes, daily for standard. For near-zero RPO, use SnapMirror Synchronous (SM-S)."),
        "enable_feature": ("How do I enable SnapMirror throttling to avoid WAN saturation?",
            "`snapmirror modify -destination-path <path> -max-transfer-rate 100MB`. Throttle during business hours and release overnight. Use `snapmirror show -fields transfer-size` to monitor transfer rates."),
        "rolling_upgrade": ("How do I pause SnapMirror during an ONTAP upgrade and resume without resync?",
            "Quiesce before upgrade: `snapmirror quiesce -destination-path <path>`. After upgrade, resume: `snapmirror resume -destination-path <path>`. Resync is not needed unless the relationship is broken."),
        "add_resource": ("What is the correct procedure to set up a new SnapMirror relationship?",
            "Create destination volume (DP type): `volume create -vserver dst -volume dst_vol -type DP`. Initialize relationship: `snapmirror create -source-path src:src_vol -destination-path dst:dst_vol -type XDP -policy MirrorAllSnapshots`. `snapmirror initialize`."),
        "warning": ("SnapMirror shows 'lag-time > RPO target'. What does it mean?",
            "The replica is behind the defined recovery point objective. Check transfer status: `snapmirror show -instance`. Look for errors. Manually trigger update: `snapmirror update -destination-path <path>`. Check network bandwidth."),
        "perf": ("SnapMirror transfers are not completing within the schedule interval — where do I start?",
            "Check transfer rate vs data change rate. Increase throttle limit or reduce change rate. Enable compression: `snapmirror modify -compression true`. Switch to XDP with `MirrorAndVault` policy to reduce initial baseline transfers."),
        "backup_freq": ("How often should I verify SnapMirror relationship health?",
            "Daily automated check via `snapmirror show -health false` in a monitoring script. Alert on any unhealthy relationship. Test failover quarterly by breaking and resyncing a non-production relationship."),
        "restore": ("How do I restore from SnapMirror when the source volume is lost?",
            "Break the SnapMirror relationship on the destination: `snapmirror break -destination-path <path>`. The destination becomes read-write. Mount it on the target host. After source recovery, reverse-resync: `snapmirror resync -source-path dst:dst_vol -destination-path src:src_vol`."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/netapp/superna-eyeglass/operations", "netapp-superna-eyeglass", "Superna Eyeglass for NetApp", {
        "version_check": ("What Superna Eyeglass version is recommended?",
            "Eyeglass 2.9.x is the current recommendation. Check via Eyeglass Admin UI → Help → About. Eyeglass runs as a virtual appliance — update via the Eyeglass update mechanism."),
        "version_cmd": "Eyeglass Admin UI → Help → About",
        "default_setting": ("What is the default configuration replication interval?",
            "Eyeglass replicates CIFS/SMB share and export configurations between clusters every 15 minutes by default. Increase to 5 minutes for environments requiring tighter config sync. Decrease frequency for stable environments to reduce overhead."),
        "enable_feature": ("How do I enable Eyeglass ransomware detector?",
            "Eyeglass Ransomware Defender is a licensed add-on. Enable via Eyeglass → Settings → Ransomware → Enable. Configure FPolicy integration on PowerScale. Set entropy threshold and alert recipients."),
        "rolling_upgrade": ("How do I upgrade Eyeglass without interrupting configuration replication?",
            "Eyeglass upgrades require a brief restart of the appliance. Configuration replication pauses during upgrade (typically 5-10 minutes). After upgrade, verify all managed clusters reconnect via Eyeglass → Inventory."),
        "add_resource": ("What is the correct procedure to add a new PowerScale cluster to Eyeglass?",
            "Eyeglass UI → Inventory → Add Cluster. Provide management IP, API credentials, and cluster name. Eyeglass discovers all SVMs and begins monitoring share/export configurations."),
        "warning": ("Eyeglass shows 'Configuration Sync Error' for a cluster pair. What does it mean?",
            "Eyeglass cannot push configuration changes to the destination cluster. Check API connectivity to the destination cluster. Verify credentials have not expired. Review Eyeglass logs under Administration → Logs."),
        "perf": ("Eyeglass is slow to reflect configuration changes — where do I start?",
            "Check the replication interval setting. Verify network connectivity between Eyeglass and all clusters. Review the Eyeglass task queue — large configuration changes (many shares) may queue. Increase Eyeglass VM resources if needed."),
        "backup_freq": ("How often should I back up Eyeglass configuration?",
            "Weekly via Eyeglass → Administration → Backup. Backup includes all cluster registrations, replication policies, and alert settings. Store off-appliance."),
        "restore": ("Can I restore Eyeglass configuration after appliance failure?",
            "Yes — deploy a new Eyeglass OVA, apply the backup via the Eyeglass restore wizard. All cluster registrations and policies are restored. Re-authenticate any expired cluster credentials after restore."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    # Pure
    ("storage/pure/evergreen-one/operations", "pure-evergreen-one", "Pure Storage Evergreen//One", {
        "version_check": ("How do I check my Evergreen//One consumption and service level?",
            "Log in to Pure1 (pure1.purestorage.com) → Evergreen//One → Subscriptions. View consumed capacity vs committed, performance tier, and burst usage."),
        "version_cmd": "Pure1 → Evergreen//One → Subscriptions",
        "default_setting": ("What is the default burst tolerance for Evergreen//One?",
            "Evergreen//One includes burst capacity as part of the subscription model. The specific burst allowance depends on your contract (typically 20-30% above committed). Review your SOW for exact terms."),
        "enable_feature": ("How do I enable Pure Evergreen//One capacity reporting notifications?",
            "In Pure1 → Evergreen//One → Alerts, configure consumption threshold alerts. Set notifications at 80% and 95% of committed capacity. Alerts are sent via email to the subscription contacts."),
        "rolling_upgrade": ("How does Pure manage hardware and software upgrades under Evergreen//One?",
            "Pure handles all hardware and software upgrades proactively as part of the service. Upgrades are scheduled with the customer and performed non-disruptively. You receive Purity//FA or Purity//FB upgrades automatically."),
        "add_resource": ("What is the correct procedure to add capacity to an Evergreen//One subscription?",
            "Contact your Pure account team or submit a request via Pure1. Capacity additions under Evergreen//One are provisioned by Pure — no hardware procurement required. Changes take effect at the next billing period."),
        "warning": ("Pure1 shows 'Evergreen//One capacity at risk'. What does it mean?",
            "Projected growth will exceed committed capacity before the next renewal. Contact your Pure account team immediately to adjust the subscription. Evergreen//One includes proactive capacity management from Pure."),
        "perf": ("Evergreen//One performance is below the contracted SLA tier — where do I start?",
            "Open a case with Pure Support. Evergreen//One SLAs are contractually backed — Pure is responsible for delivering the contracted performance tier. Pure1 analytics will be used to investigate."),
        "backup_freq": ("How is Evergreen//One data protected?",
            "Evergreen//One includes the underlying FlashArray or FlashBlade platform redundancy. Application-level backup (Veeam, SnapCenter) is the customer's responsibility. SafeMode snapshots are available as an add-on."),
        "restore": ("Can I restore from a snapshot under Evergreen//One?",
            "Yes — snapshots are managed on the underlying FlashArray/FlashBlade platform. Restore via Pure1, the array CLI, or the Pure Storage vSphere plugin. Evergreen//One does not change the snapshot restore mechanism."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/pure/evergreen/operations", "pure-evergreen", "Pure Storage Evergreen", {
        "version_check": ("How do I verify my array is enrolled in the Evergreen programme?",
            "Log in to Pure1 → Arrays → select the array → Support Contracts → confirm Evergreen subscription is active. Check that Controller Evergreen is enabled for non-disruptive controller upgrades."),
        "version_cmd": "Pure1 → Arrays → Support Contracts",
        "default_setting": ("What does Evergreen//Forever include by default?",
            "Evergreen//Forever includes non-disruptive controller upgrades every 3 years (for FlashArray), software upgrades, and DirectFlash module refreshes. Capacity is not included — only the controller and software refresh."),
        "enable_feature": ("How do I schedule a controller upgrade under Evergreen//Forever?",
            "Contact Pure Support or your account team 90 days before the 3-year refresh window. Pure coordinates the upgrade timing and performs the non-disruptive controller swap. Downtime is not required."),
        "rolling_upgrade": ("How does Pure perform non-disruptive controller upgrades under Evergreen?",
            "Pure connects remotely, migrates I/O to one controller, replaces the other, then migrates back. Total host-visible impact: zero (HA failover handles I/O during swap). Typically completed in 2-4 hours per array."),
        "add_resource": ("What is the correct procedure to initiate an Evergreen controller refresh?",
            "Log a support case with Pure labelled 'Evergreen Controller Refresh'. Pure verifies eligibility, schedules the work, and ships new controllers. Coordinate with your maintenance window calendar."),
        "warning": ("Pure1 shows 'Evergreen refresh due'. What does it mean?",
            "Your array is eligible for a controller refresh under the Evergreen programme. Schedule the refresh within the eligibility window — delaying too long may forfeit the refresh entitlement."),
        "perf": ("Post-Evergreen upgrade performance is different from pre-upgrade — where do I start?",
            "New controllers may have different performance characteristics (higher baseline throughput, different latency profiles). Review Pure1 performance metrics before and after. Contact Pure if performance is below pre-upgrade baselines."),
        "backup_freq": ("Is there any configuration backup needed before an Evergreen upgrade?",
            "Pure backs up all array configuration as part of the upgrade process. No customer action required. However, verify your application-level backups are current before the upgrade window as a standard precaution."),
        "restore": ("What if an Evergreen upgrade causes unexpected issues?",
            "Contact Pure Support immediately. Pure can roll back the controller swap if issues occur within the upgrade window. Pure1 monitoring is active throughout the upgrade to detect anomalies."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/pure/flasharray/operations", "pure-flasharray", "Pure Storage FlashArray", {
        "version_check": ("What Purity//FA version is recommended?",
            "Purity//FA 6.5.x is the current recommendation. Check via Pure1 or `purearray list --version` on the CLI. Pure1 will also recommend the latest qualified upgrade path for your array model."),
        "version_cmd": "purearray list --version",
        "default_setting": ("What is the default data reduction setting and when should it change?",
            "Inline deduplication and compression are enabled by default on all FlashArray models. Never disable these — they are always beneficial and do not impact latency on flash media. DRR typically ranges 3:1 to 5:1."),
        "enable_feature": ("How do I enable SafeMode for ransomware protection?",
            "Contact Pure Support to enable SafeMode. Once enabled, snapshots cannot be deleted for the configured retention period (minimum 24 hours, configurable up to years). Eradication requires a 24-hour hold plus dual admin approval."),
        "rolling_upgrade": ("How do I upgrade Purity//FA without downtime?",
            "Pure upgrades are non-disruptive: Pure1 → select array → Update Software. Purity updates each controller sequentially with automatic HA failover. Typically completes in 30-90 minutes. Monitor via Pure1 during upgrade."),
        "add_resource": ("What is the correct procedure to add a new host and provision a volume?",
            "Create host: `purehost create <hostname> --iqn <iqn>` (iSCSI) or `--wwn <wwn>` (FC). Create volume: `purevol create <vol> --size 1T`. Connect: `purehost connect <hostname> --vol <vol> --lun 1`. Rescan on host."),
        "warning": ("FlashArray shows 'SafeMode eradication pending'. What does it mean?",
            "A volume or snapshot is scheduled for SafeMode eradication after the mandatory hold period. This cannot be cancelled by standard admins once initiated under SafeMode. Contact Pure Support if this was triggered accidentally."),
        "perf": ("FlashArray latency spiked above 1ms — where do I start?",
            "Check Pure1 → Performance → per-volume latency. Review host QoS policies. Look for queue depth storms from a single host (`purearray list --qos`). Check for garbage collection activity. Pure1 AI analytics will flag if this is anomalous."),
        "backup_freq": ("How often should I back up FlashArray configuration?",
            "Pure1 automatically backs up array configuration. Additionally: `puresupport bundle --transfer` weekly for an offline backup bundle. Back up before any Purity upgrade."),
        "restore": ("Can I restore a single volume from a FlashArray snapshot?",
            "Yes — copy from snapshot: `purevol copy <snapshot>.<vol> <new-vol>`. Or overwrite in-place: `purevol copy --overwrite <snapshot>.<vol> <existing-vol>`. Connect the restored volume to the host and mount."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/pure/flashblade/operations", "pure-flashblade", "Pure Storage FlashBlade", {
        "version_check": ("What Purity//FB version is recommended?",
            "Purity//FB 4.3.x is the current recommendation. Check via Pure1 or FlashBlade UI → System → Software Version."),
        "version_cmd": "purefb list --version",
        "default_setting": ("What is the default NFS export security and when should it change?",
            "Default NFS exports use `sec=sys` (AUTH_SYS). For security-sensitive environments, use Kerberos (`sec=krb5p` for encryption). Kerberos requires KDC integration and DNS configuration on the FlashBlade."),
        "enable_feature": ("How do I enable S3 object store on FlashBlade?",
            "Create an Object Store account: `purefb objectstoreaccount create <acct>`. Create a bucket: `purefb objectstorebucket create <bucket> --account <acct>`. Create an access key: `purefb objectstoreuser create <user> --account <acct>`."),
        "rolling_upgrade": ("How do I upgrade Purity//FB without disrupting NFS/S3 clients?",
            "Purity//FB upgrades are non-disruptive. Initiate via Pure1 or FlashBlade UI → System → Software → Upgrade. Blades upgrade sequentially; clients reconnect automatically. Monitor via Pure1 during the upgrade."),
        "add_resource": ("What is the correct procedure to add a new file system and NFS export?",
            "`purefb fs create <fs> --size 10T`. Create export: `purefb nfs exportpolicy add --fs <fs> --rules 'client=*,access=rw,security=sys'`. Mount from client: `mount -t nfs <fb-vip>:/<fs> /mnt/point`."),
        "warning": ("FlashBlade shows 'Blade in Service Mode'. What does it mean?",
            "A blade has been taken offline for service (hardware issue or scheduled maintenance). Data is redistributed to remaining blades. Contact Pure Support if a blade enters service mode unexpectedly."),
        "perf": ("FlashBlade NFS throughput is below expected — where do I start?",
            "Check Pure1 performance metrics for the file system. Verify clients are using NFSv3 or NFSv4 (NFSv4.1 is preferred). Check NIC bonding on clients. Review rsize/wsize mount options (recommend 1M for large sequential I/O)."),
        "backup_freq": ("How often should I back up FlashBlade configuration?",
            "Weekly configuration export from FlashBlade UI → System → Download Configuration. Pure1 also maintains configuration history. For data protection, use FlashBlade native replication or integrate with a backup tool."),
        "restore": ("Can I restore a specific file from a FlashBlade snapshot?",
            "Yes — snapshots appear as read-only directories. Access via NFS: `ls /mnt/fs/.snapshot/<snapshot-name>/`. Copy the specific file from the snapshot directory back to the active file system."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("storage/pure/operations", "pure", "Pure Storage", {
        "version_check": ("How do I get a consolidated view of software versions across all Pure arrays?",
            "Pure1 → Arrays → view the Software Version column. Use Pure1 API to export version data for all arrays: `GET /api/1.latest/arrays?fields=name,version`. Pure1 also shows upgrade recommendations per array."),
        "version_cmd": "Pure1 → Arrays → Software Version column",
        "default_setting": ("What is the default Pure1 alert notification configuration?",
            "By default, alerts go to the array admin email set during installation. Add team email aliases via Pure1 → Administration → Notification Settings. Configure PagerDuty or Slack webhooks for critical alert routing."),
        "enable_feature": ("How do I enable Pure1 AI-driven forecasting?",
            "Pure1 predictive analytics are enabled by default for all enrolled arrays. View under Pure1 → Arrays → select array → Forecasting. Forecasting models capacity and performance trends using fleet-wide ML models."),
        "rolling_upgrade": ("How do I coordinate Purity upgrades across a mixed FlashArray and FlashBlade environment?",
            "Upgrade FlashArray first (more workloads depend on it). Then FlashBlade. Use Pure1's upgrade scheduler to stagger upgrades. Ensure no critical backup windows overlap with the upgrade schedule."),
        "add_resource": ("What is the correct procedure to add a new Pure array to Pure1 monitoring?",
            "Arrays enrol automatically via phone-home (HTTPS 443 to pure1.purestorage.com). Verify in Pure1 → Arrays — the new array should appear within 1 hour of first contact. If not, check firewall rules."),
        "warning": ("Pure1 shows 'Array at Risk' for a system. What does it mean?",
            "Pure AI has detected a hardware degradation, software bug, or configuration risk. Click through for details and recommended action. Pure Support may reach out proactively for Critical risks under Evergreen support."),
        "perf": ("Pure1 shows a performance anomaly for an array — where do I start?",
            "Pure1 → Arrays → select array → Performance. Review the anomaly timeline. Pure1 AI contextualises the anomaly against historical baseline and fleet averages. If anomalous, open a Pure Support case with the Pure1 link."),
        "backup_freq": ("How often should I review Pure1 health summaries?",
            "Daily quick check of Pure1 dashboard for any new Critical/Warning alerts. Weekly review of capacity forecasting and upgrade recommendations. Monthly review of performance trends against workload growth."),
        "restore": ("Can I use Pure1 to initiate a restore from a snapshot?",
            "Pure1 provides visibility but not direct restore initiation. Initiate restores via the array CLI, FlashArray UI, or vSphere/PowerShell plugins. Pure1 shows snapshot inventory and protection policy compliance."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("storage/pure/pure1/operations", "pure1", "Pure1", {
        "version_check": ("What version of Pure1 is currently deployed?",
            "Pure1 is a SaaS platform — Dell manages versioning. Check release notes at support.purestorage.com. Pure1 updates automatically; no customer action required."),
        "version_cmd": "Pure1 → Help → What's New",
        "default_setting": ("What is the default data retention period in Pure1?",
            "Pure1 retains performance and capacity data for 365 days by default. Historical data beyond 365 days is available in aggregated (daily) form for trend analysis. Real-time (1-minute) data is retained for 30 days."),
        "enable_feature": ("How do I enable Pure1 REST API access for automation?",
            "Pure1 → Administration → API Registration → Create. Generate an API key pair. Use the Pure1 API at `https://api.pure1.purestorage.com/api/1.latest/`. Full API reference at developer.purestorage.com."),
        "rolling_upgrade": ("How does Pure1 handle SaaS version updates?",
            "Pure1 updates automatically without customer involvement. New features appear in the UI with 'New' badges. Pure1 release notes are published at support.purestorage.com after each update."),
        "add_resource": ("What is the correct procedure to add a team member to Pure1?",
            "Pure1 → Administration → Users → Invite User. Enter email address and assign role (Array Admin, Fleet Admin, or Read-Only). The invited user receives an email to activate their Pure1 account."),
        "warning": ("Pure1 shows 'Array Not Connected' for a system. What does it mean?",
            "The array has not sent telemetry to Pure1 for an extended period. Check the array's network connectivity to pure1.purestorage.com (port 443). Verify the proxy configuration if outbound traffic is proxied."),
        "perf": ("Pure1 dashboard is slow to load — where do I start?",
            "Pure1 is a SaaS platform — performance is managed by Pure. If consistently slow, check your local network. For large fleets (100+ arrays), use Pure1 API for bulk data retrieval instead of UI browsing."),
        "backup_freq": ("Is Pure1 data backed up?",
            "Pure1 is a SaaS platform — Pure manages all data retention and backup. Array configuration backups and telemetry history are maintained by Pure. No customer backup action required."),
        "restore": ("Can I restore deleted Pure1 reports or dashboards?",
            "Custom dashboards and reports cannot be restored if deleted. Re-create them manually or export dashboard configurations (JSON) before deletion. Pure1 built-in dashboards are always available and cannot be deleted."),
        "ts_link": "../../troubleshooting/index.md",
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

print(f"Created {len(created_files)} FAQ files, {len(created_svgs)} SVGs (batch 3)")
