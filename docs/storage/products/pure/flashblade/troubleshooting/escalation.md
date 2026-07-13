---
tags:
  - pure
  - troubleshooting
search:
  boost: 1.5
description: "Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path."
---
# FlashBlade — Escalation


<div class="kb-summary">
Escalation reference covering Support Portal, Opening a Case, Information to Collect, SLA Tiers, Escalation Path.

*Applies to: FlashBlade Purity//FB 4.x*
</div>
![FlashBlade — Escalation](../../../../../assets/storage-pure-flashblade-troubleshooting-escalation.svg)




![FlashBlade — Escalation — Diagram](../../../../../assets/storage-pure-flashblade-troubleshooting-escalation-diagram.svg)

> Part of the [FlashBlade Troubleshooting](index.md) reference.

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
support_portal: "Support Portal" {shape: rectangle}
opening_a_case: "Opening a Case" {shape: rectangle}
information_to_collect: "Information to Collect" {shape: rectangle}
sla_tiers: "SLA Tiers" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> support_portal: investigate
symptom -> opening_a_case: investigate
symptom -> information_to_collect: investigate
symptom -> sla_tiers: investigate
symptom -> escalation_path: investigate
symptom -> verify_resolution: investigate
support_portal -> resolution
opening_a_case -> resolution
information_to_collect -> resolution
sla_tiers -> resolution
escalation_path -> resolution
verify_resolution -> resolution
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Support Portal

Pure Storage support is accessed through the support portal at **https://support.purestorage.com**.

All FlashBlade arrays with an active subscription have automatic case creation capability through Pure1. Pure1 (https://pure1.purestorage.com) provides a unified view of array health, active alerts, and open support cases. Phonehome telemetry is transmitted from the array to Pure1 over port 443; when a hardware fault is detected, Pure1 can automatically open a support case and dispatch a replacement part without customer action.

Ensure phonehome is active at all times. To verify from the array:

```bash
purearray phonehome --status
```


```text title="Expected output"
Phone Home Status
=================
Status: Enabled
Last successful phone home: 2024-01-15 14:32:18 UTC
Next scheduled phone home: 2024-01-22 14:32:18 UTC
Phone home server: https://phonehome.purestorage.com
Connection status: Connected
Last error: None
Proxy configured: No
Data collected: 7.2 MB
Last collection timestamp: 2024-01-15 14:30:45 UTC
```

!!! warning "Common errors"
    **`purearray: command not found`** — Ensure you are logged into the FlashBlade management interface or have the Pure Storage CLI tools installed and in your PATH.
    **`Error: Unable to connect to phone home server`** — Verify network connectivity and firewall rules allow outbound HTTPS to phonehome.purestorage.com on port 443.
    **`Error: Authentication failed`** — Confirm your array credentials are valid and you have administrative privileges to query phone home status.
## Opening a Case

When opening a case manually, provide the following information to reduce time to resolution:

| Field | How to Obtain |
|---|---|
| Array serial number | Purity GUI > System > Array, or `purearray list` |
| Purity//FB version | `purensshow --version` or `purearray list` |
| Symptom description | Clear description of what is wrong, when it started, and what changed |
| Impact severity | Number of affected users/services, whether production is down or degraded |
| Steps already taken | Commands run, reboots attempted, any changes made before opening the case |

Severity classification at case open determines SLA response time — set severity accurately to receive appropriate response.

## Information to Collect

Run the following commands and attach output to the support case before or immediately after opening:

```bash
# Array identity and software version
purearray list

# All active alerts with severity and description
purealert list

# Full diagnostic bundle (generates a support file on the array)
purediag

# Drive health and status
puredrive list

# Capacity usage across filesystems and object store
purearray list --space

# Recent system message log
puremsg list

# Filesystem list with provisioned and used capacity
purefb filesystem list

# Blade health and status
purefb blade list

# Replication link health and lag
purefb replication list
```


```text title="Expected output"
$ purearray list
Name                          Version           Model
flashblade-prod-01            4.2.1.0           FB15K
$ purealert list
Name                          Severity          Description
drive_failed                  critical          Drive 3.4 failed in enclosure 2
thermal_warning               warning           Chassis temperature elevated
$ purediag
Diagnostic bundle generation started
Bundle ID: diag-2024-01-15-fb15k-prod-01-a7f3e2c1
Estimated time: 5-10 minutes
$ puredrive list
Name                          Status            Capacity
3.1                           healthy           1.92TB
3.2                           healthy           1.92TB
3.3                           healthy           1.92TB
3.4                           failed            1.92TB
...
$ purearray list --space
Name                          Total             Used              Available
flashblade-prod-01            100TB             67.3TB            32.7TB
$ puremsg list
Timestamp                     Severity          Message
2024-01-15T14:32:18Z          info              Replication sync completed for fs-backup
2024-01-15T13:45:02Z          warning           High latency detected on link-02
2024-01-15T12:11:55Z          info              Snapshot created: fs-data.snap-20240115
$ purefb filesystem list
Name                          Provisioned       Used              Status
fs-data                       50TB              38.2TB            healthy
fs-backup                     30TB              22.1TB            healthy
fs-logs                       20TB              8.9TB             healthy
$ purefb blade list
Name                          Status            Model             IP
blade-1                       healthy           FB15K             10.20.1.11
blade-2                       healthy           FB15K             10.20.1.12
blade-3                       healthy           FB15K             10.20.1.13
$ purefb replication list
Name                          Status            Lag               Remote Array
fs-data-to-dr                 synced            0s                flashblade-dr-01
fs-backup-to-dr               synced            2.3s              flashblade-dr-01
```

!!! warning "Common errors"
    **`Error: Unable to connect to array management interface`** — Verify network connectivity to the array management IP and confirm firewall rules allow port 443.
    **`Error: Authentication failed - invalid credentials`** — Ensure your Pure Storage API token is valid and has not expired; regenerate credentials in the management console if needed.
    **`Error: Drive 3.4 failed in enclosure 2 - immediate replacement required`** — Schedule a maintenance window and replace the failed drive using the Pure Storage support portal to obtain the correct replacement part.
The `purediag` command generates a diagnostic bundle that Pure Support can pull directly via phonehome if the support tunnel is active. If phonehome is offline, download the diagnostic output and attach it to the case via the support portal.

## SLA Tiers

| Priority | Response Time | Description |
|---|---|---|
| P1 | 1 hour, 24x7 | Production system down or critically impaired; no workaround available |
| P2 | 4 hours, 24x7 | Production system degraded; workaround in place but operation is impacted |
| P3 | Next business day | Non-critical issue or question; system is operational with minor impact |
| P4 | Best effort | General enquiry, feature request, or documentation question |

P1 and P2 cases should be followed up with a phone call to the Pure Support line to ensure immediate engagement. Case severity can be escalated at any time if business impact increases.

## Escalation Path

If a case is not progressing at the expected pace or the business impact increases:

1. **Request a duty manager** — use the escalation option in the support portal or ask the support engineer to escalate to a duty manager for senior engagement
2. **Pure TAM contact** — for customers with a Technical Account Manager (TAM), contact the TAM directly for major incidents; the TAM can coordinate resources across support, engineering, and account management
3. **Account team escalation** — for contractual or SLA compliance issues, contact the Pure account executive or customer success manager
4. **Executive escalation** — in cases of sustained outage or repeated resolution failures, request executive-level escalation through your TAM or account executive

For P1 incidents involving data loss risk, request immediate engineering involvement alongside standard support engagement.

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [FlashBlade — Diagnostics](../diagnostics/)
- [FlashBlade — Common Issues](../common-issues/)
