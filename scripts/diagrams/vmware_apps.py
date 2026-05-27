"""
VMware Apps (Horizon, SRM, Tanzu, vSphere Replication) diagram functions.
Auto-registered via @kb_diagram decorator at import time.
"""
from ._core import (
    kb_diagram, make_helpers, layout,
    row, bTop, bMid, bBot, sections, connector, arrow, title_border, merge,
)

@kb_diagram(
    'horizon',
    'docs/virtualization/vmware/horizon/index.md',
    'Horizon VDI Stack — Connection Server, UAG, desktop pools, App Volumes, DEM',
)
def horizon_stack():
    """VMware Horizon VDI Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Horizon VDI Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Horizon — Virtual Desktop and App Delivery Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server: broker authenticating users and directing them to desktop pools')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG: Unified Access Gateway; external proxy terminating Blast/PCoIP from internet')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pools: instant clone (fast provision), linked clone, or full-clone pools')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes: application layering; real-time delivery via AppStacks and WritableVolumes')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Connection Server brokers sessions · UAG secures external access · pools deliver desktops'))
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
        bMid(B1_L, B1_R, 'Connection Server HA'),
        bMid(B2_L, B2_R, 'Pool: provision+resize'),
        bMid(B3_L, B3_R, 'Smart card + MFA auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG: Blast/PCoIP proxy'),
        bMid(B2_L, B2_R, 'Session: monitor+reset'),
        bMid(B3_L, B3_R, 'UAG: cert + TLS config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Instant clone: parent VM'),
        bMid(B2_L, B2_R, 'App Volumes: AppStack'),
        bMid(B3_L, B3_R, 'DEM: user env policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'ADAM: CS config DB'),
        bMid(B2_L, B2_R, 'Certificate: renew CS'),
        bMid(B3_L, B3_R, 'Blast: protocol lockdown'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'DEM: user profile mgmt'),
        bMid(B2_L, B2_R, 'Events DB: query logs'),
        bMid(B3_L, B3_R, 'Entitlement: AD group'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the brokering stack · Operations manage pools and sessions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Login loop: CS che', 'Horizon events DB', 'CS: services up?', 'GSS + CS log bundl', 'vdmadmin -l'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Black screen: blas', 'UAG edge log', 'UAG: reachable?', 'TAM escalation', 'vdmadmin -A'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pool not provision', 'instant-clone.log', 'Pool: available VMs', 'Collect debug log', 'vdmadmin -n'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['App Volumes not mo', 'AppVolumes.log', 'AppStack: attached?', 'P1: VDI outage', 'vdmadmin -c'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere cluster for VDI VMs · Connection Server Windows VMs · UAG VMs in DMZ · GPU hosts if needed'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server= Windows service brokering user sessions to desktop pools; requires AD membership'))
    lines.append(txt_row('UAG           = Unified Access Gateway; DMZ appliance proxying Blast/PCoIP without VPN'))
    lines.append(txt_row('Desktop pool  = Collection of VMs or RDS hosts assigned to users; persistent or floating'))
    lines.append(txt_row('Instant clone = Fast desktop provision using vmFork; creates linked child from running parent VM'))
    lines.append(txt_row('Linked clone  = Template-based pool sharing a parent snapshot; saves storage vs full clone'))
    lines.append(txt_row('App Volumes   = Application layering; AppStack VMDK attached at login; WritableVolume for user data'))
    lines.append(txt_row('DEM           = Dynamic Environment Manager; user profile and policy management for VDI sessions'))
    lines.append(txt_row('Blast         = VMware display protocol; H.264/H.265; works over HTTPS 443; preferred for WAN'))
    lines.append(txt_row('PCoIP         = PC-over-IP; Teradici display protocol; UDP 4172; good for LAN/graphics'))
    lines.append(txt_row('ADAM          = Active Directory Application Mode; Connection Server internal config database'))
    lines.append(txt_row('Entitlement   = AD user or group granted access to a pool or application in Horizon'))
    lines.append(txt_row('vdmadmin      = Horizon CLI; manage users, entitlements, machines, and Connection Server config'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'tanzu',
    'docs/virtualization/vmware/tanzu/index.md',
    'Tanzu Kubernetes Stack — Supervisor Cluster, TKG, vSphere namespaces, Harbor, TMC',
)
def tanzu_stack():
    """VMware Tanzu Kubernetes Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu Kubernetes Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Tanzu — Enterprise Kubernetes on vSphere')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor Cluster: vSphere-integrated Kubernetes control plane on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'TKG Workload Clusters: tenant Kubernetes clusters provisioned in vSphere namespaces')))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere Namespace: resource boundary per team with CPU/RAM/storage quotas and RBAC')))
    lines.append(R(bMid(IV_L, IV_R, 'Harbor: private OCI-compliant registry; image scanning, replication, content trust')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Supervisor hosts the control plane · namespaces isolate tenants · TKG runs workload clusters'))
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
        bMid(B1_L, B1_R, 'Supervisor: Kubernetes CP'),
        bMid(B2_L, B2_R, 'Cluster: create+upgrade'),
        bMid(B3_L, B3_R, 'RBAC: namespace + cluster'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere namespace: quota'),
        bMid(B2_L, B2_R, 'Harbor: image push/pull'),
        bMid(B3_L, B3_R, 'Network policy: pod L4'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'NSX-T CNI: pod networking'),
        bMid(B2_L, B2_R, 'kubectl + tanzu CLI'),
        bMid(B3_L, B3_R, 'PSA: pod security admit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Harbor: OCI registry'),
        bMid(B2_L, B2_R, 'Carvel: package mgmt'),
        bMid(B3_L, B3_R, 'Image scan: Trivy/Clair'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TMC: multi-cluster mgmt'),
        bMid(B2_L, B2_R, 'TMC: policy + lifecycle'),
        bMid(B3_L, B3_R, 'Audit: API server logs'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines the Kubernetes layers · Operations manage clusters'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster stuck: che', 'kubectl describe', 'Supervisor: healthy', 'GSS + bundle', 'tanzu cluster ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pod pending: no no', 'kubectl get events', 'Nodes: Ready?', 'TAM escalation', 'kubectl get pods -'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image pull: Harbor', 'Harbor harbor.log', 'Harbor: running?', 'Collect API logs', 'tanzu package ls'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['NSX CNI not ready', 'NSX node agent log', 'CNI: pods running?', 'P1: cluster down', 'kubectl get ns'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vSphere + vSAN cluster · NSX-T for pod networking · Harbor VM · management network + workload network'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor Cluster= vSphere-integrated Kubernetes control plane running as ESXi kernel components'))
    lines.append(txt_row('TKG           = Tanzu Kubernetes Grid; tenant Kubernetes clusters deployed from Supervisor'))
    lines.append(txt_row('vSphere Namespace= Resource boundary with CPU/RAM/storage quotas; maps to Kubernetes namespace'))
    lines.append(txt_row('Harbor        = VMware open-source OCI registry; image scanning, replication, and content trust'))
    lines.append(txt_row('TMC           = Tanzu Mission Control; SaaS multi-cluster management, policy, and observability'))
    lines.append(txt_row('Carvel        = Tool suite (kapp, ytt, kbld, imgpkg) for Kubernetes packaging and deployment'))
    lines.append(txt_row('PSA           = Pod Security Admission; Kubernetes enforcer for restricted/baseline/privileged modes'))
    lines.append(txt_row('NSX CNI       = NSX-T container network interface; provides pod networking and policy for TKG'))
    lines.append(txt_row('Content trust = Harbor feature ensuring only signed images can be pulled; uses Notary/cosign'))
    lines.append(txt_row('RBAC          = Kubernetes Role-Based Access Control; ClusterRole, Role, RoleBinding,'))
    lines.append(txt_row('Network policy= Kubernetes L4 firewall rules between pods; enforced by NSX CNI in Tanzu'))
    lines.append(txt_row('tanzu CLI     = kubectl plugin for TKG; cluster create, upgrade, kubeconfig management'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'srm',
    'docs/virtualization/vmware/srm/index.md',
    'Site Recovery Manager Stack — site pair, protection groups, recovery plans, test failover',
)
def srm_stack():
    """VMware Site Recovery Manager Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Site Recovery Manager Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Site Recovery Manager (SRM) — DR Orchestration Platform')))
    lines.append(R(bMid(IV_L, IV_R, 'Site pair: SRM Server at protected site paired with recovery site SRM Server')))
    lines.append(R(bMid(IV_L, IV_R, 'Protection groups: VMs grouped by replication method (vSphere Replication or array-based)')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plans: ordered failover runbook — VM priority, IP mapping, startup scripts')))
    lines.append(R(bMid(IV_L, IV_R, 'Test failover: creates isolated test network bubble; no production impact during DR test')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Site pairing enables recovery · protection groups define scope'))
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
        bMid(B1_L, B1_R, 'SRM Server: per site'),
        bMid(B2_L, B2_R, 'Protection group: create'),
        bMid(B3_L, B3_R, 'RBAC: SRM roles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair: tunnel + cert'),
        bMid(B2_L, B2_R, 'Recovery plan: design'),
        bMid(B3_L, B3_R, 'Network isolation: test'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere Replication: RPO'),
        bMid(B2_L, B2_R, 'Test failover: validate'),
        bMid(B3_L, B3_R, 'TLS: site pair cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array replication: SRA'),
        bMid(B2_L, B2_R, 'Planned migration: exec'),
        bMid(B3_L, B3_R, 'IP customisation: rules'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'IP mapping: prod→DR net'),
        bMid(B2_L, B2_R, 'Reprotect: reverse repl'),
        bMid(B3_L, B3_R, 'Audit: plan exec log'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture pairs sites · Operations execute and test recovery plans · Security governs DR access'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Plan fails: step e', 'SRM support bundle', 'Site pair: connecte', 'GSS + bundle', 'srm-util srmcli'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VR repl lag high', 'VR appliance log', 'VMs protected: yes?', 'TAM escalation', 'srm-util showvms'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Test cleanup stuck', 'recovery-plan.log', 'Test: cleanup OK?', 'Collect SRM log', 'srm-util plans'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['IP remap not appli', 'IP customisation c', 'IP map: configured?', 'P1: DR event', 'srm-util history'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('SRM VM at protected site · SRM VM at recovery site · replication network · vCenter at each site'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRM Server    = Windows service (or VA) managing protection groups and recovery plans'))
    lines.append(txt_row('Site pair     = Trusted connection between two SRM Servers; established via certificate exchange'))
    lines.append(txt_row('Protection group= Set of VMs replicated together; associated with one or more recovery plans'))
    lines.append(txt_row('Recovery plan = Ordered failover script: VM priority groups, startup delays, IP mappings, scripts'))
    lines.append(txt_row('Test failover = Validates recovery plan; VMs start in isolated network; no production impact'))
    lines.append(txt_row('Planned migration= Controlled move of workloads to recovery site; apps shut down cleanly at source'))
    lines.append(txt_row('Reprotect     = Reverses replication direction after failover; makes DR site the new protected site'))
    lines.append(txt_row('vSphere Replication= Built-in VM replication engine; RPO 5 minutes or more; host-based delta sync'))
    lines.append(txt_row('SRA           = Storage Replication Adapter; plugin allowing SRM to use array-based replication'))
    lines.append(txt_row('IP customisation= Rules mapping VM IP addresses from production subnet to recovery site subnet'))
    lines.append(txt_row('Test bubble   = Isolated network created during test failover; VMs boot but cannot reach production'))
    lines.append(txt_row('RPO           = Recovery Point Objective; maximum acceptable data loss; drives replication frequency'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'vsphere-replication',
    'docs/virtualization/vmware/vsphere-replication/index.md',
    'vSphere Replication Stack — VRMS, HBRSVC, delta sync, RPO, MPIT, failover/failback',
)
def vsphere_replication_stack():
    """vSphere Replication Stack — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication Stack'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware vSphere Replication — VM-Level Asynchronous Replication')))
    lines.append(R(bMid(IV_L, IV_R, 'VR Server (VRMS): appliance per site managing replication config and site pairing')))
    lines.append(R(bMid(IV_L, IV_R, 'Delta sync: only changed disk blocks transmitted; compressed over replication network')))
    lines.append(R(bMid(IV_L, IV_R, 'RPO: configurable 5 min to 24 hours per VM; drives how often delta syncs occur')))
    lines.append(R(bMid(IV_L, IV_R, 'MPIT: Multiple Point-In-Time snapshots at target; retain recovery points for rollback')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  VR Server pairs sites · HBRSVC on ESXi sends deltas · RPO and MPIT control recovery options'))
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
        bMid(B1_L, B1_R, 'VRMS: site pair + config'),
        bMid(B2_L, B2_R, 'Configure: VM + RPO'),
        bMid(B3_L, B3_R, 'RBAC: VR roles in vCenter'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBRSVC: ESXi repl agent'),
        bMid(B2_L, B2_R, 'Monitor: lag + bandwidth'),
        bMid(B3_L, B3_R, 'TLS: site pair cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Delta sync: block-level'),
        bMid(B2_L, B2_R, 'MPIT: snapshot at target'),
        bMid(B3_L, B3_R, 'Encryption: in-transit'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO: 5 min to 24 hrs'),
        bMid(B2_L, B2_R, 'Failover: planned / forced'),
        bMid(B3_L, B3_R, 'Quiescing: app-consistent'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Seed: initial full copy'),
        bMid(B2_L, B2_R, 'Failback: reprotect VM'),
        bMid(B3_L, B3_R, 'Audit: vCenter events'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Architecture defines replication data path · Operations monitor and execute failover'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Common Issues', 'Diagnostics', 'Health Checks', 'Escalation', 'CLI Quick Ref'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Repl lag exceeds R', 'VRMS appliance log', 'RPO: met for all VM', 'GSS + bundle', 'vicfg-module VR'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Sync stuck at 0%', 'HBRSVC log on host', 'Site pair: connecte', 'TAM escalation', 'hbr-manager stat'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Full sync triggere', 'vr-transfer.log', 'Bandwidth: adequate', 'Collect VR logs', 'esxcli vr config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['MPIT: snapshot err', 'target-datastore l', 'MPIT: captured OK?', 'P1: repl loss', 'vr-manager status'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('VRMS appliance at each site · ESXi hosts running HBRSVC · replication network (dedicated or shared)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VRMS          = vSphere Replication Management Server; per-site VA; manages config and site pair'))
    lines.append(txt_row('HBRSVC        = Host-Based Replication Service; ESXi kernel module transmitting VM disk deltas'))
    lines.append(txt_row('Delta sync    = Incremental block-level replication; only changed disk regions are transmitted'))
    lines.append(txt_row('RPO           = Recovery Point Objective; minimum sync frequency; 5 min, 1 hr, or up to 24 hrs'))
    lines.append(txt_row('MPIT          = Multiple Point-In-Time; snapshots of replicated VM at target site for rollback'))
    lines.append(txt_row('Seed          = Initial full-copy replication; can be seeded from backup media to reduce WAN transfer'))
    lines.append(txt_row('Quiescing     = VSS/sync quiesce of VM guest before snapshot for application-consistent recovery'))
    lines.append(txt_row('Failover      = Powered-on recovery of replicated VM at target site; planned (clean) or forced'))
    lines.append(txt_row('Failback      = After failover: reprotect from recovery site back to original protected site'))
    lines.append(txt_row('Replication lag= Time between a change at source and its arrival at target; must stay under RPO'))
    lines.append(txt_row('Site pair     = VRMS-to-VRMS trust established via certificate exchange; required for replication'))
    lines.append(txt_row('Compression   = vSphere Replication compresses delta blocks in transit; reduces WAN bandwidth'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'horizon-architecture',
    'docs/virtualization/vmware/horizon/architecture/index.md',
    'Horizon Architecture — Connection Server, UAG, Blast/PCoIP, App Volumes, DEM, pools',
)
def horizon_architecture():
    """Horizon Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'VMware Horizon = Connection Servers (HA pair+) + Unified Access Gateway (UAG) in DMZ')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pools: instant clone (fast refresh) or full clone; RDS for published applications')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes delivers applications on-demand; Dynamic Environment Manager controls user settings')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG in DMZ proxies Blast Extreme and PCoIP protocols; Connection Server authenticates users')))
    lines.append(R(bMid(IV_L, IV_R, 'vGPU (NVIDIA) profiles attached to pools for 3D/graphics workloads; vCenter manages ESXi pools')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines broker and pool mechanics · integrations connect directory and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Connection Server HA'),
        bMid(B2_L, B2_R, 'vCenter/ESXi pools'),
        bMid(B3_L, B3_R, '≥2 CS per pod'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG: DMZ proxy'),
        bMid(B2_L, B2_R, 'Active Directory'),
        bMid(B3_L, B3_R, 'UAG in DMZ'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Desktop pools'),
        bMid(B2_L, B2_R, 'WS1 Access SSO'),
        bMid(B3_L, B3_R, 'vGPU profile size'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RDS: pub apps'),
        bMid(B2_L, B2_R, 'NSX microseg'),
        bMid(B3_L, B3_R, 'Pool quota'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'App Volumes'),
        bMid(B2_L, B2_R, 'vGPU (NVIDIA)'),
        bMid(B3_L, B3_R, 'Image mgmt std'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Dyn Env Mgr'),
        bMid(B2_L, B2_R, 'Horizon Cloud'),
        bMid(B3_L, B3_R, 'RDS session lim'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers broker and pools · integrations connect vCenter and directory'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Connection Svr', 'vCenter pools', '≥2 CS per pod', 'Single pod', 'CS sizing'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['UAG reverse proxy', 'Active Directory', 'UAG in DMZ', 'Multi-pod', 'Pool quota'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Instant clone', 'WS1 Access', 'vGPU profiles', 'Cloud pod', 'Image std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['App Volumes', 'NSX microseg', 'RDS limits', 'Enterprise', 'Session limit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards (NVIDIA) · RAM DIMMs · Network NICs · UAG appliance VMs · vCenter'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker VM; authenticates users, entitles desktops, manages sessions'))
    lines.append(txt_row('UAG (Unified Access Gateway) = DMZ reverse proxy for Blast/PCoIP; replaces Security Server'))
    lines.append(txt_row('Instant clone      = Desktop provisioning method; child VMs forked from parent snapshot at login'))
    lines.append(txt_row('Full clone         = Independent desktop VM cloned from template; persists independently'))
    lines.append(txt_row('RDS (Remote Desktop Services) = Windows Server role publishing apps or desktops via Horizon'))
    lines.append(txt_row('App Volumes        = On-demand application delivery using AppStacks mounted at login'))
    lines.append(txt_row('Dynamic Environment Manager = Per-user Windows settings and policy management for Horizon desktops'))
    lines.append(txt_row('Blast Extreme      = VMware display protocol; optimized for LAN and WAN; supports H.264/H.265'))
    lines.append(txt_row('PCoIP              = PC-over-IP protocol; Teradici-based display protocol supported by Horizon'))
    lines.append(txt_row('vGPU               = NVIDIA virtual GPU; shared GPU profile assigned to desktop pool VMs'))
    lines.append(txt_row('Cloud Pod Architecture = Horizon feature linking multiple pods for global entitlements across sites'))
    lines.append(txt_row('Entitlement        = Assignment of a user or group to a Horizon desktop or application pool'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'horizon-operations',
    'docs/virtualization/vmware/horizon/operations/index.md',
    'Horizon Operations — pod health, pool management, composer recompose, upgrade',
)
def horizon_operations():
    """Horizon Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server health monitoring; active session count and session management daily')))
    lines.append(R(bMid(IV_L, IV_R, 'Desktop pool provisioning and recompose; image management and push to instant clone pools')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes assignment per user or group; log review and event DB monitoring for errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade Connection Server first, then UAG, then push agent via pool recompose')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: PowerCLI Horizon module, REST API, Provisioning API for at-scale pool management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops track sessions and pool health · lifecycle upgrades CS first'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CS health check'),
        bMid(B2_L, B2_R, 'Horizon upgrades'),
        bMid(B3_L, B3_R, 'PowerCLI Horizon'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Active sessions'),
        bMid(B2_L, B2_R, 'CS upgrade 1st'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pool provision'),
        bMid(B2_L, B2_R, 'UAG upgrade'),
        bMid(B3_L, B3_R, 'Provisioning API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Composer status'),
        bMid(B2_L, B2_R, 'Agent via recomp'),
        bMid(B3_L, B3_R, 'Connection API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image push'),
        bMid(B2_L, B2_R, 'App Vol upgrade'),
        bMid(B3_L, B3_R, 'LDAP query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Log review'),
        bMid(B2_L, B2_R, 'Add new CS'),
        bMid(B3_L, B3_R, 'Dashboard API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch session and pool issues · lifecycle upgrades in order'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['REST API', 'CS: running', 'Pool recompose', 'CS upgrade 1st', 'Event DB bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI Hor', 'Sessions: ok', 'Image push', 'UAG upgrade', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP query', 'UAG: healthy', 'App Vol assign', 'Agent recomp', 'CS config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Event DB query', 'Pool: ready', 'User reset', 'Post-upg val', 'Restore config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker; health monitored via vCenter plugin and Horizon Admin console'))
    lines.append(txt_row('UAG                = Unified Access Gateway; DMZ proxy; upgrade after Connection Server upgrade'))
    lines.append(txt_row('Desktop pool       = Group of Horizon desktops provisioned from a parent image or template'))
    lines.append(txt_row('Recompose          = Horizon operation pushing a new parent image to all instant clone pool desktops'))
    lines.append(txt_row('Instant clone      = Pool type where desktops are forked from a live parent VM snapshot'))
    lines.append(txt_row('App Volumes        = Application delivery layer; AppStacks assigned per user, group, or OU'))
    lines.append(txt_row('Dynamic Environment Manager = User environment and settings roaming for Horizon virtual desktops'))
    lines.append(txt_row('vGPU profile       = NVIDIA vGPU slice assigned to a VM; profile determines VRAM allocation'))
    lines.append(txt_row('Event database     = Horizon SQL database logging all session, admin, and provisioning events'))
    lines.append(txt_row('REST API           = Horizon REST API for pool, session, and entitlement management at scale'))
    lines.append(txt_row('Horizon agent      = Software installed in guest OS; communicates with Connection Server'))
    lines.append(txt_row('Image management   = Process of updating parent VM, taking snapshot, and recomposing pool'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'horizon-security',
    'docs/virtualization/vmware/horizon/security/index.md',
    'Horizon Security — UAG smart card, AD auth, TLS, RBAC, Blast encryption',
)
def horizon_security():
    """Horizon Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Active Directory authentication; MFA via RSA SecurID/RADIUS or SAML with Workspace ONE')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management for Connection Servers and UAG; Horizon RBAC for entitlements')))
    lines.append(R(bMid(IV_L, IV_R, 'Blast Extreme and PCoIP traffic encrypted with TLS 1.2+; smart card auth supported')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG performs certificate passthrough; Connection Server validates AD credentials and MFA')))
    lines.append(R(bMid(IV_L, IV_R, 'App Volumes and DEM file encryption; USB policy enforces device restriction per pool')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates user access · RBAC controls entitlements'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD auth primary'),
        bMid(B2_L, B2_R, 'Horizon RBAC'),
        bMid(B3_L, B3_R, 'Blast TLS 1.2+'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RSA/RADIUS MFA'),
        bMid(B2_L, B2_R, 'AD group entitle'),
        bMid(B3_L, B3_R, 'PCoIP TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SAML/WS1 SSO'),
        bMid(B2_L, B2_R, 'Pool permissions'),
        bMid(B3_L, B3_R, 'Cert CS/UAG'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Smart card auth'),
        bMid(B2_L, B2_R, 'Global admin role'),
        bMid(B3_L, B3_R, 'App Vol cert'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert-based auth'),
        bMid(B2_L, B2_R, 'Help desk role'),
        bMid(B3_L, B3_R, 'DEM file encr'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG passthrough'),
        bMid(B2_L, B2_R, 'Audit events'),
        bMid(B3_L, B3_R, 'USB policy'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who connects · access control limits entitlements'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD auth', 'RBAC entitle', 'Blast TLS', 'Cert rotation', 'CS event log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RSA MFA', 'Pool access', 'PCoIP TLS', 'MFA enforce', 'Session audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SAML/WS1', 'Admin role', 'CS/UAG cert', 'Smart card', 'UAG access log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Smart card', 'Help desk role', 'App Vol cert', 'Lockout policy', 'Entitle audit'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · RSA/MFA server · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blast Extreme      = VMware display protocol; encrypted with TLS 1.2+; supports H.264 and H.265'))
    lines.append(txt_row('PCoIP              = PC-over-IP display protocol; TLS-encrypted tunnel between client and UAG'))
    lines.append(txt_row('UAG (Unified Access Gateway) = DMZ proxy performing cert passthrough and MFA pre-authentication'))
    lines.append(txt_row('RSA SecurID        = RADIUS-based MFA token server integrated with Connection Server'))
    lines.append(txt_row('SAML               = Security Assertion Markup Language; enables WS1 Access SSO for Horizon'))
    lines.append(txt_row('Smart card auth    = PIV/CAC card authentication via Connection Server or UAG'))
    lines.append(txt_row('Connection Server certificate = TLS cert on CS for Blast/PCoIP and admin UI; must be CA-signed'))
    lines.append(txt_row('Entitlement        = Assignment of AD user or group to a Horizon desktop or application pool'))
    lines.append(txt_row('RBAC               = Role-Based Access Control in Horizon Admin console; admin, helpdesk, auditor'))
    lines.append(txt_row('Help desk role     = Horizon RBAC role allowing session management without pool administration'))
    lines.append(txt_row('DEM (Dynamic Environment Manager) = User settings manager; supports file encryption for profiles'))
    lines.append(txt_row('Session audit      = Horizon event DB records all session start, disconnect, and logoff events'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'horizon-troubleshooting',
    'docs/virtualization/vmware/horizon/troubleshooting/index.md',
    'Horizon Troubleshooting — black screen, provisioning errors, UAG, log bundle',
)
def horizon_troubleshooting():
    """Horizon Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'Horizon — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Connection Server failures; desktop not starting or stuck in provisioning state')))
    lines.append(R(bMid(IV_L, IV_R, 'Blast/PCoIP protocol latency; session disconnects; pool provisioning errors')))
    lines.append(R(bMid(IV_L, IV_R, 'UAG certificate issues; vGPU driver issues; App Volumes mount failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: Horizon events DB, /opt/vmware/hzn logs, UAG admin UI, esxtop for vGPU')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: collect Horizon log bundle and UAG support bundle; open GSS case with TAM')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define the triage path · diagnostics isolate the layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CS fail/down'),
        bMid(B2_L, B2_R, 'Horizon events DB'),
        bMid(B3_L, B3_R, 'Horizon log bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Desktop stuck'),
        bMid(B2_L, B2_R, '/opt/vmware/hzn'),
        bMid(B3_L, B3_R, 'UAG support bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Blast/PCoIP lag'),
        bMid(B2_L, B2_R, 'UAG admin UI'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Session disconn'),
        bMid(B2_L, B2_R, 'esxtop vGPU'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pool prov err'),
        bMid(B2_L, B2_R, 'App Vol log'),
        bMid(B3_L, B3_R, 'Event DB query'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'UAG cert err'),
        bMid(B2_L, B2_R, 'DCT tool'),
        bMid(B3_L, B3_R, 'RCA template'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics pinpoint root cause'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CS down', 'Events DB', '/opt/vmware/hzn', 'Horizon bundle', 'Restart CS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Desktop stuck', 'UAG admin UI', '/var/log/vmware', 'GSS P1 case', 'Recompose pool'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Blast/PCoIP lag', 'esxtop vGPU', 'UAG /var/log', 'TAM escalate', 'Check MTU/QoS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Pool prov err', 'DCT tool', 'App Vol logs', 'Event DB query', 'Re-prov pool'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 ESXi hosts · GPU cards · RAM DIMMs · Network NICs · UAG VMs · vCenter · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server  = Horizon broker; if down no new sessions; check Windows service and event log'))
    lines.append(txt_row('UAG                = Unified Access Gateway; cert issues cause client connection failures'))
    lines.append(txt_row('Desktop pool       = Group of desktops; stuck provisioning may indicate snapshot or vCenter error'))
    lines.append(txt_row('Instant clone provisioning = Fork operation from parent VM; fails if parent snapshot is stale'))
    lines.append(txt_row('Blast Extreme      = Display protocol; lag indicates MTU, QoS, or bandwidth constraint'))
    lines.append(txt_row('PCoIP              = Display protocol; session drops often tied to UDP port blockage or MTU'))
    lines.append(txt_row('vGPU               = NVIDIA virtual GPU; driver mismatch causes display or performance failures'))
    lines.append(txt_row('DCT (Desktop Connectivity Tool) = Horizon diagnostic tool for end-to-end session connectivity'))
    lines.append(txt_row('Horizon events database = SQL DB logging all session and admin events; query for error codes'))
    lines.append(txt_row('Recompose          = Operation to push new image to pool desktops; resolves stuck provisioning'))
    lines.append(txt_row('Log bundle         = Horizon diagnostic package collected from Connection Server for GSS'))
    lines.append(txt_row('TAM escalation     = Technical Account Manager escalation for critical production incidents'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'srm-architecture',
    'docs/virtualization/vmware/srm/architecture/index.md',
    'SRM Architecture — site pair, SRA, protection groups, recovery plans, IP customisation',
)
def srm_architecture():
    """SRM Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Site Recovery Manager = SRM server pair (one per site) + protection groups (VM sets)')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plans are ordered runbooks: test / planned migration / failover workflows')))
    lines.append(R(bMid(IV_L, IV_R, 'Uses vSphere Replication or array-based replication for data movement between sites')))
    lines.append(R(bMid(IV_L, IV_R, 'Inventory mappings connect protected site resources to recovery site equivalents')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX network remapping automates IP customization during failover or planned migration')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines replication and runbooks · integrations connect vCenter and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM server pair'),
        bMid(B2_L, B2_R, 'vCenter pair sites'),
        bMid(B3_L, B3_R, 'RTO/RPO per VM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Protection groups'),
        bMid(B2_L, B2_R, 'NSX: net remap'),
        bMid(B3_L, B3_R, 'PG granularity'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plans'),
        bMid(B2_L, B2_R, 'vSAN+SAN replic'),
        bMid(B3_L, B3_R, 'Net mapping'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test failover'),
        bMid(B2_L, B2_R, 'AD auth'),
        bMid(B3_L, B3_R, 'DS mapping'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Planned migration'),
        bMid(B2_L, B2_R, 'Aria Ops monitor'),
        bMid(B3_L, B3_R, 'IP customization'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Inventory maps'),
        bMid(B2_L, B2_R, 'Array API'),
        bMid(B3_L, B3_R, 'Test schedule'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers replication and recovery plans · integrations connect sites'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM server pair', 'vCenter pair', 'RTO/RPO tiers', '2-site setup', 'PG naming'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Protection grps', 'NSX net remap', 'PG granularity', 'Bi-directional', 'RPO policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery plans', 'vSAN/SAN replic', 'Net mapping', 'Active-passive', 'IP custom std'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Test failover', 'Array API', 'IP customization', 'Active-active', 'Test schedule'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · Shared storage or vSAN · Network uplinks · WAN/DCI link'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SRM server         = Site Recovery Manager appliance; one per site; paired across protected and'))
    lines.append(txt_row('Protection group   = Logical set of VMs grouped for replication and recovery together'))
    lines.append(txt_row('Recovery plan      = Ordered runbook of steps executed during test, migration, or failover'))
    lines.append(txt_row('Test failover      = Non-disruptive recovery validation in an isolated network; production unaffected'))
    lines.append(txt_row('Planned migration  = Controlled workload move from protected to recovery site; no data loss'))
    lines.append(txt_row('Failover           = Emergency activation of recovery site after protected site failure'))
    lines.append(txt_row('Reprotect          = Reverses replication direction after failover to enable failback'))
    lines.append(txt_row('Inventory mapping  = Maps protected site resource (network, folder, pool) to recovery site equivalent'))
    lines.append(txt_row('Network mapping    = SRM mapping of protected site port group to recovery site port group'))
    lines.append(txt_row('Datastore mapping  = Maps protected datastore to recovery site datastore for VM registration'))
    lines.append(txt_row('IP customization   = SRM rules that change VM IP/gateway/DNS during failover to recovery network'))
    lines.append(txt_row('RPO (Recovery Point Objective) = Maximum acceptable data loss; drives replication frequency'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'srm-operations',
    'docs/virtualization/vmware/srm/operations/index.md',
    'SRM Operations — test failover, planned migration, reprotect, failback, upgrade',
)
def srm_operations():
    """SRM Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Replication status and RPO compliance monitoring; protection group health checks daily')))
    lines.append(R(bMid(IV_L, IV_R, 'Test failover on schedule; recovery plan validation; planned migration for maintenance')))
    lines.append(R(bMid(IV_L, IV_R, 'Reprotect after failover to restore replication in reverse direction for failback')))
    lines.append(R(bMid(IV_L, IV_R, 'Lifecycle: upgrade SRM on both sites; run pre-checks; validate partner compatibility')))
    lines.append(R(bMid(IV_L, IV_R, 'Automation: SRM REST API, PowerCLI SRM, PG API, Recovery plan API for at-scale ops')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor RPO and PG health · lifecycle upgrades both sites'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication status'),
        bMid(B2_L, B2_R, 'SRM upgrades both'),
        bMid(B3_L, B3_R, 'SRM REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO compliance'),
        bMid(B2_L, B2_R, 'Appliance mode'),
        bMid(B3_L, B3_R, 'PowerCLI SRM'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PG health'),
        bMid(B2_L, B2_R, 'Pre-check run'),
        bMid(B3_L, B3_R, 'PG API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plan'),
        bMid(B2_L, B2_R, 'Partner compat'),
        bMid(B3_L, B3_R, 'Recovery plan API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test schedule'),
        bMid(B2_L, B2_R, 'Test post-upg'),
        bMid(B3_L, B3_R, 'Test API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Alert review'),
        bMid(B2_L, B2_R, 'HBCR agent upg'),
        bMid(B3_L, B3_R, 'Inventory map API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops catch RPO breaches early · lifecycle upgrades both sites together'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM REST API', 'Replic: ok', 'Test failover', 'SRM upg both', 'SRM config bk'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PowerCLI SRM', 'RPO: compliant', 'Planned migr', 'HBCR upg', 'Recovery plan'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PG API', 'PG: healthy', 'Reprotect', 'Pre-check run', 'Mapping backup'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery API', 'Test: passed', 'IP custom', 'Post-upg val', 'Restore config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · vSAN/SAN storage · WAN/DCI link · Network connectivity'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Protection group   = Set of VMs replicated and recovered together; health monitored daily'))
    lines.append(txt_row('Recovery plan      = Ordered runbook; validated by test failover before a real event'))
    lines.append(txt_row('Test failover      = Isolated recovery validation; confirms plan works without impacting production'))
    lines.append(txt_row('Planned migration  = Zero-RPO controlled site move for scheduled maintenance or evacuation'))
    lines.append(txt_row('Failover           = Emergency activation of recovery site; may have data loss up to RPO'))
    lines.append(txt_row('Reprotect          = Post-failover operation that reverses replication to enable failback'))
    lines.append(txt_row('RPO compliance     = Monitoring that replication lag stays within the configured RPO threshold'))
    lines.append(txt_row('HBCR (Host-Based Changed Block Replication) = vSphere Replication agent on ESXi hosts'))
    lines.append(txt_row('SRM REST API       = REST interface for automating protection group and recovery plan operations'))
    lines.append(txt_row('PowerCLI SRM       = PowerShell cmdlets for SRM automation: plan execution, PG management'))
    lines.append(txt_row('Inventory mapping  = Config object linking protected site resources to recovery site equivalents'))
    lines.append(txt_row('Partner site       = The paired remote site in an SRM configuration; protected or recovery role'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'srm-security',
    'docs/virtualization/vmware/srm/security/index.md',
    'SRM Security — vCenter SSO, RBAC, TLS site pair, SRA authentication, audit',
)
def srm_security():
    """SRM Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter SSO for SRM authentication; site pair credentials for cross-site trust')))
    lines.append(R(bMid(IV_L, IV_R, 'RBAC roles: admin / recovery execute / test operator / read-only for least privilege')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management for SRM servers; array replication auth; audit log for all ops')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication traffic encrypted with TLS; vSAN encryption at rest for DR datastores')))
    lines.append(R(bMid(IV_L, IV_R, 'Test isolation network prevents recovery test VMs from reaching production systems')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication controls SRM access · RBAC scopes recovery roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO auth'),
        bMid(B2_L, B2_R, 'SRM admin: full'),
        bMid(B3_L, B3_R, 'Replic TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'AD integration'),
        bMid(B2_L, B2_R, 'Recovery exec'),
        bMid(B3_L, B3_R, 'Array replic auth'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'SRM admin role'),
        bMid(B2_L, B2_R, 'Test exec only'),
        bMid(B3_L, B3_R, 'SRM cert mgmt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair creds'),
        bMid(B2_L, B2_R, 'Read-only audit'),
        bMid(B3_L, B3_R, 'Test isolation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array creds'),
        bMid(B2_L, B2_R, 'Custom roles'),
        bMid(B3_L, B3_R, 'vSAN encr DR'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert management'),
        bMid(B2_L, B2_R, 'vCenter RBAC'),
        bMid(B3_L, B3_R, 'Audit log TLS'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls who uses SRM · RBAC limits recovery execution'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'SRM admin', 'Replic TLS', 'Cert rotation', 'Recovery audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['AD integration', 'Recovery exec', 'Array auth', 'Site pair cert', 'Test log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site pair creds', 'Test exec', 'SRM cert', 'Least privilege', 'Plan changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Array creds', 'Read-only', 'vSAN encr', 'Isolation net', 'GSS audit trail'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (SRM VMs both sites) · vSAN/SAN · WAN link · AD domain · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter SSO        = Single Sign-On; SRM authenticates all users via vCenter SSO domain'))
    lines.append(txt_row('Site pair          = Trusted connection between two SRM servers across protected and recovery sites'))
    lines.append(txt_row('Array-based replication = Storage array replicates LUNs/volumes; SRM integrates via SRA adapter'))
    lines.append(txt_row('vSphere Replication = Host-based replication using HBCR agent; RPO minimum 5 minutes'))
    lines.append(txt_row('SRM RBAC           = Role-Based Access Control in SRM; roles: admin, recovery exec, test, read-only'))
    lines.append(txt_row('Recovery admin     = SRM role with full recovery plan and protection group management'))
    lines.append(txt_row('Recovery user      = SRM role that can execute recovery plans but not modify them'))
    lines.append(txt_row('Test operator      = SRM role that can run test failovers only; cannot run real failover'))
    lines.append(txt_row('Certificate management = SRM server TLS cert lifecycle; must be CA-signed for site pair trust'))
    lines.append(txt_row('Audit log          = SRM records all recovery, test, reprotect, and admin operations'))
    lines.append(txt_row('Test isolation network = Isolated port group used during test failover; blocks production access'))
    lines.append(txt_row('Least privilege    = Principle of assigning minimum SRM role needed for each operator function'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'srm-troubleshooting',
    'docs/virtualization/vmware/srm/troubleshooting/index.md',
    'SRM Troubleshooting — site pair failure, plan errors, replication issues, log bundle',
)
def srm_troubleshooting():
    """SRM Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'SRM — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Site pair connectivity failures; replication lag and RPO breaches; PG config errors')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plan execution failures; array API connectivity issues; HBCR agent failures')))
    lines.append(R(bMid(IV_L, IV_R, 'Diagnostics: SRM log files, VR appliance log, array API test, RPO dashboard review')))
    lines.append(R(bMid(IV_L, IV_R, 'Recovery plan test identifies misconfigurations before a real failover event occurs')))
    lines.append(R(bMid(IV_L, IV_R, 'Escalation: collect SRM bundles from both sites; engage array vendor; contact TAM for P1')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues define triage path · diagnostics isolate replication or plan layer'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair conn'),
        bMid(B2_L, B2_R, 'SRM log files'),
        bMid(B3_L, B3_R, 'SRM bndl both'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replic lag/RPO'),
        bMid(B2_L, B2_R, 'VR appliance log'),
        bMid(B3_L, B3_R, 'GSS P1 case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'PG config err'),
        bMid(B2_L, B2_R, 'Array API test'),
        bMid(B3_L, B3_R, 'Both site logs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Recovery plan fail'),
        bMid(B2_L, B2_R, 'Recovery plan test'),
        bMid(B3_L, B3_R, 'Array vendor esc'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Array API err'),
        bMid(B2_L, B2_R, 'RPO dashboard'),
        bMid(B3_L, B3_R, 'TAM contact'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'HBCR agent fail'),
        bMid(B2_L, B2_R, 'Support bundle'),
        bMid(B3_L, B3_R, 'P1 process'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use logs and RPO dashboard'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site pair fail', 'SRM log files', '/var/log/vmware/srm', 'SRM bundle', 'Re-pair sites'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Replic lag', 'RPO dashboard', 'VR app /logs', 'GSS P1 case', 'Resync data'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['PG config err', 'Recovery test', '/var/log/hms', 'Array vendor', 'Fix PG config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Recovery fail', 'Array API test', '/var/log/vr', 'TAM contact', 'Plan dry run'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 servers (both sites) · vSAN/SAN · WAN/DCI link · Array storage · AD domain'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Site pair          = Trusted link between SRM servers; failure blocks all SRM operations cross-site'))
    lines.append(txt_row('RPO breach         = Replication lag exceeds configured RPO threshold; alerts in SRM dashboard'))
    lines.append(txt_row('Protection group   = VM set in SRM; config error prevents inclusion in recovery plans'))
    lines.append(txt_row('Recovery plan      = Ordered failover runbook; execution failures logged with step-level detail'))
    lines.append(txt_row('HBCR agent         = Host-Based Changed Block Replication agent; failure stops vSphere Replication'))
    lines.append(txt_row('Array-based replication = Array LUN replication via SRA; API errors block SRM inventory sync'))
    lines.append(txt_row('SRM support bundle = Log package from SRM appliance; collected from both sites for GSS cases'))
    lines.append(txt_row('VR appliance log   = vSphere Replication appliance logs; diagnose HBCR and replication failures'))
    lines.append(txt_row('TAM escalation     = Technical Account Manager escalation for P1 DR incidents'))
    lines.append(txt_row('Test failover      = Non-disruptive test; use to validate plan config before real event'))
    lines.append(txt_row('Reprotect          = Post-failover step; reverses replication; required before failback'))
    lines.append(txt_row('Recovery time      = Actual elapsed time of recovery plan execution; compare against RTO target'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'tanzu-architecture',
    'docs/virtualization/vmware/tanzu/architecture/index.md',
    'Tanzu Architecture — Supervisor Cluster, TKGs/TKGm, Cluster API, NSX-T, Harbor, TMC',
)
def tanzu_architecture():
    """Tanzu Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu portfolio: TKGs (Supervisor Cluster on vSphere) + TKGm (standalone management cluster)')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor Cluster: vSphere control plane enabling Kubernetes namespaces on ESXi hosts')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload clusters: Tanzu Kubernetes clusters provisioned via Cluster API on vSphere')))
    lines.append(R(bMid(IV_L, IV_R, 'NSX-T or VDS networking: pod networking, load balancing via NSX Advanced LB (Avi)')))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu Mission Control: multi-cluster governance, policy, and lifecycle management plane')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines supervisor and workload clusters · integrations connect NSX and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Supervisor cluster'),
        bMid(B2_L, B2_R, 'NSX-T networking'),
        bMid(B3_L, B3_R, 'Namespace sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Workload clusters'),
        bMid(B2_L, B2_R, 'Avi load balancer'),
        bMid(B3_L, B3_R, 'Cluster profiles'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere namespaces'),
        bMid(B2_L, B2_R, 'vSAN storage'),
        bMid(B3_L, B3_R, 'Image policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster API'),
        bMid(B2_L, B2_R, 'Harbor registry'),
        bMid(B3_L, B3_R, 'Network config'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'TKG node pools'),
        bMid(B2_L, B2_R, 'TMC governance'),
        bMid(B3_L, B3_R, 'RBAC namespaces'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Control plane HA'),
        bMid(B2_L, B2_R, 'vCenter auth'),
        bMid(B3_L, B3_R, 'Resource quota'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers supervisor + workload clusters · integrations connect NSX and Harbor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Supervisor cluster', 'NSX-T network', 'Namespace sizing', 'Single cluster', 'Namespace policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Workload clusters', 'Avi LB', 'Cluster profile', 'HA control plane', 'Image policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere namespace', 'vSAN storage', 'RBAC namespaces', 'Multi-cluster', 'Quota policy'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster API', 'Harbor registry', 'Resource quota', 'TMC governed', 'Network config'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN or NFS storage · NSX-T or VDS virtual switch fabric'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor Cluster  = vSphere control plane running Kubernetes API server on ESXi host kernel'))
    lines.append(txt_row('TKGs               = Tanzu Kubernetes Grid Service; provisions workload clusters via Supervisor'))
    lines.append(txt_row('TKGm               = Tanzu Kubernetes Grid multicloud; standalone management cluster on any infra'))
    lines.append(txt_row('vSphere namespace   = Kubernetes namespace mapped to vSphere resource pool, storage policy, and'))
    lines.append(txt_row('Workload cluster   = Tanzu Kubernetes cluster provisioned in a namespace via Cluster API'))
    lines.append(txt_row('Cluster API        = Kubernetes-native API for declarative lifecycle management of workload clusters'))
    lines.append(txt_row('Node pool          = Group of identically sized worker nodes within a Tanzu Kubernetes cluster'))
    lines.append(txt_row('Control plane HA   = 3 control plane nodes per cluster across ESXi hosts for Kubernetes API HA'))
    lines.append(txt_row('Avi Load Balancer  = NSX Advanced LB (Avi); provides L4/L7 load balancing for Tanzu services'))
    lines.append(txt_row('Harbor             = VMware container registry; private image registry integrated with Tanzu'))
    lines.append(txt_row('Tanzu Mission Ctrl = SaaS management plane for multi-cluster policy, RBAC, and lifecycle governance'))
    lines.append(txt_row('Resource quota     = vSphere namespace CPU, memory, storage limits enforced across all cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'tanzu-operations',
    'docs/virtualization/vmware/tanzu/operations/index.md',
    'Tanzu Operations — cluster lifecycle, node pool scaling, upgrade, Harbor, Tanzu CLI',
)
def tanzu_operations():
    """Tanzu Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster lifecycle: provision, scale, and upgrade workload clusters via kubectl or Tanzu CLI')))
    lines.append(R(bMid(IV_L, IV_R, 'Node pool management: add/remove workers; drain nodes before maintenance operations')))
    lines.append(R(bMid(IV_L, IV_R, 'Supervisor health: check vCenter Workload Management status; validate namespace quotas')))
    lines.append(R(bMid(IV_L, IV_R, 'Image management: scan and promote images in Harbor; enforce OPA/admission policies')))
    lines.append(R(bMid(IV_L, IV_R, 'Tanzu CLI: tanzu cluster create/delete/upgrade/scale; kubeconfig context management')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops manage cluster state · lifecycle upgrades Kubernetes versions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster status'),
        bMid(B2_L, B2_R, 'Cluster upgrade'),
        bMid(B3_L, B3_R, 'Tanzu CLI'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node pool scale'),
        bMid(B2_L, B2_R, 'K8s version bump'),
        bMid(B3_L, B3_R, 'kubectl apply'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Namespace quotas'),
        bMid(B2_L, B2_R, 'Node drain/cordon'),
        bMid(B3_L, B3_R, 'GitOps pipelines'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image scanning'),
        bMid(B2_L, B2_R, 'Supervisor upg'),
        bMid(B3_L, B3_R, 'TMC automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Harbor registry'),
        bMid(B2_L, B2_R, 'OVA bundle upg'),
        bMid(B3_L, B3_R, 'Cluster API CR'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'kubeconfig mgmt'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'Helm deploys'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops check cluster and node health · lifecycle upgrades Kubernetes safely'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['tanzu cluster', 'Cluster: Running', 'Scale workers', 'Cluster upgrade', 'kubeconfig bkp'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['kubectl apply', 'Nodes: Ready', 'Add namespace', 'Supervisor upg', 'ETCD snapshot'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['kubectl drain', 'Quotas: ok', 'Update quota', 'OVA bundle', 'Cluster config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['tanzu login', 'Harbor: healthy', 'Image promote', 'Post-upg val', 'Namespace bkp'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Tanzu CLI          = kubectl plug-in and tanzu binary for cluster lifecycle and context management'))
    lines.append(txt_row('tanzu cluster      = CLI sub-command for create, scale, upgrade, delete of workload clusters'))
    lines.append(txt_row('Node drain         = kubectl drain removes pods from a node before maintenance or upgrade'))
    lines.append(txt_row('Node pool scaling  = Adding or removing worker VMs in a pool via Cluster API update'))
    lines.append(txt_row('Supervisor upgrade = vCenter-driven update of the Workload Management control plane version'))
    lines.append(txt_row('OVA bundle         = Tanzu node OS image OVA; uploaded to vCenter content library for upgrades'))
    lines.append(txt_row('kubeconfig         = Kubernetes configuration file with cluster endpoint and credentials for kubectl'))
    lines.append(txt_row('Namespace quota    = CPU/memory/storage limits applied to a vSphere namespace; enforced by Supervisor'))
    lines.append(txt_row('Cluster API CR     = Custom Resource defining desired cluster state; reconciled by Cluster API'))
    lines.append(txt_row('GitOps pipeline    = Declarative deployment pipeline applying manifests from git to Kubernetes'))
    lines.append(txt_row('Harbor             = VMware OCI-compatible registry; image scanning and replication built-in'))
    lines.append(txt_row('ETCD snapshot      = Backup of Kubernetes cluster state; taken before any major upgrade operation'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'tanzu-security',
    'docs/virtualization/vmware/tanzu/security/index.md',
    'Tanzu Security — vSphere SSO, RBAC, Pod Security Admission, NSX-T policies, mTLS',
)
def tanzu_security():
    """Tanzu Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere SSO and LDAP/AD integration for Kubernetes RBAC; namespace-scoped role bindings')))
    lines.append(R(bMid(IV_L, IV_R, 'Pod Security Admission: enforce Restricted/Baseline/Privileged policies per namespace')))
    lines.append(R(bMid(IV_L, IV_R, 'Network policies via NSX-T: micro-segmentation between pods and namespaces')))
    lines.append(R(bMid(IV_L, IV_R, 'Harbor image scanning: Trivy/Clair CVE scanning; admission webhook rejects vulnerable images')))
    lines.append(R(bMid(IV_L, IV_R, 'mTLS between services via Tanzu Service Mesh (TSM); certificate rotation automated')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Authentication gates cluster access · RBAC scopes namespace permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Workload Security'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vSphere SSO'),
        bMid(B2_L, B2_R, 'RBAC bindings'),
        bMid(B3_L, B3_R, 'Pod Security Adm'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP/AD groups'),
        bMid(B2_L, B2_R, 'Namespace RBAC'),
        bMid(B3_L, B3_R, 'Network policy'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'OIDC provider'),
        bMid(B2_L, B2_R, 'Service accounts'),
        bMid(B3_L, B3_R, 'Image scanning'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'kubeconfig auth'),
        bMid(B2_L, B2_R, 'Cluster roles'),
        bMid(B3_L, B3_R, 'mTLS (TSM)'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cert rotation'),
        bMid(B2_L, B2_R, 'OPA/Gatekeeper'),
        bMid(B3_L, B3_R, 'Admission webhook'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Audit logging'),
        bMid(B2_L, B2_R, 'TMC policies'),
        bMid(B3_L, B3_R, 'vSAN encryption'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Auth controls cluster access · RBAC scopes roles'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Workload Sec', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere SSO', 'RBAC roles', 'Pod Sec Adm', 'CIS k8s bench', 'API audit log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'Namespace RBAC', 'Network policy', 'PSA Restricted', 'RBAC changes'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['OIDC provider', 'Cluster roles', 'Image scanning', 'Cert rotation', 'Harbor scan log'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Service accounts', 'OPA policies', 'mTLS TSM', 'Min-priv SA', 'Admission log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · NSX-T fabric · vSAN encryption · CA infrastructure'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vSphere SSO        = vCenter Single Sign-On; identity source for Kubernetes RBAC in Tanzu'))
    lines.append(txt_row('RBAC               = Kubernetes Role-Based Access Control; ClusterRole/Role bound to users or groups'))
    lines.append(txt_row('Pod Security Adm   = Kubernetes built-in policy enforcing Restricted/Baseline/Privileged per'))
    lines.append(txt_row('Network policy     = Kubernetes resource restricting pod-to-pod traffic; enforced by NSX-T CNI'))
    lines.append(txt_row('OPA/Gatekeeper     = Open Policy Agent admission controller; enforces custom policy constraints'))
    lines.append(txt_row('Admission webhook  = Kubernetes API hook that validates or mutates resources before admission'))
    lines.append(txt_row('Image scanning     = Harbor Trivy/Clair CVE scan; blocks deployment of images above severity'))
    lines.append(txt_row('mTLS               = Mutual TLS between services; provided by Tanzu Service Mesh (Istio-based)'))
    lines.append(txt_row('OIDC               = OpenID Connect; used by Pinniped to federate identity to Kubernetes API server'))
    lines.append(txt_row('Service account    = Kubernetes identity for pods; scoped to namespace; used for API server auth'))
    lines.append(txt_row('vSAN encryption    = Data-at-rest encryption for node disks; uses vCenter Key Provider (KMS)'))
    lines.append(txt_row('Kubernetes audit   = API server audit log capturing all API calls; forwarded to Aria Logs for SIEM'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'tanzu-troubleshooting',
    'docs/virtualization/vmware/tanzu/troubleshooting/index.md',
    'Tanzu Troubleshooting — cluster stuck, node NotReady, WCP degraded, tanzu diagnostics',
)
def tanzu_troubleshooting():
    """Tanzu Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'VMware Tanzu — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Cluster creation stuck: check Supervisor status in vCenter; validate NSX-T and storage config')))
    lines.append(R(bMid(IV_L, IV_R, 'Nodes NotReady: check kubelet status on node; verify vSAN/network connectivity from node VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Workload Management degraded: validate vCenter health, vSphere namespace quota, and NTP sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Image pull failures: check Harbor availability; verify imagePullSecret and network policy')))
    lines.append(R(bMid(IV_L, IV_R, 'kubectl logs and describe events are first diagnostic step; tanzu diagnostics collects bundles')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues guide triage · diagnostics use kubectl and events · escalation bundles for VMware GSS'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Cluster stuck'),
        bMid(B2_L, B2_R, 'kubectl describe'),
        bMid(B3_L, B3_R, 'tanzu diagnostics'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Node NotReady'),
        bMid(B2_L, B2_R, 'kubectl logs'),
        bMid(B3_L, B3_R, 'GSS case'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'WCP degraded'),
        bMid(B2_L, B2_R, 'kubectl events'),
        bMid(B3_L, B3_R, 'Skyline Health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Image pull fail'),
        bMid(B2_L, B2_R, 'vCenter events'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pod pending'),
        bMid(B2_L, B2_R, 'NSX-T logs'),
        bMid(B3_L, B3_R, 'Log bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Quota exceeded'),
        bMid(B2_L, B2_R, 'Harbor health'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage cluster and node faults · diagnostics use kubectl and vCenter'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Cluster stuck', 'kubectl descr', 'vCenter tasks', 'tanzu diagnos', 'Re-provision'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Node NotReady', 'kubectl logs', 'kubelet journal', 'GSS P1 case', 'Drain+replace'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['WCP degraded', 'kubectl events', 'NSX-T manager', 'TAM escalate', 'Restart WCP'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Image pull fail', 'Harbor health', 'Harbor logs', 'Skyline health', 'Update secret'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('ESXi hosts · RAM DIMMs · Network NICs · vSAN/NFS storage · NSX-T fabric · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Supervisor status  = Workload Management health shown in vCenter UI; Running/Degraded/Error states'))
    lines.append(txt_row('Node NotReady      = Kubernetes node condition when kubelet cannot communicate with API server'))
    lines.append(txt_row('kubelet            = Node agent managing pod lifecycle; check journalctl -u kubelet for errors'))
    lines.append(txt_row('WCP                = Workload Control Plane; VMware internal name for the Supervisor Cluster'))
    lines.append(txt_row('kubectl describe   = Shows detailed state and events for any Kubernetes resource'))
    lines.append(txt_row('kubectl events     = Lists recent events in a namespace; critical for cluster and pod triage'))
    lines.append(txt_row('imagePullSecret    = Kubernetes secret holding registry credentials for pulling private images'))
    lines.append(txt_row('tanzu diagnostics  = CLI command collecting cluster diagnostic bundle for GSS escalation'))
    lines.append(txt_row('Pod Pending        = Pod scheduled but not running; check events for resource or image pull errors'))
    lines.append(txt_row('Quota exceeded     = vSphere namespace CPU/memory/storage limit reached; expand or reclaim resources'))
    lines.append(txt_row('Skyline Health     = VMware proactive support tool validating Tanzu configuration against best'))
    lines.append(txt_row('Cluster API events = Events on TanzuKubernetesCluster CR showing provisioning error details'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'vsphere-replication-architecture',
    'docs/virtualization/vmware/vsphere-replication/architecture/index.md',
    'vSphere Replication Architecture — VRMS/VRS per site, per-VMDK RPO, SRM integration',
)
def vsphere_replication_architecture():
    """vSphere Replication Architecture sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Architecture'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vSphere Replication (VR): per-VM async replication from source vCenter to target vCenter')))
    lines.append(R(bMid(IV_L, IV_R, 'VR appliance (VRMS) per site; VR server (VRS) handles bulk of replication traffic per site')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication granularity: per-VMDK; RPO configurable from 5 minutes to 24 hours per VM')))
    lines.append(R(bMid(IV_L, IV_R, 'Network compression and encryption of replication traffic; FQDN-resolved endpoints')))
    lines.append(R(bMid(IV_L, IV_R, 'Site Recovery Manager integration: VR seeds VM copies used for SRM orchestrated failover')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works defines VR appliances · integrations connect SRM · standards govern RPO and sizing'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'How It Works'),
        bMid(B2_L, B2_R, 'Integrations'),
        bMid(B3_L, B3_R, 'Design Standards'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS per site'),
        bMid(B2_L, B2_R, 'SRM integration'),
        bMid(B3_L, B3_R, 'RPO per VM class'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRS per site'),
        bMid(B2_L, B2_R, 'vCenter plugin'),
        bMid(B3_L, B3_R, 'Bandwidth sizing'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Per-VMDK rep'),
        bMid(B2_L, B2_R, 'Storage compat'),
        bMid(B3_L, B3_R, 'Encryption on'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO 5 min-24 hr'),
        bMid(B2_L, B2_R, 'vSAN as target'),
        bMid(B3_L, B3_R, 'Compression on'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Traffic encrypt'),
        bMid(B2_L, B2_R, 'NFS/VMFS target'),
        bMid(B3_L, B3_R, 'Max VMs per VRS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Delta sync'),
        bMid(B2_L, B2_R, 'Aria Ops intg'),
        bMid(B3_L, B3_R, 'FQDN config'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  How-it-works covers VR appliances and RPO · integrations connect SRM and storage'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['How It Works', 'Integrations', 'Design Stds', 'Deployment', 'Key Stds'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS per site', 'SRM pairing', 'RPO tiers', 'VRMS deploy', 'RPO per class'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRS per site', 'vCenter plugin', 'BW planning', 'VRS deploy', 'Encrypt traffic'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Per-VMDK rep', 'vSAN target', 'Compress on', 'Site pairing', 'Max VM/VRS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Delta sync', 'NFS/VMFS tgt', 'FQDN config', 'Multi-VRS', 'Storage policy'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link for replication traffic · Target storage (vSAN/NFS/VMFS)'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('VRMS               = vSphere Replication Management Server; registers with vCenter; manages'))
    lines.append(txt_row('VRS                = vSphere Replication Server; handles the bulk replication data transfer per site'))
    lines.append(txt_row('Per-VMDK replication = Each virtual disk replicated independently; exclude swap VMDKs to save'))
    lines.append(txt_row('RPO                = Recovery Point Objective; minimum 5 minutes in VR; defines max data loss window'))
    lines.append(txt_row('Delta sync         = Changed block tracking (CBT) used to send only modified blocks each replication'))
    lines.append(txt_row('Site pairing       = vCenter-level trust relationship between source and target VR sites'))
    lines.append(txt_row('Replication target = Datastore on target site where replica VMDK files are stored'))
    lines.append(txt_row('Traffic encryption = TLS-encrypted replication stream between source VRS and target VRS'))
    lines.append(txt_row('Compression        = Network compression of replication data; reduces bandwidth at cost of CPU'))
    lines.append(txt_row('SRM integration    = Site Recovery Manager uses VR as the replication provider for orchestrated'))
    lines.append(txt_row('vSAN target        = vSAN datastore on target site used as replication destination; policy-based'))
    lines.append(txt_row('Changed block track = CBT bitmap tracking written blocks in a VMDK; enables efficient delta'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'vsphere-replication-operations',
    'docs/virtualization/vmware/vsphere-replication/operations/index.md',
    'vSphere Replication Operations — RPO monitoring, pause/resume, test recovery, upgrade',
)
def vsphere_replication_operations():
    """vSphere Replication Operations sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Operations'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Monitor replication status for all protected VMs; check RPO compliance and missed sync counts')))
    lines.append(R(bMid(IV_L, IV_R, 'Configure replication: select VM, set RPO, choose target datastore and network compression')))
    lines.append(R(bMid(IV_L, IV_R, 'Pause and resume replication: maintenance window operations; resume to trigger full delta sync')))
    lines.append(R(bMid(IV_L, IV_R, 'Test recovery: recover to isolated test network; validate VM boots at target; revert test')))
    lines.append(R(bMid(IV_L, IV_R, 'Appliance upgrades: upgrade VRMS and VRS before upgrading protected VMs and vCenter hosts')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops monitor RPO compliance · lifecycle upgrades appliances before hosts · automation via SRM'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Daily Ops'),
        bMid(B2_L, B2_R, 'Lifecycle'),
        bMid(B3_L, B3_R, 'Automation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO compliance'),
        bMid(B2_L, B2_R, 'VRMS upgrade'),
        bMid(B3_L, B3_R, 'SRM plans'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Missed sync'),
        bMid(B2_L, B2_R, 'VRS upgrade'),
        bMid(B3_L, B3_R, 'REST API'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Rep health'),
        bMid(B2_L, B2_R, 'Cert rotation'),
        bMid(B3_L, B3_R, 'Aria Ops alerts'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Pause/resume'),
        bMid(B2_L, B2_R, 'vCenter upg'),
        bMid(B3_L, B3_R, 'Scheduled test'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Test recovery'),
        bMid(B2_L, B2_R, 'Config backup'),
        bMid(B3_L, B3_R, 'VR API calls'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'BW utilisation'),
        bMid(B2_L, B2_R, 'Post-upg val'),
        bMid(B3_L, B3_R, 'Monitoring API'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Daily ops track RPO and sync health · lifecycle upgrades appliances · automation tests and alerts'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CLI Ref', 'Health Chk', 'Procedures', 'Install/Up', 'Backup/Rest'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VR REST API', 'RPO: met', 'Configure VM', 'VRMS upgrade', 'Config export'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vSphere API', 'Sync: ok', 'Pause rep', 'VRS upgrade', 'Rep metadata'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['SRM API', 'BW: normal', 'Resume rep', 'Cert rotation', 'Restore config'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Aria Ops API', 'Appliance: up', 'Test recovery', 'Post-upg val', 'Site re-pair'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Target storage array or vSAN · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('RPO compliance     = All replicated VMs meeting their configured RPO within the monitoring window'))
    lines.append(txt_row('Missed sync        = Replication cycle that failed to complete within the RPO window; alerts in'))
    lines.append(txt_row('Pause replication  = Temporarily halting delta sync; all changes accumulate until resumed'))
    lines.append(txt_row('Resume replication = Restarting replication after pause; triggers full delta resync of changed blocks'))
    lines.append(txt_row('Test recovery      = Recovering replica to isolated test network; validates DR readiness without'))
    lines.append(txt_row('Bandwidth usage    = Network throughput consumed by replication; monitored to prevent link saturation'))
    lines.append(txt_row('VRMS upgrade       = OVF/VAMI-based upgrade of the management appliance; must precede VRS upgrade'))
    lines.append(txt_row('VRS upgrade        = Upgrade of the replication server appliance; precedes vCenter and host upgrades'))
    lines.append(txt_row('Configuration backup = Export of VR replication config; used for recovery if appliance rebuild needed'))
    lines.append(txt_row('Site pairing health = vCenter-to-vCenter VR trust relationship; must be green for replication to'))
    lines.append(txt_row('SRM recovery plan  = Orchestrated failover workflow that uses VR replicas as recovery source'))
    lines.append(txt_row('VR REST API        = HTTP API for querying and managing replication config programmatically'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'vsphere-replication-security',
    'docs/virtualization/vmware/vsphere-replication/security/index.md',
    'vSphere Replication Security — vCenter SSO, RBAC, TLS traffic, cert management, FIPS',
)
def vsphere_replication_security():
    """vSphere Replication Security sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Security'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'vCenter SSO authentication for VR appliance management; RBAC via vCenter roles')))
    lines.append(R(bMid(IV_L, IV_R, 'Replication traffic encrypted over TLS between source VRS and target VRS')))
    lines.append(R(bMid(IV_L, IV_R, 'Certificate management: VRMS and VRS certs signed by CA or vCenter CA; rotated on schedule')))
    lines.append(R(bMid(IV_L, IV_R, 'Firewall rules: VRMS port 8043/443, VRS port 31031, vCenter port 443 between sites')))
    lines.append(R(bMid(IV_L, IV_R, 'Audit: all replication config changes logged in vCenter Tasks and Events; syslog forward')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  vCenter SSO gates management · TLS encrypts replication traffic'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Authentication'),
        bMid(B2_L, B2_R, 'Access Control'),
        bMid(B3_L, B3_R, 'Encryption'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'vCenter SSO'),
        bMid(B2_L, B2_R, 'vCenter RBAC'),
        bMid(B3_L, B3_R, 'Traffic TLS'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'LDAP via vCenter'),
        bMid(B2_L, B2_R, 'Admin role'),
        bMid(B3_L, B3_R, 'Cert management'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS local admin'),
        bMid(B2_L, B2_R, 'Read-only role'),
        bMid(B3_L, B3_R, 'CA-signed certs'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Plugin auth'),
        bMid(B2_L, B2_R, 'Datastore perm'),
        bMid(B3_L, B3_R, 'FIPS mode'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site trust cert'),
        bMid(B2_L, B2_R, 'Site admin roles'),
        bMid(B3_L, B3_R, 'Compress+encrypt'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VAMI local auth'),
        bMid(B2_L, B2_R, 'Firewall rules'),
        bMid(B3_L, B3_R, 'Audit logging'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  SSO controls management access · RBAC scopes permissions'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Auth', 'Access Ctrl', 'Encryption', 'Hardening', 'Audit'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['vCenter SSO', 'vCenter RBAC', 'Traffic TLS', 'Cert rotation', 'vCenter tasks'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['LDAP groups', 'Admin role', 'CA-signed cert', 'Firewall rules', 'Config events'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS local', 'Read-only role', 'FIPS mode', 'Min-perm RBAC', 'Syslog forward'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Site trust cert', 'Firewall scope', 'Compress+enc', 'VAMI hardening', 'Site pair log'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN firewall · CA infrastructure · vCenter appliance'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vCenter SSO        = Single Sign-On; authenticates admin access to VR plugin within vCenter UI'))
    lines.append(txt_row('RBAC               = Role-Based Access Control; VR uses vCenter roles for permissions scoping'))
    lines.append(txt_row('Admin role         = Full VR management: configure, pause, resume, reconfigure replication'))
    lines.append(txt_row('Read-only role     = View replication status only; cannot configure or modify replication'))
    lines.append(txt_row('Traffic encryption = TLS between source and target VRS; enabled by default; FIPS mode optional'))
    lines.append(txt_row('VRMS certificate   = TLS cert for the VRMS management UI; signed by vCenter CA or external CA'))
    lines.append(txt_row('VRS certificate    = TLS cert for the VRS data path; must be trusted at both source and target sites'))
    lines.append(txt_row('Site trust         = Certificate-based trust between source vCenter and target vCenter for VR pairing'))
    lines.append(txt_row('VAMI               = Virtual Appliance Management Interface; admin UI for VRMS/VRS; secured with'))
    lines.append(txt_row('Firewall rules     = Required: 8043/443 for VRMS, 31031 for VRS data, 443 for vCenter communication'))
    lines.append(txt_row('Audit log          = All VR config changes logged in vCenter Tasks/Events; forwarded via syslog to'))
    lines.append(txt_row('FIPS 140-2         = Federal cryptographic standard; enabled for VR traffic encryption at cluster'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines

@kb_diagram(
    'vsphere-replication-troubleshooting',
    'docs/virtualization/vmware/vsphere-replication/troubleshooting/index.md',
    'vSphere Replication Troubleshooting — rep failures, RPO violations, CBT, VAMI bundle',
)
def vsphere_replication_troubleshooting():
    """vSphere Replication Troubleshooting sub-section — W=103."""
    W2 = 103
    R, txt_row = make_helpers(W2)
    IV_L, IV_R = 3, 99
    B1_L, B1_R = 3, 33
    B2_L, B2_R = 36, 66
    B3_L, B3_R = 69, 99
    M1, M2, M3 = 18, 51, 84
    PD1, PD2, PD3, PD4 = 22, 41, 61, 80
    lines = []

    lines.append(title_border(W2, 'vSphere Replication — Troubleshooting'))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(bMid(IV_L, IV_R, 'Replication failing: verify firewall rules on ports 443, 8043, 31031; check site pairing cert')))
    lines.append(R(bMid(IV_L, IV_R, 'RPO violations: check available WAN bandwidth; review missed sync count in VR monitor')))
    lines.append(R(bMid(IV_L, IV_R, 'VR appliance unreachable: verify VRMS/VRS VM is powered on; check VAMI service status')))
    lines.append(R(bMid(IV_L, IV_R, 'CBT issues: reset CBT on VM via snapshot cycle; required after hardware change events')))
    lines.append(R(bMid(IV_L, IV_R, 'Collect support bundle from VRMS VAMI; attach to VMware GSS case with vCenter logs')))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage network and appliance faults · diagnostics use logs and VAMI'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(merge(bTop(B1_L, B1_R), bTop(B2_L, B2_R), bTop(B3_L, B3_R))))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Common Issues'),
        bMid(B2_L, B2_R, 'Diagnostics'),
        bMid(B3_L, B3_R, 'Escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Replication fail'),
        bMid(B2_L, B2_R, 'vCenter events'),
        bMid(B3_L, B3_R, 'VRMS bundle'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'RPO violation'),
        bMid(B2_L, B2_R, 'VAMI health'),
        bMid(B3_L, B3_R, 'GSS case open'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'VRMS unreachable'),
        bMid(B2_L, B2_R, 'VR monitor UI'),
        bMid(B3_L, B3_R, 'vCenter log bndl'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'CBT corruption'),
        bMid(B2_L, B2_R, '/var/log/vmware/vr'),
        bMid(B3_L, B3_R, 'TAM escalation'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Site pair fail'),
        bMid(B2_L, B2_R, 'Firewall test'),
        bMid(B3_L, B3_R, 'Skyline health'),
    )))
    lines.append(R(merge(
        bMid(B1_L, B1_R, 'Disk space target'),
        bMid(B2_L, B2_R, 'Cert validity'),
        bMid(B3_L, B3_R, 'Version compat'),
    )))
    lines.append(R(merge(bBot(B1_L, B1_R), bBot(B2_L, B2_R), bBot(B3_L, B3_R))))

    lines.append(txt_row())
    lines.append(txt_row('  Common issues triage replication faults · diagnostics use VAMI and VR monitor'))
    lines.append(txt_row())
    lines.append(R(arrow([M1, M2, M3])))
    lines.append(txt_row())

    lines.append(R(bTop(IV_L, IV_R)))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Issues', 'Diagnostics', 'Log Paths', 'Escalation', 'Recovery'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['Rep failing', 'vCenter events', '/var/log/vmware/vr', 'VRMS bundle', 'Re-configure'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['RPO violated', 'VAMI health pg', '/var/log/hms', 'GSS P1 case', 'Reduce RPO'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['VRMS down', 'VR monitor UI', '/var/log/vmware', 'TAM escalate', 'Restart VRMS'])))
    lines.append(R(sections(IV_L, IV_R, [PD1, PD2, PD3, PD4],
        ['CBT issue', 'Firewall test', 'VRMS syslog', 'Skyline health', 'Reset CBT'])))
    lines.append(R(bBot(IV_L, IV_R)))

    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('x86 VMs (VRMS + VRS) · RAM DIMMs · WAN link · Firewall between sites · Target datastore'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Replication failure = VR sync cycle did not complete; check vCenter events for error code and source'))
    lines.append(txt_row('RPO violation      = Missed sync count > 0 in VR monitor; investigate bandwidth or appliance health'))
    lines.append(txt_row('CBT               = Changed Block Tracking; bitmap tracking VMDK changes; corruption causes resync'))
    lines.append(txt_row('CBT reset          = Snapshot + delete cycle on a VM to force CBT bitmap rebuild; triggers full'))
    lines.append(txt_row('VAMI               = Virtual Appliance Management Interface; check service status and disk usage here'))
    lines.append(txt_row('VR Monitor UI      = vCenter plugin tab showing per-VM replication status, RPO, and last sync time'))
    lines.append(txt_row('Site pairing failure = Lost trust between source/target vCenter; re-pair after certificate change'))
    lines.append(txt_row('Firewall ports     = 443 (vCenter), 8043 (VRMS mgmt), 31031 (VRS data); all required between sites'))
    lines.append(txt_row('VRMS support bundle = Diagnostic archive from VAMI including VR logs; attach to GSS case'))
    lines.append(txt_row('Disk space target  = Insufficient space on target datastore; VR pauses replication until resolved'))
    lines.append(txt_row('Skyline Health     = VMware proactive tool validating VR configuration against known best practices'))
    lines.append(txt_row('Log path           = Primary VR logs at /var/log/vmware/vr/; HMS service logs at /var/log/hms'))
    lines.append(txt_row())

    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-arch-how',
    'docs/virtualization/vmware/horizon/architecture/how-it-works/index.md',
    'VMware Horizon — How It Works',
)
def horizon_arch_how():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — How It Works'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon delivers virtualised desktops and apps via Connection Servers that broker'))
    lines.append(txt_row('sessions between clients and desktop pools or RDS farms.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session Broker Layer'), bMid(L2, R2, 'Desktop & App Layer'))))
    lines.append(R(merge(bMid(L1, R1, 'Connection Server: broker'), bMid(L2, R2, 'Instant clone pools'))))
    lines.append(R(merge(bMid(L1, R1, 'Authenticates via AD'), bMid(L2, R2, 'Full clone pools (persistent)'))))
    lines.append(R(merge(bMid(L1, R1, 'Selects resource from pool'), bMid(L2, R2, 'RDS: App/Desktop farms'))))
    lines.append(R(merge(bMid(L1, R1, 'Blast Extreme: display prot'), bMid(L2, R2, 'GPUs: vGPU pools'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server brokers AD auth then hands session to pool agent on target VM.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Client Layer'), bMid(L2, R2, 'Unified Access Gateway'))))
    lines.append(R(merge(bMid(L1, R1, 'Horizon Client: native app'), bMid(L2, R2, 'UAG: DMZ reverse proxy'))))
    lines.append(R(merge(bMid(L1, R1, 'HTML Access: browser'), bMid(L2, R2, 'Offloads external auth'))))
    lines.append(R(merge(bMid(L1, R1, 'Blast TCP/UDP 8443/443'), bMid(L2, R2, 'SAML to Connection Server'))))
    lines.append(R(merge(bMid(L1, R1, 'PCoIP: legacy protocol'), bMid(L2, R2, 'Dual NIC: internal+external'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Connection Servers run as Windows VMs; desktop VMs run on ESXi hosts with vSAN'))
    lines.append(txt_row('or NFS storage; UAG VMs sit in DMZ with dual-NIC on separate networks.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server= Windows Server VM; Horizon broker and management'))
    lines.append(txt_row('Instant clone   = desktop provisioned in seconds from parent snapshot'))
    lines.append(txt_row('Full clone      = independent persistent VM; slow to provision'))
    lines.append(txt_row('RDS             = Remote Desktop Services; server-based desktop/app'))
    lines.append(txt_row('UAG             = Unified Access Gateway; replaces Security Server'))
    lines.append(txt_row('Blast Extreme   = VMware display protocol; lower latency than PCoIP'))
    lines.append(txt_row('PCoIP           = PC over IP; legacy display protocol; UDP-based'))
    lines.append(txt_row('HTML Access     = browser-based Horizon client; uses WebSocket'))
    lines.append(txt_row('SAML            = assertion from UAG to Connection Server for auth'))
    lines.append(txt_row('vGPU            = NVIDIA GPU partition shared across desktop VMs'))
    lines.append(txt_row('Pool            = collection of desktops with same policy'))
    lines.append(txt_row('Farm            = collection of RDS hosts for app/desktop delivery'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-arch-int',
    'docs/virtualization/vmware/horizon/architecture/integrations/index.md',
    'VMware Horizon — Integrations',
)
def horizon_arch_int():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Integrations'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon integrates with AD for identity, vCenter for VM management, Workspace ONE'))
    lines.append(txt_row('for unified endpoint management, and third-party printing/profile solutions.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Identity & Auth'), bMid(L2, R2, 'Infrastructure'))))
    lines.append(R(merge(bMid(L1, R1, 'Active Directory: required'), bMid(L2, R2, 'vCenter: VM lifecycle'))))
    lines.append(R(merge(bMid(L1, R1, 'RADIUS: MFA integration'), bMid(L2, R2, 'vSAN/NFS: desktop storage'))))
    lines.append(R(merge(bMid(L1, R1, 'RSA/Duo: OTP token'), bMid(L2, R2, 'NSX: micro-seg desktop VLAN'))))
    lines.append(R(merge(bMid(L1, R1, 'Smart card: PIV/CAC'), bMid(L2, R2, 'vSphere HA: pool recovery'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('AD is mandatory; all other integrations are optional but recommended for enterprise.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Workspace ONE Integration'), bMid(L2, R2, 'Profile & Printing'))))
    lines.append(R(merge(bMid(L1, R1, 'W1 Access: SAML gateway'), bMid(L2, R2, 'DEM: profile management'))))
    lines.append(R(merge(bMid(L1, R1, 'W1 UEM: policy + apps'), bMid(L2, R2, 'FSLogix: profile container'))))
    lines.append(R(merge(bMid(L1, R1, 'Digital workspace: unified'), bMid(L2, R2, 'ThinPrint: virtual printing'))))
    lines.append(R(merge(bMid(L1, R1, 'App Volumes: app delivery'), bMid(L2, R2, 'CIFS/NFS: profile share'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('All Horizon components on management network; UAG on DMZ; desktop VMs on'))
    lines.append(txt_row('dedicated VLAN; profile shares on NAS over CIFS/NFS.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Workspace ONE Access= SAML-based app portal; unified access layer'))
    lines.append(txt_row('Workspace ONE UEM  = Unified Endpoint Management; policy/app delivery'))
    lines.append(txt_row('App Volumes        = app delivery via AppStacks; no per-desktop install'))
    lines.append(txt_row('DEM               = Dynamic Environment Manager; profile personalisation'))
    lines.append(txt_row('FSLogix           = Microsoft profile container; VHDX per user on share'))
    lines.append(txt_row('RADIUS            = Multi-Factor Auth backend protocol'))
    lines.append(txt_row('Smart card        = PIV/CAC certificate login; AD smart card auth'))
    lines.append(txt_row('NSX               = micro-segment desktop VMs from each other'))
    lines.append(txt_row('ThinPrint         = virtual printing solution for VDI'))
    lines.append(txt_row('AppStack          = App Volumes package; writable volume or app layer'))
    lines.append(txt_row('SAML gateway      = W1 Access presents SAML to Horizon Connection Server'))
    lines.append(txt_row('CIFS              = file share protocol; desktop profiles stored here'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-arch-design',
    'docs/virtualization/vmware/horizon/architecture/design-standards/index.md',
    'VMware Horizon — Design Standards',
)
def horizon_arch_design():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Design Standards'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon design standards define Connection Server sizing, UAG placement, desktop'))
    lines.append(txt_row('pool type selection, storage tier, and display protocol choices.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Connection Server Sizing'), bMid(L2, R2, 'Pool Design'))))
    lines.append(R(merge(bMid(L1, R1, 'Max 4000 sessions per CS'), bMid(L2, R2, 'Instant clone: non-persist'))))
    lines.append(R(merge(bMid(L1, R1, 'Min 2 CS for HA'), bMid(L2, R2, 'Full clone: persistent desks'))))
    lines.append(R(merge(bMid(L1, R1, '2 UAGs per site minimum'), bMid(L2, R2, 'RDS farm: server-based'))))
    lines.append(R(merge(bMid(L1, R1, 'Replica CS: read-only pod'), bMid(L2, R2, 'vGPU: graphics-intensive'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Instant clone pools for non-persistent; full clone for persistent with profile.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Storage Standards'), bMid(L2, R2, 'Protocol Standards'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN: preferred for pools'), bMid(L2, R2, 'Blast Extreme: default'))))
    lines.append(R(merge(bMid(L1, R1, 'Separate OS from profile'), bMid(L2, R2, 'UDP: Blast over 8443'))))
    lines.append(R(merge(bMid(L1, R1, 'vSAN dedupe: instant clones'), bMid(L2, R2, 'PCoIP: legacy use only'))))
    lines.append(R(merge(bMid(L1, R1, 'Profile: CIFS share or vVol'), bMid(L2, R2, 'HTML5: fallback for browsers'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Desktop ESXi hosts need high RAM (512GB+) and fast storage for pool density;'))
    lines.append(txt_row('Connection Server VMs need 8 vCPU / 32GB RAM per 4000 sessions.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server= Horizon broker; max 4000 concurrent sessions'))
    lines.append(txt_row('Replica CS    = secondary Connection Server; read-only LDAP replica'))
    lines.append(txt_row('UAG           = Unified Access Gateway; external session proxy'))
    lines.append(txt_row('Instant clone = forked from running parent VM in seconds'))
    lines.append(txt_row('Full clone    = independent persistent VM; user-assigned'))
    lines.append(txt_row('RDS farm      = RDSH hosts delivering published apps or desktops'))
    lines.append(txt_row('Blast Extreme = VMware display protocol; adaptive UDP/TCP'))
    lines.append(txt_row('PCoIP         = PC over IP; Teradici protocol; use for legacy clients'))
    lines.append(txt_row('vSAN dedupe   = space savings on instant clone OS disks'))
    lines.append(txt_row('vGPU          = NVIDIA GRID partition; for CAD/graphics VDI'))
    lines.append(txt_row('Profile share = Windows file share for DEM/FSLogix user profiles'))
    lines.append(txt_row('Pod           = group of Connection Servers in same broadcast domain'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-backup',
    'docs/virtualization/vmware/horizon/operations/backup-restore/index.md',
    'VMware Horizon — Backup & Restore',
)
def horizon_ops_backup():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Backup & Restore'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon backup covers the LDAP config database on Connection Servers, golden image'))
    lines.append(txt_row('VMs, and user profile shares; desktop VMs themselves are stateless (instant clone).'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Config Backup'), bMid(L2, R2, 'Golden Image Backup'))))
    lines.append(R(merge(bMid(L1, R1, 'LDAP backup: vdmexport.exe'), bMid(L2, R2, 'VM snapshot before update'))))
    lines.append(R(merge(bMid(L1, R1, 'Schedule: daily minimum'), bMid(L2, R2, 'Clone golden image: pre-push'))))
    lines.append(R(merge(bMid(L1, R1, 'Store: secure file share'), bMid(L2, R2, 'Keep N-1 + N-2 images'))))
    lines.append(R(merge(bMid(L1, R1, 'Include: Events DB backup'), bMid(L2, R2, 'VADP: backup if persistent'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('LDAP backup is most critical; without it Horizon config must be rebuilt manually.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Profile & Restore'), bMid(L2, R2, 'Restore Procedure'))))
    lines.append(R(merge(bMid(L1, R1, 'User profiles: FSLogix/DEM'), bMid(L2, R2, 'Restore LDAP: vdmimport'))))
    lines.append(R(merge(bMid(L1, R1, 'Profile share: daily backup'), bMid(L2, R2, 'Re-register CS: reconnect'))))
    lines.append(R(merge(bMid(L1, R1, 'DEM config: GPO + share'), bMid(L2, R2, 'Rebuild pools from golden'))))
    lines.append(R(merge(bMid(L1, R1, 'AppStack: backup VMDK file'), bMid(L2, R2, 'Validate: test login'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Connection Server VMs should be backed up via VADP as well; profile CIFS share'))
    lines.append(txt_row('must be on backed-up NAS; AppStack VMDKs on backed-up datastore.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vdmexport.exe = Horizon LDAP config export tool; run on Connection Server'))
    lines.append(txt_row('vdmimport     = Horizon LDAP config import; restore from backup'))
    lines.append(txt_row('LDAP          = Horizon stores its config in AD LDS (LDAP store)'))
    lines.append(txt_row('Golden image  = template VM; all instant clones derive from this'))
    lines.append(txt_row('N-1/N-2       = keep two previous golden image versions for rollback'))
    lines.append(txt_row('Events DB     = Horizon event log; SQL Server; backup separately'))
    lines.append(txt_row('FSLogix       = user profile container; VHDX file on CIFS share'))
    lines.append(txt_row('DEM           = Dynamic Environment Manager; policy-based profile'))
    lines.append(txt_row('AppStack      = App Volumes VMDK; contains installed applications'))
    lines.append(txt_row('VADP          = backup API; use for persistent full clone VMs'))
    lines.append(txt_row('CIFS share    = Windows file share; user profile store'))
    lines.append(txt_row('Re-register   = reconnect Connection Server to Horizon pod after restore'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-cli',
    'docs/virtualization/vmware/horizon/operations/cli-reference/index.md',
    'VMware Horizon — CLI Reference',
)
def horizon_ops_cli():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — CLI Reference'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon CLI tools: vdmadmin.exe on Connection Server, PowerCLI Horizon module,'))
    lines.append(txt_row('and the Horizon REST API for automation.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'vdmadmin Commands'), bMid(L2, R2, 'Horizon REST API'))))
    lines.append(R(merge(bMid(L1, R1, 'vdmadmin -L (list sessions)'), bMid(L2, R2, 'POST /rest/login'))))
    lines.append(R(merge(bMid(L1, R1, 'vdmadmin -Q (kiosk mode)'), bMid(L2, R2, 'GET /rest/inventory/v1/farms'))))
    lines.append(R(merge(bMid(L1, R1, 'vdmadmin -A (agent config)'), bMid(L2, R2, 'GET /rest/inventory/v1/pools'))))
    lines.append(R(merge(bMid(L1, R1, 'vdmexport / vdmimport'), bMid(L2, R2, 'DELETE /rest/sessions/{id}'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('vdmadmin runs on Connection Server; REST API requires Horizon admin credentials.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'PowerCLI Horizon'), bMid(L2, R2, 'Desktop & Session Ops'))))
    lines.append(R(merge(bMid(L1, R1, 'Connect-HVServer -Server cs'), bMid(L2, R2, 'Send-HVDesktopReboot'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-HVPool (list pools)'), bMid(L2, R2, 'Disconnect-HVSession'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-HVMachine (list desktops)'), bMid(L2, R2, 'Set-HVPool -Enable'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-HVLocalSession (sessions)'), bMid(L2, R2, 'Remove-HVMachine'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('vdmadmin runs locally on Connection Server; PowerCLI connects from jump host;'))
    lines.append(txt_row('REST API accessible on Connection Server port 443.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('vdmadmin      = Horizon admin CLI; Windows .exe on Connection Server'))
    lines.append(txt_row('vdmexport     = export Horizon LDAP config to backup file'))
    lines.append(txt_row('vdmimport     = import Horizon LDAP config from backup file'))
    lines.append(txt_row('Connect-HVServer= PowerCLI; connect to Horizon Connection Server'))
    lines.append(txt_row('Get-HVPool    = PowerCLI; list all Horizon desktop/app pools'))
    lines.append(txt_row('Get-HVMachine = PowerCLI; list desktop VM status'))
    lines.append(txt_row('REST API      = Horizon REST API; JSON; bearer token auth'))
    lines.append(txt_row('POST /rest/login= obtain session token for REST API'))
    lines.append(txt_row('DELETE /rest/sessions= force disconnect a Horizon session'))
    lines.append(txt_row('Kiosk mode    = shared desktop mode; no user AD account needed'))
    lines.append(txt_row('Agent config  = configure Horizon Agent on desktop VM via vdmadmin'))
    lines.append(txt_row('Remove-HVMachine= PowerCLI; remove a desktop VM from pool'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-health',
    'docs/virtualization/vmware/horizon/operations/health-checks/index.md',
    'VMware Horizon — Health Checks',
)
def horizon_ops_health():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Health Checks'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon health checks verify Connection Server status, pool availability, agent'))
    lines.append(txt_row('health, UAG connectivity, and session counts against licensed capacity.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Connection Server Health'), bMid(L2, R2, 'Pool Health'))))
    lines.append(R(merge(bMid(L1, R1, 'All CS: Connected status'), bMid(L2, R2, 'Available desktops count'))))
    lines.append(R(merge(bMid(L1, R1, 'AD: reachable from all CS'), bMid(L2, R2, 'No pool in error state'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert: not expired on CS'), bMid(L2, R2, 'Provisioning: no stuck VMs'))))
    lines.append(R(merge(bMid(L1, R1, 'Services: all running on CS'), bMid(L2, R2, 'vCenter: connected to pool'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('CS status and pool availability are the primary daily health indicators.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'UAG & Session Health'), bMid(L2, R2, 'Capacity & Performance'))))
    lines.append(R(merge(bMid(L1, R1, 'UAG: reachable from external'), bMid(L2, R2, 'Sessions < licensed limit'))))
    lines.append(R(merge(bMid(L1, R1, 'UAG: health endpoint green'), bMid(L2, R2, 'Blast latency <50ms'))))
    lines.append(R(merge(bMid(L1, R1, 'Active sessions: normal range'), bMid(L2, R2, 'vCPU/RAM: no contention'))))
    lines.append(R(merge(bMid(L1, R1, 'Abandoned sessions: none'), bMid(L2, R2, 'Disk IOPS: within baseline'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Connection Servers and UAGs are VMs; desktop VMs on ESXi cluster; monitor'))
    lines.append(txt_row('ESXi host resource utilisation to predict capacity for new sessions.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('CS Connected  = Connection Server can reach LDAP and vCenter'))
    lines.append(txt_row('UAG health    = REST endpoint /rest/healthcheck on UAG port 443'))
    lines.append(txt_row('Pool error    = pool stuck in provisioning, error, or maintenance'))
    lines.append(txt_row('Available count= desktops ready for session assignment'))
    lines.append(txt_row('Blast latency = display protocol round-trip; <50ms = good UX'))
    lines.append(txt_row('Abandoned     = session disconnected without logout; wasted license'))
    lines.append(txt_row('Licensed limit= concurrent sessions allowed by Horizon licence'))
    lines.append(txt_row('Provisioning stuck= instant clone VM not completing creation'))
    lines.append(txt_row('vCenter link  = Connection Server must reach vCenter for pool management'))
    lines.append(txt_row('AD reachable  = Connection Server must reach AD for user authentication'))
    lines.append(txt_row('Cert expiry   = expired cert causes browser login failures'))
    lines.append(txt_row('Session count = active + disconnected; both consume licence'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-install',
    'docs/virtualization/vmware/horizon/operations/install-upgrade/index.md',
    'VMware Horizon — Install & Upgrade',
)
def horizon_ops_install():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Install & Upgrade'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon installation deploys Connection Servers on Windows VMs; upgrade applies'))
    lines.append(txt_row('the installer sequentially to each CS, then updates UAGs and agents.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Pre-Install Requirements'), bMid(L2, R2, 'Install Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'Windows Server 2019/2022'), bMid(L2, R2, 'Install first CS: standard'))))
    lines.append(R(merge(bMid(L1, R1, 'AD domain joined'), bMid(L2, R2, 'Add replica CS: same pod'))))
    lines.append(R(merge(bMid(L1, R1, 'SQL Server: events DB'), bMid(L2, R2, 'Deploy UAGs via OVA'))))
    lines.append(R(merge(bMid(L1, R1, 'DNS: CS FQDN resolves'), bMid(L2, R2, 'Link to vCenter in Horizon'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Install first Connection Server before replicas; all share same LDAP config.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Upgrade Sequence'), bMid(L2, R2, 'Agent Upgrade'))))
    lines.append(R(merge(bMid(L1, R1, '1. Snapshot all CS VMs'), bMid(L2, R2, 'Update golden image'))))
    lines.append(R(merge(bMid(L1, R1, '2. Upgrade first CS'), bMid(L2, R2, 'Push: Horizon Agent install'))))
    lines.append(R(merge(bMid(L1, R1, '3. Upgrade replica CSs'), bMid(L2, R2, 'Instant clones: auto-reclone'))))
    lines.append(R(merge(bMid(L1, R1, '4. Upgrade UAGs'), bMid(L2, R2, 'Full clone: manual agent push'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Connection Server VMs need 8 vCPU / 32GB RAM; Windows Server licence required;'))
    lines.append(txt_row('UAGs need dual-NIC access to both internal and external networks.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Connection Server= Horizon broker; requires Windows Server OS'))
    lines.append(txt_row('Replica CS    = secondary broker; replicates LDAP from first CS'))
    lines.append(txt_row('Pod           = group of Connection Servers sharing same LDAP'))
    lines.append(txt_row('UAG           = Unified Access Gateway; OVA deployed; DMZ placement'))
    lines.append(txt_row('Events DB     = SQL Server; stores Horizon event log and reports'))
    lines.append(txt_row('LDAP          = Horizon config store; Active Directory Lightweight DS'))
    lines.append(txt_row('Golden image  = master VM; Horizon Agent installed; used for clones'))
    lines.append(txt_row('Reclone       = instant clone pool refreshes from updated golden image'))
    lines.append(txt_row('Agent push    = software distribution to full clone VMs'))
    lines.append(txt_row('Snapshot CS   = pre-upgrade rollback point; delete within 72h'))
    lines.append(txt_row('vCenter link  = Horizon must register vCenter in Administration UI'))
    lines.append(txt_row('Windows Server= required OS; 2019 or 2022; domain joined'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-proc',
    'docs/virtualization/vmware/horizon/operations/procedures/index.md',
    'VMware Horizon — Common Procedures',
)
def horizon_ops_proc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Common Procedures'))
    lines.append(txt_row())
    lines.append(txt_row('Common Horizon procedures: update golden image, push to pool, manage sessions,'))
    lines.append(txt_row('entitle users, and maintain certificates on Connection Servers.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Golden Image Update'), bMid(L2, R2, 'Session Management'))))
    lines.append(R(merge(bMid(L1, R1, 'Power off, snapshot parent'), bMid(L2, R2, 'Logoff: force if stuck'))))
    lines.append(R(merge(bMid(L1, R1, 'Install patches/apps'), bMid(L2, R2, 'Reset: restart desktop'))))
    lines.append(R(merge(bMid(L1, R1, 'Snapshot: new version'), bMid(L2, R2, 'Send message to user'))))
    lines.append(R(merge(bMid(L1, R1, 'Push scheduled via Horizon UI'), bMid(L2, R2, 'Disable: maintenance mode'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Golden image update is the most frequent Horizon maintenance task; schedule off-hours.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Entitlements & Certs'), bMid(L2, R2, 'Pool Maintenance'))))
    lines.append(R(merge(bMid(L1, R1, 'Add entitlement: AD group'), bMid(L2, R2, 'Pool in maintenance: drain'))))
    lines.append(R(merge(bMid(L1, R1, 'Remove: revoke from pool'), bMid(L2, R2, 'Delete stuck VM: force'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert: replace on CS via MMC'), bMid(L2, R2, 'Add machines: increase pool'))))
    lines.append(R(merge(bMid(L1, R1, 'vdmadmin: reset passwords'), bMid(L2, R2, 'Disable provisioning: pause'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Golden image updates temporarily reduce pool availability; schedule maintenance windows;'))
    lines.append(txt_row('certificate replacement requires IIS restart on Connection Server.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Golden image  = parent VM for instant clone pools'))
    lines.append(txt_row('Push          = schedule pool to use new parent snapshot'))
    lines.append(txt_row('Maintenance mode= pool unavailable; existing sessions continue'))
    lines.append(txt_row('Entitlement   = AD user or group assigned to a pool'))
    lines.append(txt_row('Revoke        = remove AD group/user entitlement from pool'))
    lines.append(txt_row('MMC           = Microsoft Management Console; cert store on Windows'))
    lines.append(txt_row('IIS restart   = required after cert replacement on CS'))
    lines.append(txt_row('Force delete  = remove stuck VM from pool that failed to provision'))
    lines.append(txt_row('Send message  = warn users before forced logoff/pool push'))
    lines.append(txt_row('Pool size     = min/max/spare desktops; tuned for peak usage'))
    lines.append(txt_row('Drain         = wait for sessions to end before pool action'))
    lines.append(txt_row('Provisioning  = Horizon auto-creates VMs to fill pool spare count'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ops-scripts',
    'docs/virtualization/vmware/horizon/operations/scripts/index.md',
    'VMware Horizon — Operational Scripts',
)
def horizon_ops_scripts():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Operational Scripts'))
    lines.append(txt_row())
    lines.append(txt_row('PowerCLI Horizon View module and REST API scripts automate pool reporting,'))
    lines.append(txt_row('session management, golden image push, and licence capacity checks.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Reporting Scripts'), bMid(L2, R2, 'Session Scripts'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-HVPool | Export-Csv'), bMid(L2, R2, 'Get-HVLocalSession (all)'))))
    lines.append(R(merge(bMid(L1, R1, 'Get-HVMachine | Ft Status'), bMid(L2, R2, 'Disconnect-HVSession'))))
    lines.append(R(merge(bMid(L1, R1, 'Licence usage: API /usage'), bMid(L2, R2, 'Send-HVSessionMessage'))))
    lines.append(R(merge(bMid(L1, R1, 'Pool capacity: available count'), bMid(L2, R2, 'Remove-HVSession (logoff)'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Read-only scripts for reporting; destructive session ops require Horizon admin role.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Maintenance Scripts'), bMid(L2, R2, 'REST API Examples'))))
    lines.append(R(merge(bMid(L1, R1, 'Start-HVMachineRecycle (push)'), bMid(L2, R2, 'POST /rest/login'))))
    lines.append(R(merge(bMid(L1, R1, 'Reset-HVMachine (reboot)'), bMid(L2, R2, 'GET /rest/inventory/v1/pools'))))
    lines.append(R(merge(bMid(L1, R1, 'Set-HVPool -Enable/-Disable'), bMid(L2, R2, 'PUT /rest/config/pools/{id}'))))
    lines.append(R(merge(bMid(L1, R1, 'Rebuild stuck clone: remove'), bMid(L2, R2, 'GET /rest/monitor/pools'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('PowerCLI scripts connect from jump host to Connection Server; REST API on port 443;'))
    lines.append(txt_row('use service account with minimum Horizon admin privileges.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Get-HVPool        = list all Horizon pools and their status'))
    lines.append(txt_row('Get-HVMachine     = list desktop VMs and their state'))
    lines.append(txt_row('Get-HVLocalSession= list active and disconnected sessions'))
    lines.append(txt_row('Disconnect-HVSession= disconnect user session without logoff'))
    lines.append(txt_row('Remove-HVSession  = force logoff of a session'))
    lines.append(txt_row('Send-HVSessionMessage= send popup message to user sessions'))
    lines.append(txt_row('Start-HVMachineRecycle= push golden image update to pool'))
    lines.append(txt_row('Reset-HVMachine   = force reboot a desktop VM'))
    lines.append(txt_row('POST /rest/login  = obtain Horizon REST API session token'))
    lines.append(txt_row('PUT /rest/config/pools= update pool configuration via REST'))
    lines.append(txt_row('GET /rest/monitor = health monitor endpoints for CS/pools'))
    lines.append(txt_row('Licence /usage    = REST endpoint for licence consumption reporting'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-sec-access',
    'docs/virtualization/vmware/horizon/security/access-control/index.md',
    'VMware Horizon — Access Control',
)
def horizon_sec_access():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Access Control'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon access control uses AD groups for pool entitlements, Horizon admin roles'))
    lines.append(txt_row('for management, and UAG for external session access control.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Admin Roles'), bMid(L2, R2, 'Pool Entitlements'))))
    lines.append(R(merge(bMid(L1, R1, 'Administrators: full control'), bMid(L2, R2, 'Entitle: AD user or group'))))
    lines.append(R(merge(bMid(L1, R1, 'Local role: per pod scope'), bMid(L2, R2, 'Per-pool entitlement'))))
    lines.append(R(merge(bMid(L1, R1, 'Custom roles: limited ops'), bMid(L2, R2, 'Global entitlement: CPA'))))
    lines.append(R(merge(bMid(L1, R1, 'Read-only: helpdesk role'), bMid(L2, R2, 'No direct VM access'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Entitlements control who gets a desktop; admin roles control who manages Horizon.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'UAG Access Control'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'Allowlist: source IP filter'), bMid(L2, R2, 'Events DB: log all logins'))))
    lines.append(R(merge(bMid(L1, R1, 'Authentication: MFA via RADIUS'), bMid(L2, R2, 'Horizon reports: usage'))))
    lines.append(R(merge(bMid(L1, R1, 'SAML: forward to CS'), bMid(L2, R2, 'Review: admin roles qtrly'))))
    lines.append(R(merge(bMid(L1, R1, 'DMZ rules: only 443 inbound'), bMid(L2, R2, 'Alert: login failures'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('UAG sits in DMZ with firewall rules; internal network only allows CS management;'))
    lines.append(txt_row('desktop VLAN isolated from management network.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Entitlement    = AD user/group assigned to pool; grants access'))
    lines.append(txt_row('Admin role     = Horizon admin privilege set; applied to AD group'))
    lines.append(txt_row('Custom role    = restricted admin role; e.g., helpdesk only'))
    lines.append(txt_row('Global entitlement= Cloud Pod Architecture; cross-pod pool access'))
    lines.append(txt_row('CPA            = Cloud Pod Architecture; multi-site/pod federation'))
    lines.append(txt_row('UAG allowlist  = IP source filtering on external UAG'))
    lines.append(txt_row('RADIUS         = MFA backend; UAG proxies auth before CS'))
    lines.append(txt_row('SAML           = UAG passes assertion to Connection Server'))
    lines.append(txt_row('Events DB      = SQL DB; Horizon audit log; login/logoff events'))
    lines.append(txt_row('Read-only role = view sessions and machines; no changes'))
    lines.append(txt_row('DMZ firewall   = only port 443 inbound to UAG from internet'))
    lines.append(txt_row('Qtrly review   = audit Horizon admin role assignments'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-sec-auth',
    'docs/virtualization/vmware/horizon/security/authentication/index.md',
    'VMware Horizon — Authentication',
)
def horizon_sec_auth():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Authentication'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon authenticates users via AD; external users authenticate through UAG with'))
    lines.append(txt_row('optional MFA (RADIUS/RSA); smart card and SAML federation are also supported.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Internal Auth Flow'), bMid(L2, R2, 'External Auth Flow'))))
    lines.append(R(merge(bMid(L1, R1, 'Client → Connection Server'), bMid(L2, R2, 'Client → UAG (internet)'))))
    lines.append(R(merge(bMid(L1, R1, 'CS validates AD credentials'), bMid(L2, R2, 'UAG → optional MFA'))))
    lines.append(R(merge(bMid(L1, R1, 'Kerberos or NTLM to AD'), bMid(L2, R2, 'UAG → SAML to CS'))))
    lines.append(R(merge(bMid(L1, R1, 'Session token issued'), bMid(L2, R2, 'CS validates with AD'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Internal flow is direct to CS; external flow proxies through UAG with optional MFA.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'MFA Options'), bMid(L2, R2, 'Passwordless Options'))))
    lines.append(R(merge(bMid(L1, R1, 'RADIUS: OTP token'), bMid(L2, R2, 'Smart card: PIV/CAC'))))
    lines.append(R(merge(bMid(L1, R1, 'RSA SecurID token'), bMid(L2, R2, 'Kerberos SSO: domain joined'))))
    lines.append(R(merge(bMid(L1, R1, 'Duo: RADIUS proxy'), bMid(L2, R2, 'SAML: Workspace ONE Access'))))
    lines.append(R(merge(bMid(L1, R1, 'Configured on UAG'), bMid(L2, R2, 'Windows Hello: W1 UEM'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('AD DCs must be reachable from Connection Servers on management network;'))
    lines.append(txt_row('RADIUS server reachable from UAG; smart card reader at physical endpoint.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('AD auth       = Kerberos (domain joined) or NTLM to AD DC'))
    lines.append(txt_row('RADIUS        = MFA protocol; UAG sends credentials to RADIUS server'))
    lines.append(txt_row('RSA SecurID   = OTP hardware token; RADIUS integration'))
    lines.append(txt_row('Duo           = cloud MFA; accessed via RADIUS proxy from UAG'))
    lines.append(txt_row('SAML          = federated auth; Workspace ONE Access as IdP'))
    lines.append(txt_row('Smart card    = PIV/CAC cert-based login; AD smart card auth'))
    lines.append(txt_row('Kerberos SSO  = domain-joined client gets desktop without re-auth'))
    lines.append(txt_row('UAG           = Unified Access Gateway; handles external MFA flow'))
    lines.append(txt_row('CS            = Connection Server; final auth validator with AD'))
    lines.append(txt_row('Windows Hello = biometric/PIN auth; requires Workspace ONE UEM'))
    lines.append(txt_row('Session token = issued by CS after successful auth; used for session'))
    lines.append(txt_row('OTP           = One-Time Password; from hardware or soft token'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-sec-enc',
    'docs/virtualization/vmware/horizon/security/encryption/index.md',
    'VMware Horizon — Encryption',
)
def horizon_sec_enc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Encryption'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon encrypts all sessions via Blast Extreme (TLS) or PCoIP; management traffic'))
    lines.append(txt_row('is TLS 1.2+; VM disk encryption is handled by vSphere/vSAN layer.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Session Encryption'), bMid(L2, R2, 'Management Encryption'))))
    lines.append(R(merge(bMid(L1, R1, 'Blast Extreme: TLS + AES'), bMid(L2, R2, 'CS to CS: TLS 1.2+'))))
    lines.append(R(merge(bMid(L1, R1, 'PCoIP: AES-256 + UDP'), bMid(L2, R2, 'CS to vCenter: TLS'))))
    lines.append(R(merge(bMid(L1, R1, 'HTML Access: WebSocket TLS'), bMid(L2, R2, 'CS to UAG: TLS'))))
    lines.append(R(merge(bMid(L1, R1, 'USB redirection: TLS tunnel'), bMid(L2, R2, 'REST API: TLS 1.2+'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('All Horizon traffic is encrypted; PCoIP UDP uses AES-256 even without TLS wrapper.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Certificate Management'), bMid(L2, R2, 'Data at Rest'))))
    lines.append(R(merge(bMid(L1, R1, 'CS cert: replace in Windows'), bMid(L2, R2, 'Desktop VMDK: vSAN enc'))))
    lines.append(R(merge(bMid(L1, R1, 'UAG cert: import via UI'), bMid(L2, R2, 'Profile share: SMB enc'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2 minimum: enforce'), bMid(L2, R2, 'BitLocker: full clone VMs'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expiry: monitor 30d+'), bMid(L2, R2, 'AppStack: enc on datastore'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Certificate replacement on CS triggers IIS restart; brief service interruption;'))
    lines.append(txt_row('UAG cert import via admin UI on port 9443 (no restart needed).'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Blast Extreme = VMware display protocol; TLS 1.2+ with AES-256'))
    lines.append(txt_row('PCoIP         = Teradici protocol; AES-256; UDP-based'))
    lines.append(txt_row('HTML Access   = WebSocket over HTTPS; TLS-protected Blast'))
    lines.append(txt_row('TLS 1.2+      = minimum for all Horizon management traffic'))
    lines.append(txt_row('UAG cert      = public cert on UAG; presented to external clients'))
    lines.append(txt_row('CS cert       = Windows cert store on Connection Server'))
    lines.append(txt_row('IIS restart   = required after cert replace on CS; brief downtime'))
    lines.append(txt_row('vSAN enc      = disk-level AES-256; transparent to Horizon'))
    lines.append(txt_row('BitLocker     = Windows full-disk encryption on persistent VMs'))
    lines.append(txt_row('SMB enc       = encryption on CIFS profile shares'))
    lines.append(txt_row('AppStack      = App Volumes VMDK; encrypt at vSAN/datastore level'))
    lines.append(txt_row('USB tunnel    = redirected USB over TLS tunnel to desktop'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-sec-hard',
    'docs/virtualization/vmware/horizon/security/hardening/index.md',
    'VMware Horizon — Hardening',
)
def horizon_sec_hard():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Hardening'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon hardening follows the VMware Horizon Security Hardening Guide: TLS enforcement,'))
    lines.append(txt_row('MFA, network isolation, session timeout, and audit logging.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Network Hardening'), bMid(L2, R2, 'Session Hardening'))))
    lines.append(R(merge(bMid(L1, R1, 'Desktop VLAN: isolated'), bMid(L2, R2, 'Session timeout: 8h max'))))
    lines.append(R(merge(bMid(L1, R1, 'DMZ: UAG only, port 443'), bMid(L2, R2, 'Disconnect timeout: 1h'))))
    lines.append(R(merge(bMid(L1, R1, 'No direct CS from internet'), bMid(L2, R2, 'Logoff on disconnect: enable'))))
    lines.append(R(merge(bMid(L1, R1, 'Firewall: CS mgmt only'), bMid(L2, R2, 'USB: restrict or disable'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('UAG as the only external entry point is the most important network control.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Auth Hardening'), bMid(L2, R2, 'Audit & Compliance'))))
    lines.append(R(merge(bMid(L1, R1, 'MFA: RADIUS/RSA on UAG'), bMid(L2, R2, 'Events DB: all logins'))))
    lines.append(R(merge(bMid(L1, R1, 'TLS 1.2 minimum: enforce'), bMid(L2, R2, 'Syslog: CS events to SIEM'))))
    lines.append(R(merge(bMid(L1, R1, 'Smart card: enforce for govt'), bMid(L2, R2, 'SIEM: login failure alerts'))))
    lines.append(R(merge(bMid(L1, R1, 'SSO: Workspace ONE + MFA'), bMid(L2, R2, 'Quarterly: entitlement audit'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Desktop VMs run on dedicated ESXi hosts with isolated VLAN; Connection Server VMs'))
    lines.append(txt_row('on management network; UAG in DMZ; profile shares on NAS.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Session timeout= max session age; logoff user after 8h inactivity'))
    lines.append(txt_row('Disconnect timeout= auto-logoff disconnected sessions after 1h'))
    lines.append(txt_row('Logoff on disconnect= destroy instant clone on disconnect for security'))
    lines.append(txt_row('USB restrict  = limit USB redirection to approved device classes'))
    lines.append(txt_row('DMZ           = demilitarised zone; UAG sits here with dual NIC'))
    lines.append(txt_row('Events DB     = Horizon SQL event log; login/session/admin events'))
    lines.append(txt_row('SIEM          = Security Info and Event Mgmt; receives CS syslog'))
    lines.append(txt_row('TLS 1.2       = minimum; disable TLS 1.0/1.1 in CS config'))
    lines.append(txt_row('MFA           = Multi-Factor Auth; configured on UAG'))
    lines.append(txt_row('Entitlement audit= check all pool entitlements; remove stale groups'))
    lines.append(txt_row('RADIUS        = MFA backend; OTP from RSA/Duo/Okta'))
    lines.append(txt_row('Isolated VLAN = desktop VMs cannot reach management or other VLANs'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ts-common',
    'docs/virtualization/vmware/horizon/troubleshooting/common-issues/index.md',
    'VMware Horizon — Common Issues',
)
def horizon_ts_common():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Common Issues'))
    lines.append(txt_row())
    lines.append(txt_row('Common Horizon issues: black screen, pool provisioning failure, Connection Server'))
    lines.append(txt_row('error, slow Blast sessions, and UAG certificate errors.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Black Screen Issues'), bMid(L2, R2, 'Provisioning Failures'))))
    lines.append(R(merge(bMid(L1, R1, 'Agent not running on VM'), bMid(L2, R2, 'vCenter: not reachable'))))
    lines.append(R(merge(bMid(L1, R1, 'Blast port 8443 blocked'), bMid(L2, R2, 'Template: no snapshot'))))
    lines.append(R(merge(bMid(L1, R1, 'GPU driver mismatch'), bMid(L2, R2, 'Disk space: datastore full'))))
    lines.append(R(merge(bMid(L1, R1, 'Profile load fails: DEM'), bMid(L2, R2, 'Clone error: check events'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Black screen = Blast connected but agent not ready; check agent services.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'CS & UAG Issues'), bMid(L2, R2, 'Performance Issues'))))
    lines.append(R(merge(bMid(L1, R1, 'CS error: check services'), bMid(L2, R2, 'Blast latency >100ms'))))
    lines.append(R(merge(bMid(L1, R1, 'Cert expired: replace on CS'), bMid(L2, R2, 'Check ESXi host CPU'))))
    lines.append(R(merge(bMid(L1, R1, 'UAG: health check fails'), bMid(L2, R2, 'Disk IOPS: vSAN contention'))))
    lines.append(R(merge(bMid(L1, R1, 'AD unreachable: local user?'), bMid(L2, R2, 'Network BW: 1–5Mbps/user'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Most issues: agent not running (black screen), network ports blocked, vCenter'))
    lines.append(txt_row('unreachable (provisioning), or cert expired (login/UAG); check all four.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon Agent = service on desktop VM; must be running for session'))
    lines.append(txt_row('Blast port 8443= UDP/TCP port for display protocol; must be open'))
    lines.append(txt_row('Black screen  = connected session but no display; agent issue'))
    lines.append(txt_row('DEM           = Dynamic Environment Manager; profile load at login'))
    lines.append(txt_row('UAG health    = REST /rest/healthcheck; returns 200 if healthy'))
    lines.append(txt_row('CS services   = VMware Horizon View Connection Server service on Windows'))
    lines.append(txt_row('Template      = golden image VM must have current snapshot'))
    lines.append(txt_row('Clone error   = check vCenter tasks and events for provisioning log'))
    lines.append(txt_row('GPU driver    = agent + driver version must match; black screen if not'))
    lines.append(txt_row('Blast latency = display round-trip; >100ms = degraded user experience'))
    lines.append(txt_row('IOPS contention= vSAN or NFS storage saturation during peak clone'))
    lines.append(txt_row('1–5Mbps/user  = Blast bandwidth per session; plan WAN accordingly'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ts-diag',
    'docs/virtualization/vmware/horizon/troubleshooting/diagnostics/index.md',
    'VMware Horizon — Diagnostics',
)
def horizon_ts_diag():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Diagnostics'))
    lines.append(txt_row())
    lines.append(txt_row('Horizon diagnostics use Connection Server logs, support bundles, Horizon admin UI,'))
    lines.append(txt_row('and desktop agent logs to identify root causes of session and provisioning failures.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Connection Server Logs'), bMid(L2, R2, 'Agent Logs'))))
    lines.append(R(merge(bMid(L1, R1, 'C:\\ProgramData\\VMware\\VDM'), bMid(L2, R2, 'C:\\ProgramData\\VMware\\VDM'))))
    lines.append(R(merge(bMid(L1, R1, 'debug-*.log: main broker'), bMid(L2, R2, 'debug-*.log on desktop VM'))))
    lines.append(R(merge(bMid(L1, R1, 'vlsi-*.log: vCenter ops'), bMid(L2, R2, 'wsnm_*.log: display path'))))
    lines.append(R(merge(bMid(L1, R1, 'support bundle: zip via UI'), bMid(L2, R2, 'Event log: Windows App'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Start with CS debug log; if session connects but black screen, check agent logs.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Admin UI Diagnostics'), bMid(L2, R2, 'UAG Diagnostics'))))
    lines.append(R(merge(bMid(L1, R1, 'Horizon Admin: Dashboard'), bMid(L2, R2, 'UAG admin UI: 9443'))))
    lines.append(R(merge(bMid(L1, R1, 'Events: filter by severity'), bMid(L2, R2, '/rest/healthcheck: 200?'))))
    lines.append(R(merge(bMid(L1, R1, 'Pool: provisioning errors'), bMid(L2, R2, 'UAG log: /opt/vmware/etc'))))
    lines.append(R(merge(bMid(L1, R1, 'Sessions: filter by state'), bMid(L2, R2, 'Cert: check UAG cert date'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('Collect CS support bundle via Horizon Admin UI; agent logs from desktop VM;'))
    lines.append(txt_row('UAG logs via SSH to UAG appliance.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('debug-*.log   = CS main log; broker decisions, auth, pool operations'))
    lines.append(txt_row('vlsi-*.log    = vCenter API interaction log; provisioning details'))
    lines.append(txt_row('wsnm_*.log    = agent display protocol log; Blast/PCoIP session'))
    lines.append(txt_row('ProgramData   = Windows hidden folder; Horizon stores logs here'))
    lines.append(txt_row('Support bundle= Horizon Admin UI > Support > Generate Bundle'))
    lines.append(txt_row('Horizon Admin = web UI for Horizon management; port 443 on CS'))
    lines.append(txt_row('Events tab    = Horizon UI event log; filter by error/warning'))
    lines.append(txt_row('UAG admin     = port 9443; cert, edge service, health config'))
    lines.append(txt_row('/rest/healthcheck= UAG health endpoint; returns 200 OK if healthy'))
    lines.append(txt_row('UAG log       = /opt/vmware/etc/esmanager/; edge service logs'))
    lines.append(txt_row('Windows App log= Windows Event Viewer; Horizon Agent events here'))
    lines.append(txt_row('Pool error    = UI shows red error; hover for provisioning reason'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines


@kb_diagram(
    'horizon-ts-esc',
    'docs/virtualization/vmware/horizon/troubleshooting/escalation/index.md',
    'VMware Horizon — Escalation',
)
def horizon_ts_esc():
    W2 = 103
    R, txt_row = make_helpers(W2)
    L1, R1, L2, R2 = 3, 50, 53, 99
    lines = []
    lines.append(title_border(W2, 'VMware Horizon — Escalation'))
    lines.append(txt_row())
    lines.append(txt_row('Escalate Horizon issues to VMware GSS when all users are impacted, agent fails'))
    lines.append(txt_row('on all desktops, or Connection Server is unresponsive.'))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'Escalation Triggers'), bMid(L2, R2, 'Pre-Escalation Steps'))))
    lines.append(R(merge(bMid(L1, R1, 'All users: cannot login'), bMid(L2, R2, 'Collect CS support bundle'))))
    lines.append(R(merge(bMid(L1, R1, 'CS unresponsive: all failed'), bMid(L2, R2, 'Collect agent logs'))))
    lines.append(R(merge(bMid(L1, R1, 'Pool provisioning: 100% error'), bMid(L2, R2, 'Document error messages'))))
    lines.append(R(merge(bMid(L1, R1, 'Agent crash loop: all VMs'), bMid(L2, R2, 'Timeline of changes'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('If all Connection Servers fail simultaneously, priority is restore from snapshot or backup.'))
    lines.append(txt_row())
    lines.append(R(arrow([26, 76])))
    lines.append(txt_row())
    lines.append(R(merge(bTop(L1, R1), bTop(L2, R2))))
    lines.append(R(merge(bMid(L1, R1, 'GSS Engagement'), bMid(L2, R2, 'Escalation Path'))))
    lines.append(R(merge(bMid(L1, R1, 'Open P1 SR: broadcom portal'), bMid(L2, R2, 'T1: triage + bundles'))))
    lines.append(R(merge(bMid(L1, R1, 'Include Horizon version'), bMid(L2, R2, 'T2: Horizon SE'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach CS support bundle'), bMid(L2, R2, 'T3: engineering review'))))
    lines.append(R(merge(bMid(L1, R1, 'Attach agent logs ZIP'), bMid(L2, R2, 'CritSit: P1 with VIP impact'))))
    lines.append(R(merge(bBot(L1, R1), bBot(L2, R2))))
    lines.append(txt_row())
    lines.append(txt_row('Physical Infrastructure (the hardware everything above runs on):'))
    lines.append(txt_row('GSS may request Bomgar remote access to Connection Server and desktop VMs;'))
    lines.append(txt_row('provide admin RDP to CS and vCenter access for remote engineers.'))
    lines.append(txt_row())
    lines.append(txt_row('Key terms:'))
    lines.append(txt_row())
    lines.append(txt_row('SR            = Service Request; support ticket at support.broadcom.com'))
    lines.append(txt_row('P1 severity   = highest; production VDI outage; 24/7 response'))
    lines.append(txt_row('CS support bundle= generated via Horizon Admin UI > Support'))
    lines.append(txt_row('Agent logs    = C:\\ProgramData\\VMware\\VDM\\debug*.log on desktop'))
    lines.append(txt_row('Timeline      = list of recent changes before failure'))
    lines.append(txt_row('Horizon version= check Administration > Product Licensing'))
    lines.append(txt_row('T2 Horizon SE = VMware senior Horizon specialist'))
    lines.append(txt_row('CritSit       = Critical Situation; exec escalation; 24/7 war room'))
    lines.append(txt_row('Bomgar        = remote support tool; GSS engineer connect'))
    lines.append(txt_row('Snapshot restore= fastest recovery for CS failure'))
    lines.append(txt_row('LDAP restore  = vdmimport from backup if CS config lost'))
    lines.append(txt_row('KB article    = check VMware KB before raising SR'))
    lines.append(txt_row())
    lines.append('└' + '─' * W2 + '┘')
    return lines
