# Host Build Standard


<div class="kb-summary">
> Part of the [Standards](../index.md) reference.
</div>

```
┌───────────────────────────────────── ESXi — Host Build Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Baseline configuration applied to every ESXi host via host profile — enforced in vCenter   │   │
│   │       NTP: 2+ NTP servers; drift < 250ms; required for vSAN, vMotion, and Kerberos auth       │   │
│   │         Syslog: forwarded to centralised SIEM; retention 90 days minimum at SIEM level        │   │
│   │     Lockdown: Normal mode on all production hosts; exception list for LCM service accounts    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Build standard items enforced via host profile; non-compliant hosts flagged in vCenter             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Time & DNS         │  │           Security          │  │          Networking         │   │
│   │        NTP servers x2       │  │       Lockdown: Normal      │  │        VDS uplinks x2       │   │
│   │       DNS primary/sec       │  │        SSH: disabled        │  │          MTU: 9000          │   │
│   │       DNS suffix list       │  │       ESXi Shell: off       │  │       LACP / failover       │   │
│   │        Syslog target        │  │       VIB: PartnerSupp      │  │         VMkernel IPs        │   │
│   │        Drift < 250ms        │  │         Host profile        │  │          iDRAC VLAN         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Host profile compliance checked after every LCM patch; non-compliant hosts remediated              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Item       │  Required value  │    Enforced by    │      Check       │   Remediation    │   │
│   │  Lockdown mode   │      Normal      │    Host profile   │    vCenter UI    │  Profile apply   │   │
│   │   SSH service    │   Stopped/off    │    Host profile   │   esxcli check   │  Profile apply   │   │
│   │    NTP drift     │     < 250ms      │     NTP daemon    │     ntpq -p      │ Sync NTP servers │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management NIC on VLAN 10; iDRAC on OOB VLAN; vSAN NIC on VLAN 30                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Host profile  = vCenter template enforcing consistent config across all cluster hosts              │
│    Lockdown mode = ESXi state blocking direct SSH; all management routed through vCenter              │
│    Exception list = Accounts permitted direct host access in lockdown (VxRail Mgr SVC acct)           │
│    VIB acceptance = Host policy for VIB package signing: VMwareCertified > PartnerSupported           │
│    NTP drift     = Clock offset tolerance; >250ms breaks vSAN resync and Kerberos tickets             │
│    ESXi Shell    = TSM service; disabled in production to reduce attack surface                       │
│    SSH service   = TSM-SSH service; disabled in production; enabled only for troubleshooting          │
│    Syslog target = Remote syslog server (SIEM) receiving all ESXi log events                          │
│    LACP          = Link Aggregation Control Protocol; bonds uplinks for bandwidth and failover        │
│    PartnerSupp   = VIB acceptance level allowing Dell, NetApp, and VMware-signed VIBs                 │
│    VMkernel IP   = Per-VLAN ESXi virtual NIC IP: management, vMotion, vSAN, iSCSI/NFS                 │
│    iDRAC VLAN    = OOB management VLAN for iDRAC; isolated from ESXi and VM traffic                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── ESXi — Host Build Standard ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Baseline configuration applied to every ESXi host via host profile — enforced in vCenter   │   │
│   │       NTP: 2+ NTP servers; drift < 250ms; required for vSAN, vMotion, and Kerberos auth       │   │
│   │         Syslog: forwarded to centralised SIEM; retention 90 days minimum at SIEM level        │   │
│   │     Lockdown: Normal mode on all production hosts; exception list for LCM service accounts    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Build standard items enforced via host profile; non-compliant hosts flagged in vCenter             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Time & DNS         │  │           Security          │  │          Networking         │   │
│   │        NTP servers x2       │  │       Lockdown: Normal      │  │        VDS uplinks x2       │   │
│   │       DNS primary/sec       │  │        SSH: disabled        │  │          MTU: 9000          │   │
│   │       DNS suffix list       │  │       ESXi Shell: off       │  │       LACP / failover       │   │
│   │        Syslog target        │  │       VIB: PartnerSupp      │  │         VMkernel IPs        │   │
│   │        Drift < 250ms        │  │         Host profile        │  │          iDRAC VLAN         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Host profile compliance checked after every LCM patch; non-compliant hosts remediated              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Item       │  Required value  │    Enforced by    │      Check       │   Remediation    │   │
│   │  Lockdown mode   │      Normal      │    Host profile   │    vCenter UI    │  Profile apply   │   │
│   │   SSH service    │   Stopped/off    │    Host profile   │   esxcli check   │  Profile apply   │   │
│   │    NTP drift     │     < 250ms      │     NTP daemon    │     ntpq -p      │ Sync NTP servers │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management NIC on VLAN 10; iDRAC on OOB VLAN; vSAN NIC on VLAN 30                        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Host profile  = vCenter template enforcing consistent config across all cluster hosts              │
│    Lockdown mode = ESXi state blocking direct SSH; all management routed through vCenter              │
│    Exception list = Accounts permitted direct host access in lockdown (VxRail Mgr SVC acct)           │
│    VIB acceptance = Host policy for VIB package signing: VMwareCertified > PartnerSupported           │
│    NTP drift     = Clock offset tolerance; >250ms breaks vSAN resync and Kerberos tickets             │
│    ESXi Shell    = TSM service; disabled in production to reduce attack surface                       │
│    SSH service   = TSM-SSH service; disabled in production; enabled only for troubleshooting          │
│    Syslog target = Remote syslog server (SIEM) receiving all ESXi log events                          │
│    LACP          = Link Aggregation Control Protocol; bonds uplinks for bandwidth and failover        │
│    PartnerSupp   = VIB acceptance level allowing Dell, NetApp, and VMware-signed VIBs                 │
│    VMkernel IP   = Per-VLAN ESXi virtual NIC IP: management, vMotion, vSAN, iSCSI/NFS                 │
│    iDRAC VLAN    = OOB management VLAN for iDRAC; isolated from ESXi and VM traffic                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---


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
