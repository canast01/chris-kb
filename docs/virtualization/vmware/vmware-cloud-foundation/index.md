# VMware Cloud Foundation

<div class="kb-summary">
Technical and operational reference for VMware Cloud Foundation (VCF). Covers SDDC Manager, workload domains, lifecycle management, vSphere, vSAN, and NSX integration across the full-stack private cloud platform.
</div>

```
┌────────────────────────────── VMware Cloud Foundation (VCF) Full Stack ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  VMware Cloud Foundation — Integrated Private Cloud Platform                  │   │
│   │       SDDC Manager: lifecycle orchestration for vCenter, NSX, vSAN, and workload domains      │   │
│   │         Management Domain: first domain; runs SDDC Manager, vCenter, NSX Manager, vSAN        │   │
│   │          Workload Domains: VI (vSphere+vSAN+NSX) or VVF (VI+Tanzu); up to 15 per SDDC         │   │
│   │     Bring-up: CloudBuilder deploys VCF from Day 0; creates management domain automatically    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SDDC Manager orchestrates · management domain runs platform services · workload domains host apps  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    SDDC Manager: LCM core   │  │   SOS: health diagnostics   │  │     SDDC Mgr RBAC: roles    │   │
│   │    Mgmt domain: 4+ hosts    │  │    LCM: bundle + upgrade    │  │   Cert rotation: all comps  │   │
│   │   Workload domain: VI/VVF   │  │   Password rotation: SDDC   │  │   Security baseline: DISA   │   │
│   │   NSX: overlay per domain   │  │      Host commissioning     │  │    KMS: key mgmt for vSAN   │   │
│   │  CloudBuilder: day-0 deploy │  │   Network pools: IP blocks  │  │   Compliance: audit + log   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines domain layout · Operations execute LCM and commissioning                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │ LCM upgrade fail │ SOS health-check │ SDDC Mgr: running?│ GSS: SOS bundle  │ sddc-manager api │   │
│   │ Domain add fail  │vcf-support bundle│ Domain state: UP? │  TAM escalation  │sddc-manager hosts│   │
│   │NSX cert rotation │ SDDC Mgr UI logs │   LCM state: OK?  │ Collect all logs │sddc-manager domai│   │
│   │Password out-of-sy│SOS password-check│ Certs valid +30d? │ P1: mgmt domain  │sddc-manager certs│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Rack servers (HCL certified) · 25 GbE ToR switches · management network · vSAN-ready NVMe/SSD drives │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF orchestration appliance; manages lifecycle, inventory, passwords, and            │
│  Workload Domain= Isolated vSphere+vSAN+NSX instance for a workload type; VI or VVF flavour           │
│  VI Domain     = vSphere Infrastructure domain; vCenter + NSX + vSAN for VM workloads                 │
│  VVF Domain    = vSphere with Tanzu; VI domain plus Supervisor Cluster for Kubernetes                 │
│  CloudBuilder  = Day-0 VCF deployment appliance; validates HW and deploys management domain           │
│  LCM           = Lifecycle Management; SDDC Manager downloads bundles and upgrades all components     │
│  SOS           = SDDC Operations Support; health-check and log bundle tool in VCF                     │
│  Network Pool  = IP address range assigned in SDDC Manager for VMkernel port allocation               │
│  Management Domain= First VCF domain; runs SDDC Manager, vCenter, NSX Manager, vSAN                   │
│  Host commissioning= Adding a bare-metal host to SDDC Manager inventory before domain assignment      │
│  Bundle        = LCM upgrade package downloaded from VMware depot containing product updates          │
│  DISA STIG     = US government security baseline; VCF includes DISA STIG compliance profile           │
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
