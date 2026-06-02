# SANnav — Install & Upgrade


<div class="kb-summary">
> Part of the [SANnav](../../index.md) reference.
</div>

---

## Overview

SANnav Management Portal is deployed as a virtual appliance (OVA for VMware, QCOW2 for KVM). Upgrades are performed in-place via the SANnav GUI or appliance CLI. This page covers new installation and in-place upgrade procedures.

---

## Pre-Installation Requirements

| Requirement | Detail |
|---|---|
| Hypervisor | VMware ESXi 6.7 / 7.x / 8.x, or KVM (RHEL/CentOS 8+) |
| vCPU | 8 minimum (16 recommended for medium environments) |
| RAM | 32 GB minimum |
| Storage | 300 GB thin provisioned (500 GB for > 50 switches) |
| NIC | 1 vNIC on management VLAN with static IP |
| NTP | SANnav must be able to reach NTP servers |
| DNS | Forward and reverse DNS for SANnav management IP |
| Ports | TCP 443 from client browsers; UDP 162 from managed switches |

Obtain the OVA or ISO from Broadcom Support portal. Verify the SHA-256 checksum against the published hash before deployment.

---

## New Installation — VMware ESXi (OVA)

### 1. Deploy OVA

1. In vCenter or ESXi web client, select **Actions > Deploy OVF Template**.
2. Browse to the SANnav OVA file.
3. Accept the license agreement.
4. Configure the deployment settings:
   - VM name: `sannav-dc1-01`
   - Datastore: select a datastore with sufficient free space (recommend 500 GB reserve)
   - Network: select the management port group
5. On the **Customize template** screen, configure:
   - Management IP address
   - Subnet mask
   - Default gateway
   - DNS server 1 / DNS server 2
   - NTP server
   - Hostname (FQDN): `sannav-dc1.corp.example.com`
6. Review settings and click **Finish**.

### 2. Power On and Initial Setup

```bash
# After VM powers on, access the console or SSH with default credentials
# Default credentials: admin / passw0rd (change on first login)
ssh admin@<sannav-ip>

# Verify network connectivity
ping 8.8.8.8       # or internal NTP/DNS server
hostname           # should return configured FQDN

# Check service startup
sannav status
# Wait 5-10 minutes for all services to start on first boot

# Change default admin password
passwd admin
```
```text
┌──────────────────────────────── Brocade SANnav — Install and Upgrade ─────────────────────────────────┐
│                                                                                                       │
│  SANnav deployment: OVA to vSphere, initial config, discover switches, upgrade path.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Fresh Install Steps              │  │            Initial Configuration            │   │
│   │       1. Download SANnav OVA from BCM        │  │         1. Set hostname + IP address        │   │
│   │           2. Deploy OVA in vSphere           │  │           2. Configure NTP servers          │   │
│   │          3. Power on + accept EULA           │  │            3. Set admin password            │   │
│   │        4. Assign: 4 vCPU / 16 GB RAM         │  │          4. Configure TACACS+/LDAP          │   │
│   │       5. 2 TB datastore for perf data        │  │         5. Discover fabric switches         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  OVA deployment is quick; NTP and TACACS+ must be configured before adding switches.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Procedure               │  │           Post-Upgrade Validation           │   │
│   │          1. Backup SANnav DB to NFS          │  │        1. Verify all switches present       │   │
│   │          2. Download new SANnav OVA          │  │       2. Check MAPS alerts forwarding       │   │
│   │        3. Deploy standby; restore DB         │  │           3. Re-test TACACS+ auth           │   │
│   │        4. Validate standby operation         │  │        4. Verify NFS backup schedule        │   │
│   │           5. Swing DNS; decom old            │  │        5. Confirm zone management ok        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · shared 2 TB datastore · management network · NFS backup share                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA             = Open Virtual Appliance; SANnav package for vSphere deployment                      │
│  BCM             = Broadcom; download SANnav OVA from support.broadcom.com                            │
│  EULA            = End User License Agreement; accepted on first SANnav boot                          │
│  vCPU            = virtual CPU; SANnav minimum is 4 vCPU for production use                           │
│  Datastore       = vSphere storage; SANnav needs ~2 TB for 90-day perf history                        │
│  NFS backup      = SANnav DB backup destination; required before any upgrade                          │
│  Swing DNS       = update DNS A record to point to new SANnav VM after validation                     │
│  TACACS+         = centralised auth; must be re-tested after every SANnav upgrade                     │
│  MAPS forwarding = MAPS alerts from switches must flow to new SANnav after upgrade                    │
│  NTP servers     = time sync; must be configured before adding switches to SANnav                     │
│  Zone management = ability to push zone changes from SANnav GUI after upgrade                         │
│  Standby upgrade = deploy new SANnav version as standby; validate before DNS swing                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

Post-upgrade, delete the VM snapshot taken before the upgrade. Snapshots held for more than 48 hours degrade VM performance.

---

## Rollback

If the upgrade fails or a critical issue is found post-upgrade:

1. Power off the SANnav VM.
2. Revert to the pre-upgrade snapshot in vCenter.
3. Power on the VM and verify services start.
4. Contact Broadcom Support with the upgrade log: `/opt/sannav/logs/upgrade.log`.

There is no in-place rollback mechanism within SANnav itself — the VM snapshot is the only rollback path.

---

## Decommission

To decommission a SANnav instance:

1. Export all zone configurations: **Inventory > Fabrics > Export**.
2. Export the full backup: **Administration > Backup > Backup Now**.
3. Remove the SANnav instance from Global View (if registered): Global View **Administration > Portals > Remove**.
4. On each managed switch, remove the SANnav SNMP trap destination and HTTPS service account:

```bash
# On each switch (FOS CLI)
snmpconfig --set trapdest -index <n> -trapdest 0.0.0.0   # clear trap destination
userconfig --delete sannav_svc
```

5. Power off and delete the SANnav VM.
