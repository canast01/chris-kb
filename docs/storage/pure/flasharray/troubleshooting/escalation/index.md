# FlashArray — Escalation

```
Pure Support Escalation Path
  Array alert / incident
          │
          ▼
  Pure1 portal ──► Array auto-detected fault?
          │ Yes ──► Pure may auto-open case + dispatch parts
          │ No  ──► Open case manually at support.purestorage.com
          │
          ▼
  Case opened ──► Support engineer reviews Pure1 telemetry
          │
          ▼
  If needed: purediag --send ──► diagnostic bundle to case
          │
          ▼
  Pure TAC ──► Remote session / field engineer dispatch
```

## Support Portal

Pure Storage support is accessed at **[https://support.purestorage.com](https://support.purestorage.com)**.

**Account setup:**

1. Request an account from your Pure account team or register using your company email on the support portal
2. Your Pure1 login (pure1.purestorage.com) uses the same credentials — link your array serial number to your Pure1 organisation during onboarding
3. Once the array is registered in Pure1, it automatically appears in the support portal for case association
4. Add all relevant team members (storage admins, on-call engineers) as sub-users in the portal so they can open and track cases independently

**Pure1 integration with support:**

- Cases opened via the support portal are automatically linked to the array's Pure1 data
- Pure Support engineers can view array telemetry, alert history, and diagnostic data from Pure1 without requiring a manual diagnostic upload in most situations
- For critical issues, the support engineer may request you run `purediag --send` to push a fresh diagnostic bundle directly to the case

## Opening a Case

When opening a support case, provide the following minimum information to avoid delays:

| Field | Where to Find It |
|---|---|
| Array serial number | `purearray list` (Serial field) or Pure1 portal |
| Purity//FA version | `purearray list` (Version field) |
| Symptom description | Clear description of what is wrong, when it started, and what changed before the issue |
| Business impact | Number of affected hosts/VMs, applications impacted, whether the issue is production-down or degraded |
| Steps already taken | List of diagnostic commands run and their output |
| Severity / priority | P1 (production down) through P4 (general question) — see SLA tiers below |

Set the severity accurately — Pure uses it to determine response time and resource allocation.

## Information to Collect

Run and capture the following before or immediately after opening a case:

```bash
# Array identity and version
purearray list

# Controller health
purearray list --controller

# All active alerts
purealert list

# Drive health and status
puredrive list

# Array capacity and data reduction
purearray list --space

# Host connectivity
purehost list --connection

# Port status (FC/iSCSI/NVMe)
pureport list

# ActiveCluster pod status (if applicable)
purepod list

# Replication group status (if applicable)
purepgroup list

# Snapshot space usage (if capacity-related)
puresnap list --space

# Generate and save a full diagnostic bundle
purediag --output /tmp/diag_$(hostname)_$(date +%Y%m%d_%H%M).tgz
# Or send directly to Pure Support if phone-home is active:
purediag --send
```

## Before Calling Support

- [ ] Array name and serial number: `purearray list`
- [ ] Purity//FA version: `purearray list` (Version field)
- [ ] Active alerts: `purealert list` — copy full output
- [ ] Drive status: `puredrive list` — copy full output
- [ ] Controller status: `purearray list --controller`
- [ ] Relevant performance data: `purearray monitor` output at time of issue
- [ ] Host connection details if the issue is host-facing: `purehost list --connection`
- [ ] Pod status for ActiveCluster issues: `purepod list`
- [ ] Diagnostic bundle: `purediag --output /tmp/diag_<date>.tgz` and upload to case
- [ ] Symptom description: what changed before the issue, when it started, and business impact
- [ ] Change log: any changes made in the 24 hours before the issue (firmware, zoning, network, OS patching)

## SLA Tiers

| Severity | Response Time | Description |
|---|---|---|
| P1 — Critical | 1 hour | Production system down or data at risk; array inaccessible or both controllers failed |
| P2 — High | 4 hours | Production significantly degraded; single controller down, drive failures reducing redundancy, or replication broken |
| P3 — Medium | Next business day | Non-critical issue with a workaround in place; performance degradation, non-urgent configuration questions |
| P4 — Low | Best effort | General questions, documentation requests, feature enquiries, non-impacting observations |

> Response time = time from case submission to first contact from a Pure Support engineer. Resolution time varies by issue complexity.

Severity can be escalated after the case is opened if the situation worsens — call the Pure Support hotline directly for P1 issues rather than relying solely on the web portal.

**Support hotlines** (available 24x7 for P1/P2):

- Global: +1-650-729-4088
- EMEA: +44 808 189 0119
- Specific regional numbers available on the support portal after login

## Escalation Path

If a case is not progressing at the expected pace:

1. **Request escalation in the case** — add a case note requesting escalation to a senior support engineer or support manager
2. **Call the support hotline** — reference the existing case number; ask for a duty manager or case escalation
3. **Contact your Pure account team** — your Account Executive (AE) and Systems Engineer (SE) have escalation paths into the Pure Support management chain; use this channel for P1 situations where the standard process is not moving fast enough
4. **Pure executive escalation** — for sustained high-severity incidents, your AE can engage the VP of Customer Support directly
5. **Pure1 case tracking** — all cases are visible in Pure1 portal > Support > Cases; use this to track status and add attachments without calling
