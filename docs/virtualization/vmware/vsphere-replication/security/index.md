# vSphere Replication — Security
```
┌─────────────────────────────────── vSphere Replication — Security ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         vCenter SSO authentication for VR appliance management; RBAC via vCenter roles        │   │
│   │            Replication traffic encrypted over TLS between source VRS and target VRS           │   │
│   │   Certificate management: VRMS and VRS certs signed by CA or vCenter CA; rotated on schedule  │   │
│   │       Firewall rules: VRMS port 8043/443, VRS port 31031, vCenter port 443 between sites      │   │
│   │    Audit: all replication config changes logged in vCenter Tasks and Events; syslog forward   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    vCenter SSO gates management · TLS encrypts replication traffic                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Encryption         │   │
│   │         vCenter SSO         │  │         vCenter RBAC        │  │         Traffic TLS         │   │
│   │       LDAP via vCenter      │  │          Admin role         │  │       Cert management       │   │
│   │       VRMS local admin      │  │        Read-only role       │  │       CA-signed certs       │   │
│   │         Plugin auth         │  │        Datastore perm       │  │          FIPS mode          │   │
│   │       Site trust cert       │  │       Site admin roles      │  │       Compress+encrypt      │   │
│   │       VAMI local auth       │  │        Firewall rules       │  │        Audit logging        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SSO controls management access · RBAC scopes permissions                                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Auth       │   Access Ctrl    │     Encryption    │    Hardening     │      Audit       │   │
│   │   vCenter SSO    │   vCenter RBAC   │    Traffic TLS    │  Cert rotation   │  vCenter tasks   │   │
│   │   LDAP groups    │    Admin role    │   CA-signed cert  │  Firewall rules  │  Config events   │   │
│   │    VRMS local    │  Read-only role  │     FIPS mode     │  Min-perm RBAC   │  Syslog forward  │   │
│   │ Site trust cert  │  Firewall scope  │    Compress+enc   │  VAMI hardening  │  Site pair log   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (VRMS + VRS) · RAM DIMMs · WAN firewall · CA infrastructure · vCenter appliance              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vCenter SSO        = Single Sign-On; authenticates admin access to VR plugin within vCenter UI       │
│  RBAC               = Role-Based Access Control; VR uses vCenter roles for permissions scoping        │
│  Admin role         = Full VR management: configure, pause, resume, reconfigure replication           │
│  Read-only role     = View replication status only; cannot configure or modify replication            │
│  Traffic encryption = TLS between source and target VRS; enabled by default; FIPS mode optional       │
│  VRMS certificate   = TLS cert for the VRMS management UI; signed by vCenter CA or external CA        │
│  VRS certificate    = TLS cert for the VRS data path; must be trusted at both source and target sites │
│  Site trust         = Certificate-based trust between source vCenter and target vCenter for VR pairing│
│  VAMI               = Virtual Appliance Management Interface; admin UI for VRMS/VRS; secured with     │
│  Firewall rules     = Required: 8043/443 for VRMS, 31031 for VRS data, 443 for vCenter communication  │
│  Audit log          = All VR config changes logged in vCenter Tasks/Events; forwarded via syslog to   │
│  FIPS 140-2         = Federal cryptographic standard; enabled for VR traffic encryption at cluster    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>SSO, LDAP, local accounts, and identity sources.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>Roles, permissions, and least privilege access.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data encryption and certificate management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baselines and compliance configuration.</span>
</a>

</div>
