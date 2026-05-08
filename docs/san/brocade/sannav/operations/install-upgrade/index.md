# SANnav — Install & Upgrade

> Part of the [SANnav](../../) reference.

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

### 3. Initial Configuration

Access the SANnav UI at `https://<sannav-ip>`. Log in with `admin` and the new password.

**First-time setup checklist:**

1. **Administration > Server Settings > NTP** — confirm NTP is configured and synchronized
2. **Administration > Server Settings > SMTP** — configure email relay
3. **Administration > Server Settings > LDAP** — configure Active Directory integration
4. **Administration > License Management** — apply SANnav license key
5. **Discovery > Add Switch** — discover first managed switch
6. **Administration > Backup** — configure backup schedule and remote target

---

## In-Place Upgrade

### Pre-Upgrade Checklist

- [ ] Review SANnav Release Notes for the target version (check for upgrade path restrictions)
- [ ] Take a VM snapshot in vCenter before starting
- [ ] Run a manual backup: **Administration > Backup > Backup Now**
- [ ] Record current SANnav version: `sannav version`
- [ ] Confirm all switches are reachable and no critical alerts are active
- [ ] Notify stakeholders of the planned maintenance window

### Upgrade via GUI

1. Download the SANnav upgrade package (`.bin` file) from Broadcom Support.
2. Navigate to **Administration > System > Software Update**.
3. Click **Upload Upgrade File** and select the `.bin` file.
4. The UI validates the package and displays the target version.
5. Click **Start Upgrade**.
6. SANnav services restart during the upgrade. The UI is unavailable for 15–30 minutes.
7. After the upgrade completes, log back in and verify the version: **Administration > System > About**.

### Upgrade via CLI

```bash
# Transfer upgrade package to SANnav (from admin workstation)
scp sannav-upgrade-2.4.0.bin admin@sannav-dc1.corp.example.com:/tmp/

# SSH to appliance and start upgrade
ssh admin@sannav-dc1.corp.example.com

# Verify package checksum
sha256sum /tmp/sannav-upgrade-2.4.0.bin
# Compare with published checksum

# Apply upgrade
sannav upgrade /tmp/sannav-upgrade-2.4.0.bin

# Monitor upgrade log
tail -f /opt/sannav/logs/upgrade.log

# After completion, verify version
sannav version
# Expected: 2.4.0
```

### Post-Upgrade Validation

```bash
# Verify all services running
sannav status

# Check log for post-upgrade errors
grep -i "ERROR\|FATAL" /opt/sannav/logs/server.log | tail -30

# Verify switch connectivity restored
# In GUI: Dashboard > Fabric Summary — all switches should be Online within 5 min
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
