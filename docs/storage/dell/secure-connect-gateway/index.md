# Dell Secure Connect Gateway

<div class="kb-summary">
Dell Secure Connect Gateway navigation for Operations, CLI Reference, Scripts.
</div>

```text
┌────────────────────────────────── Dell Secure Connect Gateway (SCG) ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       SCG: Dell phone-home gateway; relays support telemetry from on-prem arrays to Dell      │   │
│   │            Outbound HTTPS port 443 to Dell support; no inbound connections required           │   │
│   │         Supports: PowerMax, Unity, PowerScale, PowerStore, VxBlock, iDRAC, VxRail, ECS        │   │
│   │       Deployment: VM or physical appliance; registered devices enroll via support portal      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Array sends telemetry → SCG collects → HTTPS to Dell → CloudIQ ingests → alert/analytics           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Connectivity        │  │       Managed Devices       │  │          Functions          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        HTTPS port 443       │  │           PowerMax          │  │       Telemetry relay       │   │
│   │       No inbound req.       │  │            Unity            │  │        Alert forward        │   │
│   │        Proxy support        │  │          PowerScale         │  │        Log collection       │   │
│   │           TLS 1.2+          │  │          PowerStore         │  │         CloudIQ feed        │   │
│   │       VM or appliance       │  │        iDRAC / VxRail       │  │       Support SR open       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Device enrolled → SCG polls or receives events → batches telemetry → forwards to Dell              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │      Aspect      │      Detail      │    Requirement    │   Alternative    │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Network      │  HTTPS 443 out   │   Firewall allow  │    HTTP proxy    │  DNS resolution  │   │
│   │    Deployment    │     VM (OVA)     │    4 vCPU, 8 GB   │  Physical appl.  │  vCenter needed  │   │
│   │   Registration   │   Support acct   │  Active contract  │        —         │  Per device SN   │   │
│   │     CloudIQ      │    Auto-feeds    │    SCG enrolled   │ Direct call home │  SaaS analytics  │   │
│                                                                                                       │
│    Physical: SCG VM on management network; DNS and port 443 to esrs.emc.com required                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Phone-home     = Automated outbound telemetry from array to Dell Support; no manual uploads        │
│    CloudIQ        = Dell SaaS analytics and health platform; receives data from SCG relay             │
│    ESRS           = EMC Secure Remote Support; earlier name for SCG protocol/service                  │
│    Alert forward  = SCG forwards array alerts to Dell Support; can auto-open Service Requests         │
│    Log collection = SCG pulls diagnostic logs from enrolled arrays for support case upload            │
│    Proxy support  = SCG can use HTTP/HTTPS proxy for outbound if direct internet not allowed          │
│    TLS 1.2+       = All traffic from SCG to Dell uses TLS; no unencrypted support traffic             │
│    OVA            = Open Virtualization Appliance; SCG deployment format for VMware                   │
│    Support SR     = Service Request; SCG can auto-create SRs when critical alerts fire                │
│    Enrolled device= Array registered with SCG; SCG relays its events and telemetry to Dell            │
│    Direct call home= Some arrays can phone home directly without SCG; SCG is preferred                │
│    Active contract= SCG and CloudIQ require valid Dell support contract for enrolled devices          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
</div>
## Overview

Dell Secure Connect Gateway (SCG) is the outbound-only connectivity appliance that tunnels telemetry, support data, and remote access sessions from Dell storage and server infrastructure to Dell's support back-end. It replaces the legacy ESRS (EMC Secure Remote Services) gateway. SCG is deployed as a virtual appliance (OVA/QCOW2) or as a software package on a Linux host. It brokers all support-related communication including CloudIQ telemetry, SupportAssist diagnostics, and remote access for Dell support engineers.

## Where It Fits

| Use Case |
|---|
| Required for CloudIQ telemetry collection from PowerMax, PowerStore, PowerScale, Unity, VPLEX, and other Dell platforms |
| Required for SupportAssist automated case creation and proactive alerting |
| Enables Dell remote support sessions without opening inbound firewall rules — all connections are outbound on port 443 |
| Central connectivity point for APEX STaaS and FOD metering telemetry |
| Replaces legacy ESRS in environments still running older EMC/Dell infrastructure |

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Confirm SCG appliance is running and reachable from the management net |  |  |
| Check SCG appliance GUI (HTTPS port 9443) for connectivity status |  |  |
| Review the SCG event log for any failed telemetry uploads or device re |  |  |
| Confirm outbound HTTPS (port 443) to Dell endpoints (`esrs.emc.com`, ` | `esrs.emc.com` |  |
| Check that all registered devices are actively sending telemetry |  | a device showing as offline in CloudIQ is usually an SCG connectivity issue |

## Health Commands

~~~bash
# Test outbound connectivity from the SCG appliance to Dell support endpoints
curl -sv --max-time 10 https://esrs.emc.com/esrs/v2/device/heartbeat 2>&1 | grep -E "(connected|SSL|error|timeout)"

curl -sv --max-time 10 https://cloudiq.dell.com 2>&1 | grep -E "(connected|SSL|error|timeout)"

# Check SCG service status on Linux-based SCG
systemctl status dell-scg 2>/dev/null || service dell-scg status 2>/dev/null

# Check SCG version via REST API (local)
curl -sk https://localhost:9443/scg/api/v1/system/version | python3 -m json.tool

# List registered devices via SCG REST API
curl -sk -u "admin:<password>" \
  https://localhost:9443/scg/api/v1/devices | python3 -m json.tool

# Check SCG log for recent errors
journalctl -u dell-scg --since "24 hours ago" | grep -i "error\|fail\|disconnect" | tail -30

# From a registered array — test SCG reachability (PowerMax example via Solutions Enabler)
symcfg -sid <SID> -esrs list
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| CloudIQ shows array as offline | SCG cannot reach Dell CloudIQ endpoint, or device telemetry stopped | Check SCG connectivity to `cloudiq.dell.com`; verify SCG service is running; check firewall rules for port 443 outbound |
| SCG device shows as disconnected in SCG GUI | Array lost connectivity to SCG (network change, IP change, certificate issue) | Re-register the device from the array management interface; verify SCG IP/hostname is reachable from the array |
| SupportAssist cases not being auto-created | SCG cannot reach Dell ESRS endpoint, or SupportAssist not configured on the array | Test connectivity to `esrs.emc.com`; check SupportAssist configuration on the platform; review SCG event log |
| SCG appliance certificate expired | SCG TLS certificate has lapsed | Renew the SCG appliance certificate via the SCG GUI → Settings → Security |
| SCG upgrade fails or hangs | Upgrade package corrupted or insufficient disk space on appliance | Check appliance disk space; download a fresh upgrade package; retry via SCG GUI → Software Update |
| Duplicate SCG registrations | Array registered to multiple SCG appliances | Remove stale registrations from both the SCG and the array side; confirm only one active SCG registration per device |

## Operational Tasks

| Task | Command |
|---|---|
| Deploy a new SCG virtual appliance: download OVA from Dell Support, deploy to vS |  |
| Register a new array to SCG: from the array management interface (e.g., Unispher |  |
| Upgrade SCG: download the update bundle from Dell Support and apply via SCG GUI |  |
| Add a second SCG for redundancy and configure failover registration on each arra |  |
| Review and export SCG event logs for audit or troubleshooting via SCG GUI → Logs |  |
| Decommission an SCG: remove all device registrations before shutting down to avo |  |

## Best Practices

| Recommendation | Detail |
|---|---|
| Deploy two SCG appliances in active/passive for redundancy | a single SCG failure silently stops all telemetry and support connectivity |
| Place SCG appliances in a dedicated management network segment with direct outbound HTTPS access | avoid proxies where possible as they often break SCG certificate pinning |
| Keep SCG software current | Dell releases SCG updates regularly to address TLS certificate chain changes at the Dell back-end |
| Register devices to both SCG appliances (primary and | Register devices to both SCG appliances (primary and secondary) so failover is automatic |
| Audit SCG device registrations quarterly to remove | Audit SCG device registrations quarterly to remove decommissioned systems that are still registered |
| Monitor the SCG appliance's own health (CPU, memory, disk) | the SCG is a VM and can be neglected during storage health reviews |
