---
tags:
  - troubleshooting
  - vcenter
  - vmware
  - vsphere-8
search:
  boost: 1.5
---
# vCenter — Troubleshooting

<div class="kb-summary">
Troubleshooting reference for VMware vCenter Server. Covers common VCSA failure patterns, SSO and certificate issues, diagnostic commands, log collection, and escalation procedures.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌────────────────────────────────────── vCenter — Troubleshooting ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ SSO login failures: expired certs, clock skew, or identity source misconfiguration most common│   │
│   │Certificate expiry cascade: expired VMCA root causes all host and service cert failures at once│   │
│   │  VCSA service failures: vpxd process restart for vCenter main service; check VAMI health tab  │   │
│   │ vCenter HA split-brain: both active and passive claim active role; check witness connectivity │   │
│   │ VCSA shell and vcsa-check script for diagnostics; PSC sync issues resolved by SSO repair tool │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics isolate the service layer                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │        SSO login fail       │  │       VCSA shell cmds       │  │      VCSA support bndl      │   │
│   │         Cert expired        │  │       /var/log/vmware       │  │        GSS P1/P2 case       │   │
│   │        VCSA svc down        │  │         VAMI health         │  │       Cert reset steps      │   │
│   │        HA split-brain       │  │        API debug mode       │  │         RCA template        │   │
│   │        LCM task stuck       │  │        SSO health chk       │  │        TAM escalation       │   │
│   │       NSX plugin error      │  │      vcsa-check script      │  │         Log archive         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide triage · diagnostics use VCSA shell and logs · escalation bundles logs for GSS │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issues      │   Diagnostics    │     Log Paths     │    Escalation    │     Recovery     │   │
│   │  SSO login fail  │    VCSA shell    │    /var/log/sso   │  VCSA bndl.tgz   │   Restart SSO    │   │
│   │   Cert expired   │   VAMI health    │  /var/log/vmware  │   GSS P1 case    │  Cert re-issue   │   │
│   │  VCSA svc down   │    API debug     │   /var/log/vpxd   │   TAM escalate   │ Restart service  │   │
│   │  HA split-brain  │    vcsa-check    │   /var/log/vmsvc  │   RCA template   │    HA re-init    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server (VCSA VM) · RAM DIMMs · Network NICs · Shared datastore · OOB management                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSO           = Single Sign-On; vSphere identity service; login failures from cert or clock issues   │
│  VCSA shell    = Bash shell on VCSA; enabled via VAMI or SSH; run service-control and log review      │
│  VAMI          = vCenter Appliance Management Interface; port 5480; shows service and health status   │
│  vpxd          = Main vCenter process (VMware vCenter Server daemon); restart to recover vCenter UI   │
│  /var/log/vmware = VCSA log directory; vpxd.log, sso/vmware-sts*.log, vapi-endpoint.log               │
│  vcsa-check    = VMware script validating VCSA service and configuration health pre/post upgrade      │
│  vCenter HA split-brain = Both active and passive nodes active; isolate passive and re-init HA        │
│  VCSA support bundle = Full log archive generated via VAMI or CLI; attach to GSS support case         │
│  PSC           = Platform Services Controller; embedded 7.0+; SSO token and certificate management    │
│  LCM task      = Lifecycle Manager upgrade task; if stuck, check vpxd.log and LCM log for errors      │
│  Certificate cascade = Expired VMCA root invalidates all child certs simultaneously across cluster    │
│  RCA           = Root Cause Analysis; post-incident document capturing timeline, cause, and fix       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known failure modes, symptoms, causes, and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>What to collect before opening a support case and how to engage vendor support.</span>
</a>

</div>

