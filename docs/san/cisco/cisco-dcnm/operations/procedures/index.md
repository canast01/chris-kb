# Cisco DCNM — Procedures


<div class="kb-summary">
> Part of the [Cisco DCNM](../../index.md) reference.
</div>

---

## Overview

This page covers the most common SAN operational procedures performed through DCNM: fabric discovery, VSAN management, device alias management, zoning, and firmware upgrades.

---

## 1. Discovering a New Fabric

1. Navigate to **SAN > Fabrics > Discover**.
2. Enter the seed switch IP address (use a director or well-connected switch).
3. Enter credentials:
   - SSH username: `dcnm_mgmt`
   - SSH password: service account password
   - SNMP v3 username: `dcnm_poll`
   - SNMP auth protocol: SHA / auth password
   - SNMP priv protocol: AES-128 / priv password
4. Select discovery scope: **Discover All Reachable Switches**.
5. Click **Discover**. DCNM will crawl the fabric from the seed switch.
6. After discovery, navigate to **SAN > Fabrics** to confirm the new fabric appears with all expected switches.
7. Rename the fabric: select the fabric > **Edit** > set name to `DC1-FABRIC-A`.

---

## 2. VSAN Configuration

### Create a New VSAN

1. Navigate to **SAN > VSANs > Create VSAN**.
2. Enter:
   - VSAN ID: 20
   - VSAN Name: `DC1-VSAN-20`
   - Fabric: DC1-FABRIC-A
3. Select member switches (all switches that will carry this VSAN).
4. Click **Create**.
5. DCNM pushes the VSAN configuration to all selected switches via SSH.
6. Verify: **SAN > VSANs** — VSAN 20 should show **Active** on all member switches.

### Assign a Port to a VSAN

1. Navigate to **SAN > Interfaces** and select the target switch.
2. Select the F_Port or E_Port.
3. Click **Edit** and set the VSAN.
4. Click **Apply**.

---

## 3. Device Alias Management

Device aliases should be managed through DCNM rather than per-switch to ensure CFS-based fabric-wide distribution.

### Create a Device Alias

1. Navigate to **SAN > Device Alias**.
2. Click **Create**.
3. Enter:
   - Alias name: `esxi01-hba0` (follow naming convention)
   - WWN: `50:00:10:00:00:ab:cd:ef`
4. Click **Create**.
5. Click **Commit** to trigger CFS distribution to all switches in the fabric.

### Import Device Aliases from CSV

Useful for bulk onboarding:

```bash
# CSV format: alias_name,wwn
# esxi01-hba0,500010000abcdef0
# esxi01-hba1,500010000abcdef1

# REST API bulk import
curl -sk -b dcnm-cookie.txt -X POST \
  "${DCNM}/rest/san/devicealias?fabricName=DC1-FABRIC-A" \
  -H "Content-Type: application/json" \
  -d '{
    "aliases": [
      {"aliasName": "esxi01-hba0", "pwwn": "50:00:10:00:00:ab:cd:ef"},
      {"aliasName": "purestor01-ct0-fc0", "pwwn": "52:4a:93:70:ab:cd:ef:00"}
    ]
  }' | python3 -m json.tool
```
┌───────────────────────────────── Cisco DCNM — Operations Procedures ──────────────────────────────────┐
│                                                                                                       │
│  DCNM day-2 procedures: zone changes, switch adds, firmware upgrades, health monitoring.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Zone Change Procedure             │  │             Switch Add / Remove             │   │
│   │         1. Create device alias (WWN)         │  │           1. Add switch IP in DCNM          │   │
│   │         2. Create zone with aliases          │  │          2. Set SNMPv3 credentials          │   │
│   │           3. Add zone to zone set            │  │           3. Discover: verify VSAN          │   │
│   │         4. Review zone diff in DCNM          │  │         4. Set SNMP threshold rules         │   │
│   │         5. Activate zone set in VSAN         │  │           5. Verify NX-OS version           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Zone set activation requires change ticket; always review diff before activation.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Firmware Management              │  │          Health Monitoring Routine          │   │
│   │         1. Upload NX-OS to DCNM repo         │  │           Daily: SNMP alert review          │   │
│   │          2. Validate compatibility           │  │          Weekly: port error report          │   │
│   │           3. ISSU upgrade via DCNM           │  │           Monthly: ISL utilisation          │   │
│   │          4. Verify via show version          │  │          Quarterly: zone set audit          │   │
│   │         5. Post-upgrade traffic test         │  │             Annual: DCNM upgrade            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DCNM VM · management network · Cisco MDS switch chassis · SFP transceivers                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Device alias    = named mapping for WWN in VSAN; used as zone member instead of raw WWN              │
│  Zone set        = collection of zones applied to a VSAN; only one active at a time                   │
│  Zone diff       = DCNM shows before/after comparison before activating zone set                      │
│  zoneset activate= NX-OS command; activates zone set in VSAN; DCNM triggers remotely                  │
│  ISSU            = In-Service Software Upgrade; NX-OS upgrade without traffic disruption              │
│  SNMPv3          = SNMP v3 credentials required for DCNM switch discovery and polling                 │
│  VSAN            = Virtual SAN; logical FC fabric partition; zones are per-VSAN                       │
│  Port error report= weekly DCNM report on CRC/discard/loss-of-sync per port                           │
│  Zone set audit  = quarterly review of all zones for stale aliases and orphaned WWNs                  │
│  Change ticket   = ITSM approval required before zone activation or firmware upgrade                  │
│  ISL utilisation = monthly DCNM ISL throughput trend; > 70% = add more ISLs                           │
│  NX-OS repo      = DCNM internal firmware storage; images staged before upgrade                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

---

## 5. MDS Firmware Upgrade via DCNM

### Upload Firmware Image

1. Navigate to **Administration > Image Management > Manage Images**.
2. Click **Upload Image** and select the MDS NX-OS `.bin` file.
3. Wait for upload and checksum verification.

### Upgrade a Switch

1. Navigate to **Administration > Image Management > Upgrade**.
2. Select the target switches.
3. Select the firmware image from the repository.
4. Set options:
   - Install mode: **Non-disruptive** (ISSU, for dual-supervisor switches)
   - **Disruptive** (for single-supervisor or fixed-port switches)
5. Click **Upgrade**.
6. Monitor progress under **Administration > Image Management > Upgrade Status**.

For dual-supervisor MDS directors (9706/9710/9718), ISSU upgrades the standby supervisor first, then failovers, then upgrades the previously active supervisor. I/O is not disrupted.

---

## 6. Event and Alert Management

### View and Acknowledge Alarms

1. Navigate to **Monitor > Alarms > Active Alarms**.
2. Select an alarm.
3. Click **Acknowledge** — assigns the alarm and marks it in-progress.
4. After resolution, click **Clear**.

### Configure Alarm Notification Rules

1. Navigate to **Administration > Event Settings > Notification Rules**.
2. Click **New Rule**:
   - Name: `Critical-Email-SAN-Team`
   - Severity: Critical
   - Action: Email
   - To: `san-team@corp.example.com`
3. Click **Save**.

### Suppress Alarms for Maintenance

During planned maintenance, suppress alarms to avoid noise:

1. Navigate to **Monitor > Alarms > Suppression Rules**.
2. Click **New Rule**:
   - Name: `MAINT-esxi01-20260506`
   - Scope: specific switch or port
   - Duration: maintenance window start and end time
3. Click **Save**. Alarms matching the rule will be suppressed during the window.

---

## 7. ISL Monitoring and Capacity Planning

1. Navigate to **SAN > ISLs** and select the fabric.
2. Review the **Utilization** column for all ISLs.
3. For detailed trending, navigate to **Monitor > Performance > ISLs**.
4. Set the time range to **Last 7 Days** and review peak utilization.
5. If any ISL consistently exceeds 70% peak: raise a capacity concern and evaluate adding inter-switch links or upgrading port speed.

Export ISL performance data:
```bash
curl -sk -b dcnm-cookie.txt \
  "${DCNM}/rest/monitor/performance/isl?fabricName=DC1-FABRIC-A&interval=1d&duration=7d" \
  -H "Accept: text/csv" -o isl-perf-$(date +%Y%m%d).csv
```
