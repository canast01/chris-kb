# Pure1 — Support

```text
Support Flow — Pure1
┌─────────────────────────────┐
│  Pure1 (cloud monitoring)   │
│  detects issue / you observe│
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  MyPure tab / Support Cases │
│  → Create Case              │
│  → Select array & severity  │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Attach diagnostic bundle   │
│  puresupport create <name>  │
│  (logs, config, perf data)  │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│  Pure TAC assigned          │
│  ┌──────────────────────┐   │
│  │ Sev 1: 15 min (24x7) │   │
│  │ Sev 2:  1 hr  (24x7) │   │
│  │ Sev 3:  4 hr  (biz)  │   │
│  └──────────────────────┘   │
└─────────────────────────────┘
```

Pure Storage's support model is built around proactive monitoring via Pure1 and the Evergreen subscription. Most hardware replacements and upgrades are non-disruptive and covered under the subscription.

## Support Portal

**pure1.purestorage.com** — single portal for:
- Opening and tracking support cases
- Downloading Purity software bundles
- Accessing documentation and knowledge base
- Viewing support entitlement and contract details

## Opening a Support Case

### Via Pure1 UI

1. Log into pure1.purestorage.com
2. **Support → Cases → Create Case**
3. Select array, provide description and severity
4. Attach diagnostic bundle (see below)

### Via Phone

| Region | Number |
|---|---|
| US / Canada | +1 650-729-4088 |
| EMEA | +44 20 3318 9181 |
| APAC | +65 6521 2890 |

Use phone for Severity 1 (complete loss of access or data loss risk).

### Via CLI (auto-case creation)

Pure arrays with Phone Home enabled will auto-open cases for hardware failures:

```bash
# Verify Phone Home is enabled and connected
purearray list | grep phone_home
puresupport list

# Force a Phone Home transmission (sends diagnostics to Pure)
puresupport phonehome --transmit
```

## Diagnostic Bundle Collection

Pure support will typically request a diagnostic bundle for non-obvious issues.

```bash
ssh pureuser@<flasharray-ip>

# Generate and download a support bundle
puresupport create --name "issue-description-$(date +%F)"

# List generated bundles
puresupport list

# Download via SCP
scp pureuser@<flasharray-ip>:/support/<bundle-name>.tar.gz /local/path/
```

Bundles include: system logs, configuration, performance data, hardware status, and event history. No customer data is included.

## Severity Definitions

| Severity | Definition | Response target |
|---|---|---|
| **1 — Critical** | Complete loss of access to data or production outage | 15-minute initial response (24×7) |
| **2 — High** | Significant degradation — redundancy lost, DR at risk | 1-hour initial response (24×7) |
| **3 — Medium** | Non-critical degradation, workaround available | 4-hour business hours |
| **4 — Low** | Information request, general question | Next business day |

Always call for Severity 1 — do not rely on portal-only submission for critical issues.

## Evergreen Support — What's Covered

| Included | Not included |
|---|---|
| Drive replacement (any failure) | Data recovery from user-initiated deletions |
| Controller replacement | Professional services for design changes |
| Non-disruptive Purity upgrades | Connectivity troubleshooting beyond the array |
| Capacity expansion credits | Third-party integration issues |
| Pure1 cloud monitoring | |

## Proactive Support Features

### CloudIQ / AI-Assisted Analysis

Pure1 includes anomaly detection that flags performance deviations before they become incidents. Review the **Analytics → Wellness** view weekly.

### Upgrade Recommendations

Pure1 → **Arrays → select array → Settings → Software** shows available Purity upgrades with release notes. Pure Support proactively recommends upgrades when critical fixes apply.

### Log Forwarding to Pure

```bash
# Enable automatic log collection (supports proactive case creation)
puresupport set --log-forwarding enabled
puresupport list | grep log_forwarding
```

## Escalation Path

```text
L1 Support Case (portal / phone)
  ↓ if unresolved after agreed time
L2 Senior Support Engineer (request via case notes)
  ↓ if design or architecture question
Solutions Architect / Systems Engineer (account team)
  ↓ if software defect confirmed
Engineering (TAC escalation — handled by Pure internally)
```

## Common Support Scenarios

| Scenario | Action |
|---|---|
| Drive failed | Pure1 auto-detects; auto-ships replacement (Evergreen). Confirm shipping address in Pure1 → Profile |
| Controller fault | Open Sev 1 by phone immediately |
| Unexpected performance degradation | Collect `puresupport create` bundle; open Sev 2 case |
| Purity upgrade failed / stuck | Open Sev 1 — do not power off array |
| Need to extend snapshot retention | Adjust snapshot policy in array UI; no case needed |
| Volume restore from snapshot | Perform self-service via CLI/UI; open case only if data appears missing |
