# Architecture
## Purpose

Use this page for practical Vmware Cloud Foundation Architecture notes, checks, troubleshooting, commands, change notes, and field references.


## SDDC Stack Architecture

```mermaid
graph TB
  SDDC["SDDC Manager\n(VCF orchestration)"] --> MGMT["Management Domain\nvCenter · NSX · vSAN"]
  SDDC --> WL1["Workload Domain I\n(VI workloads)"]
  SDDC --> WL2["Workload Domain II\n(VVF cloud workloads)"]
  MGMT --> EMH["ESXi Mgmt Hosts\n(4 minimum)"]
  WL1 --> EWH["ESXi Workload Hosts"]
  SDDC --> CLOUD["VMware Cloud\n(optional hybrid)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class SDDC mgmt
  class MGMT,WL1,WL2 ctrl
  class EMH,EWH host
  class CLOUD cloud
```

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful commands

Add tested commands here.

## Known issues

Add known issues here as they come up.
