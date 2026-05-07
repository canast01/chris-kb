# Dell Secure Connect Gateway


## Overview

Dell Secure Connect Gateway (SCG) is the outbound-only connectivity appliance that tunnels telemetry, support data, and remote access sessions from Dell storage and server infrastructure to Dell's support back-end. It replaces the legacy ESRS (EMC Secure Remote Services) gateway. SCG is deployed as a virtual appliance (OVA/QCOW2) or as a software package on a Linux host. It brokers all support-related communication including CloudIQ telemetry, SupportAssist diagnostics, and remote access for Dell support engineers.

## Where It Fits

- Required for CloudIQ telemetry collection from PowerMax, PowerStore, PowerScale, Unity, VPLEX, and other Dell platforms
- Required for SupportAssist automated case creation and proactive alerting
- Enables Dell remote support sessions without opening inbound firewall rules — all connections are outbound on port 443
- Central connectivity point for APEX STaaS and FOD metering telemetry
- Replaces legacy ESRS in environments still running older EMC/Dell infrastructure

## Daily Checks

- Confirm SCG appliance is running and reachable from the management network
- Check SCG appliance GUI (HTTPS port 9443) for connectivity status: all devices should show as Connected
- Review the SCG event log for any failed telemetry uploads or device registration errors
- Confirm outbound HTTPS (port 443) to Dell endpoints (`esrs.emc.com`, `cloudiq.dell.com`) is reachable
- Check that all registered devices are actively sending telemetry — a device showing as offline in CloudIQ is usually an SCG connectivity issue

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

- Deploy a new SCG virtual appliance: download OVA from Dell Support, deploy to vSphere, configure IP/DNS/gateway via the initial setup wizard
- Register a new array to SCG: from the array management interface (e.g., Unisphere, SYMCLI), specify the SCG hostname/IP and complete the registration
- Upgrade SCG: download the update bundle from Dell Support and apply via SCG GUI → Software Update
- Add a second SCG for redundancy and configure failover registration on each array (primary/secondary SCG)
- Review and export SCG event logs for audit or troubleshooting via SCG GUI → Logs → Export
- Decommission an SCG: remove all device registrations before shutting down to avoid orphaned records in Dell's support back-end

## Best Practices

- Deploy two SCG appliances in active/passive for redundancy — a single SCG failure silently stops all telemetry and support connectivity
- Place SCG appliances in a dedicated management network segment with direct outbound HTTPS access — avoid proxies where possible as they often break SCG certificate pinning
- Keep SCG software current — Dell releases SCG updates regularly to address TLS certificate chain changes at the Dell back-end
- Register devices to both SCG appliances (primary and secondary) so failover is automatic
- Audit SCG device registrations quarterly to remove decommissioned systems that are still registered
- Monitor the SCG appliance's own health (CPU, memory, disk) — the SCG is a VM and can be neglected during storage health reviews
