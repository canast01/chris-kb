"""
OpenShift diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

# ── OpenShift Root ─────────────────────────────────────────────────────────────

@kb_diagram(
    'openshift',
    'docs/virtualization/openshift/index.md',
    'OpenShift Platform Overview — control plane, etcd, OVN-K, operators',
)
def openshift_root():
    """OpenShift Platform Overview — W=103."""
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
    lines.append(title_border(W2, 'OpenShift Container Platform Overview'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Red Hat OpenShift Container Platform (OCP)')))
    lines.append(R(bMid(IV_L, IV_R, 'Enterprise Kubernetes with RHCOS, OLM operators, and integrated security')))
    lines.append(R(bMid(IV_L, IV_R, 'Control plane: 3 masters, etcd quorum, API server, controller-manager, scheduler')))
    lines.append(R(bMid(IV_L, IV_R, 'Network: OVN-Kubernetes SDN, Routes + Ingress, multi-tenant NetworkPolicy')))
    lines.append(R(bMid(IV_L, IV_R, 'Install: IPI (automated) or UPI (manual); air-gap supported via mirror registry')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Control plane and worker nodes separated; platform managed via Cluster Operators (CO)'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Control Plane'),
        bMid(B2_L, B2_R, 'Worker Nodes'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  3× master (RHCOS)'),
        bMid(B2_L, B2_R, '  Compute workload pods'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  etcd quorum (3 members)'),
        bMid(B2_L, B2_R, '  MachineSet-managed scaling'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  API server (TLS :6443)'),
        bMid(B2_L, B2_R, '  kubelet + CRI-O runtime'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  OAuth server (auth)'),
        bMid(B2_L, B2_R, '  OVN-K pod networking'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(R(connector([PD1, PD2, PD3, PD4])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B3_L, B3_R), bTop(B4_L, B4_R))))
    lines.append(R(merge(
        bMid(B3_L, B3_R, 'Security'),
        bMid(B4_L, B4_R, 'Storage & Registry'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  SCC / PSA enforcement'),
        bMid(B4_L, B4_R, '  ODF / persistent storage'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  RBAC + OAuth/LDAP'),
        bMid(B4_L, B4_R, '  Internal image registry'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  etcd encryption at rest'),
        bMid(B4_L, B4_R, '  Quay (external registry)'),
    )))
    lines.append(R(merge(
        bMid(B3_L, B3_R, '  NetworkPolicy isolation'),
        bMid(B4_L, B4_R, '  StorageClass provisioning'),
    )))
    lines.append(R(merge(bBot(B3_L, B3_R), bBot(B4_L, B4_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  RHCOS    = Red Hat CoreOS; immutable, managed node OS for control plane and workers'))
    lines.append(txt_row('  OLM      = Operator Lifecycle Manager; installs and updates operators from OperatorHub'))
    lines.append(txt_row('  MachineSet= Defines worker node pool; scales nodes via Machine API (IPI only)'))
    lines.append(txt_row('  etcd     = Distributed KV store; cluster state; requires 3 nodes for quorum'))
    lines.append(txt_row('  OVN-K    = OVN-Kubernetes; default SDN since OCP 4.12; replaces OpenShift SDN'))
    lines.append(txt_row('  IPI      = Installer Provisioned Infrastructure; fully automated install'))
    lines.append(txt_row())

    return lines


# ── OpenShift Architecture ─────────────────────────────────────────────────────

@kb_diagram(
    'openshift-architecture',
    'docs/virtualization/openshift/architecture/index.md',
    'OpenShift architecture landing — control plane, design, integrations',
)
def openshift_architecture():
    """OpenShift Architecture landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'OpenShift Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OpenShift Architecture Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: How It Works (internals), Design Standards (sizing/CIDR), Integrations')))
    lines.append(R(bMid(IV_L, IV_R, 'Control plane: etcd quorum + API server + controller-manager + scheduler on RHCOS')))
    lines.append(R(bMid(IV_L, IV_R, 'Operator pattern: platform components self-manage via Cluster Operators (CO reconciliation)')))
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
        bMid(B1_L, B1_R, '  etcd I/O path'),
        bMid(B2_L, B2_R, '  Node sizing rules'),
        bMid(B3_L, B3_R, '  vSphere IPI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  OVN-K data path'),
        bMid(B2_L, B2_R, '  CIDR planning'),
        bMid(B3_L, B3_R, '  LDAP identity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Operator pattern'),
        bMid(B2_L, B2_R, '  StorageClass'),
        bMid(B3_L, B3_R, '  Quay registry'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  MachineSet scaling'),
        bMid(B2_L, B2_R, '  MachineSet config'),
        bMid(B3_L, B3_R, '  ACM / ODF'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines


# ── OpenShift Deploy ──────────────────────────────────────────────────────────

@kb_diagram(
    'openshift-deploy',
    'docs/virtualization/openshift/deploy/index.md',
    'OpenShift deployment — IPI/UPI install, air-gap, post-install validation',
)
def openshift_deploy():
    """OpenShift Deploy page — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'OpenShift Deployment'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OpenShift Installation Methods')))
    lines.append(R(bMid(IV_L, IV_R, 'IPI: installer manages infrastructure (vSphere, AWS, bare-metal); fully automated')))
    lines.append(R(bMid(IV_L, IV_R, 'UPI: admin provisions infra manually; installer only bootstraps the cluster software')))
    lines.append(R(bMid(IV_L, IV_R, 'Air-gap: all images mirrored to internal registry; no internet required during install')))
    lines.append(R(bMid(IV_L, IV_R, 'install-config.yaml: single source of truth for cluster topology and parameters')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IPI Install (Automated)'),
        bMid(B2_L, B2_R, 'UPI Install (Manual)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  openshift-install create cluster'),
        bMid(B2_L, B2_R, '  Provision nodes manually'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Installer creates VMs (vSphere)'),
        bMid(B2_L, B2_R, '  Generate ignition configs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Manages load balancers, DNS'),
        bMid(B2_L, B2_R, '  Bootstrap node → masters'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  MachineAPI for worker scaling'),
        bMid(B2_L, B2_R, '  Manual worker CSR approval'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Recommended for vSphere/cloud'),
        bMid(B2_L, B2_R, '  Required for bare-metal/custom'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Key terms:'))
    lines.append(txt_row('  Bootstrap  = Temporary node that initializes first master; removed after install'))
    lines.append(txt_row('  Ignition   = CoreOS provisioning system; configures RHCOS nodes on first boot'))
    lines.append(txt_row('  CSR        = Certificate Signing Request; workers submit CSRs; admin approves'))
    lines.append(txt_row())

    return lines


# ── OpenShift Operations ──────────────────────────────────────────────────────

@kb_diagram(
    'openshift-operations',
    'docs/virtualization/openshift/operations/index.md',
    'OpenShift operations landing — CLI, health, procedures, upgrades',
)
def openshift_operations():
    """OpenShift Operations landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99
    B4_L, B4_R = 3, 50
    B5_L, B5_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'OpenShift Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OpenShift Day-2 Operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Six sub-sections: CLI, Health Checks, Procedures, Upgrades, Backup, Scripts')))
    lines.append(R(bMid(IV_L, IV_R, 'Health baseline: all COs True/False/False; all nodes Ready; etcd 3 members')))
    lines.append(R(bMid(IV_L, IV_R, 'Upgrades: oc adm upgrade → EUS-to-EUS path for minor version jumps')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2, (B3_L + B3_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Health'),
        bMid(B2_L, B2_R, 'Procedures'),
        bMid(B3_L, B3_R, 'Upgrades'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  oc get co,nodes'),
        bMid(B2_L, B2_R, '  Node drain/uncordon'),
        bMid(B3_L, B3_R, '  oc adm upgrade'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  etcd endpoint health'),
        bMid(B2_L, B2_R, '  MachineSet scaling'),
        bMid(B3_L, B3_R, '  EUS channel path'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  cert rotation check'),
        bMid(B2_L, B2_R, '  Cert rotation'),
        bMid(B3_L, B3_R, '  Version lifecycle'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(R(arrow([(B4_L + B4_R) // 2, (B5_L + B5_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B4_L, B4_R), bTop(B5_L, B5_R))))
    lines.append(R(merge(
        bMid(B4_L, B4_R, 'Backup & Restore'),
        bMid(B5_L, B5_R, 'Scripts'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  etcd snapshot backup'),
        bMid(B5_L, B5_R, '  health-check.sh'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  Restore from etcd snap'),
        bMid(B5_L, B5_R, '  csr-approve.sh'),
    )))
    lines.append(R(merge(
        bMid(B4_L, B4_R, '  OADP / Velero apps'),
        bMid(B5_L, B5_R, '  node-drain.sh'),
    )))
    lines.append(R(merge(bBot(B4_L, B4_R), bBot(B5_L, B5_R))))

    lines.append(txt_row())

    return lines


# ── OpenShift Security ────────────────────────────────────────────────────────

@kb_diagram(
    'openshift-security',
    'docs/virtualization/openshift/security/index.md',
    'OpenShift security landing — RBAC, OAuth, encryption, hardening',
)
def openshift_security():
    """OpenShift Security landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 50
    B2_L, B2_R = 53, 99

    lines = []
    lines.append(title_border(W2, 'OpenShift Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OpenShift Security Controls')))
    lines.append(R(bMid(IV_L, IV_R, 'Four sub-sections: Access Control (RBAC), Authentication, Encryption, Hardening')))
    lines.append(R(bMid(IV_L, IV_R, 'SCC enforcement: default restricted-v2; deny root; drop all capabilities')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC + OAuth: role bindings per namespace; LDAP, HTPasswd, or OIDC identity providers')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(R(arrow([(B1_L + B1_R) // 2, (B2_L + B2_R) // 2])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Identity & Access'),
        bMid(B2_L, B2_R, 'Platform Hardening'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  RBAC Roles + ClusterRoles'),
        bMid(B2_L, B2_R, '  SCC: restricted-v2 default'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  OAuth identity providers'),
        bMid(B2_L, B2_R, '  PSA namespace labels'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  LDAP group sync'),
        bMid(B2_L, B2_R, '  etcd encryption at rest'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Service account tokens'),
        bMid(B2_L, B2_R, '  NetworkPolicy default deny'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Remove kubeadmin secret'),
        bMid(B2_L, B2_R, '  CIS benchmark controls'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R))))

    lines.append(txt_row())

    return lines


# ── OpenShift Troubleshooting ─────────────────────────────────────────────────

@kb_diagram(
    'openshift-troubleshooting',
    'docs/virtualization/openshift/troubleshooting/index.md',
    'OpenShift troubleshooting landing — common issues, diagnostics, escalation',
)
def openshift_troubleshooting():
    """OpenShift Troubleshooting landing — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)

    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 32
    B2_L, B2_R = 35, 64
    B3_L, B3_R = 67, 99

    lines = []
    lines.append(title_border(W2, 'OpenShift Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'OpenShift Troubleshooting Overview')))
    lines.append(R(bMid(IV_L, IV_R, 'Three sub-sections: Common Issues, Diagnostics (must-gather), Escalation (Red Hat)')))
    lines.append(R(bMid(IV_L, IV_R, 'First step: oc get events -A and oc logs <pod> --previous; resolves 90% of issues')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: always attach must-gather; Sev 1 = call Red Hat after opening case')))
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
        bMid(B1_L, B1_R, '  CrashLoopBackOff'),
        bMid(B2_L, B2_R, '  must-gather bundle'),
        bMid(B3_L, B3_R, '  Sev 1–4 definitions'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  ImagePullBackOff'),
        bMid(B2_L, B2_R, '  oc adm inspect'),
        bMid(B3_L, B3_R, '  SOS report per node'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Node NotReady'),
        bMid(B2_L, B2_R, '  etcd diagnostics'),
        bMid(B3_L, B3_R, '  Case data checklist'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  OOMKilled'),
        bMid(B2_L, B2_R, '  Network debug'),
        bMid(B3_L, B3_R, '  TAM escalation path'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, '  Operator Degraded'),
        bMid(B2_L, B2_R, '  Node crictl/kubelet'),
        bMid(B3_L, B3_R, '  access.redhat.com'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())

    return lines
