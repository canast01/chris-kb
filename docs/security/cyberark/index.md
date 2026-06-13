---
tags:
  - security
---
# CyberArk

<div class="kb-summary">
CyberArk Privileged Access Manager knowledge base covering Digital Vault architecture, CPM rotation, PSM session proxying, PVWA administration, DR activation, and PAM hardening for enterprise privileged access environments.

*Applies to: CyberArk PAM*
</div>
```text
┌────────────────────────────────────────── Security Cyberark ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Cyberark: Security Cyberark platform                             │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                        Management: Security Cyberark management console                       │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Cyberark infrastructure · management network · monitoring                       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Cyberark           = Security Cyberark platform overview and core concepts                         │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```



```text
┌───────────────────────────────── CyberArk PAM — Deployment Sequence ──────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Windows Server 2019+  ·  8 vCPU  ·  16 GB RAM for Vault  ·  200 GB dedicated disk                    │
│  AD service accounts: Vault admin, CPM, PSM, PVWA  ·  all pre-created in dedicated OU                 │
│  TCP 1858 (Vault)  ·  443 (PVWA)  ·  1858+2022 (PSM RDP proxy)  ·  8080 (CPM)                         │
│  SQL Server for PVWA (or PostgreSQL)  ·  NTP synced  ·  all FQDNs in DNS                              │
│  Obtain CyberArk licence  ·  download installation packages from CyberArk Marketplace                 │
│                                                                                                       │
│                                        │  install Digital Vault                                       │
│                                        ▼                                                              │
│  Step 2 · Digital Vault                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install CyberArk Digital Vault on isolated hardened Windows Server                                   │
│  Run PAReplicate to set Vault master CD encryption key  ·  store CD in physical safe                  │
│  Complete Vault installation wizard  ·  set Vault admin password  ·  vault starts                     │
│  Verify CyberArk Vault service running  ·  test Vault connectivity with PrivateArk Client             │
│  Apply Vault hardening baseline: disable unnecessary services, restrict local logon                   │
│                                                                                                       │
│                                        │  install DR Vault                                            │
│                                        ▼                                                              │
│  Step 3 · DR Vault                                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install DR Vault on separate server (different rack/site)  ·  same version as primary                │
│  Configure VaultReplication.ini  ·  test initial sync from primary to DR Vault                        │
│  Verify DR Vault receives and stores replication  ·  document manual failover steps                   │
│  Test DR activation: stop primary  ·  activate DR  ·  verify PVWA connects to DR Vault                │
│  Document and rehearse Vault failover runbook with ops team quarterly                                 │
│                                                                                                       │
│                                        │  install CPM                                                 │
│                                        ▼                                                              │
│  Step 4 · Central Policy Manager (CPM)                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install CPM on dedicated Windows Server  ·  connect CPM to Vault during setup                        │
│  Import platform packages (Windows, Unix, Oracle, AD) via PVWA Platform Management                    │
│  Configure account platform policies: rotation interval, complexity, reconcile account                │
│  Test password rotation: onboard a test account  ·  verify rotation and verify new creds              │
│  Enable Dual Control for critical platforms: rotation requires approval workflow                      │
│                                                                                                       │
│                                        │  deploy PVWA and PSM                                         │
│                                        ▼                                                              │
│  Step 5 · PVWA & PSM                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install PVWA on Windows IIS server  ·  SQL connection configured  ·  SSL cert applied                │
│  Configure LDAP/AD integration in PVWA  ·  map AD groups to CyberArk roles                            │
│  Install PSM on dedicated Windows Server  ·  RDP Connector  ·  SSH proxy configured                   │
│  Configure PSM connection components per target platform (RDP, SSH, Web, etc.)                        │
│  Test end-to-end: login to PVWA → launch PSM session → PSM records session                            │
│                                                                                                       │
│                                        │  onboard accounts and validate                               │
│                                        ▼                                                              │
│  Step 6 · Account Onboarding & Validation                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install Connector (CCP/AIM) for application credential retrieval if needed                           │
│  Onboard privileged accounts: administrators, service accounts, root, break-glass                     │
│  Assign accounts to Safes with PVWA role-based access (no direct vault access)                        │
│  Run Discovery: scan subnets for unmanaged privileged accounts  ·  remediate gaps                     │
│  Validate: session recording plays back  ·  CPM rotated successfully  ·  audit log entries            │
│  Go-live checklist: DR tested  ·  backup verified  ·  SIEM integration  ·  on-call briefed            │
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
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, and scripts.</span>
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

