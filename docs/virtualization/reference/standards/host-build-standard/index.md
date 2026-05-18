# Host Build Standard

> Part of the [Standards](../) reference.

---

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  ESXi Host Build Checklist — Order                       │
├─────────┬────────────────────────────────────────────────────────────────┤
│  Phase  │  Steps                                                         │
├─────────┼────────────────────────────────────────────────────────────────┤
│ Install │ Vendor ISO (Dell VIB bundle) │ VMFS 6 boot │ scratch on local  │
│ Network │ vmk0=mgmt(1500) │ vmk1=vMotion(9000) │ vmk2=vSAN(9000)       │
│         │ vmk3=NSX-TEP(9000) │ All uplinks to vDS                        │
│ System  │ Hostname in DNS (fwd+rev) │ NTP (2 servers) │ Syslog → Aria   │
│ Security│ Lockdown Mode ON │ SSH off │ Root → CyberArk │ Host Profile   │
│ Firmware│ BIOS/iDRAC/HBA/NIC at approved baseline                       │
│ vCenter │ Add to vCenter → correct cluster │ Host Profile applied       │
│ Monitor │ Add to monitoring platform │ Inventory updated                 │
└─────────┴────────────────────────────────────────────────────────────────┘
```
## Overview

All ESXi hosts must be built to this standard before joining a cluster. Deviations require documented approval. This standard applies to bare-metal ESXi deployments and VxRail nodes (where applicable — VxRail nodes are managed via VxRail LCM and may have additional vendor-specific requirements).

## ESXi Installation

| Setting | Required Value |
|---|---|
| ESXi Version | Current approved baseline (see Version Inventory) |
| Installation Source | Approved vendor-customised ISO (Dell VIB bundle for Dell hardware) |
| Boot Device | Internal SD card, USB, or M.2 (avoid shared SAN LUNs for boot) |
| Scratch Partition | Must be on a persistent local device — not the boot device |

## Hostname and DNS

| Setting | Requirement |
|---|---|
| Hostname | Follow naming standard (`esx-<site>-<##>`) |
| DNS Servers | Two DNS servers configured (primary and secondary) |
| DNS Search Domain | Corporate domain (e.g. `example.com`) |
| Forward and reverse DNS | Host must resolve by name and IP |

## NTP

| Setting | Requirement |
|---|---|
| NTP Service | Enabled and set to start with host |
| NTP Servers | Two NTP servers configured (internal stratum 2 preferred) |
| Time Sync Policy | Do not use VMware Tools time sync as the sole time source |

Verify NTP is synchronised after build: `esxcli system time get` and check clock skew.

## Syslog

| Setting | Requirement |
|---|---|
| Remote Syslog | Configured to forward to central syslog / Aria Logs |
| Local Log Location | `/scratch/log` on persistent storage |
| Log Rotation | Default (sufficient for most environments) |

Configure via:

```bash
esxcli system syslog config set --loghost=udp://aria-logs-01.example.com:514
esxcli system syslog reload
```

## Management VMkernel

| Setting | Requirement |
|---|---|
| vmk0 IP | Static — follow host IP addressing plan |
| vmk0 VLAN | Management VLAN (e.g. 1004) |
| MTU | 1500 |
| Default Gateway | Management gateway |

## Additional VMkernels

| VMkernel | Service | MTU | VLAN |
|---|---|---|---|
| vmk1 | vMotion | 9000 | vMotion VLAN |
| vmk2 | vSAN | 9000 | vSAN VLAN |
| vmk3 | NSX Overlay (TEP) | 9000 | Overlay VLAN |

Jumbo frames (MTU 9000) must be configured end-to-end on all switches handling vMotion, vSAN, and overlay traffic.

## Security Profile

| Setting | Requirement |
|---|---|
| SSH | Disabled at rest. Enable only for break-glass operations, then disable immediately. |
| ESXi Shell | Disabled. Same policy as SSH. |
| Lockdown Mode | Normal Lockdown Mode enabled after host joins vCenter |
| Firewall | Default — open only required ports |
| Root Password | Set to approved complexity standard, stored in CyberArk |

Do not enable SSH or ESXi Shell as a standing configuration in production.

## Host Profiles

After build, apply the approved Host Profile from vCenter to enforce configuration consistency and detect drift.

## Firmware

| Component | Requirement |
|---|---|
| BIOS / UEFI | Approved firmware baseline for the hardware model |
| iDRAC / iLO | Approved firmware baseline |
| HBA Firmware | Approved firmware baseline |
| NIC Firmware | Approved firmware baseline |

For VxRail, firmware is managed exclusively through VxRail LCM bundles. Do not update firmware manually on VxRail nodes.

## Post-Build Verification

- [ ] ESXi version matches approved baseline
- [ ] Hostname resolves in DNS (forward and reverse)
- [ ] NTP synchronised
- [ ] Syslog forwarding active (check Aria Logs)
- [ ] All VMkernels configured with correct IPs, MTU, and services
- [ ] Lockdown Mode enabled
- [ ] SSH and Shell disabled
- [ ] Root password stored in CyberArk
- [ ] Firmware at approved baseline
- [ ] Host added to vCenter and correct cluster
- [ ] Host Profile applied and compliant
- [ ] Host added to monitoring
- [ ] Host Inventory updated
