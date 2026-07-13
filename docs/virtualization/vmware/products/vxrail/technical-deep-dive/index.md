---
tags:
  - vxrail
description: "VxRail Technical Deep Dive reference covering Overview, Platform Role, Core Components, Main Dependencies, Ports and Protocols and 7 more sections."
---
# VxRail Technical Deep Dive

<div class="kb-summary">
VxRail Technical Deep Dive reference covering Overview, Platform Role, Core Components, Main Dependencies, Ports and Protocols and 7 more sections.

*Applies to: VxRail 7.x · 8.x*
</div>

```d2
direction: down

platform_role: "Platform Role" {shape: rectangle}
core_components: "Core Components" {shape: rectangle}
main_dependencies: "Main Dependencies" {shape: rectangle}
ports_and_protocols: "Ports and Protocols" {shape: rectangle}
key_logs: "Key Logs" {shape: rectangle}
health_checks: "Health Checks" {shape: rectangle}

platform_role -> core_components: uses
core_components -> main_dependencies: uses
main_dependencies -> ports_and_protocols: uses
ports_and_protocols -> key_logs: uses
key_logs -> health_checks: uses
```

## Overview

VxRail is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

VxRail is a Dell integrated HCI platform built on VMware vSphere and vSAN with Dell lifecycle, hardware, and support integration.

## Core Components

- VxRail Manager
- vCenter
- ESXi hosts
- vSAN cluster
- Dell hardware
- iDRAC
- Lifecycle services
- Support bundle tooling
- Secure Remote Services / support connectivity

## Main Dependencies

- DNS resolution
- NTP/time sync
- Authentication source
- Management network
- Storage access
- Certificate trust
- Monitoring
- Backup/recovery process
- Vendor support access

## Ports and Protocols

| Use | Protocol | Port |
|-----|----------|------|
| VxRail Manager UI/API | HTTPS | 443 |
| vCenter | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| iDRAC | HTTPS | 443 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- VxRail Manager logs
- Lifecycle operation logs
- Support bundles
- ESXi logs
- vCenter logs
- iDRAC hardware logs

## Health Checks

- Confirm management access.
- Review current alarms.
- Review recent failed tasks.
- Validate DNS and NTP.
- Confirm certificate status.
- Check service health.
- Check capacity and performance.
- Confirm monitoring data is current.
- Review recent changes.

## Useful Commands

```bash
df -h
systemctl --failed
systemctl status vmware-marvin
journalctl -xe
curl -k https://localhost/rest/vxm/internal/system
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sda2       500G  320G  180G  64% /var
/dev/sda3       200G   85G  115G  42% /opt
tmpfs           32G  1.2G   31G   4% /dev/shm
● vmware-marvin.service - VMware Marvin Service
     Loaded: loaded (/etc/systemd/system/vmware-marvin.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2024-01-17 14:32:18 UTC; 2 days ago
   Main PID: 8742 (marvin)
      Tasks: 24 (limit: 4915)
     Memory: 512.3M
        CPU: 2h 14m 23s
{
  "id": "vxrail-cluster-prod-01",
  "version": "8.0.210.45821",
  "health_status": "Healthy",
  "cluster_mode": "Stretched",
  "nodes": 4,
  "last_update": "2024-01-19T08:42:15Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to curl to skip certificate verification, or import the VxRail certificate into your system trust store.
    **`Unit vmware-marvin.service not found.`** — Verify the VxRail management VM is running and the vmware-marvin service is installed with `systemctl list-units | grep marvin`.
    **`Failed to get D-Bus connection: Operation not permitted`** — Run the command with `sudo` or as root, as systemctl requires elevated privileges to query service status.
## Common Failure Points

- LCM pre-check failure
- Bundle compatibility issue
- Hardware warning
- vSAN health issue
- VxRail Manager service issue
- Support bundle failure
- iDRAC connectivity issue
- DNS/NTP issue

## Troubleshooting Workflow

1. Confirm the impact and scope.
2. Check recent changes.
3. Review alerts, tasks, and events.
4. Validate DNS, NTP, authentication, and certificates.
5. Check service status.
6. Check storage and network dependencies.
7. Review logs.
8. Capture screenshots, timestamps, errors, and task IDs.
9. Escalate with clean evidence if needed.

## Upgrade and Compatibility Notes

- Check product interoperability before upgrades.
- Confirm supported version path.
- Confirm backup or rollback method.
- Confirm maintenance window.
- Run pre-checks before change work.
- Validate health after the change.
- Document version before and after.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep versions aligned. | Keep versions aligned. |
| Keep certificates tracked. | Keep certificates tracked. |
| Keep DNS and NTP clean. | Keep DNS and NTP clean. |
| Keep alerting actionable. | Keep alerting actionable. |
| Document support ownership. | Document support ownership. |
| Avoid undocumented changes. | Avoid undocumented changes. |
