# vCenter — Architecture

<div class="kb-summary">
vCenter Server is the management plane for VMware vSphere, deployed as the VCSA appliance. It supports standard single-node, vCenter HA (3-node active/passive/witness), and Enhanced Linked Mode topologies.
</div>

```
┌─────────────────────────────────────── vCenter — Architecture ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ VCSA — virtual appliance (Linux-based); PSC embedded since vCenter 7.0; no external PSC needed│   │
│   │SSO domain provides identity federation; AD/LDAP identity sources for enterprise authentication│   │
│   │   Inventory hierarchy: Datacenter > Cluster > Host > VM; permissions inherited down the tree  │   │
│   │   vCenter HA: 3-node active/passive/witness; protects VCSA from host failure; same-site only  │   │
│   │     VAMI (port 5480) manages appliance: network, time, backup, update, and service control    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines VCSA internals · integrations connect identity and tools                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │      VCSA appliance VM      │  │       AD/LDAP identity      │  │       VCSA sizing L/XL      │   │
│   │       SSO domain: IdP       │  │        NSX-T: plugin        │  │        HA 3-node prod       │   │
│   │      Inventory: DC>Clst     │  │      Aria Ops: adapter      │  │        Backup: daily        │   │
│   │      vCenter HA: 3-node     │  │        LCM: built-in        │  │        NTP: 2 sources       │   │
│   │         PSC embedded        │  │       Backup: SFTP/NFS      │  │      Cert: VMCA/custom      │   │
│   │        VAMI: web mgmt       │  │       Aria Auto: cloud      │  │      SSO single domain      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines VCSA and SSO · integrations connect identity and tools                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │  VCSA appliance  │   AD/LDAP IdP    │   VCSA L sizing   │  Single vCenter  │  NTP 2 sources   │   │
│   │    SSO domain    │   NSX-T plugin   │     HA 3-node     │   Linked mode    │   Cert policy    │   │
│   │  Inventory hier  │ Aria Ops adapter │    Daily backup   │    Multi-site    │     RBAC std     │   │
│   │    vCenter HA    │   Backup SFTP    │    VMCA/custom    │  Multi-vCenter   │  SSO domain std  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server (VCSA VM target) · RAM DIMMs · Network NICs · Shared datastore · OOB management           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VCSA          = vCenter Server Appliance; Linux-based OVA deployed as a VM; single management plane  │
│  SSO domain    = Single Sign-On domain (vsphere.local by default); identity hub for vSphere auth      │
│  PSC           = Platform Services Controller; embedded in VCSA 7.0+; manages SSO, certs, licensing   │
│  VMCA          = VMware Certificate Authority; built-in CA signing VCSA and host certificates         │
│  vCenter HA    = 3-node VCSA cluster: active, passive, witness; automatic failover on host failure    │
│  VAMI          = vCenter Appliance Management Interface; web UI on port 5480 for appliance operations │
│  Linked Mode   = Multiple vCenters sharing SSO domain; unified inventory view across instances        │
│  RBAC          = Role-Based Access Control; permissions set at inventory objects and inherited down   │
│  Inventory hierarchy = DC > Cluster > Host > VM; permissions and policies propagate downward          │
│  AD/LDAP       = Active Directory or LDAP identity source added to SSO for enterprise user auth       │
│  File-based backup = VCSA periodic backup to SFTP or NFS; restores full appliance configuration       │
│  Update Planner = vCenter tool that checks interoperability and schedules upgrade order               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>VCSA internals, SSO domain, inventory hierarchy, and vCenter HA.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>AD/LDAP identity, NSX-T, Aria Operations, and backup targets.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing, HA topology, certificate policy, and NTP requirements.</span>
</a>

</div>

## vCenter Deployment Models

![vCenter Deployment Models](../../../../assets/vcenter-architecture-overview.svg)
