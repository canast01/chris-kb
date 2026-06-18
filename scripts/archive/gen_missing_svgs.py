#!/usr/bin/env python3
"""Generate the 6 missing architecture SVGs and embed them in their pages."""
import os

W, H = 820, 750
C1X, C2X, C3X = 20, 285, 550
CW = 250
TITLE_H = 58
COL_Y = 72
COL_H = 390
TABLE_Y = 480
TABLE_H = 222
FOOTER_Y = 720

ITEM_YS = [126, 152, 178, 204, 230]
NOTE_YS = [282, 300, 318, 336, 354, 372, 390, 408]


def svg_header(title, subtitle):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="'Segoe UI',Arial,sans-serif">
  <rect width="{W}" height="{H}" fill="#f4f6f9"/>
  <rect x="0" y="0" width="{W}" height="{TITLE_H}" fill="#1a2744"/>
  <text x="410" y="36" text-anchor="middle" fill="white" font-size="20" font-weight="700" letter-spacing="0.5">{title}</text>
  <text x="410" y="52" text-anchor="middle" fill="#7a8fbb" font-size="11">{subtitle}</text>'''


def svg_column(cx, col_name, col_sub, hdr_color, light, dark, mid, items, notes):
    mid_x = cx + CW // 2
    lines = [
        f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="{COL_H}" fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
        f'  <rect x="{cx}" y="{COL_Y}" width="{CW}" height="42" fill="{hdr_color}" rx="6"/>',
        f'  <rect x="{cx}" y="{COL_Y+28}" width="{CW}" height="14" fill="{hdr_color}"/>',
        f'  <text x="{mid_x}" y="{COL_Y+25}" text-anchor="middle" fill="white" font-size="13" font-weight="700">{col_name}</text>',
        f'  <text x="{mid_x}" y="{COL_Y+39}" text-anchor="middle" fill="{mid}" font-size="9">{col_sub}</text>',
    ]
    for y, item in zip(ITEM_YS, items):
        lines += [
            f'  <rect x="{cx+10}" y="{y}" width="{CW-20}" height="22" fill="{light}" rx="3" stroke="{mid}" stroke-width="1"/>',
            f'  <text x="{mid_x}" y="{y+15}" text-anchor="middle" fill="{dark}" font-size="9" font-weight="700">{item}</text>',
        ]
    for y, note in zip(NOTE_YS, notes):
        lines.append(f'  <text x="{mid_x}" y="{y}" text-anchor="middle" fill="#78909c" font-size="9">{note}</text>')
    return '\n'.join(lines)


def svg_table(table_title, col_headers, rows):
    """rows = list of (label, c1, c2, c3) tuples."""
    TW = 780
    TX = 20
    lines = [
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="{TABLE_H}" fill="#fff" rx="6" stroke="#dde2ec" stroke-width="1.2"/>',
        f'  <rect x="{TX}" y="{TABLE_Y}" width="{TW}" height="36" fill="#1a2744" rx="6"/>',
        f'  <rect x="{TX}" y="{TABLE_Y+24}" width="{TW}" height="12" fill="#1a2744"/>',
        f'  <text x="410" y="{TABLE_Y+24}" text-anchor="middle" fill="white" font-size="13" font-weight="700">{table_title}</text>',
        f'  <rect x="{TX}" y="{TABLE_Y+36}" width="{TW}" height="28" fill="#eceff1"/>',
    ]
    # Column header positions (4 columns)
    hdr_xs = [120, 320, 520, 700]
    for x, h in zip(hdr_xs, col_headers):
        lines.append(f'  <text x="{x}" y="{TABLE_Y+55}" text-anchor="middle" fill="#37474f" font-size="10" font-weight="700">{h}</text>')
    # Vertical dividers
    for dx in [220, 415, 610]:
        lines.append(f'  <line x1="{TX+dx}" y1="{TABLE_Y+36}" x2="{TX+dx}" y2="{TABLE_Y+TABLE_H}" stroke="#dde2ec" stroke-width="1"/>')
    # Data rows
    for i, (label, c1, c2, c3) in enumerate(rows):
        ry = TABLE_Y + 64 + i * 26
        if i % 2 == 0:
            lines.append(f'  <rect x="{TX}" y="{ry-14}" width="{TW}" height="26" fill="#f7f9fb"/>')
        lines += [
            f'  <text x="120" y="{ry}" text-anchor="middle" fill="#455a64" font-size="9">{label}</text>',
            f'  <text x="320" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{c1}</text>',
            f'  <text x="520" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{c2}</text>',
            f'  <text x="700" y="{ry}" text-anchor="middle" fill="#546e7a" font-size="9">{c3}</text>',
        ]
    lines.append(f'  <line x1="{TX}" y1="{TABLE_Y+TABLE_H}" x2="{TX+TW}" y2="{TABLE_Y+TABLE_H}" stroke="#dde2ec" stroke-width="1"/>')
    return '\n'.join(lines)


def svg_footer(text):
    return f'''  <rect x="0" y="{FOOTER_Y}" width="{W}" height="30" fill="#1a2744"/>
  <text x="410" y="{FOOTER_Y+19}" text-anchor="middle" fill="#7a8fbb" font-size="9">{text}</text>
</svg>'''


def make_svg(title, subtitle, cols, table_title, col_headers, rows, footer):
    parts = [svg_header(title, subtitle)]
    for cx, (name, sub, hdr, light, dark, mid, items, notes) in zip([C1X, C2X, C3X], cols):
        parts.append(svg_column(cx, name, sub, hdr, light, dark, mid, items, notes))
    parts.append(svg_table(table_title, col_headers, rows))
    parts.append(svg_footer(footer))
    return '\n'.join(parts)


# ── SVG definitions ─────────────────────────────────────────────────────────

SVGS = {}

# 1 — Top-level architecture
SVGS['architecture-overview'] = make_svg(
    title="Architecture — Design Principles",
    subtitle="Compute HA · Storage Resilience · Network Redundancy · Disaster Recovery",
    cols=[
        ("Compute & HA", "vSphere clusters · HA/DRS",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["vSphere Cluster (HA/DRS)", "Anti-Affinity Rules", "vCenter HA (3-node)", "Fault Domains", "Heartbeat Datastores"],
         ["N+1 host capacity minimum", "HA admission control: 25%", "DRS: fully automated", "VM restart priority defined", "Cross-host vMotion enabled", "VCSA backed up daily", "No single host dependency", "Capacity headroom monitored"]),
        ("Storage & Networking", "SAN/NAS/HCI · redundant paths",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Primary Storage (SAN/HCI)", "Backup Storage (DD/NFS)", "Dual-fabric SAN (FC)", "Redundant NICs (LACP)", "Storage Replication", "Network Segmentation"],
         ["RAID / FTT per workload tier", "Backup to separate datastore", "Multipath I/O (Round Robin)", "VLAN isolation per tier", "NSX microsegmentation", "Jumbo frames on storage", "Storage queue depth tuned", "Path failover tested"]),
        ("Disaster Recovery", "RPO/RTO · site pairing",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["RPO / RTO Defined per App", "Site Pairing (SRM/SRDF)", "Sync Replication (RecoverPoint)", "Async Replication (SnapMirror)", "Backup + Recovery (Veeam)"],
         ["RPO: mission-critical ≤ 15 min", "RTO: tier-1 ≤ 4 hours", "DR test: quarterly minimum", "Runbooks: documented+tested", "Failover: automated SRM", "Backup retention: 30 days+", "Offsite copy mandatory", "Recovery validated annually"]),
    ],
    table_title="Architecture Pattern Comparison",
    col_headers=["Pattern", "Active/Active", "Active/Passive", "Backup Only"],
    rows=[
        ("Compute HA", "DRS + HA across hosts", "vCenter HA (VCSA)", "Manual restart"),
        ("Storage HA", "vSAN / dual-fabric FC", "SnapMirror async", "Backup restore"),
        ("Network HA", "LACP / dual uplinks", "NIC teaming failover", "Single path"),
        ("Recovery Model", "Zero-downtime failover", "SRM orchestrated", "Restore from backup"),
        ("RPO Target", "0 (synchronous)", "≤ 15 min async", "≤ 24 hours"),
        ("RTO Target", "Seconds (automatic)", "≤ 4 hours (SRM)", "Hours to days"),
    ],
    footer="Architecture Design Reference · Compute HA · Storage Resilience · Network Redundancy · DR Patterns"
)

# 2 — AWS
SVGS['aws-architecture-overview'] = make_svg(
    title="AWS — Multi-Account Platform Architecture",
    subtitle="Management Account · Transit Gateway · Workload Accounts · SCPs",
    cols=[
        ("Management Account", "Org root · SCPs · SSO · Billing",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["AWS Organizations Root", "Service Control Policies (SCPs)", "IAM Identity Center (SSO)", "AWS Config (Detective)", "Security Hub + GuardDuty"],
         ["No workloads in mgmt account", "SCPs: preventive guardrails", "SSO: centralized login", "Config: compliance rules org-wide", "Security Hub: aggregated findings", "Billing: consolidated + CUR", "CloudTrail: org-wide logging", "Delegated admins per service"]),
        ("Shared Services Account", "TGW hub · DNS · Inspection",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Transit Gateway (Hub)", "Shared Services VPC", "Route 53 Resolver", "AWS Directory Service", "Network Firewall / Inspection"],
         ["TGW: hub-and-spoke routing", "VPC peering via TGW attachments", "Centralized egress (NAT/FW)", "Private DNS resolvers", "Certificate Manager (ACM)", "Inspector: vuln scanning", "Macie: data classification", "VPN/DirectConnect termination"]),
        ("Workload Accounts", "Dev · Staging · Prod isolation",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["Dedicated per Env/Team", "Spoke VPCs (RFC 1918)", "EC2 / ECS / EKS / Lambda", "RDS / S3 / DynamoDB", "IAM Roles (least privilege)"],
         ["One account per environment", "No direct internet egress", "All egress via TGW to FW", "S3: bucket policy + SCP", "CloudWatch + X-Ray telemetry", "Cost tagged: env+owner+team", "SCPs restrict risky actions", "Separate blast radius"]),
    ],
    table_title="AWS Account Type Comparison",
    col_headers=["Characteristic", "Management", "Shared Services", "Workload"],
    rows=[
        ("Workloads permitted", "✗ — governance only", "Shared infra only", "✓ — all workloads"),
        ("Internet egress", "✗ restricted by SCP", "Centralized NAT/FW", "Via TGW to shared"),
        ("SCPs applied", "Root — all OUs", "Shared Services OU", "Per environment OU"),
        ("DirectConnect", "Management plane", "✓ — VIF termination", "Via TGW"),
        ("Billing scope", "Consolidated root", "Shared cost allocation", "Per-team chargeback"),
        ("Security tooling", "GuardDuty / Hub master", "Network Firewall", "Detective controls"),
    ],
    footer="AWS Platform Reference · Organizations · IAM Identity Center · Transit Gateway · SCPs · Security Hub"
)

# 3 — Azure
SVGS['azure-architecture-overview'] = make_svg(
    title="Azure — Platform Architecture",
    subtitle="Management Groups · Hub-Spoke VNets · Entra ID · Azure Policy",
    cols=[
        ("Management Layer", "Tenant · MGs · Subscriptions",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["Entra ID Tenant", "Management Groups (Org Scope)", "Subscriptions (Isolation)", "Resource Groups", "Azure Policy (Preventive)"],
         ["Root MG: org-wide policies", "MG hierarchy: platform/workloads", "Sub per environment or team", "RBAC: least privilege", "Policy: audit + deny effects", "Blueprints / Landing Zones", "Cost Management + Budgets", "Activity Log: all changes"]),
        ("Hub-Spoke Networking", "Shared services · Peering",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Hub VNet (Shared Services)", "Azure Firewall / NVA", "ExpressRoute / VPN Gateway", "Azure DNS Private Zones", "Spoke VNets (Workloads)"],
         ["Hub-spoke via VNet peering", "Centralized egress inspection", "ExpressRoute: on-prem ≥1 Gbps", "Private DNS resolves to RFC1918", "Bastion: no public RDP/SSH", "NSG + UDR on each spoke", "Service endpoints: PaaS lockdown", "Peering: non-transitive — use hub"]),
        ("Identity & Security", "Entra ID · PIM · Defender",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["Entra ID (formerly Azure AD)", "SSO / MFA / Conditional Access", "PIM (Privileged Identity Mgmt)", "Defender for Cloud", "Microsoft Sentinel (SIEM)"],
         ["MFA enforced for all users", "Conditional Access: device+location", "PIM: just-in-time elevated access", "No standing Owner/Contributor", "Defender: secure score tracked", "Sentinel: SOC SIEM platform", "Key Vault: secrets, certs, keys", "Managed Identity over service accts"]),
    ],
    table_title="Azure Subscription Type Comparison",
    col_headers=["Characteristic", "Connectivity Hub", "Prod Workload", "Dev/Test"],
    rows=[
        ("VNet peering", "Hub — connects all spokes", "Spoke to hub only", "Spoke to hub only"),
        ("Internet egress", "Azure Firewall (centralized)", "Via hub firewall", "Via hub firewall"),
        ("Policy strictness", "Platform baseline", "Production + stricter", "Relaxed for dev"),
        ("ExpressRoute access", "✓ — directly connected", "Via hub (peering)", "Via hub (peering)"),
        ("PIM required", "✓ — platform team", "✓ — all elevated", "Recommended"),
        ("Cost allocation", "Shared infra tag", "Per-team BU tag", "Dev tag + budget alert"),
    ],
    footer="Azure Platform Reference · Management Groups · Hub-Spoke Networking · Entra ID · Azure Policy"
)

# 4 — FlashArray
SVGS['flasharray-architecture-overview'] = make_svg(
    title="Pure FlashArray — Architecture Models",
    subtitle="Dual-Controller HA · //X · //C · //E · ActiveCluster · Purity OS",
    cols=[
        ("FlashArray //X", "High-performance all-NVMe",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["Dual Controllers (CT0 / CT1)", "NVMe DirectFlash Modules", "FC / iSCSI / NVMe-oF / NFS", "Inline Dedup + Compression", "ActiveCluster (RPO=0)"],
         ["Active/active controller pair", "NVRAM write mirroring < 1 ms ACK", "DirectFlash: no SSD translation", "Dedup+compress before flash write", "Thin provisioning always on", "Evergreen subscription model", "Purity//FA OS update non-disruptive", "REST API + Pure1 cloud mgmt"]),
        ("FlashArray //C", "Capacity-optimised QLC flash",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Dual Controllers (CT0 / CT1)", "NVMe + QLC Capacity Flash", "FC / iSCSI / NVMe-oF", "Inline Dedup + Compression", "ActiveDR (async low-RPO)"],
         ["Optimised for warm/cold data", "Higher capacity per U vs //X", "Same Purity OS as //X", "Compatible with //X pods", "ActiveCluster with //X arrays", "S3 offload to FlashBlade / cloud", "Non-disruptive controller upgrade", "Shared management via Pure1"]),
        ("Replication & HA", "ActiveCluster · ActiveDR · Pods",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["ActiveCluster (Sync, RPO=0)", "ActiveDR (Async, low RPO)", "Stretch Pod (both sites active)", "Mediator (split-brain resolution)", "ActiveDR Failover < 30 s"],
         ["ActiveCluster: both sites serve I/O", "Mediator required for AC split-brain", "Pod contains volumes+hosts+policies", "Sync pod replicates before ACK", "ActiveDR: RPO configurable (sec–min)", "Cross-array volume replication", "Pod promote/demote for failover", "Compatible across //X and //C"]),
    ],
    table_title="FlashArray Product Line Comparison",
    col_headers=["Feature", "FlashArray //X", "FlashArray //C", "FlashArray //E"],
    rows=[
        ("Flash media", "NVMe DirectFlash", "NVMe + QLC", "NVMe SSD"),
        ("Protocol support", "FC / iSCSI / NVMe-oF / NFS", "FC / iSCSI / NVMe-oF", "FC / iSCSI"),
        ("ActiveCluster", "✓", "✓ (with //X)", "✗"),
        ("Inline dedup/compress", "✓ always-on", "✓ always-on", "✓"),
        ("Target workload", "Tier-1 / latency-sensitive", "Mixed / capacity-oriented", "Entry / remote sites"),
        ("Max usable (eff.)", "Multi-PB with dedup", "High-density PB+", "Smaller footprint"),
    ],
    footer="Pure FlashArray Reference · Dual-Controller HA · //X · //C · //E · ActiveCluster · Purity OS"
)

# 5 — vCenter
SVGS['vcenter-architecture-overview'] = make_svg(
    title="vCenter — VCSA Deployment Models",
    subtitle="Standard VCSA · vCenter HA · Enhanced Linked Mode",
    cols=[
        ("Standard VCSA", "Single appliance — default",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["VCSA Linux Appliance (OVA)", "Embedded PSC (vCenter 7.0+)", "Embedded Postgres DB", "SSO Domain (vsphere.local)", "VAMI (Port 5480)"],
         ["No external PSC since vSphere 7", "SSO: add AD/LDAP identity source", "VAMI: network, NTP, backup, certs", "Backed up to SFTP/NFS (VAMI)", "File-based backup: scheduled daily", "VMCA: built-in cert authority", "Update via VAMI or LCM", "Sizing: Small/Medium/Large/XL"]),
        ("vCenter HA", "3-node: active/passive/witness",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Active Node (primary VCSA)", "Passive Node (hot standby)", "Witness Node (quorum only)", "HA Network (2nd NIC)", "Automatic Failover < 5 min"],
         ["Protects VCSA from host failure", "Passive: full DB sync continuously", "Witness: prevents split-brain", "HA network: dedicated segment/vLAN", "All 3 nodes on separate ESXi hosts", "Shared datastore: NFS or VMFS", "Failover: automatic + alerts", "Not a replacement for backup!"]),
        ("Enhanced Linked Mode", "Multi-vCenter unified view",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["Multiple VCSA Instances", "Single SSO Domain (federated)", "Unified Inventory View (vSphere UI)", "Cross-vCenter vMotion", "Cross-vCenter SRM DR"],
         ["Up to 15 vCenters per SSO domain", "Linked Mode: join existing SSO", "Cross-vCenter: same datacenter/DC", "Long-distance vMotion via HCX", "SRM: multi-vCenter protection", "Each vCenter: independent DB", "Permissions replicated across", "Used in multi-site / multi-DC"]),
    ],
    table_title="vCenter Deployment Model Comparison",
    col_headers=["Characteristic", "Standard VCSA", "vCenter HA", "Enhanced Linked Mode"],
    rows=[
        ("VCSA count", "1", "3 (active+passive+witness)", "2–15 independent"),
        ("Host failure protection", "✗ — restart manually", "✓ — auto failover", "Per-site"),
        ("Failover time", "N/A (manual)", "< 5 minutes", "Per-site"),
        ("Cross-vCenter visibility", "✗", "Same vCenter only", "✓ — unified UI"),
        ("SSO domain", "Independent", "Single shared", "Single federated"),
        ("Use case", "Single-site standard", "Production HA", "Multi-site/multi-DC"),
    ],
    footer="VMware vCenter Reference · VCSA Appliance · vCenter HA · Enhanced Linked Mode · SSO Domain"
)

# 6 — vSAN
SVGS['vsan-architecture-overview'] = make_svg(
    title="vSAN — Storage Architecture Models",
    subtitle="OSA · ESA · Stretched Cluster · 2-Node Remote",
    cols=[
        ("vSAN OSA", "Original Storage Architecture",
         "#1565c0", "#e3f2fd", "#1565c0", "#90caf9",
         ["Disk Groups (cache + capacity)", "NVMe/SSD Cache Tier", "SSD/HDD Capacity Tier", "RAID-1 / RAID-5 / RAID-6", "FTT=1 (RAID-1) default"],
         ["Min 3 hosts (RAID-1/FTT=1)", "Cache: ≥ 10% of capacity tier", "All-flash or hybrid config", "RAID-5 FTT=1: 4 hosts min", "RAID-6 FTT=2: 6 hosts min", "Dedup + compress: all-flash only", "vSAN health: continuous monitoring", "SPBM policies per VM"]),
        ("vSAN ESA", "Express Storage Architecture",
         "#6a1b9a", "#f3e5f5", "#4a148c", "#ce93d8",
         ["Single-Tier NVMe Only", "No Separate Cache Disk", "Compression-First Write Path", "RAID-5/6 Default (space-eff.)", "Min 4 Hosts Required"],
         ["Next-gen hardware required (HCL)", "No disk groups — single pool", "Higher space efficiency vs OSA", "Snapshots: space-efficient", "RAID-5: 4 hosts / RAID-6: 6 hosts", "vSAN Max: highest perf tier", "Requires vSAN ESA-certified NICs", "ESA license required"]),
        ("Stretched / 2-Node", "Multi-site resilience",
         "#00695c", "#e0f2f1", "#004d40", "#80cbc4",
         ["2 Data Sites + 1 Witness", "Synchronous Write Both Sites", "RPO=0 on Site Failure", "Witness VM (2 vCPU / 8 GB)", "2-Node: ROBO / Branch"],
         ["Stretched: metro distance only", "Stretched: low latency < 5 ms RTT", "Witness: separate 3rd site / cloud", "2-Node: 2 hosts + witness VM", "2-Node: min 25 Mbps bandwidth", "Manual failover for stretched", "PFTT=1 across sites", "vSAN Witness Appliance OVA"]),
    ],
    table_title="vSAN Architecture Comparison",
    col_headers=["Characteristic", "OSA", "ESA", "Stretched / 2-Node"],
    rows=[
        ("Min hosts (RAID-1)", "3", "4", "2 + 1 witness"),
        ("Cache tier", "Separate disk group", "None (single pool)", "Per-site disk groups"),
        ("NVMe required", "✗ (SSD supported)", "✓ NVMe only", "✗ (OSA hardware)"),
        ("Space efficiency", "Good (dedup+compress)", "Higher (compress-first)", "Per-site RAID policy"),
        ("Site resilience", "Host-level only", "Host-level only", "Full site failure"),
        ("Use case", "Standard HCI", "Next-gen high-density", "Metro DR / ROBO"),
    ],
    footer="VMware vSAN Reference · OSA · ESA · Stretched Cluster · 2-Node · SPBM · Disk Groups"
)

# ── Write SVG files ──────────────────────────────────────────────────────────

SVG_DIR = 'docs/assets'
os.makedirs(SVG_DIR, exist_ok=True)

for name, content in SVGS.items():
    path = f'{SVG_DIR}/{name}.svg'
    with open(path, 'w') as f:
        f.write(content)
    print(f'  Wrote {path}')

# ── Embed in pages ────────────────────────────────────────────────────────────

EMBEDS = [
    ('docs/architecture/index.md',
     'Architecture Design Principles',
     '../assets/architecture-overview.svg'),
    ('docs/cloud/aws/architecture/index.md',
     'AWS Platform Architecture',
     '../../../assets/aws-architecture-overview.svg'),
    ('docs/cloud/azure/architecture/index.md',
     'Azure Platform Architecture',
     '../../../assets/azure-architecture-overview.svg'),
    ('docs/storage/pure/flasharray/architecture/index.md',
     'FlashArray Architecture Models',
     '../../../../assets/flasharray-architecture-overview.svg'),
    ('docs/virtualization/vmware/vcenter/architecture/index.md',
     'vCenter Deployment Models',
     '../../../../assets/vcenter-architecture-overview.svg'),
    ('docs/virtualization/vmware/vsan/architecture/index.md',
     'vSAN Architecture Models',
     '../../../../assets/vsan-architecture-overview.svg'),
]

for page_path, section_title, svg_rel_path in EMBEDS:
    with open(page_path) as f:
        content = f.read()
    if svg_rel_path.split('/')[-1].replace('.svg', '') in content:
        print(f'  SKIP (already embedded): {page_path}')
        continue
    addition = f'\n\n## {section_title}\n\n![{section_title}]({svg_rel_path})\n'
    with open(page_path, 'a') as f:
        f.write(addition)
    print(f'  Embedded in {page_path}')

print('\nDone.')
