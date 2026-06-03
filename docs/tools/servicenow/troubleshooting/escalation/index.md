# ServiceNow Escalation

```yaml
SUBJECT: [PROD] [P1] Instance unavailable — login page not loading

INSTANCE: mycompany.service-now.com
BUILD: Yokohama Patch 5 (check stats.do)
PRIORITY REQUESTED: P1 Critical
ISSUE START TIME: 2026-05-08 09:00 UTC

---
ISSUE DESCRIPTION:
Production instance is returning HTTP 503 for all requests since 09:00 UTC.
Users cannot log in. All business operations dependent on ServiceNow are halted.

IMPACT:
- 500+ users unable to access ServiceNow
- ITSM incident management unavailable
- Service desk operating on manual processes

STEPS TO REPRODUCE:
1. Navigate to https://mycompany.service-now.com
2. Observe HTTP 503 response (confirmed via curl from multiple locations)

WHAT HAS BEEN CHECKED:
- ServiceNow Status page (status.servicenow.com): No active incidents for EMEA
- stats.do: Unreachable
- Network: Outbound connectivity from user locations confirmed working

LOGS:
[Paste any available error messages]

DIAGNOSTICS ATTACHED:
- curl output showing 503 response
- Screenshot of status.servicenow.com

CONTACT:
Primary: Chris Anastasiadis, platform-team@example.com, +44-xxx-xxx-xxxx
Secondary: [Platform Lead name + contact]
```

```text
┌──────────────────────────────────────── ServiceNow Escalation ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Escalation Path                                        │   │
│   │                       L1: Local admin → check logs, ECC queue, stats.do                       │   │
│   │                   L2: ServiceNow support → HI portal case with instance logs                  │   │
│   │                    L3: ServiceNow engineering → P1 hotfix or patch request                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │              Before Escalating               │                                                    │
│   │           Capture stats.do output            │                                                    │
│   │            Export sys_log entries            │                                                    │
│   │           Note exact error + time            │                                                    │
│   │             Check Known Error DB             │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                HI Portal Case               │   │
│                                                     │           Instance name + version           │   │
│                                                     │              Steps to reproduce             │   │
│                                                     │            Attach diagnostics zip           │   │
│                                                     │             Set correct severity            │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · HI (High Impact) support portal · ServiceNow NOC                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HI Portal   = Hi.service-now.com; ServiceNow customer support case management                        │
│  P1          = Priority 1 incident; production down; 24x7 response from ServiceNow                    │
│  Diagnostics zip= stats.do + sys_log export + thread dump; attach to HI case                          │
│  Known Error = documented known issue in ServiceNow KB with workaround                                │
│  Hotfix      = emergency patch for critical defect outside normal release cycle                       │
│  Instance version= ServiceNow release (e.g. Xanadu Patch 3); visible at /stats.do                     │
│  Thread dump = JVM stack trace; identifies deadlocked or stuck threads                                │
│  sys_log     = application log; filter by level=error and time of incident                            │
│  NOC         = ServiceNow Network Operations Centre; monitors platform health                         │
│  Severity    = P1 production down, P2 major function impaired, P3 minor issue                         │
│  Patch       = scheduled fix release; applied during maintenance window                               │
│  Reproduce   = confirm issue in sub-production instance to isolate platform vs config                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
