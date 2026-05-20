# vCenter

<div class="kb-summary">
Technical and operational reference for VMware vCenter Server (VCSA). Covers architecture, cluster management, lifecycle, security, and troubleshooting for the vSphere management plane.
</div>

```
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

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
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
