---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# COD — Escalation

<div class="kb-summary">
Dell Cloud on Demand (COD) escalation: how to collect array license state, key file details, and Unisphere events, when to escalate to Dell Licensing versus Dell TAC, and the escalation path for key rejections, capacity activation failures, and contract disputes.

*Applies to: Dell Cloud on Demand (COD) / PowerMax Cloud on Demand*
</div>

```text
┌──────────────────────────────────────── Dell CoD — Escalation ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CoD escalation: when self-service resolution fails, escalate to Dell licensing or TAC     │   │
│   │   Dell Licensing team: for key purchase issues, duplicate keys, SN re-binding, wrong account  │   │
│   │   Dell TAC: for capacity not appearing after valid key applied; firmware or hardware faults   │   │
│   │   Account team: for budget or contract issues affecting CoD entitlements or key availability  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Licensing Team       │  │           Dell TAC          │  │         Account Team        │   │
│   │         Key re-issue        │  │        Firmware issue       │  │       Contract dispute      │   │
│   │        SN re-binding        │  │        Hardware fault       │  │      Entitlement query      │   │
│   │        Account merge        │  │      Capacity conflict      │  │        Pricing review       │   │
│   │        Duplicate key        │  │       License conflict      │  │       Key pre-purchase      │   │
│   │        Order history        │  │       Event log review      │  │       Exec escalation       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CoD          = Cloud on Demand; Dell capacity-on-demand licensing model for PowerMax               │
│    SN re-binding  = Dell process to re-issue a key for a replacement array serial number              │
│    Dell Licensing = Dell internal team managing CoD keys, SN binding, and licensing portal accounts   │
│    Dell TAC       = Technical Assistance Center; handles firmware, hardware, and capacity issues      │
│    SR             = Service Request; Dell support case opened at support.dell.com                     │
│    P2 SLA         = Dell TAC 4-hour response for degraded production; CoD failure may qualify         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** PowerMax admin credentials (Unisphere admin or Solutions Enabler); Dell support portal account linked to the array's ProSupport contract
- **Gather first:** array SID (System Identifier), current license state from `symlicense list`, the key file contents (VENDOR_SN field), and the exact error from the failed key import
- **Scope:** determine whether the issue is a key rejection (Licensing team), capacity not reflecting after successful import (TAC), or a billing concern (account team)
- **Do not retry import:** if the key import failed, do not retry until you understand the error — repeated failed imports may require a Dell backend reset to clear

---

## Severity Levels (by Issue Type)

| Issue Type | Escalate To | Response SLA | Contact |
|---|---|---|---|
| Key rejected / SN mismatch | Dell Licensing team | 1 business day | Via SR + account team routing |
| Capacity not appearing after valid key | Dell TAC | P2: 4h (if production capacity event) | support.dell.com |
| Contract / entitlement dispute | Dell Account team | 1 business day | Your Dell account executive |
| Exec escalation (capacity emergency) | Dell Account executive | Same day | Account team contact |

## Pre-Escalation Triage Checklist

| Check | Command | Expected |
|---|---|---|
| Array SID | `symcfg list` | SID visible (e.g., `000120000001`) |
| Current license state | `symlicense -sid <SID> list` | Active licenses listed |
| Key file SN matches array SN | `grep -i "VENDOR_SN" <key-file>.lic` and compare to `symcfg list` output | Exact match |
| Key file not expired | `grep -i "Expiry\|Expire" <key-file>.lic` | Future date or `PERMANENT` |
| Firmware version meets CoD requirement | `symcfg -sid <SID> list -v \| grep microcode` | Meets Dell CoD minimum version |
| Order number available | Dell support portal → My Orders | Order number for the CoD key purchase |
| Support contract covers this SID | support.dell.com → Check Entitlement by serial | Contract `Active` for this SID |

---

## Step-by-Step Data Collection

### 1. Get the array SID and firmware version

```bash
# List all arrays visible to Solutions Enabler
symcfg list

# Get detailed configuration for a specific array
symcfg -sid <SID> list -v

# Get firmware (microcode) version
symcfg -sid <SID> list -v | grep -i "microcode\|firmware"

# Check Unisphere version
# Unisphere web UI → Help → About
```

### 2. Collect current license state

```bash
# List all currently active licenses and their state
symlicense -sid <SID> list 2>&1 | tee /tmp/cod-licenses-$(date +%F).txt

# Show detailed license info for a specific feature
symlicense -sid <SID> list -feature CLOUD_ON_DEMAND 2>&1

# Preview a key file before importing (dry run — does not apply the key)
symlicense -sid <SID> preview -file /path/to/cod-key.lic 2>&1 | tee /tmp/cod-preview.txt
```

### 3. Capture the error from a failed key import

```bash
# Attempt to import the CoD key and capture all output
symlicense -sid <SID> install -file /path/to/cod-key.lic 2>&1 | tee /tmp/cod-install-$(date +%F).txt

# Common error codes:
# SYMAPI_C_INVALID_LICENSE: key file is invalid or SN mismatch
# SYMAPI_C_LICENSE_CONFLICT: conflicting license already active
# SYMAPI_C_NO_LICENSE:       feature requires additional license
```

### 4. Collect Unisphere events and SYMAPI logs

```bash
# SYMAPI error log (on the Solutions Enabler host)
cat /var/symapi/log/symapi_log.txt | grep -i "error\|license\|cod" | tail -100 \
  > /tmp/symapi-errors.txt

# PowerMax event log via CLI (requires Solutions Enabler)
symaudit -sid <SID> list -last 100 | grep -i "license\|key\|cod\|error" \
  > /tmp/powermax-events.txt

# Alternatively: Unisphere web UI → Events → filter by Source = Licensing, Severity = Error
# Export as CSV
```

### 5. Check key file fields (do not share key file publicly)

```bash
# Key files are plain text — check the VENDOR_SN field to confirm it matches your array SID
grep -E "VENDOR_SN|SN=|FEATURE|Expiry|PERMANENT" /path/to/cod-key.lic

# Key fields to note:
# VENDOR_SN: should match your array's full SID (e.g., 000120000001)
# FEATURE:   lists the CoD features/capacity blocks
# Expiry:    date or PERMANENT

# Do NOT share the raw key file in the SR — share only the VENDOR_SN and error output
# If the licensing team requests the key file, upload only through the secure case attachment
```

### 6. Write the timeline

```text
Array SID: 000120000001 (PowerMax 8000)
Unisphere version: 9.2.0.28
Firmware: 5978.221.221 (PowerMaxOS)

Issue first observed: 2026-06-15 11:00 UTC

Error from symlicense install:
  SYMAPI_C_INVALID_LICENSE: The license key serial number does not match this array.
  License VENDOR_SN: 000120000002
  Array SID:         000120000001

Key file details:
  FEATURE: COD_ENTERPRISE_CAPACITY_100TB
  Expiry: PERMANENT
  Order: ORD-2026-45678

Steps already taken:
  - Compared chassis label SN to key file VENDOR_SN — MISMATCH
  - Did NOT retry the failed import

Root cause suspected:
  - Key was generated for a different array (wrong SN binding by Dell Licensing)
  - OR: array was recently replaced and key was not rebound to new SID

Escalation needed:
  - Dell Licensing team to re-issue key with correct SID binding
```

---

## How to Open a Dell Support Case

1. Go to **support.dell.com** and sign in with your Dell account.

2. Click **Create Service Request** and select the affected PowerMax array by serial number.

3. Under **Category**, select **Licensing / Cloud on Demand** or **General Software — Licensing**.

4. Under **Priority**, select:
   - **P2**: CoD key rejection blocking an emergency capacity activation during a production event
   - **P3**: Key rejected for a planned capacity expansion (non-urgent)
   - **P4**: General CoD billing or entitlement question

5. In the **Summary**: `PowerMax SID 000120000001 — CoD key import failing: SYMAPI_C_INVALID_LICENSE (SN mismatch) — Licensing team re-issue needed`.

6. In the **Description**, paste:
   - Array SID and firmware version
   - SN shown in the license file vs array SID
   - Error message from `symlicense install`
   - Dell order number for the CoD key
   - Whether this is a replacement array (new SID requiring re-binding)

7. Upload attachments:
   - `cod-install-<date>.txt` — symlicense install output
   - `cod-licenses-<date>.txt` — current license state
   - `cod-preview.txt` — preview output (if run)
   - `powermax-events.txt` — Unisphere event log

8. In the **Notes** field, specify:
   - "Route to Dell Licensing team for key re-issue" (for SN mismatch or duplicate key)
   - "Route to TAC for capacity not reflecting after valid key import" (for activation failures)

---

## Escalation Path

```text
Step 1 — Open SR at support.dell.com with error output and SN comparison
         Specify in Notes which team should handle (Licensing vs TAC vs Account team)
         ↓
Step 2 — Key rejection / SN mismatch → Dell Licensing team
         → Licensing re-generates the key with the correct SID
         → SLA: 1 business day; for emergency capacity events, account team can expedite
         ↓
Step 3 — Capacity not reflecting after valid key import → Dell TAC
         → TAC checks firmware version requirements and backend license flag state
         → May require a firmware update or a backend unlock on the PowerMax array
         ↓
Step 4 — Contract or billing dispute → Dell Account team
         → Account team connects to Dell Contract Management
         → Purchase order number required to locate the key history
         ↓
Step 5 — If unresolved after 1 business day (P3) or 4 hours (P2):
         → Add case update: "Requesting escalation — capacity expansion blocked since [date]"
         → Contact your Dell account executive to expedite with the Licensing team
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Retry a failed key import before reading the error | Repeated `SYMAPI_C_INVALID_LICENSE` failures may require Dell backend intervention to clear the error counter | Understand the error first; open SR; retry only after Dell guidance |
| Edit the `.lic` key file to change the VENDOR_SN | License files are cryptographically signed — edited files are rejected; may invalidate the key entirely | Open SR with Dell Licensing to re-issue with the correct SID |
| Deactivate an existing CoD license to install a replacement | Removes active capacity from the array immediately; can cause I/O failures if storage is in use | Leave existing licenses active; open SR to resolve the conflict first |
| Purchase a second CoD key for the same feature without checking if one is already active | Creates a conflicting license situation requiring Dell backend resolution | Check `symlicense -sid <SID> list` first; contact account team if confused about entitlement |

---

## Information to Collect Before Opening a Case

Before opening a case, collect:

- Array SID: `symcfg list`
- Current license state: `symlicense -sid <SID> list`
- Full error from failed license install: `symlicense -sid <SID> install -file <file> 2>&1`
- License file VENDOR_SN field: `grep VENDOR_SN <key-file>.lic`
- Unisphere version and SCG connectivity status
- Dell order number for the CoD key purchase

---

## Useful Commands for Case Updates

```bash
# Quick state snapshot — paste into every case update
symcfg list
symlicense -sid <SID> list 2>&1

# Dry-run import (safe — does not apply the key)
symlicense -sid <SID> preview -file /path/to/cod-key.lic 2>&1

# Firmware version
symcfg -sid <SID> list -v | grep -i microcode

# NSR audit log for license events
symaudit -sid <SID> list -last 50 | grep -i "license\|cod\|key"

# SYMAPI log errors
tail -100 /var/symapi/log/symapi_log.txt | grep -i "error\|license"
```

---

## Verify resolution

- Confirm key imports successfully: `symlicense -sid <SID> install -file <new-key>.lic` returns no errors
- Verify the new CoD capacity feature is listed as active: `symlicense -sid <SID> list` shows the feature with status `Enabled`
- In Unisphere: navigate to Licensing → Current Licenses and confirm the new capacity block is visible and active
- Test the newly activated capacity: create a storage group or thin device using the new CoD capacity pool

---

## Support Portal

Open a Dell support case at [https://www.dell.com/support](https://www.dell.com/support). For COD license issues, select the affected PowerMax array as the primary product and specify COD / licensing as the impacted component.

---

## See also

- [COD — Diagnostics](diagnostics/)
- [COD — Common Issues](common-issues/)
