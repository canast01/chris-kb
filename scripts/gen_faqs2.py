#!/usr/bin/env python3
"""Generate FAQ stubs — batch 2: SAN + security."""

import os
import xml.etree.ElementTree as ET

BASE = "/Users/chrisanastasiadis/chris-kb/docs"
ASSETS = "/Users/chrisanastasiadis/chris-kb/docs/assets"

PRODUCTS = [
    # SAN
    ("san/brocade/fabric-os/operations", "fabric-os", "Brocade Fabric OS", {
        "version_check": ("What Fabric OS version is recommended for new deployments?",
            "FOS 9.2.x is the current recommended release for Gen 7 (64G) switches. For Gen 6 (32G), FOS 8.2.x. Check with `version` CLI command on the switch."),
        "version_cmd": "version",
        "default_setting": ("What is the default zoning mode and when should it change?",
            "Soft zoning (WWN-based) is the default but provides no enforcement at the ASIC level. Use hard zoning (port-based) for security-sensitive environments. Enable with `defzone --noaccess`."),
        "enable_feature": ("How do I enable FIPS mode on Fabric OS?",
            "Run `fipscfg --enable` after verifying all connected devices support FIPS-compliant algorithms. Note: FIPS mode disables older SSH/TLS cipher suites — test connectivity first. Reboot required after enabling."),
        "rolling_upgrade": ("How do I perform a non-disruptive firmware upgrade on a Brocade switch?",
            "Use `firmwaredownload -s` (single reboot) for non-disruptive upgrade on supported platforms. For chassis switches, upgrade one blade at a time using `firmwaredownload -b`. Verify ISL stability post-upgrade with `islshow`."),
        "add_resource": ("What is the correct procedure to add a new host to an existing zone?",
            "Get the host HBA WWN with `nsshow`. Add to the zone: `zoneadd zonename --member <wwn>`. Save config: `cfgsave`. Enable: `cfgenable configname`. Verify with `zoneshow`."),
        "warning": ("Switch shows 'E_Port Isolated' on an ISL. What does it mean?",
            "The ISL is isolated due to a fabric parameter mismatch (e.g., BB credit, speed, or domain ID conflict). Check `islshow` and `errdump`. Common causes: speed mismatch, duplicate domain IDs, or incompatible fabric parameters."),
        "perf": ("FC fabric throughput degraded — where do I start?",
            "Run `perfshow` or `toptalkers` to identify congested ports. Check BB credit zero counts with `portperfshow`. Look for SCSI timeouts in host logs. Check ISL utilisation — add ISLs if above 70% sustained."),
        "backup_freq": ("How often should I back up Fabric OS switch configuration?",
            "Weekly via `configupload` to a SFTP server. Back up before any firmware upgrade or zoning change. Store named configs with date stamps. Test restore on a lab switch annually."),
        "restore": ("Can I restore a single zone without a full configuration restore?",
            "Yes — export the zone database with `configupload -all`, edit the zone file, then `configdownload` the modified file. Alternatively, re-create the zone manually with `zonecreate` and `zoneadd` commands."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("san/brocade/sannav/operations", "sannav", "Brocade SANnav", {
        "version_check": ("What SANnav version is recommended?",
            "SANnav 2.3.x is the current release. Check via SANnav UI → Administration → About SANnav. SANnav runs as a Docker-based appliance — update via `sannav upgrade` CLI."),
        "version_cmd": "sannav --version",
        "default_setting": ("What is the default performance polling interval and when should it change?",
            "Default is 60 seconds. Reduce to 30 seconds for high-density environments where you need tighter visibility into congestion events. Increasing to 300 seconds reduces database growth for large fabrics."),
        "enable_feature": ("How do I enable SANnav Flow Vision for latency monitoring?",
            "Flow Vision is enabled per-fabric under Fabric → Flow Vision → Enable. Requires FOS 8.2.1+ on monitored switches. Generates per-flow latency metrics visible in SANnav dashboards."),
        "rolling_upgrade": ("How do I upgrade SANnav without losing historical data?",
            "Back up the SANnav database before upgrade (`sannav backup`). Run the upgrade via `sannav upgrade <image>`. Historical data is preserved in the PostgreSQL backend. Verify fabric connectivity post-upgrade."),
        "add_resource": ("What is the correct procedure to add a new fabric to SANnav?",
            "Navigate to Fabrics → Add Fabric. Provide the seed switch IP and credentials. SANnav discovers the entire fabric via SNMP and REST. Verify all switches appear under the fabric view within 5 minutes."),
        "warning": ("SANnav shows 'Switch Not Reachable'. What does it mean?",
            "SANnav cannot reach the switch via management IP. Check network connectivity, SNMP community strings, and firewall rules (port 161/UDP, 443/TCP). Verify the switch management IP matches what SANnav has configured."),
        "perf": ("SANnav UI is slow — where do I start?",
            "Check SANnav server resource usage (`docker stats`). Increase JVM heap if under-allocated. Review the number of discovered switches — very large fabrics (500+ switches) require the large-deployment sizing. Purge old performance data."),
        "backup_freq": ("How often should I back up SANnav?",
            "Weekly automated backup via `sannav backup --schedule`. Store backups off the SANnav host. Include the backup in your overall infrastructure backup strategy. Test restore to a secondary SANnav instance annually."),
        "restore": ("Can I restore SANnav to a previous version if an upgrade fails?",
            "Yes — if the upgrade fails and a rollback is needed, restore from the pre-upgrade backup using `sannav restore <backup-file>`. This restores both the application and database to the pre-upgrade state."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("san/cisco/cisco-dcnm/operations", "cisco-dcnm", "Cisco DCNM", {
        "version_check": ("What DCNM version is recommended?",
            "Cisco DCNM 11.5(x) is the last release before NDFC (Nexus Dashboard Fabric Controller). New deployments should use NDFC 12.x. Check DCNM version via Web UI → Settings → About."),
        "version_cmd": "show version  # on DCNM CLI",
        "default_setting": ("What is the default fabric management mode and when should it change?",
            "Monitor mode (read-only) is the default after initial setup. Switch to Managed mode to allow DCNM to push configuration changes to switches. Change under Fabric Settings → Fabric Type."),
        "enable_feature": ("How do I enable DCNM telemetry streaming for real-time fabric metrics?",
            "Configure Telemetry under Administration → Performance Setup. Select switches, enable gRPC streaming, and set the collection interval. Requires Nexus switches with NX-OS 9.3.5+ for full telemetry support."),
        "rolling_upgrade": ("How do I upgrade DCNM without disrupting fabric management?",
            "Back up DCNM database. Upgrade DCNM appliance via the inline upgrade process. During upgrade, switch management is unavailable but fabric forwarding continues unaffected. Plan for 30-60 minute management outage."),
        "add_resource": ("What is the correct procedure to add a new switch to DCNM?",
            "Ensure DCNM can reach the switch management IP. Go to Fabric → Add Switches → Discover. Enter the seed IP, credentials, and SNMP community. DCNM discovers neighbours via CDP/LLDP and adds them automatically."),
        "warning": ("DCNM shows 'Out-of-Sync' for a switch. What does it mean?",
            "The switch running config does not match what DCNM expects to have deployed. Use Fabric → Deploy → Recalculate and Deploy to reconcile. Review the diff before deploying to avoid unexpected config changes."),
        "perf": ("DCNM inventory refresh is very slow — where do I start?",
            "Check DCNM server resource utilisation. Verify SNMP connectivity to all switches. Reduce poller frequency for large fabrics. Split very large fabrics into multiple DCNM-managed domains if needed."),
        "backup_freq": ("How often should I back up DCNM?",
            "Weekly via DCNM Administration → Backup & Restore. Backup includes the database and switch configurations. Store off-appliance. Back up before any software upgrade."),
        "restore": ("Can I restore a single switch configuration from DCNM backup?",
            "Yes — individual switch configs are stored in DCNM. Go to Configure → Backup → select the switch and restore point. This restores only that switch's configuration, not the full DCNM database."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("san/cisco/mds/operations", "cisco-mds", "Cisco MDS", {
        "version_check": ("What NX-OS version is recommended for Cisco MDS?",
            "MDS NX-OS 9.4(x) is the current recommended release for new deployments. Check with `show version` from the switch CLI. Always review the Cisco Field Notice list before upgrading production switches."),
        "version_cmd": "show version",
        "default_setting": ("What is the default VSANs configuration and when should it be changed?",
            "VSAN 1 is the default and all ports are assigned to it. Always create dedicated VSANs per fabric (e.g., VSAN 10 for Fabric A, VSAN 20 for Fabric B). Remove unused ports from VSAN 1 to limit broadcast domain."),
        "enable_feature": ("How do I enable Cisco MDS NPIV for virtualisation environments?",
            "NPIV is enabled per-interface: `feature npiv` globally, then `switchport mode NP` on the F-ports connecting to virtual HBA environments. Allows each VM HBA to register its own WWPN with the fabric."),
        "rolling_upgrade": ("How do I perform a non-disruptive upgrade on a Cisco MDS switch?",
            "Use ISSU (In-Service Software Upgrade) if supported for the target release: `install all nxos <image>`. ISSU upgrades supervisors and linecards sequentially without disrupting I/O. Verify ISSU compatibility in the release notes first."),
        "add_resource": ("What is the correct procedure to add a new host to a zone on Cisco MDS?",
            "Get WWN from `show flogi database`. Add to zone: `zone name MyZone vsan 10; member pwwn <wwn>`. Update zoneset: `zoneset name MyZoneset vsan 10; member MyZone`. Activate: `zoneset activate name MyZoneset vsan 10`."),
        "warning": ("MDS shows 'Domain overlap' error. What does it mean?",
            "Two switches have the same domain ID, causing fabric segmentation. Fix by changing domain ID on one switch: `fcdomain domain <id> preferred vsan <id>` and remerging the fabric. Plan domain IDs before connecting new switches."),
        "perf": ("FC performance degraded on MDS — where do I start?",
            "Run `show interface fc x/x counters` for error counts. Check credit loss with `show interface fc x/x | include credit`. Use `show analytics top-ports` for congestion visibility. Look for SCSI timeouts in host/storage logs."),
        "backup_freq": ("How often should I back up MDS configuration?",
            "Weekly via `copy running-config sftp://<server>/mds-config-$(date).txt`. Always back up before firmware upgrades or major zoning changes. Store configs in version control."),
        "restore": ("Can I restore a single zone without a full configuration restore?",
            "Yes — use `show zoneset active vsan 10` to view current active zones. Edit the zone database interactively using `zone` commands, then re-activate the zoneset. No full config restore needed for zone-only changes."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    ("san/cisco/nexus-dashboard/operations", "nexus-dashboard", "Cisco Nexus Dashboard", {
        "version_check": ("What Nexus Dashboard version is recommended?",
            "Nexus Dashboard 3.1.x with NDFC 12.2.x is the current recommendation. Check via UI → Admin → System Settings → About. Nexus Dashboard runs as a cluster of 3 or 5 nodes."),
        "version_cmd": "acs version  # on ND CLI",
        "default_setting": ("What is the default cluster size and when should it be changed?",
            "3-node cluster is the minimum for production (provides HA). Scale to 5 nodes for large deployments with multiple services (NDFC + NDI + NDO) co-hosted. Single-node is for lab/evaluation only."),
        "enable_feature": ("How do I enable Nexus Dashboard Insights (NDI) on an existing cluster?",
            "Go to Admin → Services → install NDI from Cisco App Store or upload the service image. NDI requires minimum 3 nodes and specific memory (128 GB per node recommended). Enable after NDI install under the Services hub."),
        "rolling_upgrade": ("How do I upgrade the Nexus Dashboard cluster without downtime?",
            "ND supports rolling upgrades: Admin → Software Management → Upgrade. One node upgrades at a time; the cluster remains operational during the process. The upgrade completes when all nodes are on the new version."),
        "add_resource": ("What is the correct procedure to add a new site to Nexus Dashboard?",
            "Go to Sites → Add Site. For ACI: provide APIC IP and credentials. For DCNM/NDFC: provide NDFC IP. ND discovers the site inventory. Associate the site with NDO/NDFC/NDI services as needed."),
        "warning": ("Nexus Dashboard shows 'Cluster Health Degraded'. What does it mean?",
            "One or more ND nodes are unhealthy. Check Admin → System Status for node-level details. Common causes: disk full, node unreachable, or service crash. Review ND node logs via `acs logs` on the affected node."),
        "perf": ("Nexus Dashboard UI is slow or services are unresponsive — where do I start?",
            "Check cluster resource utilisation: Admin → Infrastructure → Nodes. If disk is above 80%, purge old data. Check Kubernetes pod health with `kubectl get pods -A` from the ND CLI. Restart unhealthy pods if needed."),
        "backup_freq": ("How often should I back up Nexus Dashboard?",
            "Weekly via Admin → System Settings → Backup & Restore. Backup includes ND cluster configuration and all service data. Store externally (remote SCP/SFTP). Back up before every upgrade."),
        "restore": ("Can I restore a single service's data without a full ND restore?",
            "Not independently for all services. NDFC allows individual fabric backup/restore. NDI data is re-synced from the fabric after restore. For full ND failure, restore from the cluster backup."),
        "ts_link": "../../../troubleshooting/index.md",
    }),
    # security
    ("security/access-review/operations", "access-review", "Access Review", {
        "version_check": ("How do I determine the current access review cycle status?",
            "Check your IGA platform (SailPoint, Saviynt, or similar) for the active campaign. For manual reviews, check the access review register in your GRC tool or SharePoint. Review campaigns typically run quarterly."),
        "version_cmd": "Check IGA platform → Campaigns → Active",
        "default_setting": ("What is the default access review frequency and when should it change?",
            "Quarterly for privileged access, semi-annual for standard user access. High-risk systems (financial, PII) may require monthly reviews. Adjust frequency based on risk classification and regulatory requirements (SOX, ISO 27001)."),
        "enable_feature": ("How do I enable automated access review reminders?",
            "Configure escalation rules in your IGA platform: send reminder at day 3, escalate to manager at day 7, auto-revoke or flag at day 14. For manual campaigns, use Power Automate or ServiceNow workflow for reminders."),
        "rolling_upgrade": ("How do I transition from manual to automated access reviews?",
            "Start with an IGA pilot for one application. Map roles and entitlements. Configure reviewers. Run parallel manual and automated reviews for one cycle. Expand to additional applications after validating accuracy."),
        "add_resource": ("What is the correct procedure to add a new application to the access review scope?",
            "Onboard the application to your IGA platform (configure connector or manual import). Define reviewers (application owner, manager, or risk owner). Set review frequency and remediation SLA. Add to the next scheduled campaign."),
        "warning": ("Access review shows many 'certify all' approvals without individual review. What does it mean?",
            "Rubber-stamping is a common audit finding. Implement controls: require per-item certification, add justification fields, track review time. Flag reviewers with >50 certifications/minute for manager follow-up."),
        "perf": ("Access review completion rate is below 80% — where do I start?",
            "Send targeted reminders to incomplete reviewers. Escalate to their managers. Reduce scope by excluding inactive accounts before the campaign. Consider delegating review to application owners rather than managers."),
        "backup_freq": ("How often should I archive access review evidence?",
            "Retain completed review records for at least 3 years (ISO 27001, SOX requirement). Export certification reports to your GRC tool or document management system after each campaign. Include reviewer decisions and timestamps."),
        "restore": ("Can I reopen a completed access review campaign?",
            "Most IGA platforms do not allow reopening completed campaigns. If remediation is needed post-completion, raise an exception in your GRC tool and revoke access manually with documented justification."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/certificates/operations", "certificates", "Certificate Management", {
        "version_check": ("How do I check certificate expiry dates across my infrastructure?",
            "Use `openssl x509 -in cert.pem -noout -dates` for individual certs. For bulk checks: use Venafi, cert-manager, or a script with `echo | openssl s_client -connect host:443 2>/dev/null | openssl x509 -noout -dates`."),
        "version_cmd": "openssl x509 -in cert.pem -noout -dates",
        "default_setting": ("What is the recommended certificate validity period?",
            "TLS certificates: maximum 397 days (browser requirement since 2020). Internal CA certificates: 5 years for intermediate, 10-20 years for root. Code signing: 1-3 years. Shorter validity reduces exposure window from key compromise."),
        "enable_feature": ("How do I enable automatic certificate renewal with ACME/Let's Encrypt?",
            "Deploy cert-manager in Kubernetes (`kubectl apply -f cert-manager.yaml`), or use Certbot on standalone servers (`certbot renew --pre-hook 'stop nginx' --post-hook 'start nginx'`). Configure renewal at 30 days before expiry."),
        "rolling_upgrade": ("How do I rotate a wildcard certificate across multiple servers without downtime?",
            "Stage the new cert on all servers before the cutover. Use a load balancer to health-check each server. Reload (not restart) nginx/Apache per server: `nginx -s reload`. Verify with `openssl s_client -connect host:443`."),
        "add_resource": ("What is the correct procedure to issue a new internal certificate?",
            "Generate CSR: `openssl req -new -key server.key -out server.csr -subj '/CN=hostname.corp.local'`. Submit to internal CA (EJBCA, ADCS, Vault PKI). Verify SAN fields include all hostnames and IPs. Install cert and chain."),
        "warning": ("Browser shows 'Certificate Not Trusted' for an internal site. What does it mean?",
            "The internal CA root certificate is not in the client's trust store. Deploy the root CA cert via GPO (Windows), `/etc/ssl/certs/` (Linux), or MDM (macOS/iOS). Alternatively, issue a cert from a public CA for externally accessible services."),
        "perf": ("TLS handshake latency is high — where do I start?",
            "Check OCSP stapling is enabled on the server (`ssl_stapling on` in nginx). Ensure session resumption is configured. Review certificate chain length — intermediate certs should be bundled. Use ECDSA certs (faster) over RSA 4096."),
        "backup_freq": ("How often should I back up certificate private keys?",
            "Private keys should be stored in a secrets manager (HashiCorp Vault, AWS Secrets Manager) with automatic backups. For HSM-backed keys, the HSM backup schedule applies. Never store private keys in Git or shared drives."),
        "restore": ("Can I recover a lost private key?",
            "No — private keys cannot be recovered if lost. Issue a new certificate with a new key pair. Revoke the old certificate via CRL or OCSP. This is why private keys must be backed up securely at issuance time."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/compliance-standards/operations", "compliance-standards", "Compliance Standards", {
        "version_check": ("How do I determine which compliance frameworks apply to my organisation?",
            "Review regulatory requirements by industry (PCI-DSS for payments, HIPAA for healthcare, SOX for public companies) and geography (GDPR for EU data). Map against your data classification and system inventory."),
        "version_cmd": "Review GRC platform → Frameworks → Active",
        "default_setting": ("What is the default control review frequency under ISO 27001?",
            "ISO 27001 requires annual internal audits at minimum. Critical controls (access management, incident response) should be reviewed quarterly. Some controls (patch management, backup verification) need monthly evidence collection."),
        "enable_feature": ("How do I enable continuous compliance monitoring?",
            "Deploy a CSPM tool (Prisma Cloud, AWS Security Hub, Azure Defender for Cloud) for cloud controls. For on-premises, use a vulnerability scanner (Tenable, Qualys) with scheduled scans mapped to compliance controls in your GRC tool."),
        "rolling_upgrade": ("How do I transition from a manual compliance programme to a GRC platform?",
            "Start with control inventory in the GRC tool. Map evidence sources. Automate evidence collection for technical controls first. Migrate risk register and audit findings. Train control owners on evidence upload process."),
        "add_resource": ("What is the correct procedure to add a new system to the compliance scope?",
            "Classify the system by data type and regulatory relevance. Assign a system owner. Add to the CMDB and GRC asset inventory. Identify applicable controls. Schedule initial baseline assessment within 30 days of go-live."),
        "warning": ("GRC tool shows a control with 'Evidence Overdue'. What does it mean?",
            "The scheduled evidence collection date has passed without submission. Escalate to the control owner immediately. Late evidence is an audit finding. Investigate whether the control activity is occurring — the gap may indicate a real deficiency."),
        "perf": ("Compliance programme is generating too many low-quality findings — where do I start?",
            "Tune risk thresholds in your GRC tool to suppress accepted risks. Consolidate duplicate findings from overlapping frameworks (map ISO 27001 to SOC 2 controls). Focus remediation effort on high-risk, high-impact findings first."),
        "backup_freq": ("How long should I retain compliance evidence?",
            "PCI-DSS: 12 months online, 12 months offline. SOX: 7 years. ISO 27001: duration of certification + 3 years. GDPR: as long as processing continues plus applicable statute of limitations. Store in tamper-evident repository."),
        "restore": ("Can I retroactively collect compliance evidence after an audit period?",
            "No — evidence must be contemporaneous (collected at the time of the control activity). Retroactive collection is not acceptable to auditors. If evidence was not collected, the control is considered not operating effectively for that period."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/cyberark/operations", "cyberark", "CyberArk PAM", {
        "version_check": ("What CyberArk version is recommended for new deployments?",
            "CyberArk v13.x (Privilege Cloud) or v12.6+ for self-hosted. Check via PrivateArk Client → Help → About or PVWA → Administration → System Health. Keep within 2 versions of latest for support."),
        "version_cmd": "PVWA → Administration → System Health → Version",
        "default_setting": ("What is the default Master Policy setting for session recording?",
            "Session recording is disabled by default. Enable for all privileged sessions: PVWA → Policies → Master Policy → Session Management → Record and save sessions. This is a key control for SOX and PCI-DSS compliance."),
        "enable_feature": ("How do I enable CyberArk PSM for SSH session recording?",
            "Install PSM for SSH (PSMP) on a Linux server. Configure the PSMP in PVWA under Administration → Components → PSM. Add the PSMP server as a Connection Component in your Platforms. Test SSH proxy via `ssh user@psmp-host`."),
        "rolling_upgrade": ("How do I upgrade CyberArk Vault without downtime?",
            "DR Vault must be upgraded first. Pause replication, upgrade DR Vault, verify, resume replication. Then upgrade the Primary Vault during a maintenance window. Component upgrades (PVWA, CPM, PSM) can be done rolling."),
        "add_resource": ("What is the correct procedure to onboard a new privileged account?",
            "In PVWA, go to Accounts → Add Account. Select the Safe, Platform, and enter credentials. Configure reconcile account if needed. CPM will manage the password automatically per the Platform policy."),
        "warning": ("CyberArk shows 'Dual Control request pending'. What does it mean?",
            "A privileged account retrieval requires approval from a second authorised user (Dual Control is enabled on the Safe or Platform). The requester is waiting. The approver must log in to PVWA → My Requests to approve."),
        "perf": ("PVWA login is slow — where do I start?",
            "Check PVWA server IIS application pool health. Verify Vault connectivity from PVWA. Check Windows event logs on PVWA server. Verify LDAP/AD integration response time. Check CyberArk Vault log (`italog.log`) for errors."),
        "backup_freq": ("How often should I back up the CyberArk Vault?",
            "Daily replication to DR Vault is the primary protection. Additionally, configure Vault Backup utility (`CAVaultManager`) for an encrypted offline backup weekly. Store offsite. Test restore to an isolated environment quarterly."),
        "restore": ("Can I restore a single account's password history without a full Vault restore?",
            "No — individual account history is embedded in the Vault database. For single-account recovery, use the CAVaultManager restore to a test Vault, then export the specific account. Full Vault restore is needed for bulk recovery."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/incident-handling/operations", "incident-handling", "Incident Handling", {
        "version_check": ("How do I check the current incident handling process version?",
            "Check your incident response plan (IRP) document version in your GRC tool or document management system. ISO 27001 requires annual review of the IRP. Verify last review date is within 12 months."),
        "version_cmd": "Check GRC tool → Policies → Incident Response Plan → Version history",
        "default_setting": ("What is the default incident severity classification?",
            "P1 (Critical): service down, data breach active. P2 (High): significant degradation or potential breach. P3 (Medium): limited impact, workaround available. P4 (Low): cosmetic or informational. Adjust definitions per organisation risk tolerance."),
        "enable_feature": ("How do I enable automated incident triage with SOAR?",
            "Integrate your SIEM (Splunk, Microsoft Sentinel) with a SOAR platform (Palo Alto XSOAR, Splunk SOAR). Configure playbooks to auto-triage common alert types (failed logins, malware detection) and create incidents in ServiceNow automatically."),
        "rolling_upgrade": ("How do I update the incident response plan without disrupting active incident handling?",
            "Update the IRP in draft status. Review with the incident response team. Publish the new version. Brief all responders on changes. Run a tabletop exercise within 30 days to validate the updated procedures."),
        "add_resource": ("What is the correct procedure to add a new system to the incident scope?",
            "Add the system to your CMDB with security classification. Configure logging to the SIEM. Create detection rules for expected threat scenarios. Brief the incident response team on the system's architecture and blast radius."),
        "warning": ("SIEM shows a 'High Severity Alert' for unusual admin activity. What does it mean?",
            "An admin account accessed systems outside normal patterns. Immediately verify with the account owner. If unconfirmed: disable the account, preserve logs, and invoke the incident response plan for potential credential compromise."),
        "perf": ("Incident resolution times are exceeding SLA — where do I start?",
            "Review MTTR metrics per incident type. Identify bottlenecks (escalation delays, missing runbooks, tool access). Create or improve runbooks for the top 5 most common incident types. Conduct post-incident reviews for all P1/P2."),
        "backup_freq": ("How often should I test the incident response plan?",
            "Tabletop exercise quarterly. Full technical drill (simulated incident) annually. Test communication trees (call lists, out-of-band comms) semi-annually. Document results and update the IRP based on findings."),
        "restore": ("Can I recover deleted security logs needed for an incident investigation?",
            "Logs should be shipped to an immutable SIEM/log storage (Splunk, Elastic, S3 with Object Lock) where deletion is prevented. If local logs are deleted, check your log forwarding pipeline — well-architected environments retain logs independently of source systems."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/ldap-integration/operations", "ldap-integration", "LDAP Integration", {
        "version_check": ("How do I verify the LDAP server version and connectivity?",
            "Check AD DS version with `Get-ADDomainController | Select OperatingSystem`. For OpenLDAP: `ldapsearch -x -H ldap://server -b '' -s base objectClass=* namingContexts`. Verify port 389 (LDAP) or 636 (LDAPS) is open."),
        "version_cmd": "ldapsearch -x -H ldap://server:389 -b '' -s base",
        "default_setting": ("What is the default LDAP bind method and when should it change?",
            "Anonymous bind is the default in many configurations but should be disabled in production. Use a dedicated service account (bind DN) with read-only access. Always use LDAPS (port 636) or StartTLS — never plain LDAP in production."),
        "enable_feature": ("How do I enable LDAP over TLS (LDAPS) for an application integration?",
            "Install the LDAP server's CA certificate in the application's trust store. Configure the application's LDAP connection to use port 636 and `ssl: true`. Test with `ldapsearch -H ldaps://server:636`. Renew the LDAP server cert before expiry."),
        "rolling_upgrade": ("How do I migrate an LDAP integration from one directory server to another?",
            "Run both servers in parallel. Update the application's LDAP config to point to the new server. Test in staging. Switch DNS/IP to the new server for production. Keep the old server running for 1 week as fallback."),
        "add_resource": ("What is the correct procedure to add a new application LDAP integration?",
            "Create a dedicated service account in AD/LDAP with minimal permissions (read-only, specific OU). Configure the application with the bind DN, password, base DN, and search filter. Test with `ldapsearch` before go-live."),
        "warning": ("Application shows 'LDAP: error code 49 — 80090308: invalid credentials'. What does it mean?",
            "The bind DN password is incorrect or the account is locked/expired. Reset the service account password (coordinate with all applications using it). Check the account's lockout policy and review failed login events in AD."),
        "perf": ("LDAP-based authentication is slow — where do I start?",
            "Check network latency to the LDAP server. Verify the search base DN is scoped narrowly (specific OU, not root). Add indexes for commonly searched attributes (`sAMAccountName`, `mail`). Check DC load during peak login periods."),
        "backup_freq": ("How often should I back up LDAP configuration?",
            "For AD: backed up as part of DC System State backup (daily). For OpenLDAP: export with `slapcat > backup.ldif` weekly. Store bind DN passwords in a secrets manager. Document all integrations in CMDB."),
        "restore": ("Can I restore a single LDAP entry without a full directory restore?",
            "For AD: use AD Recycle Bin (`Restore-ADObject`) for deleted objects. For OpenLDAP: manually re-add the entry from the LDIF backup using `ldapadd`. For modified entries, use `ldapmodify` to restore specific attributes."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/mfa/operations", "mfa", "Multi-Factor Authentication", {
        "version_check": ("How do I check MFA coverage across all users and applications?",
            "Run an MFA coverage report from your IdP (Azure AD: Sign-in logs → filter by MFA status; Okta: Reports → MFA Usage). Aim for 100% coverage on privileged accounts and 95%+ on all users."),
        "version_cmd": "Azure AD: Get-MgUser -All | Select DisplayName,StrongAuthenticationRequirements",
        "default_setting": ("What is the recommended default MFA method?",
            "TOTP (authenticator app) or hardware FIDO2/WebAuthn keys for privileged accounts. Push notification (Duo, Microsoft Authenticator) for standard users. Avoid SMS OTP — it is phishable (SIM-swap attacks) and not acceptable for high-assurance requirements."),
        "enable_feature": ("How do I enable phishing-resistant MFA (FIDO2) in Azure AD?",
            "Register FIDO2 keys: Azure AD → Security → Authentication Methods → FIDO2 Security Key → Enable. Create a Conditional Access policy requiring FIDO2 for admin roles. Users register keys at `aka.ms/mfasetup`."),
        "rolling_upgrade": ("How do I migrate users from SMS OTP to authenticator app MFA?",
            "Enable the authenticator app method alongside SMS. Run an awareness campaign. Set a deprecation date for SMS. Use Conditional Access to block SMS-only users after the deadline. Provide a helpdesk escalation path for users who cannot enrol."),
        "add_resource": ("What is the correct procedure to enrol a new user in MFA?",
            "Send the user to `aka.ms/mfasetup` (Azure) or the Okta enrolment portal. Require at least two methods (app + backup). For hardware tokens, register the token serial number in the MFA platform. Verify enrolment before disabling bypass."),
        "warning": ("MFA shows many 'Unexpected MFA prompt' user complaints. What does it mean?",
            "Users are receiving MFA challenges they did not initiate — potential MFA fatigue attack. Audit sign-in logs for the affected accounts. Enable 'Number Matching' or 'Additional Context' in Authenticator to prevent fatigue approvals. Check for suspicious IPs."),
        "perf": ("MFA prompts are causing user friction and reducing productivity — where do I start?",
            "Configure risk-based Conditional Access: only prompt MFA when risk is elevated (unfamiliar location, new device). Enable session persistence for low-risk scenarios (14-day remembered devices). Reduce MFA frequency for trusted networks."),
        "backup_freq": ("How do I ensure users don't lose MFA access if they lose their device?",
            "Require users to register at least two MFA methods. Provide a recovery code (stored securely) or TAP (Temporary Access Pass) process. Document the identity verification process for MFA reset in your helpdesk procedures."),
        "restore": ("Can I bypass MFA temporarily for a locked-out admin?",
            "Yes — use a Temporary Access Pass (TAP) in Azure AD: `New-MgUserAuthenticationTemporaryAccessPassMethod`. Or break-glass admin accounts with FIDO2 keys stored in a physical safe should be pre-configured. Audit all bypass events."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/operations", "security", "Security Operations", {
        "version_check": ("How do I check the version and health of core security tooling?",
            "Check SIEM version in the platform admin UI. Verify EDR agent versions on endpoints via your EDR console (target: 100% of managed endpoints on current version). Check firewall firmware versions against vendor advisories."),
        "version_cmd": "Check SIEM → Admin → System Health; EDR console → Endpoints → Agent Version",
        "default_setting": ("What is the default log retention period and when should it change?",
            "90 days hot storage is a common default. Increase to 12 months for PCI-DSS, SOX, or GDPR compliance. Archive to cold storage (S3 Glacier) for 3-7 years. Define retention per log type in your data classification policy."),
        "enable_feature": ("How do I enable UEBA (User and Entity Behaviour Analytics) in the SIEM?",
            "Most modern SIEMs (Splunk UBA, Microsoft Sentinel) include UEBA. Enable via Admin → Settings → Analytics. Requires minimum 30 days of baseline data before generating meaningful anomaly alerts. Tune initial alert thresholds to reduce noise."),
        "rolling_upgrade": ("How do I upgrade SIEM infrastructure without losing log ingestion?",
            "Deploy the new SIEM version in parallel. Redirect log sources incrementally (10% at a time). Monitor ingestion gaps. Once validated, redirect all sources. Decommission the old SIEM after 2 weeks of parallel run."),
        "add_resource": ("What is the correct procedure to add a new log source to the SIEM?",
            "Identify the log format (syslog, CEF, JSON). Configure the source to forward logs to the SIEM collector. Create a parsing rule for the log format. Build detection rules for the source's key events. Test with sample log injection."),
        "warning": ("SIEM alert volume spiked 10x overnight. What does it mean?",
            "Either a real security event or a detection rule producing false positives (misconfigured threshold, new system added). Check the alert source — if a single rule is generating all alerts, tune the rule. If multiple rules, investigate as potential incident."),
        "perf": ("SIEM search queries are timing out — where do I start?",
            "Optimise queries: narrow time range, use indexed fields, avoid wildcards at the start of search terms. Check ingestion rate — if above capacity, scale out indexers. Review dashboard queries — auto-refreshing wide-range searches are common culprits."),
        "backup_freq": ("How often should I back up SIEM configuration?",
            "Export SIEM configuration (detection rules, dashboards, saved searches) weekly via API or config-as-code (Splunk: `.conf` files in Git; Sentinel: ARM templates). Log data itself is protected by the SIEM's storage replication."),
        "restore": ("Can I restore deleted detection rules without a full SIEM restore?",
            "Yes — if rules are version-controlled in Git, restore with `git checkout`. For Splunk, rules in `$SPLUNK_HOME/etc/apps/` can be restored from backup. Microsoft Sentinel rules can be redeployed from exported ARM/Bicep templates."),
        "ts_link": "../troubleshooting/index.md",
    }),
    ("security/patch-compliance/operations", "patch-compliance", "Patch Compliance", {
        "version_check": ("How do I determine the current patch compliance status across my fleet?",
            "Run a compliance report from WSUS, SCCM, Ansible, or your vulnerability scanner (Tenable, Qualys). Target: critical patches applied within 72 hours, high within 7 days, medium within 30 days per standard patching SLAs."),
        "version_cmd": "SCCM: Run 'Compliance 1 - Overall Compliance' report",
        "default_setting": ("What is the recommended default patch deployment schedule?",
            "Weekly Patch Tuesday cycle for Windows. Monthly patching window for Linux. Emergency patch process (24-48 hours) for critical/exploited CVEs. Use deployment rings: dev → test → prod with 1-week gap between rings."),
        "enable_feature": ("How do I enable automatic patching for critical security updates?",
            "WSUS/SCCM: create an ADR (Automatic Deployment Rule) for Critical severity, auto-approve and deploy to test collection, then prod 7 days later. For Linux: configure `unattended-upgrades` (Ubuntu) or `dnf-automatic` (RHEL) for security-only updates."),
        "rolling_upgrade": ("How do I patch a fleet of 500+ servers without disrupting production?",
            "Group servers into maintenance windows by role (e.g., web tier Monday, app tier Tuesday, DB tier Wednesday). Use SCCM deployment rings. Exclude clustered nodes from simultaneous patching — patch one node at a time, verify, proceed."),
        "add_resource": ("What is the correct procedure to add a new server to the patching programme?",
            "Enrol in WSUS/SCCM. Assign to the correct collection (based on OS and role). Include in the appropriate maintenance window. Run an initial compliance scan to establish baseline. Schedule first patch cycle within 30 days."),
        "warning": ("Patch compliance report shows a server at 0% compliance for 30+ days. What does it mean?",
            "The server is either offline, not enrolled in patch management, or has a broken patch agent. Verify the server is reachable, the SCCM/WSUS agent is running, and the server is assigned to a collection. Investigate immediately for security risk."),
        "perf": ("Patch deployment is taking too long and missing maintenance windows — where do I start?",
            "Check SCCM distribution point reachability from target servers. Verify content pre-staged to branch DPs. Review client settings — download bandwidth limits may be too restrictive. Check SMSTS.log on clients for failure details."),
        "backup_freq": ("How long should I retain patch compliance records?",
            "Retain compliance reports for 12 months for standard audits, 3 years for SOX/PCI-DSS. Export SCCM compliance reports monthly. Store in your GRC tool with evidence timestamps. Provide to auditors on request."),
        "restore": ("Can I roll back a problematic patch without rebuilding the server?",
            "For Windows: `wusa /uninstall /kb:<KB_number>` or via Programs and Features. For SCCM: create a task sequence with the uninstall step. For Linux: `yum history undo <transaction_id>` or `apt-get remove --purge`. Test rollback in dev first."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/saml-configuration/operations", "saml-configuration", "SAML Configuration", {
        "version_check": ("How do I verify the SAML metadata version and validity?",
            "Check `validUntil` attribute in IdP metadata XML. Download fresh metadata from your IdP (e.g., Azure AD: `https://login.microsoftonline.com/<tenantid>/federationmetadata/2007-06/federationmetadata.xml`). Verify SP metadata is current in the IdP."),
        "version_cmd": "curl -s <idp-metadata-url> | grep validUntil",
        "default_setting": ("What is the default SAML assertion lifetime and when should it change?",
            "Default is typically 1 hour (3600 seconds) for the assertion validity period. Reduce to 5-15 minutes for high-security applications. Extend to 8 hours for low-sensitivity internal apps where user experience is the priority."),
        "enable_feature": ("How do I enable SAML attribute mapping for role-based access?",
            "In the IdP, configure claim rules to include group membership in the SAML assertion (e.g., `http://schemas.microsoft.com/ws/2008/06/identity/claims/groups`). In the SP, map the group claim to the application's role attribute. Test with a SAML tracer."),
        "rolling_upgrade": ("How do I rotate SAML signing certificates without breaking SSO?",
            "Add the new certificate to the IdP as a secondary signing cert. Update the SP's metadata with both certificates. Verify SSO works with both. Remove the old certificate from the IdP after the SP's certificate cache has expired (usually 24-48 hours)."),
        "add_resource": ("What is the correct procedure to add a new SP to an existing SAML IdP?",
            "Obtain the SP's metadata XML. Add as an Enterprise Application (Azure AD) or SAML SP (ADFS/Okta). Configure ACS URL, Entity ID, and attribute mapping. Test with SAML tracer (Chrome extension). Verify NameID format matches SP expectations."),
        "warning": ("SAML SSO fails with 'Response has wrong InResponseTo'. What does it mean?",
            "The SP received a SAML response for a different request (replay or session mismatch). Usually caused by load balancers breaking sticky sessions. Ensure session affinity is configured, or the SP uses a distributed session store. Check clock skew (must be <5 minutes)."),
        "perf": ("SAML SSO login takes >5 seconds — where do I start?",
            "Check IdP response time. Verify SP-to-IdP network latency. Review SAML assertion size (large group claims inflate assertion and parsing time). Check if SP is doing synchronous LDAP lookup on each SSO event."),
        "backup_freq": ("How often should I back up SAML configuration?",
            "Export SP metadata and IdP configuration weekly. Store in version control. Include claim rules, attribute mappings, and certificate thumbprints. Before rotating certificates, always back up the current IdP/SP configuration."),
        "restore": ("Can I restore a broken SAML integration without affecting other SP integrations?",
            "Yes — each SP integration is independent in Azure AD/Okta/ADFS. Remove the broken app registration and re-add it using the backed-up SP metadata. Other SP integrations are not affected."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/security-audit/operations", "security-audit", "Security Audit", {
        "version_check": ("How do I determine which security audit was most recently completed?",
            "Check your GRC tool audit log or audit register. For ISO 27001, the last surveillance audit date is on the certificate. Internal audit schedule should be in the GRC tool under Audit Management → Audit Calendar."),
        "version_cmd": "GRC tool → Audit Management → Completed Audits",
        "default_setting": ("What is the standard security audit frequency?",
            "ISO 27001: annual external surveillance + 3-year recertification. SOC 2: annual Type II audit (12-month observation period). Internal audits: quarterly for high-risk areas, annual for standard controls. Penetration testing: annual minimum, after significant changes."),
        "enable_feature": ("How do I enable continuous audit evidence collection?",
            "Integrate your SIEM, vulnerability scanner, and ITSM tool with your GRC platform via API. Configure automated evidence collection for technical controls (patch compliance, access reviews, firewall rules). Reduces manual evidence gathering by 60-70%."),
        "rolling_upgrade": ("How do I expand the audit scope to include a newly acquired business unit?",
            "Conduct a gap assessment of the new unit's controls against your existing framework. Assign control owners. Include the unit in the next internal audit cycle. Notify your external auditor of scope change before the next audit engagement starts."),
        "add_resource": ("What is the correct procedure to track a new audit finding?",
            "Log in GRC tool: finding description, severity, affected control, root cause, remediation owner, and target date. Link to evidence. Track remediation progress weekly for critical findings. Close only when evidence of remediation is accepted by the audit team."),
        "warning": ("External auditor raises a 'Repeat Finding'. What does it mean?",
            "The same deficiency was identified in a previous audit and not fully remediated. Repeat findings are serious — they indicate inadequate remediation or systemic process weakness. Root cause analysis is mandatory; escalate to CISO."),
        "perf": ("Audit preparation is consuming too much team time — where do I start?",
            "Implement continuous control monitoring (CCM) to pre-collect evidence. Create an audit request portal in ServiceNow/Jira for auditors. Standardise evidence formats. Designate a single audit coordinator per business unit."),
        "backup_freq": ("How long should I retain audit records?",
            "Audit reports: indefinitely (legal record). Evidence: per framework requirement (SOX: 7 years, PCI-DSS: 12 months online + 12 months offline). Store in an audit repository with access controls and tamper protection."),
        "restore": ("Can I dispute an audit finding if I believe the evidence is incorrect?",
            "Yes — submit a formal management response with counter-evidence during the draft report review period. Auditors must consider management responses before issuing the final report. Document the dispute in your GRC tool regardless of outcome."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/security-monitoring/operations", "security-monitoring", "Security Monitoring", {
        "version_check": ("How do I check the version and coverage of security monitoring tools?",
            "Check SIEM version in admin console. Verify EDR agent coverage: target 100% of managed endpoints. Review log source inventory in SIEM — identify gaps. Check detection rule last-updated dates (stale rules miss new TTPs)."),
        "version_cmd": "SIEM admin console → System Health → Version",
        "default_setting": ("What is the default alert severity threshold and when should it change?",
            "Most SIEMs default to alerting on Medium and above. Tune to High/Critical only during initial deployment to reduce noise. Once tuned, lower threshold back to Medium. Never suppress Low severity silently — log them for trend analysis."),
        "enable_feature": ("How do I enable threat intelligence feed integration in the SIEM?",
            "Most SIEMs support TAXII/STIX feeds. Configure in SIEM → Threat Intelligence → Add Feed. Use feeds from CISA, ISAC, or commercial providers (Recorded Future, CrowdStrike). Correlate IOCs against log data in detection rules."),
        "rolling_upgrade": ("How do I upgrade detection rules to cover new MITRE ATT&CK techniques?",
            "Map current rules to ATT&CK framework. Identify coverage gaps. Source new rules from Sigma project or SIEM vendor content packs. Test in a staging SIEM before production deployment. Review for false positive rate before enabling."),
        "add_resource": ("What is the correct procedure to add a new monitored asset?",
            "Install log forwarding agent (Splunk UF, Elastic Agent, Azure Monitor Agent). Configure to forward relevant log sources (security, application, system). Create asset entry in SIEM asset inventory. Verify log ingestion within 24 hours."),
        "warning": ("SIEM shows a spike in 'Logon Failure' events from a single source. What does it mean?",
            "Potential brute-force or password spray attack in progress. Immediately check the source IP — if external, block at the firewall. If internal, investigate the source host for malware. Lock the targeted accounts if attack is ongoing."),
        "perf": ("SIEM alert queue has thousands of unreviewed alerts — where do I start?",
            "Triage by severity (Critical first). Identify top alert-generating rules and tune false positives. Implement automated enrichment/disposition for known-benign patterns. Consider SOAR for auto-closing low-confidence, high-volume alerts."),
        "backup_freq": ("How often should I back up SIEM detection rules and dashboards?",
            "Export to Git after every rule change. Automate via SIEM API on a weekly schedule. Rules-as-code approach (Sigma, Terraform) provides version history automatically. Test re-import from backup quarterly."),
        "restore": ("Can I restore accidentally deleted detection rules without a full SIEM restore?",
            "Yes — from Git: `git checkout HEAD~1 -- rules/`. For Splunk, restore from `$SPLUNK_HOME/etc/apps/` backup. For Sentinel, redeploy ARM template. This is why rules-as-code is essential for any production SIEM."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/venafi/operations", "venafi", "Venafi Trust Protection Platform", {
        "version_check": ("What Venafi version is recommended for new deployments?",
            "Venafi TPP 23.4+ or Venafi as a Service (cloud) for new deployments. Check TPP version via Administration → About Venafi. Keep within 2 major versions for support and security patches."),
        "version_cmd": "Administration → About Venafi",
        "default_setting": ("What is the default certificate discovery schedule and when should it change?",
            "Discovery is manual by default. Enable scheduled network scanning (TPP → Discovery → Network Scanning) weekly for your certificate inventory. Increase to daily for large, dynamic environments or when approaching audit season."),
        "enable_feature": ("How do I enable Venafi automated certificate renewal?",
            "Configure Certificate Management → Auto-Renewal: set renewal threshold (e.g., 30 days before expiry). Install the Venafi Agent on servers for automated replacement. Configure application-specific renewal workflows (IIS, Apache, F5)."),
        "rolling_upgrade": ("How do I upgrade Venafi TPP without disrupting certificate operations?",
            "Back up TPP database and config. Upgrade in a maintenance window. Policy-based renewals queue during upgrade. Post-upgrade, verify engine health and resume processing. Rolling upgrades across nodes are supported in clustered deployments."),
        "add_resource": ("What is the correct procedure to add a new CA to Venafi?",
            "In TPP: Administration → CA Templates → Add. Provide CA type (ADCS, DigiCert, Entrust), connection parameters, and credentials. Test with a certificate request before adding to production policy folders."),
        "warning": ("Venafi shows 'Certificate Expiring in 7 days — No Renewal Pending'. What does it mean?",
            "Auto-renewal failed or was not configured for this certificate. Manually renew via TPP or the certificate owner's workflow immediately. Investigate why auto-renewal did not trigger — check policy folder settings and agent connectivity."),
        "perf": ("Venafi discovery scan is not completing within the scheduled window — where do I start?",
            "Reduce scan scope (narrow IP range, specific ports). Increase scanner thread count in Discovery settings. Deploy additional distributed engines close to large subnets. Schedule scans during off-peak hours."),
        "backup_freq": ("How often should I back up Venafi TPP?",
            "Daily database backup (SQL Server). Weekly config export via `VEDiag`. The TPP database contains all certificate metadata, keys, and policy — protect it at least as carefully as a CA database."),
        "restore": ("Can I restore a single certificate and private key from Venafi without a full restore?",
            "Yes — in TPP, navigate to the certificate object → Private Key → Download. Venafi stores private keys escrow if configured. If keys are not escrowed, a new key pair must be generated and the certificate reissued."),
        "ts_link": "../../troubleshooting/index.md",
    }),
    ("security/vulnerability-management/operations", "vulnerability-management", "Vulnerability Management", {
        "version_check": ("How do I check the current vulnerability scanner version and plugin currency?",
            "Tenable.sc: Admin → About; Nessus: Settings → About. Check plugin feed date: should be within 24 hours. Qualys: VM → Appliances → Last Update. Outdated plugins miss new CVEs."),
        "version_cmd": "Tenable.sc: Admin → About → Version & Plugin Feed Date",
        "default_setting": ("What is the default scan frequency and when should it change?",
            "Weekly internal scans and monthly external scans are a common baseline. Increase internal scan frequency to daily for internet-facing or critical assets. Immediately re-scan after patching to verify remediation."),
        "enable_feature": ("How do I enable credentialed scanning for more accurate results?",
            "Configure a scan credential (Windows: domain admin service account; Linux: SSH key with sudo). In Tenable: Credentials → Add. Run a credentialed scan — this finds 2-3x more vulnerabilities than unauthenticated scans (local software, registry checks)."),
        "rolling_upgrade": ("How do I upgrade the vulnerability scanner without creating scan gaps?",
            "Schedule upgrade outside scan windows. For Tenable.sc, upgrade the Security Center appliance, then Nessus scanners one at a time. Scans continue from active scanners during the upgrade. Verify plugin currency post-upgrade."),
        "add_resource": ("What is the correct procedure to add a new network segment to scan scope?",
            "Add the IP range to a scan policy. Place a scanner with network access to the segment. Run a discovery scan first to enumerate live hosts. Then run a full vulnerability scan. Add new assets to your asset tracking tool."),
        "warning": ("Scanner shows many 'Info' level findings on production servers. What does it mean?",
            "Info findings are not vulnerabilities — they are informational (open ports, service banners). Filter them from remediation reports. Focus on Critical/High CVEs first. Review Info findings during quarterly baseline assessments only."),
        "perf": ("Scans are causing performance impact on production servers — where do I start?",
            "Reduce scan concurrency (scanner threads). Schedule scans during off-peak hours. Use 'Safe Checks' mode in Nessus (disables potentially disruptive checks). Exclude database servers from aggressive scan policies."),
        "backup_freq": ("How long should I retain vulnerability scan data?",
            "Retain scan reports for 12 months minimum (PCI-DSS requirement). Archive trend data for 3 years for programme metrics. Export scan results to your GRC tool for evidence correlation with patch compliance records."),
        "restore": ("Can I revert a false-positive acceptance if re-scanned vulnerability is real?",
            "Yes — in Tenable.sc/Qualys, accepted risks can be reopened. Navigate to Accepted Risks → find the entry → Reopen. Investigate whether the accepted risk was valid — re-evaluate original justification if the vulnerability appears again."),
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

print(f"Created {len(created_files)} FAQ files, {len(created_svgs)} SVGs (batch 2)")
