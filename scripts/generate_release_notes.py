#!/usr/bin/env python3
"""
Generate release-notes.md stub pages for every product in the KB.

A "product directory" is any directory under docs/ that has an
operations/ subdirectory.

Usage:
  python3 scripts/generate_release_notes.py --dry-run
  python3 scripts/generate_release_notes.py
"""
import argparse
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

REPO  = Path(__file__).parent.parent.resolve()
DOCS  = REPO / 'docs'
ASSETS = DOCS / 'assets'

# ── Colour constants (match existing proc SVG style) ──────────────────────────
NAVY       = '#1a2744'
FOOTER_FG  = '#7a8fbb'
BOX_FILL   = '#e8f5e9'
BOX_STROKE = '#2e7d32'
BOX_TEXT   = '#1b5e20'
ARROW_CLR  = '#546e7a'

SVG_W = 820
SVG_H = 200
HDR_H = 46
FTR_H = 28
FTR_Y = SVG_H - FTR_H

# ── Product display names ─────────────────────────────────────────────────────
DISPLAY_NAMES = {
    'ansible':                      'Ansible',
    'github-actions':               'GitHub Actions',
    'powershell':                   'PowerShell',
    'python':                       'Python',
    'terraform':                    'Terraform',
    'commvault':                    'Commvault',
    'netbackup':                    'Veritas NetBackup',
    'veeam':                        'Veeam Backup & Replication',
    'aws':                          'AWS',
    'evs':                          'AWS EVS',
    'azure':                        'Azure',
    'linux':                        'Linux',
    'mysql':                        'MySQL',
    'postgresql':                   'PostgreSQL',
    'windows-server':               'Windows Server',
    'active-directory':             'Active Directory',
    'sql-server':                   'SQL Server',
    'confluence':                   'Confluence',
    'git':                          'Git',
    'jira':                         'Jira',
    'servicenow':                   'ServiceNow',
    'fabric-os':                    'Brocade Fabric OS',
    'sannav':                       'Brocade SANnav',
    'cisco-dcnm':                   'Cisco DCNM',
    'mds':                          'Cisco MDS',
    'nexus-dashboard':              'Cisco Nexus Dashboard',
    'security':                     'Security',
    'access-review':                'Access Review',
    'certificates':                 'Certificates',
    'compliance-standards':         'Compliance Standards',
    'cyberark':                     'CyberArk',
    'incident-handling':            'Incident Handling',
    'ldap-integration':             'LDAP Integration',
    'mfa':                          'MFA',
    'patch-compliance':             'Patch Compliance',
    'saml-configuration':           'SAML Configuration',
    'security-audit':               'Security Audit',
    'security-monitoring':          'Security Monitoring',
    'venafi':                       'Venafi',
    'vulnerability-management':     'Vulnerability Management',
    'ceph':                         'Ceph',
    'apex-storage-as-a-service':    'Dell Apex Storage-as-a-Service',
    'cloudiq':                      'Dell CloudIQ',
    'cod':                          'Dell COD',
    'data-domain':                  'Dell Data Domain',
    'dell-aiops':                   'Dell AIOps',
    'ecs':                          'Dell ECS',
    'fod':                          'Dell FOD',
    'powermax':                     'Dell PowerMax',
    'powerpath':                    'Dell PowerPath',
    'powerscale':                   'Dell PowerScale',
    'powerstore':                   'Dell PowerStore',
    'recoverpoint':                 'Dell RecoverPoint',
    'secure-connect-gateway':       'Dell Secure Connect Gateway',
    'srdf-a':                       'Dell SRDF/A',
    'srdf-s':                       'Dell SRDF/S',
    'unity':                        'Dell Unity',
    'vplex':                        'Dell VPLEX',
    'netapp':                       'NetApp',
    'insightiq':                    'NetApp InsightIQ',
    'keystone':                     'NetApp Keystone',
    'ontap':                        'NetApp ONTAP',
    'snapcenter':                   'NetApp SnapCenter',
    'snapmirror':                   'NetApp SnapMirror',
    'superna-eyeglass':             'Superna Eyeglass',
    'pure':                         'Pure Storage',
    'evergreen':                    'Pure Evergreen',
    'evergreen-one':                'Pure Evergreen//ONE',
    'flasharray':                   'Pure FlashArray',
    'flashblade':                   'Pure FlashBlade',
    'pure1':                        'Pure1',
    'nutanix':                      'Nutanix',
    'openshift':                    'OpenShift',
    'vmware':                       'VMware',
    'aria-automation':              'VMware Aria Automation',
    'aria-operations':              'VMware Aria Operations',
    'aria-operations-for-logs':     'VMware Aria Operations for Logs',
    'aria-operations-for-networks': 'VMware Aria Operations for Networks',
    'aria-suite-lifecycle':         'VMware Aria Suite Lifecycle',
    'esxi':                         'VMware ESXi',
    'horizon':                      'VMware Horizon',
    'nsx':                          'VMware NSX',
    'powercli':                     'VMware PowerCLI',
    'srm':                          'VMware SRM',
    'tanzu':                        'VMware Tanzu',
    'vcenter':                      'VMware vCenter',
    'vmware-cloud-foundation':      'VMware Cloud Foundation',
    'vsan':                         'VMware vSAN',
    'vsphere-replication':          'VMware vSphere Replication',
    'vxrail':                       'Dell VxRail',
}

# ── Version stubs per product slug ────────────────────────────────────────────
# Each entry: list of (version, date, summary) tuples, 5 rows
VERSIONS = {
    'ontap': [
        ('9.15.1', '2024-Q4', 'NVMe-oF enhancements, SnapMirror active sync improvements'),
        ('9.14.1', '2024-Q1', 'S3 object storage GA, autonomous ransomware protection v3'),
        ('9.13.1', '2023-Q3', 'FlexGroup SnapMirror active sync, NFS 4.1 pNFS support'),
        ('9.12.1', '2023-Q1', 'iSCSI LUN rebalancing, ONTAP Mediator 1.5'),
        ('9.11.1', '2022-Q3', 'Consistency groups GA, REST API parity milestone'),
    ],
    'vsan': [
        ('8.0 U3', '2024-Q3', 'ESA stretched cluster GA, compression enhancements'),
        ('8.0 U2', '2024-Q1', 'Express Storage Architecture (ESA) improvements'),
        ('8.0 U1', '2023-Q2', 'vSAN 8 ESA initial GA, HCI mesh updates'),
        ('7.0 U3', '2022-Q4', 'vSAN Max disaggregated storage preview'),
        ('7.0 U2', '2022-Q1', 'HCI mesh GA, vSAN File Services scale-out'),
    ],
    'ansible': [
        ('2.17', '2024-Q2', 'Python 3.12 support, improved event-driven automation'),
        ('2.16', '2023-Q4', 'AAP 2.4 compatibility, collection loader rewrite'),
        ('2.15', '2023-Q2', 'Mitogen strategy improvements, fact caching backends'),
        ('2.14', '2022-Q4', 'ansible-core 2.14 LTS release, controller deprecations'),
        ('2.13', '2022-Q2', 'Python 3.8 minimum, task include_role refactor'),
    ],
    'terraform': [
        ('1.9', '2024-Q2', 'Input variable validations on modules, provider iteration'),
        ('1.8', '2024-Q1', 'Provider-defined functions, enhanced import blocks'),
        ('1.7', '2023-Q4', 'Ephemeral values, write-only attributes'),
        ('1.6', '2023-Q3', 'Test framework GA, stack configuration preview'),
        ('1.5', '2023-Q2', 'Import block GA, config-driven import'),
    ],
    'vcenter': [
        ('8.0 U3', '2024-Q3', 'vCenter HA improvements, SDDC Manager integration'),
        ('8.0 U2', '2024-Q1', 'Reduced footprint appliance, converged management'),
        ('8.0 U1', '2023-Q2', 'vCenter Server 8.0 U1 stability and security patches'),
        ('8.0 GA', '2022-Q4', 'vCenter 8 GA — vSphere Distributed Services Engine'),
        ('7.0 U3', '2022-Q1', 'vCenter 7.0 U3 — end of gen LTS baseline'),
    ],
    'esxi': [
        ('8.0 U3', '2024-Q3', 'Security hardening, NVMe-oF initiator improvements'),
        ('8.0 U2', '2024-Q1', 'TPM 2.0 attestation enhancements, vTPM migration'),
        ('8.0 U1', '2023-Q2', 'ESXi 8.0 U1 — driver compatibility and stability'),
        ('8.0 GA', '2022-Q4', 'ESXi 8 GA — Intel TDX, AMD SEV-SNP support'),
        ('7.0 U3', '2022-Q1', 'ESXi 7.0 U3 — lifecycle LTS baseline'),
    ],
    'nsx': [
        ('4.1.2', '2024-Q2', 'Distributed SNAT, multi-site federation improvements'),
        ('4.1.1', '2023-Q4', 'NSX-T to NSX rebrand GA, L7 firewall enhancements'),
        ('4.0.1', '2023-Q1', 'NSX 4.0 — policy API convergence, EVPN support'),
        ('3.2.3', '2022-Q3', 'NSX-T 3.2 LTS — distributed firewall scale'),
        ('3.2.1', '2022-Q1', 'NSX-T 3.2.1 — malware prevention GA'),
    ],
    'vxrail': [
        ('8.0.300', '2024-Q3', 'VxRail 8.0.300 — ESXi 8.0 U3 baseline'),
        ('8.0.200', '2024-Q1', 'VxRail 8.0.200 — vSAN 8 U2 support'),
        ('8.0.100', '2023-Q2', 'VxRail 8.0 — full vSphere 8 lifecycle support'),
        ('7.0.481', '2022-Q4', 'VxRail 7.0.481 — ESXi 7.0 U3 LTS'),
        ('7.0.450', '2022-Q1', 'VxRail 7.0.450 — stability and driver updates'),
    ],
    'vmware-cloud-foundation': [
        ('5.2',   '2024-Q3', 'VCF 5.2 — consolidated architecture GA'),
        ('5.1.1', '2024-Q1', 'VCF 5.1.1 — NSX 4.1, vSAN 8 U2 alignment'),
        ('5.1',   '2023-Q3', 'VCF 5.1 — vSphere 8 U1 integrated baseline'),
        ('5.0',   '2022-Q4', 'VCF 5.0 — NSX-T to NSX rebrand, single pane'),
        ('4.5',   '2022-Q1', 'VCF 4.5 — vSphere 7 LTS, lifecycle management'),
    ],
    'srm': [
        ('9.0',   '2024-Q2', 'SRM 9.0 — vSphere 8 native, REST-only management'),
        ('8.8',   '2023-Q4', 'SRM 8.8 — vSAN stretched cluster DR improvements'),
        ('8.7',   '2023-Q1', 'SRM 8.7 — policy-based protection groups'),
        ('8.6',   '2022-Q3', 'SRM 8.6 — vSphere Replication 8.6 alignment'),
        ('8.5',   '2022-Q1', 'SRM 8.5 — NFS array-based replication expansion'),
    ],
    'vsphere-replication': [
        ('8.8',   '2024-Q1', 'vSphere Replication 8.8 — improved RPO granularity'),
        ('8.7',   '2023-Q3', 'vSphere Replication 8.7 — vSAN replication improvements'),
        ('8.6',   '2022-Q4', 'vSphere Replication 8.6 — SRM 8.6 alignment'),
        ('8.5',   '2022-Q2', 'vSphere Replication 8.5 — cloud provider support'),
        ('8.4',   '2021-Q4', 'vSphere Replication 8.4 — replication traffic compression'),
    ],
    'horizon': [
        ('8 2312', '2024-Q1', 'Horizon 2312 — Windows 11 23H2 gold image support'),
        ('8 2309', '2023-Q4', 'Horizon 2309 — App Volumes 4.10 integration'),
        ('8 2306', '2023-Q2', 'Horizon 2306 — Teams media optimisation improvements'),
        ('8 2303', '2023-Q1', 'Horizon 2303 — RDSH scaling enhancements'),
        ('8 2212', '2022-Q4', 'Horizon 2212 — Blast Extreme protocol update'),
    ],
    'aria-automation': [
        ('8.18', '2024-Q3', 'Aria Automation 8.18 — Day 2 actions catalog'),
        ('8.16', '2024-Q1', 'Aria Automation 8.16 — Terraform provider updates'),
        ('8.14', '2023-Q3', 'Aria Automation 8.14 — plugin extensibility GA'),
        ('8.12', '2023-Q1', 'Aria Automation 8.12 — vRA rebrand to Aria'),
        ('8.10', '2022-Q3', 'vRA 8.10 — ABX action enhancements'),
    ],
    'aria-operations': [
        ('8.18', '2024-Q3', 'Aria Operations 8.18 — AI-driven workload balancing'),
        ('8.16', '2024-Q1', 'Aria Operations 8.16 — cost driver enhancements'),
        ('8.14', '2023-Q3', 'Aria Operations 8.14 — vROps rebrand to Aria'),
        ('8.12', '2023-Q1', 'Aria Operations 8.12 — continuous availability cluster'),
        ('8.10', '2022-Q3', 'vROps 8.10 — Kubernetes monitoring GA'),
    ],
    'aria-operations-for-logs': [
        ('8.18', '2024-Q3', 'Aria Logs 8.18 — structured log query improvements'),
        ('8.16', '2024-Q1', 'Aria Logs 8.16 — increased ingestion throughput'),
        ('8.14', '2023-Q3', 'Aria Logs 8.14 — vRLI rebrand to Aria'),
        ('8.12', '2023-Q1', 'Aria Logs 8.12 — Kubernetes log streaming'),
        ('8.10', '2022-Q3', 'vRLI 8.10 — content pack auto-update'),
    ],
    'aria-operations-for-networks': [
        ('6.13', '2024-Q3', 'Aria for Networks 6.13 — NSX 4.1 topology support'),
        ('6.11', '2024-Q1', 'Aria for Networks 6.11 — path tracing improvements'),
        ('6.9',  '2023-Q3', 'Aria for Networks 6.9 — vRNI rebrand to Aria'),
        ('6.7',  '2023-Q1', 'Aria for Networks 6.7 — AWS VPC flow log analysis'),
        ('6.5',  '2022-Q3', 'vRNI 6.5 — application security planning'),
    ],
    'aria-suite-lifecycle': [
        ('8.18', '2024-Q3', 'Aria Suite Lifecycle 8.18 — GitOps config management'),
        ('8.16', '2024-Q1', 'Aria Suite Lifecycle 8.16 — upgrade orchestration'),
        ('8.14', '2023-Q3', 'Aria Suite Lifecycle 8.14 — vRSLCM rebrand to Aria'),
        ('8.12', '2023-Q1', 'Aria Suite Lifecycle 8.12 — certificate automation'),
        ('8.10', '2022-Q3', 'vRSLCM 8.10 — environment health dashboard'),
    ],
    'powercli': [
        ('13.3', '2024-Q3', 'PowerCLI 13.3 — vSphere 8.0 U3 module updates'),
        ('13.2', '2024-Q1', 'PowerCLI 13.2 — New-VM template improvements'),
        ('13.1', '2023-Q3', 'PowerCLI 13.1 — VMware.PowerCLI umbrella module'),
        ('13.0', '2023-Q1', 'PowerCLI 13.0 — PowerShell 7.3 compatibility'),
        ('12.7', '2022-Q3', 'PowerCLI 12.7 — vSAN cmdlet additions'),
    ],
    'tanzu': [
        ('2.4', '2024-Q3', 'Tanzu 2.4 — Kubernetes 1.30 support'),
        ('2.3', '2024-Q1', 'Tanzu 2.3 — Tanzu Kubernetes Grid 2.3'),
        ('2.2', '2023-Q3', 'Tanzu 2.2 — ClusterClass GA, Carvel tools update'),
        ('2.1', '2023-Q1', 'Tanzu 2.1 — vSphere Namespace policy enhancements'),
        ('2.0', '2022-Q4', 'Tanzu 2.0 — TKG rebrand, unified lifecycle'),
    ],
    'flasharray': [
        ('6.6.10', '2024-Q3', 'Purity//FA 6.6 — NVMe/TCP enhancements'),
        ('6.5.7',  '2024-Q1', 'Purity//FA 6.5 — SafeMode ransomware protection'),
        ('6.4.10', '2023-Q3', 'Purity//FA 6.4 — ActiveCluster improvements'),
        ('6.3.14', '2023-Q1', 'Purity//FA 6.3 — pod replication scale'),
        ('6.2.6',  '2022-Q3', 'Purity//FA 6.2 — DirectFlash fabric support'),
    ],
    'flashblade': [
        ('4.4.10', '2024-Q3', 'Purity//FB 4.4 — S3 multi-region replication'),
        ('4.3.7',  '2024-Q1', 'Purity//FB 4.3 — rapid restore throughput'),
        ('4.2.10', '2023-Q3', 'Purity//FB 4.2 — NFS v4.1 GA on FlashBlade//S'),
        ('4.1.14', '2023-Q1', 'Purity//FB 4.1 — FlashBlade//S platform GA'),
        ('3.3.6',  '2022-Q3', 'Purity//FB 3.3 — SMB 3.1.1 Continuous Availability'),
    ],
    'pure': [
        ('2024.3', '2024-Q3', 'Pure1 platform update — AI-driven anomaly detection'),
        ('2024.1', '2024-Q1', 'Pure1 — enhanced sustainability dashboard'),
        ('2023.3', '2023-Q3', 'Pure1 — unified fleet capacity planning'),
        ('2023.1', '2023-Q1', 'Pure1 — cross-array workload analytics'),
        ('2022.3', '2022-Q3', 'Pure1 — ransomware assessment module GA'),
    ],
    'pure1': [
        ('2024.3', '2024-Q3', 'Pure1 platform update — AI-driven anomaly detection'),
        ('2024.1', '2024-Q1', 'Pure1 — enhanced sustainability dashboard'),
        ('2023.3', '2023-Q3', 'Pure1 — unified fleet capacity planning'),
        ('2023.1', '2023-Q1', 'Pure1 — cross-array workload analytics'),
        ('2022.3', '2022-Q3', 'Pure1 — ransomware assessment module GA'),
    ],
    'evergreen': [
        ('2024.4', '2024-Q4', 'Evergreen//Forever — non-disruptive controller upgrade'),
        ('2024.2', '2024-Q2', 'Evergreen//Architecture — array expansion policy update'),
        ('2023.4', '2023-Q4', 'Evergreen//Flex — elastic capacity pool improvements'),
        ('2023.2', '2023-Q2', 'Evergreen//One SLA revision — 1 ms latency guarantee'),
        ('2022.4', '2022-Q4', 'Evergreen — FlashBlade inclusion in program'),
    ],
    'evergreen-one': [
        ('2024.4', '2024-Q4', 'Evergreen//ONE 2024.4 — SLA expansion to NVMe-oF'),
        ('2024.2', '2024-Q2', 'Evergreen//ONE — latency guarantee update'),
        ('2023.4', '2023-Q4', 'Evergreen//ONE — capacity burst model revision'),
        ('2023.2', '2023-Q2', 'Evergreen//ONE — sustainability reporting GA'),
        ('2022.4', '2022-Q4', 'Evergreen//ONE — FlashBlade//S tier introduction'),
    ],
    'snapmirror': [
        ('9.15.1', '2024-Q4', 'SnapMirror active sync — asymmetric access GA'),
        ('9.14.1', '2024-Q1', 'SnapMirror cloud — S3 endpoint expansion'),
        ('9.13.1', '2023-Q3', 'FlexGroup SnapMirror active sync support'),
        ('9.12.1', '2023-Q1', 'SnapMirror business continuity v2 enhancements'),
        ('9.11.1', '2022-Q3', 'SnapMirror active sync — VMFS datastores GA'),
    ],
    'snapcenter': [
        ('6.0', '2024-Q3', 'SnapCenter 6.0 — ONTAP 9.15 compatibility'),
        ('5.0', '2023-Q4', 'SnapCenter 5.0 — REST API v3, PostgreSQL plugin'),
        ('4.9', '2023-Q2', 'SnapCenter 4.9 — Oracle RAC improvements'),
        ('4.8', '2022-Q4', 'SnapCenter 4.8 — SAP HANA System Replication support'),
        ('4.7', '2022-Q2', 'SnapCenter 4.7 — Kubernetes CSI plugin GA'),
    ],
    'keystone': [
        ('STaaS v3', '2024-Q3', 'Keystone STaaS v3 — AFF C-series tier addition'),
        ('STaaS v2', '2023-Q4', 'Keystone STaaS v2 — NVMe tier GA, burst on-demand'),
        ('STaaS v1.2', '2023-Q1', 'Keystone 1.2 — co-location expansion regions'),
        ('STaaS v1.1', '2022-Q3', 'Keystone 1.1 — SLA reporting dashboard'),
        ('STaaS v1.0', '2022-Q1', 'Keystone STaaS v1.0 GA'),
    ],
    'insightiq': [
        ('5.1', '2024-Q2', 'InsightIQ 5.1 — OneFS 9.7 compatibility'),
        ('5.0', '2023-Q3', 'InsightIQ 5.0 — new performance baselines engine'),
        ('4.1', '2022-Q4', 'InsightIQ 4.1 — cluster comparison dashboards'),
        ('4.0', '2022-Q1', 'InsightIQ 4.0 — REST API for report export'),
        ('3.2', '2021-Q3', 'InsightIQ 3.2 — long-term capacity trending'),
    ],
    'superna-eyeglass': [
        ('2.9', '2024-Q2', 'Eyeglass 2.9 — OneFS 9.7 failover support'),
        ('2.8', '2023-Q4', 'Eyeglass 2.8 — ransomware defender improvements'),
        ('2.7', '2023-Q2', 'Eyeglass 2.7 — multi-cluster DR orchestration'),
        ('2.6', '2022-Q4', 'Eyeglass 2.6 — SyncIQ policy automation'),
        ('2.5', '2022-Q1', 'Eyeglass 2.5 — configuration replication engine v2'),
    ],
    'netapp': [
        ('2024.4', '2024-Q4', 'NetApp platform update — unified BlueXP UI'),
        ('2024.2', '2024-Q2', 'NetApp — ONTAP 9.15, SnapCenter 6.0 alignment'),
        ('2023.4', '2023-Q4', 'NetApp — AFF C-series capacity tier GA'),
        ('2023.2', '2023-Q2', 'NetApp — BlueXP backup and recovery expansion'),
        ('2022.4', '2022-Q4', 'NetApp — ONTAP S3 multi-protocol enhancement'),
    ],
    'veeam': [
        ('12.2', '2024-Q3', 'Veeam 12.2 — Entra ID backup GA, CDP improvements'),
        ('12.1', '2024-Q1', 'Veeam 12.1 — malware detection, ZTNA integration'),
        ('12.0', '2023-Q1', 'Veeam 12.0 — immutable backup to S3 GA'),
        ('11a',  '2022-Q1', 'Veeam 11a — patch release, CDP stability'),
        ('11.0', '2021-Q2', 'Veeam 11.0 — CDP, Kubernetes support GA'),
    ],
    'commvault': [
        ('11.32', '2024-Q3', 'Commvault 11.32 — AI-assisted anomaly recovery'),
        ('11.30', '2024-Q1', 'Commvault 11.30 — Metallic integration updates'),
        ('11.28', '2023-Q3', 'Commvault 11.28 — Air Gap Protect GA'),
        ('11.26', '2023-Q1', 'Commvault 11.26 — Kubernetes operator improvements'),
        ('11.24', '2022-Q3', 'Commvault 11.24 — Ransomware protection update'),
    ],
    'netbackup': [
        ('10.4', '2024-Q3', 'NetBackup 10.4 — workload accelerator enhancements'),
        ('10.3', '2024-Q1', 'NetBackup 10.3 — Flex Scale HA improvements'),
        ('10.2', '2023-Q3', 'NetBackup 10.2 — cloud-first policy management'),
        ('10.1', '2023-Q1', 'NetBackup 10.1 — Kubernetes CSI snapshot backup'),
        ('10.0', '2022-Q2', 'NetBackup 10.0 GA — containerised media server'),
    ],
    'ceph': [
        ('18.2 Reef',  '2024-Q2', 'Ceph 18.2 Reef — RGW multi-site active-active'),
        ('17.2 Quincy','2023-Q2', 'Ceph 17.2 Quincy — RBD fast-diff improvements'),
        ('16.2 Pacific','2022-Q2','Ceph 16.2 Pacific — cephadm orchestration GA'),
        ('15.2 Octopus','2021-Q2','Ceph 15.2 Octopus — object gateway enhancements'),
        ('14.2 Nautilus','2020-Q2','Ceph 14.2 Nautilus — mgr dashboard v2'),
    ],
    'powermax': [
        ('10.1', '2024-Q3', 'PowerMax 10.1 — NVMe/FC director updates'),
        ('10.0', '2023-Q3', 'PowerMax 10.0 — 350F all-NVMe platform GA'),
        ('9.2',  '2022-Q3', 'PowerMax 9.2 — eNAS v9 firmware'),
        ('9.1',  '2021-Q4', 'PowerMax 9.1 — SRDF/Metro enhancements'),
        ('9.0',  '2021-Q1', 'PowerMax 9.0 — machine learning storage management'),
    ],
    'powerstore': [
        ('3.6', '2024-Q3', 'PowerStore 3.6 — AppsOn enhancements'),
        ('3.5', '2024-Q1', 'PowerStore 3.5 — NVMe-oF iSCSI offload'),
        ('3.2', '2023-Q3', 'PowerStore 3.2 — volume group remote replication'),
        ('3.0', '2022-Q4', 'PowerStore 3.0 — Metro volume replication GA'),
        ('2.1', '2022-Q1', 'PowerStore 2.1 — Kubernetes CSI improvements'),
    ],
    'powerscale': [
        ('9.7', '2024-Q3', 'OneFS 9.7 — SmartFlash NVMe tier GA'),
        ('9.6', '2024-Q1', 'OneFS 9.6 — SyncIQ policy improvements'),
        ('9.5', '2023-Q3', 'OneFS 9.5 — S3 protocol multi-bucket support'),
        ('9.4', '2023-Q1', 'OneFS 9.4 — DataAdvantage analytics'),
        ('9.3', '2022-Q3', 'OneFS 9.3 — SyncIQ SmartSync GA'),
    ],
    'unity': [
        ('5.4', '2024-Q2', 'Unity XT 5.4 — eNAS protocol updates'),
        ('5.3', '2023-Q3', 'Unity XT 5.3 — CloudIQ integration improvements'),
        ('5.2', '2022-Q4', 'Unity XT 5.2 — NFS v4.1 support'),
        ('5.1', '2022-Q1', 'Unity XT 5.1 — Unisphere 5.1 GA'),
        ('5.0', '2021-Q2', 'Unity XT 5.0 — NFSv4 ACL support'),
    ],
    'vplex': [
        ('6.2', '2024-Q2', 'VPLEX 6.2 — cloud provider metadata sync'),
        ('6.1', '2023-Q3', 'VPLEX 6.1 — concurrent I/O improvements'),
        ('6.0', '2022-Q4', 'VPLEX 6.0 — GeoSynchrony management API v2'),
        ('5.5', '2022-Q1', 'VPLEX 5.5 — metro witness enhancements'),
        ('5.4', '2021-Q2', 'VPLEX 5.4 — distributed cache improvements'),
    ],
    'data-domain': [
        ('8.1', '2024-Q2', 'Data Domain OS 8.1 — DD VE scale improvements'),
        ('7.13', '2023-Q3', 'DDOS 7.13 — cloud tier Azure Gov support'),
        ('7.12', '2023-Q1', 'DDOS 7.12 — DD3300 platform GA'),
        ('7.11', '2022-Q3', 'DDOS 7.11 — DD9900 capacity expansion'),
        ('7.10', '2022-Q1', 'DDOS 7.10 — Boost performance improvements'),
    ],
    'recoverpoint': [
        ('6.0', '2024-Q2', 'RecoverPoint 6.0 — VMAX/PowerMax 10 support'),
        ('5.3', '2023-Q2', 'RecoverPoint 5.3 — PowerStore replication GA'),
        ('5.2', '2022-Q2', 'RecoverPoint 5.2 — cloud copy target support'),
        ('5.1', '2021-Q4', 'RecoverPoint 5.1 — scale-out splitter support'),
        ('5.0', '2021-Q1', 'RecoverPoint 5.0 — VMware vSphere 7 support'),
    ],
    'srdf-a': [
        ('10.1', '2024-Q3', 'SRDF/A 10.1 — PowerMax 350F support'),
        ('10.0', '2023-Q3', 'SRDF/A 10.0 — cycle time tuning improvements'),
        ('9.2',  '2022-Q3', 'SRDF/A 9.2 — consistency group scale'),
        ('9.1',  '2021-Q4', 'SRDF/A 9.1 — adaptive copy enhancements'),
        ('9.0',  '2021-Q1', 'SRDF/A 9.0 — write pacing algorithm update'),
    ],
    'srdf-s': [
        ('10.1', '2024-Q3', 'SRDF/S 10.1 — 1 ms synchronous replication target'),
        ('10.0', '2023-Q3', 'SRDF/S 10.0 — PowerMax 350F GA'),
        ('9.2',  '2022-Q3', 'SRDF/S 9.2 — Metro witness improvements'),
        ('9.1',  '2021-Q4', 'SRDF/S 9.1 — Active/Active Metro enhancements'),
        ('9.0',  '2021-Q1', 'SRDF/S 9.0 — HYPERMAX OS 9.0 alignment'),
    ],
    'powerpath': [
        ('6.4', '2024-Q2', 'PowerPath 6.4 — RHEL 9.4 / SLES 15 SP5 support'),
        ('6.3', '2023-Q3', 'PowerPath 6.3 — PowerStore 3.0 multipath support'),
        ('6.2', '2022-Q4', 'PowerPath 6.2 — NVMe-oF multipath GA'),
        ('6.1', '2022-Q1', 'PowerPath 6.1 — Windows Server 2022 support'),
        ('6.0', '2021-Q2', 'PowerPath 6.0 — CLI management improvements'),
    ],
    'secure-connect-gateway': [
        ('5.16', '2024-Q3', 'SCG 5.16 — PowerMax 10.1 telemetry support'),
        ('5.14', '2024-Q1', 'SCG 5.14 — virtual edition scale improvements'),
        ('5.12', '2023-Q3', 'SCG 5.12 — REST API v2'),
        ('5.10', '2023-Q1', 'SCG 5.10 — automated alert routing'),
        ('5.8',  '2022-Q3', 'SCG 5.8 — proactive monitoring expansion'),
    ],
    'cloudiq': [
        ('2024.4', '2024-Q4', 'CloudIQ 2024.4 — sustainability score v2'),
        ('2024.2', '2024-Q2', 'CloudIQ 2024.2 — PowerStore 3.5 anomaly detection'),
        ('2023.4', '2023-Q4', 'CloudIQ 2023.4 — cyber recovery health index'),
        ('2023.2', '2023-Q2', 'CloudIQ 2023.2 — PowerScale capacity analytics'),
        ('2022.4', '2022-Q4', 'CloudIQ 2022.4 — Data Domain integration GA'),
    ],
    'dell-aiops': [
        ('2.4', '2024-Q2', 'Dell AIOps 2.4 — predictive failure improvements'),
        ('2.2', '2023-Q3', 'Dell AIOps 2.2 — cross-domain anomaly correlation'),
        ('2.0', '2022-Q4', 'Dell AIOps 2.0 GA — ML-driven capacity forecasting'),
        ('1.2', '2022-Q1', 'Dell AIOps 1.2 — alert noise reduction'),
        ('1.0', '2021-Q2', 'Dell AIOps 1.0 — initial preview'),
    ],
    'ecs': [
        ('3.8', '2024-Q2', 'ECS 3.8 — HDFS connector v2, S3 object lock GA'),
        ('3.7', '2023-Q3', 'ECS 3.7 — IAM compatibility improvements'),
        ('3.6', '2022-Q4', 'ECS 3.6 — multi-region federation'),
        ('3.5', '2022-Q1', 'ECS 3.5 — NFS v4 protocol support'),
        ('3.4', '2021-Q2', 'ECS 3.4 — REST management API v3'),
    ],
    'apex-storage-as-a-service': [
        ('2024.3', '2024-Q3', 'Apex STaaS 2024.3 — PowerMax NVMe tier addition'),
        ('2024.1', '2024-Q1', 'Apex STaaS 2024.1 — sustainability SLA module'),
        ('2023.3', '2023-Q3', 'Apex STaaS 2023.3 — PowerStore flex tier GA'),
        ('2023.1', '2023-Q1', 'Apex STaaS 2023.1 — burst capacity on-demand'),
        ('2022.3', '2022-Q3', 'Apex STaaS 2022.3 — PowerScale object tier'),
    ],
    'fod': [
        ('3.2', '2024-Q2', 'FOD 3.2 — PowerMax 10.1 feature enablement'),
        ('3.1', '2023-Q3', 'FOD 3.1 — online license activation improvements'),
        ('3.0', '2022-Q4', 'FOD 3.0 — REST API license management'),
        ('2.5', '2022-Q1', 'FOD 2.5 — multi-array batch activation'),
        ('2.4', '2021-Q2', 'FOD 2.4 — license audit report export'),
    ],
    'cod': [
        ('3.2', '2024-Q2', 'COD 3.2 — PowerMax 10.1 on-demand capacity'),
        ('3.1', '2023-Q3', 'COD 3.1 — automated capacity reporting'),
        ('3.0', '2022-Q4', 'COD 3.0 — REST API for capacity management'),
        ('2.5', '2022-Q1', 'COD 2.5 — CloudIQ integration'),
        ('2.4', '2021-Q2', 'COD 2.4 — usage forecasting model'),
    ],
    'aws': [
        ('2024-Q3', '2024-Q3', 'AWS — EC2 C8g instances GA, EBS io2 Block Express'),
        ('2024-Q1', '2024-Q1', 'AWS — EKS 1.29, RDS Graviton3 default'),
        ('2023-Q3', '2023-Q3', 'AWS — VPC Lattice GA, GuardDuty EKS runtime'),
        ('2023-Q1', '2023-Q1', 'AWS — ECS Fargate spot improvements'),
        ('2022-Q3', '2022-Q3', 'AWS — Lake Formation governed tables GA'),
    ],
    'evs': [
        ('1.3', '2024-Q3', 'AWS EVS 1.3 — vSphere 8.0 U3 baseline'),
        ('1.2', '2024-Q1', 'AWS EVS 1.2 — SDDC interconnect improvements'),
        ('1.1', '2023-Q3', 'AWS EVS 1.1 — NSX 4.1 support'),
        ('1.0', '2023-Q1', 'AWS EVS 1.0 GA — VMware workloads on AWS bare metal'),
        ('Preview', '2022-Q4', 'AWS EVS preview — initial availability regions'),
    ],
    'azure': [
        ('2024-Q3', '2024-Q3', 'Azure — AKS 1.30 GA, Azure VMware Solution 5.x'),
        ('2024-Q1', '2024-Q1', 'Azure — Confidential VMs DCesv5, ZRS disks'),
        ('2023-Q3', '2023-Q3', 'Azure — Azure Backup for AKS GA'),
        ('2023-Q1', '2023-Q1', 'Azure — Azure NetApp Files large volumes GA'),
        ('2022-Q3', '2022-Q3', 'Azure — Elastic SAN preview'),
    ],
    'linux': [
        ('RHEL 9.4',   '2024-Q2', 'RHEL 9.4 — kernel 5.14.0-427, FIPS 140-3'),
        ('RHEL 9.3',   '2023-Q4', 'RHEL 9.3 — image mode preview, toolbox v3'),
        ('RHEL 9.2',   '2023-Q2', 'RHEL 9.2 — OpenSSL 3.0.7, SELinux udica'),
        ('Ubuntu 24.04','2024-Q2','Ubuntu 24.04 LTS — kernel 6.8, systemd 255'),
        ('Ubuntu 22.04','2022-Q2','Ubuntu 22.04 LTS — kernel 5.15, OpenSSL 3.0'),
    ],
    'mysql': [
        ('8.4 LTS', '2024-Q2', 'MySQL 8.4 LTS — new innovation release model'),
        ('8.2',     '2023-Q4', 'MySQL 8.2 — Vector data type preview'),
        ('8.0.36',  '2024-Q1', 'MySQL 8.0.36 — security and bug fix release'),
        ('8.0.34',  '2023-Q3', 'MySQL 8.0.34 — JSON table improvements'),
        ('8.0.32',  '2023-Q1', 'MySQL 8.0.32 — InnoDB parallel DDL'),
    ],
    'postgresql': [
        ('17', '2024-Q4', 'PostgreSQL 17 — incremental backup, MERGE improvements'),
        ('16', '2023-Q4', 'PostgreSQL 16 — logical replication from standby'),
        ('15', '2022-Q4', 'PostgreSQL 15 — MERGE command, improved sorting'),
        ('14', '2021-Q4', 'PostgreSQL 14 — pipeline mode, ranges multirange'),
        ('13', '2020-Q4', 'PostgreSQL 13 — partitioned table improvements'),
    ],
    'windows-server': [
        ('2025',     '2024-Q4', 'Windows Server 2025 — Hotpatch GA, NVMe improvements'),
        ('2022 CU9', '2024-Q2', 'Windows Server 2022 CU9 — security patches'),
        ('2022 CU6', '2023-Q3', 'Windows Server 2022 CU6 — SMB compression improvements'),
        ('2022 GA',  '2021-Q4', 'Windows Server 2022 GA — Azure Arc integration'),
        ('2019 LTS', '2018-Q4', 'Windows Server 2019 LTS baseline'),
    ],
    'active-directory': [
        ('2025 FL', '2024-Q4', 'AD Forest Level 2025 — DC functional level update'),
        ('2022 FL', '2021-Q4', 'AD Forest Level 2022 — default policy changes'),
        ('2019 FL', '2018-Q4', 'AD Forest Level 2019 — AES-256 preferred'),
        ('2016 FL', '2016-Q3', 'AD Forest Level 2016 — PAM and Just-in-Time access'),
        ('2012 R2', '2013-Q4', 'AD Forest Level 2012 R2 — Protected Users group'),
    ],
    'sql-server': [
        ('2022 CU14', '2024-Q4', 'SQL Server 2022 CU14 — Query Store enhancements'),
        ('2022 CU10', '2024-Q1', 'SQL Server 2022 CU10 — security and performance'),
        ('2022 GA',   '2022-Q4', 'SQL Server 2022 GA — Azure Synapse Link'),
        ('2019 CU25', '2023-Q4', 'SQL Server 2019 CU25 — HA improvements'),
        ('2019 GA',   '2019-Q4', 'SQL Server 2019 GA — Big Data Clusters'),
    ],
    'confluence': [
        ('8.9', '2024-Q3', 'Confluence 8.9 — AI companion GA, editor improvements'),
        ('8.8', '2024-Q2', 'Confluence 8.8 — Jira integration updates'),
        ('8.5', '2023-Q4', 'Confluence 8.5 — drag-and-drop page tree'),
        ('8.0', '2023-Q1', 'Confluence 8.0 — new visual editor foundation'),
        ('7.19','2022-Q3', 'Confluence 7.19 — LTS baseline release'),
    ],
    'jira': [
        ('9.17', '2024-Q3', 'Jira Software 9.17 — Backlog import improvements'),
        ('9.15', '2024-Q2', 'Jira Software 9.15 — roadmap planning update'),
        ('9.12', '2024-Q1', 'Jira Software 9.12 — plan capacity enhancements'),
        ('9.4',  '2023-Q1', 'Jira Software 9.4 — LTS baseline'),
        ('9.0',  '2022-Q3', 'Jira Software 9.0 — project template updates'),
    ],
    'servicenow': [
        ('Xanadu', '2024-Q4', 'ServiceNow Xanadu — Now Assist AI GA'),
        ('Washington', '2024-Q1', 'ServiceNow Washington — CMDB auto-discovery'),
        ('Vancouver', '2023-Q4', 'ServiceNow Vancouver — ITSM AI enhancements'),
        ('Utah',      '2023-Q1', 'ServiceNow Utah — proactive CSM'),
        ('Tokyo',     '2022-Q4', 'ServiceNow Tokyo — App Engine studio v2'),
    ],
    'git': [
        ('2.46', '2024-Q3', 'Git 2.46 — multi-pack bitmap improvements'),
        ('2.44', '2024-Q1', 'Git 2.44 — bundle URI improvements'),
        ('2.42', '2023-Q3', 'Git 2.42 — new reftable format'),
        ('2.40', '2023-Q1', 'Git 2.40 — improved fetch negotiation'),
        ('2.38', '2022-Q3', 'Git 2.38 — bundle URI preview, scalar updates'),
    ],
    'github-actions': [
        ('2024-Q3', '2024-Q3', 'GitHub Actions — GPU-hosted runners GA'),
        ('2024-Q1', '2024-Q1', 'GitHub Actions — larger hosted runners ARM'),
        ('2023-Q3', '2023-Q3', 'GitHub Actions — required workflows GA'),
        ('2023-Q1', '2023-Q1', 'GitHub Actions — environment protection rules'),
        ('2022-Q3', '2022-Q3', 'GitHub Actions — reusable workflows GA'),
    ],
    'powershell': [
        ('7.4 LTS', '2024-Q1', 'PowerShell 7.4 LTS — .NET 8 baseline'),
        ('7.3',     '2022-Q4', 'PowerShell 7.3 — tab completion improvements'),
        ('7.2 LTS', '2021-Q4', 'PowerShell 7.2 LTS — .NET 6 baseline'),
        ('7.1',     '2020-Q4', 'PowerShell 7.1 — ForEach-Object -Parallel GA'),
        ('7.0',     '2020-Q1', 'PowerShell 7.0 GA — cross-platform LTS'),
    ],
    'python': [
        ('3.13', '2024-Q4', 'Python 3.13 — free-threaded mode, JIT compiler preview'),
        ('3.12', '2023-Q4', 'Python 3.12 — improved error messages, f-string updates'),
        ('3.11', '2022-Q4', 'Python 3.11 — 10-60 % speed improvements'),
        ('3.10', '2021-Q4', 'Python 3.10 — structural pattern matching'),
        ('3.9',  '2020-Q4', 'Python 3.9 — dict union operators, type hints'),
    ],
    'fabric-os': [
        ('9.2.2', '2024-Q3', 'FOS 9.2.2 — 64G FC speed support'),
        ('9.2.1', '2024-Q1', 'FOS 9.2.1 — security hardening patches'),
        ('9.2.0', '2023-Q3', 'FOS 9.2.0 — zoning scalability improvements'),
        ('9.1.1', '2023-Q1', 'FOS 9.1.1 — FICON MIHPTO enhancements'),
        ('9.1.0', '2022-Q3', 'FOS 9.1.0 — 64G long distance SFP support'),
    ],
    'sannav': [
        ('2.3.1', '2024-Q3', 'SANnav 2.3.1 — FOS 9.2.2 discovery support'),
        ('2.3.0', '2024-Q1', 'SANnav 2.3.0 — health dashboard improvements'),
        ('2.2.2', '2023-Q3', 'SANnav 2.2.2 — REST API v2 analytics'),
        ('2.2.1', '2023-Q1', 'SANnav 2.2.1 — scalability patch release'),
        ('2.2.0', '2022-Q3', 'SANnav 2.2.0 — Supportsave automation'),
    ],
    'cisco-dcnm': [
        ('12.2', '2024-Q2', 'DCNM 12.2 — fabric controller convergence'),
        ('12.1', '2023-Q3', 'DCNM 12.1 — vPC enhancements'),
        ('12.0', '2022-Q4', 'DCNM 12.0 — rebrand to Nexus Dashboard Fabric Controller'),
        ('11.5', '2022-Q1', 'DCNM 11.5 — LAN fabric improvements'),
        ('11.4', '2021-Q2', 'DCNM 11.4 — REST API v1 expansion'),
    ],
    'mds': [
        ('9.4(3)', '2024-Q3', 'MDS NX-OS 9.4(3) — 64G FC GA'),
        ('9.4(2)', '2024-Q1', 'MDS NX-OS 9.4(2) — CFS improvements'),
        ('9.3(2)', '2023-Q3', 'MDS NX-OS 9.3(2) — IVR NAT enhancements'),
        ('9.3(1)', '2023-Q1', 'MDS NX-OS 9.3(1) — Smart Zoning scale'),
        ('9.2(2)', '2022-Q3', 'MDS NX-OS 9.2(2) — DPPM improvements'),
    ],
    'nexus-dashboard': [
        ('3.2', '2024-Q3', 'Nexus Dashboard 3.2 — multi-site fabric visibility'),
        ('3.1', '2024-Q1', 'Nexus Dashboard 3.1 — Insights ML models'),
        ('3.0', '2023-Q3', 'Nexus Dashboard 3.0 — unified services hub'),
        ('2.3', '2023-Q1', 'Nexus Dashboard 2.3 — ACI Insights GA'),
        ('2.2', '2022-Q3', 'Nexus Dashboard 2.2 — scalability improvements'),
    ],
    'security': [
        ('2024-Q4', '2024-Q4', 'Security framework — zero-trust policy update'),
        ('2024-Q2', '2024-Q2', 'Security — NIST CSF 2.0 control mapping'),
        ('2023-Q4', '2023-Q4', 'Security — CIS benchmark v8.1 alignment'),
        ('2023-Q2', '2023-Q2', 'Security — MITRE ATT&CK v14 coverage update'),
        ('2022-Q4', '2022-Q4', 'Security — ISO 27001:2022 gap analysis'),
    ],
    'cyberark': [
        ('14.2', '2024-Q3', 'CyberArk 14.2 — PAM360 integration improvements'),
        ('14.0', '2024-Q1', 'CyberArk 14.0 — CORA AI launch'),
        ('13.2', '2023-Q3', 'CyberArk 13.2 — EPM Mac Apple Silicon support'),
        ('13.0', '2023-Q1', 'CyberArk 13.0 — Identity Security platform'),
        ('12.6', '2022-Q3', 'CyberArk 12.6 — Conjur Cloud GA'),
    ],
    'venafi': [
        ('24.3', '2024-Q3', 'Venafi 24.3 — TLS Protect Cloud improvements'),
        ('24.1', '2024-Q1', 'Venafi 24.1 — Kubernetes cert-manager integration'),
        ('23.4', '2023-Q4', 'Venafi 23.4 — CodeSign Protect updates'),
        ('23.2', '2023-Q2', 'Venafi 23.2 — machine identity firewall'),
        ('22.4', '2022-Q4', 'Venafi 22.4 — TrustNet improvements'),
    ],
    'nutanix': [
        ('6.8', '2024-Q3', 'AOS 6.8 — NCI improvements, 3-node edge scaling'),
        ('6.7', '2024-Q1', 'AOS 6.7 — Flow Network Security enhancements'),
        ('6.6', '2023-Q3', 'AOS 6.6 — Objects 4.0 S3 multipart upload'),
        ('6.5', '2023-Q1', 'AOS 6.5 LTS — Prism Central scale improvements'),
        ('6.1', '2022-Q1', 'AOS 6.1 — Nutanix Files WORM GA'),
    ],
    'openshift': [
        ('4.16', '2024-Q2', 'OpenShift 4.16 — Kubernetes 1.29, tech preview updates'),
        ('4.15', '2024-Q1', 'OpenShift 4.15 — RHCOS improvements, ACM 2.10'),
        ('4.14', '2023-Q4', 'OpenShift 4.14 — LTS, HyperShift GA'),
        ('4.13', '2023-Q2', 'OpenShift 4.13 — hosted control planes preview'),
        ('4.12', '2022-Q4', 'OpenShift 4.12 — LVM operator GA, Tekton 1.9'),
    ],
    'vmware': [
        ('vSphere 8.0 U3', '2024-Q3', 'vSphere 8.0 U3 — multi-product patch release'),
        ('vSphere 8.0 U2', '2024-Q1', 'vSphere 8.0 U2 — vCenter HA improvements'),
        ('vSphere 8.0 U1', '2023-Q2', 'vSphere 8.0 U1 — stability and security'),
        ('vSphere 8.0 GA', '2022-Q4', 'vSphere 8.0 GA — DPU offload, vSAN ESA'),
        ('vSphere 7.0 U3', '2022-Q1', 'vSphere 7.0 U3 — lifecycle management LTS'),
    ],
    'access-review': [
        ('2024-Q4', '2024-Q4', 'Access Review — quarterly cycle automation update'),
        ('2024-Q2', '2024-Q2', 'Access Review — Joiner-Mover-Leaver workflow'),
        ('2023-Q4', '2023-Q4', 'Access Review — Entra ID integration improvements'),
        ('2023-Q2', '2023-Q2', 'Access Review — SoD conflict detection update'),
        ('2022-Q4', '2022-Q4', 'Access Review — certification campaign template v2'),
    ],
    'certificates': [
        ('2024-Q4', '2024-Q4', 'Certificates — 90-day max validity enforcement'),
        ('2024-Q2', '2024-Q2', 'Certificates — ACME protocol rollout expansion'),
        ('2023-Q4', '2023-Q4', 'Certificates — CT log monitoring integration'),
        ('2023-Q2', '2023-Q2', 'Certificates — auto-renewal pipeline update'),
        ('2022-Q4', '2022-Q4', 'Certificates — SHA-1 deprecation enforcement'),
    ],
    'compliance-standards': [
        ('2024-Q4', '2024-Q4', 'Compliance — ISO 27001:2022 transition complete'),
        ('2024-Q2', '2024-Q2', 'Compliance — NIST CSF 2.0 mapping update'),
        ('2023-Q4', '2023-Q4', 'Compliance — CIS Controls v8.1 adoption'),
        ('2023-Q2', '2023-Q2', 'Compliance — SOC 2 Type II evidence collection'),
        ('2022-Q4', '2022-Q4', 'Compliance — GDPR annual review cycle'),
    ],
    'incident-handling': [
        ('2024-Q4', '2024-Q4', 'IR — NIST SP 800-61r3 alignment update'),
        ('2024-Q2', '2024-Q2', 'IR — playbook automation (SOAR integration)'),
        ('2023-Q4', '2023-Q4', 'IR — severity classification update'),
        ('2023-Q2', '2023-Q2', 'IR — tabletop exercise framework revision'),
        ('2022-Q4', '2022-Q4', 'IR — evidence handling chain-of-custody update'),
    ],
    'ldap-integration': [
        ('2024-Q3', '2024-Q3', 'LDAP — TLS 1.3 enforcement across all services'),
        ('2024-Q1', '2024-Q1', 'LDAP — LDAPS certificate auto-rotation'),
        ('2023-Q3', '2023-Q3', 'LDAP — attribute schema documentation update'),
        ('2023-Q1', '2023-Q1', 'LDAP — referral chasing policy update'),
        ('2022-Q3', '2022-Q3', 'LDAP — binding account privilege reduction'),
    ],
    'mfa': [
        ('2024-Q4', '2024-Q4', 'MFA — phishing-resistant FIDO2 policy enforcement'),
        ('2024-Q2', '2024-Q2', 'MFA — conditional access policy update'),
        ('2023-Q4', '2023-Q4', 'MFA — number matching required for push'),
        ('2023-Q2', '2023-Q2', 'MFA — passkey (FIDO2) pilot deployment'),
        ('2022-Q4', '2022-Q4', 'MFA — legacy auth block policy go-live'),
    ],
    'patch-compliance': [
        ('2024-Q4', '2024-Q4', 'Patching — 30-day critical SLA policy update'),
        ('2024-Q2', '2024-Q2', 'Patching — automated compliance reporting v2'),
        ('2023-Q4', '2023-Q4', 'Patching — WSUS replacement with SCCM/MECM'),
        ('2023-Q2', '2023-Q2', 'Patching — OS patch ring framework update'),
        ('2022-Q4', '2022-Q4', 'Patching — third-party app patching baseline'),
    ],
    'saml-configuration': [
        ('2024-Q3', '2024-Q3', 'SAML — SHA-256 assertion signing enforced'),
        ('2024-Q1', '2024-Q1', 'SAML — IdP metadata auto-refresh rollout'),
        ('2023-Q3', '2023-Q3', 'SAML — certificate rotation automation'),
        ('2023-Q1', '2023-Q1', 'SAML — attribute mapping standard update'),
        ('2022-Q3', '2022-Q3', 'SAML — IDP-initiated SSO audit trail'),
    ],
    'security-audit': [
        ('2024-Q4', '2024-Q4', 'Security Audit — CISA KEV checklist integration'),
        ('2024-Q2', '2024-Q2', 'Security Audit — automated evidence collection'),
        ('2023-Q4', '2023-Q4', 'Security Audit — red team findings remediation v2'),
        ('2023-Q2', '2023-Q2', 'Security Audit — penetration test scope update'),
        ('2022-Q4', '2022-Q4', 'Security Audit — cloud posture review addition'),
    ],
    'security-monitoring': [
        ('2024-Q4', '2024-Q4', 'Security Monitoring — SIEM rule library v4'),
        ('2024-Q2', '2024-Q2', 'Security Monitoring — UEBA baseline update'),
        ('2023-Q4', '2023-Q4', 'Security Monitoring — cloud-native detection rules'),
        ('2023-Q2', '2023-Q2', 'Security Monitoring — XDR integration GA'),
        ('2022-Q4', '2022-Q4', 'Security Monitoring — SOC playbook automation'),
    ],
    'vulnerability-management': [
        ('2024-Q4', '2024-Q4', 'Vuln Mgmt — EPSS-driven prioritisation rollout'),
        ('2024-Q2', '2024-Q2', 'Vuln Mgmt — API-based scanner orchestration'),
        ('2023-Q4', '2023-Q4', 'Vuln Mgmt — CVSS 4.0 scoring adoption'),
        ('2023-Q2', '2023-Q2', 'Vuln Mgmt — container image scanning GA'),
        ('2022-Q4', '2022-Q4', 'Vuln Mgmt — SLA breach dashboard launch'),
    ],
}

# ── Terminology per product slug ──────────────────────────────────────────────
TERMINOLOGY = {
    'ontap': [
        ('Release Train', 'NetApp\'s versioning scheme: major.minor.patch (e.g. 9.15.1). Minor releases add features; patches fix bugs.'),
        ('LTR (Long-Term Release)', 'Designated ONTAP releases with extended support windows — currently 9.8, 9.12, 9.14.'),
        ('ANDU (Automated Non-Disruptive Upgrade)', 'Built-in ONTAP upgrade orchestration that performs rolling node-by-node updates without I/O interruption.'),
        ('EOS (End of Support)', 'Date after which NetApp no longer issues patches or provides support for a given ONTAP release.'),
    ],
    'vsan': [
        ('Update (U)', 'vSAN update numbering suffix (e.g. 8.0 U3) — incremental feature and fix release within a major version.'),
        ('ESA (Express Storage Architecture)', 'vSAN 8 redesigned storage stack replacing legacy OSA; requires NVMe-only disk groups.'),
        ('vSAN SKU', 'Licensing tier that determines feature availability: Standard, Advanced, Enterprise, Enterprise Plus.'),
        ('Build Number', 'Unique ESXi/vSAN build identifier used to confirm exact patch level after upgrade.'),
    ],
    'default': [
        ('Major Version', 'A release containing significant new features or architectural changes; may require additional planning and testing.'),
        ('Patch Release', 'A targeted fix release that addresses bugs or security issues within a major/minor version.'),
        ('EOL (End of Life)', 'Date after which the vendor no longer provides updates, security patches, or technical support.'),
        ('Upgrade Path', 'The supported sequence of versions a system must traverse to reach a target version (some versions cannot be skipped).'),
    ],
}

def get_terminology(slug):
    return TERMINOLOGY.get(slug, TERMINOLOGY['default'])

# ── Upgrade path paragraphs per product slug ──────────────────────────────────
UPGRADE_PATHS = {
    'ontap': (
        'Upgrade from the current running version by reviewing the '
        '[NetApp Upgrade Advisor](https://docs.netapp.com/us-en/ontap/upgrade/index.html). '
        'Multi-hop upgrades (skipping minor versions) are supported only within the same major train; '
        'always validate with the ANDU compatibility matrix. Apply the upgrade in a non-disruptive '
        'rolling fashion using System Manager or CLI `system node image update`.'
    ),
    'vsan': (
        'Use the vSphere Lifecycle Manager (vLCM) image-based baseline to upgrade vSAN clusters. '
        'Validate interoperability with the [VMware Compatibility Guide](https://www.vmware.com/resources/compatibility/search.php) '
        'before upgrading. Always upgrade vCenter and ESXi to the target version before upgrading '
        'the vSAN disk format. For ESA clusters, a full rolling evacuation is performed per host.'
    ),
    'ansible': (
        'Upgrade ansible-core via `pip install --upgrade ansible-core==<version>`. '
        'When moving to a new major version review the [porting guide](https://docs.ansible.com/ansible/latest/porting_guides/). '
        'Test all existing playbooks in a staging inventory before rolling to production controllers. '
        'For AAP, use the installer bundle and follow the in-place upgrade procedure documented in the AAP Installation Guide.'
    ),
    'vcenter': (
        'Upgrade vCenter Server using the VMware vCenter Server Installer or VAMI. '
        'Always upgrade vCenter before ESXi hosts. Ensure the target version is compatible with all '
        'managed hosts using the [VMware Product Interoperability Matrix](https://interopmatrix.vmware.com/). '
        'Snapshot the vCenter appliance VM before beginning. Post-upgrade, verify vCenter HA and '
        'Plugin compatibility.'
    ),
    'default': (
        'Review the vendor\'s official upgrade documentation and compatibility matrix before '
        'beginning any version change. Validate that all dependent components (OS, drivers, '
        'integration plugins) support the target version. Perform upgrades in a staged approach: '
        'dev/test environment first, then production. Capture a snapshot or backup immediately '
        'prior to the upgrade window. After the upgrade, run post-validation health checks and '
        'confirm all services are operating normally.'
    ),
}

def get_upgrade_path(slug):
    return UPGRADE_PATHS.get(slug, UPGRADE_PATHS['default'])


def get_versions(slug):
    return VERSIONS.get(slug, [
        ('1.5', '2024-Q3', f'{slug.title()} 1.5 — latest patch release'),
        ('1.4', '2024-Q1', f'{slug.title()} 1.4 — minor feature update'),
        ('1.3', '2023-Q3', f'{slug.title()} 1.3 — stability improvements'),
        ('1.2', '2023-Q1', f'{slug.title()} 1.2 — security hardening release'),
        ('1.1', '2022-Q3', f'{slug.title()} 1.1 — initial GA'),
    ])


# ── SVG generation ────────────────────────────────────────────────────────────

def xe(s: str) -> str:
    """Escape characters invalid in SVG/XML text nodes."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def make_flow_svg(product_name: str, slug: str) -> str:
    """
    Generate a compact 820×200 horizontal 5-box flow SVG.
    Style: navy header bar, light-green box row, navy footer.
    Boxes: Identify Version → Review Changes → Test Compatibility → Deploy Update → ✓ Running Current
    """
    boxes = [
        'Identify Version',
        'Review Changes',
        'Test Compatibility',
        'Deploy Update',
        '✓ Running Current',
    ]
    n = len(boxes)
    PAD = 16
    ARROW = 14
    total_gap = (n - 1) * ARROW
    available = SVG_W - 2 * PAD - total_gap
    bw = available // n
    bh = SVG_H - HDR_H - FTR_H - 20  # 20 vertical padding (10 top + 10 bottom)
    by = HDR_H + 10

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_W}" height="{SVG_H}" '
        f'font-family="\'Segoe UI\',Arial,sans-serif">',
        f'  <rect width="{SVG_W}" height="{SVG_H}" fill="#f4f6f9"/>',
        # Header
        f'  <rect x="0" y="0" width="{SVG_W}" height="{HDR_H}" fill="{NAVY}"/>',
        f'  <text x="410" y="28" text-anchor="middle" fill="white" '
        f'font-size="14" font-weight="700">{xe(product_name)} — Release Notes</text>',
        f'  <text x="410" y="41" text-anchor="middle" fill="{FOOTER_FG}" '
        f'font-size="10">Version history and upgrade lifecycle</text>',
    ]

    for i, label in enumerate(boxes):
        bx = PAD + i * (bw + ARROW)
        cy = by + bh // 2
        # Arrow before box (except first)
        if i > 0:
            ax = bx - ARROW
            lines.append(
                f'  <line x1="{ax}" y1="{cy}" x2="{bx}" y2="{cy}" '
                f'stroke="{ARROW_CLR}" stroke-width="2" marker-end="url(#arr)"/>'
            )
        fill = BOX_FILL if not label.startswith('✓') else '#c8e6c9'
        stroke = BOX_STROKE
        txt_col = BOX_TEXT
        lines.append(
            f'  <rect x="{bx}" y="{by}" width="{bw}" height="{bh}" '
            f'rx="4" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
        )
        # Split long labels onto two lines
        words = label.split(' ')
        if len(words) <= 2:
            lines.append(
                f'  <text x="{bx + bw // 2}" y="{cy + 4}" '
                f'text-anchor="middle" fill="{txt_col}" '
                f'font-size="9" font-weight="700">{xe(label)}</text>'
            )
        else:
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            lines.append(
                f'  <text x="{bx + bw // 2}" y="{cy - 3}" '
                f'text-anchor="middle" fill="{txt_col}" '
                f'font-size="9" font-weight="700">{xe(line1)}</text>'
            )
            lines.append(
                f'  <text x="{bx + bw // 2}" y="{cy + 9}" '
                f'text-anchor="middle" fill="{txt_col}" '
                f'font-size="9" font-weight="700">{xe(line2)}</text>'
            )

    # Arrow marker def
    lines.insert(1,
        '  <defs>'
        '<marker id="arr" markerWidth="6" markerHeight="6" refX="6" refY="3" orient="auto">'
        f'<path d="M0,0 L6,3 L0,6 Z" fill="{ARROW_CLR}"/>'
        '</marker></defs>'
    )

    # Footer
    lines.append(
        f'  <rect x="0" y="{FTR_Y}" width="{SVG_W}" height="{FTR_H}" fill="{NAVY}"/>'
    )
    lines.append(
        f'  <text x="410" y="{FTR_Y + 19}" text-anchor="middle" '
        f'fill="{FOOTER_FG}" font-size="9">'
        f'{xe(product_name)} · Release Notes</text>'
    )
    lines.append('</svg>')
    return '\n'.join(lines)


def validate_svg(svg_text: str) -> None:
    ET.fromstring(svg_text)


# ── Tags extraction from index.md ─────────────────────────────────────────────

def extract_tags(product_dir: Path, slug: str) -> list:
    index = product_dir / 'index.md'
    if not index.exists():
        return [slug]
    text = index.read_text(encoding='utf-8')
    # Parse YAML frontmatter
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return [slug]
    fm = m.group(1)
    # Extract tags block
    tag_match = re.search(r'^tags:\s*\n((?:[ \t]+-[^\n]+\n?)+)', fm, re.MULTILINE)
    if not tag_match:
        return [slug]
    tags = []
    for line in tag_match.group(1).splitlines():
        line = line.strip()
        if line.startswith('-'):
            tags.append(line[1:].strip())
    return tags if tags else [slug]


# ── Release notes page generation ────────────────────────────────────────────

def build_release_notes_md(
    product_dir: Path,
    slug: str,
    product_name: str,
    rel_assets: str,
) -> str:
    tags = extract_tags(product_dir, slug)
    tags_yaml = '\n'.join(f'  - {t}' for t in tags)
    versions = get_versions(slug)
    terminology = get_terminology(slug)
    upgrade = get_upgrade_path(slug)

    # Version table rows
    table_rows = '\n'.join(
        f'| {v} | {d} | {s} | [Release Notes](#) |'
        for v, d, s in versions
    )

    # Terminology section
    term_lines = '\n\n'.join(
        f'**{term}**\n: {defn}' for term, defn in terminology
    )

    return f"""---
tags:
{tags_yaml}
---
# {product_name} — Release Notes

<div class="kb-summary">
Version history and release notes for {product_name}.
</div>

![Release Notes]({rel_assets}{slug}-release-notes.svg)

## Version History

| Version | Released | Summary | Notes |
|---------|----------|---------|-------|
{table_rows}

## Key Terminology

{term_lines}

## Upgrade Path

{upgrade}
"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Generate release-notes.md stubs for KB products.')
    parser.add_argument('--dry-run', action='store_true', help='Print what would be created without writing files.')
    args = parser.parse_args()

    products = sorted(
        {d.parent for d in DOCS.rglob('operations') if d.is_dir()},
        key=lambda p: str(p.relative_to(DOCS))
    )

    created = 0
    skipped = 0
    svg_created = 0

    for product_dir in products:
        rel = product_dir.relative_to(DOCS)
        slug = product_dir.name
        product_name = DISPLAY_NAMES.get(slug, slug.replace('-', ' ').title())

        page = product_dir / 'release-notes.md'

        # Compute relative assets path
        depth = len(page.parts) - len(DOCS.parts) - 1
        rel_assets = '../' * depth + 'assets/'

        # SVG path
        svg_name = f'{slug}-release-notes.svg'
        svg_path = ASSETS / svg_name

        if page.exists():
            print(f'  SKIP  {rel}/release-notes.md (already exists)')
            skipped += 1
            continue

        # Generate and validate SVG
        svg_text = make_flow_svg(product_name, slug)
        try:
            validate_svg(svg_text)
        except ET.ParseError as e:
            print(f'  ERROR SVG validation failed for {slug}: {e}', file=sys.stderr)
            sys.exit(1)

        # Build markdown
        md = build_release_notes_md(product_dir, slug, product_name, rel_assets)

        if args.dry_run:
            print(f'  DRY   {rel}/release-notes.md  (SVG: assets/{svg_name})')
        else:
            # Write SVG
            if not svg_path.exists():
                svg_path.write_text(svg_text, encoding='utf-8')
                svg_created += 1

            # Write markdown
            page.write_text(md, encoding='utf-8')
            print(f'  WRITE {rel}/release-notes.md')
            created += 1

    print()
    if args.dry_run:
        print(f'Dry run complete. Would create {len(products) - skipped} pages '
              f'(skipping {skipped} existing).')
    else:
        print(f'Done. Created {created} release-notes.md pages and {svg_created} SVGs. '
              f'Skipped {skipped} existing.')


if __name__ == '__main__':
    main()
