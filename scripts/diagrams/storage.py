"""
Storage (Pure, Dell, NetApp) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

@kb_diagram(
    'dell',
    'docs/storage/dell/index.md',
    'Dell Storage Portfolio — PowerMax, PowerStore, Unity, PowerScale, Data Domain, ECS',
)
def dell_storage_portfolio():
    """Dell Storage Portfolio — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    MGMT_L, MGMT_R = 3, 99   # full-width management, inner=95

    # Primary block tier (inner=29)
    PM_L, PM_R =  3, 33   # PowerMax,   MID=18
    PS_L, PS_R = 36, 66   # PowerStore, MID=51
    UT_L, UT_R = 69, 99   # Unity XT,   MID=84

    PM_MID = (PM_L + PM_R) // 2   # 18
    PS_MID = (PS_L + PS_R) // 2   # 51
    UT_MID = (UT_L + UT_R) // 2   # 84

    # Specialty tier (inner=29, same positions)
    SC_L, SC_R =  3, 33   # PowerScale
    DD_L, DD_R = 36, 66   # Data Domain
    EC_L, EC_R = 69, 99   # ECS

    # Protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    lines.append(title_border(W2, 'Dell Storage Portfolio'))
    lines.append(txt_row())

    # ── Management ───────────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Dell Storage Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Unisphere: unified web UI for PowerMax, PowerStore, and Unity management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'CloudIQ: cloud analytics, health scoring, capacity forecasting, and proactive alerts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'InsightIQ: performance analytics and capacity management for PowerScale/OneFS')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmatic management across all Dell storage platforms')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Dell AIOps: AI-driven recommendations and anomaly detection across the portfolio')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Unisphere and CloudIQ manage arrays via REST APIs — on-prem UI or cloud analytics portal'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Primary Block Storage ────────────────────────────────────────────────
    lines.append(R(merge(bTop(PM_L, PM_R), bTop(PS_L, PS_R), bTop(UT_L, UT_R))))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'Dell PowerMax'),
        bMid(PS_L, PS_R, 'Dell PowerStore'),
        bMid(UT_L, UT_R, 'Dell Unity XT'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'Enterprise all-flash block'),
        bMid(PS_L, PS_R, 'Mid-range all-flash unified'),
        bMid(UT_L, UT_R, 'Mid-range unified storage'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'FC · iSCSI · NVMe/FC'),
        bMid(PS_L, PS_R, 'Block + file in one platform'),
        bMid(UT_L, UT_R, 'Block · file · VMware ready'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'SRDF: sync + async repl'),
        bMid(PS_L, PS_R, 'AppsON: containers on-array'),
        bMid(UT_L, UT_R, 'FC · iSCSI · NFS · SMB'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'TimeFinder: local snapshots'),
        bMid(PS_L, PS_R, 'Intelligent automation + ML'),
        bMid(UT_L, UT_R, 'Async replication + snaps'),
    )))
    lines.append(R(merge(
        bMid(PM_L, PM_R, 'NVMe end-to-end, up to 4PB'),
        bMid(PS_L, PS_R, 'NVMe-based storage nodes'),
        bMid(UT_L, UT_R, 'VAAI/VASA VMware support'),
    )))
    lines.append(R(merge(bBot(PM_L, PM_R), bBot(PS_L, PS_R), bBot(UT_L, UT_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Block arrays expose LUNs to hosts via FC, iSCSI, or NVMe; file via NFS and SMB'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Specialty Storage ────────────────────────────────────────────────────
    lines.append(R(merge(bTop(SC_L, SC_R), bTop(DD_L, DD_R), bTop(EC_L, EC_R))))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Dell PowerScale'),
        bMid(DD_L, DD_R, 'Dell Data Domain'),
        bMid(EC_L, EC_R, 'Dell ECS'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Scale-out NAS, OneFS OS'),
        bMid(DD_L, DD_R, 'Purpose-built backup dedup'),
        bMid(EC_L, EC_R, 'Enterprise object storage'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'NFS · SMB · HDFS · S3'),
        bMid(DD_L, DD_R, 'DD Boost: client-side dedup'),
        bMid(EC_L, EC_R, 'S3 · Swift · Atmos APIs'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'SmartQuotas: quota mgmt'),
        bMid(DD_L, DD_R, 'DD Replicator: remote copy'),
        bMid(EC_L, EC_R, 'Geo-distribution + WORM'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'SyncIQ: async replication'),
        bMid(DD_L, DD_R, 'WORM: compliance retention'),
        bMid(EC_L, EC_R, 'Erasure coding for durability'),
    )))
    lines.append(R(merge(
        bMid(SC_L, SC_R, 'Up to 100PB per cluster'),
        bMid(DD_L, DD_R, 'Cloud Tier: long-term archive'),
        bMid(EC_L, EC_R, 'Petabyte-scale capacity'),
    )))
    lines.append(R(merge(bBot(SC_L, SC_R), bBot(DD_L, DD_R), bBot(EC_L, EC_R))))

    lines.append(txt_row())
    lines.append(txt_row('  VPLEX: storage federation and active-active data mobility across arrays and sites'))
    lines.append(txt_row('  PowerPath: host multipathing software; automatic path failover and load balancing'))
    lines.append(txt_row())
    lines.append(R(arrow([PM_MID, PS_MID, UT_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD/NL-SAS drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('PowerMax     = Dell high-end all-flash block array; NVMe end-to-end, up to 4PB usable capacity'))
    lines.append(txt_row('PowerStore   = Dell mid-range unified array; block + file, AppsON containers, intelligent automation'))
    lines.append(txt_row('Unity XT     = Dell mid-range unified array; block, file, and deep VMware integration'))
    lines.append(txt_row('PowerScale   = Dell scale-out NAS running OneFS; supports NFS, SMB, HDFS, S3; scales to 100PB'))
    lines.append(txt_row('Data Domain  = Dell purpose-built backup appliance; DD Boost dedup, replication, cloud tier'))
    lines.append(txt_row('ECS          = Dell Enterprise Content Storage; S3-compatible object with geo-distribution and WORM'))
    lines.append(txt_row('VPLEX        = Dell storage federation; active-active data mobility across arrays and sites'))
    lines.append(txt_row('PowerPath    = Dell host multipathing software; automatic path failover and load balancing'))
    lines.append(txt_row('SRDF         = Symmetrix Remote Data Facility; sync or async replication between PowerMax arrays'))
    lines.append(txt_row('TimeFinder   = Dell local snapshot technology for PowerMax; point-in-time copies of volumes'))
    lines.append(txt_row('DD Boost     = Data Domain client-side dedup library; reduces data sent to the backup target'))
    lines.append(txt_row('OneFS        = PowerScale distributed file system OS; spans all nodes as a single namespace'))
    lines.append(txt_row('SyncIQ       = PowerScale async replication engine; policy-based replication to DR site'))
    lines.append(txt_row('SmartQuotas  = PowerScale quota management; enforces hard/soft limits per directory or user'))
    lines.append(txt_row('AppsON       = PowerStore capability to run VMs and containers directly on the storage array'))
    lines.append(txt_row('CloudIQ      = Dell cloud analytics SaaS; health scoring, capacity forecasting, proactive alerts'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure',
    'docs/storage/pure/index.md',
    'Pure Storage Stack — Pure1, FlashArray, FlashBlade, Evergreen, replication',
)
def pure_storage_stack():
    """Pure Storage Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Management — full width
    MGMT_L, MGMT_R = 3, 99   # inner=95

    # Product tier — three equal boxes (inner=29)
    FA_L, FA_R =  3, 33   # FlashArray, MID=18
    FB_L, FB_R = 36, 66   # FlashBlade, MID=51
    EG_L, EG_R = 69, 99   # Evergreen/One, MID=84

    FA_MID = (FA_L + FA_R) // 2   # 18
    FB_MID = (FB_L + FB_R) // 2   # 51
    EG_MID = (EG_L + EG_R) // 2   # 84

    # Services tier — three equal boxes (inner=29)
    AC_L, AC_R =  3, 33   # ActiveCluster
    AD_L, AD_R = 36, 66   # ActiveDR
    PO_L, PO_R = 69, 99   # Purity OS + SafeMode

    # Protocol layer — full width with 5 sections
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Pure Storage Stack'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Pure1')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'SaaS cloud management portal — no on-prem management appliance required')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Fleet health monitoring · capacity analytics · AI-driven anomaly detection')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Upgrade orchestration: non-disruptive controller and software refreshes')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'Auto-opens support cases; integrates with Pure Technical Services team')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API · Purity CLI · Pure Service Orchestrator (PSO) for Kubernetes')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 manages all arrays via HTTPS — no on-prem management server required'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Product tier ─────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(FA_L, FA_R), bTop(FB_L, FB_R), bTop(EG_L, EG_R))))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'Pure FlashArray'),
        bMid(FB_L, FB_R, 'Pure FlashBlade'),
        bMid(EG_L, EG_R, 'Evergreen / Evergreen//One'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, '//X · //C · //E models'),
        bMid(FB_L, FB_R, '//S: perf · //E: capacity'),
        bMid(EG_L, EG_R, 'Non-disruptive refreshes'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'All-flash block storage'),
        bMid(FB_L, FB_R, 'Scale-out file + object'),
        bMid(EG_L, EG_R, 'Controller swap, no downtime'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'FC · iSCSI · NVMe-oF'),
        bMid(FB_L, FB_R, 'NFS · SMB · S3 · HDFS'),
        bMid(EG_L, EG_R, 'Evergreen//One: STaaS'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'Always-on dedup + compress'),
        bMid(FB_L, FB_R, 'DirectFlash blade modules'),
        bMid(EG_L, EG_R, 'Pure-owned HW on-premises'),
    )))
    lines.append(R(merge(
        bMid(FA_L, FA_R, 'SafeMode: immutable snaps'),
        bMid(FB_L, FB_R, 'Rapid Restore: backup target'),
        bMid(EG_L, EG_R, 'SLA-guaranteed performance'),
    )))
    lines.append(R(merge(bBot(FA_L, FA_R), bBot(FB_L, FB_R), bBot(EG_L, EG_R))))

    lines.append(txt_row())
    lines.append(txt_row('  FlashArray serves block workloads · FlashBlade serves file and object workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Services tier ────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(AC_L, AC_R), bTop(AD_L, AD_R), bTop(PO_L, PO_R))))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'ActiveCluster (Sync)'),
        bMid(AD_L, AD_R, 'ActiveDR (Async)'),
        bMid(PO_L, PO_R, 'Purity OS · SafeMode'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Active-active stretch cluster'),
        bMid(AD_L, AD_R, 'Asynchronous replication'),
        bMid(PO_L, PO_R, 'Purity//FA: FlashArray OS'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Sync replication, RPO=0'),
        bMid(AD_L, AD_R, 'RPO configurable (seconds)'),
        bMid(PO_L, PO_R, 'Purity//FB: FlashBlade OS'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Mediator: tie-breaker node'),
        bMid(AD_L, AD_R, 'Cross-array and cross-site DR'),
        bMid(PO_L, PO_R, 'SafeMode: retention-locked'),
    )))
    lines.append(R(merge(
        bMid(AC_L, AC_R, 'Transparent host failover'),
        bMid(AD_L, AD_R, 'Non-disruptive failover test'),
        bMid(PO_L, PO_R, 'Policy-based snap scheduling'),
    )))
    lines.append(R(merge(bBot(AC_L, AC_R), bBot(AD_L, AD_R), bBot(PO_L, PO_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Replication and data services protect workloads across sites and against ransomware'))
    lines.append(txt_row())
    lines.append(R(arrow([FA_MID, FB_MID, EG_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NVMe-oF', 'NFS / SMB', 'S3 / HDFS'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'NVMe over Fabrics', 'File protocols', 'Object / analytics'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP network', 'Ethernet / RoCE', 'NFS v3/v4.1 · SMB', 'REST · SDK · POSIX'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'NVMe host adapter', 'Exports + shares', 'Buckets + keys'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'RDMA low latency', 'Perms + quotas', 'IAM + policies'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('DirectFlash NVMe modules · Dual controllers · 10/25/100 GbE · FC 16G/32G · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('FlashArray    = Pure all-flash block array; //X (performance), //C (capacity), //E (entry)'))
    lines.append(txt_row('FlashBlade    = Pure scale-out file + object platform built on DirectFlash blade modules'))
    lines.append(txt_row('Pure1         = Pure SaaS cloud management; health, analytics, and upgrade orchestration'))
    lines.append(txt_row('Purity//FA    = FlashArray operating system; manages volumes, snapshots, and replication'))
    lines.append(txt_row('Purity//FB    = FlashBlade operating system; manages NFS, SMB, S3 buckets, and expansion'))
    lines.append(txt_row('ActiveCluster = Sync active-active stretch cluster; RPO=0, transparent host failover'))
    lines.append(txt_row('ActiveDR      = Async replication with configurable RPO (seconds); used for cross-site DR'))
    lines.append(txt_row('SafeMode      = Immutable retention-locked snapshots; immune to admin or ransomware deletion'))
    lines.append(txt_row('Evergreen     = Pure upgrade programme; controller refresh without downtime or data migration'))
    lines.append(txt_row('Evergreen//One= STaaS model; Pure owns and maintains hardware on-premises, billed by use'))
    lines.append(txt_row('DirectFlash   = Pure proprietary NVMe modules; bypasses SSD firmware for lower latency'))
    lines.append(txt_row('PSO           = Pure Service Orchestrator; Kubernetes operator for dynamic volume provisioning'))
    lines.append(txt_row('Mediator      = Lightweight VM that arbitrates ActiveCluster split-brain scenarios'))
    lines.append(txt_row('RPO           = Recovery Point Objective; max acceptable data loss (ActiveCluster=0, ActiveDR=secs)'))
    lines.append(txt_row('STaaS         = Storage-as-a-Service; hardware owned by Pure, customer pays by consumption'))
    lines.append(txt_row('NVMe-oF       = NVMe over Fabrics; extends NVMe protocol across Ethernet (RoCE) or FC'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'storage',
    'docs/storage/index.md',
    'Enterprise Storage Landscape — Pure, Dell, NetApp arrays + protocol layer',
)
def enterprise_storage_landscape():
    """Enterprise Storage Landscape — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Three equal-width boxes (inner=29, margin=3, gap=2)
    PURE_L, PURE_R =  3, 33   # inner=29, MID=18
    DELL_L, DELL_R = 36, 66   # inner=29, MID=51
    NTAP_L, NTAP_R = 69, 99   # inner=29, MID=84

    PURE_MID = (PURE_L + PURE_R) // 2   # 18
    DELL_MID = (DELL_L + DELL_R) // 2   # 51
    NTAP_MID = (NTAP_L + NTAP_R) // 2   # 84

    # Full-width protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'Enterprise Storage Landscape'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure1'),
        bMid(DELL_L, DELL_R, 'Unisphere / CloudIQ'),
        bMid(NTAP_L, NTAP_R, 'ONTAP System Manager'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Cloud mgmt portal'),
        bMid(DELL_L, DELL_R, 'Unisphere: array admin UI'),
        bMid(NTAP_L, NTAP_R, 'Browser-based admin UI'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'FlashArray & FlashBlade'),
        bMid(DELL_L, DELL_R, 'CloudIQ: cloud analytics'),
        bMid(NTAP_L, NTAP_R, 'Volume, LUN & quota mgmt'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Capacity & performance'),
        bMid(DELL_L, DELL_R, 'Health scoring & forecast'),
        bMid(NTAP_L, NTAP_R, 'ActiveIQ: cloud analytics'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Proactive support alerts'),
        bMid(DELL_L, DELL_R, 'REST API & automation'),
        bMid(NTAP_L, NTAP_R, 'Proactive health alerting'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Management planes connect to arrays via HTTPS / REST APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Primary Storage Arrays ───────────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure FlashArray'),
        bMid(DELL_L, DELL_R, 'Dell PowerMax / VMAX'),
        bMid(NTAP_L, NTAP_R, 'NetApp ONTAP'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'All-flash block storage'),
        bMid(DELL_L, DELL_R, 'Mission-critical block'),
        bMid(NTAP_L, NTAP_R, 'Unified block + file'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'FC · iSCSI · NVMe-oF'),
        bMid(DELL_L, DELL_R, 'FC · iSCSI · NVMe/FC'),
        bMid(NTAP_L, NTAP_R, 'FC · iSCSI · NFS · SMB'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Always-on dedup + comp'),
        bMid(DELL_L, DELL_R, 'SRDF: sync replication'),
        bMid(NTAP_L, NTAP_R, 'SnapMirror: replication'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'ActiveCluster: active-active'),
        bMid(DELL_L, DELL_R, 'Dynamic tiering + cache'),
        bMid(NTAP_L, NTAP_R, 'SnapCenter: backup mgmt'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'SafeMode: immutable snaps'),
        bMid(DELL_L, DELL_R, 'PowerPath: multipathing'),
        bMid(NTAP_L, NTAP_R, 'FabricPool: cloud tiering'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Arrays expose LUNs (block) or volumes (file) to hosts and VMs via storage protocols'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Specialty / Extended Storage ─────────────────────────────────────────
    lines.append(R(merge(bTop(PURE_L, PURE_R), bTop(DELL_L, DELL_R), bTop(NTAP_L, NTAP_R))))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Pure FlashBlade'),
        bMid(DELL_L, DELL_R, 'PowerScale / Data Domain'),
        bMid(NTAP_L, NTAP_R, 'Keystone / StorageGRID'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Scale-out file + object'),
        bMid(DELL_L, DELL_R, 'PowerScale: scale-out NAS'),
        bMid(NTAP_L, NTAP_R, 'Keystone: STaaS model'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'NFS · SMB · S3 protocols'),
        bMid(DELL_L, DELL_R, 'Data Domain: dedup backup'),
        bMid(NTAP_L, NTAP_R, 'StorageGRID: object store'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Unstructured data at scale'),
        bMid(DELL_L, DELL_R, 'NFS · SMB · DD Boost'),
        bMid(NTAP_L, NTAP_R, 'Cloud Volumes ONTAP'),
    )))
    lines.append(R(merge(
        bMid(PURE_L, PURE_R, 'Rapid Restore: backup'),
        bMid(DELL_L, DELL_R, 'Multi-PB capacity scaling'),
        bMid(NTAP_L, NTAP_R, 'Snap replication + backup'),
    )))
    lines.append(R(merge(bBot(PURE_L, PURE_R), bBot(DELL_L, DELL_R), bBot(NTAP_L, NTAP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Specialty platforms handle unstructured data, backup, and cloud-connected workloads'))
    lines.append(txt_row())
    lines.append(R(arrow([PURE_MID, DELL_MID, NTAP_MID])))
    lines.append(txt_row())

    # ── Protocol Layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth + iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD drives · FC HBAs (16G/32G) · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('LUN          = Logical Unit Number; a block device exposed by a storage array via FC or iSCSI'))
    lines.append(txt_row('SAN          = Storage Area Network; dedicated high-speed network carrying block storage traffic'))
    lines.append(txt_row('NAS          = Network Attached Storage; file-level storage served over IP via NFS or SMB'))
    lines.append(txt_row('FC           = Fibre Channel; high-speed block protocol using HBAs, SAN switches, and WWPN zoning'))
    lines.append(txt_row('iSCSI        = Internet SCSI; block storage over standard TCP/IP — no specialised hardware required'))
    lines.append(txt_row('NFS          = Network File System; Unix/Linux file protocol; mounts remote directories over IP'))
    lines.append(txt_row('SMB          = Server Message Block; Windows file-sharing protocol, also known as CIFS'))
    lines.append(txt_row('SRDF         = Symmetrix Remote Data Facility; Dell EMC sync replication between PowerMax arrays'))
    lines.append(txt_row('SnapMirror   = NetApp replication engine; copies volumes between ONTAP systems or to cloud'))
    lines.append(txt_row('SafeMode     = Pure Storage immutable snapshot feature; protects data against ransomware deletion'))
    lines.append(txt_row('ActiveCluster= Pure active-active stretch cluster; I/O served from both sites simultaneously'))
    lines.append(txt_row('Dedup        = Deduplication; eliminates duplicate data blocks to reduce raw capacity consumption'))
    lines.append(txt_row('FabricPool   = NetApp tiering; auto-moves cold blocks to S3-compatible object storage'))
    lines.append(txt_row('ONTAP        = NetApp unified storage OS running on FAS, AFF, Cloud Volumes, and StorageGRID'))
    lines.append(txt_row('DD Boost     = Data Domain client-side dedup; reduces backup data transferred over the network'))
    lines.append(txt_row('Keystone     = NetApp STaaS subscription; on-prem arrays billed like cloud consumption'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'netapp',
    'docs/storage/netapp/index.md',
    'NetApp Storage Stack — ONTAP, StorageGRID, Keystone, SnapMirror, SnapCenter, FabricPool',
)
def netapp_storage_stack():
    """NetApp Storage Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    # Management — full width
    MGMT_L, MGMT_R = 3, 99   # inner=95

    # Product tier — three equal boxes (inner=29)
    OT_L, OT_R =  3, 33   # ONTAP (AFF/FAS), MID=18
    SG_L, SG_R = 36, 66   # StorageGRID, MID=51
    KS_L, KS_R = 69, 99   # Keystone, MID=84

    OT_MID = (OT_L + OT_R) // 2   # 18
    SG_MID = (SG_L + SG_R) // 2   # 51
    KS_MID = (KS_L + KS_R) // 2   # 84

    # Data services tier (inner=29, same positions)
    SM_L, SM_R =  3, 33   # SnapMirror
    SC_L, SC_R = 36, 66   # SnapCenter
    FP_L, FP_R = 69, 99   # FabricPool

    # Protocol layer
    PROT_L, PROT_R = 3, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []

    # ── Title ────────────────────────────────────────────────────────────────
    lines.append(title_border(W2, 'NetApp Storage Stack'))
    lines.append(txt_row())

    # ── Management tier ──────────────────────────────────────────────────────
    lines.append(R(bTop(MGMT_L, MGMT_R)))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'NetApp Management')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ONTAP System Manager: browser-based admin UI for volumes, LUNs, and quotas')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ActiveIQ: cloud analytics — health scoring, capacity forecasting, proactive alerts')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'REST API: programmatic management across AFF, FAS, Cloud Volumes, StorageGRID')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'ONTAP CLI: SSH-based command-line management for volumes, aggregates, and SVMs')))
    lines.append(R(bMid(MGMT_L, MGMT_R, 'BlueXP: unified multi-cloud management — on-prem and cloud ONTAP from one console')))
    lines.append(R(bBot(MGMT_L, MGMT_R)))

    lines.append(txt_row())
    lines.append(txt_row('  ONTAP System Manager and BlueXP manage arrays via REST APIs'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Product tier ─────────────────────────────────────────────────────────
    lines.append(R(merge(bTop(OT_L, OT_R), bTop(SG_L, SG_R), bTop(KS_L, KS_R))))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'NetApp ONTAP'),
        bMid(SG_L, SG_R, 'NetApp StorageGRID'),
        bMid(KS_L, KS_R, 'NetApp Keystone'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'AFF · FAS · ONTAP Select'),
        bMid(SG_L, SG_R, 'Enterprise object storage'),
        bMid(KS_L, KS_R, 'Storage-as-a-service'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'Unified block + file + S3'),
        bMid(SG_L, SG_R, 'S3 · Swift · NFS · HDFS'),
        bMid(KS_L, KS_R, 'NetApp-owned HW on-premises'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'FC · iSCSI · NFS · SMB'),
        bMid(SG_L, SG_R, 'WORM: compliance retention'),
        bMid(KS_L, KS_R, 'Billed by consumption (TiB)'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'MetroCluster: sync stretch'),
        bMid(SG_L, SG_R, 'Erasure coding for durability'),
        bMid(KS_L, KS_R, 'SLA-guaranteed performance'),
    )))
    lines.append(R(merge(
        bMid(OT_L, OT_R, 'Cloud Volumes ONTAP: AWS/GCP'),
        bMid(SG_L, SG_R, 'Petabyte-scale capacity'),
        bMid(KS_L, KS_R, 'Flex burst above committed'),
    )))
    lines.append(R(merge(bBot(OT_L, OT_R), bBot(SG_L, SG_R), bBot(KS_L, KS_R))))

    lines.append(txt_row())
    lines.append(txt_row('  ONTAP serves block and file workloads · StorageGRID serves object workloads at scale'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Data services tier ───────────────────────────────────────────────────
    lines.append(R(merge(bTop(SM_L, SM_R), bTop(SC_L, SC_R), bTop(FP_L, FP_R))))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'SnapMirror'),
        bMid(SC_L, SC_R, 'SnapCenter'),
        bMid(FP_L, FP_R, 'FabricPool'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'Async + sync replication'),
        bMid(SC_L, SC_R, 'Application-aware backup'),
        bMid(FP_L, FP_R, 'Auto cold-data tiering'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'DR + data distribution'),
        bMid(SC_L, SC_R, 'SQL · Oracle · SAP · VMware'),
        bMid(FP_L, FP_R, 'Tier to S3 or cloud object'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'ONTAP to ONTAP or cloud'),
        bMid(SC_L, SC_R, 'Consistent snapshot + clone'),
        bMid(FP_L, FP_R, 'Reduce on-prem footprint'),
    )))
    lines.append(R(merge(
        bMid(SM_L, SM_R, 'Active Sync: RPO=0'),
        bMid(SC_L, SC_R, 'Restore to alt. location'),
        bMid(FP_L, FP_R, 'Policy-based temp scan'),
    )))
    lines.append(R(merge(bBot(SM_L, SM_R), bBot(SC_L, SC_R), bBot(FP_L, FP_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Data services protect, replicate, and optimise capacity across all ONTAP platforms'))
    lines.append(txt_row())
    lines.append(R(arrow([OT_MID, SG_MID, KS_MID])))
    lines.append(txt_row())

    # ── Protocol layer ───────────────────────────────────────────────────────
    lines.append(R(bTop(PROT_L, PROT_R)))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Fibre Channel', 'iSCSI', 'NFS', 'SMB / CIFS', 'S3 / Object'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['SAN block access', 'IP block access', 'Unix file mounts', 'Windows shares', 'REST object store'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['16G · 32G · 64G', 'TCP/IP · iSNS', 'NFS v3 · v4.1', 'CIFS · DFS-N', 'HTTP · REST · SDK'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['HBA → SAN switch', 'iSCSI initiator', 'Mount via IP', 'SMB sessions', 'Buckets + prefixes'])))
    lines.append(R(sections(PROT_L, PROT_R, [PD1, PD2, PD3, PD4],
        ['Zoning + masking', 'CHAP auth · iSNS', 'Export policies', 'Share perms+ACL', 'Policies + IAM'])))
    lines.append(R(bBot(PROT_L, PROT_R)))

    # ── Physical Infrastructure ──────────────────────────────────────────────
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('NVMe/SSD/HDD drives · FC HBAs · 10/25/100 GbE NICs · SAN switches · Power & Cooling'))
    lines.append(txt_row())

    # ── Glossary ─────────────────────────────────────────────────────────────
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('ONTAP        = NetApp unified storage OS; runs on AFF, FAS, Cloud Volumes, and ONTAP Select'))
    lines.append(txt_row('AFF          = All-Flash FAS; NetApp all-NVMe/SSD arrays optimised for performance workloads'))
    lines.append(txt_row('FAS          = Fabric-Attached Storage; NetApp hybrid arrays with HDD and SSD capacity tiers'))
    lines.append(txt_row('SVM          = Storage Virtual Machine; logical ONTAP partition with its own namespace and protocols'))
    lines.append(txt_row('SnapMirror   = NetApp replication engine; async or sync volume copies between ONTAP systems'))
    lines.append(txt_row('SnapCenter   = Application-consistent backup tool; integrates with SQL, Oracle, SAP, and VMware'))
    lines.append(txt_row('FabricPool   = ONTAP auto-tiering; moves cold data blocks to S3-compatible object storage'))
    lines.append(txt_row('StorageGRID  = NetApp object store; S3/Swift APIs, WORM compliance, petabyte geo-distribution'))
    lines.append(txt_row('Keystone     = NetApp STaaS; NetApp-owned hardware on-prem, billed by consumption per TiB'))
    lines.append(txt_row('ActiveIQ     = NetApp SaaS analytics; predictive health, capacity forecasting, proactive support'))
    lines.append(txt_row('MetroCluster = ONTAP sync stretch cluster; RPO=0 across two sites with transparent failover'))
    lines.append(txt_row('Active Sync  = SnapMirror Active Sync; granular sync replication for persistent LUN access'))
    lines.append(txt_row('FlexVol      = ONTAP flexible volume; dynamically grows or shrinks within a storage aggregate'))
    lines.append(txt_row('FlexGroup    = ONTAP distributed volume; scales to petabytes across multiple cluster nodes'))
    lines.append(txt_row('BlueXP       = NetApp unified console; manages on-prem and cloud ONTAP from one SaaS portal'))
    lines.append(txt_row('SnapVault    = Policy-based snapshot replication to a secondary system for backup retention'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure-flasharray',
    'docs/storage/pure/flasharray/index.md',
    'Pure FlashArray Stack — CT0/CT1 HA, Purity//FA, NVMe/FC, ActiveDR, ActiveCluster, SafeMode',
)
def pure_flasharray_stack():
    """Pure FlashArray Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure FlashArray — All-Flash Block Storage (Purity//FA)')))
    lines.append(R(bMid(IV_L, IV_R, 'Dual-controller HA pair: CT0 + CT1 active/active with NVRAM mirroring for < 1 ms write ACK')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: Fibre Channel (16/32G) · iSCSI (10/25 GbE) · NVMe/FC · NVMe/RoCE · NVMe/TCP')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure1: cloud management portal — telemetry, AI support alerts, capacity forecasting, proactive')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: ActiveDR (async, RPO minutes) · ActiveCluster (sync, zero RPO, stretch cluster)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  FlashArray management layer feeds architecture, operations, security, and troubleshooting'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CT0/CT1 HA pair design'),
        bMid(B2_L, B2_R, 'purearray CLI + REST API'),
        bMid(B3_L, B3_R, 'SafeMode: immutable snaps'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NVRAM: write buffer+mirror'),
        bMid(B2_L, B2_R, 'Volume: create, expand, map'),
        bMid(B3_L, B3_R, 'RBAC: roles + API tokens'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flash shelves: NVMe SSD'),
        bMid(B2_L, B2_R, 'Snapshots + clones + PGs'),
        bMid(B3_L, B3_R, 'Data-at-rest: AES-256'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inline dedup+compression'),
        bMid(B2_L, B2_R, 'Health: drives, ports, cache'),
        bMid(B3_L, B3_R, 'Audit log + syslog export'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ActiveCluster: stretch vols'),
        bMid(B2_L, B2_R, 'ActiveDR: async replication'),
        bMid(B3_L, B3_R, 'Directory services: AD/LDAP'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines HA and data path · Operations manage volumes'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Volume offline', 'purearray list', 'Drive health OK', 'Case: array ID', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag/BW check', 'purelog download', 'Port: link state', 'Log bundle req', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['HA failover path', 'puresupport bundle', 'Capacity: >80%?', 'Remote assist', 'purehgroup list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Snap space growth', 'netconfig verify', 'Repl state: Active', 'P1/P2 severity', 'pureport list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Dual controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power & Cooling'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Purity//FA    = FlashArray operating system; manages data services, dedup, compression, and protocols'))
    lines.append(txt_row('NVRAM         = Non-volatile RAM; write buffer mirrored CT0↔CT1 before ACK — guarantees < 1 ms writes'))
    lines.append(txt_row('ActiveCluster = Synchronous stretch cluster; zero RPO across two sites or arrays on same fabric'))
    lines.append(txt_row('ActiveDR      = Asynchronous replication; RPO in minutes; automated failover and failback workflow'))
    lines.append(txt_row('SafeMode      = Pure immutable snapshot protection; delete requires PIN from Pure Storage support'))
    lines.append(txt_row('Protection Group= PG; set of volumes replicated together on a schedule to a target array or cloud'))
    lines.append(txt_row('Inline dedup  = Deduplication applied before data hits flash; no post-process latency penalty'))
    lines.append(txt_row('CT0 / CT1     = Controller 0 and Controller 1; both actively serve I/O simultaneously'))
    lines.append(txt_row('NVMe/RoCE     = NVMe over RDMA over Converged Ethernet; ultra-low latency block access over IP fabric'))
    lines.append(txt_row('NVMe/FC       = NVMe over Fibre Channel; block protocol for NVMe SSDs transported over FC fabric'))
    lines.append(txt_row('Pure1         = Cloud management portal; remote telemetry, AI-driven alerts, capacity forecasting'))
    lines.append(txt_row('RBAC          = Role-Based Access Control; Storage Admin, Array Admin, Read-Only built-in roles'))
    lines.append(txt_row('purearray     = CLI entry point on FlashArray; purearray get/list/set for array-level config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure-flashblade',
    'docs/storage/pure/flashblade/index.md',
    'Pure FlashBlade Stack — scale-out blades, NFS/SMB/S3/HDFS, Purity//FB, replication',
)
def pure_flashblade_stack():
    """Pure FlashBlade Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashBlade Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure FlashBlade — Unified Fast File and Object Storage (Purity//FB)')))
    lines.append(R(bMid(IV_L, IV_R, 'Scale-out blade architecture: blade modules add capacity + performance; no hot spots')))
    lines.append(R(bMid(IV_L, IV_R, 'Protocols: NFS v3/v4.1 · SMB 2/3 · S3 API · HDFS — unified from single platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Use cases: AI/ML training data, analytics, backup targets, unstructured data at scale')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: asynchronous object and file replication to another FlashBlade or cloud')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  FlashBlade management spans blade hardware, protocol services, operations, and security'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blade modules: F-series'),
        bMid(B2_L, B2_R, 'purefb CLI + REST API'),
        bMid(B3_L, B3_R, 'RBAC: roles + tokens'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Chassis: 4–15 blades'),
        bMid(B2_L, B2_R, 'File system + bucket ops'),
        bMid(B3_L, B3_R, 'Data-at-rest: AES-256'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NFS exports + SMB shares'),
        bMid(B2_L, B2_R, 'Snapshots: dir + object'),
        bMid(B3_L, B3_R, 'Network: subnet policies'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'S3 buckets + IAM policies'),
        bMid(B2_L, B2_R, 'Capacity: blades + forecast'),
        bMid(B3_L, B3_R, 'Audit log + syslog'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication: async FB→FB'),
        bMid(B2_L, B2_R, 'Health: blade, network'),
        bMid(B3_L, B3_R, 'Directory services: AD/LDAP'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines scale-out layout · Operations manage shares and buckets'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NFS mount fail', 'purefb list', 'Blade health OK', 'Case: array SN', 'purefb get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['S3 auth failure', 'purelog download', 'Network: ports', 'Log bundle req', 'purefb fs list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag: BW', 'purebuddy check', 'Capacity: >80%?', 'Remote assist', 'purefb bucket ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SMB slow writes', 'netconfig verify', 'Repl state: OK', 'P1/P2 severity', 'purefb snap list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashBlade chassis · F-series blade modules · 10/25/100 GbE NICs · Ethernet switches'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Purity//FB   = FlashBlade operating system; manages file, object, and HDFS data services'))
    lines.append(txt_row('F-series     = FlashBlade blade module type; NVMe-based, each adds capacity and throughput'))
    lines.append(txt_row('NFS          = Network File System; file protocol used by Linux/Unix clients; v3 and v4.1 supported'))
    lines.append(txt_row('SMB          = Server Message Block; Windows file sharing protocol; SMB 2.0 and 3.0 on FlashBlade'))
    lines.append(txt_row('S3           = AWS-compatible object storage API; FlashBlade implements S3 bucket/object model'))
    lines.append(txt_row('HDFS         = Hadoop Distributed File System API; FlashBlade serves as HDFS-compatible target'))
    lines.append(txt_row('purefb       = FlashBlade CLI entry point; purefb fs/bucket/snap/hw commands for management'))
    lines.append(txt_row('Scale-out    = Adding blades increases both capacity and performance simultaneously (no hot spots)'))
    lines.append(txt_row('Replication  = Async file/object replication to another FlashBlade or object store; RPO-based'))
    lines.append(txt_row('Subnet policy= Network access rules bound to FlashBlade interfaces for NFS, SMB, S3, replication'))
    lines.append(txt_row('RBAC         = Role-Based Access Control; Array Admin, Storage Admin, Read-Only roles on FlashBlade'))
    lines.append(txt_row('Pure1        = Cloud management portal; monitors all FlashBlade arrays; capacity and health analytics'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure-evergreen',
    'docs/storage/pure/evergreen/index.md',
    'Pure Evergreen Program — NDU controller refresh, Purity upgrades, Ever Modern lifecycle',
)
def pure_evergreen_program():
    """Pure Evergreen Program — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Evergreen Program'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure Evergreen — Hardware Subscription + Non-Disruptive Lifecycle')))
    lines.append(R(bMid(IV_L, IV_R, 'Ever Modern: periodic controller refresh with zero downtime — no forklift upgrades, ever')))
    lines.append(R(bMid(IV_L, IV_R, 'Purity upgrades: OS updates delivered non-disruptively on same hardware via Pure1 scheduling')))
    lines.append(R(bMid(IV_L, IV_R, 'Subscription tiers: Evergreen//Forever (purchased) · Evergreen//One (STaaS) · Evergreen//Flex')))
    lines.append(R(bMid(IV_L, IV_R, 'Controller refresh: new CT shipped, slide-in swap; no data migration, no reformat required')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Evergreen covers the full lifecycle: architecture, operations, refresh, security, and'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Subscription model: NDU'),
        bMid(B2_L, B2_R, 'Purity upgrade: schedule'),
        bMid(B3_L, B3_R, 'Version matrix: FA/FB'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Controller: slide-in swap'),
        bMid(B2_L, B2_R, 'Controller refresh prep'),
        bMid(B3_L, B3_R, 'EOL tracking: model dates'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Flash: add shelf/blade NDU'),
        bMid(B2_L, B2_R, 'Pre-check: health + alerts'),
        bMid(B3_L, B3_R, 'Refresh planning: timeline'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Evergreen//Forever model'),
        bMid(B2_L, B2_R, 'Post-val: array + hosts'),
        bMid(B3_L, B3_R, 'Upgrade path: hop rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure1: lifecycle visibility'),
        bMid(B2_L, B2_R, 'Security: baseline check'),
        bMid(B3_L, B3_R, 'Compatibility matrix check'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the subscription model · Operations execute upgrades'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade fails', 'purearray get', 'SW version OK?', 'Case: upgrade', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CT swap issues', 'purelog download', 'Drive health OK', 'TAM escalation', 'purearray list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Host I/O during ND', 'puresupport bundle', 'Pre-check: pass?', 'Remote assist', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl: pause+resume', 'netconfig verify', 'Post-val: vols', 'P1/P2 severity', 'pureport list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen      = Pure hardware + software subscription model; replaces forklift upgrade cycle'))
    lines.append(txt_row('NDU            = Non-Disruptive Upgrade; Purity OS updates applied with zero downtime to hosts'))
    lines.append(txt_row('Ever Modern    = Controller refresh entitlement; new CT0/CT1 shipped and swapped non-disruptively'))
    lines.append(txt_row('Purity upgrade = Operating system upgrade applied to FlashArray or FlashBlade via Pure1 schedule'))
    lines.append(txt_row('Evergreen//Forever = Purchased subscription; hardware refresh rights included; perpetual entitlement'))
    lines.append(txt_row('Evergreen//One = STaaS tier; Pure-owned hardware, consumption billing, 99.9999% SLA guaranteed'))
    lines.append(txt_row('Evergreen//Flex= Flex subscription; capacity can scale up or down; usage-based billing model'))
    lines.append(txt_row('Controller swap= Physical CT replacement; slides in while array stays online serving I/O'))
    lines.append(txt_row('EOL            = End of Life; model or Purity version reaching end of support/maintenance'))
    lines.append(txt_row('Hop limit      = Maximum Purity version jump in one upgrade step; check compatibility matrix'))
    lines.append(txt_row('Pre-check      = Automated or manual health validation before starting controller or Purity upgrade'))
    lines.append(txt_row('Pure1          = Cloud portal that schedules and monitors Evergreen upgrades and refresh events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure-evergreen-one',
    'docs/storage/pure/evergreen-one/index.md',
    'Pure Evergreen//One — STaaS, Pure-owned hardware, 99.9999% SLA, consumption billing',
)
def pure_evergreen_one():
    """Pure Evergreen//One STaaS — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Evergreen//One'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Evergreen//One — Storage-as-a-Service (Pure-Owned, Customer-Operated)')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure-owned and managed hardware installed on-premises or in colocation — customer pays per TiB')))
    lines.append(R(bMid(IV_L, IV_R, 'SLA: 99.9999% availability · performance guarantees · consumption-based billing per TiB used')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure manages: hardware refresh, Purity upgrades, capacity additions — all non-disruptive')))
    lines.append(R(bMid(IV_L, IV_R, 'Customer operates: volume provisioning, host zoning, snapshots, replication policies')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Evergreen//One combines STaaS economics with on-premises control and guaranteed SLAs'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Architecture'),
        bMid(B2_L, B2_R, 'Operations'),
        bMid(B3_L, B3_R, 'Vendor Support'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure-owned hardware on-prem'),
        bMid(B2_L, B2_R, 'Pure1: health + telemetry'),
        bMid(B3_L, B3_R, 'Vendor: hw refresh + Purity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Consumption billing: TiB'),
        bMid(B2_L, B2_R, 'Volume + host mapping ops'),
        bMid(B3_L, B3_R, 'SLA: 99.9999% + perf SLO'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '99.9999% availability SLA'),
        bMid(B2_L, B2_R, 'Snapshots + replication'),
        bMid(B3_L, B3_R, 'Support portal: case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Min committed capacity'),
        bMid(B2_L, B2_R, 'Capacity: usage reporting'),
        bMid(B3_L, B3_R, 'On-site engineer if needed'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Integration: colo/on-prem'),
        bMid(B2_L, B2_R, 'Alerts: Pure1 proactive'),
        bMid(B3_L, B3_R, 'Data to collect: log bundle'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines STaaS model · Operations run daily tasks · Vendor Support covers incidents'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Volume offline', 'purearray list', 'SLA: green OK?', 'Case: SLA breach', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Billing dispute', 'Pure1 telemetry', 'Capacity headroom', 'TAM escalation', 'purevolume list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Perf below SLO', 'purelog download', 'Perf SLO: met?', 'Remote assist', 'pureport list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Connectivity loss', 'netconfig verify', 'Repl state: OK', 'P1/P2 severity', 'purehgroup list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Pure-owned FlashArray/FlashBlade · customer data centre or colo rack · Power, Cooling, and Network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Evergreen//One  = Pure Storage-as-a-Service; Pure owns hardware, customer gets consumption pricing'))
    lines.append(txt_row('STaaS           = Storage as a Service; pay-per-TiB model with no CapEx hardware purchase'))
    lines.append(txt_row('99.9999% SLA    = Six nines availability guarantee; ~31 seconds downtime per year maximum'))
    lines.append(txt_row('Perf SLO        = Performance Service Level Objective; latency and IOPS thresholds guaranteed'))
    lines.append(txt_row('Consumption billing = Billed on actual TiB consumed above committed base; metered monthly'))
    lines.append(txt_row('Committed capacity= Minimum TiB reserved in contract; pay for this floor regardless of actual use'))
    lines.append(txt_row('Pure1           = Cloud portal; Pure team monitors SLA health and proactively resolves issues'))
    lines.append(txt_row('Vendor refresh  = Pure ships replacement controllers or blades when hardware reaches EOL'))
    lines.append(txt_row('Colo deployment = Pure-owned array installed in a customer-selected colocation facility'))
    lines.append(txt_row('Log bundle      = Diagnostic data package pulled from array for Pure support case analysis'))
    lines.append(txt_row('TAM             = Technical Account Manager; Pure escalation point for strategic and critical issues'))
    lines.append(txt_row('Remote assist   = Pure engineer connects via secure tunnel for live troubleshooting on the array'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'pure-operations',
    'docs/storage/pure/operations/index.md',
    'Pure Storage Operations Hub — Pure1 portal, alerts severity, support cases P1-P4',
)
def pure_operations_hub():
    """Pure Storage Operations Hub — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure Storage Operations Hub'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Pure Storage Operations — Pure1, Alerts, and Support Case Management')))
    lines.append(R(bMid(IV_L, IV_R, 'Pure1 cloud portal: central management for all FlashArray and FlashBlade arrays globally')))
    lines.append(R(bMid(IV_L, IV_R, 'Alerts: hardware, software, and capacity events; severity levels Info, Warning, Error, Critical')))
    lines.append(R(bMid(IV_L, IV_R, 'Support cases: opened via Pure1 or phone; include log bundle, serial number, and impact')))
    lines.append(R(bMid(IV_L, IV_R, 'Proactive support: Pure1 AI detects anomalies and opens cases automatically before failure')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 feeds alerts and support workflows — day-to-day ops span portal, CLI, and case management'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pure1 Portal'),
        bMid(B2_L, B2_R, 'Alerts'),
        bMid(B3_L, B3_R, 'Support Cases'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array fleet dashboard'),
        bMid(B2_L, B2_R, 'Severity: Info → Critical'),
        bMid(B3_L, B3_R, 'Open via Pure1 or phone'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacity + perf analytics'),
        bMid(B2_L, B2_R, 'Hardware alerts: drive, CT'),
        bMid(B3_L, B3_R, 'Collect: log bundle + SN'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AI-driven health insights'),
        bMid(B2_L, B2_R, 'SW alerts: Purity version'),
        bMid(B3_L, B3_R, 'Severity: P1-P4 tiers'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Upgrade scheduler: NDU'),
        bMid(B2_L, B2_R, 'Capacity alerts: >80%'),
        bMid(B3_L, B3_R, 'Remote assist session'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Proactive case auto-open'),
        bMid(B2_L, B2_R, 'Repl alerts: lag + state'),
        bMid(B3_L, B3_R, 'TAM for strategic issues'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Pure1 provides fleet visibility · Alerts drive action'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pure1 Features', 'Alert Types', 'Case Workflow', 'Escalation', 'CLI Commands'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Fleet dashboard', 'Drive failure', 'Collect log bundle', 'TAM engagement', 'purearray list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Capacity forecast', 'CT warning', 'Describe impact', 'Remote assist', 'purealert list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Perf analytics', 'Purity upgrade', 'Submit via portal', 'Exec escalation', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Upgrade schedule', 'Capacity >80%', 'P1: 24/7 response', 'VP escalation', 'purelog download'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray / FlashBlade arrays · customer data centre · Pure1 cloud (SaaS portal) · Internet uplink'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Pure1         = Cloud management portal for all Pure arrays; telemetry, AI health, and upgrade'))
    lines.append(txt_row('Alert severity= Info (FYI) · Warning (monitor) · Error (investigate) · Critical (act immediately)'))
    lines.append(txt_row('Log bundle    = puresupport bundle command output; full diagnostic archive for support case'))
    lines.append(txt_row('Proactive case= Pure1 AI opens a support case automatically when anomaly detected before failure'))
    lines.append(txt_row('P1 case       = Severity 1; production down or data loss; 24/7 response SLA, engineer on phone'))
    lines.append(txt_row('P2 case       = Severity 2; degraded performance or risk; business-hours response with engineer'))
    lines.append(txt_row('Remote assist = Pure engineer connects via secure tunnel to live array for real-time troubleshooting'))
    lines.append(txt_row('TAM           = Technical Account Manager; Pure named escalation contact for strategic accounts'))
    lines.append(txt_row('NDU scheduler = Non-Disruptive Upgrade scheduler in Pure1; picks maintenance window for Purity update'))
    lines.append(txt_row('purealert     = CLI command to list, acknowledge, and filter alerts on FlashArray or FlashBlade'))
    lines.append(txt_row('Capacity alert= Fires when array used capacity exceeds configured threshold (default 80%)'))
    lines.append(txt_row('SN            = Serial number; required in every Pure support case for array identification'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


def pure_flasharray_arch():
    """Pure FlashArray Architecture overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FlashArray Architecture — Purity//FA Operating System')))
    lines.append(R(bMid(IV_L, IV_R, 'Dual-controller HA: CT0 + CT1 active/active, NVRAM write mirroring, < 1 ms write ACK')))
    lines.append(R(bMid(IV_L, IV_R, 'NVMe flash shelves: DirectFlash modules eliminate SSD translation layer for lower latency')))
    lines.append(R(bMid(IV_L, IV_R, 'Inline dedup + compression + thin provisioning applied before data hits flash media')))
    lines.append(R(bMid(IV_L, IV_R, 'Scale-up: add flash shelves to existing array; scale-out via FlashArray//X and FlashArray//C')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Purity//FA manages the full data path from host I/O down to DirectFlash modules'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Controller Layer (CT0 / CT1)'),
        bMid(B2_L, B2_R, 'Data Services Layer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Active/active: both serve I/O'),
        bMid(B2_L, B2_R, 'Inline dedup: global hash table'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NVRAM: mirror write buffer CT0-CT1'),
        bMid(B2_L, B2_R, 'Compression: LZ4 + pattern detect'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Failover: < 30 s automatic takeover'),
        bMid(B2_L, B2_R, 'Thin provisioning: no pre-allocation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'FC / iSCSI / NVMe/FC host ports'),
        bMid(B2_L, B2_R, 'Snapshots: read-only space-efficient'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Mgmt: REST API + GUI + CLI'),
        bMid(B2_L, B2_R, 'Clones: writable snapshot copies'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Controllers handle protocol termination · Data services run inline on every I/O'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Controller HW', 'Flash Shelves', 'Protocols', 'Replication', 'HA Behavior'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Dual-port HBAs', 'DirectFlash DFM', 'FC: 16/32G', 'ActiveDR: async', 'CT failover <30s'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NVRAM modules', 'NVMe-attached', 'iSCSI: 10/25G', 'ActiveCluster sync', 'NVRAM protects'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['10/25G eth mgmt', 'No RAID overhead', 'NVMe/FC ports', 'PG schedules', 'No data loss'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Out-of-band IPMI', 'Hot-pluggable', 'NVMe/RoCE', 'Cloud snap target', 'Transparent'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray chassis (//X, //C, //E) · DirectFlash Shelf · FC/iSCSI HBAs · SAN switches · dual PSU'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Purity//FA    = FlashArray OS; manages data services, protocols, and replication'))
    lines.append(txt_row('CT0 / CT1     = Controller 0 and 1; active/active HA pair serving I/O simultaneously'))
    lines.append(txt_row('NVRAM         = Non-volatile RAM write buffer; mirrored between controllers before host ACK'))
    lines.append(txt_row('DirectFlash   = Pure custom NVMe SSD (DFM); removes FTL layer for deterministic low latency'))
    lines.append(txt_row('Inline dedup  = Global deduplication run inline on every write; reduces effective flash usage'))
    lines.append(txt_row('ActiveCluster = Synchronous replication stretch cluster; zero RPO, zero RTO failover'))
    lines.append(txt_row('ActiveDR      = Asynchronous replication; RPO measured in minutes; automated failover'))
    lines.append(txt_row('Protection Group= PG; set of volumes/hosts replicated together on a defined schedule'))
    lines.append(txt_row('Snapshot      = Read-only, space-efficient point-in-time copy; metadata pointer only'))
    lines.append(txt_row('Clone         = Writable copy from snapshot; instant, no data movement required'))
    lines.append(txt_row('NVMe/RoCE     = NVMe over RDMA over Converged Ethernet; low-latency block over IP'))
    lines.append(txt_row('SafeMode      = Immutable snapshot protection; delete operations require Pure Storage PIN'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flasharray-arch-how',
    'docs/storage/pure/flasharray/architecture/how-it-works/index.md',
    'Pure FlashArray How It Works — I/O path, NVRAM, dedup, compression, HA failover',
)
def pure_flasharray_arch_how():
    """Pure FlashArray How It Works — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray — How It Works'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Write I/O Path: Host to HBA to Controller to NVRAM to Dedup/Compress to Flash')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 1: Host writes LUN; controller receives I/O on FC / iSCSI / NVMe port')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 2: Write lands in NVRAM on active CT; mirrored to peer CT via NVRAM link')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 3: ACK returned to host after NVRAM mirror; data is durable before ACK')))
    lines.append(R(bMid(IV_L, IV_R, 'Step 4: Purity destages NVRAM to DirectFlash: hash dedup then compress then write DFM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Host sees < 1 ms latency; NVRAM absorbs burst while destage happens asynchronously'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NVRAM Write Buffer'),
        bMid(B2_L, B2_R, 'Dedup / Compress Engine'),
        bMid(B3_L, B3_R, 'DirectFlash (DFM) Layer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CT0 NVRAM: primary'),
        bMid(B2_L, B2_R, 'Global hash: SHA fingerprint'),
        bMid(B3_L, B3_R, 'NVMe-native: no FTL layer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CT1 NVRAM: mirror copy'),
        bMid(B2_L, B2_R, 'Pattern: zero-block detect'),
        bMid(B3_L, B3_R, 'DFM wear-levelled by Purity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ACK: after both mirrors'),
        bMid(B2_L, B2_R, 'LZ4: inline compression'),
        bMid(B3_L, B3_R, 'Hot/warm/cold data tiers'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Capacitor backup: safe flush'),
        bMid(B2_L, B2_R, 'Reduction: 4:1 typical'),
        bMid(B3_L, B3_R, 'NAND: MLC/QLC modules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NVRAM drain on destage'),
        bMid(B2_L, B2_R, 'Written unique chunks only'),
        bMid(B3_L, B3_R, 'SSD life: Purity manages'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  HA failover: CT0 fails, CT1 takes all I/O; NVRAM safe; < 30 s transparent failover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Write Path', 'Read Path', 'HA Failover', 'Dedup Stats', 'CLI Verify'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Host to CT NVRAM', 'CT to DFM read', 'CT0 heartbeat lost', 'puredataset list', 'purearray get'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Mirror to peer CT', 'Cache hit first', 'CT1 takes over', 'Data reduction %', 'purearray monitor'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['ACK to host', 'NVRAM prefetch', '< 30 s RTO', 'Unique data GB', 'puredrive list'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Destage to flash', 'No rebuild needed', 'Transparent host', 'Space savings %', 'purevolume list'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('CT0 + CT1 controllers · NVRAM DIMMs · DirectFlash modules · SAS/NVMe shelf interconnect · FC switch'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('NVRAM mirror  = Synchronous mirror of write buffer between CT0 and CT1 before host ACK'))
    lines.append(txt_row('Destage       = Process of draining NVRAM writes to flash; runs continuously in background'))
    lines.append(txt_row('Inline dedup  = Deduplication applied on every I/O before write; global hash fingerprint'))
    lines.append(txt_row('LZ4           = Compression algorithm used by Purity; fast, low-CPU, good ratio on block data'))
    lines.append(txt_row('DFM           = DirectFlash Module; Pure-custom NVMe SSD with no FTL overhead layer'))
    lines.append(txt_row('FTL           = Flash Translation Layer; removed in DFM so Purity handles flash mapping directly'))
    lines.append(txt_row('Data reduction= Ratio of logical written to physical flash used; includes dedup + compression'))
    lines.append(txt_row('Capacitor     = Backup power on NVRAM; ensures safe flush to flash on power loss'))
    lines.append(txt_row('HA failover   = Automatic controller failover; CT1 adopts all I/O from failed CT0 within 30 s'))
    lines.append(txt_row('Read path     = Reads served from NVRAM cache or DirectFlash; no read penalty from dedup'))
    lines.append(txt_row('Zero-block    = Pattern-detected zero blocks stored as metadata only; highest dedup ratio'))
    lines.append(txt_row('Heartbeat     = Inter-controller health signal; loss triggers failover to surviving controller'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flasharray-arch-int',
    'docs/storage/pure/flasharray/architecture/integrations/index.md',
    'Pure FlashArray Integrations — VMware, Kubernetes, vVols, Pure Service Orchestrator',
)
def pure_flasharray_arch_int():
    """Pure FlashArray Integrations — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray Integrations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FlashArray Integration Ecosystem — VMware, Kubernetes, Backup, Cloud, Automation')))
    lines.append(R(bMid(IV_L, IV_R, 'VMware: VASA/VAAI plugin · vVols datastore · SPBM policy-driven provisioning')))
    lines.append(R(bMid(IV_L, IV_R, 'Kubernetes: Pure Service Orchestrator (PSO) / Portworx; dynamic PVC provisioning')))
    lines.append(R(bMid(IV_L, IV_R, 'Backup: Veeam, Commvault, Veritas via snapshot-based offload via Pure APIs')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: Ansible collection, Terraform provider, REST API v2 for all operations')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Pure REST API v2 is the integration backbone — all plugins and tools consume it'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VMware Integration'),
        bMid(B2_L, B2_R, 'Kubernetes / Containers'),
        bMid(B3_L, B3_R, 'Backup + Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VASA: storage policy mgmt'),
        bMid(B2_L, B2_R, 'PSO: dynamic PVC on-demand'),
        bMid(B3_L, B3_R, 'Veeam: snap-based offload'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VAAI: HW-accelerated ops'),
        bMid(B2_L, B2_R, 'CSI driver: standard K8s API'),
        bMid(B3_L, B3_R, 'Commvault: snap management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vVols: per-VM volumes'),
        bMid(B2_L, B2_R, 'Portworx: data services layer'),
        bMid(B3_L, B3_R, 'purestorage.flasharray'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SPBM: QoS per datastore'),
        bMid(B2_L, B2_R, 'StatefulSet persistent store'),
        bMid(B3_L, B3_R, 'Terraform: volume lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM: site recovery plans'),
        bMid(B2_L, B2_R, 'Multi-attach: RWX volumes'),
        bMid(B3_L, B3_R, 'REST v2: token auth + JSON'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  All integrations leverage REST API · VMware via VASA/VAAI · K8s via CSI/PSO'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VMware Setup', 'K8s Setup', 'Backup Config', 'REST API', 'Automation'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Install VASA plug', 'Deploy PSO helm', 'Register array IP', 'GET /arrays', 'ansible-galaxy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Create vVol store', 'Set storage class', 'API token creds', 'POST /volumes', 'terraform init'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SPBM policy assign', 'Test dynamic PVC', 'Snapshot schedule', 'PATCH /hosts', 'pureuser API add'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM plugin config', 'Verify PV bind', 'Offload verify', 'DELETE /volumes', 'Idempotent runs'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray controllers · ESXi hosts · K8s worker nodes · Backup media server · IP/FC SAN fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VASA          = vSphere API for Storage Awareness; allows vSphere to query array capabilities'))
    lines.append(txt_row('VAAI          = vSphere API for Array Integration; offloads clone, zero, lock ops to array HW'))
    lines.append(txt_row('vVols         = Virtual Volumes; per-VM volume objects managed directly by FlashArray'))
    lines.append(txt_row('SPBM          = Storage Policy-Based Management; assigns QoS and protection to VMs by policy'))
    lines.append(txt_row('PSO           = Pure Service Orchestrator; Kubernetes dynamic storage provisioner for Pure arrays'))
    lines.append(txt_row('CSI           = Container Storage Interface; standard Kubernetes block/file storage API'))
    lines.append(txt_row('Portworx      = Pure-owned container data platform; distributed storage layer for K8s workloads'))
    lines.append(txt_row('SRM           = Site Recovery Manager; VMware DR orchestration using Pure replication snapshots'))
    lines.append(txt_row('REST v2       = Pure FlashArray REST API version 2; JSON, token auth, full CRUD for all objects'))
    lines.append(txt_row('Ansible coll  = purestorage.flasharray Galaxy collection; modules for volumes, hosts, PGs'))
    lines.append(txt_row('Terraform     = HashiCorp IaC; purestorage/flasharray provider for declarative volume management'))
    lines.append(txt_row('API token     = Authentication credential for REST and automation; scoped to array user role'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'pure-flasharray-arch-design',
    'docs/storage/pure/flasharray/architecture/design-standards/index.md',
    'Pure FlashArray Design Standards — naming, zoning, host config, data reduction targets',
)
def pure_flasharray_arch_design():
    """Pure FlashArray Design Standards — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Pure FlashArray Design Standards'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'FlashArray Design Standards — Naming, Zoning, Host Config, Capacity Planning')))
    lines.append(R(bMid(IV_L, IV_R, 'Naming: array-name, volume, host, hgroup follow site-consistent lowercase-hyphen scheme')))
    lines.append(R(bMid(IV_L, IV_R, 'FC zoning: single-initiator / single-target; each HBA port zoned to one array port')))
    lines.append(R(bMid(IV_L, IV_R, 'Host connect: create host, add WWN/IQN, add to hgroup, connect volume to hgroup')))
    lines.append(R(bMid(IV_L, IV_R, 'Capacity: provision at 2x data-reduction estimate; alert threshold 80% array capacity')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Standards ensure consistent deployments across sites and reduce operational errors'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Naming and Zoning Standards'),
        bMid(B2_L, B2_R, 'Capacity and Performance Design'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Volume: appname-function-lun01'),
        bMid(B2_L, B2_R, 'Target data reduction: 4:1+'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Host: hostname matches DNS'),
        bMid(B2_L, B2_R, 'Provision: 2x DR estimate'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'hgroup: cluster or app group'),
        bMid(B2_L, B2_R, 'Alert: 80% capacity threshold'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'FC zone: SI-ST per HBA port'),
        bMid(B2_L, B2_R, 'QoS: bandwidth + IOPS limits'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'iSCSI: CHAP + portal per port'),
        bMid(B2_L, B2_R, 'Snap retention: 24h/7d/4w/1y'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PG: one PG per app tier'),
        bMid(B2_L, B2_R, 'Volume size: multiples of 1 TB'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Consistent naming and single-initiator zoning are the two most impactful design decisions'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Volume Design', 'Host Design', 'FC Zoning', 'PG Design', 'Monitoring'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['512-byte aligned', '1 host per hgroup', 'SI-ST mandatory', '1 PG per app', 'Pure1 DR metric'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Thin: no reserve', 'WWNs per HBA port', 'Zone activation', 'Hourly schedule', 'Capacity alerts'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Limit QoS shared', 'iSCSI: 2+ portals', 'Alias hostname_p1', 'Retain: 24 snaps', 'Latency < 1 ms'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LUN ID consistent', 'MPIO multipath', 'Verify login', 'Target: remote PG', 'purearray monitor'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('FlashArray pair · FC director switches · iSCSI ToR switches · ESXi/bare-metal hosts · Pure1 portal'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SI-ST zoning  = Single-Initiator/Single-Target; best practice FC zoning reduces blast radius'))
    lines.append(txt_row('hgroup        = Host group; collection of hosts sharing access to the same volumes'))
    lines.append(txt_row('Protection Group= PG; volumes/hosts replicated together on schedule; one PG per application'))
    lines.append(txt_row('Data reduction= Ratio of written logical data to physical flash used; 4:1 typical on VMs'))
    lines.append(txt_row('QoS limits    = Per-volume IOPS/bandwidth cap; set with purevolume setattr --iops-limit'))
    lines.append(txt_row('CHAP          = Challenge Handshake Auth Protocol; iSCSI authentication between host and array'))
    lines.append(txt_row('MPIO          = Multipath I/O; host multipath driver balances I/O across multiple array ports'))
    lines.append(txt_row('Thin provision= Volume allocated on demand; no physical flash reserved until data is written'))
    lines.append(txt_row('Snap retention= Schedule of snapshots kept: hourly, daily, weekly, monthly, yearly counts'))
    lines.append(txt_row('Portal        = iSCSI target endpoint; IP:port on array for iSCSI initiator discovery'))
    lines.append(txt_row('WWN           = World Wide Name; 64-bit FC identifier for initiator HBA port and target port'))
    lines.append(txt_row('Pure1 DR      = Pure1 shows data-reduction ratio per array; used to validate design targets'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


# ── AWS sub-section diagrams ───────────────────────────────────────────────────
