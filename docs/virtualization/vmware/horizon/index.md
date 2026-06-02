# Horizon (VDI)

<div class="kb-summary">
Horizon knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```
┌────────────────────────────────────── VMware Horizon VDI Stack ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   VMware Horizon — Virtual Desktop and App Delivery Platform                  │   │
│   │       Connection Server: broker authenticating users and directing them to desktop pools      │   │
│   │       UAG: Unified Access Gateway; external proxy terminating Blast/PCoIP from internet       │   │
│   │        Desktop pools: instant clone (fast provision), linked clone, or full-clone pools       │   │
│   │    App Volumes: application layering; real-time delivery via AppStacks and WritableVolumes    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Connection Server brokers sessions · UAG secures external access · pools deliver desktops          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │     Connection Server HA    │  │    Pool: provision+resize   │  │    Smart card + MFA auth    │   │
│   │    UAG: Blast/PCoIP proxy   │  │    Session: monitor+reset   │  │    UAG: cert + TLS config   │   │
│   │   Instant clone: parent VM  │  │    App Volumes: AppStack    │  │     DEM: user env policy    │   │
│   │      ADAM: CS config DB     │  │    Certificate: renew CS    │  │   Blast: protocol lockdown  │   │
│   │    DEM: user profile mgmt   │  │    Events DB: query logs    │  │    Entitlement: AD group    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the brokering stack · Operations manage pools and sessions                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Login loop: CS che│Horizon events DB │  CS: services up? │GSS + CS log bundl│   vdmadmin -l    │   │
│   │Black screen: blas│   UAG edge log   │  UAG: reachable?  │  TAM escalation  │   vdmadmin -A    │   │
│   │Pool not provision│instant-clone.log │Pool: available VMs│Collect debug log │   vdmadmin -n    │   │
│   │App Volumes not mo│  AppVolumes.log  │AppStack: attached?│  P1: VDI outage  │   vdmadmin -c    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere cluster for VDI VMs · Connection Server Windows VMs · UAG VMs in DMZ · GPU hosts if needed   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Connection Server= Windows service brokering user sessions to desktop pools; requires AD membership  │
│  UAG           = Unified Access Gateway; DMZ appliance proxying Blast/PCoIP without VPN               │
│  Desktop pool  = Collection of VMs or RDS hosts assigned to users; persistent or floating             │
│  Instant clone = Fast desktop provision using vmFork; creates linked child from running parent VM     │
│  Linked clone  = Template-based pool sharing a parent snapshot; saves storage vs full clone           │
│  App Volumes   = Application layering; AppStack VMDK attached at login; WritableVolume for user data  │
│  DEM           = Dynamic Environment Manager; user profile and policy management for VDI sessions     │
│  Blast         = VMware display protocol; H.264/H.265; works over HTTPS 443; preferred for WAN        │
│  PCoIP         = PC-over-IP; Teradici display protocol; UDP 4172; good for LAN/graphics               │
│  ADAM          = Active Directory Application Mode; Connection Server internal config database        │
│  Entitlement   = AD user or group granted access to a pool or application in Horizon                  │
│  vdmadmin      = Horizon CLI; manage users, entitlements, machines, and Connection Server config      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```
┌───────────────────────────── VMware Horizon VDI — Installation Sequence ──────────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Requisites                                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Active Directory: OUs for VDI computers  ·  Service accounts for Horizon + AD                        │
│  vCenter with shared storage and adequate compute for VM pools                                        │
│  SQL Server (or PostgreSQL) for Horizon Events DB and App Volumes DB                                  │
│  Load balancer VIP for Connection Server pool  ·  Certs from CA ready                                 │
│  DNS: A-records for UAG FQDNs, Connection Server pool VIP, Horizon FQDN                               │
│                                                                                                       │
│                                        │  install Connection Server (primary)                         │
│                                        ▼                                                              │
│  Step 2 · Connection Server — Primary                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install Horizon Connection Server on Windows Server 2019/2022                                        │
│  Select role: Standard Server (first/primary)  ·  Enter FQDN + admin creds                            │
│  Set data recovery password (LDAP backup passphrase)                                                  │
│  Apply Horizon licence key  ·  Connect vCenter and vCenter-linked View Composer                       │
│  Confirm vCenter trust  ·  Connection Server admin console accessible                                 │
│                                                                                                       │
│                                        │  install replica Connection Servers                          │
│                                        ▼                                                              │
│  Step 3 · Connection Server — Replicas                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install 2+ Replica Connection Server instances for HA                                                │
│  During install: select Replica role  ·  Enter primary CS FQDN                                        │
│  Replica joins AD LDS (internal LDAP) cluster  ·  Config replicated automatically                     │
│  Add all CS instances to load balancer pool  ·  Health checks configured                              │
│  Verify LDAP replication: any change on primary appears on replica within 1 min                       │
│                                                                                                       │
│                                        │  deploy Unified Access Gateway                               │
│                                        ▼                                                              │
│  Step 4 · Unified Access Gateway (UAG)                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy UAG OVA  ·  Configure admin, internet-facing, and backend NICs                                │
│  Set edge service: Horizon (Blast, PCoIP, HTML Access tunnels)                                        │
│  Upload Horizon CA certificate to UAG  ·  Configure thumbprint or cert trust                          │
│  SAML auth: integrate with Workspace ONE Access for SSO if required                                   │
│  Verify external URL resolves to UAG VIP  ·  Test connection from external client                     │
│                                                                                                       │
│                                        │  create desktop pools and farms                              │
│                                        ▼                                                              │
│  Step 5 · Desktop Pools & RDSH Farms                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Golden image: create master VM  ·  Install Horizon Agent  ·  Snapshot (parent)                       │
│  Instant clone pool: define pool  ·  Parent VM + snapshot  ·  Provisioning count                      │
│  RDSH farm: create farm on RDSH server VMs  ·  Install Horizon Agent (RDSH role)                      │
│  Application pool: publish apps from RDSH farm to Horizon catalogue                                   │
│  Entitlements: assign pools/apps to AD users or groups  ·  Verify user access                         │
│                                                                                                       │
│                                        │  configure App Volumes and DEM                               │
│                                        ▼                                                              │
│  Step 6 · App Volumes & Dynamic Environment Manager                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  App Volumes Manager: deploy appliance  ·  Register with vCenter + Horizon                            │
│  AppStacks: capture application packages (MSI/legacy)  ·  Assign to AD groups                         │
│  Writable Volumes: per-user volumes for profile and user-installed apps                               │
│  DEM: deploy DEM agent in golden image  ·  Configure file share for user settings                     │
│  DEM policies: map printers, drives, environment variables  ·  Loopback GPO                           │
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
