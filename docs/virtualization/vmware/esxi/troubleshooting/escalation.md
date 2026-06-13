---
tags:
  - esxi
  - troubleshooting
  - vmware
  - vsphere-8
search:
  boost: 1.5
---
# ESXi — Escalation

```text
┌────────────────────────────────────────── ESXi — Escalation ──────────────────────────────────────────┐
│                                                                                                       │
│  VMware GSS escalation, support bundle collection, and severity level matrix.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Decision              │  │             Pre-Escalation Steps            │   │
│   │            PSOD / data loss risk             │  │            Collect support bundle           │   │
│   │           Unexplained host failure           │  │           Document symptoms + time          │   │
│   │          Storage APD not resolving           │  │             Capture esxtop batch            │   │
│   │          Cluster HA not recovering           │  │          Note ESXi/vCenter version          │   │
│   │          Suspected driver/firmware           │  │           Verify HCL status first           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Internal diagnosis → pre-escalation bundle → VMware SR → severity match.                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Severity Levels                │  │           Support Bundle Contents           │   │
│   │           S1: prod down, data loss           │  │             /var/log/* all logs             │   │
│   │           S2: major feature broken           │  │              vmkernel PSOD dump             │   │
│   │           S3: degraded, workaround           │  │            Hardware config + HCL            │   │
│   │              S4: info/question               │  │           Network config (vmknic)           │   │
│   │           S1 = 24x7 phone support            │  │          Storage path state output          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 hosts, SAN/NAS/vSAN, vCenter appliance, management network, OOB access                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GSS         = Global Support Services; VMware support organisation                                   │
│  SR          = Service Request; support ticket raised via my.vmware.com                               │
│  S1          = Severity 1; production system down; 24x7 phone response                                │
│  S2          = Severity 2; major impact but workaround possible                                       │
│  Support bundle = vm-support archive; upload to SR for GSS analysis                                   │
│  PSOD dump   = memory dump from kernel crash; captured at panic time                                  │
│  HCL         = Hardware Compatibility List; confirm before escalating                                 │
│  vmkernel.log= primary ESXi system log; first item GSS will review                                    │
│  esxtop batch= esxtop -b output; shows performance at time of issue                                   │
│  my.vmware.com= VMware customer portal; SR creation and file upload                                   │
│  Workaround  = temporary fix; allows S2 to remain S2 not S1                                           │
│  Phone bridge= S1 SR triggers phone call from VMware engineer                                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
│  Escalation Triggers                                                                                  │
│  ├── Case not progressing → request internal escalation                                               │
│  ├── Business Critical → TAM direct contact                                                           │
│  └── P1 stalled → Escalation Management request                                                       │
│                                                                                                       │
│  Portal: https://support.broadcom.com                                                                 │
│  HCL check: https://compatibilityguide.broadcom.com                                                   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
