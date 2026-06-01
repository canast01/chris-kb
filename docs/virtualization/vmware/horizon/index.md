# Horizon (VDI)

<div class="kb-summary">
Horizon knowledge base — architecture, operations, CLI references, security, and troubleshooting. Content being built out.
</div>

```text
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
