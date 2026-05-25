# Capacity on Demand (COD) — CLI Reference

> Part of the [COD](../index.md) reference.
---

Capacity on Demand is managed through **Solutions Enabler (SYMCLI)** and the **Unisphere REST API**. COD allows pre-installed but locked capacity on PowerMax/VMAX arrays to be unlocked via a license key without physical hardware installation. This page covers the commands used to inspect COD entitlement, activate capacity, and verify the result.

> **Prerequisite**: Solutions Enabler (symcli) installed and the target array registered in the local symapi database (`symcfg discover`).  
> **SID**: 12-digit SymmetrixID, e.g. `000297600123`. Find it with `symcfg list`.

---

## Quick-Reference Command Table

| Command | Purpose |
|---|---|
| `symcfg list` | List all locally-known arrays and their SIDs |
| `symcfg list -v -sid <sid>` | Array overview: model, microcode, cache, capacity |
| `symcfg show -v -sid <sid>` | Full array configuration dump |
| `symcfg -sid <sid> list -license` | All installed license entitlements |
| `symcfg -sid <sid> list -disk -thin` | Thin-provisioned disk (TDEV) pool capacity |
| `symcfg -sid <sid> show -pool` | Storage Resource Pool (SRP) capacity and COD tiers |
| `symconfigure -sid <sid> -f <cmd_file> commit` | Commit a SYMCLI configuration change (COD activation) |
| `GET /univmax/restapi/100/system/symmetrix/{sid}/system_capacity` | Unisphere REST: licensed and used capacity |

---

## SYMCLI — Discovering Arrays and Capacity

```bash
# --- Discover all arrays reachable from this host ---
symcfg discover

# List all known arrays (short form)
symcfg list

# List arrays with extended info (model, microcode, cache, licensed capacity)
symcfg list -v

# Show full array configuration for a specific SID
symcfg list -v -sid <sid>

# Full detailed configuration dump (includes all pools, directors, FE ports)
symcfg show -v -sid <sid>

# --- Storage Resource Pools (SRP) — where COD capacity surfaces ---
# Show all SRPs and their capacity by service level tier
symcfg -sid <sid> show -pool

# Show emulation/thin pool details (raw COD capacity lives here)
symcfg -sid <sid> show -pool -thin

# Show disk group capacity breakdown (identifies locked/unlocked disks)
symcfg -sid <sid> list -disk

# Show only thin/EFD disks with capacity summary
symcfg -sid <sid> list -disk -thin
```

**Key capacity fields from `symcfg list -v -sid <sid>`:**

| Field | Meaning |
|---|---|
| `Licensed Capacity (MB)` | Total capacity this array is licensed to use |
| `Configured Capacity (MB)` | Capacity actually formatted and available to pools |
| `Emulation Capacity (MB)` | Total physical raw capacity installed (including locked COD) |
| `COD Capacity (MB)` | Capacity that is installed but currently locked under COD |

---

## SYMCLI — Viewing Licensed Capacity

```bash
# List all license entitlements on the array
symcfg -sid <sid> list -license

# Output columns:
#   Feature Name     – e.g. "PowerMax 2500 COD Base", "Open Replicator"
#   Status           – Enabled / Disabled
#   Count            – Licensed count or capacity (TB/unit)
#   Expiry Date      – For time-limited licenses

# Show license details for a specific feature
symcfg -sid <sid> list -license -feature "PowerMax COD"

# Verify total licensed vs configured capacity (COD delta)
# Licensed capacity = already-active + COD available to activate
symcfg list -v -sid <sid> | grep -E "Licensed|Configured|COD|Emulation"

# --- Import a new license file (provided by Dell after COD purchase) ---
# License file is a .dat file from Dell License Management portal
symlmf -sid <sid> import -file /tmp/new_license.dat

# Verify the new license is reflected
symcfg -sid <sid> list -license
```

---

## SYMCLI — COD Activation

COD activation formats previously locked disk capacity into the array's storage pools. This is done via `symconfigure` with a configuration change file, then committed.

> **Important**: COD activation is a permanent, one-way action for the activated capacity. Always confirm the license file before committing. Changes to production arrays should follow your change management process.

```bash
# --- Step 1: Check current capacity before activation ---
symcfg list -v -sid <sid> | grep -E "Licensed|Configured|COD"

# --- Step 2: Preview (verify) the COD configuration change ---
# Create a configuration command file:
cat > /tmp/cod_activate.txt << 'EOF'
activate capacity, count=<n_disk_groups>, type=EFD;
EOF
# (Adjust type to FBA or EFD depending on disk type; count = disk groups to activate)

# Preview the change (does NOT commit)
symconfigure -sid <sid> -f /tmp/cod_activate.txt preview

# --- Step 3: Prepare and commit ---
symconfigure -sid <sid> -f /tmp/cod_activate.txt prepare

# Commit (this is the live activation — requires valid license)
symconfigure -sid <sid> -f /tmp/cod_activate.txt commit

# --- Step 4: Verify capacity increase ---
symcfg list -v -sid <sid> | grep -E "Licensed|Configured"
symcfg -sid <sid> show -pool

# --- Alternative: activate via Unisphere GUI ---
# Unisphere → <Array> → System → Capacity on Demand → Activate
# (SYMCLI commit is equivalent to this GUI workflow)

# --- Confirm new SRP capacity is visible ---
symcfg -sid <sid> show -pool -thin
```

---

## Unisphere REST API

The Unisphere REST API provides JSON-format capacity data including COD status.

```bash
UNISPHERE="https://<unisphere_host>:8443"
SID="<sid>"
USER="smc"
PASS="<password>"

# --- Get array system capacity (licensed, configured, COD available) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}/system_capacity" \
  | python3 -m json.tool

# Key response fields:
#   system_capacity.usable_total_tb         – Total usable (licensed) TB
#   system_capacity.usable_used_tb          – Currently used TB
#   system_capacity.subscribed_total_tb     – Thin-provisioned (subscribed) TB
#   system_capacity.subscribed_allocated_tb – Allocated to host devices TB

# --- Get array system info (includes license model and COD tier) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}" \
  | python3 -m json.tool

# --- Get SRP details (capacity broken down by service level) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/sloprovisioning/symmetrix/${SID}/srp" \
  | python3 -m json.tool

# Get a specific SRP
SRP_ID="SRP_1"
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/sloprovisioning/symmetrix/${SID}/srp/${SRP_ID}" \
  | python3 -m json.tool

# Key SRP fields:
#   srp_capacity.usable_total_tb
#   srp_capacity.usable_used_tb
#   srp_capacity.subscribed_total_tb
#   emulation                     – disk type (FBA, EFD)
#   diskGroupId[]                 – disk group list (add from COD activation shows here)

# --- List all disk groups (confirm COD groups are formatted) ---
curl -s -k -u "${USER}:${PASS}" \
  "${UNISPHERE}/univmax/restapi/100/system/symmetrix/${SID}/disk_group" \
  | python3 -m json.tool
```

---

## License Commands — Summary

```bash
# List all licenses with status
symcfg -sid <sid> list -license

# Show license for a specific feature
symcfg -sid <sid> list -license -feature "TimeFinder/SnapVX"

# Import a new license key file
symlmf -sid <sid> import -file /tmp/license_file.dat

# Export current license information to a file
symlmf -sid <sid> report -out /tmp/current_licenses.txt

# Check Solutions Enabler version (license compatibility)
symcfg -version

# Verify Solutions Enabler can communicate with the array
symcfg list -sid <sid> -v 2>&1 | head -5
```

**COD-relevant license feature names (examples — exact names vary by model):**

| Feature Name | Description |
|---|---|
| `PowerMax 2500 Base Capacity` | Baseline licensed capacity |
| `PowerMax 2500 COD Capacity` | Locked-until-activated COD capacity |
| `PowerMax All Flash Enclosure` | Additional enclosure COD |
| `VMAX3 COD Base` | Legacy VMAX3 COD entitlement |
| `Open Replicator` | Data migration feature license |
| `TimeFinder/SnapVX` | Snapshot license (separate from capacity) |
