# Aria Suite Lifecycle

<div class="kb-summary">
Technical and operational reference for VMware Aria Suite Lifecycle Manager. Covers deployment, patching, certificate management, upgrade orchestration, and environment health for all Aria Suite products.
</div>

```text
┌───────────────────────────────── Aria Suite Lifecycle Manager Stack ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             VMware Aria Suite Lifecycle Manager (Aria SuiteLC) — Aria Product LCM             │   │
│   │      Deploys and upgrades: Aria Operations, Logs, Networks, Automation, and Workspace ONE     │   │
│   │     Environment: logical grouping of Aria products sharing vSphere infra and certificates     │   │
│   │      Certificate manager: Aria SuiteLC manages TLS certs for all Aria products centrally      │   │
│   │         Locker: secure credential store for passwords, certificates, and licence keys         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Aria SuiteLC deploys products · manages their certs and passwords · executes upgrades              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │    Global env: infra acct   │  │    Deploy: product wizard   │  │    Locker: creds + certs    │   │
│   │   Product env: Aria suite   │  │   Upgrade: binary + apply   │  │   Cert replace: all prods   │   │
│   │    Binary mapping: depot    │  │    Cert: rotate on demand   │  │     RBAC: admin + viewer    │   │
│   │    vSphere: infra account   │  │   Health: env health check  │  │   Password: scheduled rot   │   │
│   │   Upgrade checker: pre-val  │  │    Scale: node add/remove   │  │      Audit: change log      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines environments · Operations deploy and upgrade                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │Upgrade precheck f│lcm-support bundle│ Env health: green?│   GSS + bundle   │  lcm-cli status  │   │
│   │Cert rotation fail│ certificate.log  │ Certs: valid +30d?│  TAM escalation  │  lcm-cli certs   │   │
│   │Product deploy stu│product-install.lo│ Binary: available?│Collect install lo│ lcm-cli products │   │
│   │Locker credential │locker-service.log│ Locker: reachable?│ P1: LCM failure  │  lcm-cli locker  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Aria SuiteLC VM on vSphere · vSphere infrastructure account · NFS/VMFS datastore · port 443          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Global environment= Aria SuiteLC top-level container; links to vSphere infra account and NTP/DNS     │
│  Product environment= Named grouping of Aria products sharing an infra account and cert authority     │
│  Infrastructure account= vCenter service account used by Aria SuiteLC to deploy product VMs           │
│  Locker        = Secure vault inside Aria SuiteLC; stores passwords, certs, and licence keys          │
│  Binary mapping = Links downloaded product installer to a product version for deployment/upgrade      │
│  Upgrade checker= Pre-upgrade compatibility validation; checks versions and health before proceeding  │
│  Certificate manager= Aria SuiteLC module that generates, replaces, and renews TLS certs for products │
│  Content management= Feature to import/export Aria product config (blueprints, dashboards) via LCM    │
│  Password rotation= Scheduled or manual rotation of product service account passwords via Locker      │
│  Scale out     = Adding nodes to a product (e.g. vROps data node) managed through Aria SuiteLC        │
│  Health check  = Aria SuiteLC environment health scan; validates products, certs, and credentials     │
│  Depot         = VMware Customer Connect binary source; Aria SuiteLC downloads product binaries       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────── Aria Suite Lifecycle Manager — Installation Sequence ─────────────────────────┐
│                                                                                                       │
│  Step 1 · Pre-Deploy Checks                                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  DNS A-record for LCM FQDN  ·  PTR record created  ·  Resolves from vCenter                           │
│  NTP sources confirmed  ·  vCenter service account with admin rights prepared                         │
│  Certificate Authority ready: LCM will need signed certs for all products                             │
│  Target datastore: ≥50 GB free for LCM VM  ·  Product datastores sized separately                     │
│  Internet or proxy access for downloading product binaries and patches                                │
│                                                                                                       │
│                                        │  deploy LCM OVA                                              │
│                                        ▼                                                              │
│  Step 2 · LCM OVA Deployment                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Download Aria Suite Lifecycle OVA from VMware portal                                                 │
│  Deploy OVA on vCenter: size small (labs) or medium (production)                                      │
│  Set management IP, gateway, DNS, NTP, admin password during deploy wizard                            │
│  Power on  ·  Access LCM UI at https://lcm-fqdn  ·  Initial login (admin/)                            │
│  Run initial setup wizard  ·  Accept EULA  ·  Enter licence key                                       │
│                                                                                                       │
│                                        │  configure certificates                                      │
│                                        ▼                                                              │
│  Step 3 · Certificate Configuration                                                                   │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Upload CA root and intermediate certificates to LCM trust store                                      │
│  Create certificate request for LCM itself: CN = LCM FQDN, SANs included                              │
│  Sign CSR with internal CA  ·  Import signed cert into LCM                                            │
│  Configure LCM to use CA-signed cert for all future product deployments                               │
│  Verify LCM UI accessible with trusted cert  ·  No browser warnings                                   │
│                                                                                                       │
│                                        │  integrate vCenter and identity                              │
│                                        ▼                                                              │
│  Step 4 · vCenter & Identity Integration                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Lifecycle Operations → Settings → vCenter Servers: add vCenter + credentials                         │
│  Add identity provider: Workspace ONE Access or vIDM appliance                                        │
│  Map AD groups to LCM roles: admin, operator, viewer                                                  │
│  Configure SMTP relay for email notifications (patch, deployment alerts)                              │
│  Test vCenter connectivity: verify LCM can browse inventory                                           │
│                                                                                                       │
│                                        │  onboard or deploy Aria products                             │
│                                        ▼                                                              │
│  Step 5 · Product Onboard / Deploy                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Lifecycle Operations → Environments → Create Environment                                             │
│  Add products: Aria Operations, Aria Automation, Aria Ops for Logs, etc.                              │
│  For existing installs: import environment (discover from vCenter)                                    │
│  For new installs: select binary, size, network, datastore  ·  LCM deploys                            │
│  Monitor deployment tasks  ·  Each product validated post-deploy by LCM                               │
│                                                                                                       │
│                                        │  day-2 operations                                            │
│                                        ▼                                                              │
│  Step 6 · Day-2 Operations                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Patch management: Lifecycle Operations → Environments → Trigger Upgrade                              │
│  Backup: configure snapshot/backup for LCM VM and all managed products                                │
│  Certificate renewal: LCM tracks cert expiry  ·  Automates renewal workflow                           │
│  Scale: add worker nodes or replicas through LCM for capacity growth                                  │
│  Health: LCM health dashboard shows deployment and cert status per product                            │
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
  <span>Step-by-step initial LCM deployment: OVA, Locker, depot sync, and first product environment.</span>
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
