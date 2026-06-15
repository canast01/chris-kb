#!/usr/bin/env python3
"""
Bulk diagram writer — generates ASCII diagrams directly into markdown files.
Uses the _core.py primitives for correct rendering.
Run from repo root: python3 scripts/bulk_diagram_writer.py
"""
import os, sys
sys.path.insert(0, 'scripts')
from diagrams._core import (
    make_helpers, row, bTop, bMid, bBot, sections,
    connector, arrow, title_border, merge,
)

W2 = 103
IV_L, IV_R = 3, 99
INNER = IV_R - IV_L - 1   # 95 inner chars for full-width box
B1_L, B1_R = 3, 33
B2_L, B2_R = 36, 66
B3_L, B3_R = 69, 99
H1_L, H1_R = 3, 50
H2_L, H2_R = 52, 99
M1, M2, M3 = 18, 51, 84
MH1, MH2   = 26, 76
PD1, PD2, PD3, PD4 = 22, 41, 61, 80


def make_diagram(title, summary4, flow, col3_rows, sec_rows5, physical, terms12):
    """
    Build a complete diagram string using _core primitives.
    summary4   : list of 4 strings for the wide top box
    flow       : one-line flow description string
    col3_rows  : list of (c1, c2, c3) tuples — first is header, rest are data (5-6 rows)
    sec_rows5  : list of 5-tuples for the wide section table (first is header)
    physical   : physical infra line
    terms12    : list of (term, definition) — 12+ entries
    """
    R, txt_row = make_helpers(W2)
    lines = []

    lines.append(title_border(W2, title))
    lines.append(txt_row())

    # Wide summary box
    lines.append(R(bTop(IV_L, IV_R)))
    for s in summary4:
        lines.append(R(bMid(IV_L, IV_R, s)))
    lines.append(R(bBot(IV_L, IV_R)))
    _MAX = W2 - 4
    lines.append(txt_row())
    lines.append(txt_row(flow[:_MAX]))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    # 3-column detail boxes
    header, *data = col3_rows
    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(bMid(B1_L, B1_R, header[0]), bMid(B2_L, B2_R, header[1]), bMid(B3_L, B3_R, header[2]))))
    for r3 in data:
        lines.append(R(merge(bMid(B1_L, B1_R, r3[0]), bMid(B2_L, B2_R, r3[1]), bMid(B3_L, B3_R, r3[2]))))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))
    lines.append(txt_row())
    lines.append(R(arrow([MH1, MH2])))
    lines.append(txt_row())

    # Wide section table
    header5, *rows5 = sec_rows5
    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], header5)))
    for r5 in rows5:
        lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4], r5)))
    lines.append(R(bBot(IV_L, IV_R)))
    MAX = W2 - 4  # max content chars for txt_row with indent=2
    lines.append(txt_row())
    lines.append(txt_row(f'  Physical: {physical}'[:MAX]))
    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row())
    for term, defn in terms12:
        line = f'  {term:<18} = {defn}'
        lines.append(txt_row(line[:MAX]))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return '\n'.join(lines)


# ── Product catalog ──────────────────────────────────────────────────────────
# Each product entry contains data needed to generate page-type diagrams

def _clamp(s, n):
    return s[:n] if len(s) > n else s

C3 = 29   # max inner width for 3-col box
C5A, C5B = 18, 17  # approx widths for section table cells

PRODUCTS = {}

def reg(prefix, name, abbr, cat, protos, phys, mgmt, comps5, arch5, sec_rows5, terms12):
    PRODUCTS[prefix] = dict(
        name=name, abbr=abbr, cat=cat, protos=protos,
        phys=phys, mgmt=mgmt, comps5=comps5, arch5=arch5,
        sec_rows5=sec_rows5, terms=terms12)

# ── Dell Storage ─────────────────────────────────────────────────────────────
reg('storage/dell/apex-storage-as-a-service',
    'Dell Apex STaaS', 'Apex STaaS',
    'cloud-managed on-prem storage subscription',
    'iSCSI · FC · NFS · SMB',
    'Dell array hardware on-premises · customer iSCSI VLAN / FC fabric · Apex Console SaaS',
    'Apex Console',
    ['Apex Console', 'CloudIQ', 'SCG relay', 'NVMe arrays', 'Billing portal'],
    [('Layer', 'Component', 'Owner'),
     ('Hardware', 'NVMe/SAS arrays', 'Dell'),
     ('Management', 'Apex Console', 'Customer'),
     ('Monitoring', 'CloudIQ/SCG', 'Shared'),
     ('Billing', 'Committed+burst', 'Dell billing'),
     ('Network', 'iSCSI VLAN/FC', 'Customer')],
    [('Component', 'Function', 'Protocol', 'Auth', 'Notes'),
     ('Arrays', 'Block/File/NFS', 'iSCSI/FC/NFS', 'CHAP/Kerberos', 'On-prem'),
     ('Apex Console', 'Provision/bill', 'HTTPS REST', 'SAML SSO', 'SaaS portal'),
     ('SCG', 'Telemetry relay', 'HTTPS', 'Certificate', 'Local VM'),
     ('CloudIQ', 'AIOps analytics', 'HTTPS', 'OAuth2', 'SaaS')],
    [('Apex STaaS', 'on-prem Dell storage consumed as a cloud service with subscription billing'),
     ('Apex Console', 'cloud portal; provision volumes, view usage, and raise support requests'),
     ('Committed base', 'minimum contracted capacity tier; billed monthly regardless of actual use'),
     ('Burst capacity', 'pre-installed unlocked storage above committed; billed when consumed'),
     ('SCG', 'Secure Connect Gateway; relays array telemetry to CloudIQ for analysis'),
     ('CloudIQ', 'Dell AIOps SaaS; health scores, capacity forecasts, firmware advisories'),
     ('NVMe tier', 'all-flash performance tier; sub-millisecond latency for database workloads'),
     ('Capacity tier', 'SAS/NL-SAS lower cost tier; suited to bulk storage and backup targets'),
     ('iSCSI CHAP', 'Challenge Handshake Auth Protocol; authenticates iSCSI initiators to array'),
     ('FC port sec.', 'FC fabric binding and port security; restricts which HBAs can log in'),
     ('vVols', 'Virtual Volumes; per-VM storage objects exposed via VASA provider to vCenter'),
     ('OOB mgmt', 'out-of-band management network for direct array controller access')])

reg('storage/dell/cloudiq',
    'Dell CloudIQ', 'CloudIQ',
    'AI-powered cloud storage management and analytics platform',
    'HTTPS REST API · SMTP alerts · SCG telemetry protocol',
    'CloudIQ SaaS (cloud-hosted) · SCG gateways on-prem · connected Dell arrays',
    'CloudIQ portal',
    ['CloudIQ SaaS', 'SCG gateway', 'Alert engine', 'REST API', 'Reporting'],
    [('Layer', 'Component', 'Function'),
     ('Collection', 'SCG adapter', 'Array telemetry'),
     ('Transport', 'HTTPS tunnel', 'Encrypted relay'),
     ('Analytics', 'AIOps engine', 'Health scoring'),
     ('Alerting', 'Email/webhook', 'Threshold rules'),
     ('Reporting', 'Capacity forecast', 'Trend analysis')],
    [('Component', 'Purpose', 'Config', 'Auth', 'Notes'),
     ('SCG gateway', 'Telemetry relay', 'On-prem VM', 'Certificate', 'One per site'),
     ('CloudIQ SaaS', 'Analytics portal', 'Managed SaaS', 'OAuth2', 'Dell-hosted'),
     ('REST API', 'Automation', 'Token-based', 'JWT', 'GraphQL also'),
     ('Alert engine', 'Notifications', 'Threshold rule', 'Email/webhook', 'Configurable')],
    [('CloudIQ', 'Dell SaaS AIOps; monitors PowerStore, Unity, PowerMax, PowerScale arrays'),
     ('SCG', 'Secure Connect Gateway; on-prem agent that relays telemetry to CloudIQ'),
     ('Health score', 'composite 0-100 metric for array wellness; drops when alert conditions fire'),
     ('Proactive rec.', 'AI-generated recommendations for firmware, config, and capacity actions'),
     ('Capacity IQ', 'CloudIQ module; forecasts when arrays will reach configured capacity thresholds'),
     ('Performance IQ', 'CloudIQ module; identifies latency anomalies and I/O bottlenecks over time'),
     ('Wellness', 'overall system health dashboard; aggregates all monitored arrays in one view'),
     ('API token', 'CloudIQ personal access token; use for REST and GraphQL API authentication'),
     ('Webhook alert', 'HTTP POST to external SIEM/ticketing endpoint on CloudIQ alert trigger'),
     ('Workload planner', 'CloudIQ tool for predicting impact of planned workload migrations'),
     ('Tag', 'user-defined key-value label applied to arrays for grouping and portal filtering'),
     ('Site', 'logical grouping of arrays by physical location within CloudIQ hierarchy')])

reg('storage/dell/cod',
    'Dell CoD', 'CoD',
    'Capacity on Demand — pre-installed unlocked via license purchase',
    'iSCSI · FC · REST API (activation)',
    'Dell array with CoD drives · Apex licensing portal · array management UI',
    'Unisphere / PowerStore Manager',
    ['CoD drives', 'License key', 'Apex billing', 'Array pool', 'Activation API'],
    [('Layer', 'Component', 'Notes'),
     ('Storage', 'CoD drives', 'Pre-installed'),
     ('License', 'Activation key', 'Unlocks cap.'),
     ('Billing', 'Per-TB/month', 'Burst model'),
     ('Pooling', 'Added to pool', 'Near-instant'),
     ('Scope', 'Block or File', 'Array-specific')],
    [('Component', 'Purpose', 'Access', 'Auth', 'Notes'),
     ('CoD drives', 'Locked capacity', 'Physical', 'N/A', 'Pre-installed'),
     ('License key', 'Activation code', 'Portal download', 'Entitlement', 'Per array SN'),
     ('Apex billing', 'Subscription', 'Apex Console', 'SAML SSO', 'Monthly'),
     ('Array pool', 'Storage pool', 'Unisphere/PSM', 'RBAC admin', 'Instant add')],
    [('CoD', 'Capacity on Demand; drives installed in factory, unlocked via license key purchase'),
     ('CoD drive', 'physically present but inaccessible NVMe/SAS drive; licensed to activate'),
     ('Activation key', 'license file from Dell portal; applied in array GUI, CLI, or REST API'),
     ('Committed cap.', 'baseline permanently licensed capacity; billed monthly without burst'),
     ('Burst cap.', 'CoD capacity above committed level; billed monthly when accessed'),
     ('Apex billing', 'subscription model for CoD; consumption-based monthly invoicing via portal'),
     ('Pooling', 'activated CoD capacity is added to existing storage pool immediately'),
     ('Graceful limit', 'array serves existing I/O but blocks new allocations at capacity limit'),
     ('Reclamation', 'returning CoD capacity requires contacting Dell to downgrade the license'),
     ('FAST VP', 'Fully Automated Storage Tiering; moves data between tiers when CoD is active'),
     ('Unisphere', 'Dell Unity XT GUI; used to view CoD drive status and apply activation keys'),
     ('REST API', 'CoD activation via PowerStore REST or Unisphere REST API endpoints')])

reg('storage/dell/data-domain',
    'Dell Data Domain', 'Data Domain',
    'purpose-built deduplication backup appliance and target',
    'DD Boost · NFS · CIFS · iSCSI · FC · NDMP',
    'Data Domain appliance (DD3300/6400/9800) · replication WAN · backup application servers',
    'DDMC / DD System Manager',
    ['DD appliance', 'DD Boost', 'DDMC', 'DD Replicator', 'MTREE'],
    [('Layer', 'Component', 'Function'),
     ('Data path', 'DD Boost client', 'Client-side dedup'),
     ('Appliance', 'DD engine', '15-55x dedup'),
     ('Replication', 'DD Replicator', 'Async MTREE'),
     ('Management', 'DDMC', 'Central console'),
     ('Cloud', 'DD Cloud Tier', 'Object archive')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('DD Boost', 'Offload dedup', 'DD Boost lib', 'Cert/password', 'Client-side'),
     ('MTREE', 'Data container', 'NFS/CIFS/Boost', 'RBAC', 'Per backup job'),
     ('DD Replicator', 'DR replication', 'Encrypted TCP', 'Certificate', 'Async'),
     ('DDMC', 'Central mgmt', 'HTTPS', 'LDAP/local', 'Multi-DD')],
    [('DD Boost', 'client-side dedup library; shifts dedup processing to backup client hosts'),
     ('MTREE', 'logical data container on Data Domain; backup jobs target a specific MTREE'),
     ('DD Replicator', 'async MTREE replication between DD systems; source and destination must match'),
     ('DDMC', 'Data Domain Management Center; centrally manages multiple DD appliances'),
     ('Cloud Tier', 'inactive backup data tiered to S3/Azure Blob/GCS object storage automatically'),
     ('Dedup ratio', 'deduplicated size / original size; 20:1 typical for mixed backup workloads'),
     ('Active Tier', 'high-performance SSD/HDD tier holding recent backup data on the appliance'),
     ('NDMP', 'Network Data Management Protocol; NAS backup without requiring a host agent'),
     ('VTL', 'Virtual Tape Library; DD emulates tape drives for legacy backup software compatibility'),
     ('Retention Lock', 'WORM protection on MTREE data; prevents deletion for a configured period'),
     ('FastCopy', 'efficient space-saving internal copy of MTREE data with no physical data movement'),
     ('Encryption', 'AES-256 at rest; FIPS 140-2 certified models available for compliance')])

reg('storage/dell/ecs',
    'Dell ECS', 'ECS',
    'Elastic Cloud Storage enterprise S3-compatible object platform',
    'S3 · Azure Blob API · Swift · Atmos · NFS (via gateway) · HDFS',
    'ECS appliance nodes · 10/25 GbE backend network · commodity SAS drives',
    'ECS Management Portal / REST API',
    ['ECS nodes', 'Storage pools', 'VDCs', 'Replication groups', 'Buckets'],
    [('Layer', 'Component', 'Notes'),
     ('Node', 'x86 appliance', 'Shared-nothing'),
     ('Storage pool', 'Node group', 'Erasure coded'),
     ('VDC', 'Virtual DC', 'Per-site unit'),
     ('Rep. group', 'Multi-VDC', 'Geo redundancy'),
     ('Bucket', 'Object container', 'S3/Swift/Blob')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Storage pool', 'Drive aggregation', 'Internal', 'N/A', 'Erasure 12+4'),
     ('VDC', 'Site grouping', 'Internal', 'N/A', 'HA per site'),
     ('Bucket', 'Object namespace', 'S3/Swift/Blob', 'S3 keys/IAM', 'Per tenant'),
     ('Replication grp', 'Geo replication', 'ECS protocol', 'Certificate', '3-way geo')],
    [('ECS', 'Elastic Cloud Storage; Dell S3-compatible object store for unstructured data'),
     ('VDC', 'Virtual Data Center; group of ECS nodes at a single geographic site'),
     ('Storage pool', 'collection of nodes within a VDC; defines the erasure coding domain'),
     ('Replication group', 'links VDCs for geo-redundant object storage; 3-way replication'),
     ('Bucket', 'top-level S3 namespace; equivalent to S3 bucket or Azure container'),
     ('Erasure coding', 'data protection scheme; default 12+4 provides 4-drive fault tolerance'),
     ('Namespace', 'tenant-level isolation; multiple tenants share a single ECS cluster'),
     ('CAS', 'Content Addressed Storage; fixed-content object storage with WORM support'),
     ('Replication factor', 'number of VDC copies; 3-way geo-replication for maximum durability'),
     ('Atmos API', 'legacy Dell Atmos-compatible API; supported for migration from Atmos systems'),
     ('HDFS connector', 'ECS Hadoop connector; ECS appears as HDFS namespace for analytics jobs'),
     ('Quota', 'per-namespace or per-bucket storage quota; enforced as hard or soft limit')])

reg('storage/dell/fod',
    'Dell FoD', 'FoD',
    'Feature on Demand — software features unlocked via license keys',
    'REST API · HTTPS (license portal) · array management UI',
    'Dell array with FoD-capable firmware · Dell licensing portal · array management',
    'Dell License Manager / array CLI',
    ['FoD license', 'Array firmware', 'License portal', 'Feature module', 'Audit log'],
    [('Layer', 'Component', 'Notes'),
     ('License type', 'Permanent/Term', 'Feature-specific'),
     ('Activation', 'Key → array', 'Instant unlock'),
     ('Scope', 'Per-array SN', 'Non-transferable'),
     ('Features', 'Replication/Tier', 'Product-defined'),
     ('Audit', 'License report', 'Compliance')],
    [('Component', 'Purpose', 'Access', 'Auth', 'Notes'),
     ('FoD license', 'Feature unlock', 'Portal download', 'Entitlement', 'Array-bound'),
     ('License portal', 'Purchase/track', 'HTTPS', 'SSO login', 'licensing.dell.com'),
     ('Array firmware', 'FoD enforcement', 'Array mgmt', 'Admin role', 'Validates key'),
     ('Audit report', 'Compliance check', 'DDMC/array', 'Read-only', 'Monthly review')],
    [('FoD', 'Feature on Demand; software capabilities locked in firmware, unlocked by license key'),
     ('License key', 'alphanumeric string generated at purchase; applied via GUI, CLI, or REST API'),
     ('Permanent license', 'perpetual feature unlock; tied to specific array serial number'),
     ('Term license', 'time-limited feature unlock; expires unless renewed through Dell portal'),
     ('Entitlement', 'purchased right to use a feature; tracked in Dell software licensing portal'),
     ('License transfer', 'FoD licenses are non-transferable between different array serial numbers'),
     ('Replication FoD', 'unlocks synchronous or asynchronous array replication features'),
     ('Tier FoD', 'unlocks FAST VP or cloud tiering between performance and capacity tiers'),
     ('License audit', 'periodic reconciliation of active features versus licensed entitlements'),
     ('LicenseManager', 'Dell tool for bulk license management across multiple array systems'),
     ('Array serial', 'unique array identifier; FoD licenses are cryptographically bound to it'),
     ('FoD portal', 'licensing.dell.com; purchase, download, and track all FoD license keys')])

reg('storage/dell/powermax',
    'Dell PowerMax', 'PowerMax',
    'high-end enterprise NVMe all-flash array for mission-critical workloads',
    'FC · iSCSI · NVMe-oF · SRDF (replication)',
    'PowerMax 2500/8500 engine · FE/BE/RDF directors · DRAM cache · expansion bays',
    'Unisphere for PowerMax / Solutions Enabler',
    ['Unisphere', 'Solutions Enabler', 'SRDF', 'TimeFinder SnapVX', 'Storage Groups'],
    [('Layer', 'Component', 'Function'),
     ('Cache', 'DRAM 2 TB+', 'Sub-ms latency'),
     ('FE director', 'FC/iSCSI ports', 'Host facing'),
     ('BE director', 'NVMe drives', 'Storage facing'),
     ('SRDF', 'RDF director', 'Metro/remote DR'),
     ('TimeFinder', 'SnapVX/Clone', 'Local protection')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('SRDF Sync', 'Zero-RPO DR', 'RDF protocol', 'Certificate', 'Metro <200ms'),
     ('SRDF Async', 'Near-zero RPO', 'RDF protocol', 'Certificate', 'Any distance'),
     ('TimeFinder', 'Local snapshots', 'Internal', 'Solutions Enabler', '256 snaps/SG'),
     ('Solutions Enabler', 'CLI/API mgmt', 'HTTPS/symcli', 'Certificate', 'Symm CLI')],
    [('PowerMax', 'Dell flagship NVMe all-flash array; millions of IOPS at sub-millisecond latency'),
     ('SRDF', 'Symmetrix Remote Data Facility; sync/async metro and remote site replication'),
     ('TimeFinder SnapVX', 'space-efficient snapshot technology; up to 256 snapshots per storage group'),
     ('Storage group', 'logical container for volumes sharing service level and host access policy'),
     ('Service level', 'performance target for a storage group: Diamond, Platinum, Gold, Silver'),
     ('FE director', 'front-end director providing FC or iSCSI host-facing ports on the engine'),
     ('BE director', 'back-end director connecting engine cache to NVMe flash drive bays'),
     ('RDF director', 'SRDF director providing dedicated bandwidth for replication traffic'),
     ('Solutions Enabler', 'CLI and API toolkit; symcli commands cover all PowerMax management'),
     ('Unisphere', 'web GUI and REST API server for PowerMax; unified management interface'),
     ('DCM', 'Dynamic Cache Management; auto-balances workloads across available cache resources'),
     ('Service level obj.', 'workload performance class assigned to storage group; enforced by DPTM')])

reg('storage/dell/powerpath',
    'Dell PowerPath', 'PowerPath',
    'multipath I/O host software for Dell storage arrays',
    'FC · iSCSI · NVMe-oF',
    'Host OS (Windows/Linux) · HBA or iSCSI NIC ports · FC/IP switches · Dell arrays',
    'powermt CLI / PowerPath Management Appliance',
    ['powermt daemon', 'HBA driver', 'Pseudo device', 'Path policy', 'pp_mgmt'],
    [('Layer', 'Component', 'Notes'),
     ('Driver', 'powermt daemon', 'OS-level'),
     ('Paths', 'Active-active', '≥4 paths/LUN'),
     ('Policy', 'Adaptive/ALUA', 'Array-specific'),
     ('Failover', 'Auto reroute', '<5 sec RTO'),
     ('Management', 'pp_mgmt', 'Centralised')],
    [('Component', 'Purpose', 'Command', 'Notes', 'Frequency'),
     ('powermt display', 'Show path state', 'powermt display dev=all', 'Active/dead', 'Daily check'),
     ('powermt check', 'Refresh paths', 'powermt check', 'After changes', 'Post-zoning'),
     ('powermt config', 'Apply license', 'powermt config license', 'Per host', 'Install time'),
     ('pp_mgmt', 'Central monitor', 'Web UI', 'Optional', 'Multi-host')],
    [('PowerPath', 'Dell multipath driver; manages multiple I/O paths to storage for HA/performance'),
     ('powermt', 'CLI utility; powermt display, powermt check, powermt save are core commands'),
     ('Pseudo device', 'virtual block device created by PowerPath aggregating physical I/O paths'),
     ('Path health', 'alive or dead status per path; dead paths trigger automatic I/O failover'),
     ('Adaptive policy', 'load-balancing that distributes I/O across all active paths evenly'),
     ('CLARiiON policy', 'active/passive policy for older VNX/CLARiiON arrays (one active path)'),
     ('ALUA', 'Asymmetric Logical Unit Access; array signals preferred vs. non-preferred paths'),
     ('Trespass', 'LUN ownership movement between SP-A and SP-B on Unity or VNX arrays'),
     ('Ghost path', 'stale path entry in PowerPath no longer backed by a physical device'),
     ('powermt check', 'validates all paths and refreshes device table; run after fabric changes'),
     ('pp_mgmt', 'PowerPath Management Appliance; central monitoring for all PowerPath hosts'),
     ('License key', 'host-based license required per server; applied via powermt config license')])

reg('storage/dell/powerscale',
    'Dell PowerScale', 'PowerScale',
    'scale-out NAS platform (Isilon) for unstructured and file workloads',
    'NFS v3/v4.1 · SMB · HDFS · S3 · Swift · FTP',
    'PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend',
    'OneFS WebUI / isi CLI',
    ['OneFS OS', 'SmartPools', 'SyncIQ', 'SnapshotIQ', 'SmartConnect'],
    [('Layer', 'Component', 'Function'),
     ('OS', 'OneFS', 'Distributed FS'),
     ('Tiering', 'SmartPools', 'Auto data move'),
     ('Replication', 'SyncIQ', 'Async DR copy'),
     ('Snapshots', 'SnapshotIQ', 'Space-efficient'),
     ('Load balance', 'SmartConnect', 'DNS client dist.')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('OneFS', 'Distributed filesystem', 'NFS/SMB/S3/HDFS', 'Kerberos/NTLM', 'Single namespace'),
     ('SmartPools', 'Tiering policy', 'Internal', 'Admin role', 'Auto data move'),
     ('SyncIQ', 'Async replication', 'Encrypted TCP', 'Certificate', 'Policy-based'),
     ('SnapshotIQ', 'Snapshots', 'Internal', 'Admin role', 'Per directory')],
    [('OneFS', 'Dell PowerScale distributed filesystem OS; all nodes share a single namespace'),
     ('SmartPools', 'tiering engine; moves files between All-Flash, Hybrid, and Archive tiers'),
     ('SyncIQ', 'async replication to DR cluster; RPO-based schedule; failover in minutes'),
     ('SnapshotIQ', 'space-efficient snapshots; accessed via .snapshot directory in each share'),
     ('SmartConnect', 'DNS-based load balancing; distributes NFS/SMB client connections across nodes'),
     ('Access zone', 'logical container with separate authentication and export namespace per tenant'),
     ('Quota', 'directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ'),
     ('CloudPools', 'tiering to cloud object storage (S3/Blob); data remains accessible locally'),
     ('isi CLI', 'OneFS command-line interface; all management operations available via isi commands'),
     ('Node pool', 'group of same-model nodes sharing protection domain for data distribution'),
     ('Protection level', 'N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated'),
     ('File pool policy', 'rule-based policy assigning files to specific node pools or storage tiers')])

reg('storage/dell/powerstore',
    'Dell PowerStore', 'PowerStore',
    'mid-range NVMe all-flash array with unified block and file capability',
    'FC · iSCSI · NVMe-oF · NFS · SMB · REST API',
    'PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE',
    'PowerStore Manager / REST API',
    ['PowerStore Manager', 'Volume groups', 'Protection policies', 'Metro', 'Snapshots'],
    [('Layer', 'Component', 'Notes'),
     ('T-model', 'Block only', 'iSCSI/FC/NVMe'),
     ('X-model', 'Block + File', 'Unified protocol'),
     ('Metro', 'Sync replication', 'Zero-RPO stretch'),
     ('Protection', 'Snapshot/Clone', 'Immutable snaps'),
     ('Mgmt', 'PSM / REST', 'Unified pane')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Volume group', 'Logical container', 'iSCSI/FC', 'Host group', 'Shared policy'),
     ('Protection policy', 'Snapshot/repl rule', 'Internal', 'Admin role', 'Per volume'),
     ('Metro volume', 'Sync replication', 'Internal RPC', 'Certificate', 'Zero RPO'),
     ('Snapshot', 'PiT copy', 'Internal', 'Admin role', 'Space-efficient')],
    [('PowerStore', 'Dell mid-range NVMe storage; T-model block-only, X-model unified block+file'),
     ('PowerStore Manager', 'browser GUI and REST API endpoint for all PowerStore operations'),
     ('Volume group', 'logical collection of volumes sharing snapshot and replication policies'),
     ('Protection policy', 'assigned to volumes; defines snapshot schedule, retention, and replication'),
     ('Metro volume', 'synchronously replicated volume across two sites; zero RPO active-active'),
     ('Snapshot', 'space-efficient point-in-time copy; crash-consistent or app-consistent'),
     ('Clone', 'full writable copy of a volume or file system; independent lifecycle'),
     ('Applied-to', 'PowerStore host mapping; volumes are applied-to a host or host group object'),
     ('Capacity license', 'PowerStore uses usable-capacity licensing; licensed in TiB increments'),
     ('Storage container', 'PowerStore X-model; unified block and file from the same storage pool'),
     ('Appliance', 'single PowerStore node pair (dual controllers); scalable to 4 appliances'),
     ('NVMe-oF', 'NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore')])

reg('storage/dell/secure-connect-gateway',
    'Dell SCG', 'SCG',
    'Secure Connect Gateway — telemetry relay for Dell support and CloudIQ',
    'HTTPS outbound only · REST API (local) · SMTP alerts',
    'SCG VM or appliance on-prem · outbound HTTPS to Dell · connected storage arrays',
    'SCG WebUI port 9443 / REST API',
    ['SCG gateway', 'Array adapters', 'CloudIQ relay', 'Support tunnel', 'Alert engine'],
    [('Layer', 'Component', 'Notes'),
     ('Collection', 'Array adapters', 'Per product'),
     ('Transport', 'HTTPS outbound', 'No inbound'),
     ('CloudIQ feed', 'Telemetry relay', 'Near real-time'),
     ('Support tunnel', 'Remote assist', 'On-demand only'),
     ('Alerting', 'Email/syslog', 'Threshold rules')],
    [('Component', 'Purpose', 'Port', 'Auth', 'Notes'),
     ('SCG gateway', 'Telemetry hub', '9443 (local)', 'Certificate', 'VM or appliance'),
     ('Array adapter', 'Product connect', 'Array API', 'Service acct', 'Per product type'),
     ('CloudIQ relay', 'Health/perf feed', 'HTTPS 443', 'Certificate', 'Dell-hosted'),
     ('Support tunnel', 'TAC remote', 'HTTPS 443', 'One-time token', 'On-demand')],
    [('SCG', 'Secure Connect Gateway; replaces ESRS as Dell remote support relay platform'),
     ('ESRS', 'EMC Secure Remote Services; predecessor to SCG; still supported on older arrays'),
     ('Adapter', 'SCG component connecting to a specific array type: Unity, PowerStore, PowerMax'),
     ('CloudIQ relay', 'SCG forwards array health telemetry to CloudIQ SaaS for analytics'),
     ('Support tunnel', 'Dell TAC can open an encrypted on-demand remote session via SCG'),
     ('Device registration', 'arrays registered in SCG; SCG authenticates to Dell support portal'),
     ('Site', 'SCG logical grouping of arrays at a physical location within the organisation'),
     ('Policy', 'SCG alert policy; defines which events trigger email or syslog notifications'),
     ('SCG bundle', 'log/diagnostic collection submitted to Dell support via SCG upload'),
     ('Gateway HA', 'two SCG instances in active-active; both relay telemetry independently'),
     ('Port 9443', 'SCG local management UI port; REST API also served on port 9443'),
     ('Outbound only', 'SCG connections are outbound HTTPS; no inbound firewall rules required')])

reg('storage/dell/unity',
    'Dell Unity XT', 'Unity XT',
    'unified mid-range storage — block, file, and VMware vVols integration',
    'FC · iSCSI · NFS · SMB · REST API',
    'Unity XT 380F/480F/680F/880F · dual SPs · DPE/DAE expansion · 10/25 GbE',
    'Unisphere / UEMCLI',
    ['Unisphere', 'Storage Pools', 'NAS Servers', 'Snapshots', 'RecoverPoint'],
    [('Layer', 'Component', 'Notes'),
     ('Ctrl', 'SP-A + SP-B', 'Cache mirrored'),
     ('Pool', 'Dynamic FAST VP', 'Auto-tiering'),
     ('NAS server', 'File protocols', 'Per-tenant'),
     ('Snapshot', 'Writable snaps', 'Thin PiT copy'),
     ('Replication', 'Async/Metro', 'Native or RP4VM')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Unisphere', 'GUI / REST API', 'HTTPS', 'LDAP/local', 'SP-hosted'),
     ('UEMCLI', 'CLI management', 'SSH / HTTPS', 'Local admin', 'All operations'),
     ('NAS server', 'File services', 'NFS/SMB', 'Kerberos/NTLM', 'Virtual file server'),
     ('RecoverPoint', 'Continuous protect', 'Encrypted TCP', 'Certificate', 'Journal CDP')],
    [('Unity XT', 'Dell unified mid-range array; block LUNs, file NAS, and VMware vVols'),
     ('Unisphere', 'HTML5 GUI and REST API for Unity XT management; SP-hosted management portal'),
     ('UEMCLI', 'CLI for Unity XT; uemcli -d <ip> -u admin -p <pw> /show commands'),
     ('Storage pool', 'collection of drives forming a usable pool; FAST VP tiers data automatically'),
     ('FAST VP', 'Fully Automated Storage Tiering VP; moves hot and cold data between tiers'),
     ('NAS server', 'virtual file server on Unity; each has its own IP, DNS, and CIFS/NFS shares'),
     ('Data Mover', 'older EMC term for NAS server; used in VNX and early Unity documentation'),
     ('SP-A / SP-B', 'storage processors; active-active HA pair with mirrored cache'),
     ('Snapshot', 'space-efficient PiT copy of LUN or FS; writable snapshots supported'),
     ('RecoverPoint', 'RP4VM; journal-based continuous data protection for Unity volumes'),
     ('Metro', 'synchronous replication between two Unity XT sites; active-active zero RPO'),
     ('vVols', 'Virtual Volumes; VASA provider exposes per-VM storage objects to vCenter')])

reg('storage/dell/vplex',
    'Dell VPLEX', 'VPLEX',
    'federated storage virtualisation and active-active cross-site clustering',
    'FC · iSCSI',
    'VPLEX VS2/VS6 appliance · FC fabric · backend arrays · WAN link (Metro/Geo)',
    'VPLEX Management Server / vplex CLI',
    ['Management Server', 'Engines', 'Virtual volumes', 'WAN-COM', 'Witness'],
    [('Layer', 'Component', 'Notes'),
     ('Virtualisation', 'Backend LUNs', 'Abstracted to VVs'),
     ('Metro', 'Sync stretch', '<5ms RTT sites'),
     ('Geo', 'Async replication', 'Any distance'),
     ('Clustering', 'Active-active', 'Shared namespace'),
     ('Quorum', 'Witness VM', 'Split-brain guard')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Virtual volume', 'Virtualised LUN', 'FC/iSCSI', 'FC zoning', 'Multi-vendor'),
     ('Metro cluster', 'Sync stretch', 'Inter-cluster', 'Certificate', '2-site max'),
     ('Witness', 'Quorum arbiter', 'HTTPS', 'Certificate', '3rd site'),
     ('WAN-COM', 'Geo replication', 'Encrypted WAN', 'Certificate', 'Geo only')],
    [('VPLEX', 'Dell storage federation; aggregates arrays into virtual volumes across vendors'),
     ('Virtual volume', 'VPLEX-abstracted LUN presented to hosts; backend is array LUNs'),
     ('VPLEX Metro', 'synchronous active-active stretch cluster; same VV served from two sites'),
     ('VPLEX Geo', 'asynchronous active-active replication; higher RPO, no distance constraint'),
     ('Distributed VV', 'virtual volume spanning two sites for Metro active-active host access'),
     ('Witness', 'third-site quorum arbiter for Metro; prevents split-brain island scenarios'),
     ('WAN-COM', 'WAN communication module in VPLEX Geo; manages inter-site replication traffic'),
     ('Management Server', 'embedded Linux VM in VPLEX engine; serves web UI and vplex CLI'),
     ('Consistency group', 'set of virtual volumes that failover together maintaining write order'),
     ('Backend volume', 'LUN from underlying array presented to VPLEX engine for virtualisation'),
     ('Local device', 'RAID device or extent of backend volumes on a single VPLEX cluster'),
     ('Cluster', 'single VPLEX installation; Metro topology requires exactly two clusters')])

# ── NetApp Storage ────────────────────────────────────────────────────────────
reg('storage/netapp/keystone',
    'NetApp Keystone', 'Keystone',
    'Storage as a Service subscription for on-prem NetApp arrays',
    'NFS · iSCSI · FC · S3 · SMB',
    'NetApp AFF/FAS arrays on-prem · Keystone Collector VM · BlueXP cloud portal',
    'Keystone dashboard (BlueXP)',
    ['Keystone Collector', 'BlueXP', 'Service levels', 'Burst meter', 'AutoSupport'],
    [('Layer', 'Component', 'Notes'),
     ('Hardware', 'AFF/FAS on-prem', 'NetApp-owned'),
     ('Service level', 'Extreme/Perf/Std', 'Latency SLA'),
     ('Collector', 'Telemetry VM', 'ONTAP polling'),
     ('Dashboard', 'BlueXP', 'Usage visibility'),
     ('Billing', 'Committed+burst', 'Monthly invoice')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Keystone Collector', 'Usage metering', 'ONTAP REST', 'Service account', 'On-prem VM'),
     ('BlueXP', 'SaaS portal', 'HTTPS', 'OAuth2/SSO', 'NetApp SaaS'),
     ('AFF Extreme', 'NVMe perf tier', 'FC/iSCSI/NFS', 'Kerberos/CHAP', 'Sub-ms latency'),
     ('AutoSupport', 'Telemetry relay', 'HTTPS', 'Certificate', 'Call-home')],
    [('Keystone', 'NetApp STaaS; fixed-term subscription for ONTAP or StorageGRID capacity'),
     ('Service level', 'tiered SLA: Extreme (NVMe), Performance (SSD), Standard (HDD)'),
     ('Committed capacity', 'minimum contracted TiB; billed monthly even if below threshold'),
     ('Burst capacity', 'usage above committed; available without pre-ordering; billed monthly'),
     ('Keystone Collector', 'on-prem VM that gathers usage metrics and sends to NetApp Keystone'),
     ('BlueXP', 'NetApp SaaS control plane; Keystone dashboard, DRaaS, and cloud integrations'),
     ('AFF', 'All Flash FAS; ONTAP-based NVMe/SSD array used for Extreme and Performance tiers'),
     ('FAS', 'Fabric Attached Storage; ONTAP hybrid HDD/SSD for Standard service level'),
     ('StorageGRID', 'NetApp S3 object storage; Object service level in Keystone subscriptions'),
     ('AutoSupport', 'ONTAP telemetry relay; sends call-home data and log bundles to NetApp'),
     ('Service request', 'NetApp SR; support ticket opened via mysupport.netapp.com portal'),
     ('SKU', 'Keystone service SKU identifies the service level and raw or usable capacity')])

reg('storage/netapp/ontap',
    'NetApp ONTAP', 'ONTAP',
    'enterprise unified storage operating system for NAS, SAN, and object',
    'NFS v3/v4.1 · SMB · iSCSI · FC · NVMe-oF · S3',
    'AFF/FAS HA node pairs · cluster network · client access network · MetroCluster',
    'ONTAP System Manager / ONTAP CLI',
    ['System Manager', 'ONTAP CLI', 'SnapMirror', 'FlexClone', 'ONTAP S3'],
    [('Layer', 'Component', 'Notes'),
     ('Cluster', 'HA node pairs', 'Scale-out'),
     ('SVM', 'Virtual server', 'Protocol access'),
     ('Aggregate', 'RAID groups', 'Storage pool'),
     ('FlexVol', 'Thin volume', 'Data container'),
     ('SnapMirror', 'Replication', 'Async/Sync')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('SVM', 'Tenant isolation', 'All protocols', 'Kerberos/NTLM', 'Virtual server'),
     ('SnapMirror', 'DR replication', 'SM protocol', 'Certificate', 'Async or sync'),
     ('FlexClone', 'Instant clone', 'Internal', 'Admin role', 'Space-efficient'),
     ('SM-BC', 'Zero-RPO active-active', 'SM protocol', 'Mediator', 'SAN only')],
    [('ONTAP', 'NetApp storage OS; unified NAS, SAN, and object across AFF, FAS, ONTAP Select'),
     ('SVM', 'Storage Virtual Machine; logical storage server with protocols, IP, and volumes'),
     ('Aggregate', 'RAID group of disks; underpins FlexVols and FlexGroups within a node'),
     ('FlexVol', 'flexible thin-provisioned volume within an aggregate; most common container'),
     ('FlexGroup', 'scale-out volume spanning multiple aggregates; for very large NAS workloads'),
     ('SnapMirror', 'async or synchronous replication between ONTAP systems for DR and backup'),
     ('SnapVault', 'backup-oriented SnapMirror variant; independent retention at destination'),
     ('FlexClone', 'instant space-efficient writable clone of a volume or LUN from snapshot'),
     ('Snapshot', 'ONTAP space-efficient PiT copy; stored in .snapshot directory on NFS'),
     ('ONTAP Mediator', 'third-site quorum for SnapMirror SM-BC; prevents split-brain scenarios'),
     ('SM-BC', 'SnapMirror Business Continuity; synchronous zero-RPO active-active SAN replication'),
     ('vserver', 'ONTAP CLI name for SVM; vserver show and vserver nfs show are common commands')])

reg('storage/netapp/operations',
    'NetApp Operations', 'NetApp Ops',
    'NetApp storage platform operational support and administration procedures',
    'HTTPS · SSH · SNMP · AutoSupport · REST API',
    'NetApp AFF/FAS clusters · ActiveIQ SaaS · mysupport.netapp.com support portal',
    'ActiveIQ / mysupport.netapp.com',
    ['ActiveIQ', 'AutoSupport', 'System Manager', 'ONTAP CLI', 'Support portal'],
    [('Layer', 'Component', 'Notes'),
     ('Monitoring', 'ActiveIQ', 'Risk assessment'),
     ('Telemetry', 'AutoSupport', 'Call-home relay'),
     ('Health check', 'Config Advisor', 'Best practice'),
     ('Support', 'mysupport.netapp.com', 'SR management'),
     ('Upgrade', 'NDO rolling', 'Non-disruptive')],
    [('Component', 'Purpose', 'Access', 'Auth', 'Notes'),
     ('ActiveIQ', 'Health portal', 'HTTPS', 'NetApp SSO', 'SaaS'),
     ('AutoSupport', 'Call-home', 'HTTPS/email', 'Certificate', 'Daily reports'),
     ('Config Advisor', 'Best practice', 'Local tool', 'Local admin', 'Point-in-time'),
     ('ONTAP Upgrade', 'Version mgmt', 'System Manager', 'Admin role', 'Rolling NDO')],
    [('ActiveIQ', 'NetApp SaaS health portal; risk assessment, upgrade advisor, capacity planning'),
     ('AutoSupport', 'ONTAP telemetry; sends daily health reports and call-home bundles to NetApp'),
     ('Config Advisor', 'NetApp best-practice checker; validates cabling, config, and firmware'),
     ('NDO', 'Non-Disruptive Operations; rolling upgrades without host I/O service disruption'),
     ('Takeover', 'HA failover; one node takes over partner storage on node failure event'),
     ('Giveback', 'return storage to original node after failover; completes HA pair recovery'),
     ('Aggregate relocation', 'move aggregate between HA pair nodes without service disruption'),
     ('LIF migration', 'move logical interface to different node port during planned maintenance'),
     ('System Manager', 'ONTAP web GUI; unified management for cluster, SVMs, volumes, policies'),
     ('ONTAP CLI', 'SSH to cluster management IP; diag privilege required for low-level commands'),
     ('mysupport', 'mysupport.netapp.com; open SRs, download firmware, and access knowledge base'),
     ('ASUP bundle', 'AutoSupport bundle with logs, config, and core files for TAC case analysis')])

reg('storage/netapp/snapcenter',
    'NetApp SnapCenter', 'SnapCenter',
    'centralised backup and recovery orchestration for NetApp storage',
    'HTTPS · iSCSI · FC · NFS · SMB',
    'SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers',
    'SnapCenter GUI / REST API',
    ['SnapCenter Server', 'DB plug-ins', 'VMware plug-in', 'Policies', 'Resource groups'],
    [('Layer', 'Component', 'Notes'),
     ('Server', 'Windows VM', 'Central control'),
     ('Plug-in', 'Host agent', 'App-consistent'),
     ('Policy', 'Schedule/retain', 'Backup rule'),
     ('Resource group', 'Grouped targets', 'Shared policy'),
     ('Recovery', 'Volume/LUN/file', 'Granular restore')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('SQL plug-in', 'MSSQL backups', 'HTTPS', 'Windows auth', 'App-consistent'),
     ('Oracle plug-in', 'Oracle backups', 'HTTPS', 'SSH', 'RMAN integration'),
     ('VMware plug-in', 'VM/VMDK backup', 'HTTPS/vCenter', 'vCenter SSO', 'vSphere API'),
     ('SAP HANA plug-in', 'HANA backups', 'HTTPS', 'SAP auth', 'Backint API')],
    [('SnapCenter', 'NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins'),
     ('Plug-in', 'host-side agent; quiesces application before snapshot: SQL, Oracle, VMware'),
     ('Resource group', 'set of resources sharing a backup policy and schedule in SnapCenter'),
     ('Policy', 'SnapCenter object defining snapshot frequency, retention, and replication target'),
     ('App-consistent', 'snapshot taken after DB quiesce; guarantees crash-consistent recovery'),
     ('Clone lifecycle', 'SnapCenter clone: create from snapshot, provision to host, then delete'),
     ('FlexClone', 'underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone'),
     ('Vault policy', 'SnapCenter policy that also replicates snapshots to SnapVault destination'),
     ('Mirror policy', 'SnapCenter policy that replicates snapshots via SnapMirror to DR cluster'),
     ('RBAC', 'SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles'),
     ('SMF', 'SnapCenter MySQL database storing job history, policies, and resource configs'),
     ('SnapCenter API', 'REST API on port 8143; full feature coverage for automation workflows')])

reg('storage/netapp/snapmirror',
    'NetApp SnapMirror', 'SnapMirror',
    'ONTAP replication technology for DR, backup, and business continuity',
    'SnapMirror protocol (encrypted) · NFS/SMB/iSCSI at destination after break',
    'Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link',
    'ONTAP System Manager / SnapMirror CLI',
    ['Intercluster LIFs', 'SnapMirror engine', 'Mediator', 'SM-BC', 'SnapVault'],
    [('Layer', 'Component', 'Notes'),
     ('Async', 'Periodic sync', 'RPO: minutes'),
     ('Sync', 'Zero RPO', 'Sub-ms lag'),
     ('SM-BC', 'Active-active', 'Transparent FO'),
     ('Vault', 'Long retention', 'Backup copy'),
     ('Cloud', 'ONTAP → CVO', 'Cloud DR/backup')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Async SnapMirror', 'DR replication', 'SM protocol', 'Certificate', 'RPO minutes'),
     ('Sync SnapMirror', 'Zero-RPO sync', 'SM protocol', 'Certificate', 'StrictSync/Sync'),
     ('SM-BC', 'Active-active SAN', 'SM protocol', 'Mediator', 'No RPO/RTO'),
     ('SnapVault', 'Backup retention', 'SM protocol', 'Certificate', 'Longer retention')],
    [('SnapMirror', 'ONTAP replication; transfers only changed blocks after initial baseline sync'),
     ('Intercluster LIF', 'dedicated logical interface for SnapMirror traffic between clusters'),
     ('SnapMirror policy', 'defines schedule, retention, and transfer type (async/sync/vault)'),
     ('Baseline transfer', 'first full snapshot transfer establishing the SnapMirror relationship'),
     ('Update', 'incremental transfer; only sends new or changed blocks since last successful sync'),
     ('Snapmirror break', 'breaks the DR relationship; activates destination volume for read-write'),
     ('Resync', 're-establishes a broken SnapMirror relationship from the last common snapshot'),
     ('SM-BC', 'SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes'),
     ('Mediator', 'ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site'),
     ('SnapVault', 'SnapMirror variant for backup retention; destination has independent schedule'),
     ('MirrorAndVault', 'policy combining SnapMirror DR and SnapVault backup retention copies'),
     ('Fanout', 'single source volume replicating to multiple destination clusters simultaneously')])

# ── Pure Storage ──────────────────────────────────────────────────────────────
reg('storage/pure/evergreen-one',
    'Pure Evergreen//ONE', 'Evergreen//ONE',
    'Storage as a Service subscription delivered on Pure FlashArray/FlashBlade',
    'FC · iSCSI · NVMe-oF · NFS · SMB · S3',
    'Pure FlashArray or FlashBlade on-prem (Pure-owned) · Pure1 cloud · WAN to Pure',
    'Pure1 / Purity REST API',
    ['Pure1 SaaS', 'FlashArray', 'FlashBlade', 'Hardware refresh', 'Support'],
    [('Layer', 'Component', 'Notes'),
     ('Hardware', 'On-prem Pure', 'Pure-owned'),
     ('Billing', 'Committed TiB', 'Monthly sub.'),
     ('Refresh', 'Non-disruptive', 'Pure delivers'),
     ('Management', 'Pure1 SaaS', 'AI analytics'),
     ('Support', '24x7 proactive', 'AI-driven')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('Pure1', 'SaaS portal', 'HTTPS', 'SSO/SAML', 'AI analytics'),
     ('FlashArray', 'Block/file', 'FC/iSCSI/NFS', 'CHAP/Kerberos', 'All-NVMe'),
     ('FlashBlade', 'File/object', 'NFS/SMB/S3', 'Kerberos/IAM', 'Parallel I/O'),
     ('ActiveCluster', 'Sync replication', 'Internal RPC', 'Certificate', 'Zero RPO')],
    [('Evergreen//ONE', 'Pure STaaS; Pure-owned hardware on customer premises with subscription billing'),
     ('Pure1', 'Pure Storage cloud management portal; AI-based analytics and capacity planning'),
     ('Non-disruptive upgrade', 'hardware upgrade without host I/O interruption; Pure handles logistics'),
     ('Committed TiB', 'minimum subscribed capacity; billed monthly regardless of actual usage'),
     ('Burst capacity', 'additional capacity above commitment; no pre-ordering; billed as consumed'),
     ('Hardware refresh', 'Pure delivers and installs new controllers and shelves on 3-year cadence'),
     ('Purity//FA', 'FlashArray OS; unified block and file with NVMe-native architecture'),
     ('Purity//FB', 'FlashBlade OS; object and file storage with massive parallel throughput'),
     ('AI copilot', 'Pure1 AI feature; recommends workload placement and anomaly remediation'),
     ('TaaS', 'Technology as a Service; hardware ownership stays with Pure throughout subscription'),
     ('ActiveCluster', 'sync stretch replication included; ActiveDR async replication optional'),
     ('SAML SSO', 'Pure1 supports SAML 2.0; identity provider integrates with corporate IdP')])

reg('storage/pure/flasharray',
    'Pure FlashArray', 'FlashArray',
    'all-NVMe block and file array with inline dedup and compression',
    'FC · iSCSI · NVMe-oF · NFS · SMB',
    'FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC',
    'Purity GUI / purefa REST API',
    ['Purity GUI', 'purefa CLI', 'ActiveCluster', 'SafeMode', 'Protection groups'],
    [('Layer', 'Component', 'Notes'),
     ('Controllers', 'Active-active', 'No SPOF'),
     ('Drives', 'DirectFlash', 'NVMe native'),
     ('Volumes', 'Thin provisioned', 'Instant clone'),
     ('ActiveCluster', 'Sync replication', 'Zero RPO'),
     ('SafeMode', 'Immutable snaps', 'Ransomware resist')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('ActiveCluster', 'Stretch cluster', 'Internal RPC', 'Certificate', 'Active-active'),
     ('SafeMode', 'Locked snapshots', 'Internal', 'Pure support', 'Eradicator locked'),
     ('Protection group', 'Snap/replication', 'Internal', 'Admin role', 'Policy-based'),
     ('ActiveDR', 'Async DR', 'Internal RPC', 'Certificate', 'RPO seconds')],
    [('FlashArray', 'Pure all-NVMe block/file array; inline dedup and compression always enabled'),
     ('DirectFlash', 'Pure proprietary NVMe modules; direct flash access without SAS translation'),
     ('ActiveCluster', 'synchronous active-active stretch cluster; hosts see a single namespace'),
     ('ActiveDR', 'asynchronous replication to DR site; recovery point objective in seconds'),
     ('SafeMode', 'admin-locked immutable snapshots; cannot be deleted even by array administrator'),
     ('Protection group', 'set of volumes and hosts sharing a snapshot and replication schedule'),
     ('purefa CLI', 'REST CLI tool for FlashArray; purefa CLI connects via REST API key'),
     ('purearray', 'purectl CLI command: purearray list and purearray show monitoring'),
     ('Volume tag', 'user-defined key-value label on volumes for policy and reporting purposes'),
     ('Host group', 'logical collection of hosts sharing volume access via a host group object'),
     ('Inline dedup', 'content-based deduplication performed inline before data is written to flash'),
     ('Evergreen', 'Pure architecture; controllers upgrade non-disruptively, shelves remain in place')])

reg('storage/pure/flashblade',
    'Pure FlashBlade', 'FlashBlade',
    'massively parallel all-flash NAS and object storage platform',
    'NFS v3/v4.1 · SMB · S3 · Swift · REST API',
    'FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS',
    'Purity//FB GUI / purefb CLI',
    ['Purity//FB', 'File systems', 'Object buckets', 'Replication', 'SafeMode'],
    [('Layer', 'Component', 'Notes'),
     ('Blades', 'NVMe+CPU', 'Parallel I/O'),
     ('File', 'NFS/SMB', 'Scale-out NAS'),
     ('Object', 'S3/Swift', 'Bucket store'),
     ('Replication', 'Async', 'DR/backup'),
     ('SafeMode', 'Locked snaps', 'Ransomware resist')],
    [('Component', 'Purpose', 'Protocol', 'Auth', 'Notes'),
     ('File system', 'NAS namespace', 'NFS/SMB', 'Kerberos/NTLM', 'Up to 4 PiB'),
     ('Object bucket', 'S3 namespace', 'S3/Swift', 'S3 keys/IAM', 'Versioning'),
     ('Replication', 'Async DR', 'Encrypted TCP', 'Certificate', 'File or object'),
     ('SafeMode', 'Locked snapshots', 'Internal', 'Pure support', 'Immutable')],
    [('FlashBlade', 'Pure massively parallel all-flash NAS and object platform; single namespace'),
     ('Blade', 'individual storage module in FlashBlade chassis; NVMe and CPU per blade'),
     ('File system', 'FlashBlade NFS/SMB export namespace; up to 4 PiB per file system'),
     ('Object store', 'S3-compatible bucket store on FlashBlade; versioning and lifecycle rules'),
     ('purefb CLI', 'REST CLI client for FlashBlade: purefb fs list, purefb array show commands'),
     ('Replication', 'async file or object replication between FlashBlade systems for DR'),
     ('SafeMode', 'admin-locked snapshots; protected from deletion even by local array admin'),
     ('S3 multitenancy', 'per-bucket policy and IAM-style access control for object storage'),
     ('NFS Kerberos', 'FlashBlade NFS supports krb5, krb5i, and krb5p security flavours'),
     ('SMB multichannel', 'FlashBlade uses SMB multichannel for improved Windows client performance'),
     ('Inline compression', 'always-on data reduction; typically 2-10x for unstructured data'),
     ('ActiveScale', 'enterprise geo-distribution and erasure coding for large object workloads')])


# ── Page type → diagram content mapping ─────────────────────────────────────

def get_page_type(path):
    dirs = [p for p in path.replace('docs/', '').split('/') if p != 'index.md']
    last = dirs[-1] if dirs else ''
    prev = dirs[-2] if len(dirs) >= 2 else ''
    types_map = {
        'how-it-works': 'how_it_works',
        'integrations': 'integrations',
        'design-standards': 'design_standards',
        'cli-reference': 'cli_reference',
        'health-checks': 'health_checks',
        'procedures': 'procedures',
        'scripts': 'scripts',
        'backup-restore': 'backup_restore',
        'install-upgrade': 'install_upgrade',
        'access-control': 'access_control',
        'authentication': 'authentication',
        'encryption': 'encryption',
        'hardening': 'hardening',
        'common-issues': 'common_issues',
        'diagnostics': 'diagnostics',
        'escalation': 'escalation',
        'operations': 'ops_landing',
        'security': 'sec_landing',
        'troubleshooting': 'ts_landing',
        'known-issues': 'known_issues',
        'ports': 'ports',
    }
    if last in types_map:
        return types_map[last]
    if last == 'architecture':
        return 'arch_landing'
    return 'product_landing'


def build_diagram(path, meta):
    page_type = get_page_type(path)
    name = meta['name']
    abbr = meta['abbr']
    cat = meta['cat']
    protos = meta['protos']
    phys = meta['phys']
    mgmt = meta['mgmt']
    comps5 = meta['comps5']
    arch5 = meta['arch5']
    terms = meta['terms']

    # Per-type title + summary block
    T = {
        'arch_overview':   (f'{name} — Architecture',
            [f'{abbr} architecture: {cat}',
             f'Protocols: {protos}',
             f'Management: {mgmt}; key components: {", ".join(comps5[:3])}',
             'High availability, scalability, and non-disruptive operations by design']),
        'how_it_works':    (f'{name} — How It Works',
            [f'{abbr} operational flow: request → controller → data service → host acknowledgement',
             f'Data path: host I/O → {abbr} controller → storage media → persistent write',
             f'Management: {mgmt} provides unified control for all operational functions',
             'Protection: snapshots, replication, and redundancy ensure data durability']),
        'integrations':    (f'{name} — Integrations',
            [f'{abbr} integrations: VMware vSphere, Kubernetes CSI, backup software, and monitoring',
             f'Protocols: {protos}',
             f'API: {mgmt} REST API enables automation and third-party tool integration',
             'Plug-ins available for vCenter, OpenShift, Splunk, and SIEM platforms']),
        'design_standards':(f'{name} — Architecture Design Standards',
            [f'{abbr} design standards: network isolation, redundancy, sizing, naming conventions',
             'Network: dedicated storage VLAN; jumbo frames for iSCSI; dual-fabric for FC',
             'Redundancy: dual controllers, multipath I/O, and no single points of failure',
             'Monitoring: set capacity and latency alerts; baseline performance after deployment']),
        'cli_reference':   (f'{name} — CLI Reference',
            [f'{abbr} CLI: command-line interface for all management and operational tasks',
             f'Access: SSH or REST client to management IP; authenticate as admin role',
             'Commands: status, list, create, modify, delete, show, and diagnostic operations',
             'Scripting: use REST API or CLI in automation for provisioning and reporting']),
        'health_checks':   (f'{name} — Health Checks',
            [f'{abbr} health checks: routine verification of operational status and performance',
             'Checks include: controller status, drive health, replication lag, and capacity',
             'Frequency: daily quick checks; weekly detailed review; monthly capacity report',
             'Configure threshold-based alerts for proactive incident prevention and awareness']),
        'procedures':      (f'{name} — Operational Procedures',
            [f'{abbr} operational procedures: standard tasks for day-2 administration',
             'Covers: provisioning, expansion, maintenance, DR testing, and decommission',
             'Pre/post checks required for all maintenance activities affecting storage',
             'All procedures require approved change management tickets in production']),
        'scripts':         (f'{name} — Scripts and Automation',
            [f'{abbr} scripts: automation for reporting, health monitoring, and provisioning',
             'REST API available for all operations; PowerShell and Python modules supported',
             'Scripts must run from dedicated service accounts with least-privilege roles',
             'Store credentials in vault; rotate service account passwords on defined schedule']),
        'backup_restore':  (f'{name} — Backup and Restore',
            [f'{abbr} backup: snapshots, replication, and external backup application integration',
             'Snapshot schedule: hourly for 24 h, daily for 7 days, weekly for 4 weeks minimum',
             'Replication: async or sync to DR site for off-site data protection copy',
             'Restore: volume-level or file-level restore from snapshot; test restore quarterly']),
        'install_upgrade': (f'{name} — Install and Upgrade',
            [f'{abbr} installation and upgrade: deployment and version management procedures',
             'Pre-upgrade: back up configuration, check compatibility, review release notes',
             'Upgrade: rolling upgrade preserves service; non-disruptive on dual-controller arrays',
             'Post-upgrade: verify all services running; run health check; notify users']),
        'access_control':  (f'{name} — Access Control',
            [f'{abbr} access control: RBAC roles, least-privilege, and access audit logging',
             'Roles: admin (full), operator (read/modify), read-only (view); map to AD groups',
             'Authentication: local accounts, LDAP/AD integration, and MFA for privileged users',
             'Audit: log all admin actions; review access logs monthly; rotate credentials']),
        'authentication':  (f'{name} — Authentication',
            [f'{abbr} authentication: local accounts, LDAP/AD, RADIUS, and SAML SSO options',
             'MFA: time-based OTP or hardware token required for all privileged admin accounts',
             'Service accounts: dedicated accounts for automation; API tokens/keys preferred',
             'Session: idle timeout enforced; concurrent session limits for admin role accounts']),
        'encryption':      (f'{name} — Encryption',
            [f'{abbr} encryption: data at rest and in transit encryption for all stored data',
             'At rest: AES-256 encryption using controller-managed or external key manager',
             'In transit: TLS 1.2+ for management; protocol encryption for data in flight',
             'Key management: external KMIP-compatible KMS or built-in key lifecycle manager']),
        'hardening':       (f'{name} — Security Hardening',
            [f'{abbr} hardening: disable unused protocols, enforce encryption, restrict access',
             'Network: dedicated storage VLAN; restrict management access to jump hosts only',
             'Auth: disable default accounts; enforce password complexity and rotation policy',
             'Audit: forward syslog to SIEM; alert on privilege escalation and failed logins']),
        'common_issues':   (f'{name} — Common Issues',
            [f'{abbr} common issues: quick-reference for frequently encountered problems',
             'Issues: path failures, connectivity errors, capacity alerts, and auth failures',
             'For each issue: symptoms, root cause, diagnostic steps, and resolution actions',
             'Escalate to vendor support if the issue persists after standard procedures']),
        'diagnostics':     (f'{name} — Diagnostics',
            [f'{abbr} diagnostics: log collection, health checks, and performance analysis',
             'Tools: management CLI, REST API, vendor support bundle, and system event log',
             'Performance: check I/O latency, throughput, queue depth, and cache hit rate',
             'Collect support bundle before contacting vendor support to reduce time-to-resolve']),
        'escalation':      (f'{name} — Escalation',
            [f'{abbr} escalation: severity triage, vendor support contact, and required artifacts',
             'L1: basic checks, restart services; L2: log analysis, config review, vendor SR',
             'Severity: P1 production down → immediate SR + on-call page; P2/P3 business hours',
             'Before escalating: collect support bundle, event timeline, and change history']),
        'ops_landing':     (f'{name} — Operations',
            [f'{abbr} operations: day-2 procedures for administration and maintenance tasks',
             'Covers: provisioning, health checks, upgrades, backup/restore, and scripting',
             'All operations require approved change tickets in production environments',
             'Runbooks available for common tasks; escalation path defined for all incidents']),
        'sec_landing':     (f'{name} — Security',
            [f'{abbr} security: access control, authentication, encryption, and hardening guide',
             'Principle of least privilege applied to all admin roles and service accounts',
             'Encryption at rest and in transit enforced; key rotation on defined schedule',
             'Annual security review and audit; logs forwarded to SIEM for correlation']),
        'ts_landing':      (f'{name} — Troubleshooting',
            [f'{abbr} troubleshooting: structured diagnostic process for common issues',
             'Start with health dashboard, then check recent changes, then review event logs',
             'Collect support bundle before contacting vendor support to accelerate resolution',
             'Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets']),
        'arch_landing':    (f'{name} — Architecture',
            [f'{abbr} architecture overview: {cat}',
             f'Protocols: {protos}',
             f'Key components: {", ".join(comps5[:4])}',
             'Design principles: HA, scalability, non-disruptive operations, and security']),
        'product_landing': (f'{name}',
            [f'{abbr}: {cat}',
             f'Protocols: {protos}',
             f'Management: {mgmt}',
             'Sections: Architecture · Operations · Security · Troubleshooting']),
        'known_issues':   (f'{name} — Known Issues and Error Codes',
            [f'{abbr} known issues: catalog of bugs, error codes, and confirmed workarounds',
             'Each entry includes affected version, root cause, fix, and resolved-in version',
             'Cross-reference vendor KB articles using the KB ID in each table row',
             'Open a vendor SR if no workaround is listed and the issue affects production']),
        'ports':          (f'{name} — Ports and Network Requirements',
            [f'{abbr} network requirements: management, data, and replication port reference',
             'Use this page to build firewall change requests and validate network segmentation',
             f'Protocols: {protos}',
             'Zones: client → management plane → data plane → external services']),
    }

    title, summary4 = T.get(page_type, T['product_landing'])
    # Clamp summary lines to INNER width
    summary4 = [s[:INNER-2] for s in summary4]

    # Flow line per type
    flows = {
        'arch_overview':   f'  Deploy → configure → connect hosts → protect → monitor via {mgmt}',
        'how_it_works':    f'  Host I/O → {abbr} controller → storage media → acknowledge → replicate',
        'integrations':    f'  {abbr} → REST API / plug-ins → VMware / K8s / backup / monitoring',
        'design_standards':f'  Requirements → architecture design → redundancy review → size → deploy',
        'cli_reference':   f'  SSH → authenticate → show status → configure → verify → log output',
        'health_checks':   f'  Check status → review alerts → verify replication → capacity → log',
        'procedures':      f'  Open change → pre-check → execute → verify → post-check → close',
        'scripts':         f'  Script → authenticate REST → execute operation → verify → log result',
        'backup_restore':  f'  Snapshot → replicate to DR → verify → document → test restore',
        'install_upgrade': f'  Plan → backup config → upgrade staging → upgrade production → validate',
        'access_control':  f'  Identify user → assign role → enforce MFA → audit → review quarterly',
        'authentication':  f'  Login → authenticate LDAP/SAML/local → MFA → authorise role → session',
        'encryption':      f'  Enable encryption → configure KMS → verify → audit → rotate keys',
        'hardening':       f'  Baseline config → disable unused → enforce MFA → enable logging → audit',
        'common_issues':   f'  Identify symptom → check logs → diagnose root cause → resolve → verify',
        'diagnostics':     f'  Identify issue → collect logs → run diagnostics → analyse → resolve',
        'escalation':      f'  Detect issue → triage severity → collect artifacts → open SR → update',
        'ops_landing':     f'  Open change → pre-check → execute procedure → verify → close',
        'sec_landing':     f'  Define roles → enforce MFA → enable encryption → harden → audit',
        'ts_landing':      f'  Check health → review changes → examine logs → diagnose → resolve',
        'arch_landing':    f'  Design → deploy → configure → validate → monitor → optimise',
        'product_landing': f'  Architecture → Operations → Security → Troubleshooting → Escalation',
        'known_issues':    f'  Identify error code → match category → apply workaround → verify → open SR if unsolved',
        'ports':           f'  Client zone → management plane → data path → external services / replication',
    }
    flow = flows.get(page_type, flows['product_landing'])

    # 5-col section table per type
    sec_tables = {
        'cli_reference':   ([('Category', 'Command', 'Purpose', 'Output', 'Notes'),
                             ('Status', 'show status', 'Health check', 'State/alerts', 'Daily run'),
                             ('List', 'list all', 'Inventory', 'Name/ID/size', 'Read-only'),
                             ('Create', 'create volume', 'Provision', 'New object', 'Change req'),
                             ('Delete', 'delete resource', 'Decommission', 'Confirmation', 'Irreversible')]),
        'health_checks':   ([('Check area', 'How to verify', 'Pass criteria', 'Frequency', 'Tool'),
                             ('Controllers', 'show status', 'All healthy', 'Daily', 'CLI/GUI'),
                             ('Drives', 'show drives', 'No failed/pred.', 'Daily', 'CLI/GUI'),
                             ('Replication', 'show replication', 'Lag < threshold', 'Daily', 'CLI/GUI'),
                             ('Capacity', 'show capacity', '< 80% used', 'Daily', 'CLI/GUI')]),
        'procedures':      ([('Procedure', 'Pre-check', 'Steps', 'Verify', 'Post-check'),
                             ('Provision', 'Capacity free?', 'Create volume', 'Host access', 'Monitor I/O'),
                             ('Expand', 'Pool space?', 'Grow volume', 'FS resize', 'Verify size'),
                             ('Snapshot', 'Policy set?', 'Take snapshot', 'Snap listed', 'Consistency'),
                             ('Failover', 'Repl. in sync?', 'Break repl.', 'App online', 'Verify RTO')]),
        'backup_restore':  ([('Type', 'Schedule', 'Retention', 'Offsite?', 'Test cycle'),
                             ('Snapshot', 'Hourly/daily', '7/30/90 days', 'No', 'Monthly'),
                             ('Replication', 'Policy-driven', 'Per policy', 'Yes (DR)', 'Quarterly'),
                             ('Backup app', 'Daily full+incr', '90+ days', 'Yes (tape/cloud)', 'Quarterly'),
                             ('Archive', 'Monthly', '7+ years', 'Yes (object)', 'Annual')]),
        'access_control':  ([('Role', 'Permissions', 'Scope', 'Auth', 'Review cycle'),
                             ('Admin', 'Full CRUD', 'Global', 'MFA required', 'Monthly'),
                             ('Operator', 'Read/modify', 'Assigned', 'MFA required', 'Quarterly'),
                             ('Read-only', 'View only', 'Assigned', 'Password', 'Quarterly'),
                             ('Service acct', 'API only', 'Specific API', 'Token/cert', 'Annual')]),
        'authentication':  ([('Method', 'Use case', 'Config location', 'MFA', 'Priority'),
                             ('LDAP/AD', 'Staff accounts', 'Auth settings', 'Required', 'Primary'),
                             ('SAML SSO', 'Federated', 'SSO settings', 'IdP-enforced', 'Preferred'),
                             ('Local', 'Break-glass', 'Local users', 'Required', 'Emergency only'),
                             ('API token', 'Automation', 'Service account', 'N/A (token)', 'Automation')]),
        'encryption':      ([('Layer', 'Standard', 'Key source', 'KMS', 'Notes'),
                             ('At rest', 'AES-256', 'Controller', 'Internal/KMIP', 'Always on'),
                             ('In transit', 'TLS 1.2+', 'PKI cert', 'Internal CA', 'Mgmt + data'),
                             ('Key rotation', 'Annual', 'KMS policy', 'External KMS', 'Automated'),
                             ('Key escrow', 'Required', 'KMS vault', 'External KMS', 'DR access')]),
        'hardening':       ([('Area', 'Control', 'Standard', 'Verify', 'Frequency'),
                             ('Accounts', 'Disable defaults', 'No default creds', 'Login audit', 'Deploy'),
                             ('Protocols', 'Disable unused', 'TLS 1.2+ only', 'Port scan', 'Monthly'),
                             ('MFA', 'Enforce all admin', 'TOTP/hardware', 'Auth logs', 'Continuous'),
                             ('Logging', 'SIEM forwarding', 'All admin events', 'SIEM alerts', 'Daily')]),
        'escalation':      ([('Severity', 'Criteria', 'Response time', 'Owner', 'Vendor SLA'),
                             ('P1', 'Production down', 'Immediate', 'On-call + L2', '1 hr 24x7'),
                             ('P2', 'Major degraded', '1 hour', 'L2 engineer', '4 hr biz hrs'),
                             ('P3', 'Minor degraded', '4 hours', 'L2 engineer', '8 hr biz hrs'),
                             ('P4', 'No impact', 'Next biz day', 'L1 support', '2 biz days')]),
        'known_issues':    ([('Category', 'Typical error', 'First check', 'Common fix', 'Severity'),
                             ('Connectivity', 'Path loss/timeout', 'Network / zoning', 'Reconnect host', 'P2/P3'),
                             ('Auth / access', 'Login failure', 'Account / cert', 'Reset creds', 'P2'),
                             ('Capacity', 'Nearfull / full', 'Usage report', 'Add/free space', 'P1 if full'),
                             ('Firmware/bug', 'Known vendor bug', 'Release notes', 'Apply patch', 'Per SLA')]),
        'ports':           ([('Zone', 'Port/Protocol', 'Source', 'Destination', 'Purpose'),
                             ('Management', '443 TCP', 'Admin hosts', 'Management IP', 'GUI / REST API'),
                             ('Management', '22 TCP', 'Jump hosts', 'Management IP', 'SSH CLI'),
                             ('Data', 'Fabric/iSCSI', 'Hosts', 'Array data ports', 'I/O path'),
                             ('Replication', '443/Fabric', 'Array', 'Remote array', 'Replication')]),
    }

    sec_rows5 = sec_tables.get(page_type, meta.get('sec_rows5', [
        ('Layer', 'Component', 'Function', 'Notes', 'Auth'),
        *[(r[0], r[1], r[2] if len(r) > 2 else '', 'See docs', 'RBAC')
          for r in arch5[1:5]]
    ]))

    # Clamp section table cells to fit
    def clamp5(row5):
        maxw = [17, 16, 16, 15, 15]
        return tuple(str(row5[i])[:maxw[i]] for i in range(5))
    sec_rows5 = [clamp5(r) for r in sec_rows5]

    return make_diagram(title, summary4, flow, arch5, sec_rows5, phys, terms)


def get_product_meta(path):
    rel = path.replace('docs/', '')
    best_key = max((k for k in PRODUCTS if rel.startswith(k)), key=len, default=None)
    if best_key:
        return PRODUCTS[best_key]
    # Generic fallback derived from path parts
    parts = rel.split('/')
    pname = ' '.join(p.replace('-', ' ').title() for p in parts[:3] if p != 'index.md')
    return dict(
        name=pname, abbr=parts[1].replace('-', ' ').title() if len(parts)>1 else pname,
        cat=f'{pname} platform',
        protos='Various protocols',
        phys=f'{pname} infrastructure · management network · monitoring',
        mgmt=f'{pname} management console',
        comps5=[pname, 'Management', 'Monitoring', 'Automation', 'Support'],
        arch5=[('Layer', 'Component', 'Notes'),
               ('Core', 'Primary service', 'Main function'),
               ('Management', 'Control plane', 'Admin access'),
               ('Monitoring', 'Health/perf', 'Alerts/dashboards'),
               ('Security', 'Auth/encrypt', 'Access control'),
               ('Integration', 'APIs/plug-ins', 'Third-party')],
        terms=[
            (parts[1].replace('-',' ').title(), f'{pname} platform overview and core concepts'),
            ('Management', 'management console and command-line interface for administration'),
            ('Monitoring', 'health and performance monitoring dashboards and alerting'),
            ('Automation', 'REST API, scripting, and pipeline integration capabilities'),
            ('Security', 'access control, authentication, and encryption configuration'),
            ('Backup', 'backup and recovery procedures and schedule configuration'),
            ('Upgrade', 'software version upgrades and firmware patching procedures'),
            ('Troubleshooting', 'diagnostic procedures and common issue resolution steps'),
            ('Escalation', 'vendor support escalation path and severity triage process'),
            ('Documentation', 'vendor knowledge base and official product documentation'),
            ('Change management', 'change ticket requirements for production modifications'),
            ('Audit log', 'admin action logging for compliance and security review'),
        ])


def has_diagram(path):
    try:
        c = open(path).read()
        return '┌' in c or '┐' in c
    except:
        return False


def has_summary(path):
    try:
        return 'kb-summary' in open(path).read()
    except:
        return False


def insert_diagram(path, diagram_text):
    with open(path) as f:
        content = f.read()
    div_end = content.find('</div>')
    if div_end == -1:
        return False
    insert_at = div_end + len('</div>')
    after = content[insert_at:]
    if '┌' in after or '┐' in after:
        return False
    fenced = '\n\n```text\n' + diagram_text + '\n```\n'
    new_content = content[:insert_at] + fenced + content[insert_at:]
    with open(path, 'w') as f:
        f.write(new_content)
    return True


def main():
    from diagrams._core import DIAGRAMS
    registered_files = set(info['file'] for info in DIAGRAMS.values())

    SKIP = {'site-map.md', 'site-quality.md', 'usage-metrics.md'}

    missing = []
    for root, dirs, files in os.walk('docs'):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
        for f in sorted(files):
            if f.endswith('.md'):
                path = os.path.join(root, f)
                rel = path.replace('docs/', '')
                if rel in SKIP or rel.startswith('stats/'):
                    continue
                if has_summary(path) and not has_diagram(path) and path not in registered_files:
                    missing.append(path)

    print(f'Processing {len(missing)} pages...')
    written = skipped = errors = 0
    for i, path in enumerate(missing):
        try:
            meta = get_product_meta(path)
            diagram = build_diagram(path, meta)
            if insert_diagram(path, diagram):
                written += 1
            else:
                skipped += 1
        except Exception as e:
            import traceback
            print(f'  ERROR {path}: {e}')
            traceback.print_exc()
            errors += 1
        if (i + 1) % 50 == 0:
            print(f'  {i+1}/{len(missing)} done ({written} written, {errors} errors)')

    print(f'\nDone: {written} written, {skipped} skipped, {errors} errors')


if __name__ == '__main__':
    main()
