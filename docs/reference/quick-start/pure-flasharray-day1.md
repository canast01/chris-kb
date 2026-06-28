---
tags:
  - pure-storage
  - flasharray
  - quick-start
---
# Pure FlashArray Day 1 — New Environment Checklist

<div class="kb-summary">
What to do in your first hour with a new Pure Storage FlashArray. Covers array orientation, drive and hardware health, protection group schedules, SafeMode status, and the first operational tasks.
</div>

![Pure FlashArray Day 1](../../assets/reference-quick-start-pure-flasharray-day1.svg)

---

## 1. Orient

Start in the Purity GUI (https://`<array-ip>`) or via SSH as `pureuser`.

| What | Where |
|------|-------|
| Array name and model | **Dashboard** → top banner; or `purearray list` |
| Purity version | **Settings** → **System** → Software; or `purearray list --field version` |
| Capacity used/total | **Dashboard** → Capacity widget |
| Volume count | **Storage** → **Volumes** → count |
| Host connections | **Storage** → **Hosts** |
| Protection groups | **Protection** → **Protection Groups** |
| Pure1 connection | **Settings** → **System** → Pure1; should show **Connected** |

Key questions to answer:

- Is this array in an ActiveCluster pair or standalone?
- Is SafeMode enabled? (Requires Pure Support to disable — affects snapshot deletion)
- What replication target is configured for protection groups?
- Are hosts connected via FC, iSCSI, or NVMe-oF?

---

## 2. First Health Checks

### Array Health

```bash
purearray list
```

Key fields: `array_name`, `version`, `id`. No output means SSH connectivity issue.

```bash
purearray list --all
```

Shows all array properties including `SafeMode` status.

### Drive Health

```text
GUI: Storage → Drives
```

All drives should show **Healthy**. Drives in **Failed**, **Unhealthy**, or **Evacuating** state need immediate attention — the array may be in a degraded RAID state.

CLI:

```bash
puredrive list
```

Sort by `status`. Any status other than `healthy` is actionable.

### Hardware Component Status

```bash
purehw list
```

Check all hardware components — controllers, power supplies, fans, NVRAM. Any component showing `not_installed` that should be present, or `failed`, warrants a support case.

### Protection Group Schedules

```text
GUI: Protection → Protection Groups → select group → Schedule tab
```

Verify:

- Snapshot schedule is enabled and at the expected frequency
- Replication schedule is enabled (if replicating to a remote array or cloud)
- Retention policy matches your RPO/RTO requirements

CLI:

```bash
purepgroup list
purepgroup list --schedule
```

### SafeMode Status

SafeMode prevents snapshot deletion without Pure Support authorization — critical for ransomware protection.

```bash
purearray list --all | grep -i safemode
```

If SafeMode is enabled, confirm who holds the authorization contact — disabling requires a support call.

### Pure1 Connection

```text
GUI: Settings → System → Pure1
```

The array should show **Connected** with a recent heartbeat timestamp. A disconnected array loses call-home alerting and proactive support.

---

## 3. Common First Tasks

### List Volumes with Space Consumption

```bash
purevol list --space
```

Key columns: `name`, `size`, `total_used`, `data_reduction`, `unique`. Note any volume consuming significantly more unique space than expected (low data reduction ratio may indicate uncompressible data).

### Check Replication Lag

```bash
purepgroup list --replication
```

The `lag` field shows how far behind the remote copy is from the source. For synchronous replication (ActiveCluster), lag should be near-zero.

For asynchronous protection groups:

```bash
purepgroup list --transfer
```

Shows current in-flight replication transfer status and estimated completion.

### Verify Snapshot Schedule

```bash
purepgroup list --schedule
purepgroup listsnaps <pgroup-name>
```

Confirm:

1. Snapshots exist for the expected time periods (hourly, daily, weekly)
2. The oldest retained snapshot matches the retention policy
3. No `ERROR` status on any snapshot

### Add a Host and Connect a Volume

```bash
# Create host entry
purehost create <hostname> --iqnlist <iqn> # iSCSI
# or
purehost create <hostname> --wwnlist <wwn> # FC

# Connect volume to host
purehost connect <hostname> --vol <volume-name>

# Verify
purehost list --connection
```

---

## See Also

- [Pure FlashArray Cheat Sheet](../cheat-sheets/pure/) — top CLI commands
- [Pure FlashArray Architecture](../../storage/pure/flasharray/architecture/)
- [Pure FlashArray Health Check Runbook](../../storage/pure/flasharray/health-checks/)
- [ONTAP Day 1](ontap-day1/) — if NetApp is also in the environment
