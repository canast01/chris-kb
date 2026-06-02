# Capacity on Demand (COD) — CLI Reference


<div class="kb-summary">
> Part of the [COD](../index.md) reference.
</div>

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
```text
┌─────────────────────────────────────── Dell COD CLI Reference ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          COD license CLI commands vary by product family: PowerStore, Unity, PowerMax         │   │
│   │             All products support GUI activation; CLI/REST provides automation path            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          PowerStore         │  │           Unity XT          │  │           PowerMax          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     pstore> license list    │  │     uemcli license -list    │  │         symlic list         │   │
│   │     pstore> license add     │  │    uemcli license -upload   │  │        symlic install       │   │
│   │     REST: POST /license     │  │     REST: POST /license     │  │      Solutions Enabler      │   │
│   │     REST: GET /capacity     │  │        GUI: Settings        │  │        Unisphere GUI        │   │
│   │     GUI: Settings > Lic     │  │         >  Licenses         │  │       Solutions Enblr       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               # PowerStore REST — list licenses                               │   │
│   │              curl -sk -u admin:$PASS https://<ps>/api/rest/license | jq .[].name              │   │
│   │                                                                                               │   │
│   │                                 # Unity uemcli — list licenses                                │   │
│   │                      uemcli -d <unity_ip> -u admin -p $PASS /license show                     │   │
│   │                                                                                               │   │
│   │                          # PowerMax Solutions Enabler — list licenses                         │   │
│   │                                     symlic -sid <SID> list                                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    pstore CLI     = PowerStore management CLI; access via SSH or embedded shell                       │
│    uemcli         = Unisphere for Unity CLI; installed on mgmt workstation or run from Unity          │
│    symlic         = Solutions Enabler command for PowerMax license management                         │
│    Solutions Enabler= Dell software toolkit for PowerMax management automation                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
