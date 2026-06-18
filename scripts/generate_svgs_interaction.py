#!/usr/bin/env python3
"""
Generate SVGs for /reference/interaction-map/ pages.

Produces:
  docs/assets/interaction-map-master.svg         — all 15 products, 5 domains
  docs/assets/interaction-map-compute.svg        — ESXi, vCenter, PowerCLI
  docs/assets/interaction-map-network.svg        — NSX, vSphere Networking
  docs/assets/interaction-map-storage.svg        — vSAN, vSphere Replication, VxRail
  docs/assets/interaction-map-management.svg     — vCenter, VCF, Aria Suite Lifecycle
  docs/assets/interaction-map-automation.svg     — Aria products, Tanzu, Horizon

Usage:
    python3 scripts/generate_svgs_interaction.py           # write SVGs (default)
    python3 scripts/generate_svgs_interaction.py --dry-run # validate only
"""

import os, sys, xml.etree.ElementTree as ET
from pathlib import Path

REPO   = Path(__file__).resolve().parent.parent
ASSETS = REPO / 'docs' / 'assets'
DRY    = '--dry-run' in sys.argv

def xe(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def validate(svg_text, name):
    try:
        ET.fromstring(svg_text)
    except ET.ParseError as e:
        print(f'  INVALID XML in {name}: {e}')
        sys.exit(1)

def write_svg(filename, svg_text):
    validate(svg_text, filename)
    if DRY:
        print(f'  DRY  {filename}')
        return
    (ASSETS / filename).write_text(svg_text, encoding='utf-8')
    print(f'  OK   {filename}')


# ── Shared constants ──────────────────────────────────────────────────────────
W = 820

DOMAIN_COLORS = {
    'compute':    {'hdr': '#1565c0', 'light': '#e3f2fd', 'mid': '#1565c0'},
    'network':    {'hdr': '#2e7d32', 'light': '#e8f5e9', 'mid': '#2e7d32'},
    'storage':    {'hdr': '#6a1b9a', 'light': '#f3e5f5', 'mid': '#6a1b9a'},
    'management': {'hdr': '#e65100', 'light': '#fff3e0', 'mid': '#e65100'},
    'automation': {'hdr': '#c62828', 'light': '#ffebee', 'mid': '#c62828'},
}


# ── Master SVG — all 15 products in 5 domain bands ───────────────────────────

def make_master():
    H = 760
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'font-family="\'Segoe UI\',Arial,sans-serif">',
        f'  <rect width="{W}" height="{H}" fill="#f4f6f9"/>',
        # Header
        f'  <rect x="0" y="0" width="{W}" height="58" fill="#1a2744"/>',
        f'  <text x="410" y="36" text-anchor="middle" fill="white" '
        f'font-size="20" font-weight="700">VMware Product Interaction Map</text>',
        f'  <text x="410" y="52" text-anchor="middle" fill="#7a8fbb" '
        f'font-size="11">15 products · 5 domains · key integration protocols</text>',
    ]

    DOMAINS = [
        ('Management', 'management', '#e65100', '#fff3e0',
         ['VCF / SDDC Manager', 'Aria Suite Lifecycle'],
         ['Lifecycle management for all layers', 'Deploy: vCenter, NSX, vSAN, Aria Suite',
          'API: REST (sddc-mgr/v1), SDDC API']),
        ('Compute', 'compute', '#1565c0', '#e3f2fd',
         ['ESXi', 'vCenter Server', 'PowerCLI'],
         ['ESXi: hypervisor layer for all workloads', 'vCenter: vSphere API (SOAP/REST/govmomi)',
          'PowerCLI: PowerShell SDK over vSphere API']),
        ('Storage', 'storage', '#6a1b9a', '#f3e5f5',
         ['vSAN', 'vSphere Replication', 'VxRail'],
         ['vSAN: NVMe/SAS disks via VSAN kernel module', 'Replication: TCP/1500 VMRS to remote site',
          'VxRail: managed by VCF; includes vSAN + vCenter']),
        ('Network', 'network', '#2e7d32', '#e8f5e9',
         ['NSX Manager', 'NSX Edge', 'vSphere Networking (vDS)'],
         ['NSX: GENEVE overlay on VTEP VMkernel ports', 'Edge: BGP/ECMP to physical ToR switches',
          'vDS: VLAN-backed uplinks; VDS CDP/LLDP']),
        ('Automation', 'automation', '#c62828', '#ffebee',
         ['Aria Automation', 'Aria Operations', 'Aria Logs',
          'Aria Networks', 'Tanzu', 'Horizon'],
         ['Aria Automation: vRA REST API; IaaS API', 'Aria Ops: suite-api; collector adapters',
          'Tanzu: Kubernetes API; kubectl vsphere']),
    ]

    band_h = 110
    y0 = 68
    for i, (dname, dkey, hdr, light, products, notes) in enumerate(DOMAINS):
        y = y0 + i * (band_h + 6)
        # Band background
        lines.append(f'  <rect x="10" y="{y}" width="{W - 20}" height="{band_h}" '
                     f'fill="{light}" rx="6" stroke="{hdr}" stroke-width="1.5"/>')
        # Domain label left strip
        lines.append(f'  <rect x="10" y="{y}" width="100" height="{band_h}" '
                     f'fill="{hdr}" rx="6"/>')
        lines.append(f'  <rect x="76" y="{y}" width="34" height="{band_h}" fill="{hdr}"/>')
        mid_y = y + band_h // 2
        # Domain name (rotated via vertical centering)
        lines.append(f'  <text x="55" y="{mid_y - 6}" text-anchor="middle" fill="white" '
                     f'font-size="11" font-weight="700">{xe(dname)}</text>')
        lines.append(f'  <text x="55" y="{mid_y + 8}" text-anchor="middle" fill="rgba(255,255,255,0.7)" '
                     f'font-size="9">{xe(dkey)}</text>')

        # Product boxes
        px_start = 118
        box_w = min(130, (W - px_start - 20) // len(products) - 6)
        for j, prod in enumerate(products):
            px = px_start + j * (box_w + 6)
            py = y + 10
            lines.append(f'  <rect x="{px}" y="{py}" width="{box_w}" height="30" '
                         f'fill="white" rx="4" stroke="{hdr}" stroke-width="1.2"/>')
            lines.append(f'  <text x="{px + box_w // 2}" y="{py + 20}" text-anchor="middle" '
                         f'fill="{hdr}" font-size="9" font-weight="700">{xe(prod)}</text>')

        # Notes
        for k, note in enumerate(notes[:3]):
            ny = y + 52 + k * 16
            lines.append(f'  <text x="118" y="{ny}" fill="#546e7a" '
                         f'font-size="8">&#x25B8; {xe(note)}</text>')

    # Connector arrows between bands (right side)
    arrow_x = W - 30
    arrow_color = '#90a4ae'
    for i in range(len(DOMAINS) - 1):
        ay = y0 + i * (band_h + 6) + band_h
        ay2 = ay + 6
        mid_ay = (ay + ay2) // 2
        lines.append(f'  <line x1="{arrow_x}" y1="{ay}" x2="{arrow_x}" y2="{ay2}" '
                     f'stroke="{arrow_color}" stroke-width="2" '
                     f'marker-end="url(#arr)"/>')

    # Arrow marker def
    lines.insert(1,
        '  <defs><marker id="arr" markerWidth="6" markerHeight="6" '
        'refX="3" refY="3" orient="auto">'
        '<path d="M0,0 L6,3 L0,6 Z" fill="#90a4ae"/>'
        '</marker></defs>')

    # Footer
    footer_y = H - 30
    lines.append(f'  <rect x="0" y="{footer_y}" width="{W}" height="30" fill="#1a2744"/>')
    lines.append(f'  <text x="410" y="{footer_y + 19}" text-anchor="middle" '
                 f'fill="#7a8fbb" font-size="9">'
                 f'VCF manages all layers · NSX/vSAN embedded in ESXi kernel · Aria Suite deployed by LCM'
                 f'</text>')
    lines.append('</svg>')
    return '\n'.join(lines)


# ── Domain SVGs — detailed 3-column view per domain ──────────────────────────

def make_domain_svg(title, subtitle,
                    col1_name, col1_products, col1_apis, col1_notes,
                    col2_name, col2_products, col2_apis, col2_notes,
                    col3_name, col3_products, col3_apis, col3_notes,
                    table_title, table_rows, footer_text):
    """Build a domain interaction SVG using the existing 3-column pattern."""
    H = 750
    C = [
        (20,  col1_name, col1_products, col1_apis, col1_notes, DOMAIN_COLORS),
        (285, col2_name, col2_products, col2_apis, col2_notes, DOMAIN_COLORS),
        (550, col3_name, col3_products, col3_apis, col3_notes, DOMAIN_COLORS),
    ]
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'font-family="\'Segoe UI\',Arial,sans-serif">',
        f'  <rect width="{W}" height="{H}" fill="#f4f6f9"/>',
        f'  <rect x="0" y="0" width="{W}" height="58" fill="#1a2744"/>',
        f'  <text x="410" y="36" text-anchor="middle" fill="white" '
        f'font-size="20" font-weight="700">{xe(title)}</text>',
        f'  <text x="410" y="52" text-anchor="middle" fill="#7a8fbb" '
        f'font-size="11">{xe(subtitle)}</text>',
    ]

    COL_Y, COL_H = 72, 390
    ITEM_YS = [126, 152, 178, 204, 230]
    NOTE_YS = [282, 300, 318, 336, 354, 372, 390, 408]
    CW = 250

    for cx, cname, products, apis, notes, _ in C:
        mx = cx + CW // 2
        # Alternate column colors by position
        idx = [20, 285, 550].index(cx)
        domain_keys = ['management', 'compute', 'storage', 'network', 'automation']
        dk = domain_keys[idx % len(domain_keys)]
        dc = DOMAIN_COLORS[dk]
        hdr, light, mid = dc['hdr'], dc['light'], dc['mid']

        lines += [
            f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="{COL_H}" '
            f'fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
            f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="42" fill="{hdr}" rx="6"/>',
            f'  <rect x="{cx}" y="{COL_Y + 28}" width="{CW}" height="14" fill="{hdr}"/>',
            f'  <text x="{mx}" y="{COL_Y + 25}" text-anchor="middle" fill="white" '
            f'font-size="13" font-weight="700">{xe(cname)}</text>',
        ]
        # Products as items
        all_items = products[:5]
        for y, item in zip(ITEM_YS, all_items):
            lines += [
                f'  <rect x="{cx + 10}" y="{y}" width="{CW - 20}" height="22" '
                f'fill="{light}" rx="3" stroke="{mid}" stroke-width="1"/>',
                f'  <text x="{mx}" y="{y + 15}" text-anchor="middle" fill="{mid}" '
                f'font-size="9" font-weight="700">{xe(item)}</text>',
            ]
        # Notes (apis + notes combined)
        all_notes = (apis + notes)[:8]
        for y, note in zip(NOTE_YS, all_notes):
            lines.append(
                f'  <text x="{mx}" y="{y}" text-anchor="middle" '
                f'fill="#78909c" font-size="9">{xe(note)}</text>'
            )

    # Table
    TABLE_Y, TABLE_H = 480, 222
    TW, TX = 780, 20
    HDR_XS = [120, 320, 520, 700]
    lines += [
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="{TABLE_H}" '
        f'fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="36" fill="#1a2744" rx="6"/>',
        f'  <rect x="{TX}" y="{TABLE_Y + 24}" width="{TW}" height="12" fill="#1a2744"/>',
        f'  <text x="410" y="{TABLE_Y + 24}" text-anchor="middle" fill="white" '
        f'font-size="13" font-weight="700">{xe(table_title)}</text>',
        f'  <rect x="{TX}" y="{TABLE_Y + 36}" width="{TW}" height="28" fill="#eceff1"/>',
    ]
    for x, h in zip(HDR_XS, ['Integration', 'Protocol / API', 'Direction', 'Notes']):
        lines.append(
            f'  <text x="{x}" y="{TABLE_Y + 55}" text-anchor="middle" '
            f'fill="#37474f" font-size="10" font-weight="700">{xe(h)}</text>'
        )
    for dx in [220, 415, 610]:
        lines.append(
            f'  <line x1="{TX + dx}" y1="{TABLE_Y + 36}" '
            f'x2="{TX + dx}" y2="{TABLE_Y + TABLE_H}" stroke="#dde2ec" stroke-width="1"/>'
        )
    for i, row in enumerate(table_rows[:6]):
        padded = list(row) + ['', '', '', '']
        label, c1, c2, c3 = padded[:4]
        ry = TABLE_Y + 64 + i * 26
        if i % 2 == 0:
            lines.append(
                f'  <rect x="{TX}" y="{ry - 14}" width="{TW}" height="26" fill="#f7f9fb"/>'
            )
        lines += [
            f'  <text x="120" y="{ry}" text-anchor="middle" fill="#455a64" font-size="9">{xe(label)}</text>',
            f'  <text x="320" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{xe(c1)}</text>',
            f'  <text x="520" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{xe(c2)}</text>',
            f'  <text x="700" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{xe(c3)}</text>',
        ]
    lines.append(
        f'  <line x1="{TX}" y1="{TABLE_Y + TABLE_H}" '
        f'x2="{TX + TW}" y2="{TABLE_Y + TABLE_H}" stroke="#dde2ec" stroke-width="1"/>'
    )

    # Footer
    footer_y = H - 30
    lines += [
        f'  <rect x="0" y="{footer_y}" width="{W}" height="30" fill="#1a2744"/>',
        f'  <text x="410" y="{footer_y + 19}" text-anchor="middle" '
        f'fill="#7a8fbb" font-size="9">{xe(footer_text)}</text>',
        '</svg>',
    ]
    return '\n'.join(lines)


# ── Domain definitions ────────────────────────────────────────────────────────

def make_compute():
    return make_domain_svg(
        'Compute Domain — Interaction Map',
        'ESXi · vCenter · PowerCLI · key integration protocols',
        'ESXi', ['ESXi Hypervisor', 'VMFS/NFS Datastores', 'VMkernel Adapters', 'TEP (GENEVE)'],
        ['Hosts vSAN storage kernel module', 'Hosts NSX VIBs for overlay networking'],
        ['API: esxcli (local / remote)', 'vSphere Host Agent (hostd) on :443',
         'DCUI console + SSH shell access'],
        'vCenter Server', ['vCenter (VCSA)', 'vSphere Cluster', 'DRS / HA / FT', 'Content Library'],
        ['Manages ESXi via vSphere API (govmomi)', 'Exposes REST API (/api) + SOAP (sdk)'],
        ['Tags/categories for VM inventory', 'Storage Policy Based Management (SPBM)',
         'vCenter SSO: SAML token auth'],
        'PowerCLI / govc', ['PowerCLI Module', 'govc (govmomi CLI)', 'vSphere REST Client'],
        ['Connects to vCenter :443 (govmomi)', 'Authenticates via vCenter SSO session'],
        ['Get-VM, Get-VMHost, Get-Cluster', 'govc vm.info, govc ls',
         'Set-PowerCLIConfiguration for TLS'],
        'Key Compute Integrations',
        [
            ('ESXi → vCenter',    'vSphere API / SOAP',     'ESXi reports to vCenter',  'hostd on ESXi, vpxd on vCenter'),
            ('vCenter → vSAN',    'SPBM / kernel module',   'vCenter assigns policies',  'vSAN kernel runs inside ESXi'),
            ('vCenter → NSX',     'NSX Manager REST',        'vCenter triggers DFW sync', 'NSX plugin in vCenter UI'),
            ('PowerCLI → vCenter','govmomi / PowerShell SDK','Read/write vSphere objects','Connect-VIServer :443'),
            ('VCF → vCenter',     'SDDC Manager API',        'VCF deploys + manages',     'vcf/v1/domains API'),
            ('Tanzu → vCenter',   'vSphere API / WCP',       'Supervisor cluster via WCP', 'kubectl vsphere login'),
        ],
        'ESXi hosts all workloads · vCenter provides API control plane · VCF manages lifecycle'
    )


def make_network():
    return make_domain_svg(
        'Network Domain — Interaction Map',
        'NSX · vSphere Networking (vDS) · BGP/GENEVE · key protocols',
        'NSX Manager', ['NSX Manager Cluster', 'NSX Controller Plane', 'Policy API', 'MP API (legacy)'],
        ['REST API: /policy/api/v1 (preferred)', 'Transport zones: overlay + VLAN types'],
        ['nsxcli on Edge: get routes, get bgp', 'GENEVE encap on ESXi VTEP VMkernel',
         'Edge VM: T0/T1 gateway, NAT, LB, VPN'],
        'NSX Edge', ['Edge Node (VM)', 'T0 Gateway (BGP)', 'T1 Gateway (tenant)', 'Edge Cluster'],
        ['BGP to physical ToR on uplink VLANs', 'BFD for fast failover detection'],
        ['ECMP: 4-8 paths from T0 to ToR', 'VRF-Lite for tenant separation',
         'NAT44/NAT64 on T0/T1 boundary'],
        'vSphere Networking', ['vDistributed Switch (vDS)', 'Port Groups (VLAN)', 'VMkernel Adapters', 'NIOC'],
        ['vDS: managed by vCenter (dvs API)', 'LACP / active-active uplink teaming'],
        ['TEP VMkernel: GENEVE overlay src IP', 'Storage VMkernel: iSCSI / NFS traffic',
         'Management VMkernel: ESXi mgmt + vMotion'],
        'Key Network Integrations',
        [
            ('NSX → ESXi',            'GENEVE / VIBs',       'NSX VIB installs on ESXi',  'TEP on VMkernel adapter'),
            ('NSX → vCenter',         'NSX plugin / REST',   'vCenter UI shows NSX objects','NSX Manager registers with vCenter'),
            ('T0 → Physical ToR',     'BGP / BFD',           'ECMP routing uplink',        'VLAN-backed uplink port group'),
            ('NSX → Aria Networks',   'Flow telemetry / API','vRNI reads IPFIX + API',     'Aria Networks data source: NSX'),
            ('vDS → ESXi',            'vSphere API (dvs)',   'vCenter pushes vDS config',  'vDS lives in vCenter; agents on ESXi'),
            ('NSX DFW → VMs',         'Kernel-level filter', 'Stateful east-west firewall','No extra hop; rules on ESXi host'),
        ],
        'NSX runs inside ESXi kernel · Edge VMs route north-south · vDS provides physical uplinks'
    )


def make_storage():
    return make_domain_svg(
        'Storage Domain — Interaction Map',
        'vSAN · vSphere Replication · VxRail · key protocols',
        'vSAN', ['vSAN Cluster', 'Disk Groups (cache + cap)', 'vSAN Datastore', 'vSAN ESA (8.x)'],
        ['esxcli vsan cluster get', 'SPBM policies: FTT, RAID, encryption'],
        ['Object storage: DOM/LSOM layers in ESXi', 'Witness VM for 2-node / stretched cluster',
         'Dedup/compression: cluster-wide or per-DG'],
        'vSphere Replication', ['VRMS (Replication Mgr)', 'vSphere Replication Agent', 'Recovery Site', 'RPO Config'],
        ['TCP/1500 VMRS protocol replication', 'Managed via vCenter plugin or PowerCLI'],
        ['Get-VrReplication, New-VrReplication', 'RPO: 5 min to 24 hrs (configurable)',
         'Planned migration or DR recovery'],
        'VxRail', ['VxRail Manager', 'vSAN HCI Cluster', 'Embedded vCenter', 'VxRail MARVIN API'],
        ['VxRail: managed by VCF LCM (preferred)', 'MARVIN API for node-level ops'],
        ['Firmware lifecycle via VxRail Manager', 'All nodes: same hardware SKU required',
         'VxRail includes: ESXi + vCenter + vSAN'],
        'Key Storage Integrations',
        [
            ('vSAN → ESXi',           'Kernel module',       'vSAN LSOM runs in ESXi kernel', 'No separate appliance needed'),
            ('vSAN → vCenter',        'SPBM / vSphere API',  'vCenter assigns storage policies','vSAN health in vCenter UI'),
            ('vSAN → NSX encryption', 'D@RE / KMS',          'VM encryption via KMS/vCenter',  'KMIP KMS integration'),
            ('vSphere Repl → vCenter','vCenter plugin',       'VRMS registers with vCenter',    'Managed in vCenter UI'),
            ('VxRail → VCF',          'SDDC Manager + LCM',  'VCF manages VxRail lifecycle',   'VxRail = managed HCI node'),
            ('vSAN → SRM',            'Array-based or VASA', 'SRM protection group includes vSAN VMs','RPO via SRM plan'),
        ],
        'vSAN is kernel-native · VxRail = ESXi + vCenter + vSAN as appliance · Replication is VM-level'
    )


def make_management():
    return make_domain_svg(
        'Management Domain — Interaction Map',
        'VCF · Aria Suite Lifecycle · vCenter · management APIs',
        'VCF / SDDC Manager', ['SDDC Manager', 'Cloud Builder', 'Workload Domains', 'VCF LCM'],
        ['REST API: sddc-mgr/v1 (Bearer token)', 'Manages: vCenter, NSX, vSAN, ESXi together'],
        ['vcf-password-ops for credential rotation', 'LCM bundles for firmware + software upgrades',
         'Workload domain = vCenter + NSX + vSAN stack'],
        'Aria Suite Lifecycle (LCM)', ['LCM Node', 'Locker (credentials)', 'Environment model', 'Request engine'],
        ['REST API: lcm/api/v2/environments', 'Deploys all Aria products (vRA, vROps, vRLI, vRNI)'],
        ['Certificate management via Locker', 'Upgrade orchestration for Aria Suite',
         'VMware Identity Manager (vidm) integration'],
        'vCenter Server', ['vCenter SSO', 'Inventory Service', 'VAMI (appliance mgmt)', 'Lifecycle Manager (vLCM)'],
        ['VAMI: VCSA appliance health + update', 'vLCM: ESXi image lifecycle management'],
        ['SSO: SAML provider for all VMware UIs', 'service-control --status on VCSA shell',
         'vmon-cli for per-service health'],
        'Key Management Integrations',
        [
            ('VCF → vCenter',         'SDDC Manager API',    'VCF deploys + manages vCenter',  'One vCenter per workload domain'),
            ('VCF → NSX',             'SDDC Manager API',    'VCF deploys + manages NSX',      'NSX for workload domain networking'),
            ('VCF → vSAN',            'SDDC Manager API',    'VCF manages vSAN via vCenter',   'vSAN part of vSphere cluster'),
            ('LCM → Aria products',   'LCM REST API',        'LCM installs/upgrades Aria Suite','lcm/api/v2/environments'),
            ('vCenter SSO → all',     'SAML / LDAP',         'SSO auth for NSX, vRA, vROps',   'Single sign-on federation'),
            ('VCF → VxRail',          'SDDC Manager + MARVIN','VCF + VxRail = VxRail Foundation','VxRail is managed HCI node'),
        ],
        'VCF = full-stack manager · LCM = Aria Suite deployer · vCenter SSO = auth hub for all UIs'
    )


def make_automation():
    return make_domain_svg(
        'Automation Domain — Interaction Map',
        'Aria Automation · Aria Operations · Aria Logs · Aria Networks · Tanzu · Horizon',
        'Aria Automation + Logs', ['Aria Automation (vRA)', 'Cloud Assembly', 'Service Broker', 'Aria Logs (vRLI)'],
        ['vRA REST API: /deployment/api', 'CSP token auth for all Aria APIs'],
        ['liagent (Log Insight agent) on VMs', 'cfapi ingestion on TCP/9543 (TLS)',
         'Aria Automation: ABX actions (serverless)'],
        'Aria Operations + Networks', ['Aria Operations (vROps)', 'Aria Networks (vRNI)', 'Collector nodes', 'Adapters'],
        ['vROps suite-api/api; vCenter adapter', 'vRNI REST API: /api/ni/entities'],
        ['vROps: capacity analytics + alert mgmt', 'vRNI: IPFIX + NSX flow + path analysis',
         'Collector: lightweight proxy per site'],
        'Tanzu + Horizon', ['Tanzu Kubernetes Grid', 'Supervisor Cluster', 'Horizon Connection Server', 'UAG'],
        ['TKG: tanzu CLI + kubectl + vsphere', 'Horizon: vdmadmin / hznCliAdmin / REST API'],
        ['kubectl vsphere login --server <SV IP>', 'Tanzu packages: cert-manager, contour, harbor',
         'Horizon: UAG on DMZ for external access'],
        'Key Automation Integrations',
        [
            ('Aria Auto → vCenter',   'vSphere API',         'vRA deploys VMs via vCenter',    'Cloud account: vCenter endpoint'),
            ('Aria Ops → vCenter',    'vCenter adapter',     'vROps collects vCenter metrics',  'Adapter polls vSphere API'),
            ('Aria Logs → all VMs',   'syslog / liagent',    'All VMs ship logs to vRLI',       'liagent or direct syslog UDP/514'),
            ('vRNI → NSX + vCenter',  'IPFIX / REST',        'vRNI reads flow + topology data', 'NSX as data source in vRNI'),
            ('Tanzu → vCenter',       'WCP / vSphere API',   'Supervisor cluster on vCenter',   'kubectl vsphere login'),
            ('Horizon → vCenter',     'vSphere API',         'Horizon clones VMs in vCenter',   'Composer or instant clone'),
        ],
        'Aria Suite consumes vCenter API · Tanzu runs on vSphere · Horizon provisions via vCenter cloning'
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f'=== generate_svgs_interaction.py [{"DRY RUN" if DRY else "WRITE"}] ===\n')
    ASSETS.mkdir(parents=True, exist_ok=True)

    svgs = [
        ('interaction-map-master.svg',     make_master()),
        ('interaction-map-compute.svg',    make_compute()),
        ('interaction-map-network.svg',    make_network()),
        ('interaction-map-storage.svg',    make_storage()),
        ('interaction-map-management.svg', make_management()),
        ('interaction-map-automation.svg', make_automation()),
    ]
    for fname, svg in svgs:
        write_svg(fname, svg)

    print(f'\nDone. {len(svgs)} SVGs {"validated (dry run)" if DRY else "written to docs/assets/"}.')


if __name__ == '__main__':
    main()
