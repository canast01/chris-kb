#!/usr/bin/env python3
"""
Append VCP-DCV exam learning diagrams to virtualization how-it-works pages.
Run from repo root: python3 scripts/add_learning_diagrams.py
"""

W = 105  # total line width

# ── box helpers ────────────────────────────────────────────────────────────────

def top(title):
    t = f' {title} '
    d = W - 2 - len(t)
    return '┌' + '─' * (d // 2) + t + '─' * (d - d // 2) + '┐'

def bot():
    return '└' + '─' * (W - 2) + '┘'

def blank():
    return '│' + ' ' * (W - 2) + '│'

def L(text=''):
    return ('│  ' + text).ljust(W - 1) + '│'

def divider():
    return L('─' * 89)

# inner two-column helpers (46 left / 45 right content chars)
ILW, IRW = 46, 45

def itop():
    return '│   ┌' + '─' * ILW + '┐  ┌' + '─' * IRW + '┐   │'

def ibot():
    return '│   └' + '─' * ILW + '┘  └' + '─' * IRW + '┘   │'

def irow(left='', right=''):
    return '│   │' + left.ljust(ILW)[:ILW] + '│  │' + right.ljust(IRW)[:IRW] + '│   │'

def ititle(left, right):
    return irow(left.center(ILW), right.center(IRW))

def ifiller():
    return irow('', '')

def iarrow():
    return L('                                      │')

def iarrow2():
    return L('                                      ▼')

def fence(lines):
    return ['```'] + lines + ['```']

def section(heading, diag_lines):
    return ['\n---\n', f'## {heading}\n', '```'] + diag_lines + ['```']


# ── diagrams ───────────────────────────────────────────────────────────────────

# ══ vCenter how-it-works additions ════════════════════════════════════════════

VCENTER_SECTIONS = []

# 1. VCHA Topology
d = [
    top('vCenter HA (VCHA) — Node Topology'),
    blank(),
    L('Three-node cluster — no shared storage; replication is network-based over a dedicated HA network.'),
    blank(),
    itop(),
    ititle('Active VCSA', 'Passive VCSA'),
    divider(),
    irow(' Serves all client + API traffic', ' Hot standby — continuously synced'),
    irow(' Holds the cluster VIP (port 443)', ' Takes over VIP on active failure'),
    irow(' Runs full PostgreSQL database', ' Shares same DB replica from active'),
    irow(' Sends heartbeat to witness', ' RTO: < 60 s  ·  RPO: near-zero'),
    irow(' Write-commits replicated sync', ' Can be on separate ESXi host/rack'),
    ifiller(),
    ibot(),
    blank(),
    L('                  Replication (both nodes heartbeat to witness)'),
    L('                                      │'),
    L('                                      ▼'),
    blank(),
    L('  ┌──────────────────────────────────────────┐'),
    L('  │              Witness VCSA                │'),
    L('  │  2 vCPU / 1 GB RAM  ·  no DB, no VIP    │'),
    L('  │  Tie-breaker for split-brain quorum      │'),
    L('  │  Can run on a third site or small VM     │'),
    L('  └──────────────────────────────────────────┘'),
    blank(),
    L('  Split-brain: if Active and Passive lose contact, the node that can still reach the'),
    L('  Witness wins quorum. The losing node fences itself — prevents dual-active writes.'),
    blank(),
    L('  VCHA      = vCenter High Availability; three-node failover for the VCSA itself'),
    L('  VIP       = Virtual IP; shared between active/passive; clients always connect to VIP'),
    L('  Witness   = lightweight tie-breaker VM; holds no data; just arbitrates quorum'),
    L('  RPO       = near-zero: replication is synchronous to passive before ack'),
    L('  RTO       = typically < 60 s: automatic failover, VIP moves to passive'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('vCenter HA (VCHA) — Topology', d))

# 2. Identity Federation
d = [
    top('vCenter — Identity Federation Flow (vSphere 8)'),
    blank(),
    L('Identity federation lets vCenter delegate authentication to an external Identity Provider (IdP)'),
    L('such as ADFS, Okta, or Ping. vCenter trusts SAML / OIDC assertions from the registered IdP.'),
    blank(),
    itop(),
    ititle('Traditional (SSO / LDAP)', 'Federated (External IdP)'),
    divider(),
    irow(' User → vCenter login page', ' User → vCenter → redirect to IdP'),
    irow(' vCenter checks local SSO store', ' IdP authenticates (AD, MFA, etc.)'),
    irow(' SSO queries AD/LDAP directly', ' IdP issues SAML assertion / token'),
    irow(' vCenter issues session token', ' vCenter validates assertion, maps'),
    irow(' All auth logic inside vCenter', '   user to local role, grants access'),
    irow(' No external IdP required', ' Password never sent to vCenter'),
    ifiller(),
    ibot(),
    blank(),
    L('  Federation setup (vSphere 8):'),
    L('    1.  Register external IdP in vCenter SSO → Configuration → Identity Federation'),
    L('    2.  Upload IdP metadata (entity ID, signing cert, SSO URL)'),
    L('    3.  Configure redirect URI in IdP to vCenter callback endpoint'),
    L('    4.  Map IdP groups/users to vCenter roles (Administration → Global Permissions)'),
    blank(),
    L('  IdP        = Identity Provider; external auth service (ADFS, Okta, Azure AD, Ping)'),
    L('  SAML       = Security Assertion Markup Language; XML-based auth assertion format'),
    L('  OIDC       = OpenID Connect; OAuth 2.0-based; token is a signed JWT'),
    L('  Assertion  = signed claim from IdP confirming user identity and group membership'),
    L('  KMIP       = Key Management Interoperability Protocol; used for KMS communication'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('Identity Federation (vSphere 8)', d))

# 3. VM Encryption Key Hierarchy
d = [
    top('VM Encryption — Key Hierarchy (KMS / vTPM)'),
    blank(),
    L('VM encryption uses a two-tier key model. Keys never leave the KMS in plaintext;'),
    L('vCenter only holds the encrypted DEK (wrapped by the KEK stored in the KMS).'),
    blank(),
    itop(),
    ititle('Key Management Server (KMS)', 'VM Storage Layout'),
    divider(),
    irow(' External KMIP-compliant server', ' .vmx file — VM config (encrypted)'),
    irow(' Stores Key Encrypting Keys (KEKs)', ' .vmdk — virtual disk (encrypted)'),
    irow(' vCenter connects via KMIP/TLS', ' .nvram — firmware vars (encrypted)'),
    irow(' vCenter requests KEK per VM', ' .vswp swap excluded from encryption'),
    irow(' KEK never leaves KMS in plaintext', ' DEK generated by vSphere per VM'),
    irow(' Revoke KEK = VM cannot power on', ' DEK wrapped by KEK → stored in vmx'),
    ifiller(),
    ibot(),
    blank(),
    L('  Encrypt / decrypt flow:'),
    L('    1.  Admin enables VM encryption in storage policy'),
    L('    2.  vCenter fetches KEK from KMS (KMIP GET key)'),
    L('    3.  vSphere generates a random DEK for this VM'),
    L('    4.  DEK is encrypted with KEK → cipher-DEK stored in .vmx'),
    L('    5.  All I/O (read/write) encrypted/decrypted transparently using DEK in RAM'),
    L('    6.  On power-off DEK is discarded; power-on requires fresh KEK from KMS'),
    blank(),
    L('  KMS    = Key Management Server; external; holds KEKs; accessed via KMIP'),
    L('  KMIP   = Key Management Interoperability Protocol (port 5696)'),
    L('  KEK    = Key Encrypting Key; stored in KMS; wraps the DEK'),
    L('  DEK    = Data Encrypting Key; generated by vSphere; used for actual I/O'),
    L('  vTPM   = virtual Trusted Platform Module; requires vCenter KMS to unseal'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('VM Encryption — Key Hierarchy', d))

# 4. Content Library Topology
d = [
    top('Content Library — Publish & Subscribe Topology'),
    blank(),
    L('A published library exposes its catalogue over HTTPS. Subscribed libraries on any'),
    L('vCenter instance sync the content locally, enabling fast VM deployment without cross-site I/O.'),
    blank(),
    itop(),
    ititle('Published Library (source vCenter)', 'Subscribed Library (target vCenter)'),
    divider(),
    irow(' Contains: OVF/OVA templates', ' Subscribes to published HTTPS URL'),
    irow('   VM templates (native format)', ' Sync policy: on-demand or immediate'),
    irow('   ISO images', ' Content cached locally on datastore'),
    irow('   Scripts and files', ' VM deploy uses local copy — fast'),
    irow(' Publication endpoint: HTTPS URL', ' Read-only — changes made at source'),
    irow(' HTTPS + optional password', ' Multiple subscribers supported'),
    ifiller(),
    ibot(),
    blank(),
    L('  Published → Subscribed sync flow:'),
    L('    1.  Admin creates local library → enables "Published" checkbox → gets HTTPS URL'),
    L('    2.  On target vCenter: New Subscribed Library → paste URL → set sync policy'),
    L('    3.  Initial full sync downloads all items to target datastore'),
    L('    4.  Updates: source library changes → subscribers detect delta → sync diff only'),
    L('    5.  Deploy VM from subscribed library = pulls from local datastore copy'),
    blank(),
    L('  OVF template  = Open Virtualisation Format; portable VM descriptor + disk(s)'),
    L('  On-demand     = content downloaded only when needed for deployment'),
    L('  Immediate     = content synced as soon as source library updates'),
    L('  ISO sync      = entire ISO downloaded; large files sync in background'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('Content Library — Publish & Subscribe', d))

# 5. Resource Pool Hierarchy
d = [
    top('Resource Pools — Shares, Limits & Reservations'),
    blank(),
    L('Resource pools create a hierarchy of guaranteed and throttled resource entitlements.'),
    L('Shares determine proportional access when contention exists; limits cap usage absolutely.'),
    blank(),
    L('  Cluster root  (all hosts combined: e.g. 128 pCPU, 1024 GB RAM)'),
    L('  │'),
    L('  ├── Resource Pool: Production  [shares: High 8000, limit: none, reservation: 64 GHz]'),
    L('  │     │  VMs here guaranteed 64 GHz floor; can burst to cluster max'),
    L('  │     ├── VM-Prod-1  (4 vCPU, reservation: 4 GHz)'),
    L('  │     └── VM-Prod-2  (8 vCPU, no reservation)'),
    L('  │'),
    L('  ├── Resource Pool: Dev  [shares: Normal 4000, limit: 32 GHz, reservation: none]'),
    L('  │     │  VMs capped at 32 GHz total even if cluster is idle'),
    L('  │     └── VM-Dev-1  (2 vCPU, no reservation or limit)'),
    L('  │'),
    L('  └── Resource Pool: Test  [shares: Low 2000, limit: 16 GHz, reservation: none]'),
    L('        │  During contention: Prod gets 2x Dev shares, 4x Test shares'),
    L('        └── VM-Test-1  (2 vCPU, limit: 2 GHz — hard cap always enforced)'),
    blank(),
    L('  Shares      = relative priority during contention; High:Normal:Low = 4:2:1'),
    L('  Reservation = guaranteed minimum CPU/mem; cluster must be able to meet all reservations'),
    L('  Limit       = hard ceiling on usage; never exceeded even if resources are free'),
    L('  Expandable  = if set, child pool can borrow from parent when parent has slack'),
    L('  Overhead    = vSphere reserves CPU/mem for VMkernel overhead per running VM'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('Resource Pools — Shares, Limits & Reservations', d))

# 6. vMotion Types Comparison
d = [
    top('VM Migration — vMotion Type Comparison'),
    blank(),
    L('  Type                  VM State     What Moves           Storage         vCenter'),
    L('  ────────────────────────────────────────────────────────────────────────────────────'),
    L('  vMotion               Powered ON   CPU + memory state   Stays on same   Same SSO'),
    L('                                     vNIC reconnects      datastore       domain'),
    L('                                     < 1 s downtime                              '),
    blank(),
    L('  Storage vMotion       Powered ON   VMDK files (live)    Moves to new    Same SSO'),
    L('  (svMotion)                         VM stays running     datastore       domain'),
    L('                                     Mirror → switch                             '),
    blank(),
    L('  Cold Migration        Powered OFF  All VM files         Moves (opt.)    Same or'),
    L('                                     .vmx .vmdk .nvram    New datastore   cross-VC'),
    L('                                     No memory to xfer    or same                '),
    blank(),
    L('  Cross-vCenter Export  Powered OFF  All VM files         Moves           Different'),
    L('  (cross-VC vMotion*)   (or ON**)    Registered at dest   Optional        vCenters'),
    L('  * Enhanced linked mode required for powered-on cross-VC vMotion (xvMotion)         '),
    blank(),
    L('  vMotion requirements: shared storage visible from both hosts; same L2 or vDS port group;'),
    L('    compatible CPU families (or EVC mode enabled); sufficient memory on target host.'),
    blank(),
    L('  vMotion    = live migration of running VM between hosts; no storage move'),
    L('  svMotion   = live storage migration; VM stays on same host; VMDK mirrored then cut'),
    L('  EVC        = Enhanced vMotion Compatibility; masks CPU features for cross-gen moves'),
    L('  xvMotion   = cross-vCenter vMotion (powered-on); requires Enhanced Linked Mode'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('vMotion Types — Comparison', d))

# 7. DRS Placement and Balancing Logic
d = [
    top('DRS — Placement & Balancing Logic'),
    blank(),
    itop(),
    ititle('Initial Placement (VM power-on)', 'Ongoing Balancing (every 5 min)'),
    divider(),
    irow(' DRS scores all eligible hosts', ' Measures host resource utilisation'),
    irow(' Prefers host with most headroom', ' Calculates cluster imbalance score'),
    irow(' Respects: affinity rules,', ' Generates migration recommendations'),
    irow('  reservations, NUMA topology', ' Weighs move cost vs. benefit gained'),
    irow(' Picks best-scored host,', ' Applies recs per automation level:'),
    irow('  powers on VM there', '  Manual / Partial / Fully Automated'),
    ifiller(),
    ibot(),
    blank(),
    L('  Automation levels:'),
    L('    Manual          — DRS generates recommendations; admin reviews and applies each'),
    L('    Partially Auto  — Auto power-on placement; manual approval for ongoing balancing'),
    L('    Fully Automated — Auto placement + auto migration; threshold 1 (aggr) – 5 (cons)'),
    blank(),
    L('  Affinity / Anti-affinity rules:'),
    L('    VM-VM affinity      — keep these VMs on the same host (HA pair, licensing)'),
    L('    VM-VM anti-affinity — keep these VMs on different hosts (HA separation)'),
    L('    VM-Host affinity    — prefer or require VMs on specific hosts (licensing, hardware)'),
    blank(),
    L('  DRS     = Distributed Resource Scheduler; runs in vCenter; uses vMotion to balance'),
    L('  Score   = per-host metric: 0 (ideal) to 100 (overloaded); DRS targets uniform score'),
    L('  Imbal.  = deviation of host scores from cluster average; triggers migration at threshold'),
    L('  DPM     = Distributed Power Management; companion to DRS; powers off idle hosts'),
    blank(),
    bot(),
]
VCENTER_SECTIONS.append(section('DRS — Placement & Balancing Logic', d))


# ══ ESXi how-it-works additions ═══════════════════════════════════════════════

ESXI_SECTIONS = []

# 8. Storage Protocol Stack
d = [
    top('ESXi — Storage Protocol Comparison'),
    blank(),
    L('  Protocol     Initiator         Transport         Array presents     ESXi sees'),
    L('  ─────────────────────────────────────────────────────────────────────────────────'),
    L('  Fibre         HBA (QLogic/      FC fabric         LUN (SCSI block)   naa.xxxx'),
    L('  Channel       Emulex)           16/32/64 GFC      Zoned per HBA      VMFS or RDM'),
    blank(),
    L('  iSCSI SW      vmknic + TCP/IP   Ethernet (1/10/   LUN (SCSI block)   naa.xxxx'),
    L('  initiator     stack (no HBA)    25 GbE)           CHAP auth          VMFS or RDM'),
    blank(),
    L('  iSCSI HW      iSCSI HBA        Ethernet          LUN (SCSI block)   naa.xxxx'),
    L('  initiator     (TOE offload)     1/10/25 GbE       CHAP auth          VMFS or RDM'),
    blank(),
    L('  NFS v3        NFS client in     Ethernet          Export (file)      /vmfs/volumes/'),
    L('                vmkernel          1/10/25 GbE       No CHAP; IP auth   UUID          '),
    blank(),
    L('  NFS v4.1      NFS client in     Ethernet          Export (file)      /vmfs/volumes/'),
    L('                vmkernel          1/10/25 GbE       Kerberos / SYS     UUID (pNFS ok)'),
    blank(),
    L('  vSAN          vSAN VMkernel     Ethernet (RDMA    Local disk groups  vsanDatastore'),
    L('                (vmk UDP)         optional)         pooled across hosts (single DS)  '),
    blank(),
    L('  VAAI    = vStorage APIs for Array Integration; offloads clone/zeroing to array'),
    L('  VMFS    = VMware File System; clustered; shared read/write across all ESXi hosts'),
    L('  RDM     = Raw Device Mapping; guest OS accesses LUN directly; bypasses VMFS'),
    L('  pNFS    = parallel NFS; NFSv4.1 feature; multiple I/O paths to same mount'),
    L('  naa.    = Network Address Authority; ESXi canonical name for a storage device'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('Storage Protocol Stack — Comparison', d))

# 9. HA Admission Control
d = [
    top('vSphere HA — Admission Control Modes'),
    blank(),
    L('Admission Control ensures the cluster retains enough spare capacity to restart all'),
    L('VMs from N failed hosts. It blocks VM power-on if headroom would drop below the policy.'),
    blank(),
    itop(),
    ititle('Cluster Resource Percentage', 'Slot Policy'),
    divider(),
    irow(' Default mode in vSphere 6.5+', ' Legacy mode; still available'),
    irow(' Reserve X% of total cluster', ' Slot = largest VM CPU + largest VM'),
    irow('   CPU and memory as failover', '   memory in cluster'),
    irow('   capacity (e.g. 25% each)', ' Slots reserved = hosts to tolerate'),
    irow(' Simple: easy to reason about', ' Conservative: one large VM inflates'),
    irow(' Adjustable per cluster', '   slot size for all VMs'),
    ifiller(),
    ibot(),
    blank(),
    L('  Dedicated Failover Hosts mode:'),
    L('    Named ESXi hosts held completely idle — reserved exclusively for HA recovery.'),
    L('    No VMs run on them normally; they are powered on and waiting.'),
    L('    Most resource-expensive option; guarantees instant failover capacity.'),
    blank(),
    L('  Admission Control enforcement:'),
    L('    vCenter blocks VM power-on if the operation would consume reserved failover capacity.'),
    L('    DRS does not migrate VMs to failover hosts (VM-Host anti-affinity rule auto-created).'),
    blank(),
    L('  HA restarts VMs in priority order: High → Medium → Low → Disabled'),
    L('  VM Monitoring: restarts a VM if VMware Tools heartbeat fails for > threshold seconds'),
    blank(),
    L('  AC      = Admission Control; enforced by vCenter HA; not by ESXi itself'),
    L('  Slot    = unit of failover reservation; slot policy sizes slot to worst-case VM'),
    L('  FTH     = Failures To Host (tolerate); HA restarts VMs after this many host failures'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('vSphere HA — Admission Control', d))

# 10. Proactive HA
d = [
    top('Proactive HA — Hardware Degradation Response'),
    blank(),
    L('Proactive HA works alongside DRS to evacuate VMs from hosts showing hardware degradation'),
    L('before the hardware fails — rather than reacting after failure.'),
    blank(),
    L('  Flow:'),
    blank(),
    L('  ① Hardware health event'),
    L('       Server management agent (IPMI/iDRAC/iLO) or partner module detects:'),
    L('       degraded fan, PSU failure, memory ECC errors, NIC errors, temperature warning'),
    blank(),
    L('  ② vCenter receives health update'),
    L('       CIM provider or Proactive HA provider sends event to vCenter'),
    L('       vCenter marks host with a degradation level: Moderate or Severe'),
    blank(),
    L('  ③ DRS generates evacuation recommendation'),
    L('       Moderate → DRS quarantines host: no new VMs placed; existing VMs may stay'),
    L('       Severe   → DRS recommends evacuating all VMs off the host immediately'),
    blank(),
    L('  ④ VMs migrated proactively'),
    L('       vMotion moves VMs to healthy hosts in cluster before hardware failure'),
    L('       Host enters Quarantine Mode or Maintenance Mode per severity'),
    blank(),
    L('  ⑤ Hardware repaired'),
    L('       Admin repairs hardware → clears degradation state → host re-enters cluster'),
    blank(),
    L('  Proactive HA = DRS extension; requires Proactive HA provider (Dell, HPE, Lenovo, etc.)'),
    L('  Quarantine   = host receives no new VMs but existing VMs can stay (Moderate)'),
    L('  Maintenance  = host evacuated completely; no VMs running (Severe)'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('Proactive HA — Hardware Degradation Flow', d))

# 11. NIOC
d = [
    top('NIOC — Network I/O Control Traffic Classes'),
    blank(),
    L('NIOC divides physical uplink bandwidth among competing traffic types using shares,'),
    L('reservations, and limits — preventing any single traffic class from starving others.'),
    blank(),
    L('  Physical uplink (e.g. 2 × 25 GbE = 50 Gbps aggregate per host)'),
    L('  │'),
    L('  ├── System Traffic Classes (configured on the dvSwitch):'),
    L('  │     Management        shares: 20   limit: none   reservation: 0 Mbps'),
    L('  │     vMotion           shares: 50   limit: none   reservation: 0 Mbps'),
    L('  │     vSAN              shares: 100  limit: none   reservation: 0 Mbps'),
    L('  │     vSphere Repl.     shares: 50   limit: none   reservation: 0 Mbps'),
    L('  │     iSCSI             shares: 50   limit: none   reservation: 0 Mbps'),
    L('  │     NFS               shares: 50   limit: none   reservation: 0 Mbps'),
    L('  │     FT Logging        shares: 50   limit: none   reservation: 0 Mbps'),
    L('  │'),
    L('  └── VM Traffic (per port group):'),
    L('        Each port group can set shares (High/Normal/Low) + optional bandwidth limit'),
    L('        Applies when uplink is congested; no enforcement at < 75% utilisation'),
    blank(),
    L('  Enforcement: NIOC only activates when an uplink exceeds 75% utilisation threshold.'),
    L('  Below that, all traffic flows at line rate. Above it, shares determine allocation.'),
    blank(),
    L('  NIOC    = Network I/O Control; requires dvSwitch (Enterprise Plus licence)'),
    L('  Shares  = relative priority during congestion; vSAN 2x management gets 5x more'),
    L('  Limit   = hard ceiling in Mbps/Gbps; enforced even when uplink is idle'),
    L('  Reserv. = guaranteed Mbps always available; cluster must be able to meet total'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('NIOC — Network I/O Control', d))

# 12. vLCM Image Workflow
d = [
    top('vSphere Lifecycle Manager — Image-Based Upgrade'),
    blank(),
    L('vLCM manages ESXi hosts using a cluster image (base ESXi + add-on VIBs + firmware).'),
    L('Compliance-based workflow: define desired state → measure deviation → remediate.'),
    blank(),
    L('  ① Define Cluster Image'),
    L('       Base ESXi release  +  vendor add-ons (driver VIBs)  +  firmware spec'),
    L('       Stored in SDDC depot (online) or imported from offline bundle'),
    blank(),
    L('  ② Check for Recommended Image'),
    L('       vLCM queries depot for latest validated image for this hardware'),
    L('       Hardware Compatibility Check: cross-references host HCL automatically'),
    blank(),
    L('  ③ Compliance Check'),
    L('       vLCM compares each host installed components against cluster image'),
    L('       Non-compliant hosts listed with delta: missing VIBs, wrong firmware version'),
    blank(),
    L('  ④ Pre-check'),
    L('       Validates host is ready for remediation: no open VMs, DRS enabled,'),
    L('       sufficient cluster capacity to evacuate one host at a time'),
    blank(),
    L('  ⑤ Remediation (rolling, one host at a time)'),
    L('       DRS evacuates host → host enters maintenance mode → vLCM applies image'),
    L('       Host reboots → vLCM validates installed version → exits maintenance mode'),
    blank(),
    L('  ⑥ Post-check'),
    L('       All hosts compliant → cluster image version confirmed → health checks pass'),
    blank(),
    L('  vLCM image  = desired state: base ESXi + add-ons + firmware spec'),
    L('  Baseline    = legacy VUM approach; vLCM images replace baselines in vSphere 7+'),
    L('  HW compat.  = vLCM queries VMware HCL API; flags unsupported driver/firmware combos'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('vSphere Lifecycle Manager — Image Workflow', d))

# 13. DPU / SmartNIC Architecture
d = [
    top('vSphere 8 — DPU (Data Processing Unit) Architecture'),
    blank(),
    L('A DPU (SmartNIC) offloads networking and security from the host CPU to a dedicated'),
    L('processor on the NIC, freeing all host CPU cycles for VM workloads.'),
    blank(),
    itop(),
    ititle('Without DPU (traditional ESXi)', 'With DPU (vSphere 8 + SmartNIC)'),
    divider(),
    irow(' Host CPU handles everything:', ' Host CPU: VM compute only'),
    irow('  · VM guest OS compute', ' DPU handles all I/O plane work:'),
    irow('  · NSX networking (overlay)', '  · vNIC I/O + packet processing'),
    irow('  · DFW rule evaluation', '  · NSX overlay encap/decap'),
    irow('  · Encryption/decryption', '  · Distributed Firewall rules'),
    irow('  · vSwitch / uplink mgmt', '  · Encryption offload'),
    irow(' CPU% used for networking', ' Networking CPU% ≈ 0 on host CPU'),
    ifiller(),
    ibot(),
    blank(),
    L('  DPU components (e.g. NVIDIA BlueField, Pensando/AMD):'),
    L('    · ARM processors on NIC SoC  · On-NIC RAM (8–32 GB)  · PCIe host interface'),
    L('    · Runs a separate ESXi instance (ESXi-DPU) or management agent'),
    blank(),
    L('  vSphere 8 integration:'),
    L('    · vCenter manages DPU as part of host inventory'),
    L('    · NSX policies pushed to DPU directly; no host CPU involvement for DFW'),
    L('    · vSphere Distributed Services Engine = feature name for DPU offload in vSphere 8'),
    blank(),
    L('  DPU   = Data Processing Unit; SmartNIC with dedicated ARM CPUs and RAM'),
    L('  SoC   = System on Chip; the DPU processor integrating CPU + NIC + crypto'),
    L('  DSE   = vSphere Distributed Services Engine; the DPU offload feature in vSphere 8'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('DPU / SmartNIC — Architecture', d))

# 14. vTPM + Secure Boot
d = [
    top('VM Security — vTPM & Secure Boot Chain'),
    blank(),
    L('vTPM provides a virtualised Trusted Platform Module 2.0 to guest VMs. Secure Boot'),
    L('validates the OS bootloader signature before the OS kernel loads — at UEFI layer.'),
    blank(),
    L('  Secure Boot chain (UEFI firmware → OS):'),
    blank(),
    L('  ① UEFI firmware (OVMF in VMware)'),
    L('       Contains Platform Key (PK), Key Exchange Keys (KEK), allowed DB signers'),
    L('       Validates signature of bootloader before executing it'),
    blank(),
    L('  ② Bootloader (GRUB2 / Windows Boot Manager)'),
    L('       Must be signed by a key in UEFI DB (Microsoft or custom CA)'),
    L('       Bootloader then validates OS kernel signature'),
    blank(),
    L('  ③ OS Kernel'),
    L('       Signed kernel modules only (Secure Boot enforced at kernel level too)'),
    L('       Unsigned drivers blocked — common source of Secure Boot failures on ESXi'),
    blank(),
    L('  vTPM provides (per VM):'),
    L('    · PCR (Platform Configuration Registers) — measurements of boot chain integrity'),
    L('    · Key storage — BitLocker encryption keys sealed to TPM PCR state'),
    L('    · Attestation — prove to remote party that VM booted from expected software'),
    L('    · vTPM state stored encrypted in VM files; requires vCenter KMS to unseal'),
    blank(),
    L('  Requirements for vTPM:'),
    L('    · VM hardware version 14+  · EFI firmware (not BIOS)  · vCenter KMS configured'),
    blank(),
    L('  vTPM   = virtual TPM 2.0; provided by vSphere; no physical TPM on host needed'),
    L('  PCR    = Platform Config Register; hash chain of boot measurements stored in TPM'),
    L('  VBS    = Virtualisation Based Security (Windows); uses vTPM + Hyper-V compatibility'),
    L('  UEFI   = Unified Extensible Firmware Interface; replaces BIOS; required for vTPM'),
    blank(),
    bot(),
]
ESXI_SECTIONS.append(section('vTPM & Secure Boot Chain', d))


# ══ vSAN how-it-works additions ════════════════════════════════════════════════

VSAN_SECTIONS = []

# 15. SIOC
d = [
    top('SIOC — Storage I/O Control Congestion Management'),
    blank(),
    L('SIOC monitors a shared datastore for latency congestion. When latency exceeds the'),
    L('threshold, it enforces per-VM I/O shares to prevent noisy VMs starving others.'),
    blank(),
    L('  Normal state (latency below threshold):'),
    L('  │  No SIOC enforcement  ·  All VMs issue I/O at full speed  ·  Threshold: 30 ms default'),
    blank(),
    L('  Congested state (latency ≥ threshold):'),
    L('  │'),
    L('  ├── SIOC activates — measures each VM I/O demand'),
    L('  ├── Distributes IOPS proportionally according to per-VM shares:'),
    L('  │     VM-A  shares: High  (2000) → gets 4× more IOPS than VM-C'),
    L('  │     VM-B  shares: Normal (1000) → gets 2× more IOPS than VM-C'),
    L('  │     VM-C  shares: Low   (500)  → gets baseline allocation'),
    L('  └── SIOC throttles VMs exceeding their share allocation via I/O scheduler'),
    blank(),
    L('  SIOC vs NIOC:'),
    L('  ┌──────────────────────────────────────┬───────────────────────────────────────┐'),
    L('  │  SIOC                                │  NIOC                                 │'),
    L('  │  Storage I/O Control                 │  Network I/O Control                  │'),
    L('  │  Shared datastore throttling         │  Shared uplink throttling             │'),
    L('  │  Triggered by latency threshold      │  Triggered by uplink % saturation     │'),
    L('  │  Per-VM shares on VMDK               │  Per traffic-class shares             │'),
    L('  └──────────────────────────────────────┴───────────────────────────────────────┘'),
    blank(),
    L('  SIOC        = Storage I/O Control; requires Enterprise Plus; enabled per datastore'),
    L('  Threshold   = latency (ms) that triggers SIOC; default 30 ms; tune per array type'),
    L('  Shares      = per-VM relative priority; same High/Normal/Low as CPU/mem shares'),
    L('  IOPS limit  = absolute cap per VM VMDK; enforced regardless of contention'),
    blank(),
    bot(),
]
VSAN_SECTIONS.append(section('SIOC — Storage I/O Control', d))


# ── write logic ────────────────────────────────────────────────────────────────

def append_sections(filepath, sections):
    with open(filepath) as f:
        content = f.read()

    additions = []
    for sec in sections:
        additions.extend(sec)

    # Check for duplicates
    skipped = []
    to_add = []
    for sec in sections:
        heading = next((l for l in sec if l.startswith('## ')), '')
        title = heading.replace('## ', '').strip()
        if title and title in content:
            skipped.append(title)
        else:
            to_add.extend(sec)

    if not to_add:
        print(f'  SKIP (all sections present): {filepath}')
        return 0

    with open(filepath, 'a') as f:
        f.write('\n')
        f.writelines(l + '\n' for l in to_add)

    added = len(sections) - len(skipped)
    print(f'  DONE (+{added} sections): {filepath}')
    if skipped:
        print(f'    skipped (already present): {skipped}')
    return added


def main():
    import os
    os.chdir('/Users/chrisanastasiadis/chris-kb')

    total = 0
    total += append_sections(
        'docs/virtualization/vmware/vcenter/architecture/how-it-works/index.md',
        VCENTER_SECTIONS,
    )
    total += append_sections(
        'docs/virtualization/vmware/esxi/architecture/how-it-works/index.md',
        ESXI_SECTIONS,
    )
    total += append_sections(
        'docs/virtualization/vmware/vsan/architecture/how-it-works/index.md',
        VSAN_SECTIONS,
    )
    print(f'\n{total} sections added across 3 files.')


if __name__ == '__main__':
    main()
