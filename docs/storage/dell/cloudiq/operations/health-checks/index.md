# CloudIQ — Health Checks


<div class="kb-summary">
Health Checks reference covering Daily Checks, Health Check Commands, Change Readiness, Incident Triage, Post-Change Validation.
</div>

```
┌───────────────────────────────────── Dell CloudIQ Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Verify CloudIQ and SCG health: telemetry currency, SCG connectivity, alert review       │   │
│   │        Check last telemetry timestamp per system; red/yellow health scores; open alerts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SCG Health                  │  │                CloudIQ Health               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │         SCG service status: running          │  │       All systems: last seen < 15 min       │   │
│   │           Outbound connectivity OK           │  │        Health scores: no red systems        │   │
│   │        All devices: poll state green         │  │            Active alerts reviewed           │   │
│   │             SCG version current              │  │          Capacity runway > 30 days          │   │
│   │             Certificate validity             │  │        No stale/disconnected systems        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Check       │      Where       │   Pass criteria   │   Fail action    │    Frequency     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    SCG status    │     SCG CLI      │     All green     │   Restart SCG    │      Daily       │   │
│   │  Telemetry age   │    CloudIQ UI    │      < 15 min     │  Test SCG conn   │      Daily       │   │
│   │  Health scores   │   CloudIQ dash   │     All green     │  Review alerts   │      Daily       │   │
│   │   Capacity IQ    │   CloudIQ dash   │      >30 days     │   Expand pools   │      Weekly      │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Telemetry age  = Time since last successful telemetry upload per system; > 15 min = gap            │
│    Stale system   = System in CloudIQ with no telemetry for > 1 hour; SCG poll failure                │
│    Capacity runway= Days until storage pool reaches fill threshold based on growth rate               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Dell CloudIQ Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Verify CloudIQ and SCG health: telemetry currency, SCG connectivity, alert review       │   │
│   │        Check last telemetry timestamp per system; red/yellow health scores; open alerts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SCG Health                  │  │                CloudIQ Health               │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │         SCG service status: running          │  │       All systems: last seen < 15 min       │   │
│   │           Outbound connectivity OK           │  │        Health scores: no red systems        │   │
│   │        All devices: poll state green         │  │            Active alerts reviewed           │   │
│   │             SCG version current              │  │          Capacity runway > 30 days          │   │
│   │             Certificate validity             │  │        No stale/disconnected systems        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │      Check       │      Where       │   Pass criteria   │   Fail action    │    Frequency     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    SCG status    │     SCG CLI      │     All green     │   Restart SCG    │      Daily       │   │
│   │  Telemetry age   │    CloudIQ UI    │      < 15 min     │  Test SCG conn   │      Daily       │   │
│   │  Health scores   │   CloudIQ dash   │     All green     │  Review alerts   │      Daily       │   │
│   │   Capacity IQ    │   CloudIQ dash   │      >30 days     │   Expand pools   │      Weekly      │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Telemetry age  = Time since last successful telemetry upload per system; > 15 min = gap            │
│    Stale system   = System in CloudIQ with no telemetry for > 1 hour; SCG poll failure                │
│    Capacity runway= Days until storage pool reaches fill threshold based on growth rate               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Change Readiness

- [ ] No active CRITICAL alerts on the affected system in CloudIQ
- [ ] SCG connectivity status for the affected system shows CONNECTED
- [ ] Record the current health score as a pre-change baseline
- [ ] Confirm CloudIQ alert notifications are routing to the correct email or webhook destination
- [ ] If using the REST API for automation during the window, confirm token is valid

| Item | Status | Notes |
|---|---|---|
| No active CRITICAL alerts on target system | | |
| SCG connectivity: CONNECTED | | |
| Pre-change health score recorded | | |
| Alert notification routing confirmed | | |
| API token valid (if applicable) | | |

## Incident Triage

**On alert or issue:**
1. Log in to CloudIQ and identify the affected system and alert severity
2. Check the anomaly timeline on the system's detail page (Timeline tab) to identify when the issue began
3. Pull performance metrics from the Analytics tab to correlate with the alert timestamp
4. Check SCG connectivity — if the system shows "Not Reporting", the issue may be SCG rather than the storage array itself
5. Cross-reference with any change activity at the time the anomaly was detected
6. Open a Dell support case directly from the CloudIQ alert if the issue cannot be resolved internally

| Symptom | Likely Cause | Action |
|---|---|---|
| Health score dropped suddenly | Performance anomaly or hardware fault | Check Timeline tab, pull performance metrics, review active alerts |
| System shows "Not Reporting" | SCG connectivity failure | SSH to SCG, run `dsagw status` and `dsagw list-devices`, check proxy/firewall |
| CRITICAL alert: drive fault | Disk hardware failure | Confirm in array management UI, open Dell support case from CloudIQ alert |
| CRITICAL alert: capacity threshold | Array nearing full | Review capacity forecast, initiate capacity expansion or data reduction review |
| Alert notifications not received | Notification routing misconfigured | Verify notification settings under Settings > Alerts in CloudIQ |
| API returning 401 Unauthorized | Expired or revoked API token | Regenerate token in CloudIQ Settings > API Tokens |

## Post-Change Validation

- [ ] System health score has returned to the pre-change baseline (or improved)
- [ ] No new CRITICAL or WARNING alerts have been generated on the affected system
- [ ] SCG connectivity for the system shows CONNECTED in CloudIQ
- [ ] Capacity forecast is unchanged or improved (no unexpected capacity consumption)
- [ ] Alert notification routing is confirmed active — no suppression window left open
