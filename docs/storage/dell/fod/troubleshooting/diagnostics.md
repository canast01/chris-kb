---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# FOD — Diagnostics

<div class="kb-summary">
Dell Flex on Demand diagnostic commands: inspect the FoD license key file, verify array serial number binding, check currently active licenses with symlicense, and perform a dry-run install to diagnose key rejection errors before opening a Dell SR.

*Applies to: Dell Flex on Demand (FoD) / APEX Flex on Demand*
</div>
![FOD — Diagnostics](../../../../assets/storage-dell-fod-troubleshooting-diagnostics.svg)

```d2
direction: right

A: "FoD Key Issue" {shape: rectangle}
B: "symlicense -sid SID list\nCheck current licenses" {shape: rectangle}
C: "C" {shape: rectangle}
D: "grep VENDOR_SN fod-key.lic\nCompare to array SN" {shape: rectangle}
E: "symlicense preview\nDry-run install check" {shape: rectangle}
F: "Check ExpiryDate in .lic\nCheck term renewal status" {shape: rectangle}
G: "G" {shape: rectangle}
H: "Contact Dell Licensing\nRequest key re-issue" {shape: rectangle}
I: "Check firmware version\nsymcfg list -v grep firmware" {shape: rectangle}
J: "J" {shape: rectangle}
K: "Check firmware minimum\nand feature flag state" {shape: rectangle}
L: "Contact Dell TAC\nwith symlicense output" {shape: rectangle}
M: "Renew via Dell portal\nlicensing.dell.com" {shape: rectangle}
N: "Open Dell SR\nsupport.dell.com — route to Licensing" {shape: rectangle}

A -> B
C -> D
C -> E
C -> F
G -> H
G -> I
J -> K
J -> L
F -> M
I -> L
K -> L
H -> N
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_list_current_active_licenses: "Step 1 — List current active licenses" {shape: rectangle}
step_2_check_array_serial_number: "Step 2 — Check array serial number" {shape: rectangle}
step_3_inspect_the_fod_key_file: "Step 3 — Inspect the FoD key file" {shape: rectangle}
step_4_dryrun_the_key_install_previe: "Step 4 — Dry-run the key install (preview)" {shape: rectangle}
step_5_check_firmware_version_compat: "Step 5 — Check firmware version compatibility" {shape: rectangle}
step_6_collect_diagnostic_output_for: "Step 6 — Collect diagnostic output for Dell SR" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_list_current_active_licenses: investigate
symptom -> step_2_check_array_serial_number: investigate
symptom -> step_3_inspect_the_fod_key_file: investigate
symptom -> step_4_dryrun_the_key_install_previe: investigate
symptom -> step_5_check_firmware_version_compat: investigate
symptom -> step_6_collect_diagnostic_output_for: investigate
step_1_list_current_active_licenses -> resolution
step_2_check_array_serial_number -> resolution
step_3_inspect_the_fod_key_file -> resolution
step_4_dryrun_the_key_install_previe -> resolution
step_5_check_firmware_version_compat -> resolution
step_6_collect_diagnostic_output_for -> resolution
```

## Before you begin

- **Access:** Solutions Enabler access to the array (gatekeeper LUNs or Unisphere); the FoD `.lic` license file received from Dell
- **Gather first:** array serial number (from `symcfg list` or chassis label), the exact error from the failed key import, and the Dell order number for the key purchase
- **Do not retry a failed import:** if `symlicense install` failed with an error, do not retry until you understand the error — repeated failed imports on some platforms increment a counter that requires Dell Licensing team to reset
- **Protect the key file:** do not share the `.lic` file publicly; it contains a cryptographically signed key bound to your array SN — upload only through the Dell SR secure attachment portal

---

## Step 1 — List current active licenses

```bash
# List all FoD and regular licenses currently active on the array
symlicense -sid <SID> list
# Output columns: License Name, Feature, Status, Expiry
# Expected: FoD features show Status = Enabled
# Problem: the feature you expect to be active is Missing or Expired

# Show a specific feature's license detail
symlicense -sid <SID> show -feature <feature-name>
# Feature names: COD, CLOUD_TIERING, SRDF_ASYNC, SRDF_SYNC, etc.
# Shows: installed date, expiry, key ID, and SN the key is bound to
```

---

## Step 2 — Check array serial number

The FoD key is cryptographically bound to the array serial number. A serial number mismatch is the most common cause of key rejection.

```bash
# List all arrays visible from this SE host
symcfg list
# Output columns: SID, Name, Microcode, Model, Size (GB)
# Note the SID you are working with

# Get the full array configuration including serial number
symcfg -sid <SID> list -v
# Look for: "System Serial Number" or "Array Serial Number" in the output
# This value must match the VENDOR_SN field in the .lic key file

# Alternative: check array management web UI
# Unisphere → System → Properties → Serial Number

# Compare to chassis label
# The serial number is on a physical label on the front of the array
# Photo the label if there is any mismatch concern
```

---

## Step 3 — Inspect the FoD key file

The `.lic` file is plain text. You can open it with any text editor or inspect specific fields:

```bash
# Check which array serial number the key is bound to
grep -E "VENDOR_SN|SN|SERIAL" /path/to/fod-key.lic
# Expected: VENDOR_SN=<your-array-SN>
# If VENDOR_SN does not match your array SN → key was generated for a different array

# Check expiry date
grep -i "expiry\|expire\|date" /path/to/fod-key.lic
# Expected: either no expiry line (perpetual) or a future date
# If expired: contact Dell Account team to renew the term license

# Check which features this key enables
grep -i "feature\|increment" /path/to/fod-key.lic
# Lists the specific features (e.g., CLOUD_TIERING, SRDF_ASYNC, COD_CAPACITY)

# DO NOT edit any field in the .lic file
# License files have cryptographic signatures — edited files will always be rejected
```

---

## Step 4 — Dry-run the key install (preview)

Before installing a key on the array, use `preview` to validate it without activating:

```bash
# Test whether the key file is valid for this array (no changes made)
symlicense -sid <SID> preview -file /path/to/fod-key.lic
# Expected output (if key is valid):
#   Feature: CLOUD_TIERING
#   Status: Will be enabled
#   Expiry: <date or None>
#   Ready to install.

# If preview fails with "SYMAPI_C_INVALID_LICENSE":
#   The key SN does not match the array SN → request re-issue from Dell Licensing

# Capture preview output for the SR
symlicense -sid <SID> preview -file /path/to/fod-key.lic 2>&1 | tee /tmp/fod-preview-$(date +%F).txt
```

---

## Step 5 — Check firmware version compatibility

```bash
# Check firmware version on the array
symcfg -sid <SID> list -v | grep -i "microcode\|firmware\|enginuity"
# Compare to the minimum firmware version listed in the Dell FoD documentation for the feature

# For Unisphere-based arrays (Unity/PowerStore):
uemcli -d <mgmt-ip> /sys/general show
# Look for: "Model", "Software version", and "Serial Number"
```

---

## Step 6 — Collect diagnostic output for Dell SR

```bash
# All-in-one diagnostic snapshot
{
  echo "=== Array list ==="
  symcfg list
  echo "=== Current licenses ==="
  symlicense -sid <SID> list
  echo "=== Firmware version ==="
  symcfg -sid <SID> list -v | grep -i "microcode\|firmware"
  echo "=== Key preview (if key available) ==="
  symlicense -sid <SID> preview -file /path/to/fod-key.lic 2>&1
  echo "=== Key file SN field ==="
  grep -E "VENDOR_SN|SN" /path/to/fod-key.lic
} > /tmp/fod-diag-$(date +%F-%H%M).txt

# Attach to SR: fod-diag-<date>.txt
# Include: Dell order number, SN from chassis label, expected feature name
```

---

## See also

- [FOD — Common Issues](../common-issues/)
- [FOD — Escalation](../escalation/)
- [FOD — Health Checks](../../operations/health-checks/)

## Verify resolution

- `symlicense -sid <SID> list` shows the expected feature with `Status = Enabled`
- `symlicense -sid <SID> show -feature <feature-name>` shows the correct expiry date
- Test the activated feature (e.g., create a cloud tiering pool, initiate a replication job) to confirm it functions
- In Unisphere: navigate to Licensing → Current Licenses and confirm the feature is visible and active
