"""
Amazon EVS (Elastic VMware Service) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── EVS Root ──────────────────────────────────────────────────────────────────

@kb_diagram(
    'evs',
    'docs/cloud/aws/evs/index.md',
    'Amazon EVS Overview — VCF on bare-metal EC2, vSAN, NSX-T, HCX',
)
def evs_root():
    """Amazon EVS Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99
    M1 = (B1_L + B1_R) // 2
    M2 = (B2_L + B2_R) // 2
    B3_L, B3_R = 3, 50
    B4_L, B4_R = 53, 99
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80

    lines = []
    lines.append(title_border(W2, 'Amazon EVS — Elastic VMware Service'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Amazon Elastic VMware Service (EVS)')))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Cloud Foundation (VCF) running on dedicated bare-metal EC2 in your VPC')))
    lines.append(R(bMid(IV_L, IV_R, 'Hosts: i4i.metal / i3en.metal; ESXi installed by AWS; vSAN HCI storage')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: OVN via NSX-T overlay on ENIs; T0 BGP to VPC routing tables')))
    lines.append(R(bMid(IV_L, IV_R, 'Migration: HCX vMotion / bulk migration from on-premises; no re-IP required')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Control plane and storage are VCF-managed; host lifecycle is AWS-managed'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VCF Management Domain'),
        bMid(B2_L, B2_R, 'AWS Layer'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  SDDC Manager'),
        bMid(B2_L, B2_R, '  Bare-metal EC2 hosts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vCenter Server'),
        bMid(B2_L, B2_R, '  VPC + subnets + ENIs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  NSX-T Manager (3-node)'),
        bMid(B2_L, B2_R, '  Direct Connect / TGW'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vSAN (NVMe disk groups)'),
        bMid(B2_L, B2_R, '  S3, KMS, Secrets Mgr'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(R(connector([PD1, PD2, PD3, PD4])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B3_L, B3_R), bTop(B4_L, B4_R))))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Security'),
        bMid(B4_L, B4_R, 'Migration & Connectivity'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  IAM roles (cluster mgmt)'),
        bMid(B4_L, B4_R, '  HCX: vMotion + bulk migrate'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  vSphere RBAC + SSO/AD'),
        bMid(B4_L, B4_R, '  Network Extension (L2 stretch)'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  NSX-T DFW micro-segment'),
        bMid(B4_L, B4_R, '  DX private VIF to EVS VPC'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  vSAN encryption (KMS)'),
        bMid(B4_L, B4_R, '  Transit Gateway (multi-VPC)'),
    )))
    lines.append(R(merge(bBot(B3_L, B3_R), bBot(B4_L, B4_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  EVS         = Amazon Elastic VMware Service; managed VCF on dedicated bare-metal EC2'))
    lines.append(txt_row('  i4i.metal   = Primary EVS host type; 128 vCPU, 1 TB RAM, 30 TB NVMe; supports vSAN ESA'))
    lines.append(txt_row('  VCF         = VMware Cloud Foundation; SDDC Manager + vCenter + vSAN + NSX-T stack'))
    lines.append(txt_row('  HCX         = VMware Hybrid Cloud Extension; live + cold VM migration to/from on-prem'))
    lines.append(txt_row('  ENI         = Elastic Network Interface; used for NSX-T VTEP and management VMkernels'))
    lines.append(txt_row('  DX          = Direct Connect; private 1G or 10G link between on-premises and AWS'))
    lines.append(txt_row())

    return lines


# ── EVS Architecture ──────────────────────────────────────────────────────────

def evs_architecture():
    """EVS Architecture landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Amazon EVS Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'EVS Architecture Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: How It Works (bare-metal model), Design Standards, Integrations')))
    lines.append(R(bMid(IV_L, IV_R, 'Hosts: dedicated i4i.metal; ESXi runs natively on hardware in your VPC subnet')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX-T overlay on ENIs; T0 router BGP to VPC; workload CIDRs propagated to TGW')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Design Standards'),
        bMid(B3_L, B3_R, 'Integrations'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Bare-metal host model'),
        bMid(B2_L, B2_R, '  Cluster sizing rules'),
        bMid(B3_L, B3_R, '  HCX migration'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  VPC subnet layout'),
        bMid(B2_L, B2_R, '  CIDR planning'),
        bMid(B3_L, B3_R, '  Direct Connect'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  NSX-T Geneve overlay'),
        bMid(B2_L, B2_R, '  AZ placement'),
        bMid(B3_L, B3_R, '  Transit Gateway'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vSAN HCI storage'),
        bMid(B2_L, B2_R, '  DX bandwidth guide'),
        bMid(B3_L, B3_R, '  AWS native services'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines


# ── EVS Deploy ────────────────────────────────────────────────────────────────

@kb_diagram(
    'evs-deploy',
    'docs/cloud/aws/evs/deploy/index.md',
    'EVS deployment — VPC prereqs, cluster creation, VCF init, HCX setup',
)
def evs_deploy():
    """EVS Deploy page — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99

    lines = []
    lines.append(title_border(W2, 'Amazon EVS Deployment'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'EVS Deployment Sequence')))
    lines.append(R(bMid(IV_L, IV_R, 'Pre-requisites: VPC, subnets, SGs, IAM service-linked role, key pair, DX')))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster creation via AWS console or CLI; takes 90-120 minutes')))
    lines.append(R(bMid(IV_L, IV_R, 'Post-deploy: retrieve secrets, configure SDDC Manager, deploy HCX service mesh')))
    lines.append(R(bMid(IV_L, IV_R, 'Validation: cluster CREATED + vSAN green + NSX-T stable + HCX service mesh Up')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  SDDC Manager = VCF control plane; manages hosts, domains, upgrades, credentials'))
    lines.append(txt_row('  VTEP subnet  = NSX-T tunnel endpoint traffic; separate from management subnet'))
    lines.append(txt_row('  Service mesh = HCX Interconnect + WAN Opt + Network Extension appliance pair'))
    lines.append(txt_row())

    return lines


# ── EVS Operations ────────────────────────────────────────────────────────────

@kb_diagram(
    'evs-operations',
    'docs/cloud/aws/evs/operations/index.md',
    'EVS operations landing — health checks, procedures, lifecycle, backup',
)
def evs_operations():
    """EVS Operations landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Amazon EVS Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'EVS Day-2 Operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Six sub-sections: CLI, Health Checks, Procedures, Upgrades, Backup, Scripts')))
    lines.append(R(bMid(IV_L, IV_R, 'Health baseline: cluster CREATED + all hosts CREATED + vSAN green + NSX stable')))
    lines.append(R(bMid(IV_L, IV_R, 'Host add/remove via AWS EVS API after vSAN evacuation completes (BytesToSync=0)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Health'),
        bMid(B2_L, B2_R, 'Host Management'),
        bMid(B3_L, B3_R, 'VCF Lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  AWS cluster state'),
        bMid(B2_L, B2_R, '  Add host (API)'),
        bMid(B3_L, B3_R, '  SDDC Manager upgrades'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vSAN health checks'),
        bMid(B2_L, B2_R, '  Remove host (evacuate)'),
        bMid(B3_L, B3_R, '  VCF upgrade sequence'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  NSX-T component status'),
        bMid(B2_L, B2_R, '  HCX migration'),
        bMid(B3_L, B3_R, '  HCX version upgrade'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines


# ── EVS Security ──────────────────────────────────────────────────────────────

@kb_diagram(
    'evs-security',
    'docs/cloud/aws/evs/security/index.md',
    'EVS security landing — IAM, vSphere RBAC, NSX-T DFW, encryption',
)
def evs_security():
    """EVS Security landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'Amazon EVS Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'EVS Security Controls')))
    lines.append(R(bMid(IV_L, IV_R, 'Four sub-sections: Access Control (IAM + vSphere RBAC), Auth, Encryption, Hardening')))
    lines.append(R(bMid(IV_L, IV_R, 'Two RBAC planes: AWS IAM (host/cluster lifecycle) + vSphere RBAC (VM operations)')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX-T DFW: default deny + explicit allow; VPC SGs restrict management access')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Identity & Access'),
        bMid(B2_L, B2_R, 'Data & Network Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  AWS IAM scoped policies'),
        bMid(B2_L, B2_R, '  vSAN encryption (NKP/KMS)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vSphere RBAC roles'),
        bMid(B2_L, B2_R, '  VM encryption policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  AD/LDAP SSO integration'),
        bMid(B2_L, B2_R, '  NSX-T DFW default deny'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  MFA for AWS console'),
        bMid(B2_L, B2_R, '  VPC Flow Logs audit'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())

    return lines


# ── EVS Troubleshooting ───────────────────────────────────────────────────────

@kb_diagram(
    'evs-troubleshooting',
    'docs/cloud/aws/evs/troubleshooting/index.md',
    'EVS troubleshooting landing — host failures, vSAN, HCX, AWS support',
)
def evs_troubleshooting():
    """EVS Troubleshooting landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Amazon EVS Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'EVS Troubleshooting Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: Common Issues, Diagnostics (bundles/logs), Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Host FAILED state: contact AWS support before deleting (preserves diagnostics)')))
    lines.append(R(bMid(IV_L, IV_R, 'Joint issues (HCX, NSX-T/VPC): open both AWS and VMware support cases')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Host FAILED state'),
        bMid(B2_L, B2_R, '  CloudTrail EVS events'),
        bMid(B3_L, B3_R, '  AWS severity levels'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  vSAN degraded health'),
        bMid(B2_L, B2_R, '  VPC Flow Logs query'),
        bMid(B3_L, B3_R, '  Required case data'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  HCX service mesh down'),
        bMid(B2_L, B2_R, '  NSX-T support bundle'),
        bMid(B3_L, B3_R, '  AWS + VMware joint'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  NSX-T routing failure'),
        bMid(B2_L, B2_R, '  Log locations table'),
        bMid(B3_L, B3_R, '  TAM escalation path'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines
