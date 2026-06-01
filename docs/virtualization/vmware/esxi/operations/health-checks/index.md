# ESXi — Health Checks


<div class="kb-summary">
Health Checks reference covering Health Checklist.
</div>

```
┌──────────────────────────────────────── ESXi — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  Daily/weekly health runbook: hardware sensors, alarms, capacity, and storage.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Hardware Health                │  │            vSphere Cluster Health           │   │
│   │           IPMI/iDRAC sensor status           │  │          HA master elected & green          │   │
│   │            CPU/mem/fan/PSU alarms            │  │            DRS balance score < 2            │   │
│   │           esxcli hardware ipmi sdr           │  │          vMotion network reachable          │   │
│   │            HBA/NIC link state up             │  │            No disconnected hosts            │   │
│   │         Boot media health S.M.A.R.T.         │  │             EVC mode consistent             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Hardware sensors → vSphere alarms → storage health → capacity review.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Storage Health                │  │               Capacity Review               │   │
│   │           All paths active per LUN           │  │           Host CPU util < 70% avg           │   │
│   │           No APD/PDL events today            │  │           Host mem util < 80% avg           │   │
│   │             Datastore free > 20%             │  │             VM balloon/swap = 0             │   │
│   │          VMFS no ATS heartbeat err           │  │           vSAN disk capacity < 70%          │   │
│   │            vSAN health: all green            │  │          Trend forecast 30/60 days          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts with IPMI/iDRAC BMC, SAN/NAS/vSAN storage, 10/25 GbE NICs                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IPMI     = Intelligent Platform Mgmt Interface; OOB hardware sensor access                           │
│  iDRAC    = Dell Remote Access Controller; OOB management BMC                                         │
│  S.M.A.R.T = Self-Monitoring Analysis; disk health from boot media                                    │
│  APD      = All Paths Down; storage unreachable but PDL not declared                                  │
│  PDL      = Permanent Device Loss; device signals loss is permanent                                   │
│  ATS      = Atomic Test & Set; VMFS locking primitive; heartbeat mechanism                            │
│  DRS score= 1-5 imbalance rating; 1=balanced, 5=critical imbalance                                    │
│  Balloon  = VMware memory mgmt; guest driver returns idle pages to host                               │
│  EVC      = Enhanced vMotion Compat; consistent CPU flags across cluster                              │
│  fdm      = Fault Domain Manager; HA agent; must run on all hosts                                     │
│  vSAN health = Skyline Health dashboard in vCenter; 60+ automated checks                              │
│  BMC      = Baseboard Management Controller; embedded OOB management chip                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
ESXi Health Check — Decision Flow
                           │
           ┌───────────────▼───────────────┐
           │  Host Connection State?        │
           │  Get-VMHost | Select ...       │
           └──────┬──────────────┬─────────┘
                  │ Connected    │ Disconnected / NotResponding
                  │              └──► restart hostd/vpxa or IPMI
           ┌──────▼──────────────────────┐
           │  Hardware Health?           │
           │  esxcli hardware health get │
           └──────┬──────────────────────┘
                  │ Green        │ Warning/Error → alert ticket
           ┌──────▼──────────────────────┐
           │  Storage Paths?             │
           │  esxcli storage core path   │
           │  list | grep dead           │
           └──────┬──────────────────────┘
                  │ 0 dead paths │ Dead paths → rescan / escalate
           ┌──────▼──────────────────────┐
           │  NTP Running & Synced?      │
           │  esxcli system ntp get      │
           └──────┬──────────────────────┘
                  │ Running=true │ Not synced → fix NTP config
           ┌──────▼──────────────────────┐
           │  vmnic Uplinks Up?          │
           │  esxcli network nic list    │
           └──────┬──────────────────────┘
                  │ All up       │ Down links → check switch/cable
           ┌──────▼──────────────┐
           │  PASS — host healthy │
           └─────────────────────┘
```text
┌──────────────────────────────────────── ESXi — Health Checks ─────────────────────────────────────────┐
│                                                                                                       │
│  Daily/weekly health runbook: hardware sensors, alarms, capacity, and storage.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Hardware Health                │  │            vSphere Cluster Health           │   │
│   │           IPMI/iDRAC sensor status           │  │          HA master elected & green          │   │
│   │            CPU/mem/fan/PSU alarms            │  │            DRS balance score < 2            │   │
│   │           esxcli hardware ipmi sdr           │  │          vMotion network reachable          │   │
│   │            HBA/NIC link state up             │  │            No disconnected hosts            │   │
│   │         Boot media health S.M.A.R.T.         │  │             EVC mode consistent             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Hardware sensors → vSphere alarms → storage health → capacity review.                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Storage Health                │  │               Capacity Review               │   │
│   │           All paths active per LUN           │  │           Host CPU util < 70% avg           │   │
│   │           No APD/PDL events today            │  │           Host mem util < 80% avg           │   │
│   │             Datastore free > 20%             │  │             VM balloon/swap = 0             │   │
│   │          VMFS no ATS heartbeat err           │  │           vSAN disk capacity < 70%          │   │
│   │            vSAN health: all green            │  │          Trend forecast 30/60 days          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts with IPMI/iDRAC BMC, SAN/NAS/vSAN storage, 10/25 GbE NICs                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  IPMI     = Intelligent Platform Mgmt Interface; OOB hardware sensor access                           │
│  iDRAC    = Dell Remote Access Controller; OOB management BMC                                         │
│  S.M.A.R.T = Self-Monitoring Analysis; disk health from boot media                                    │
│  APD      = All Paths Down; storage unreachable but PDL not declared                                  │
│  PDL      = Permanent Device Loss; device signals loss is permanent                                   │
│  ATS      = Atomic Test & Set; VMFS locking primitive; heartbeat mechanism                            │
│  DRS score= 1-5 imbalance rating; 1=balanced, 5=critical imbalance                                    │
│  Balloon  = VMware memory mgmt; guest driver returns idle pages to host                               │
│  EVC      = Enhanced vMotion Compat; consistent CPU flags across cluster                              │
│  fdm      = Fault Domain Manager; HA agent; must run on all hosts                                     │
│  vSAN health = Skyline Health dashboard in vCenter; 60+ automated checks                              │
│  BMC      = Baseboard Management Controller; embedded OOB management chip                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Health Checklist

- [ ] All hosts Connected and PoweredOn
- [ ] No hardware health warnings or critical alerts
- [ ] All storage paths active — no dead paths
- [ ] All vmnic uplinks connected
- [ ] NTP running and synchronized
- [ ] No vmkernel errors in recent log entries
- [ ] PowerCLI hardware summary clean
- [ ] No unexpected maintenance mode hosts
