# Reference

<div class="kb-summary">
Standards, inventory, upgrade readiness checklists, and quick reference material for the virtualization platform.
</div>

```text
┌──────────────────────────────────────── VMware Reference Hub ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      VMware Reference Hub                                     │   │
│   │    Central reference for platform standards, inventory, upgrade readiness, and quick lookup   │   │
│   │          Standards define how the environment is built · Inventory tracks what exists         │   │
│   │      Upgrade Readiness validates compatibility · Quick Reference gives commands on demand     │   │
│   │      Maintained alongside change records to stay current with deployed platform versions      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Standards, inventory, and readiness work together to keep the platform well-managed                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Standards          │  │          Inventory          │  │      Upgrade Readiness      │   │
│   │  Naming: VM, host, cluster  │  │  Host register: cluster map │  │    HCL: hardware compat.    │   │
│   │  Host build: BIOS/ESXi std  │  │   VM catalog: owner + tier  │  │   Interop matrix: VC+ESXi   │   │
│   │   Port groups: VLAN design  │  │   Datastore: usage+policy   │  │   Pre-checks: health+certs  │   │
│   │   vSAN policy: FTT+stripe   │  │   Network: VDS + VLAN map   │  │   Rollback: snapshot+plan   │   │
│   │   Change control: process   │  │     Certs + SVC accounts    │  │     Post-val: VM + vSAN     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Reference content drives consistency across builds, changes, and upgrade events                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Quick Reference                                        │   │
│   │           Port reference: vCenter 443/8443 · ESXi 443/902 · NFC 2049 · vMotion 8000           │   │
│   │          Common CLI: esxcli network nic list · vim-cmd vmsvc/getallvms · govc vm.info         │   │
│   │         vSphere versions: vCenter must be ≥ ESXi; 2-hop version hop limit for upgrades        │   │
│   │       License SKUs: Essentials+ · Standard · Enterprise Plus · vSAN Standard/Enterprise       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Quick Reference covers commands, ports, versioning, and license SKU details                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Standards     │    Inventory     │      Upgrades     │    Quick Ref     │      Ports       │   │
│   │   Naming std.    │  Host register   │     HCL lookup    │   esxcli cmds    │    HTTPS 443     │   │
│   │    Build std.    │    VM catalog    │     Pre-checks    │    govc cmds     │   vMotion 8000   │   │
│   │   VLAN design    │  Cert tracking   │   Rollback plan   │  PowerCLI ref.   │     NFC 2049     │   │
│   │   Change ctrl    │   SVC accounts   │      Post-val     │  API reference   │     ESXi 902     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts · vCenter appliance · vSAN datastores · NSX Managers · Power & Cooling                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HCL     = VMware Hardware Compatibility List; certified hardware for vSphere and vSAN                │
│  FTT     = Failures to Tolerate; vSAN SPBM policy setting for data redundancy                         │
│  VDS     = vSphere Distributed Switch; cluster-level virtual switch in vCenter                        │
│  SPBM    = Storage Policy-Based Management; assigns vSAN rules per VM or virtual disk                 │
│  vMotion  = Live VM migration between ESXi hosts; traffic on VMkernel port 8000                       │
│  NFC     = Network File Copy; protocol for vCenter cold migrations and deployments                    │
│  Port 902 = ESXi hostd/vpxa heartbeat and management traffic from vCenter to host                     │
│  Interop  = VMware interoperability matrix; validates vCenter + ESXi version combinations             │
│  SVC Account= Service account for vCenter, backup, and monitoring tool authentication                 │
│  Enterprise Plus= vSphere top-tier licence; includes DRS, HA, vSAN, and all features                  │
│  Change Control= Documented process for approved infra changes; tracks risk and rollback              │
│  Essentials+= vSphere entry licence; limited to 3 hosts; HA but no DRS or vSAN                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Platform standards, naming conventions, and configuration baselines.</span>
</a>

<a class="kb-card" href="inventory/">
  <strong>Inventory</strong>
  <span>Environment inventory, asset registers, and platform documentation.</span>
</a>

<a class="kb-card" href="upgrade-readiness/">
  <strong>Upgrade Readiness</strong>
  <span>Pre-upgrade checklists, compatibility matrices, and readiness assessments.</span>
</a>

<a class="kb-card" href="quick-reference/"><strong>Quick Reference</strong><span>Command cheat sheets, port references, and quick lookup guides.</span></a>
<a class="kb-card" href="gotchas/"><strong>Gotchas</strong><span>Known edge cases, unexpected behaviours, and platform quirks to watch for.</span></a>
<a class="kb-card" href="design-decisions/"><strong>Design Decisions</strong><span>Architectural decision records for platform design choices and rationale.</span></a>
<a class="kb-card" href="licensing/"><strong>Licensing</strong><span>VMware licensing models, SKU comparison, capacity planning, and compliance.</span></a>
<a class="kb-card" href="certification/"><strong>Certification</strong><span>Certification reference materials, paths, and exam notes.</span></a>
<a class="kb-card" href="high-availability/"><strong>High Availability</strong><span>HA design patterns, vSphere HA, admission control, redundancy tiers, and multi-site architecture.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Cross-platform virtualization diagnostics — vSphere host failures, vSAN issues, Tanzu, and SRM.</span></a>

</div>
