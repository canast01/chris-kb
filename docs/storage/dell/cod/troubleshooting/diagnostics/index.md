---
tags:
  - dell
  - troubleshooting
---
# Dell COD Diagnostics

```bash
# Check current license status for the array
symlicense -sid <SID> list

# Show COD-specific feature license
symlicense -sid <SID> show -feature COD

# Show total installed capacity and active capacity breakdown
symcfg -sid <SID> list -capacity

# Show full array configuration including director and capacity details
symcfg -sid <SID> show -detail

# List all physical drives — identify COD reserved drives
sympd list -sid <SID>

# Show thin pool utilisation (confirms new capacity is usable)
symcfg -sid <SID> -pool -dp list

# Trigger device discovery after COD activation
symcfg -sid <SID> discover

# Review SYMCLI audit log for COD activations
symaudit -sid <SID> list -action "license"
```
```text
┌──────────────────────────────────────── Dell COD Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         COD diagnostics: key rejected, capacity not increasing, license portal errors         │   │
│   │               Key rejection: wrong serial number, duplicate use, corrupted file               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Common Problems                │  │               Diagnostic Steps              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │        Key rejected: serial mismatch         │  │        Verify array serial in portal        │   │
│   │             Key already applied              │  │          Check license list in GUI          │   │
│   │           Capacity not increasing            │  │         Verify pool expansion needed        │   │
│   │         Portal error generating key          │  │            Open Dell licensing SR           │   │
│   │              Key file corrupted              │  │           Re-download from portal           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │     Problem      │    Root cause    │        Fix        │      Verify      │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Key rejected   │   Wrong serial   │  Get correct key  │  Apply succeeds  │  Portal issues   │   │
│   │  No cap change   │Pool not expanded │    Expand pool    │  Capacity grows  │  HW not visible  │   │
│   │     Key used     │ Duplicate apply  │   Check lic list  │  Already active  │        —         │   │
│   │   File corrupt   │  Download issue  │    Re-download    │  Apply succeeds  │    Portal SR     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Serial mismatch = License key generated for different array serial; portal may have wrong SN       │
│    Pool expansion  = After COD unlock, pool must be expanded to include new drives in capacity        │
│    Duplicate apply = Applying same key twice; array reports already activated; not an error           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
symlicense -sid <SID> list
```
```bash
symlicense -sid <SID> install -file cod-license.xml
```
```bash
symlicense -sid <SID> install -file cod-license.xml 2>&1 | tee /tmp/cod-install-error.txt
```
```bash
# Step 1 — trigger device discovery
symcfg -sid <SID> discover

# Step 2 — wait 3–5 minutes, then check for new devices
sympd list -sid <SID> | grep -i "ready\|avail"

# Step 3 — confirm pool capacity has increased
symcfg -sid <SID> -pool -dp list

# Step 4 — if devices are visible but not in a pool, add them:
# (Use Unisphere GUI → Storage → Storage Pools → Add Drives)
# Or via SYMCLI:
symconfigure -sid <SID> -cmd "add drives to pool <pool-name> type thin;" commit
```
```bash
# Review SYMCLI operations log for the activation date
symaudit -sid <SID> list -start_time <date> -end_time <date>

# Review Unisphere audit log via REST API (if activation was done through Unisphere GUI)
curl -sk -u <user>:<pass> \
  "https://<unisphere-host>:8443/univmax/restapi/103/system/audit?startTime=<epoch>" \
  -H "Content-Type: application/json" | jq .
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
