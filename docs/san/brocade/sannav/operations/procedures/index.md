# SANnav — Procedures

> Part of the [SANnav](../../) reference.

---

## Overview

This page covers the most common operational procedures performed through the SANnav Management Portal: zoning changes, firmware upgrades, fabric discovery, MAPS policy management, and alert handling.

---

## 1. Adding a New Switch to SANnav

### Prerequisites

- Switch is powered on, has a management IP, and HTTPS is enabled
- FOS service account (`sannav_svc`) created on the switch
- SNMPv3 configured on the switch with SANnav as trap destination

### Procedure

1. Navigate to **Discovery > Switches > Add Switch**.
2. Enter the switch management IP address.
3. Enter HTTPS credentials:
   - Username: `sannav_svc`
   - Password: service account password
4. Enter SNMPv3 credentials:
   - Username: `sannav_mgmt`
   - Auth protocol: SHA, auth password
   - Priv protocol: AES-128, priv password
5. Click **Test Connection** — confirm both HTTPS and SNMP show **Success**.
6. Click **Add**.
7. Assign the switch to the correct resource group (fabric): **Discovery > Switches > Assign to Fabric**.
8. Navigate to **Dashboard** and confirm the switch appears Online within 2 minutes.

---

## 2. Zoning — Add a New Host Zone

This procedure creates a zone for a new host HBA being added to an existing storage group.

### Gather Information

- Host HBA WWN: obtain from host HBA driver (`systool -c fc_host -v` on Linux, Device Manager on Windows, or from SANnav **Inventory > Ports** after the HBA is connected)
- Storage port WWN: obtain from storage array admin or from SANnav **Inventory > Ports**
- Target zone name: `HOST-<hostname>-<array>-<port>` (e.g., `HOST-esxi01-purestor-A0`)
- Target zone set: the fabric's active zone set name

### Procedure in SANnav

1. Navigate to **Zoning > Zone Administration > [Fabric Name]**.
2. Click **New Zone Alias** to create aliases (if not already existing):
   - Alias name: `esxi01-hba0`; member: `<host HBA WWN>`
   - Alias name: `purestor-A0`; member: `<storage port WWN>`
3. Click **New Zone**:
   - Zone name: `HOST-esxi01-purestor-A0`
   - Members: add aliases `esxi01-hba0` and `purestor-A0`
   - Zone type: **Default** (single-initiator, single-target)
4. Click **Add Zone to Zone Set**:
   - Select the active zone set
   - Click **Add**
5. Click **Save Zone Configuration**.
6. Click **Activate Zone Set** — select the modified zone set and click **Activate**.
7. Confirm activation: the active zone set timestamp should update in the dashboard.

**Validate:** From the host, run a storage scan (`rescan-scsi-bus.sh` on Linux, `Rescan Disks` in Disk Management on Windows). The new storage LUN should appear.

---

## 3. Firmware Upgrade — Individual Switch

### Pre-Upgrade Steps

1. Upload the target FOS image to SANnav: **Image Management > Upload Image** — select the `.zip` firmware file.
2. Confirm the image uploads and appears in **Image Management > Images**.
3. Verify the switch is in a healthy state: no critical alerts, all ports Online.
4. Take a backup: **Administration > Backup > Backup Now**.

### Upgrade Procedure

1. Navigate to **Image Management > Firmware Upgrade**.
2. Select the target switch.
3. Select the target firmware version from the image repository.
4. Set activation mode:
   - **Auto** — immediately activate after download (non-disruptive on dual-CP directors)
   - **Manual** — download only; operator activates separately
5. Click **Upgrade**.
6. Monitor progress under **Image Management > Upgrade Status**.
   - Download: ~5 minutes
   - Activation: ~10 minutes (hitless on directors; brief outage on fixed-port switches)
7. After completion, navigate to **Inventory > Switches** and confirm the firmware version matches the target.

---

## 4. MAPS Policy Review and Application

SANnav displays MAPS policy violations but does not push MAPS policies. MAPS is configured per-switch via FOS CLI or the FOS Web Tools GUI. SANnav aggregates violations for reporting.

### Review MAPS Violations in SANnav

1. Navigate to **Monitor > MAPS Violations**.
2. Set time range to **Last 24 Hours**.
3. Filter by violation type:
   - `CRC_ERR` — physical layer errors (cable/SFP)
   - `CREDIT_ZERO` — buffer credit starvation
   - `LOS` — loss of signal
4. Click any violation to see the affected port, switch, and violation count.

### Apply MAPS Policy on Switch (FOS CLI)

```bash
# SSH to the affected switch
ssh admin@switch-ip

# List available MAPS policies
mapsPolicy --show

# Activate a MAPS policy
mapsPolicy --enable dflt_aggressive_policy

# Verify active policy
mapsPolicy --show
```

---

## 5. Alert Management

### Acknowledge and Close Alerts

1. Navigate to **Events > Active Alerts**.
2. Select one or more alerts (checkbox).
3. Click **Acknowledge** — assigns the alert to your user account and marks it as in-progress.
4. After the underlying issue is resolved, click **Clear** to remove it from the active list.

Cleared alerts remain in the historical event log and are searchable.

### Configure Alert Forwarding

1. Navigate to **Administration > Alert Policies > Forwarding Rules**.
2. Click **New Rule**:
   - Severity: Critical, Warning, or All
   - Action: Email, SNMP Trap, or Webhook
   - Recipients: enter email address(es) or SNMP receiver IP
3. Click **Save**.
4. Test the rule: **Administration > Alert Policies > Test Notification**.

---

## 6. Generating Reports

### On-Demand Reports

1. Navigate to **Reports > Generate Report**.
2. Select report type:
   - **Fabric Inventory** — all switches, ports, and devices
   - **Port Statistics** — traffic and error counters per port
   - **Event Summary** — alert history for a time period
   - **Firmware Summary** — firmware versions across all switches
3. Select scope: All Fabrics or specific fabric.
4. Select output format: PDF or CSV.
5. Click **Generate**.

### Scheduled Reports

1. Navigate to **Reports > Scheduled Reports > New**.
2. Configure schedule (daily, weekly, monthly), report type, recipients, and format.
3. Click **Save**. Reports are emailed at the scheduled time.

---

## 7. SAN Analytics — Investigating a Slow-Drain Device

SAN Analytics can identify hosts or storage ports that are absorbing buffer credits and causing congestion cascades.

1. Navigate to **SAN Analytics > Flow Analysis**.
2. Set the time range to the period of the reported I/O performance issue.
3. Sort by **Exchange Completion Time (ECT)** descending — high ECT on a target port suggests a slow-drain device.
4. Click the suspect port to view per-flow details.
5. Identify the initiator-target pairs with the highest ECT and lowest throughput.
6. Report findings to the storage or server team for investigation.

For quick credit starvation check on a switch port (FOS CLI):

```bash
portshow <port-index>
# Check: Credits: Tx buffer2buffer credit to zero count
# Non-zero value confirms credit starvation events
```
