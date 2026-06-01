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
```
```
