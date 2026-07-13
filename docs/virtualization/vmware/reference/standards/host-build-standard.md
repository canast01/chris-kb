---
tags:
  - reference
description: "ESXi host build standard: NTP server list, syslog destination, vSwitch MTU, BIOS power profile, scratch datastore, and lockdown mode requirements."
---
# Host Build Standard

<div class="kb-summary">
ESXi host build standard: NTP server list, syslog destination, vSwitch MTU, BIOS power profile, scratch datastore, and lockdown mode requirements.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

management_vmkernel: "Management VMkernel" {shape: rectangle}
additional_vmkernels: "Additional VMkernels" {shape: rectangle}
security_profile: "Security Profile" {shape: rectangle}
host_profiles: "Host Profiles" {shape: rectangle}
firmware: "Firmware" {shape: rectangle}
postbuild_verification: "Post-Build Verification" {shape: rectangle}

management_vmkernel -> additional_vmkernels: hardens
additional_vmkernels -> security_profile: hardens
security_profile -> host_profiles: hardens
host_profiles -> firmware: hardens
firmware -> postbuild_verification: hardens
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
