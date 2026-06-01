# Disaster Recovery Runbook


<div class="kb-summary">
Disaster Recovery Runbook reference covering Overview, Activation Criteria, Communication Tree, Phased Recovery Procedure, Validation Checklist and 1 more sections.
</div>

```
┌───────────────────────────────────────────── DR Runbook ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       DR Runbook — pre-defined response steps for declared disaster across all DR tools       │   │
│   │                   See product-specific sub-sections for detailed procedures                   │   │
│   │          DR success depends on: documented runbooks · tested failover · validated RTO         │   │
│   │          Minimum DR posture: defined RPO/RTO · tested backups · known escalation path         │   │
│   │        Test DR procedures quarterly; document results; update runbooks after each test        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery                    │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  DR Test       = planned failover test; validates RTO without real disaster                           │
│  Replication   = continuous or periodic data copy to secondary site or vault                          │
│  Recovery Tier = classification: hot/warm/cold based on RTO requirement                               │
│  BIA           = Business Impact Analysis; drives RPO/RTO targets per system                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────────────── DR Runbook ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       DR Runbook — pre-defined response steps for declared disaster across all DR tools       │   │
│   │                   See product-specific sub-sections for detailed procedures                   │   │
│   │          DR success depends on: documented runbooks · tested failover · validated RTO         │   │
│   │          Minimum DR posture: defined RPO/RTO · tested backups · known escalation path         │   │
│   │        Test DR procedures quarterly; document results; update runbooks after each test        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Production site · DR site · Replication link · Management network · Vault network                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO           = Recovery Point Objective; max acceptable data loss window                            │
│  RTO           = Recovery Time Objective; max acceptable downtime before restore                      │
│  Failover      = activating the DR site; redirecting hosts to replica resources                       │
│  Failback      = returning operations to production site after DR resolved                            │
│  Runbook       = step-by-step documented procedure for a specific DR scenario                         │
│  IRE           = Isolated Recovery Environment; air-gapped clean-room for recovery                    │
│  Clean Room    = isolated vCenter + workstations for cyber recovery validation                        │
│  Air Gap       = network isolation preventing attacker lateral movement to vault                      │
│  DR Test       = planned failover test; validates RTO without real disaster                           │
│  Replication   = continuous or periodic data copy to secondary site or vault                          │
│  Recovery Tier = classification: hot/warm/cold based on RTO requirement                               │
│  BIA           = Business Impact Analysis; drives RPO/RTO targets per system                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

This runbook defines the activation criteria, phased recovery procedures, communication obligations, and validation requirements for declaring and executing a disaster recovery event. It applies to all infrastructure tiers managed under this platform.

---

## Activation Criteria

A DR event may be declared when one or more of the following conditions are met. The declaring authority varies by severity.

| Severity | Condition | Declaring Authority | RPO/RTO Target |
|---|---|---|---|
| **P1 — Critical** | Full data centre loss, unrecoverable storage failure, ransomware with confirmed data corruption | CTO or VP Infrastructure | RPO ≤ 1 hr / RTO ≤ 4 hr |
| **P2 — Major** | Site-level network outage > 2 hrs with no restoration ETA, primary vCenter/management plane loss | Infrastructure Director | RPO ≤ 4 hr / RTO ≤ 8 hr |
| **P3 — Significant** | Single application tier failure unrecoverable in-place, loss of backup target for > 24 hrs | Lead Platform Engineer | RPO ≤ 24 hr / RTO ≤ 24 hr |
| **Cybersecurity** | Active compromise of production environment confirmed by Security team | CISO + CTO jointly | Isolate first; RTO determined post-containment |

> Before declaring a DR event, confirm: (1) the fault is not resolvable within normal incident process, (2) the DR site / backup infrastructure is healthy, and (3) relevant stakeholders have been engaged.

---

## Communication Tree

Notify in the order below at each phase. Do not skip tiers — escalate if a contact is unreachable after two attempts.

| Phase | Who to Notify | Method | Owner |
|---|---|---|---|
| **Declaration** | CTO, CISO, VP Infrastructure | Phone call | Incident Commander |
| **Declaration** | Platform Engineering team | Incident bridge / Slack #dr-active | Infrastructure Director |
| **Declaration** | Application owners (P1/P2 only) | Email + phone | Incident Commander |
| **Execution start** | All staff (P1 only) | Company-wide email from CEO/CTO | Communications lead |
| **Execution start** | Key customers / SLA holders | Account Manager outreach | Customer Success lead |
| **Progress (every 30 min)** | Stakeholder group | Incident bridge status update | Incident Commander |
| **Recovery complete** | All notified parties | Written update via email | Incident Commander |
| **Post-DR review** | Platform Engineering + Management | Scheduled meeting (48 hrs post-recovery) | Infrastructure Director |

---

## Phased Recovery Procedure

### Phase 0 — Declare and Mobilise (T+0 to T+30 min)

| Step | Action | Owner | Est. Time |
|---|---|---|---|
| 0.1 | Confirm activation criteria met; declare DR event formally | Incident Commander | 5 min |
| 0.2 | Open incident bridge (Zoom/Teams war room) and Slack #dr-active channel | Incident Commander | 5 min |
| 0.3 | Notify communication tree (Declaration phase — see above) | Incident Commander | 10 min |
| 0.4 | Confirm DR site / recovery infrastructure is available and healthy | Lead Platform Engineer | 10 min |
| 0.5 | Assign roles: Network lead, Storage lead, Compute lead, App lead | Infrastructure Director | 5 min |

### Phase 1 — Network and Management Plane (T+30 to T+90 min)

| Step | Action | Owner | Est. Time |
|---|---|---|---|
| 1.1 | Confirm DR site network segments are active; verify firewall rules | Network lead | 15 min |
| 1.2 | Validate DNS resolution at DR site (internal + external) | Network lead | 10 min |
| 1.3 | Power on / verify management infrastructure: vCenter, NSX Manager, vRO | Compute lead | 20 min |
| 1.4 | Confirm backup/DR management plane reachable (SRM, Veeam, NetBackup) | Storage lead | 15 min |

### Phase 2 — Storage and Data Recovery (T+90 to T+180 min)

| Step | Action | Owner | Est. Time |
|---|---|---|---|
| 2.1 | Assess RPO: check replication lag on RecoverPoint / SRM protection groups | Storage lead | 15 min |
| 2.2 | Initiate SRM recovery plan or RecoverPoint failover for affected CGs | Storage lead | 30 min |
| 2.3 | Verify datastore mounts at DR site; confirm no VMFS resignaturing required | Storage lead | 15 min |
| 2.4 | Run Veeam / NetBackup restore for any systems not covered by replication | Storage lead | Variable |

### Phase 3 — Compute and Application Recovery (T+180 to T+300 min)

| Step | Action | Owner | Est. Time |
|---|---|---|---|
| 3.1 | Power on VMs in dependency order: domain controllers → middleware → app tier | Compute lead | 30 min |
| 3.2 | Confirm AD replication and DNS are functioning at DR site | Network lead | 15 min |
| 3.3 | Application owners validate each application tier (see Validation Checklist) | App leads | 60 min |
| 3.4 | Redirect external traffic (DNS failover, load balancer cutover) | Network lead | 15 min |
| 3.5 | Confirm monitoring agents reporting to DR-site monitoring stack | Platform Eng | 15 min |

### Phase 4 — Stabilise and Operate from DR (T+300 min onward)

| Step | Action | Owner | Est. Time |
|---|---|---|---|
| 4.1 | Brief all application teams: DR site is now production | Incident Commander | 30 min |
| 4.2 | Confirm backup jobs are running against DR-site workloads | Storage lead | 15 min |
| 4.3 | Disable replication from (failed) primary site to avoid data conflicts | Storage lead | 15 min |
| 4.4 | Begin 30-minute status update cadence until primary site recovery is scoped | Incident Commander | Ongoing |

---

## Validation Checklist

Run all checks after Phase 3 is complete. Record pass/fail and the name of the engineer who validated each item.

| System / Service | Validation Command / Test | Pass Criteria |
|---|---|---|
| Active Directory | `nltest /dsgetdc:<domain> /force` on a domain member | Returns a DC at the DR site; no LDAP errors |
| DNS resolution | `nslookup <internal-fqdn> <dr-dc-ip>` | Resolves correctly in < 500 ms |
| vCenter availability | Browse `https://<dr-vcenter>/ui` | Login succeeds; all hosts visible and green |
| NSX Manager | Browse `https://<dr-nsx-manager>` | All transport nodes connected |
| Storage paths | `esxcli storage nmp device list` on DR ESXi host | All expected LUNs present with Active (I/O) paths |
| Veeam VBR | VBR console → Home → Jobs | No jobs in error; proxy/repo infrastructure green |
| NetBackup | `bpps -a` on master server | All core daemons running: bprd, bpdbm, nbsl, nbwmc |
| Primary application | HTTP GET `https://<app-url>/health` | HTTP 200; response body confirms healthy |
| Database tier | Application-specific query or `SELECT 1` via DBA | Returns result in < 2 s; no replication lag errors |
| External DNS | `dig @8.8.8.8 <public-fqdn>` | Resolves to DR-site public IP |
| TLS certificates | `openssl s_client -connect <app-fqdn>:443 </dev/null` | Certificate valid, not expired, chain trusted |
| Monitoring | Grafana / monitoring UI | DR-site dashboards active; alert routing confirmed |
| Backup jobs | Veeam / NetBackup job history | At least one successful backup since cutover |

---

## Return-to-Normal Checklist (Failback)

Only begin failback after the primary site is confirmed healthy and capacity has been validated.

| Step | Action | Owner | Notes |
|---|---|---|---|
| F.1 | Confirm primary site infrastructure is fully restored and tested | Infrastructure Director | Do not failback to an untested site |
| F.2 | Re-enable replication from DR site back to primary (reverse replication) | Storage lead | Use RecoverPoint re-protect or SRM re-protect workflow |
| F.3 | Allow replication to synchronise; verify lag reaches near-zero | Storage lead | Monitor via `boxmgmt cgs show_lag` or SRM dashboard |
| F.4 | Schedule failback window; notify all application owners and stakeholders | Incident Commander | Treat as a planned maintenance event |
| F.5 | Execute planned failback (SRM planned migration or RecoverPoint planned failover) | Storage lead | Confirm all VMs gracefully shut down before storage switch |
| F.6 | Validate all services at primary site using the Validation Checklist above | App leads | Run full checklist — do not assume success |
| F.7 | Redirect traffic back to primary site (DNS, load balancers) | Network lead | Verify external resolution before closing the event |
| F.8 | Re-enable standard backup schedules targeting primary site storage | Storage lead | Confirm first backup job completes successfully |
| F.9 | Restore monitoring to primary-site configuration; decommission DR-site monitoring overrides | Platform Eng | Verify alerting is routing correctly |
| F.10 | Hold post-DR review meeting within 48 hours | Infrastructure Director | Document timeline, gaps, action items — update this runbook |

### Post-DR Review Agenda

- Timeline reconstruction: when was the incident detected, declared, and resolved?
- RPO and RTO actuals vs targets — did we meet them?
- What went well and what failed?
- Action items with owners and due dates
- Runbook updates required based on lessons learned

> Update this runbook after every DR event and every annual DR test. Version-control all changes via git.
