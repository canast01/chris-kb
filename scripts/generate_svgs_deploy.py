#!/usr/bin/env python3
"""
Generate SVG diagrams for VMware product deploy pages (product/deploy/index.md).
Each product gets TWO SVGs:
  1. *-deploy-stages.svg   — Prerequisites → Components Deployed → Verification
  2. *-deploy-topology.svg — Physical / Logical / Management layers

Usage:
  python3 scripts/generate_svgs_deploy.py            # generate + inject
  python3 scripts/generate_svgs_deploy.py --generate # SVG files only, skip inject
  python3 scripts/generate_svgs_deploy.py --inject   # inject only (SVGs must exist)
  python3 scripts/generate_svgs_deploy.py --dry-run  # preview inject without writing

NOTE on ASCII diagrams:
  This script REPLACES the ASCII diagram block on each page with SVG img tags.
  The ASCII source is preserved in scripts/diagrams/*.py and can be regenerated
  with `python3 scripts/ascii_diagram_gen.py --write-all`.
  After running, `--check` will show these pages as OUT OF SYNC until you comment
  out their @kb_diagram registrations in the relevant diagram script.
"""
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO / 'scripts'))
from svg_helpers import make_svg, inject_svgs  # noqa: E402

ASSETS = REPO / 'docs' / 'assets'

# ── Colour palettes (hdr, light, dark, mid) ───────────────────────────────────
BLUE   = ('#1565c0', '#e3f2fd', '#1565c0', '#90caf9')
PURPLE = ('#6a1b9a', '#f3e5f5', '#4a148c', '#ce93d8')
TEAL   = ('#00695c', '#e0f2f1', '#004d40', '#80cbc4')
GREY   = ('#37474f', '#eceff1', '#37474f', '#b0bec5')
ORANGE = ('#e65100', '#fbe9e7', '#bf360c', '#ffab91')
RED    = ('#b71c1c', '#ffebee', '#7f0000', '#ef9a9a')


def col(name, sub, palette, items, notes):
    hdr, light, dark, mid = palette
    return (name, sub, hdr, light, dark, mid, items, notes)


# ── SVG data: stages ──────────────────────────────────────────────────────────

def _vcenter_stages():
    return make_svg(
        'vCenter Deploy — Stage Overview',
        'Prerequisites · Components Deployed · Post-Deploy Verification',
        [
            col('Prerequisites', 'Before you begin', GREY,
                ['ESXi 7.0+ host (HCL-listed)', 'FQDN + forward/reverse DNS', 'NTP source reachable',
                 'Datastore ≥ 50 GB free', 'Management network segment'],
                ['ESXi: target host for VCSA OVA', 'DNS: VCSA FQDN must resolve',
                 'NTP: time sync required for SSO', 'Datastore: sizing by VCSA size',
                 'Network: VLAN + IP + gateway',
                 'Ports: 443, 5480, 7080 open']),
            col('Deployed Components', 'What gets installed', BLUE,
                ['VCSA OVA (Linux appliance)', 'Embedded PSC (vSphere 7.0+)', 'vPostgres (embedded DB)',
                 'SSO domain (vsphere.local)', 'VAMI service (port 5480)'],
                ['VCSA: deployed via ISO installer', 'PSC: embedded since vSphere 7', 'vPostgres: all inventory data',
                 'SSO: initial admin password set', 'VAMI: network + cert + backup config',
                 'VMCA: built-in cert authority']),
            col('Post-Deploy Verification', 'Confirm it worked', TEAL,
                ['FQDN resolves to VCSA IP', 'vSphere Client UI loads (:443)', 'VAMI UI loads (:5480)',
                 'First ESXi host added to inventory', 'HA cluster created + configured'],
                ['https://vcsa-fqdn: login with admin@vsphere.local', 'VAMI: verify NTP sync status',
                 'Add first ESXi host via UI', 'Create datacenter + cluster',
                 'Configure HA admission control',
                 'Set backup schedule in VAMI']),
        ],
        'VCSA Sizing Reference',
        ['Deployment Size', 'vCPU', 'RAM (GB)', 'Storage (GB)'],
        [('Tiny (≤10 hosts, ≤100 VMs)', '2', '12', '415'),
         ('Small (≤100 hosts, ≤1000 VMs)', '4', '19', '480'),
         ('Medium (≤400 hosts, ≤4000 VMs)', '8', '28', '700'),
         ('Large (≤1000 hosts, ≤10000 VMs)', '16', '37', '1065'),
         ('XL (≤2000 hosts, ≤35000 VMs)', '24', '56', '1805'),
         ('Note', 'Thin provision OK', 'Reservation required', 'NFS or VMFS')],
        'VMware vCenter Deploy Reference · VCSA OVA · PSC · SSO · VAMI · ESXi · DNS · NTP'
    )


def _vcenter_topology():
    return make_svg(
        'vCenter Deploy — Topology Overview',
        'Physical Infrastructure · VCSA Components · Management Access',
        [
            col('Physical Infrastructure', 'What you need before deploying', GREY,
                ['ESXi host (management cluster)', 'Shared datastore (NFS/VMFS)', 'Management VLAN + IP range',
                 'DNS server (forward + reverse)', 'NTP server (stratum 2 or better)'],
                ['ESXi host: staging host for VCSA', 'Datastore: VCSA thin-provisioned OVA',
                 'VLAN: isolated management segment', 'DNS: static A + PTR records',
                 'NTP: pool.ntp.org or internal PDC',
                 'Firewall: permit 443, 5480, 902']),
            col('VCSA Components', 'Inside the appliance', BLUE,
                ['vCenter Server service (vpxd)', 'Embedded PSC (sso-service)',
                 'vPostgres (database service)', 'VMCA (cert authority service)',
                 'rhttpproxy (reverse proxy :443)'],
                ['vpxd: core vCenter daemon', 'sso-service: token auth + SAML',
                 'vPostgres: inventory + events DB', 'VMCA: issue machine SSL certs',
                 'rhttpproxy: routes /ui, /api, /sdk',
                 'VAMI: lighttpd on port 5480']),
            col('Management Access', 'How admins reach vCenter', TEAL,
                ['vSphere Client (https://:443)', 'VAMI (https://:5480)', 'REST API (https://:443/api)',
                 'SSH (port 22, disabled default)', 'SDK / PowerCLI / Python'],
                ['vSphere Client: HTML5 admin UI', 'VAMI: appliance settings only',
                 'REST API: /api/vcenter namespace', 'SSH: enable only when needed',
                 'PowerCLI: Connect-VIServer cmdlet',
                 'MOB: disable in production']),
        ],
        'vCenter Network Port Reference',
        ['Port', 'Protocol', 'Direction', 'Purpose'],
        [('443', 'HTTPS', 'Client → VCSA', 'vSphere Client + API + SDK'),
         ('902', 'TCP', 'ESXi → VCSA / VCSA → ESXi', 'VPXA heartbeat + NFC'),
         ('5480', 'HTTPS', 'Admin → VCSA', 'VAMI appliance management'),
         ('7080', 'HTTP', 'Internal only', 'Reverse proxy health check'),
         ('2012', 'HTTPS', 'PSC→PSC / VCSA', 'CRL + STS internal (embedded)'),
         ('9090', 'HTTP', 'Internal only', 'VMware Analytics service')],
        'VMware vCenter Topology Reference · VCSA · PSC · VAMI · REST API · Ports · DNS'
    )


def _vsan_stages():
    return make_svg(
        'vSAN Deploy — Stage Overview',
        'Prerequisites · Components Deployed · Post-Deploy Verification',
        [
            col('Prerequisites', 'Before you begin', GREY,
                ['ESXi hosts on vSAN HCL (≥3)', 'vCenter managing the cluster', '10GbE NICs for vSAN traffic',
                 'Cache + capacity disks per host', 'vSAN license applied'],
                ['HCL: vmware.com/resources/compat', 'vCenter: cluster must exist first',
                 'NICs: dedicated vmknic recommended', 'Cache SSD: ≥ 10% of capacity tier',
                 'License: check via vCenter UI',
                 'MTU 9000 (jumbo frames) on vSAN VLAN']),
            col('Deployed Components', 'What gets enabled', BLUE,
                ['vSAN cluster enabled on cluster', 'Disk groups claimed (OSA)', 'vSAN VMkernel port (vmk)',
                 'Storage policies created (SPBM)', 'Witness VM (if stretched / 2-node)'],
                ['Enable: Cluster → Configure → vSAN', 'Disk groups: cache + capacity per host',
                 'vmknic: vSAN traffic type on 10GbE', 'SPBM: FTT=1 RAID-1 default policy',
                 'Witness: separate ESXi or cloud OVA',
                 'Health service: auto-enabled']),
            col('Post-Deploy Verification', 'Confirm it worked', TEAL,
                ['vSAN datastore visible in vCenter', 'Skyline Health all green', 'First VM deployed on vSAN policy',
                 'Network performance test (iPerf)', 'HCL validation passes'],
                ['Datastore: 1 per cluster, appears auto', 'Health: Monitor → vSAN → Skyline Health',
                 'VM: deploy on vSAN SPBM policy', 'iPerf: esxcli vsan network ipconfig test',
                 'HCL: Skyline → Hardware Compatibility',
                 'Space: ≥ 30% slack recommended']),
        ],
        'vSAN Minimum Host Count by FTT Policy',
        ['Policy', 'RAID Level', 'Min Hosts', 'Overhead'],
        [('FTT=1, RAID-1', 'Mirroring', '3 hosts', '2× space'),
         ('FTT=1, RAID-5', 'Erasure coding', '4 hosts', '1.33× space'),
         ('FTT=2, RAID-1', 'Mirroring', '5 hosts', '3× space'),
         ('FTT=2, RAID-6', 'Erasure coding', '6 hosts', '1.5× space'),
         ('FTT=3, RAID-1', 'Mirroring', '7 hosts', '4× space'),
         ('Stretched FTT=1', 'Site mirroring', '2+1 witness', '2× + witness')],
        'VMware vSAN Deploy Reference · HCL · Disk Groups · SPBM · Skyline Health · MTU'
    )


def _vsan_topology():
    return make_svg(
        'vSAN Deploy — Topology Overview',
        'Physical Layer · vSAN Logical Layer · Management Plane',
        [
            col('Physical Layer', 'Hosts · Disks · Network', GREY,
                ['ESXi hosts (≥3, HCL-listed)', 'NVMe/SSD cache per host', 'SSD/HDD capacity per host',
                 '10GbE dedicated vSAN NIC', 'TOR switch (MTU 9000, VLAN)'],
                ['Hosts: all in same vSAN cluster', 'Cache: ≥ 10% of capacity tier',
                 'OSA: cache disk group + capacity', 'ESA: single NVMe pool (no groups)',
                 '10GbE: dedicated vmknic for vSAN',
                 'Switch: jumbo frames + vSAN VLAN']),
            col('vSAN Logical Layer', 'Datastore · Objects · CLOM', BLUE,
                ['vSAN Datastore (cluster-wide)', 'Storage Objects (components)',
                 'CLOM (object placement engine)', 'DOM (data object manager)',
                 'Health Service (Skyline)'],
                ['Datastore: single namespace all VMs', 'Objects: VM disk = witness + replicas',
                 'CLOM: places components per policy', 'DOM: handles read/write to objects',
                 'Health: 170+ automated checks',
                 'Rebalance: triggered at >10% skew']),
            col('Management Plane', 'vCenter · Aria · CLI', TEAL,
                ['vCenter vSAN plugin (in VC)', 'Aria Operations adapter', 'esxcli vsan commands',
                 'PowerCLI (Get-VsanView)', 'vSAN Observer (on-demand trace)'],
                ['vCenter: health, disk mgmt, policies', 'Aria Ops: capacity + alerts',
                 'esxcli: low-level disk/net debug', 'PowerCLI: bulk policy operations',
                 'Observer: real-time perf trace',
                 'RVC: Ruby vSphere Console (older)']),
        ],
        'vSAN Network Requirements',
        ['Requirement', 'Minimum', 'Recommended', 'Notes'],
        [('NIC bandwidth', '1 GbE', '10 GbE', '25 GbE for ESA'),
         ('MTU', '1500', '9000 (jumbo frames)', 'Must match across switch'),
         ('Latency (RTT)', '< 1 ms', '< 0.5 ms', 'Critical for OSA/ESA'),
         ('VLAN isolation', 'Shared OK', 'Dedicated vSAN VLAN', 'QoS if shared'),
         ('vmknic', '1 per host', '2 for redundancy', 'Both on same VLAN'),
         ('Witness bandwidth', '100 Mbps', '1 Gbps', '2-node or stretched')],
        'VMware vSAN Topology Reference · Disk Groups · ESA · CLOM · Skyline · MTU · HCL'
    )


def _nsx_stages():
    return make_svg(
        'NSX Deploy — Stage Overview',
        'Prerequisites · Components Deployed · Post-Deploy Verification',
        [
            col('Prerequisites', 'Before you begin', GREY,
                ['vCenter 7.0+ managing ESXi hosts', 'DNS + NTP for NSX Manager FQDN', 'ESXi 7.0+ on HCL',
                 'Routable TEP IP range (overlay)', 'NSX license applied'],
                ['vCenter: NSX registers as plugin', 'DNS: NSX Manager FQDNs must resolve',
                 'ESXi: VIBs installed by NSX', 'TEP: /26 or larger per cluster',
                 'License: NSX-T 3.x or NSX 4.x',
                 'Ports: 443, UDP 6081 (TEP) open']),
            col('Deployed Components', 'What gets installed', BLUE,
                ['NSX Manager cluster (3 nodes)', 'Transport Nodes (ESXi + Edge)', 'TEP vmknic (per ESXi host)',
                 'Tier-0 Gateway (N-S routing)', 'Tier-1 Gateway (E-W per tenant)'],
                ['Manager cluster: 3 VMs active/active', 'Transport nodes: VIBs + TEP IP',
                 'TEP vmknic: Geneve UDP 6081', 'T0: uplink to physical router BGP',
                 'T1: connects to overlay segments',
                 'Segments: overlay L2 per workload']),
            col('Post-Deploy Verification', 'Confirm it worked', TEAL,
                ['NSX Manager cluster status UP', 'Transport nodes status UP', 'BGP sessions established',
                 'DFW active on transport nodes', 'First overlay segment reachable'],
                ['Manager cluster: System → Appliances', 'Transport nodes: Fabric → Nodes',
                 'BGP: Networking → T0 → BGP sessions', 'DFW: Security → Distributed Firewall',
                 'Segment: ping across overlay VMs',
                 'Traceflow: verify packet path']),
        ],
        'NSX Manager Appliance Sizing',
        ['Size', 'vCPU', 'RAM (GB)', 'Max Hosts'],
        [('Small', '4', '16', '64 hosts'),
         ('Medium', '6', '24', '256 hosts'),
         ('Large', '12', '48', '1024 hosts'),
         ('NSX Edge (Small)', '2', '4', '100 VMs throughput'),
         ('NSX Edge (Medium)', '4', '8', '1 Gbps throughput'),
         ('NSX Edge (Large)', '8', '32', '10 Gbps throughput')],
        'VMware NSX Deploy Reference · Manager Cluster · Transport Nodes · TEP · T0/T1 · BGP'
    )


def _nsx_topology():
    return make_svg(
        'NSX Deploy — Topology Overview',
        'Physical Infrastructure · NSX Logical Layer · Management Plane',
        [
            col('Physical Infrastructure', 'Hosts · NICs · Switches', GREY,
                ['ESXi transport node hosts', 'NSX Edge VMs (T0 / T1 gateway)', '10GbE NICs for TEP traffic',
                 'Physical ToR switches (BGP)', 'Uplink network (routed segment)'],
                ['Transport hosts: VIBs + TEP vmknic', 'Edge VMs: bare-metal or vSphere',
                 '10GbE: TEP Geneve UDP 6081', 'ToR: BGP peer with T0 gateway',
                 'Uplink: VLAN to physical router',
                 'Rack ToR: ECMP to 2+ T0 uplinks']),
            col('NSX Logical Layer', 'Overlay · Gateways · DFW', BLUE,
                ['Overlay Segments (per workload)', 'Tier-0 Gateway (N-S; BGP)', 'Tier-1 Gateway (E-W per tenant)',
                 'DFW (on each transport node)', 'TEP network (Geneve tunnels)'],
                ['Segments: Geneve-encapsulated L2', 'T0: connects to physical via BGP',
                 'T1: service router + SR for NAT/LB', 'DFW: stateful kernel firewall',
                 'TEP: /26 per AZ minimum',
                 'BFD: fast link detection on T0']),
            col('Management Plane', 'Manager · Policy API · Aria', TEAL,
                ['NSX Manager cluster (3 VMs)', 'Policy API (HTTPS 443)', 'NSX Intelligence (flow viz)',
                 'Aria Operations for Networks', 'vCenter plugin (network topology)'],
                ['Manager: /nsx UI + REST API', 'Policy: intent-based declarative', 'Intelligence: IPFIX flows',
                 'Aria Net: topology + latency', 'vCenter plugin: net topology overlay',
                 'nsxcli: on manager + edge CLI']),
        ],
        'NSX Network Port Reference',
        ['Port', 'Protocol', 'Direction', 'Purpose'],
        [('443', 'HTTPS', 'Admin → NSX Manager', 'UI + REST Policy API'),
         ('6081', 'UDP (Geneve)', 'Host ↔ Host', 'Overlay TEP tunnels'),
         ('179', 'TCP (BGP)', 'T0 Edge ↔ ToR', 'BGP route advertisement'),
         ('4789', 'UDP (VXLAN)', 'Legacy only', 'Older NSX-v deployments'),
         ('9042', 'TCP', 'NSX Manager ↔ Agent', 'MPA (management plane agent)'),
         ('5671', 'AMQP', 'Manager ↔ Transport', 'Message bus (RabbitMQ)')],
        'VMware NSX Topology Reference · Overlay · TEP · T0/T1 · DFW · BGP · Manager Cluster'
    )


def _esxi_stages():
    return make_svg(
        'ESXi Deploy — Stage Overview',
        'Prerequisites · Components Deployed · Post-Deploy Verification',
        [
            col('Prerequisites', 'Before you begin', GREY,
                ['HCL-listed server hardware', 'BIOS: VT-x/VT-d enabled', 'iDRAC / iLO configured',
                 'Network cabling complete', 'ESXi ISO + deployment plan'],
                ['HCL: vmware.com/resources/compat', 'BIOS: enable virtualisation + IOMMU',
                 'iDRAC/iLO: virtual KVM for install', 'NICs: mgmt + vSAN + vMotion cabled',
                 'Boot: USB/SD or local SSD',
                 'IP plan: vmk0 + vMotion + vSAN']),
            col('Deployed Components', 'What gets installed', BLUE,
                ['ESXi 8.x (bare-metal hypervisor)', 'vmk0 (management vmknic)', 'Standard vSwitch (vSwitch0)',
                 'NTP + DNS + syslog configured', 'Host added to vCenter cluster'],
                ['ESXi: boot from USB, SD, or local', 'vmk0: management IP via DCUI',
                 'vSwitch0: default uplink ports', 'NTP: esxcli system ntp set', 'DNS: FQDN + search domain',
                 'vCenter: add host → cluster']),
            col('Post-Deploy Verification', 'Confirm it worked', TEAL,
                ['Host connected in vCenter UI', 'NTP sync status green', 'vSAN vmknic active (if HCI)',
                 'dvSwitch uplinks active', 'First test VM powers on'],
                ['vCenter: host status "Connected"', 'Monitor → Hardware → Sensors: all green',
                 'NTP: esxcli system time get', 'dvSwitch: migrate vmk0 from vSwitch',
                 'VM: power on + ping network gateway',
                 'Storage: see expected datastores']),
        ],
        'ESXi Minimum Hardware Requirements',
        ['Component', 'Minimum', 'Recommended', 'Notes'],
        [('CPU', '2-core x86-64 (2018+)', '2 socket × 20 core', 'VT-x + VT-d required'),
         ('RAM', '8 GB', '256 GB+', 'More = more VMs per host'),
         ('Boot device', '8 GB (USB/SD)', '32 GB SSD local', 'SSD strongly preferred'),
         ('NIC', '1 × 1 GbE', '2+ × 10 GbE', 'Redundancy + vSAN'),
         ('Storage', 'Any HCL SAN/NAS', 'NVMe SSD local + vSAN', 'See HCL for RAID cards'),
         ('BIOS', 'VT-x enabled', 'VT-d + IOMMU enabled', 'Required for NPIV, SR-IOV')],
        'VMware ESXi Deploy Reference · HCL · DCUI · vmk0 · vSwitch · NTP · vCenter · iDRAC'
    )


def _esxi_topology():
    return make_svg(
        'ESXi Deploy — Topology Overview',
        'Physical Hardware · ESXi Software Layer · Management Access',
        [
            col('Physical Hardware', 'Server · NICs · Storage', GREY,
                ['Server (HCL-listed x86-64)', 'iDRAC / iLO (BMC out-of-band)', '2+ NICs (10 GbE min)',
                 'Boot device (SSD/USB/SD)', 'Local or SAN storage'],
                ['Server: HCL validates driver compat', 'iDRAC/iLO: out-of-band power + KVM',
                 'NIC 1: management + VM traffic', 'NIC 2: vMotion + vSAN traffic',
                 'Boot: persistent SSD recommended',
                 'SAN: FC/iSCSI HBA if needed']),
            col('ESXi Software Layer', 'VMkernel + agents + datastores', BLUE,
                ['ESXi VMkernel (type-1 hypervisor)', 'vmk0 (management IP)', 'vSwitch0 (default switch)',
                 'VPXA (vCenter agent)', 'VMFS / NFS / vSAN datastores'],
                ['VMkernel: no general-purpose OS', 'vmk0: primary IP, port 443 + 902',
                 'vSwitch0: vmnic0 uplink by default', 'VPXA: heartbeat to vCenter every 5 s',
                 'VMFS: auto-created on local disk',
                 'VIBs: NSX + vSAN install here']),
            col('Management Access', 'Inbound management paths', TEAL,
                ['vCenter (via VPXA agent)', 'DCUI (Direct Console UI)', 'SSH (port 22, optional)',
                 'esxcli (local or remote)', 'iDRAC / iLO (hardware level)'],
                ['vCenter: primary admin path', 'DCUI: emergency network + password reset',
                 'SSH: enable only when needed', 'esxcli: scripting + diagnostics',
                 'iDRAC: power cycle, BIOS, KVM',
                 'Syslog: forward to log aggregator']),
        ],
        'ESXi Management Port Reference',
        ['Port', 'Protocol', 'Direction', 'Purpose'],
        [('22', 'SSH', 'Admin → ESXi', 'SSH shell (disabled by default)'),
         ('80', 'HTTP', 'Any → ESXi', 'Redirect to 443'),
         ('443', 'HTTPS', 'vCenter + admin', 'SOAP API + REST + vSphere UI'),
         ('902', 'TCP', 'vCenter ↔ ESXi', 'VPXA heartbeat + NFC'),
         ('8300', 'HTTPS', 'ESXi → vCenter', 'vSAN health reporting'),
         ('9000-9100', 'TCP', 'Internal', 'ESXi service discovery')],
        'VMware ESXi Topology Reference · VMkernel · VPXA · DCUI · SSH · VMFS · NFS · iDRAC'
    )


def _vcf_stages():
    return make_svg(
        'VCF Deploy — Stage Overview',
        'Prerequisites · Components Deployed · Post-Deploy Verification',
        [
            col('Prerequisites', 'Before you begin', GREY,
                ['4+ HCL servers (management domain)', 'Cloud Builder VM deployed + powered on', 'JSON deployment spec prepared',
                 'DNS + NTP + routing in place', 'VCF license keys ready'],
                ['HCL: ≥4 servers for mgmt domain vSAN', 'Cloud Builder: OVA on any ESXi host',
                 'JSON spec: network/password/component', 'DNS: all VCF FQDNs pre-registered',
                 'NTP: stratum 2 for all components',
                 'Licenses: vSphere + vSAN + NSX + VCF']),
            col('Deployed Components', 'What Cloud Builder provisions', BLUE,
                ['SDDC Manager VM (orchestrator)', 'NSX Management Cluster (3 VMs)', 'vCenter Server (management)',
                 'vSAN Datastore (management hosts)', 'Aria Suite Lifecycle (optional)'],
                ['Cloud Builder: stages all components', 'SDDC Mgr: portal + lifecycle engine',
                 'NSX Mgmt: overlay for mgmt VMs', 'vCenter: manages mgmt domain hosts',
                 'vSAN: management host local disks',
                 'Bring-up: typically 3–4 hours']),
            col('Post-Deploy Verification', 'Confirm it worked', TEAL,
                ['SDDC Manager UI accessible', 'Management domain health green', 'NSX Manager cluster UP',
                 'vCenter managing all mgmt hosts', 'Ready to create workload domain'],
                ['SDDC Mgr: https://sddc-mgr-fqdn', 'Health: Dashboard → Management Domain',
                 'NSX cluster: System → Appliances', 'vCenter: all 4 hosts connected',
                 'WD: Commission hosts → Create WD',
                 'Cloud Builder: power off / retire']),
        ],
        'VCF Management Domain Minimum BOM',
        ['Component', 'Min Count', 'Min Spec', 'Notes'],
        [('Management hosts', '4 (vSAN FTT=1)', '2-socket, 512 GB RAM', 'All on HCL'),
         ('NICs per host', '2 × 25 GbE', '4 ports total', '2 for vSAN, 2 for overlay'),
         ('vSAN disks', '1 NVMe cache + 2 capacity', 'Per host', 'HCL SSD required'),
         ('SDDC Manager VM', '1', '4 vCPU / 16 GB RAM', 'Deployed by Cloud Builder'),
         ('NSX Manager VMs', '3 (cluster)', '6 vCPU / 24 GB each', 'Medium sizing'),
         ('vCenter VCSA', '1', '8 vCPU / 28 GB RAM', 'Medium sizing on mgmt hosts')],
        'VMware VCF Deploy Reference · Cloud Builder · SDDC Manager · JSON Spec · BOM · Bring-up'
    )


def _vcf_topology():
    return make_svg(
        'VCF Deploy — Topology Overview',
        'Physical Infrastructure · Management Domain Stack · Day-2 Services',
        [
            col('Physical Infrastructure', '4+ servers + switches', GREY,
                ['4 management hosts (HCL)', 'Top-of-rack switches (25 GbE+)', 'Out-of-band (iDRAC/iLO)',
                 'External DNS + NTP servers', 'Cloud Builder VM (temp)'],
                ['4 hosts: mgmt vSAN FTT=1 cluster', '25 GbE: vSAN + overlay NICs',
                 'iDRAC/iLO: boot + install access', 'DNS: pre-register all FQDNs',
                 'NTP: all components sync here',
                 'Cloud Builder: OVA on any ESXi']),
            col('Management Domain Stack', 'All VMs live on these 4 hosts', BLUE,
                ['SDDC Manager (control tower)', 'NSX Manager cluster (3 VMs)', 'vCenter Server (mgmt)',
                 'vSAN datastore (mgmt hosts)', 'NSX Edge (mgmt N-S routing)'],
                ['SDDC Mgr: VCF API + lifecycle', 'NSX Mgmt: overlay for mgmt VMs',
                 'vCenter: manages the 4 hosts', 'vSAN: management VM storage',
                 'NSX Edge: outbound for mgmt VMs',
                 'All IPs from JSON spec']),
            col('Day-2 Services', 'After bring-up completes', TEAL,
                ['Commission workload hosts', 'Create Workload Domains', 'Deploy Aria Suite Lifecycle',
                 'Connect Aria Ops / Aria Auto', 'Run LCM (patch all components)'],
                ['Workload hosts: rack + commission', 'WD: vCenter + NSX + vSAN per team',
                 'Aria SLC: manages Aria products', 'Aria Ops: monitoring adapter',
                 'Aria Auto: IaC integrations',
                 'LCM: upgrade via SDDC Mgr UI']),
        ],
        'VCF Network Segment Requirements',
        ['Segment', 'VLAN', 'Purpose', 'Sizing'],
        [('Management', 'Dedicated', 'SDDC Mgr, vCenter, NSX Mgr', '/24 minimum'),
         ('vMotion', 'Dedicated', 'VM live migration', '/24 minimum'),
         ('vSAN', 'Dedicated', 'vSAN storage traffic', '/24, MTU 9000'),
         ('TEP (overlay)', 'Dedicated', 'NSX Geneve tunnels', '/26 per AZ'),
         ('Uplink (N-S)', 'Routed', 'NSX T0 to physical router', 'BGP peer IPs'),
         ('Workload (VMs)', 'Per-WD', 'VM overlay segments', 'Per workload domain')],
        'VMware VCF Topology Reference · Cloud Builder · SDDC Manager · NSX · vSAN · BOM'
    )


# ── Target definitions ────────────────────────────────────────────────────────

TARGETS = [
    {
        'page': 'docs/virtualization/vmware/vcenter/deploy/index.md',
        'svgs': [
            ('vcenter-deploy-stages.svg', 'vCenter Deploy Stages', _vcenter_stages()),
            ('vcenter-deploy-topology.svg', 'vCenter Deploy Topology', _vcenter_topology()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/vsan/deploy/index.md',
        'svgs': [
            ('vsan-deploy-stages.svg', 'vSAN Deploy Stages', _vsan_stages()),
            ('vsan-deploy-topology.svg', 'vSAN Deploy Topology', _vsan_topology()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/nsx/deploy/index.md',
        'svgs': [
            ('nsx-deploy-stages.svg', 'NSX Deploy Stages', _nsx_stages()),
            ('nsx-deploy-topology.svg', 'NSX Deploy Topology', _nsx_topology()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/esxi/deploy/index.md',
        'svgs': [
            ('esxi-deploy-stages.svg', 'ESXi Deploy Stages', _esxi_stages()),
            ('esxi-deploy-topology.svg', 'ESXi Deploy Topology', _esxi_topology()),
        ],
    },
    {
        'page': 'docs/virtualization/vmware/vmware-cloud-foundation/deploy/index.md',
        'svgs': [
            ('vcf-deploy-stages.svg', 'VCF Deploy Stages', _vcf_stages()),
            ('vcf-deploy-topology.svg', 'VCF Deploy Topology', _vcf_topology()),
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
