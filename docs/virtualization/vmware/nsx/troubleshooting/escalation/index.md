---
tags:
  - nsx
  - nsx-4
  - troubleshooting
  - vmware
---
# NSX — Escalation

```bash
# Trigger support bundle generation
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"log_age": 48}' \
  "https://<nsx-manager>/api/v1/node/support-bundles"

# Poll for completion
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/node/support-bundles/status"

# Download the bundle (URL returned in the status response)
curl -sk -u 'admin:password' \
  -O "https://<nsx-manager>/api/v1/node/support-bundles/download/<bundle-id>"
```
```text
┌────────────────────────────────────────── NSX — Escalation ───────────────────────────────────────────┐
│                                                                                                       │
│  VMware GSS escalation, pre-escalation steps, severity matrix, bundle contents.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │             Pre-Escalation Steps            │   │
│   │           Manager cluster DEGRADED           │  │            Collect support bundle           │   │
│   │           BGP flapping unexplained           │  │           Document symptoms + time          │   │
│   │            DFW drops all traffic             │  │          Run Traceflow and capture          │   │
│   │            Upgrade failed mid-way            │  │          Note NSX + vCenter version         │   │
│   │            Data plane unreachable            │  │            Verify HCL and interop           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Internal triage → bundle → VMware SR → severity assignment → bridge.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Severity Matrix                │  │           Support Bundle Contents           │   │
│   │         S1: network down / data loss         │  │          Manager + edge + host logs         │   │
│   │           S2: major feature broken           │  │            Traceflow trace export           │   │
│   │         S3: degraded with workaround         │  │             IPFIX collector data            │   │
│   │            S4: question or how-to            │  │            Config export (API/UI)           │   │
│   │           S1 = 24x7 phone support            │  │              Timeline of events             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NSX Manager VMs, Edge VMs, ESXi nodes, ToR switches, vCenter, OOB access                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GSS         = Global Support Services; VMware support organisation                                   │
│  SR          = Service Request; VMware ticket raised on my.vmware.com                                 │
│  S1          = Severity 1; network down/data loss; 24x7 phone response                                │
│  S2          = Severity 2; major degradation but workaround exists                                    │
│  Support bundle = NSX diagnostic archive; manager + edge + hosts                                      │
│  DEGRADED    = NSX Manager cluster health status indicating node failure                              │
│  BGP flapping= BGP session cycling between up and down rapidly                                        │
│  Traceflow   = NSX path debug tool; export results for GSS                                            │
│  Interop     = VMware Interoperability Matrix; check version support                                  │
│  HCL         = VMware Hardware Compatibility List; verify NICs/HBAs                                   │
│  Phone bridge= S1 SR triggers live call with VMware engineer                                          │
│  Config export = API GET of all NSX config; provides GSS full picture                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# NSX Manager CLI (SSH to any Manager node)
nsxcli
get cluster status
get managers
get services
get corfu-cluster status
get transport-node-status
get tunnel status
get version

# Edge node CLI (SSH to each Edge)
get version
get services
get interfaces
get bgp neighbor summary
get edge-cluster status

# From NSX Manager API
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/cluster/status"
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/transport-nodes/status"
curl -sk -u 'admin:password' "https://<nsx-manager>/api/v1/alarms?status=OPEN&severity=CRITICAL"
```

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

