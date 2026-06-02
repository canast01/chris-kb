# SRM — Hardening


<div class="kb-summary">
Hardening reference covering Least-Privilege SRA Service Accounts, Rotate SRA Credentials, Test Recovery Plans Regularly, Restrict Who Can Execute Recovery, Secure Recovery Site Network Design and 3 more sections.
</div>

  SRM Hardening Controls
```text
┌──────────────────────────────────────────────────────────────┐
│  Network Restrictions        Access Controls                                                          │
│  ┌──────────────────────┐    ┌──────────────────────────┐                                             │
│  │ SRM ← only from:     │    │ Separate config role from │                                            │
│  │  vCenter TCP 443     │    │  run role:                │                                            │
│  │  Remote SRM TCP 9086 │    │  SRM Admin: config+run   │                                             │
│  │  Mgmt WS TCP 443     │    │  DR RunTeam: run only    │                                             │
│  └──────────────────────┘    └──────────────────────────┘                                             │
│                                                                                                       │
│  Test Network Isolation      Credential Rotation                                                      │
│  ┌──────────────────────┐    ┌──────────────────────────┐                                             │
│  │ Isolated portgroup:  │    │ SRA API token: rotate    │                                             │
│  │  no uplinks assigned │    │  quarterly               │                                             │
│  │ Test VMs must NOT    │    │ 1. New token on array    │                                             │
│  │  reach production    │    │ 2. Update in SRM         │                                             │
│  └──────────────────────┘    │ 3. Delete old token      │                                             │
│                              └──────────────────────────┘                                             │
└──────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── VMware SRM — Hardening ────────────────────────────────────────┐
│                                                                                                       │
│  SRM hardening: restrict failover to authorised users, enforce TLS 1.2+, isolate                      │
│  SRM management traffic, audit all plan runs, and use MFA for DR access.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Access Hardening               │  │              Network Hardening              │   │
│   │         SRM Admin: 2–3 accounts max          │  │             Mgmt VLAN: isolated             │   │
│   │             MFA: via vCenter SSO             │  │            No SRM from guest nets           │   │
│   │          Dual-person: real failover          │  │             WAN: encrypted link             │   │
│   │         Least privilege: plan tester         │  │           Firewall: SRM ↔ SRM only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Dual-person control for real failover prevents accidental production impact.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Config Hardening               │  │              Audit & Compliance             │   │
│   │           TLS 1.2 min: disable old           │  │          Log: all plan runs + user          │   │
│   │       Enterprise cert: replace self-s        │  │             SIEM: vCenter events            │   │
│   │           Patch: SRM on 30-day SLA           │  │           DR test evidence: stored          │   │
│   │          SQL: TDE + regular backup           │  │            Quarterly: role audit            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server VMs on management network; WAN replication over encrypted link;                           │
│  SQL Server VM hardened separately with Windows security baseline.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dual-person   = two approvals required to trigger real failover                                      │
│  Least privilege= Plan Admin role for testers; Admin for DR team only                                 │
│  TLS 1.2       = disable TLS 1.0/1.1 via IIS TLS settings on SRM                                      │
│  Enterprise cert= replace self-signed for compliance; re-pair required                                │
│  SQL TDE       = Transparent Data Encryption for SRM config DB                                        │
│  MFA           = enforced at SSO layer; requires RADIUS or smart card                                 │
│  SIEM          = collect vCenter events including SRM failover events                                 │
│  Evidence      = DR test results; screenshot or export of plan run                                    │
│  Quarterly audit= review SRM admin + plan admin role assignments                                      │
│  WAN encrypted = IPSEC or MPLS encryption for replication traffic                                     │
│  Patch SLA     = apply SRM patches within 30 days of release                                          │
│  DR test evidence= required for DR compliance (ISO 22301, SOC 2)                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── VMware SRM — Hardening ────────────────────────────────────────┐
│                                                                                                       │
│  SRM hardening: restrict failover to authorised users, enforce TLS 1.2+, isolate                      │
│  SRM management traffic, audit all plan runs, and use MFA for DR access.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Access Hardening               │  │              Network Hardening              │   │
│   │         SRM Admin: 2–3 accounts max          │  │             Mgmt VLAN: isolated             │   │
│   │             MFA: via vCenter SSO             │  │            No SRM from guest nets           │   │
│   │          Dual-person: real failover          │  │             WAN: encrypted link             │   │
│   │         Least privilege: plan tester         │  │           Firewall: SRM ↔ SRM only          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Dual-person control for real failover prevents accidental production impact.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Config Hardening               │  │              Audit & Compliance             │   │
│   │           TLS 1.2 min: disable old           │  │          Log: all plan runs + user          │   │
│   │       Enterprise cert: replace self-s        │  │             SIEM: vCenter events            │   │
│   │           Patch: SRM on 30-day SLA           │  │           DR test evidence: stored          │   │
│   │          SQL: TDE + regular backup           │  │            Quarterly: role audit            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SRM Server VMs on management network; WAN replication over encrypted link;                           │
│  SQL Server VM hardened separately with Windows security baseline.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Dual-person   = two approvals required to trigger real failover                                      │
│  Least privilege= Plan Admin role for testers; Admin for DR team only                                 │
│  TLS 1.2       = disable TLS 1.0/1.1 via IIS TLS settings on SRM                                      │
│  Enterprise cert= replace self-signed for compliance; re-pair required                                │
│  SQL TDE       = Transparent Data Encryption for SRM config DB                                        │
│  MFA           = enforced at SSO layer; requires RADIUS or smart card                                 │
│  SIEM          = collect vCenter events including SRM failover events                                 │
│  Evidence      = DR test results; screenshot or export of plan run                                    │
│  Quarterly audit= review SRM admin + plan admin role assignments                                      │
│  WAN encrypted = IPSEC or MPLS encryption for replication traffic                                     │
│  Patch SLA     = apply SRM patches within 30 days of release                                          │
│  DR test evidence= required for DR compliance (ISO 22301, SOC 2)                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Rotate SRA Credentials

Rotate array credentials in SRM on a regular schedule (quarterly or when personnel changes):

```text
1. Create new API token / password on storage array
2. Site Recovery → Storage → Array Pairs → [pair] → Configure Adapter → Update credentials
3. Test: Site Recovery → Storage → Array Pairs → Discover Devices (verify discovery succeeds)
4. Delete old token / change old password on array
5. Repeat for recovery site SRM Server
```

---

## Test Recovery Plans Regularly

Monthly testing is the single most effective hardening measure for DR:

```text
Site Recovery → Recovery Plans → [plan] → Test
  Frequency: monthly minimum for critical plans, quarterly for non-critical
  Document: pass/fail, duration, issues found, actions taken
```

An untested recovery plan is not a recovery plan — it's a guess.

---

## Restrict Who Can Execute Recovery

```text
vCenter → Administration → Global Permissions
  DR Run Team: Site Recovery Recovery Admin role (can execute plans, cannot configure)
  SRM Admins: Site Recovery Administrator role (can configure and execute)

Process: DR execution requires approval from two DR team members (documented in runbook)
```

---

## Secure Recovery Site Network Design

Test failover uses an "isolated network" — verify it is truly isolated:

```text
vCenter (Recovery Site) → Networking → [isolated portgroup] → 
  Verify: no uplinks assigned (isolated portgroup = no physical NIC)
  OR: dedicated VLAN with all-deny firewall rule at switch

If test VMs can ping production IPs, the test network is NOT isolated.
```

---

## Windows Hardening of SRM Server

```powershell
# Disable unused services on SRM Server OS
Stop-Service -Name "RemoteRegistry" -ErrorAction SilentlyContinue
Set-Service -Name "RemoteRegistry" -StartupType Disabled

# Configure NTP
w32tm /config /manualpeerlist:"ntp.example.local" /syncfromflags:manual /reliable:yes
w32tm /config /update

# Enable Windows Defender or your corporate AV (with exclusions):
# Exclude: C:\Program Files\VMware\VMware vCenter Site Recovery Manager\
```

---

## Audit Recovery Plan Changes

```bash
vCenter → Monitor → Events
  Filter: "drm" events (all SRM events)
  Alert on: Recovery Plan configuration changes, SRA credential updates

Export weekly audit report:
vCenter → Monitor → Events → Export → filter by "drm"
```

---

## Review and Remove Stale Protection Groups

Quarterly: audit protection groups for VMs that have been decommissioned:

```powershell
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    $vmNames = $vms | Select-Object -ExpandProperty Vm | Select-Object -ExpandProperty Name
    Write-Host "PG: $($pg.Name) — VMs: $($vmNames -join ', ')"
}
# Cross-reference with current VM inventory — remove protection for decommissioned VMs
```
