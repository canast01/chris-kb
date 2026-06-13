---
tags:
  - windows
---
# Active Directory

<div class="kb-summary">
Windows Server Active Directory knowledge base covering forest and domain architecture, FSMO roles, Kerberos authentication, replication topology, GPO management, and troubleshooting for enterprise directory environments.
</div>
```text
┌────────────────────────────────────── Security Active Directory ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Active Directory: Security Active Directory platform                     │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                    Management: Security Active Directory management console                   │   │
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
│    Physical: Security Active Directory infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Active Directory   = Security Active Directory platform overview and core concepts                 │
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
┌──────────────────────────── Active Directory — Forest Deployment Sequence ────────────────────────────┐
│                                                                                                       │
│  Step 1 · Infrastructure Prerequisites                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Windows Server 2022 (recommended)  ·  4 vCPU  ·  8 GB RAM  ·  60 GB OS disk                          │
│  Static IP on management VLAN  ·  DNS suffix matches planned domain name                              │
│  NTP: point to reliable time source before promoting  ·  PDC will be stratum 2                        │
│  Network: DCs on VLAN accessible to all client VLANs  ·  port 88 (Kerberos) open                      │
│  Plan: forest name, domain name, NetBIOS name, DSRM password (vault it)                               │
│                                                                                                       │
│                                        │  promote forest root DC                                      │
│                                        ▼                                                              │
│  Step 2 · Forest Root Domain Controller                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Install AD DS role  ·  run Install-ADDSForest -DomainName <fqdn> -InstallDns                         │
│  Set forest/domain functional level to 2016 minimum (2019 preferred)                                  │
│  Set DSRM password (document in vault)  ·  reboot  ·  confirm AD DS service running                   │
│  Verify DNS: nslookup <domain>  ·  test Kerberos: klist  ·  check _msdcs SRV records                  │
│  Run dcdiag /test:all  ·  netlogon SYSVOL share visible  ·  repadmin /showrepl clean                  │
│                                                                                                       │
│                                        │  add replica DCs                                             │
│                                        ▼                                                              │
│  Step 3 · Replica Domain Controllers                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Promote 2+ additional DCs per domain: Install-ADDSDomainController -DomainName                       │
│  Stagger promotions  ·  verify AD replication after each: repadmin /replsummary                       │
│  Distribute DCs across physical hosts and sites (never co-locate all on one hypervisor)               │
│  Configure each DC as a DNS server  ·  register all DC IPs in DNS scavenging                          │
│  Set DC as NTP client of PDC emulator  ·  all member servers point to DCs for NTP                     │
│                                                                                                       │
│                                        │  verify FSMO role placement                                  │
│                                        ▼                                                              │
│  Step 4 · FSMO Roles                                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Forest roles (Schema Master, Domain Naming Master): remain on forest root DC                         │
│  Domain roles (PDC Emulator, RID Master, Infrastructure Master): distribute per site                  │
│  Transfer PDC Emulator to the most reliable, best-connected DC in primary site                        │
│  Verify: netdom query fsmo  ·  document FSMO holder hostnames in runbook                              │
│  Test PDC emulator failover procedure: transfer role, test auth, transfer back                        │
│                                                                                                       │
│                                        │  configure DNS, sites, and subnets                           │
│                                        ▼                                                              │
│  Step 5 · DNS, Sites & Subnets                                                                        │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create AD sites: Active Directory Sites and Services → New Site per physical location                │
│  Create subnets and associate to sites  ·  enables optimal DC referral for clients                    │
│  Configure site links and replication intervals  ·  enable change notification on LAN                 │
│  AD-integrated DNS zones (automatic)  ·  enable DNS scavenging (14-day intervals)                     │
│  Verify conditional forwarders for all internal domains  ·  stub zones to external DNS                │
│                                                                                                       │
│                                        │  deploy GPO security baseline                                │
│                                        ▼                                                              │
│  Step 6 · GPO Security Baseline                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Create Default Domain Policy: password complexity, length ≥14, history 24, lockout 5                 │
│  Create DC security baseline GPO: audit policy, SMB signing, NTLMv2 only, no LM hash                  │
│  Deploy LAPS (Local Administrator Password Solution)  ·  randomises local admin                       │
│  Link CIS/STIG baseline GPO to all OUs  ·  test with gpresult /h before wide rollout                  │
│  Enable advanced audit policy: logon events, account management, directory service                    │
│  Test: login, GPO apply, replication, and restore of deleted object from Recycle Bin                  │
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
