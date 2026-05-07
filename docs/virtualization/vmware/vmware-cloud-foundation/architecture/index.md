# Architecture
## Purpose

Use this page for practical Vmware Cloud Foundation Architecture notes, checks, troubleshooting, commands, change notes, and field references.


## SDDC Stack Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  VMware Cloud Foundation (VCF)                           │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  SDDC Manager                                                   │    │
  │  │  Lifecycle orchestration  |  Workload domain management         │    │
  │  │  Certificate / password management  |  API / UI                 │    │
  │  └───────────────────────────────────────────────────────────────── ┘    │
  │          │  manages                                                      │
  │  ┌───────┴────────────────────────────────────────────────────────┐     │
  │  │  Workload Domains                                              │     │
  │  │  ┌──────────────────────┐    ┌──────────────────────────────┐  │     │
  │  │  │  Management Domain   │    │  VI Workload Domain(s)       │  │     │
  │  │  │  vCenter (mgmt)      │    │  vCenter (workload)          │  │     │
  │  │  │  NSX Manager cluster │    │  NSX (per domain or shared)  │  │     │
  │  │  │  vSAN (mgmt)         │    │  vSAN / external storage     │  │     │
  │  │  └──────────────────────┘    └──────────────────────────────┘  │     │
  │  └────────────────────────────────────────────────────────────────┘     │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Shared Services (Cloud Builder automates day-0 bring-up)       │    │
  │  │  vCenter  NSX  vSAN  SDDC Manager  Aria Ops  Aria Automation    │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  └──────────────────────────────────────────────────────────────────────────┘
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
