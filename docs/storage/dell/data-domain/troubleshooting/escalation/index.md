# Data Domain — Escalation

## Support Portal

**URL:** [https://www.dell.com/support](https://www.dell.com/support)

Log in with your Dell account linked to your organisation's support entitlement. The support portal provides:

- Case creation and management
- Knowledge base and documentation
- Software downloads (DDOS upgrades, DD Boost plug-ins, MIB files)
- Hardware dispatch tracking
- ProSupport Plus health dashboard

## SLA Tiers

| Support Tier | P1 (Critical) | P2 (High) | P3 (Medium) | P4 (Low) |
|---|---|---|---|---|
| ProSupport Plus | 2-hour response | 4-hour response | Next business day | Next business day |
| ProSupport | 4-hour response | 4-hour response | Next business day | Next business day |
| Basic | Next business day | Next business day | Next business day | Next business day |

**P1 definition:** Production backup environment completely unavailable; data loss risk; no workaround available.

ProSupport Plus includes proactive monitoring via CloudIQ and automated case creation on hardware failure. This requires an active SCG registration for the DD.

## Information to Collect Before Opening a Case

Gather the following before calling or opening a case online — providing this upfront significantly reduces resolution time.

```bash
# 1. System identification
system show  # DDOS version, serial number, model

# 2. Current alert status
alerts show current

# 3. Filesystem status and space
filesys status
filesys show space
filesys show compression

# 4. Replication status (if replication is the issue)
replication show
replication status

# 5. Hardware status
disk show state

# 6. Network status
net show all
net show stats

# 7. Generate and send an AutoSupport bundle
autosupport send <case-number>

# 8. Manually generate a support bundle (if AutoSupport is not working)
support bundle generate
# Bundle is saved to /ddr/var/support/ — download via SCP or SFTP
```

## AutoSupport

AutoSupport is Dell's automated diagnostic collection mechanism. When correctly configured, it sends periodic telemetry and triggered diagnostics to Dell without manual intervention.

```bash
# Check AutoSupport status
autosupport status

# Enable AutoSupport (should be enabled at commissioning)
autosupport enable

# Send a manual AutoSupport bundle for an open case
autosupport send <case-number>

# Test AutoSupport connectivity
autosupport test
```

AutoSupport requires SCG (Secure Connect Gateway) registration or direct HTTPS outbound access to Dell's support endpoints.

## Remote Support

Dell ProSupport Plus includes remote support access via the SCG tunnel. Dell support engineers can connect to the DD CLI and System Manager remotely through the SCG — no inbound firewall rules are required.

To enable or verify remote support capability:

1. Confirm SCG registration: **System Manager → Administration → Autosupport → ESRS/SCG**
2. Dell opens a remote session through the SCG tunnel after the customer approves the session
3. All remote sessions are logged in the SCG audit log

## Escalation Path

1. **Online case** — open via [https://www.dell.com/support](https://www.dell.com/support) for non-urgent issues
2. **Phone (P1/P2)** — call Dell support directly; reference the case number opened online
3. **Account team escalation** — contact your Dell account manager or technical account manager for SLA breaches or cases not progressing
4. **Executive escalation** — if the account team escalation does not resolve within the agreed timeframe, request an executive sponsor escalation via the account manager

## Useful Support Links

| Resource | URL |
|---|---|
| Dell Support Portal | https://www.dell.com/support |
| Data Domain Documentation | https://www.dell.com/support → Product Documentation → PowerProtect DD |
| DDOS Downloads | Dell Support → Drivers & Downloads → PowerProtect DD series |
| Compatibility Matrix | Search "Data Domain Compatibility Guide" in Dell Support |
| NIST CMVP (FIPS) | https://csrc.nist.gov/projects/cryptographic-module-validation-program |

## Common Support Scenarios

| Scenario | What to Provide |
|---|---|
| Disk failure (hardware replacement) | Serial number, `disk show state` output, service tag from the DD chassis |
| DDOS upgrade issue | DDOS version before and after, error message from upgrade log, `system show` output |
| Replication failure | `replication show errors` output, both source and target DD serial numbers, DDOS versions on both |
| DD Boost connectivity failure | `ddboost show clients`, `ddboost status`, backup software version and OS version |
| Dedup ratio concern | `filesys show compression`, MTree names involved, data type description, time the ratio changed |
