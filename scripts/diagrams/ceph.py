"""
Ceph distributed storage diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── Ceph Root ─────────────────────────────────────────────────────────────────

@kb_diagram(
    'ceph',
    'docs/storage/ceph/index.md',
    'Ceph distributed storage overview — RADOS, OSD/MON/MGR, RBD/CephFS/RGW',
)
def ceph_root():
    """Ceph Platform Overview — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99
    B4_L, B4_R = 3, 50
    B5_L, B5_R = 53, 99
    PD1, PD2, PD3, PD4 = 18, 48, 68, 88

    lines = []
    lines.append(title_border(W2, 'Ceph Distributed Storage'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph — Open-source Distributed Storage System')))
    lines.append(R(bMid(IV_L, IV_R, 'Provides block (RBD), file (CephFS), and object (RGW/S3) from one cluster')))
    lines.append(R(bMid(IV_L, IV_R, 'RADOS: object store engine; CRUSH: placement algorithm without metadata server')))
    lines.append(R(bMid(IV_L, IV_R, 'OSD: 1 per disk; MON: 3-5 for quorum; MGR: 2 for orchestration + dashboard')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication: N copies (replica pool) or erasure coding (k+m chunks)')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Block (RBD)'),
        bMid(B2_L, B2_R, 'File (CephFS)'),
        bMid(B3_L, B3_R, 'Object (RGW)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Thin-prov images'),
        bMid(B2_L, B2_R, '  POSIX filesystem'),
        bMid(B3_L, B3_R, '  S3/Swift compatible'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Snapshots + clones'),
        bMid(B2_L, B2_R, '  MDS for namespace'),
        bMid(B3_L, B3_R, '  radosgw-admin users'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  K8s CSI / OpenStack'),
        bMid(B2_L, B2_R, '  NFS-Ganesha export'),
        bMid(B3_L, B3_R, '  Bucket lifecycle/quota'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(R(connector([PD1, PD2, PD3, PD4])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B4_L, B4_R), bTop(B5_L, B5_R))))
    lines.append(R(merge(
        bMid(B4_L, B4_R, 'RADOS Layer'),
        bMid(B5_L, B5_R, 'Daemon Layer'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  Object store (all pools)'),
        bMid(B5_L, B5_R, '  OSD: 1 per disk'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  CRUSH placement algo'),
        bMid(B5_L, B5_R, '  MON: cluster map quorum'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  PG replication/EC'),
        bMid(B5_L, B5_R, '  MGR: metrics + orchestration'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  Self-healing recovery'),
        bMid(B5_L, B5_R, '  cephadm: container mgmt'),
    )))
    lines.append(R(merge(bBot(B4_L, B4_R), bBot(B5_L, B5_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  RADOS   = Reliable Autonomic Distributed Object Store; storage engine for all Ceph services'))
    lines.append(txt_row('  OSD     = Object Storage Daemon; one per disk; stores data + handles replication/recovery'))
    lines.append(txt_row('  CRUSH   = Controlled Replication Under Scalable Hashing; placement algorithm (no lookup)'))
    lines.append(txt_row('  PG      = Placement Group; unit of replication; ~100 per OSD; maps to set of OSDs'))
    lines.append(txt_row('  BlueStore= Default OSD backend; raw block device; superior to older FileStore/XFS'))
    lines.append(txt_row())

    return lines


# ── Ceph Architecture ─────────────────────────────────────────────────────────

def ceph_architecture():
    """Ceph Architecture landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Ceph Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph Architecture Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: How It Works (RADOS I/O), Design Standards, Integrations')))
    lines.append(R(bMid(IV_L, IV_R, 'CRUSH: clients compute placement directly; no metadata bottleneck at any scale')))
    lines.append(R(bMid(IV_L, IV_R, 'PG model: each pool divided into PGs; each PG maps to N OSDs via CRUSH rule')))
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
        bMid(B1_L, B1_R, '  RADOS I/O path'),
        bMid(B2_L, B2_R, '  Node/disk sizing'),
        bMid(B3_L, B3_R, '  Kubernetes CSI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  OSD peering model'),
        bMid(B2_L, B2_R, '  Network separation'),
        bMid(B3_L, B3_R, '  OpenStack Cinder'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  CRUSH algorithm'),
        bMid(B2_L, B2_R, '  CRUSH hierarchy'),
        bMid(B3_L, B3_R, '  RGW S3 clients'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Pool types'),
        bMid(B2_L, B2_R, '  Capacity planning'),
        bMid(B3_L, B3_R, '  CephFS NFS export'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines


# ── Ceph Deploy ───────────────────────────────────────────────────────────────

@kb_diagram(
    'ceph-deploy',
    'docs/storage/ceph/deploy/index.md',
    'Ceph deployment — cephadm bootstrap, OSD provisioning, pool creation',
)
def ceph_deploy():
    """Ceph Deploy page — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99

    lines = []
    lines.append(title_border(W2, 'Ceph Deployment'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph Deployment with cephadm')))
    lines.append(R(bMid(IV_L, IV_R, 'cephadm manages Ceph daemons as containers (Podman/Docker)')))
    lines.append(R(bMid(IV_L, IV_R, 'Sequence: bootstrap first MON → add hosts → add MONs → add OSDs → pools')))
    lines.append(R(bMid(IV_L, IV_R, 'Bootstrap: cephadm bootstrap --mon-ip <ip> --cluster-network <CIDR>')))
    lines.append(R(bMid(IV_L, IV_R, 'Validation: HEALTH_OK + all OSDs up+in + PGs all active+clean')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  cephadm   = Ceph Admin tool; deploys and manages Ceph daemons as containers'))
    lines.append(txt_row('  Bootstrap = First command; creates initial MON + MGR on one node'))
    lines.append(txt_row('  noout flag= Prevent OSDs from being marked out during maintenance'))
    lines.append(txt_row())

    return lines


# ── Ceph Operations ───────────────────────────────────────────────────────────

@kb_diagram(
    'ceph-operations',
    'docs/storage/ceph/operations/index.md',
    'Ceph operations landing — health, OSD management, pools, upgrades',
)
def ceph_operations():
    """Ceph Operations landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Ceph Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph Day-2 Operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Six sub-sections: CLI, Health Checks, Procedures, Lifecycle, Backup, Scripts')))
    lines.append(R(bMid(IV_L, IV_R, 'Health baseline: HEALTH_OK + all OSDs up+in + all PGs active+clean')))
    lines.append(R(bMid(IV_L, IV_R, 'Before maintenance: set noout flag; ensure HEALTH_OK before removing flag')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Health'),
        bMid(B2_L, B2_R, 'OSD Management'),
        bMid(B3_L, B3_R, 'Lifecycle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  ceph health detail'),
        bMid(B2_L, B2_R, '  OSD replacement'),
        bMid(B3_L, B3_R, '  cephadm upgrade'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  PG status'),
        bMid(B2_L, B2_R, '  Add/remove nodes'),
        bMid(B3_L, B3_R, '  Upgrade sequence'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Capacity review'),
        bMid(B2_L, B2_R, '  CRUSH rebalance'),
        bMid(B3_L, B3_R, '  RBD mirroring'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines


# ── Ceph Security ─────────────────────────────────────────────────────────────

@kb_diagram(
    'ceph-security',
    'docs/storage/ceph/security/index.md',
    'Ceph security landing — CephX auth, capabilities, encryption, hardening',
)
def ceph_security():
    """Ceph Security landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'Ceph Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph Security Controls')))
    lines.append(R(bMid(IV_L, IV_R, 'Four sub-sections: Access Control (CephX), Authentication, Encryption, Hardening')))
    lines.append(R(bMid(IV_L, IV_R, 'CephX: all clients require a key; granular capabilities per pool/service')))
    lines.append(R(bMid(IV_L, IV_R, 'Encryption: dmcrypt at OSD level; msgr2 secure for in-transit encryption')))
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
        bMid(B1_L, B1_R, '  CephX shared-secret auth'),
        bMid(B2_L, B2_R, '  OSD dmcrypt encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Capability per pool/service'),
        bMid(B2_L, B2_R, '  RBD per-image encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  profile rbd preset'),
        bMid(B2_L, B2_R, '  RGW SSE-S3 / SSE-KMS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Key rotation (manual)'),
        bMid(B2_L, B2_R, '  msgr2 secure mode'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())

    return lines


# ── Ceph Troubleshooting ──────────────────────────────────────────────────────

@kb_diagram(
    'ceph-troubleshooting',
    'docs/storage/ceph/troubleshooting/index.md',
    'Ceph troubleshooting landing — OSD down, PG stuck, nearfull, escalation',
)
def ceph_troubleshooting():
    """Ceph Troubleshooting landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'Ceph Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Ceph Troubleshooting Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: Common Issues, Diagnostics (logs/health codes), Escalation')))
    lines.append(R(bMid(IV_L, IV_R, 'Start: ceph health detail — every warning has a health code with context')))
    lines.append(R(bMid(IV_L, IV_R, 'Sev 1: any HEALTH_ERR with inactive PGs or cluster full → open case immediately')))
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
        bMid(B1_L, B1_R, '  OSD down'),
        bMid(B2_L, B2_R, '  Health code guide'),
        bMid(B3_L, B3_R, '  Red Hat RHCS cases'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  PG degraded/stuck'),
        bMid(B2_L, B2_R, '  OSD log analysis'),
        bMid(B3_L, B3_R, '  Required data bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Slow requests'),
        bMid(B2_L, B2_R, '  Crash dump review'),
        bMid(B3_L, B3_R, '  Community resources'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Nearfull/Full cluster'),
        bMid(B2_L, B2_R, '  Network diagnostics'),
        bMid(B3_L, B3_R, '  Emergency commands'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines
