#!/usr/bin/env python3
"""
Generate and insert installation-sequence diagrams into virtualization landing pages.
Each diagram follows the same format as docs/virtualization/vmware/index.md.
Run from the repo root: python3 scripts/add_installation_diagrams.py
"""

WIDTH = 105  # total line width including outer │ chars

# ── helpers ────────────────────────────────────────────────────────────────────

def top(title):
    inner = WIDTH - 2
    t = f' {title} '
    dashes = inner - len(t)
    left = dashes // 2
    right = dashes - left
    return '┌' + '─' * left + t + '─' * right + '┐'

def bot():
    return '└' + '─' * (WIDTH - 2) + '┘'

def blank():
    return '│' + ' ' * (WIDTH - 2) + '│'

def line(text):
    """Content line — padded to WIDTH by alignment script on commit."""
    inner = f'  {text}'
    if len(inner) > WIDTH - 2:
        inner = inner[:WIDTH - 2]
    return '│' + inner.ljust(WIDTH - 2) + '│'

def sep():
    """Section separator under step title."""
    return line('─' * 89)

def arrow(label):
    return [
        blank(),
        line(f'                                      │  {label}'),
        line('                                      ▼'),
    ]

def step(number, name, lines):
    out = [line(f'Step {number} · {name}'), sep()]
    for l in lines:
        out.append(line(l))
    return out

def diagram(title, steps_data):
    out = ['```', top(title), blank()]
    for i, (name, content, arrow_label) in enumerate(steps_data):
        out += step(i + 1, name, content)
        if i < len(steps_data) - 1:
            out += arrow(arrow_label)
    out += [blank(), bot(), '```']
    return '\n'.join(out)


# ── diagram definitions ────────────────────────────────────────────────────────

DIAGRAMS = {}

# ── VxRail (top-level) ─────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vxrail/index.md'] = diagram(
    'VxRail Platform — Installation Sequence',
    [
        ('Physical Infrastructure', [
            'Rack VxRail nodes  ·  Cable to ToR switches: mgmt, vSAN, vMotion, VM uplinks',
            'ToR: MTU 9000 on vSAN + vMotion ports  ·  LACP/LAG on uplinks if required',
            'iDRAC: dedicated management port on every node  ·  Out-of-band access confirmed',
            'DNS: A-records for all node FQDNs + VxRail Manager VIP + vCenter FQDN',
            'NTP: two sources reachable from management network  ·  Time sync verified',
        ], 'update firmware on every node'),
        ('iDRAC, BIOS & Firmware', [
            'iDRAC firmware at minimum required version per VxRail compatibility matrix',
            'BIOS: VT-x/AMD-V on  ·  Hyperthreading on  ·  C-states tuned for workload',
            'HBA/NIC firmware at VxRail-qualified levels — verify against VxRail HCL',
            'Boot order: local disk first  ·  PXE disabled  ·  RAID controller configured',
            'All nodes show healthy in iDRAC  ·  No outstanding hardware alerts',
        ], 'run VxRail first-run wizard'),
        ('VxRail Manager Bootstrap', [
            'Boot nodes from VxRail factory image  ·  Nodes receive management IPs',
            'Access VxRail Manager first-run wizard  ·  Set mgmt network, gateway, DNS, NTP',
            'Select deployment type: standard / stretched / two-node  ·  Choose vCenter mode',
            'Input vSAN disk configuration  ·  Wizard validates hardware + network prereqs',
            'Wizard provisions vCenter, SSO, vSAN, VxRail Manager — fully automated bringup',
        ], 'vCenter available post-wizard'),
        ('vCenter & Cluster Validation', [
            'Login to vCenter  ·  All nodes joined cluster  ·  HA and DRS enabled',
            'Licences applied  ·  SSO identity source configured (AD integration if needed)',
            'Distributed switch created by wizard  ·  Confirm port groups and uplinks',
            'vSAN health: all checks green  ·  Objects in compliance  ·  No disk warnings',
            'Alarm baselines set  ·  vCenter backup schedule configured',
        ], 'optional: add NSX overlay networking'),
        ('NSX Integration (optional)', [
            'Deploy NSX Manager appliances via LCM or manually  ·  Register vCenter',
            'Configure transport zones and uplink profiles  ·  TEP pool assigned',
            'Prepare all cluster hosts as host transport nodes  ·  Verify TEP connectivity',
            'Deploy Edge cluster  ·  Configure Tier-0/Tier-1 gateways  ·  BGP/static routing',
            'Micro-segmentation: review default DFW rules  ·  Enable IDS if licensed',
        ], 'lifecycle management and day-2 operations'),
        ('LCM, Monitoring & Day-2', [
            'VxRail LCM: download bundle from Dell  ·  Run pre-check  ·  Schedule window',
            'Register cluster with VMware Cloud (optional)  ·  Enable Skyline Health',
            'Aria Operations: add vCenter adapter  ·  Configure alert policies + dashboards',
            'Backup: vCenter DB schedule  ·  VxRail Manager backup  ·  NSX backup if deployed',
            'Support bundle path documented  ·  iDRAC call-home alerts enabled',
        ], ''),
    ]
)

# ── ESXi ───────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/esxi/index.md'] = diagram(
    'ESXi Host — Installation Sequence',
    [
        ('Physical Host Readiness', [
            'Firmware: server BIOS, HBA, and NIC at vendor-recommended minimum versions',
            'BIOS: VT-x/AMD-V on  ·  Hyperthreading on  ·  NUMA topology visible to OS',
            'Cabling: dedicated NICs for management, vMotion, vSAN, VM traffic (or LACP)',
            'DNS: A + PTR records for host FQDN created before ESXi install',
            'NTP sources reachable  ·  IPMI/iDRAC configured for out-of-band access',
        ], 'boot from ESXi ISO or PXE'),
        ('ESXi Installation', [
            'Boot from ISO (USB, PXE, iDRAC virtual media)  ·  Select install datastore',
            'Set keyboard/locale  ·  Accept EULA  ·  Target disk confirmed',
            'Set root password  ·  Installation completes  ·  Reboot to ESXi',
            'Configure management IP, subnet, gateway via DCUI (F2)',
            'Set hostname (FQDN)  ·  DNS servers  ·  NTP servers  ·  SSH enabled for setup',
        ], 'configure networking'),
        ('Network Configuration', [
            'Assign vmnic(s) to vSwitch0 (management)  ·  vSwitch0: vmk0 IP confirmed',
            'Create vMotion VMkernel on dedicated vSwitch or portgroup  ·  MTU 9000 if jumbo',
            'Create vSAN VMkernel on dedicated portgroup  ·  MTU 9000  ·  vSAN traffic tagged',
            'Additional vSwitches for VM traffic  ·  Uplink teaming policy set (LB / LACP)',
            'Verify connectivity: ping gateway, vCenter FQDN, NTP, DNS from each VMkernel',
        ], 'configure storage paths'),
        ('Storage Configuration', [
            'iSCSI: software initiator enabled  ·  target IPs bound to vmk  ·  CHAP set',
            'Fibre Channel: HBA WWPNs noted  ·  zoning confirmed by storage team',
            'Multipathing: PSP Round Robin for active-active arrays  ·  MRU for active-passive',
            'Local datastore visible  ·  Shared datastores mounted and accessible',
            'VAAI plugin installed if array supports hardware acceleration',
        ], 'add to vCenter'),
        ('Add to vCenter', [
            'In vCenter: Add Host wizard  ·  Enter FQDN  ·  Accept thumbprint  ·  Credentials',
            'Assign licence  ·  Select datacenter and cluster  ·  Confirm placement',
            'Host profile applied if cluster baseline exists  ·  Remediate if needed',
            'HA agent installed automatically  ·  DRS enabled  ·  Host enters Connected state',
            'vSAN disk claim if applicable  ·  Verify host contributes to cluster health',
        ], 'harden and validate'),
        ('Hardening & Baseline', [
            'Lockdown mode: normal lockdown enabled  ·  SSH disabled post-config',
            'Host certificates replaced with CA-signed cert or confirmed thumbprint',
            'NTP service policy: Start and stop with host  ·  NTP confirmed synced',
            'Syslog forwarded to Aria Ops for Logs / syslog server  ·  Log level set',
            'Baseline remediation: patches applied via vSphere Lifecycle Manager',
        ], ''),
    ]
)

# ── vCenter ───────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/vcenter/index.md'] = diagram(
    'vCenter Server — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS: A-record and PTR for vCenter FQDN created  ·  Resolves from all hosts',
            'NTP: two sources reachable  ·  ESXi hosts already time-synced',
            'Service account in AD: SSO admin, AD join credentials ready',
            'Certificates: CA ready to sign or self-signed accepted per policy',
            'Target datastore free space: ≥550 GB (small), ≥1150 GB (medium), ≥1700 GB (large)',
        ], 'deploy VCSA OVA'),
        ('VCSA Deploy — Stage 1', [
            'Mount VCSA ISO  ·  Launch installer (UI or CLI)  ·  Select Deploy',
            'Enter ESXi host FQDN + credentials  ·  Accept host thumbprint',
            'VM name, size selection (tiny/small/medium/large/x-large)',
            'Select datastore  ·  Set network, IP, gateway, DNS, FQDN',
            'Stage 1 completes: VCSA VM powered on, OS booted, ready for Stage 2',
        ], 'complete Stage 2 configuration'),
        ('VCSA Configure — Stage 2', [
            'Connect to Stage 2 wizard at https://vcsa-fqdn:5480',
            'NTP servers entered  ·  SSH access: enable for setup, disable post-config',
            'SSO domain name (vsphere.local or custom)  ·  SSO admin password set',
            'Inventory size: select to match expected VM/host count for DB sizing',
            'Stage 2 completes: vCenter services start  ·  vSphere Client accessible',
        ], 'integrate with Active Directory'),
        ('AD Integration & Identity', [
            'Add AD identity source: Administration → SSO → Identity Sources',
            'Service account for LDAP bind  ·  Base DN for users and groups',
            'Assign AD groups to vCenter roles: administrators, read-only, operators',
            'Verify AD login works  ·  Remove default permissions after role mapping',
            'Confirm token lifetime and lockout policy match security baseline',
        ], 'build inventory'),
        ('Inventory Build', [
            'Create datacenter object  ·  Add cluster  ·  Configure HA and DRS settings',
            'Add all ESXi hosts to cluster  ·  Hosts enter connected state',
            'Create distributed switch  ·  Migrate hosts from vSS to vDS uplinks',
            'Configure port groups: management, vMotion, vSAN, VM networks',
            'Assign licences to hosts and cluster  ·  Verify no licence warnings',
        ], 'validate and harden'),
        ('Post-Install Validation', [
            'Configure alarm definitions: host disconnect, datastore full, HA failure',
            'vCenter backup: File-Based Backup (FTP/SCP/HTTP) schedule configured daily',
            'Certificate: replace MACHINE_SSL_CERT with CA-signed if required',
            'Skyline Health: enable and confirm green status for vCenter',
            'SNMP or syslog forwarding configured for monitoring platform',
        ], ''),
    ]
)

# ── vSAN ──────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/vsan/index.md'] = diagram(
    'vSAN — Installation Sequence',
    [
        ('Pre-Checks', [
            'All hosts in cluster have vSAN VMkernel adapter  ·  MTU 9000 confirmed',
            'vSAN HCL: SSD/NVMe cache tier and HDD/NVMe capacity tier all listed',
            'Minimum disk requirements: 1 cache + 1 capacity per disk group per host',
            'Network: dedicated 10 GbE+ uplinks for vSAN traffic  ·  No shared vMotion',
            'Cluster has ≥3 hosts for FTT=1  ·  ≥5 hosts for RAID-5 erasure coding',
        ], 'enable vSAN on cluster'),
        ('Enable vSAN', [
            'vCenter → Cluster → Configure → vSAN → Turn On',
            'Select single-site or stretched cluster  ·  Enable deduplication/compression',
            'Fault domains: configure if multi-rack to honour rack-level failure tolerance',
            'Encryption: enable at rest if data-at-rest policy requires it',
            'vSAN bootstrap: first disk group created on each host during wizard',
        ], 'claim disks and configure disk groups'),
        ('Disk Group Configuration', [
            'Claim cache tier (NVMe/SSD)  ·  Claim capacity tier (NVMe/SSD/HDD)',
            'Disk format: disk group type — hybrid or all-flash  ·  On-disk format v14+',
            'Add capacity hosts: each host must contribute at least one disk group',
            'Verify disk groups healthy: no degraded, absent, or inaccessible components',
            'Capacity: confirm usable capacity matches expected after FTT overhead',
        ], 'configure storage policies'),
        ('Storage Policy Configuration', [
            'Create SPBM policies: FTT=1 RAID-1 (default), FTT=1 RAID-5, FTT=2 RAID-6',
            'Assign default policy to cluster  ·  VM home namespace policy set',
            'Tag-based placement rules if multiple datastores or fault domains exist',
            'Test policy compliance: deploy test VM, confirm object placement correct',
            'Verify existing VM storage objects are compliant (no yellow/red warnings)',
        ], 'migrate workloads'),
        ('Workload Migration', [
            'svMotion existing VMs from local/NFS datastores to vSAN datastore',
            'Monitor resyncing objects: vSAN → Monitor → Resyncing Objects',
            'Confirm all objects reach Healthy state after migration',
            'Remove old datastores and disconnect legacy storage paths if decommissioning',
            'Performance: enable vSAN Performance Service for per-VM IOPS dashboards',
        ], 'health, monitoring and day-2'),
        ('Health & Monitoring', [
            'vSAN Health Service: run full check  ·  Resolve any warnings before production',
            'Network partition test: verify all hosts see same vSAN partition',
            'Proactive rebalance: run if capacity usage is uneven across hosts',
            'Skyline Health: onboard cluster for ongoing vSAN health recommendations',
            'Backup: configure VM-level backup via Veeam/Commvault before go-live',
        ], ''),
    ]
)

# ── NSX ───────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/nsx/index.md'] = diagram(
    'NSX-T — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS/NTP confirmed on all hosts and vCenter  ·  vCenter trust established',
            'Management network: dedicated IPs for 3 NSX Manager nodes + 1 VIP reserved',
            'MTU 9000 on all physical switches for TEP (GENEVE encapsulation) traffic',
            'Host firmware and NIC drivers on NSX HCL  ·  vCenter version compatible',
            'Edge VM sizing: medium (4 vCPU/8 GB) minimum  ·  bare-metal for high throughput',
        ], 'deploy NSX Manager cluster'),
        ('NSX Manager Deployment', [
            'Deploy NSX Manager OVA on first ESXi host  ·  Set size: medium or large',
            'Set management IP, gateway, DNS, NTP  ·  Set admin + audit passwords',
            'Login to NSX Manager UI  ·  Accept EULA  ·  Enter licence key',
            'Deploy second and third NSX Manager nodes  ·  Join to form 3-node cluster',
            'Configure VIP (virtual IP) for NSX Manager cluster  ·  Confirm all nodes UP',
        ], 'register vCenter and configure transport'),
        ('Transport Zones & Profiles', [
            'Add vCenter as compute manager  ·  Accept thumbprint  ·  Sync completes',
            'Create overlay transport zone  ·  Create VLAN transport zone',
            'Create uplink profile: active/standby or LACP  ·  MTU 9000  ·  VLAN for TEP',
            'Create TEP IP pool: range of IPs on TEP subnet allocated per host/edge',
            'Host switch profile: maps physical NICs to logical uplinks',
        ], 'prepare hosts as transport nodes'),
        ('Host Transport Node Preparation', [
            'System → Fabric → Hosts: select all cluster hosts  ·  Configure NSX',
            'Select transport zone, uplink profile, TEP pool  ·  Apply to cluster',
            'Monitor host prep status: each host transitions to Success state',
            'Verify TEP IPs assigned  ·  TEP-to-TEP connectivity (ping from host)',
            'NSX kernel modules loaded on all hosts  ·  No host in degraded state',
        ], 'deploy and configure Edge nodes'),
        ('Edge Cluster Deployment', [
            'Deploy Edge VM OVA on ESXi hosts (or bare-metal)  ·  Size: medium+',
            'Edge transport node config: overlay TZ, VLAN TZ, uplink profile, TEP pool',
            'Create Edge cluster  ·  Add both Edge nodes  ·  BFD between edges enabled',
            'Tier-0 gateway: create, assign to Edge cluster  ·  Uplink port to physical router',
            'BGP or static routing: configure on Tier-0  ·  Confirm route advertisement',
        ], 'configure logical networking'),
        ('Logical Networking & Firewall', [
            'Tier-1 gateway: linked to Tier-0  ·  Route advertisement for connected segments',
            'Segments: create logical segments  ·  Assign to Tier-1 or as standalone',
            'Distributed Firewall: review default allow rules  ·  Create baseline deny policy',
            'Micro-segmentation: tag VMs with NSX groups  ·  Apply workload-based policies',
            'Enable Gateway Firewall on Tier-0/Tier-1 for perimeter controls',
        ], ''),
    ]
)

# ── Aria Suite Lifecycle Manager ───────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/aria-suite-lifecycle/index.md'] = diagram(
    'Aria Suite Lifecycle Manager — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS A-record for LCM FQDN  ·  PTR record created  ·  Resolves from vCenter',
            'NTP sources confirmed  ·  vCenter service account with admin rights prepared',
            'Certificate Authority ready: LCM will need signed certs for all products',
            'Target datastore: ≥50 GB free for LCM VM  ·  Product datastores sized separately',
            'Internet or proxy access for downloading product binaries and patches',
        ], 'deploy LCM OVA'),
        ('LCM OVA Deployment', [
            'Download Aria Suite Lifecycle OVA from VMware portal',
            'Deploy OVA on vCenter: size small (labs) or medium (production)',
            'Set management IP, gateway, DNS, NTP, admin password during deploy wizard',
            'Power on  ·  Access LCM UI at https://lcm-fqdn  ·  Initial login (admin/)',
            'Run initial setup wizard  ·  Accept EULA  ·  Enter licence key',
        ], 'configure certificates'),
        ('Certificate Configuration', [
            'Upload CA root and intermediate certificates to LCM trust store',
            'Create certificate request for LCM itself: CN = LCM FQDN, SANs included',
            'Sign CSR with internal CA  ·  Import signed cert into LCM',
            'Configure LCM to use CA-signed cert for all future product deployments',
            'Verify LCM UI accessible with trusted cert  ·  No browser warnings',
        ], 'integrate vCenter and identity'),
        ('vCenter & Identity Integration', [
            'Lifecycle Operations → Settings → vCenter Servers: add vCenter + credentials',
            'Add identity provider: Workspace ONE Access or vIDM appliance',
            'Map AD groups to LCM roles: admin, operator, viewer',
            'Configure SMTP relay for email notifications (patch, deployment alerts)',
            'Test vCenter connectivity: verify LCM can browse inventory',
        ], 'onboard or deploy Aria products'),
        ('Product Onboard / Deploy', [
            'Lifecycle Operations → Environments → Create Environment',
            'Add products: Aria Operations, Aria Automation, Aria Ops for Logs, etc.',
            'For existing installs: import environment (discover from vCenter)',
            'For new installs: select binary, size, network, datastore  ·  LCM deploys',
            'Monitor deployment tasks  ·  Each product validated post-deploy by LCM',
        ], 'day-2 operations'),
        ('Day-2 Operations', [
            'Patch management: Lifecycle Operations → Environments → Trigger Upgrade',
            'Backup: configure snapshot/backup for LCM VM and all managed products',
            'Certificate renewal: LCM tracks cert expiry  ·  Automates renewal workflow',
            'Scale: add worker nodes or replicas through LCM for capacity growth',
            'Health: LCM health dashboard shows deployment and cert status per product',
        ], ''),
    ]
)

# ── Aria Operations ────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/aria-operations/index.md'] = diagram(
    'Aria Operations (vROps) — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS A-record for master node FQDN + VIP  ·  PTR records created',
            'NTP confirmed  ·  vCenter service account with read-only minimum rights',
            'Datastore sizing: master ≥500 GB, analytics node ≥200 GB per additional node',
            'Network: management port and NFS analytics store port reachable',
            'Decide deployment size: standard (≤1500 objects) or large (≤3000+)',
        ], 'deploy master node OVA'),
        ('Master Node Deployment', [
            'Deploy Aria Operations OVA on vCenter  ·  Select size: small/medium/large',
            'Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password',
            'Power on  ·  Access admin UI at https://vrops-fqdn  ·  Initial setup wizard',
            'Accept EULA  ·  Enter licence  ·  Choose master or replica role: Master',
            'Wait for cluster to initialise  ·  Master node transitions to Running state',
        ], 'add replica and collector nodes'),
        ('Replica & Collector Nodes', [
            'Deploy additional OVAs for each data node  ·  Role: Data (replica)',
            'Join each data node to master cluster using admin UI → Cluster Management',
            'Remote Collectors: deploy lightweight collector OVA for remote sites',
            'Assign collector groups to define which adapters run on which collector',
            'Cluster health: all nodes green  ·  Online status confirmed before next step',
        ], 'add vCenter cloud account'),
        ('vCenter Adapter & Cloud Account', [
            'Add vCenter cloud account: Data Sources → Add  ·  Enter vCenter FQDN + creds',
            'Accept vCenter thumbprint  ·  Collection cycle starts immediately',
            'Verify objects discovered: hosts, clusters, VMs, datastores visible',
            'Enable continuous discovery for new VM detection  ·  Collection interval: 5 min',
            'Check adapter health: green status in Data Sources panel',
        ], 'add additional adapters'),
        ('Additional Adapters & Management Packs', [
            'NSX Adapter: add NSX Manager  ·  Topology maps and flow data collected',
            'Storage adapters: Pure1, Dell CloudIQ, NetApp adapters from marketplace',
            'OS agents: deploy Aria Operations agent on Linux/Windows VMs for in-guest',
            'Third-party: SNMP adapter for physical network devices  ·  Custom metrics',
            'Management packs installed from VMware Marketplace  ·  Restart collector if needed',
        ], 'configure dashboards and alerts'),
        ('Dashboards, Alerts & Reports', [
            'Import VMware default dashboards  ·  Assign to user groups',
            'Configure alert definitions: capacity, performance, availability thresholds',
            'Notification plugins: email, Slack, ServiceNow webhook  ·  Route by severity',
            'Compliance: assign regulatory benchmarks (PCI, CIS) to objects',
            'Reports: schedule weekly capacity and health reports  ·  Email distribution list',
        ], ''),
    ]
)

# ── Aria Automation ────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/aria-automation/index.md'] = diagram(
    'Aria Automation — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'Aria Suite LCM deployed and operational  ·  vCenter registered in LCM',
            'Workspace ONE Access (vIDM) deployed and AD-integrated',
            'DNS for all Aria Automation service FQDNs: aac, aap, pipeline, service-broker',
            'Certificates: CA ready to sign SAN certs for all Aria Automation services',
            'Datastore: ≥250 GB for standard deployment  ·  Additional per scale tier',
        ], 'deploy via LCM'),
        ('Deploy via Aria Suite LCM', [
            'LCM → Lifecycle Operations → Environments → Add Product: Aria Automation',
            'Select binary version  ·  Choose deployment size: standard / enterprise',
            'Map vCenter, datastore, network  ·  Enter FQDNs for each service component',
            'Configure certificates  ·  Set admin credentials  ·  Start deployment',
            'Monitor LCM deployment log  ·  Deployment takes 60–90 minutes',
        ], 'add cloud accounts'),
        ('Cloud Account Configuration', [
            'Login to Aria Automation  ·  Infrastructure → Cloud Accounts → Add',
            'Add vCenter cloud account: FQDN, credentials, accept thumbprint',
            'Optionally add AWS, Azure, GCP accounts for multi-cloud support',
            'Data collection starts  ·  Hosts, clusters, datastores, networks discovered',
            'Verify resource inventory populated: Infrastructure → Resources',
        ], 'configure projects and cloud zones'),
        ('Projects & Cloud Zones', [
            'Cloud Zones: define per vCenter cluster with constraints (CPU/memory limits)',
            'Projects: create per team or environment  ·  Assign cloud zones to project',
            'Flavour mappings: map standard T-shirt sizes to vCenter VM resource specs',
            'Image mappings: map logical names to VM templates per cloud account',
            'Network profiles: define IP ranges, DNS, gateway per project network',
        ], 'create blueprints and templates'),
        ('Blueprints & Templates', [
            'Blueprint Designer: YAML or graphical  ·  Add vSphere.Machine resource block',
            'Inputs: define parameters (flavour, image, count, custom props)',
            'Cloud Config / cloud-init: OS customisation, package install, scripts',
            'ABX Actions: attach pre/post-provision serverless scripts if needed',
            'Versioning: publish blueprint version  ·  Share to Service Broker catalogue',
        ], 'day-2 and governance'),
        ('Day-2 & Governance', [
            'Approval policies: require approval for large VM sizes or production deployments',
            'Lease policies: auto-reclaim after N days  ·  Extend / delete on expiry',
            'Pipeline: CI/CD integration  ·  Define stages: test → staging → production',
            'RBAC: assign project roles to AD groups  ·  Principle of least privilege',
            'Integrations: ServiceNow CMDB sync  ·  Jira ticket per deployment',
        ], ''),
    ]
)

# ── Aria Operations for Logs ───────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/aria-operations-for-logs/index.md'] = diagram(
    'Aria Operations for Logs — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS A-record for master node FQDN and VIP  ·  PTR record created',
            'NTP confirmed  ·  Firewall: ports 514 (syslog UDP), 6514 (TLS), 9543 open',
            'Datastore: ≥530 GB for master  ·  ≥530 GB per worker node',
            'Estimate log ingest rate: average environment generates 5–20 GB/day',
            'vCenter read-only service account for vSphere content pack integration',
        ], 'deploy master node OVA'),
        ('Master Node Deployment', [
            'Deploy Aria Ops for Logs OVA on vCenter  ·  Size: small / medium / large',
            'Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password',
            'Power on  ·  Access admin UI at https://loginsight-fqdn  ·  Setup wizard',
            'Accept EULA  ·  Enter licence  ·  Master node initialises log index',
            'Confirm master node Running state before adding workers',
        ], 'add worker nodes for HA'),
        ('Worker Node Deployment', [
            'Deploy 2+ additional worker OVAs  ·  Role: Worker',
            'Join each worker to master via Admin UI → Cluster → Add Worker',
            'Workers receive log forwarding configuration from master automatically',
            'Cluster enters active-active mode: logs distributed across all nodes',
            'Verify cluster health: all nodes green  ·  No missing shards',
        ], 'configure log sources'),
        ('Log Sources & Agent Install', [
            'vSphere Content Pack: add vCenter  ·  ESXi syslog auto-configured via pack',
            'Agents: install Aria Ops for Logs agent on Linux/Windows VMs',
            'Syslog sources: configure physical switches, firewalls to forward to VIP:514',
            'TLS syslog: configure sources to use port 6514 with cert validation',
            'Verify each source appears in Explore Logs with correct log stream',
        ], 'install content packs'),
        ('Content Packs', [
            'Install built-in packs: VMware vSphere, NSX-T, vSAN, Linux, Windows',
            'Content packs auto-create dashboards, queries, and alert definitions',
            'NSX content pack: forwards DFW flows and manager audit logs',
            'Third-party packs: available from VMware Marketplace for firewalls, DBs, apps',
            'Verify dashboards populate with live data  ·  Adjust time range filters',
        ], 'configure alerts and forwarding'),
        ('Alerts & Log Forwarding', [
            'Alert queries: create threshold-based alerts on error patterns',
            'Notification channels: email, webhook (Slack, PagerDuty, ServiceNow)',
            'Log forwarding: forward filtered events to SIEM (Splunk, Elasticsearch)',
            'Retention policy: default 30 days  ·  Adjust archive tier if compliance requires',
            'Integration: connect to Aria Operations for correlated infrastructure alerts',
        ], ''),
    ]
)

# ── Aria Operations for Networks ───────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/aria-operations-for-networks/index.md'] = diagram(
    'Aria Operations for Networks — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'DNS A-records for platform node and data node FQDNs  ·  PTR records created',
            'NTP confirmed  ·  vCenter + NSX Manager service accounts prepared',
            'Physical switch SNMP community or SNMPv3 credentials available',
            'IPFIX: physical switches and NSX VDS support flow export',
            'Datastore: ≥200 GB for platform node  ·  ≥200 GB per data node',
        ], 'deploy platform node OVA'),
        ('Platform Node Deployment', [
            'Deploy Aria Ops for Networks OVA  ·  Role: Platform',
            'Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password',
            'Power on  ·  Access UI at https://vrni-fqdn  ·  Initial setup wizard',
            'Accept EULA  ·  Enter licence  ·  Platform node initialises',
            'Confirm platform Running state before deploying proxy/data nodes',
        ], 'deploy proxy/data nodes'),
        ('Proxy Node Deployment', [
            'Deploy Proxy OVA  ·  Role: Proxy (also called data source node)',
            'During deploy, enter platform node FQDN and shared secret pairing key',
            'Proxy joins platform cluster  ·  Appears in Admin → Infrastructure',
            'Deploy additional proxies for scale or geographic separation if needed',
            'Verify all proxies connected and showing green health in platform UI',
        ], 'add data sources'),
        ('Data Source Configuration', [
            'Add vCenter: Infrastructure → Data Sources → Add vCenter  ·  Creds + thumbprint',
            'Add NSX Manager: enter NSX FQDN + credentials  ·  Topology sync begins',
            'Physical network: add switches via SNMP  ·  Read community / v3 credentials',
            'Verify data collection: Infrastructure → Data Sources  ·  All sources green',
            'Network topology auto-builds: VMs → logical → physical overlay visible',
        ], 'configure flow collection'),
        ('Flow Collection (IPFIX)', [
            'NSX: enable IPFIX in NSX Manager  ·  Collector IP = proxy node management IP',
            'VDS: configure IPFIX export on distributed switch  ·  Collector IP + port 2055',
            'Physical switches: configure NetFlow/IPFIX export toward proxy node',
            'Verify flows arrive: Network Map → select entity → view flows',
            'Flow data enables application discovery, security group recommendations',
        ], 'configure dashboards and security groups'),
        ('Dashboards & Security Planning', [
            'Topology maps: browse VM-to-VM paths  ·  Identify unplanned traffic flows',
            'Application discovery: AI groups related VMs into application constructs',
            'Security groups: recommended NSX micro-segmentation rules from observed flows',
            'Alerts: configure for new open ports, policy violations, topology changes',
            'Reports: schedule weekly traffic analysis and security posture reports',
        ], ''),
    ]
)

# ── SRM ────────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/srm/index.md'] = diagram(
    'Site Recovery Manager — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'Two vCenter sites operational: protected site and recovery site',
            'Network connectivity between sites: SRM ports 443, 8095, 9086 open',
            'Replication mechanism in place: array-based (SRDF, RecoverPoint) or vSphere Replication',
            'DNS: SRM appliance FQDNs resolvable from both sites',
            'vCenter Enhanced Linked Mode or at minimum both sites independently operational',
        ], 'deploy SRM at protected site'),
        ('SRM Appliance — Protected Site', [
            'Deploy SRM OVA on protected site vCenter  ·  Select size based on VM count',
            'Set FQDN, management IP, gateway, DNS, NTP  ·  Set admin password',
            'Register SRM with local vCenter: enter vCenter FQDN + SSO credentials',
            'SRM plugin appears in vSphere Client  ·  Confirm plugin loads without errors',
            'Enter SRM licence key  ·  Protected site SRM Ready state confirmed',
        ], 'deploy SRM at recovery site'),
        ('SRM Appliance — Recovery Site', [
            'Deploy SRM OVA on recovery site vCenter using same procedure',
            'Register with recovery site vCenter  ·  Confirm plugin loads',
            'Pair recovery site SRM with protected site SRM: Site Pairing wizard',
            'Enter protected site SRM FQDN + admin credentials  ·  Accept thumbprint',
            'Pairing completes  ·  Both sites show each other in SRM inventory',
        ], 'configure inventory mappings'),
        ('Inventory Mappings', [
            'Network mappings: map protected site port groups to recovery site port groups',
            'Folder mappings: map VM folders between sites for test recovery placement',
            'Resource mappings: map clusters/resource pools between sites',
            'Test network: create isolated test network at recovery site for DR tests',
            'Placeholder datastores: configure at recovery site for VM inventory placeholders',
        ], 'create protection groups'),
        ('Protection Groups', [
            'Array-based groups: use storage array replication sets (SRDF, RecoverPoint)',
            'vSphere Replication groups: select VMs  ·  RPO target  ·  Seed if needed',
            'Assign VMs to protection groups  ·  Replication health confirms no lag',
            'Placeholders created at recovery site  ·  VMs appear in recovery inventory',
            'Verify all VMs in group show Protected status  ·  No missing components',
        ], 'build and test recovery plans'),
        ('Recovery Plans & Testing', [
            'Create recovery plan: select protection group(s)  ·  Define startup priority',
            'Add custom steps: pre/post-recovery scripts, IP customisation rules',
            'Test recovery: SRM powers on VMs in isolated test network  ·  No production impact',
            'Validate VM boot order, IP changes, application startup scripts',
            'Document RTO achieved during test  ·  Clean up test  ·  Schedule recurring tests',
        ], ''),
    ]
)

# ── vSphere Replication ────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/vsphere-replication/index.md'] = diagram(
    'vSphere Replication — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'Two vCenter instances: source and target (same or different SSO domains)',
            'Network: ports 80, 443, 31031, 44046 open between sites',
            'Latency: ≤200 ms between sites for stable replication',
            'Target datastore: sufficient free space for replica disks + delta files',
            'DNS: VR appliance FQDNs resolvable from both sites  ·  PTR records created',
        ], 'deploy VR appliance at source site'),
        ('VR Appliance — Source Site', [
            'Deploy vSphere Replication OVA via vCenter  ·  Confirm OVF checksum',
            'Set FQDN, IP, gateway, DNS, NTP  ·  Set admin and root passwords',
            'Register with local vCenter: VR Admin UI → Configuration → vCenter Server',
            'Accept vCenter thumbprint  ·  VR plugin appears in vSphere Client',
            'Source site VR appliance shows Registered status',
        ], 'deploy VR appliance at target site'),
        ('VR Appliance — Target Site', [
            'Deploy second VR OVA on target site using same procedure',
            'Register with target vCenter',
            'Pair target VR with source VR: VR Admin UI → Configuration → Target Sites',
            'Enter source site VR FQDN + admin credentials  ·  Accept thumbprint',
            'Pairing confirmed  ·  Both sites visible in vSphere Client VR plugin',
        ], 'configure replications'),
        ('Configure VM Replications', [
            'Select VM in vSphere Client  ·  Actions → Configure Replication',
            'Choose target site and target datastore  ·  Set RPO (minimum 5 minutes)',
            'Initial full sync: seed from backup or online full sync over network',
            'Enable multiple point in time (MPIT) snapshots for point-in-time recovery',
            'Replication status: Initial Full Sync → Syncing  ·  Wait for first RPO met',
        ], 'monitor replication health'),
        ('Monitor Replication', [
            'vSphere Client → Site Recovery → Replications: check all VMs RPO status',
            'RPO violations: amber/red indicators — investigate network or datastore latency',
            'Delta disk growth: monitor if network bandwidth limits replication throughput',
            'VR appliance alerts: configure email notification for replication failures',
            'Integrate with SRM if orchestrated failover required (see SRM sequence)',
        ], 'test recovery and failback'),
        ('Recovery & Failback', [
            'Planned migration: graceful shutdown at source  ·  VMs start cleanly at target',
            'Disaster recovery: power off at source (if possible)  ·  Recover at target',
            'Post-failover: reverse replication to reprotect  ·  Failback when ready',
            'Failback: planned migration back to original site  ·  Verify data consistency',
            'Document recovery test results  ·  Update runbook with observed RTO/RPO',
        ], ''),
    ]
)

# ── Horizon ────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/horizon/index.md'] = diagram(
    'VMware Horizon VDI — Installation Sequence',
    [
        ('Pre-Requisites', [
            'Active Directory: OUs for VDI computers  ·  Service accounts for Horizon + AD',
            'vCenter with shared storage and adequate compute for VM pools',
            'SQL Server (or PostgreSQL) for Horizon Events DB and App Volumes DB',
            'Load balancer VIP for Connection Server pool  ·  Certs from CA ready',
            'DNS: A-records for UAG FQDNs, Connection Server pool VIP, Horizon FQDN',
        ], 'install Connection Server (primary)'),
        ('Connection Server — Primary', [
            'Install Horizon Connection Server on Windows Server 2019/2022',
            'Select role: Standard Server (first/primary)  ·  Enter FQDN + admin creds',
            'Set data recovery password (LDAP backup passphrase)',
            'Apply Horizon licence key  ·  Connect vCenter and vCenter-linked View Composer',
            'Confirm vCenter trust  ·  Connection Server admin console accessible',
        ], 'install replica Connection Servers'),
        ('Connection Server — Replicas', [
            'Install 2+ Replica Connection Server instances for HA',
            'During install: select Replica role  ·  Enter primary CS FQDN',
            'Replica joins AD LDS (internal LDAP) cluster  ·  Config replicated automatically',
            'Add all CS instances to load balancer pool  ·  Health checks configured',
            'Verify LDAP replication: any change on primary appears on replica within 1 min',
        ], 'deploy Unified Access Gateway'),
        ('Unified Access Gateway (UAG)', [
            'Deploy UAG OVA  ·  Configure admin, internet-facing, and backend NICs',
            'Set edge service: Horizon (Blast, PCoIP, HTML Access tunnels)',
            'Upload Horizon CA certificate to UAG  ·  Configure thumbprint or cert trust',
            'SAML auth: integrate with Workspace ONE Access for SSO if required',
            'Verify external URL resolves to UAG VIP  ·  Test connection from external client',
        ], 'create desktop pools and farms'),
        ('Desktop Pools & RDSH Farms', [
            'Golden image: create master VM  ·  Install Horizon Agent  ·  Snapshot (parent)',
            'Instant clone pool: define pool  ·  Parent VM + snapshot  ·  Provisioning count',
            'RDSH farm: create farm on RDSH server VMs  ·  Install Horizon Agent (RDSH role)',
            'Application pool: publish apps from RDSH farm to Horizon catalogue',
            'Entitlements: assign pools/apps to AD users or groups  ·  Verify user access',
        ], 'configure App Volumes and DEM'),
        ('App Volumes & Dynamic Environment Manager', [
            'App Volumes Manager: deploy appliance  ·  Register with vCenter + Horizon',
            'AppStacks: capture application packages (MSI/legacy)  ·  Assign to AD groups',
            'Writable Volumes: per-user volumes for profile and user-installed apps',
            'DEM: deploy DEM agent in golden image  ·  Configure file share for user settings',
            'DEM policies: map printers, drives, environment variables  ·  Loopback GPO',
        ], ''),
    ]
)

# ── Tanzu ──────────────────────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/tanzu/index.md'] = diagram(
    'VMware Tanzu Kubernetes — Installation Sequence',
    [
        ('Pre-Requisites', [
            'vSphere 7.0 U2+ or vSphere 8  ·  Enterprise Plus licence (Workload Management)',
            'NSX-T deployed OR vSphere Distributed Switch 7.0+ for VDS networking mode',
            'Shared storage: vSAN or NFS/iSCSI datastore for supervisor control plane VMs',
            'DNS: A-records for Supervisor API server VIP + worker node VMs',
            'NTP: all ESXi hosts and vCenter time-synced  ·  Registry (Harbor) planned',
        ], 'enable Workload Management (Supervisor)'),
        ('Enable Workload Management', [
            'vCenter → Workload Management → Enable  ·  Select cluster',
            'Choose networking: NSX-T (recommended) or VDS with HAProxy',
            'Control Plane VMs: size (tiny/small/medium/large)  ·  3 VMs deployed automatically',
            'Ingress/Egress CIDR, Pod CIDRs, Service CIDR: enter non-overlapping ranges',
            'Wait for Supervisor Ready state  ·  Control plane VMs healthy in vCenter',
        ], 'configure namespaces'),
        ('vSphere Namespace Configuration', [
            'Create vSphere namespace per team or environment',
            'Resource limits: CPU, memory, storage quotas per namespace',
            'Storage policy: assign vSAN or NFS storage policy for PVC provisioning',
            'Network: assign NSX segment or VDS network to namespace',
            'Permissions: assign AD users/groups to namespace with edit/view roles',
        ], 'deploy Tanzu Kubernetes Grid clusters'),
        ('TKG Cluster Deployment', [
            'kubectl vsphere login --server <supervisor-VIP>  ·  Authenticate via AD/SSO',
            'Switch context to vSphere namespace  ·  Apply TanzuKubernetesCluster YAML',
            'Define control plane + worker node pools  ·  Choose TKR (Kubernetes release)',
            'Storage class and CNI (Antrea) applied automatically  ·  Cluster provisions',
            'Get kubeconfig  ·  kubectl get nodes  ·  All nodes Ready state confirmed',
        ], 'deploy Harbor container registry'),
        ('Harbor Container Registry', [
            'Deploy Harbor via Aria Automation, Helm, or as embedded in Supervisor',
            'Set admin password  ·  Configure internal CA or upload CA-signed cert',
            'Create projects: one per team/namespace  ·  Assign project roles to AD groups',
            'Robot accounts: create per CI/CD pipeline  ·  Assign pull/push rights',
            'Configure replication: mirror images from Docker Hub / external registry',
        ], 'developer onboarding'),
        ('Developer Onboarding', [
            'Provide kubectl vsphere login command + Supervisor VIP to teams',
            'Namespace RBAC: AD groups mapped to Kubernetes RBAC roles via namespace',
            'CI/CD integration: pipeline authenticates to Harbor  ·  Build → push → deploy',
            'Resource quotas enforced: pods over quota blocked  ·  Teams manage own limits',
            'Monitoring: Aria Operations with Kubernetes MP  ·  Alerts on pod failures',
        ], ''),
    ]
)

# ── VMware Cloud Foundation ────────────────────────────────────────────────────
DIAGRAMS['docs/virtualization/vmware/vmware-cloud-foundation/index.md'] = diagram(
    'VMware Cloud Foundation (VCF) — Installation Sequence',
    [
        ('Pre-Deploy Checks', [
            'Minimum 4 ESXi hosts for management domain  ·  Each meets VCF HCL requirements',
            'DNS: all host FQDNs, vCenter FQDN, NSX FQDN, SDDC Manager FQDN pre-created',
            'NTP: all hosts synced to same source before Cloud Builder starts',
            'Network: management, vSAN, vMotion, NSX TEP VLANs configured on ToR switches',
            'VCF deployment JSON (EMS file) prepared: IPs, VLANs, credentials for all components',
        ], 'deploy Cloud Builder VM'),
        ('Cloud Builder Deployment', [
            'Download Cloud Builder OVA from VMware portal  ·  Deploy on any ESXi host',
            'Set management IP, gateway, DNS, NTP  ·  Admin password',
            'Access Cloud Builder UI  ·  Import deployment JSON (EMS/bringup spec)',
            'Cloud Builder validates JSON: DNS, NTP, network, and hardware prerequisites',
            'Resolve all validation warnings/errors before proceeding to bringup',
        ], 'run management domain bringup'),
        ('Management Domain Bringup', [
            'Cloud Builder orchestrates full management domain deployment automatically:',
            '  ① Configure ESXi hosts (networking, NTP, DNS)  → ② Deploy vCenter VCSA',
            '  ③ Create management cluster  → ④ Configure vSAN on management hosts',
            '  ⑤ Deploy NSX Manager 3-node cluster  → ⑥ Deploy SDDC Manager',
            'Bringup takes 2–4 hours  ·  Monitor progress in Cloud Builder UI',
        ], 'validate SDDC Manager'),
        ('SDDC Manager Validation', [
            'Login to SDDC Manager  ·  Review management domain health dashboard',
            'Credentials vault: update all default passwords via SDDC Manager password rotation',
            'Licences: enter vSphere, vSAN, NSX, and VCF licences in SDDC Manager',
            'Configure backup: SDDC Manager backup to external SCP/SFTP target',
            'Certificates: replace SDDC Manager and management component certs with CA-signed',
        ], 'commission hosts and create workload domain'),
        ('Workload Domain Creation', [
            'Commission additional ESXi hosts: SDDC Manager → Hosts → Commission',
            'Cloud Builder validates commissioned hosts against HCL and configuration',
            'Create Workload Domain: SDDC Manager → Workload Domains → Add Domain',
            'Wizard deploys dedicated vCenter, vSAN, NSX segments for workload domain',
            'Workload domain available in SDDC Manager  ·  Assign to project/team',
        ], 'lifecycle management and day-2'),
        ('Lifecycle Management & Day-2', [
            'LCM bundles: SDDC Manager downloads patch bundles from depot (online or air-gap)',
            'Upgrade sequencing: NSX → vCenter → ESXi hosts per SDDC Manager guidance',
            'Aria Suite: deploy Operations, Automation, Logs via LCM for full SDDC observability',
            'Capacity expansion: commission additional hosts  ·  Add to existing domain',
            'DR: configure SRM + vSphere Replication across VCF management domains',
        ], ''),
    ]
)

# ── Insertion logic ────────────────────────────────────────────────────────────

def insert_diagram(filepath, diagram_text):
    with open(filepath) as f:
        content = f.read()

    lines = content.splitlines(keepends=True)

    # Find the last ``` before the first <div class="kb-grid"
    kb_grid_line = None
    for i, l in enumerate(lines):
        if l.strip().startswith('<div class="kb-grid'):
            kb_grid_line = i
            break

    if kb_grid_line is None:
        print(f'  SKIP (no kb-grid found): {filepath}')
        return False

    # Walk backwards to find the closing ``` of the existing diagram
    close_fence = None
    for i in range(kb_grid_line - 1, -1, -1):
        if lines[i].strip() == '```':
            close_fence = i
            break

    if close_fence is None:
        print(f'  SKIP (no closing fence found): {filepath}')
        return False

    # Check if installation sequence already present
    existing = ''.join(lines)
    if 'Installation Sequence' in existing:
        print(f'  SKIP (already has Installation Sequence): {filepath}')
        return False

    # Insert: blank line + new diagram + blank line between close_fence and kb_grid
    insert_lines = ['\n'] + [l + '\n' for l in diagram_text.splitlines()] + ['\n']

    new_lines = lines[:close_fence + 1] + insert_lines + lines[close_fence + 1:]

    with open(filepath, 'w') as f:
        f.writelines(new_lines)

    print(f'  DONE: {filepath}')
    return True


def main():
    import os
    os.chdir('/Users/chrisanastasiadis/chris-kb')
    done = 0
    for path, diag in DIAGRAMS.items():
        result = insert_diagram(path, diag)
        if result:
            done += 1
    print(f'\n{done}/{len(DIAGRAMS)} diagrams inserted.')


if __name__ == '__main__':
    main()
