#!/usr/bin/env python3
"""
Generate SVG overview diagrams for VMware product landing pages (product/index.md).
Each product gets TWO SVGs:
  1. *-capabilities-overview.svg  — 3 key capability areas
  2. *-stack-overview.svg         — what manages it / the product / what it manages

Usage:
  python3 scripts/generate_svgs_landing.py            # generate + inject
  python3 scripts/generate_svgs_landing.py --generate # SVG files only, skip inject
  python3 scripts/generate_svgs_landing.py --inject   # inject only (SVGs must exist)
  python3 scripts/generate_svgs_landing.py --dry-run  # preview inject without writing

NOTE on ASCII diagrams:
  This script REPLACES the ASCII diagram block on each page with SVG img tags.
  The ASCII definitions are NOT deleted — they live in scripts/diagrams/*.py and
  can be regenerated with `python3 scripts/ascii_diagram_gen.py --write-all`.
  After running this script, `ascii_diagram_gen.py --check` will show these pages
  as OUT OF SYNC. To silence that, comment out the matching @kb_diagram decorator
  in the relevant scripts/diagrams/*.py file.
"""
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO / 'scripts'))
from svg_helpers import make_svg, inject_svgs  # noqa: E402

ASSETS = REPO / 'docs' / 'assets'

# ── Colour palettes (name, sub, hdr, light, dark, mid) ───────────────────────
BLUE   = ('#1565c0', '#e3f2fd', '#1565c0', '#90caf9')
PURPLE = ('#6a1b9a', '#f3e5f5', '#4a148c', '#ce93d8')
TEAL   = ('#00695c', '#e0f2f1', '#004d40', '#80cbc4')
GREY   = ('#37474f', '#eceff1', '#37474f', '#b0bec5')
ORANGE = ('#e65100', '#fbe9e7', '#bf360c', '#ffab91')
RED    = ('#b71c1c', '#ffebee', '#7f0000', '#ef9a9a')


def col(name, sub, palette, items, notes):
    hdr, light, dark, mid = palette
    return (name, sub, hdr, light, dark, mid, items, notes)


# ── SVG data ─────────────────────────────────────────────────────────────────

def _vcenter_caps():
    return make_svg(
        'vCenter Server — Capabilities Overview',
        'Cluster Services · Lifecycle · Management Plane',
        [
            col('Cluster Services', 'DRS · HA · vMotion · DPM', BLUE,
                ['DRS (workload balancing)', 'HA (host failure restart)',
                 'vMotion (live migration)', 'DPM (power management)',
                 'Resource Pools / Shares'],
                ['DRS: fully automated recommended', 'HA: restarts VMs on host failure',
                 'HA admission control: 25% reserve', 'vMotion: zero-downtime move',
                 'Fault Domains: host/rack isolation',
                 'Storage DRS: datastore balancing']),
            col('Lifecycle & Operations', 'LCM · Patching · Alarms', PURPLE,
                ['LCM (host patch / upgrade)', 'vSphere Update Manager (VUM)',
                 'Alarm definitions + actions', 'Performance charts / metrics',
                 'File-based backup (VAMI)'],
                ['LCM: baseline / image-based', 'VUM: scan → remediate hosts',
                 'VAMI port 5480: appliance mgmt', 'Backup: SFTP or NFS schedule',
                 'Alarms: email + SNMP trap',
                 'Cert renewal: VMCA or 3rd-party']),
            col('Management Plane', 'SSO · RBAC · vDS · APIs', TEAL,
                ['SSO + AD/LDAP identity source', 'RBAC (roles + permissions)',
                 'vDS (distributed switching)', 'Content Library (templates)',
                 'vSphere REST API / SDK'],
                ['SSO domain: vsphere.local', 'RBAC: global + object-level perms',
                 'vDS: QoS, LACP, port mirroring', 'Content Library: OVA / ISO sync',
                 'Tags: VM classification + search',
                 'API: /api/vcenter (REST)']),
        ],
        'vCenter Edition Comparison',
        ['Feature', 'vCenter Standard', 'vCenter Essentials', 'vCenter Foundation'],
        [('Host limit', 'Unlimited', '3 hosts per kit', '4 hosts per kit'),
         ('vSphere HA', '✓', '✓', '✓'),
         ('DRS / DPM', '✓', '✗', '✗'),
         ('vMotion', '✓', '✗ (Storage only)', '✓'),
         ('Linked Mode', '✓ (ELM)', '✗', '✗'),
         ('vSAN support', '✓', '✓', '✓')],
        'VMware vCenter Reference · Cluster Services · Lifecycle · Management Plane · VCSA'
    )


def _vcenter_stack():
    return make_svg(
        'vCenter Server — Stack Position',
        'What manages vCenter · VCSA core · What vCenter manages',
        [
            col('Managed By', 'Aria · VCF · Admin UI', GREY,
                ['Aria Operations (monitoring)', 'SDDC Manager (VCF LCM)',
                 'vSphere Client UI (admin)', 'REST API / PowerCLI scripts',
                 'vCenter HA (self-managed)'],
                ['Aria Ops: perf + capacity alerts', 'SDDC Mgr: patch orchestration',
                 'vSphere Client: daily admin ops', 'PowerCLI: bulk automation',
                 'VAMI :5480: appliance config']),
            col('vCenter VCSA', 'Management control plane', BLUE,
                ['VCSA (Linux appliance OVA)', 'Embedded PSC (vSphere 7+)',
                 'vPostgres (inventory DB)', 'SSO domain (vsphere.local)',
                 'VAMI (port 5480)'],
                ['Single pane: hosts, VMs, nets', 'SSO: one login across vSphere',
                 'DB: all inventory + events', 'HA option: active/passive/witness',
                 'ELM: up to 15 vCenters linked']),
            col('Manages', 'Hosts · VMs · Networking', TEAL,
                ['ESXi hosts (clusters)', 'Virtual Machines + vApps',
                 'vDS (distributed switch)', 'Datastores (VMFS/NFS/vSAN)',
                 'NSX-T (via plugin)'],
                ['Host: adds to inventory, monitors', 'VM: create, clone, snapshot, move',
                 'vDS: port groups, VLANs, QoS', 'Datastore: browse, migrate, provision',
                 'NSX plugin: network topology view']),
        ],
        'vCenter Integration Points',
        ['Integration', 'Direction', 'Protocol / Port', 'Purpose'],
        [('ESXi hosts', 'vCenter → ESXi', 'HTTPS 443 / 902', 'Management + VPXA'),
         ('NSX Manager', 'Registered plugin', 'HTTPS 443', 'Network topology'),
         ('Aria Operations', 'Aria → vCenter', 'HTTPS 443', 'Metrics + inventory'),
         ('SDDC Manager', 'Calls vCenter API', 'HTTPS 443', 'LCM orchestration'),
         ('vSphere Client', 'Browser → vCenter', 'HTTPS 443', 'Admin UI'),
         ('Backup tool', 'Veeam/Commvault', 'HTTPS 443 / NBD', 'VM data protection')],
        'VMware vCenter Reference · VCSA · SSO · ESXi · vDS · Aria Operations · VCF'
    )


def _vsan_caps():
    return make_svg(
        'vSAN — Capabilities Overview',
        'Storage Platform · Data Services · Operations',
        [
            col('Storage Platform', 'HCI · Policies · Encryption', BLUE,
                ['Disk Groups / Single Pool (ESA)', 'Storage Objects (components)',
                 'SPBM (storage policy engine)', 'Encryption at rest (KMS)',
                 'Dedup + Compression (all-flash)'],
                ['OSA: cache + capacity disk groups', 'ESA: single NVMe pool, no groups',
                 'SPBM: FTT, RAID, IOPS limits', 'Encryption: per-cluster KMS key',
                 'Dedup ratio: 4–7× typical',
                 'Thin provisioning: always on']),
            col('Data Services', 'Snapshots · iSCSI · File', PURPLE,
                ['Space-efficient snapshots', 'iSCSI target service',
                 'vSAN File Services (NFS v4)', 'Cloud Tiering (cold data)',
                 'Stretched Cluster (metro DR)'],
                ['Snapshots: capacity-aware delta', 'iSCSI: bare-metal + VMs',
                 'File Services: NFS share export', 'Cloud tier: S3 offload',
                 'Stretched: 2 sites + witness',
                 'Witness: VM or cloud (ESXi)']),
            col('Operations', 'Health · Rebalance · Perf', TEAL,
                ['Skyline Health (170+ checks)', 'Proactive rebalance',
                 'Performance Service', 'vSAN Observer diagnostics',
                 'HCL health integration'],
                ['Health: automated remediation hints', 'Rebalance: triggered on imbalance >10%',
                 'Perf service: per-VM IOPS graph', 'Observer: detailed trace on demand',
                 'HCL: flags unsupported hardware',
                 'clomRepairDelay: default 60 min']),
        ],
        'vSAN Edition Feature Comparison',
        ['Feature', 'vSAN Standard', 'vSAN Advanced', 'vSAN Enterprise Plus'],
        [('Dedup + Compression', '✗', '✓', '✓'),
         ('Encryption', '✗', '✗', '✓'),
         ('Stretched Cluster', '✗', '✗', '✓'),
         ('iSCSI Target', '✓', '✓', '✓'),
         ('File Services', '✗', '✓', '✓'),
         ('HCI Mesh (remote DS)', '✗', '✓', '✓')],
        'VMware vSAN Reference · HCI Storage · SPBM · Skyline Health · Encryption · OSA · ESA'
    )


def _vsan_stack():
    return make_svg(
        'vSAN — Stack Position',
        'What manages vSAN · vSAN platform · What vSAN provides',
        [
            col('Managed By', 'vCenter · Aria · PowerCLI', GREY,
                ['vCenter (primary management)', 'SDDC Manager (VCF LCM)',
                 'Aria Operations (monitoring)', 'PowerCLI / esxcli',
                 'vSAN Health UI plugin'],
                ['vCenter: cluster enable, disk claim', 'SDDC Mgr: LCM + validation',
                 'Aria Ops: capacity + perf alerts', 'esxcli: low-level diagnostics',
                 'Health UI: Skyline + HCL checks']),
            col('vSAN Platform', 'Distributed datastore engine', BLUE,
                ['Cluster datastore (all hosts)', 'CLOM (object placement)', 'DOM (data mgmt layer)',
                 'LSOM (log-struct object store)', 'Health service (continuous)'],
                ['CLOM: places + repairs objects', 'DOM: coordinates reads/writes',
                 'LSOM: write log on each disk', 'Witness: quorum for 2-node',
                 'Resync: auto on host rejoin']),
            col('Provides', 'VMs · iSCSI · NFS · Witness', TEAL,
                ['vSAN datastore (VMFS-like API)', 'iSCSI target (bare-metal)',
                 'NFS shares (File Services)', 'Witness traffic for 2-node',
                 'S3 cloud tier (cold data)'],
                ['Datastore: single namespace', 'IOPS/throughput via SPBM limits',
                 'iSCSI: initiator groups + LUNs', 'File Services: NFS v4.1',
                 'Cloud tier: read-heavy workloads']),
        ],
        'vSAN Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter', 'Manages vSAN cluster', 'In-band vSAN API', 'Config, health, policies'),
         ('NSX', 'Traffic on vSAN NIC', 'Shared 10GbE NIC', 'VXLAN overlay via vmknic'),
         ('Aria Operations', 'Collects metrics', 'vCenter adapter', 'Capacity + perf'),
         ('Veeam / Commvault', 'Backup VMs on vSAN', 'NBD / HotAdd', 'Data protection'),
         ('KMS server', 'Encryption keys', 'KMIP / HTTPS', 'At-rest encryption'),
         ('Witness host', 'Quorum membership', 'vSAN VMkernel port', 'Split-brain prevention')],
        'VMware vSAN Reference · HCI · CLOM · SPBM · Skyline Health · Stretched Cluster'
    )


def _nsx_caps():
    return make_svg(
        'NSX — Capabilities Overview',
        'Network Virtualization · Security · Operations',
        [
            col('Network Virtualization', 'Segments · Gateways · Routing', BLUE,
                ['Overlay Segments (VXLAN/Geneve)', 'Tier-0 Gateway (N-S routing)',
                 'Tier-1 Gateway (E-W routing)', 'BGP / OSPF / static routing',
                 'NAT / Load Balancer / DHCP'],
                ['T0: connects to physical routers', 'T1: tenant-level segmentation',
                 'ECMP: active/active T0 uplinks', 'BGP: dynamic peering to ToR',
                 'Segments: per-tenant isolation',
                 'TEP: VXLAN/Geneve tunnel EP']),
            col('Security', 'DFW · Gateway FW · IDS/IPS', PURPLE,
                ['DFW (distributed firewall)', 'Gateway Firewall (perimeter)',
                 'IDS/IPS (intrusion detection)', 'URL Analysis / FQDN groups',
                 'Security Groups / Tags'],
                ['DFW: stateful at each vNIC', 'Zero-trust microsegmentation',
                 'IDS: signature-based + ML', 'Gateway FW: North-South edge',
                 'URL: HTTPS inspection TLS-out',
                 'Groups: dynamic VM membership']),
            col('Operations', 'Manager · Federation · API', TEAL,
                ['NSX Manager (3-node cluster)', 'NSX Federation (multi-site)', 'NSX Intelligence (flow analysis)',
                 'Policy API (declarative)', 'CLI: nsxcli on edge/manager'],
                ['Manager cluster: active/active/active', 'Federation: global + local mgrs',
                 'Intelligence: visualise traffic flows', 'Policy: intent-based API',
                 'CCP: central control plane',
                 'Traceflow: packet-level debug']),
        ],
        'NSX Edition Comparison',
        ['Feature', 'NSX Base', 'NSX Professional', 'NSX Enterprise Plus'],
        [('DFW (micro-seg)', '✓', '✓', '✓'),
         ('Gateway Firewall', '✗', '✓', '✓'),
         ('IDS / IPS', '✗', '✓', '✓'),
         ('NSX Intelligence', '✗', '✗', '✓'),
         ('Federation', '✗', '✗', '✓'),
         ('URL Analysis', '✗', '✓', '✓')],
        'VMware NSX Reference · Overlay · DFW · Gateway FW · IDS/IPS · BGP · TEP'
    )


def _nsx_stack():
    return make_svg(
        'NSX — Stack Position',
        'What manages NSX · NSX platform · What NSX manages',
        [
            col('Managed By', 'vCenter · Aria · SDDC Mgr', GREY,
                ['NSX Manager UI / API (primary)', 'vCenter (compute integration)',
                 'SDDC Manager (VCF deployment)', 'Aria Ops for Networks',
                 'Terraform NSX provider'],
                ['NSX Manager: declarative policy', 'vCenter: registers transport nodes',
                 'SDDC Mgr: initial deploy + LCM', 'Aria Net: topology + flow visibility',
                 'Terraform: IaC for segments/FW']),
            col('NSX Platform', 'Manager · CCP · TEP network', BLUE,
                ['NSX Manager (3-node HA cluster)', 'NSX Controller (CCP)', 'Transport Nodes (ESXi + Edge)',
                 'TEP network (overlay tunnel)', 'Edge VMs (N-S gateway)'],
                ['Manager cluster: mgmt + policy API', 'CCP: distributed routing state',
                 'Transport nodes: ESXi + Edge VMs', 'TEP: Geneve UDP 6081 tunnels',
                 'Edge VMs: T0 N-S + load balancer']),
            col('Manages', 'Segments · VMs · Edge · Physical', TEAL,
                ['Overlay Segments (VM networks)', 'VM vNICs (DFW rules applied)',
                 'Edge Nodes (T0 / T1 gateways)', 'Physical router (BGP peering)',
                 'VLAN-backed Segments (trunk)'],
                ['Segments: per-tenant L2 domains', 'DFW: kernel-level VM firewall',
                 'Edge: N-S traffic + NAT + LB', 'BGP: advertises segment CIDRs',
                 'VLAN segment: physical uplink']),
        ],
        'NSX Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter', 'NSX registers w/ vCenter', 'HTTPS 443', 'Compute + host prep'),
         ('ESXi transport nodes', 'NSX → ESXi', 'NSX MPA', 'Install DFW + TEP vmknic'),
         ('Aria Ops for Networks', 'Pulls NSX data', 'NSX API HTTPS', 'Flow analysis + topology'),
         ('Physical routers', 'T0 peering', 'BGP (TCP 179)', 'Route advertisement'),
         ('SDDC Manager', 'Manages NSX deploy', 'HTTPS 443', 'Lifecycle management'),
         ('Aria Automation', 'Provisions segments', 'NSX REST API', 'IaC network provisioning')],
        'VMware NSX Reference · DFW · Overlay · Gateway FW · IDS/IPS · Federation · TEP'
    )


def _esxi_caps():
    return make_svg(
        'ESXi — Capabilities Overview',
        'Hypervisor Core · Storage · Networking',
        [
            col('Hypervisor Core', 'VMkernel · Scheduling · HA', BLUE,
                ['VMkernel (microkernel OS)', 'CPU scheduler (NUMA-aware)',
                 'Memory balloon + swap', 'Resource Pools / Shares / Limits',
                 'Host Profiles (config compliance)'],
                ['VMkernel: bare-metal hypervisor', 'CPU: fairshares per VM pool',
                 'NUMA: local memory preferred', 'HA agent: heartbeat to vCenter',
                 'DRS agent: vMotion on overcommit',
                 'Host profiles: enforce config']),
            col('Storage', 'VMFS · NFS · iSCSI · FC · vSAN', PURPLE,
                ['VMFS-6 (local + shared SAN)', 'NFS 3 / NFS 4.1 datastores',
                 'iSCSI (software + HW initiator)', 'Fibre Channel (FC / FCoE)',
                 'vSAN (HCI local disks)'],
                ['VMFS: clustered FS, locks per VM', 'NFS: mount via vmknic',
                 'iSCSI: round-robin multipath MIO', 'FC: NPIV for per-VM zoning',
                 'NVMe over Fabrics (NVMe-oF)',
                 'RDM: raw device mapping for apps']),
            col('Networking', 'vSwitch · dvSwitch · NSX', TEAL,
                ['Standard vSwitch (per-host)', 'vDS (distributed switch)', 'VLANs (802.1Q tagging)',
                 'SR-IOV (NIC passthrough)', 'NSX transport node (overlay)'],
                ['vSwitch: no cross-host config', 'vDS: central config, LACP, QoS',
                 'VLAN: trunk or access port group', 'SR-IOV: bypass hypervisor stack',
                 'NSX: TEP vmknic for VXLAN',
                 'RDMA: iWARP/RoCE for vSAN ESA']),
        ],
        'ESXi Free vs Licensed Features',
        ['Feature', 'ESXi Free (ESXF)', 'vSphere Ess. Kit', 'vSphere Standard+'],
        [('HA / DRS / vMotion', '✗', '✓ (basic)', '✓ (full)'),
         ('vSAN', '✗', '✓ (Ess. kit)', '✓'),
         ('vDS (distributed switch)', '✗', '✗', '✓'),
         ('NSX-T transport node', '✗', '✗', '✓'),
         ('Host Profiles', '✗', '✗', '✓'),
         ('API access', 'Read-only', '✓', '✓')],
        'VMware ESXi Reference · VMkernel · VMFS · vDS · vSAN · HA · iSCSI · FC'
    )


def _esxi_stack():
    return make_svg(
        'ESXi — Stack Position',
        'What manages ESXi · ESXi hypervisor · What ESXi manages',
        [
            col('Managed By', 'vCenter · iDRAC · esxcli', GREY,
                ['vCenter (cluster management)', 'SDDC Manager (VCF LCM)',
                 'iDRAC / iLO (hardware BMC)', 'SSH + DCUI (direct access)',
                 'esxcli / PowerCLI (scripting)'],
                ['vCenter: provisions, monitors, HA', 'SDDC Mgr: patch + lifecycle',
                 'iDRAC: power, BIOS, KVM, logs', 'DCUI: emergency console access',
                 'esxcli: low-level host commands']),
            col('ESXi Hypervisor', 'VMkernel + VMs + agents', BLUE,
                ['VMkernel (type-1 hypervisor)', 'VM execution (VMX process/VM)',
                 'VMkernel NICs (vmk0, vmk1...)', 'Storage I/O controller', 'VPXA (vCenter agent)'],
                ['VMkernel: no general-purpose OS', 'VMX: one process per running VM',
                 'vmk0: management network', 'VPXA: heartbeat to vCenter 5 s',
                 'NSX: DVS installed as VIB']),
            col('Manages', 'VMs · Datastores · Networking', TEAL,
                ['Virtual Machines + vApps', 'Datastores (VMFS/NFS/vSAN)',
                 'Physical NICs + vSwitch', 'vSAN disk groups (HCI)',
                 'Passthrough devices (PCI/SR-IOV)'],
                ['VM: full isolation per guest', 'VMFS: clustered on shared storage',
                 'vSwitch: L2 switching in kernel', 'vSAN: disk claim on add',
                 'PCI passthrough: GPU/FPGA/NIC']),
        ],
        'ESXi Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter VCSA', 'vCenter → ESXi', 'HTTPS 443 / 902', 'VPXA + management'),
         ('NSX Manager', 'NSX → ESXi', 'NSX MPA / VIB', 'DFW + TEP vmknic'),
         ('Aria Operations', 'Pulls metrics', 'vCenter adapter', 'Perf + capacity'),
         ('SAN / NAS storage', 'ESXi → storage', 'FC / iSCSI / NFS', 'Datastore access'),
         ('Backup proxy', 'Veeam / Commvault', 'HotAdd / NBD', 'VM snapshot read'),
         ('iDRAC / iLO', 'BMC side-band', 'IPMI / HTTPS', 'Power + hardware health')],
        'VMware ESXi Reference · VMkernel · VMFS · NFS · iSCSI · FC · vDS · vSAN · NSX'
    )


def _vcf_caps():
    return make_svg(
        'VMware Cloud Foundation — Capabilities Overview',
        'Management Domain · Workload Domains · Lifecycle Services',
        [
            col('Management Domain', 'SDDC Mgr · NSX · vCenter · vSAN', BLUE,
                ['SDDC Manager (orchestrator)', 'NSX Management Cluster',
                 'vCenter (management VMs)', 'vSAN Datastore (management)',
                 'Aria Suite Lifecycle (optional)'],
                ['SDDC Mgr: single pane of mgmt', 'NSX Mgmt: overlay for mgmt VMs',
                 'vCenter: manages mgmt domain hosts', 'vSAN: management domain storage',
                 'Cloud Builder: initial bring-up',
                 'BOM: validated version matrix']),
            col('Workload Domains', 'VI · vSAN WD · NSX Edge', PURPLE,
                ['VI Workload Domain (VMs)', 'vSAN Workload Domain', 'Dedicated vCenter per WD',
                 'NSX Instance (per WD or shared)', 'Edge Cluster (NSX T0/T1)'],
                ['WD: isolated compute + network', 'Each WD: own vCenter + NSX edge',
                 'Multiple WDs per VCF instance', 'Shared NSX: mgmt + workload',
                 'Edge: N-S traffic for workloads',
                 'Stretch: extend WD to 2nd site']),
            col('Lifecycle Services', 'LCM · Health · BOM', TEAL,
                ['Cloud Builder (initial deploy)', 'BOM (bill of materials)', 'Automated LCM (patch/upgrade)',
                 'Health status dashboard', 'Password lifecycle management'],
                ['Cloud Builder: JSON spec → SDDC', 'BOM: approved version combos',
                 'LCM: rolling host/component patch', 'Health: continuous checks per WD',
                 'Password: auto-rotation per policy',
                 'Async Patch: OOB hotfixes']),
        ],
        'VCF Edition Comparison',
        ['Feature', 'VCF Standard', 'VCF Advanced', 'VCF Enterprise'],
        [('Workload Domains', '✓', '✓', '✓'),
         ('NSX Federation', '✗', '✗', '✓'),
         ('HCI Mesh', '✗', '✓', '✓'),
         ('Multi-site stretch', '✗', '✓', '✓'),
         ('Aria Suite (Advanced)', '✗', '✓', '✓'),
         ('Tanzu Kubernetes Grid', '✗', '✗', '✓')],
        'VMware VCF Reference · SDDC Manager · Management Domain · Workload Domains · BOM · LCM'
    )


def _vcf_stack():
    return make_svg(
        'VMware Cloud Foundation — Stack Position',
        'What manages VCF · VCF platform · What VCF manages',
        [
            col('Managed By', 'Cloud Builder · Aria · API', GREY,
                ['Cloud Builder (initial deploy)', 'SDDC Manager UI (ongoing)',
                 'Aria Suite (monitoring/auto)', 'VCF REST API (automation)',
                 'vSphere Client (day-2 ops)'],
                ['Cloud Builder: JSON → full SDDC', 'SDDC Mgr: LCM, passwords, health',
                 'Aria: capacity + compliance', 'REST API: IaC integrations',
                 'vSphere Client: VM-level ops']),
            col('VCF Platform', 'SDDC Mgr + BOM engine + LCM', BLUE,
                ['SDDC Manager (control tower)', 'BOM Engine (version validation)', 'LCM Engine (patch orchestration)',
                 'NSX Management Cluster', 'Cloud Builder (one-time)'],
                ['SDDC Mgr: tracks all components', 'BOM: enforces compatible versions',
                 'LCM: rolling automated patches', 'NSX Mgmt: management overlay',
                 'Cloud Builder: retire after bring-up']),
            col('Manages', 'Domains · Hosts · Patching', TEAL,
                ['Management Domain (always)', 'Workload Domains (per team/app)',
                 'Host commissioning / decommission', 'Component patch orchestration',
                 'Password + cert lifecycle'],
                ['Mgmt domain: infra VMs only', 'WDs: isolated per department',
                 'Host: validated, claimed, added', 'Patch: pre-check → rolling → post-check',
                 'Password: rotation per schedule']),
        ],
        'VCF Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter instances', 'SDDC Mgr → vCenter', 'HTTPS 443', 'Cluster + host management'),
         ('NSX Manager', 'SDDC Mgr → NSX', 'HTTPS 443', 'Network lifecycle'),
         ('vSAN datastores', 'Managed inside WD', 'vSAN API', 'Storage per domain'),
         ('Aria Suite Lifecycle', 'Separate product', 'HTTPS 443', 'Aria product deploy'),
         ('Cloud Builder', 'One-time deploy', 'HTTPS 443 + JSON', 'Initial bring-up only'),
         ('External DNS / NTP', 'SDDC Mgr reads', 'DNS 53 / NTP 123', 'Required prereqs')],
        'VMware VCF Reference · SDDC Manager · BOM · Workload Domains · LCM · Cloud Builder'
    )


def _horizon_caps():
    return make_svg(
        'VMware Horizon — Capabilities Overview',
        'Brokering · Desktop Pools · Protocol & Experience',
        [
            col('Brokering', 'Connection Servers · UAG · SSO', BLUE,
                ['Connection Servers (HA pair)', 'Unified Access Gateway (UAG)',
                 'True SSO (Kerberos tickets)', 'Load Balancer (NSX / F5)',
                 'Horizon Client (all platforms)'],
                ['Connection Server: broker sessions', 'UAG: external access no VPN',
                 'True SSO: smart card + cert', 'LB: NSX ALB or F5 in front',
                 'HTML Access: browser client',
                 'Client: Win/Mac/Linux/iOS/Android']),
            col('Desktop Pools', 'Instant Clone · RDSH · Apps', PURPLE,
                ['Instant Clone (stateless VDI)', 'Full Clone (persistent VDI)',
                 'RDSH (published desktops)', 'App Publishing (per-app launch)',
                 'Floating vs Dedicated pools'],
                ['Instant clone: fast provision < 1 min', 'Full clone: persistent user data',
                 'RDSH: multi-session Win Server', 'App publish: seamless window', 'Floating: reset on logoff',
                 'Dedicated: user always same VM']),
            col('Protocol & Experience', 'Blast · PCoIP · USB · Print', TEAL,
                ['Blast Extreme (H.264 / HEVC)', 'PCoIP (legacy protocol)', 'USB Redirection (per-device)',
                 'Printer Redirection (ThinPrint)', 'Dynamic Environment Manager (DEM)'],
                ['Blast: preferred; H.264 adaptive', 'PCoIP: UDP 4172 protocol',
                 'USB: smart card / storage / audio', 'Print: virtual printer redirect',
                 'DEM: user profile + policy',
                 'Multi-monitor: up to 6 displays']),
        ],
        'Horizon Deployment Type Comparison',
        ['Feature', 'VDI (Instant Clone)', 'VDI (Full Clone)', 'RDSH Published'],
        [('VM per user', '1 (stateless)', '1 (persistent)', 'Shared sessions'),
         ('Provision time', '< 1 minute', '15–30 minutes', 'N/A (pre-built)'),
         ('User data persist', '✗ (reset on logoff)', '✓ (user disk)', '✓ (profile disk)'),
         ('Storage efficiency', 'High (shared base)', 'Low (full copy)', 'Very high'),
         ('Use case', 'Task workers', 'Power users', 'Shared apps'),
         ('GPU support', '✓ (vGPU)', '✓ (vGPU)', '✓ (vGPU RDS)')],
        'VMware Horizon Reference · Connection Server · UAG · Blast · PCoIP · DEM · vGPU'
    )


def _horizon_stack():
    return make_svg(
        'VMware Horizon — Stack Position',
        'What manages Horizon · Horizon platform · What Horizon manages',
        [
            col('Managed By', 'Horizon Console · vSphere · API', GREY,
                ['Horizon Console (admin UI)', 'vSphere Client (VM admin)',
                 'Aria Ops for Horizon', 'REST API (Horizon 8+)',
                 'UAG admin UI (:9443)'],
                ['Console: pools, entitlements, config', 'vSphere: manage template VMs',
                 'Aria: EUC capacity + UX metrics', 'REST API: automate pool actions',
                 'UAG: edge proxy config']),
            col('Horizon Platform', 'Connection Servers + services', BLUE,
                ['Connection Servers (broker pair)', 'Composer (full clone mgmt)',
                 'App Volumes (app attach)', 'DEM (Dynamic Env. Mgr)',
                 'UAG (external access proxy)'],
                ['Brokers: route sessions to VMs', 'Composer: linked-clone base mgmt',
                 'App Volumes: app layering', 'DEM: profile + policy inject',
                 'UAG: no DMZ VPN needed']),
            col('Manages', 'Desktop VMs · Sessions · Apps', TEAL,
                ['Desktop VMs (VDI pools)', 'RDSH session hosts', 'Published applications',
                 'User sessions + profiles', 'GPU-enabled VMs (vGPU)'],
                ['VDI pools: floating or dedicated', 'RDSH: Windows Server sessions',
                 'App publish: seamless window', 'Profile: FSLogix / DEM disk',
                 'vGPU: NVIDIA GRID partitions']),
        ],
        'Horizon Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter / vSphere', 'Horizon → vCenter', 'HTTPS 443', 'VM lifecycle'),
         ('Active Directory', 'Horizon → AD', 'LDAP / Kerberos', 'Auth + entitlement'),
         ('NSX / Load Balancer', 'In front of brokers', 'HTTPS / TCP', 'HA + external access'),
         ('Aria Ops for Horizon', 'Pulls session data', 'Horizon API', 'EUC monitoring'),
         ('App Volumes', 'Attach at login', 'SMB / vSphere API', 'App layering'),
         ('DEM (Dynamic Env Mgr)', 'Profile inject on login', 'SMB / GP', 'User environment')],
        'VMware Horizon Reference · Connection Server · UAG · Blast · Instant Clone · DEM'
    )


def _srm_caps():
    return make_svg(
        'Site Recovery Manager — Capabilities Overview',
        'Protection Groups · Recovery Plans · DR Operations',
        [
            col('Protection', 'Groups · Mapping · Replication', BLUE,
                ['Protection Groups (VM sets)', 'Inventory Mapping (folders/pools)',
                 'Network Mapping (src → dst)', 'vSphere Replication (RPO ≥ 5 min)',
                 'Array-Based Replication (ABR)'],
                ['PG: group related VMs together', 'Inventory map: place VMs in dst VC',
                 'Network map: re-IP or same VLAN', 'vSphere Rep: per-VM CBT replication',
                 'ABR: EMC SRDF / NetApp SnapMirror',
                 'Placeholder VMs: reserved in dst']),
            col('Recovery Plans', 'Steps · Priority · Scripts', PURPLE,
                ['Recovery Plan (ordered steps)', 'VM Priority (1–5 groups)', 'Pre/Post Power-On Scripts',
                 'IP Customization (re-IP on DR)', 'Message Prompts (manual gates)'],
                ['Plan: click Run to failover VMs', 'Priority 1: first VMs powered on',
                 'Scripts: call Aria / webhook', 'IP custom: static address remap',
                 'Prompts: wait for confirmation',
                 'RTO: configurable per priority']),
            col('DR Operations', 'Test · Failover · Failback', TEAL,
                ['Test Recovery (non-disruptive)', 'Planned Migration (zero-RPO)', 'Emergency Failover (any RPO)',
                 'Re-Protection (reverse replication)', 'Failback (return to primary)'],
                ['Test: bubble network, no impact', 'Planned: sync then power off src',
                 'Emergency: last consistent point', 'Re-protect: reverse repl direction',
                 'Failback: reverse plan execution',
                 'History: all runs logged']),
        ],
        'SRM Recovery Type Comparison',
        ['Operation', 'Test Recovery', 'Planned Migration', 'Emergency Failover'],
        [('Replication active?', 'Continues unchanged', 'Final sync then stop', 'Stop on failure'),
         ('Source VMs affected?', '✗ — no impact', '✓ — powered off', '✗ — already down'),
         ('RPO', 'N/A (bubble only)', 'Near-zero (sync)', 'Last replicated point'),
         ('RTO', 'Per plan priority', 'Per plan priority', 'Per plan priority'),
         ('Re-protect needed?', 'N/A', '✓', '✓'),
         ('Use case', 'Quarterly DR test', 'Planned maintenance', 'Actual disaster')],
        'VMware SRM Reference · Protection Groups · Recovery Plans · vSphere Replication · Failback'
    )


def _srm_stack():
    return make_svg(
        'Site Recovery Manager — Stack Position',
        'What manages SRM · SRM platform · What SRM manages',
        [
            col('Managed By', 'vSphere plugin · REST API', GREY,
                ['vSphere Client SRM plugin', 'SRM REST API (v1)',
                 'vSphere Replication UI', 'Aria Orchestrator (automation)',
                 'SRM Manager (service layer)'],
                ['vSphere Client: all SRM operations', 'REST API: automate test/failover',
                 'vSphere Rep UI: per-VM schedule', 'Aria Orch: custom DR workflows',
                 'SRM Mgr: Windows or VCSA embed']),
            col('SRM Platform', 'Server · Mappings · Plans', BLUE,
                ['SRM Server (per site)', 'Site Pairing (bidirectional)',
                 'Inventory + Network Mappings', 'Protection Groups', 'Recovery Plans'],
                ['Two SRM Servers (one per site)', 'Site pair: authenticated VCa ↔ VCb',
                 'Mappings: folder/pool/net src→dst', 'PGs: define what to protect',
                 'Plans: define how to recover']),
            col('Manages', 'VMs · Replication · Failover', TEAL,
                ['VM protection (via PGs)', 'vSphere Replication (per-VM RPO)', 'Array replication (EMC/NetApp)',
                 'Placeholder VMs at dst site', 'Network re-IP on recovery'],
                ['VM: replicated + protected in PG', 'vSphere Rep: 5 min min RPO',
                 'Array: block-level sync', 'Placeholder: registerd, not running',
                 'Re-IP: per-VM static IP map']),
        ],
        'SRM Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter (both sites)', 'SRM registers plugin', 'HTTPS 443', 'Inventory + VM ops'),
         ('vSphere Replication', 'Managed by SRM', 'HTTPS 8043', 'Per-VM delta replication'),
         ('Array SRA plugin', 'SRM → SRA → array', 'HTTPS / SOAP', 'Array snapshot control'),
         ('Aria Orchestrator', 'Calls SRM REST API', 'HTTPS 443', 'Custom DR workflows'),
         ('NSX (network mapping)', 'Map src→dst segments', 'NSX API', 'Re-IP after failover'),
         ('Aria Operations', 'Pulls SRM status', 'vCenter adapter', 'DR health dashboard')],
        'VMware SRM Reference · Protection Groups · Recovery Plans · vSphere Replication · Failback'
    )


def _tanzu_caps():
    return make_svg(
        'VMware Tanzu — Capabilities Overview',
        'Supervisor · TKG Clusters · Developer Tools',
        [
            col('Supervisor', 'Namespace Service · NSX · vSphere', BLUE,
                ['vSphere with Tanzu (Supervisor)', 'Namespace Service (per-team)', 'Supervisor VMs (3 nodes)',
                 'NSX or vDS networking', 'Harbor Registry (embedded)'],
                ['Supervisor: Kubernetes API on vSphere', 'Namespace: storage class + quotas',
                 'Supervisor VMs: control plane in VC', 'NSX: per-namespace load balancer',
                 'Harbor: image registry per namespace',
                 'kubectl vsphere login: SSO-based']),
            col('TKG Clusters', 'Workload K8s · Node Pools', PURPLE,
                ['TKG Workload Clusters', 'Node Pools (worker config)', 'Cluster Classes (templates)',
                 'Kubernetes add-ons (CNI/CSI)', 'Velero (backup + restore)'],
                ['TKG cluster: isolated K8s control plane', 'Node pool: VM class + count',
                 'Cluster class: versioned template', 'CNI: Antrea or NSX-T CNI',
                 'CSI: vSphere Cloud Provider',
                 'Velero: workload backup to S3']),
            col('Developer Tools', 'TMC · kubectl · Carvel', TEAL,
                ['Tanzu Mission Control (TMC)', 'kubectl vsphere plugin', 'Carvel tooling (packaging)',
                 'Tanzu Build Service (image build)', 'Bitnami App Catalog'],
                ['TMC: multi-cluster central mgmt', 'kubectl vsphere: login + context switch',
                 'Carvel: kapp/ytt/imgpkg/kbld', 'TBS: Buildpacks CI/CD images',
                 'App catalog: curated Helm charts',
                 'TAP: developer inner-loop platform']),
        ],
        'Tanzu Edition Comparison',
        ['Feature', 'Tanzu Standard', 'Tanzu Advanced', 'Tanzu Enterprise'],
        [('TKG on vSphere', '✓', '✓', '✓'),
         ('Tanzu Mission Control', '✗', '✓', '✓'),
         ('Tanzu Service Mesh', '✗', '✓', '✓'),
         ('Tanzu Build Service', '✗', '✓', '✓'),
         ('Tanzu App Platform', '✗', '✗', '✓'),
         ('Global cluster policy', '✗', '✓', '✓')],
        'VMware Tanzu Reference · Supervisor · TKG · TMC · Carvel · kubectl vsphere · Harbor'
    )


def _tanzu_stack():
    return make_svg(
        'VMware Tanzu — Stack Position',
        'What manages Tanzu · Tanzu platform · What Tanzu manages',
        [
            col('Managed By', 'vSphere Client · TMC · kubectl', GREY,
                ['vSphere Client (Namespaces UI)', 'Tanzu Mission Control (TMC)',
                 'kubectl vsphere plugin', 'Aria Automation (IaC K8s)',
                 'REST API (Supervisor API)'],
                ['vSphere Client: namespace + quotas', 'TMC: multi-cluster governance',
                 'kubectl vsphere login + context', 'Aria Auto: Kubernetes IaC',
                 'Supervisor API: cluster lifecycle']),
            col('Tanzu Platform', 'Supervisor + TKG + runtime', BLUE,
                ['Supervisor (vSphere Kubernetes)', 'TKG Runtime (workload clusters)', 'NSX / vDS integration',
                 'Harbor Registry (per namespace)', 'Velero (backup controller)'],
                ['Supervisor: 3-node HA control plane', 'TKG: kubelet on worker VMs',
                 'NSX: per-namespace LB + segment', 'Harbor: OCI registry + replication',
                 'Velero: schedule + restore']),
            col('Manages', 'K8s Clusters · Pods · Storage', TEAL,
                ['TKG Workload Clusters', 'Pods + containers (workloads)', 'Kubernetes namespaces',
                 'PVCs → vSphere storage class', 'LoadBalancer services (NSX)'],
                ['Cluster: isolated K8s CP + workers', 'Pods: scheduled on worker VMs',
                 'Namespaces: resource quotas', 'PVC: vSAN / vVOL via CSI driver',
                 'LB: NSX or HA Proxy VIP']),
        ],
        'Tanzu Integration Points',
        ['Integration', 'Direction', 'Protocol', 'Purpose'],
        [('vCenter / vSphere', 'Supervisor on vCenter', 'vSphere API', 'VM provisioning for nodes'),
         ('NSX-T', 'CNI + LB integration', 'NSX API', 'Pod networking + LB services'),
         ('vSAN / vVOL', 'CSI driver', 'vSphere CSI', 'Persistent volume claims'),
         ('Harbor Registry', 'Pull images', 'OCI / HTTPS 443', 'Container image source'),
         ('Tanzu Mission Control', 'TMC → Supervisor API', 'HTTPS 443', 'Multi-cluster policy'),
         ('Aria Automation', 'Provision clusters', 'Kubernetes API', 'IaC K8s lifecycle')],
        'VMware Tanzu Reference · Supervisor · TKG · TMC · kubectl vsphere · NSX CNI · Harbor'
    )


# ── Target definitions ────────────────────────────────────────────────────────

TARGETS = [
    {
        'page': 'docs/virtualization/vmware/vcenter/index.md',
        'svgs': [
            ('vcenter-capabilities-overview.svg', 'vCenter Capabilities Overview', _vcenter_caps()),
            ('vcenter-stack-overview.svg', 'vCenter Stack Position', _vcenter_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/vsan/index.md',
        'svgs': [
            ('vsan-capabilities-overview.svg', 'vSAN Capabilities Overview', _vsan_caps()),
            ('vsan-stack-overview.svg', 'vSAN Stack Position', _vsan_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/nsx/index.md',
        'svgs': [
            ('nsx-capabilities-overview.svg', 'NSX Capabilities Overview', _nsx_caps()),
            ('nsx-stack-overview.svg', 'NSX Stack Position', _nsx_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/esxi/index.md',
        'svgs': [
            ('esxi-capabilities-overview.svg', 'ESXi Capabilities Overview', _esxi_caps()),
            ('esxi-stack-overview.svg', 'ESXi Stack Position', _esxi_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/vmware-cloud-foundation/index.md',
        'svgs': [
            ('vcf-capabilities-overview.svg', 'VCF Capabilities Overview', _vcf_caps()),
            ('vcf-stack-overview.svg', 'VCF Stack Position', _vcf_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/horizon/index.md',
        'svgs': [
            ('horizon-capabilities-overview.svg', 'Horizon Capabilities Overview', _horizon_caps()),
            ('horizon-stack-overview.svg', 'Horizon Stack Position', _horizon_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/srm/index.md',
        'svgs': [
            ('srm-capabilities-overview.svg', 'SRM Capabilities Overview', _srm_caps()),
            ('srm-stack-overview.svg', 'SRM Stack Position', _srm_stack()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/tanzu/index.md',
        'svgs': [
            ('tanzu-capabilities-overview.svg', 'Tanzu Capabilities Overview', _tanzu_caps()),
            ('tanzu-stack-overview.svg', 'Tanzu Stack Position', _tanzu_stack()),
        ],
    },
]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    do_generate = '--inject' not in sys.argv
    do_inject = '--generate' not in sys.argv
    dry_run = '--dry-run' in sys.argv

    if do_generate:
        print('Generating SVG files...')
        for target in TARGETS:
            for fname, alt, svg_content in target['svgs']:
                out = ASSETS / fname
                out.write_text(svg_content, encoding='utf-8')
                print(f'  Wrote {out}')
        print()

    if do_inject:
        print('Injecting SVG references into pages...')
        for target in TARGETS:
            page_abs = str(REPO / target['page'])
            insertions = [(alt, fname) for fname, alt, _ in target['svgs']]
            inject_svgs(page_abs, insertions, dry_run=dry_run)
        print()

    print('Done.')


if __name__ == '__main__':
    main()
