---
tags:
  - vcenter
  - vmware
  - vsphere-8
---
# vCenter

<div class="kb-summary">
Technical and operational reference for VMware vCenter Server (VCSA). Covers architecture, cluster management, lifecycle, security, and troubleshooting for the vSphere management plane.
</div>

```text
┌─────────────────────────────────── vCenter Server Management Plane ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                VMware vCenter Server (VCSA) — vSphere Management Control Plane                │   │
│   │         VCSA: Linux appliance running vCenter, PSC (embedded), and vPostgres database         │   │
│   │   Cluster services: DRS (workload balancing) · HA (host failure restart) · DPM (power mgmt)   │   │
│   │     SSO: identity source (AD/LDAP); vCenter single sign-on for all Aria and vSphere tools     │   │
│   │         Linked mode: multiple vCenters share inventory via Enhanced Linked Mode (ELM)         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VCSA is the management hub · DRS/HA automate cluster operations · SSO unifies authentication       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    VCSA: embedded PSC+DB    │  │   Cluster: DRS + HA rules   │  │   SSO: AD identity source   │   │
│   │   DRS: VM workload balance  │  │   Snapshot: create+manage   │  │  RBAC: roles + global perms │   │
│   │   HA: heartbeat + restart   │  │      LCM: host patching     │  │  TLS: cert replace + renew  │   │
│   │   ELM: multi-vCenter view   │  │   vMotion: live migration   │  │     2FA: RSA/RADIUS/Duo     │   │
│   │  vDS: distributed switching │  │   Alarms: configure + ack   │  │  Audit: tasks + events log  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the management plane · Operations run day-to-day tasks                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │SSO login failure │vc-support bundle │  VCSA health: OK? │GSS: collect logs │   govc ls /dc    │   │
│   │DRS not migrating │ vpxd.log review  │   DB disk <80%?   │  TAM escalation  │   govc vm.info   │   │
│   │ HA agent restart │service-control --│ Services: running?│ Collect vpxd.log │govc cluster.usage│   │
│   │Cert expired alert│python /usr/lib/vm│ Certs: expiry OK? │P1: mgmt plane dow│   govc events    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VCSA VM on ESXi host · vSphere cluster hosts · shared datastore for VCSA · network for port 443/8443 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA          = vCenter Server Appliance; Photon OS Linux VM running vCenter and embedded PSC        │
│  DRS           = Distributed Resource Scheduler; migrates VMs via vMotion to balance cluster load     │
│  HA            = vSphere High Availability; restarts VMs on surviving hosts after host failure        │
│  SSO           = Single Sign-On; vCenter identity service; integrates AD/LDAP identity sources        │
│  ELM           = Enhanced Linked Mode; joins multiple vCenter instances to share inventory view       │
│  DPM           = Distributed Power Management; consolidates workloads and powers off idle hosts       │
│  vDS           = vSphere Distributed Switch; centrally managed virtual switch across all cluster hosts│
│  PSC           = Platform Services Controller; handles SSO, certs, licensing; now embedded in VCSA    │
│  LCM           = Lifecycle Manager; manages ESXi patching baselines and cluster remediation           │
│  govc          = Go-based vSphere CLI; faster than PowerCLI for scripting; uses GOVC_URL env var      │
│  vpxd.log      = Main vCenter service log; first place to check for management plane errors           │
│  HA heartbeat  = vCenter and datastore heartbeat; determines host isolation vs failure                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌─────────────────────────────── vCenter Server — Installation Sequence ────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  DNS: A-record and PTR for vCenter FQDN created  ·  Resolves from all hosts                           │
│  NTP: two sources reachable  ·  ESXi hosts already time-synced                                        │
│  Service account in AD: SSO admin, AD join credentials ready                                          │
│  Certificates: CA ready to sign or self-signed accepted per policy                                    │
│  Target datastore free space: ≥550 GB (small), ≥1150 GB (medium), ≥1700 GB (large)                    │
│                                                                                                       │
│                                        │  deploy VCSA OVA                                             │
│                                        ▼                                                              │
│  Step 2 · VCSA Deploy — Stage 1                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Mount VCSA ISO  ·  Launch installer (UI or CLI)  ·  Select Deploy                                    │
│  Enter ESXi host FQDN + credentials  ·  Accept host thumbprint                                        │
│  VM name, size selection (tiny/small/medium/large/x-large)                                            │
│  Select datastore  ·  Set network, IP, gateway, DNS, FQDN                                             │
│  Stage 1 completes: VCSA VM powered on, OS booted, ready for Stage 2                                  │
│                                                                                                       │
│                                        │  complete Stage 2 configuration                              │
│                                        ▼                                                              │
│  Step 3 · VCSA Configure — Stage 2                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Connect to Stage 2 wizard at https://vcsa-fqdn:5480                                                  │
│  NTP servers entered  ·  SSH access: enable for setup, disable post-config                            │
│  SSO domain name (vsphere.local or custom)  ·  SSO admin password set                                 │
│  Inventory size: select to match expected VM/host count for DB sizing                                 │
│  Stage 2 completes: vCenter services start  ·  vSphere Client accessible                              │
│                                                                                                       │
│                                        │  integrate with Active Directory                             │
│                                        ▼                                                              │
│  Step 4 · AD Integration & Identity                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Add AD identity source: Administration → SSO → Identity Sources                                      │
│  Service account for LDAP bind  ·  Base DN for users and groups                                       │
│  Assign AD groups to vCenter roles: administrators, read-only, operators                              │
│  Verify AD login works  ·  Remove default permissions after role mapping                              │
│  Confirm token lifetime and lockout policy match security baseline                                    │
│                                                                                                       │
│                                        │  build inventory                                             │
│                                        ▼                                                              │
│  Step 5 · Inventory Build                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create datacenter object  ·  Add cluster  ·  Configure HA and DRS settings                           │
│  Add all ESXi hosts to cluster  ·  Hosts enter connected state                                        │
│  Create distributed switch  ·  Migrate hosts from vSS to vDS uplinks                                  │
│  Configure port groups: management, vMotion, vSAN, VM networks                                        │
│  Assign licences to hosts and cluster  ·  Verify no licence warnings                                  │
│                                                                                                       │
│                                        │  validate and harden                                         │
│                                        ▼                                                              │
│  Step 6 · Post-Install Validation                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Configure alarm definitions: host disconnect, datastore full, HA failure                             │
│  vCenter backup: File-Based Backup (FTP/SCP/HTTP) schedule configured daily                           │
│  Certificate: replace MACHINE_SSL_CERT with CA-signed if required                                     │
│  Skyline Health: enable and confirm green status for vCenter                                          │
│  SNMP or syslog forwarding configured for monitoring platform                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>VCSA Stage 1 OVA deploy, Stage 2 SSO config, AD integration, and inventory build.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
