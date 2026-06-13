---
tags:
  - dell
  - deployment
---
# Dell APEX AIOps — Initial Setup

```text
┌────────────────────────────────── Dell APEX AIOps — Setup Sequence ───────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Active Dell Technologies account with access to apex.dell.com; valid support contract per array      │
│  Arrays already connected to CloudIQ via Secure Connect Gateway (SCG) — AIOps uses same telemetry     │
│  If CloudIQ not configured: complete CloudIQ setup first (../cloudiq/deploy/)                         │
│  Outbound HTTPS 443/TCP from SCG to apex.dell.com and cloudiq.dell.com                                │
│  Minimum 90 days of telemetry data for AI recommendation accuracy                                     │
│                                                                                                       │
│                                        │  access and activate AIOps                                   │
│                                        ▼                                                              │
│  Step 2 · Access Dell APEX AIOps Portal                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Log in to apex.dell.com with Dell Technologies account credentials                                   │
│  Navigate to AIOps → Overview; portal is cloud-native SaaS — no on-premises install needed            │
│  Verify arrays appear under Managed Systems: they auto-populate from CloudIQ telemetry                │
│  Accept any pending entitlement or service activation prompts for new arrays                          │
│                                                                                                       │
│                                        │  configure dashboards and insights                           │
│                                        ▼                                                              │
│  Step 3 · Dashboards and Recommendations                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Review AI-generated recommendations: Performance, Capacity, and Efficiency tabs per array            │
│  Customise dashboards: add widgets for capacity trend, IOPS/throughput, and latency per system        │
│  Set capacity forecast horizon (default 90 days): Capacity → Forecast Settings                        │
│  Review rightsizing recommendations — AIOps identifies over-provisioned or under-used volumes         │
│                                                                                                       │
│                                        │  configure alerts and notifications                          │
│                                        ▼                                                              │
│  Step 4 · Alerts and Notification Configuration                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Settings → Notifications: add email recipients; choose severity thresholds (Info/Warning/Critical)   │
│  Enable capacity runout alerts: trigger when forecast indicates capacity exhaustion within N days     │
│  Enable performance anomaly alerts: AIOps ML baseline detects IOPS/latency deviations                 │
│  Review alert history to confirm notifications are delivering to correct recipients                   │
│                                                                                                       │
│                                        │  validate and baseline                                       │
│                                        ▼                                                              │
│  Step 5 · Validate and Baseline                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Confirm all registered arrays show active telemetry (last seen < 30 min)                             │
│  Review initial AI recommendations list; triage and schedule any critical actions in ITSM             │
│  Record: APEX account email, arrays under management, notification recipients configured              │
│  Schedule monthly review of AIOps recommendations with storage team                                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Step-by-step guide to setting up Dell APEX AIOps, connecting storage arrays, enabling AI-driven recommendations, and configuring dashboards and capacity alerts.
</div>

## Prerequisites

Before starting Dell APEX AIOps setup, confirm the following.

**Dell account and entitlement:**

- Active Dell Technologies account with access to `apex.dell.com`
- Storage arrays must have a valid support contract with SupportAssist entitlement
- AIOps is a cloud-native SaaS product — no on-premises software installation is required beyond the data collection pathway

**Data collection pathway:**

- Arrays must already be connected to Dell CloudIQ or have an active Secure Connect Gateway (SCG) forwarding telemetry — APEX AIOps consumes the same telemetry stream as CloudIQ
- If CloudIQ is not yet configured, complete the CloudIQ setup first (see: `../cloudiq/deploy/`)
- Outbound HTTPS 443/TCP from the SCG to `apex.dell.com` and `cloudiq.dell.com`

**Supported arrays:**

- PowerStore, PowerMax, PowerFlex, PowerScale (Isilon), Unity XT
- Minimum 90 days of telemetry data required for AI recommendation accuracy

**Access:**

- Admin or Storage Admin role in the Dell Technologies portal
- User accounts for team members who will consume the AIOps dashboards and recommendations

---

## Connect Storage Arrays

If arrays are already registered in CloudIQ, they are automatically available in APEX AIOps — no additional array registration is required.

**Verify arrays are visible:**

1. Sign in to `https://apex.dell.com` with your Dell Technologies account.
2. Navigate to **AIOps → Infrastructure**.
3. All arrays registered in CloudIQ appear here within a few minutes of first sign-in.

**If an array is missing:**

1. Open the SCG UI at `https://<scg-ip>:9443`.
2. Navigate to **Devices** and confirm the array shows **Connected**.
3. If missing from the SCG device list, add it: **Devices → Add Device**, select the array type, enter the management IP and credentials, and click **Save**.
4. Allow 15–30 minutes for the array to synchronise into APEX AIOps.

**Grant array access to users:**

1. In **APEX AIOps → Settings → Access Control**, assign Storage Admin or Viewer roles to team members for the relevant arrays or sites.

---

## Enable AI-Powered Recommendations

APEX AIOps AI recommendations are enabled by default once sufficient telemetry has been collected. The system requires approximately 90 days of performance and capacity history to generate reliable recommendations.

**Check recommendation readiness:**

1. Navigate to **AIOps → Recommendations**.
2. If fewer than 90 days of data are available, a banner indicates when recommendations will become active.
3. Once active, recommendations are categorised as: **Capacity**, **Performance**, **Configuration**, and **Workload Placement**.

**Review and action recommendations:**

1. Click any recommendation to see the full detail: affected resource, predicted impact, recommended action, and confidence score.
2. Recommendations are flagged as **High**, **Medium**, or **Low** priority.
3. Use the **Export** button to download the recommendations list as CSV for change management review.
4. Mark completed recommendations as **Resolved** after implementing the suggested change.

**Enable anomaly detection notifications:**

1. Navigate to **AIOps → Settings → Notifications**.
2. Enable **Anomaly Alerts** — this sends a notification when AIOps detects a deviation from predicted performance baseline.
3. Set the notification recipients (email addresses or webhook URL).

---

## Configure Dashboards

1. Navigate to **AIOps → Dashboards**.
2. The default view shows a cross-array summary with health scores, capacity utilisation, and active recommendations.
3. To create a custom dashboard, click **Add Dashboard**.
4. Add widgets by clicking **Add Widget** and selecting from:
   - **Capacity Trend** — projected capacity exhaustion date per array
   - **Performance Heatmap** — IOPS and latency across all arrays
   - **Health Score Trend** — health score over time per array
   - **Recommendation Summary** — count by category and priority
   - **Anomaly Events** — timeline of detected anomalies
5. Arrange widgets by dragging and resize by pulling the corner handle.
6. Click **Save Dashboard** and set visibility (personal or shared with all users).

**Recommended starter dashboards:**

- **Executive Summary:** health score trend, capacity forecast, open high-priority recommendations
- **Ops Daily:** active anomalies, recent performance deviations, pending recommendations
- **Capacity Planning:** capacity trend widgets for all arrays with 90-day forecast lines

---

## Set Capacity Alert Thresholds

1. Navigate to **AIOps → Settings → Alert Thresholds**.
2. The default capacity warning threshold is 80% and critical is 90% — adjust to match site standards.
3. To modify thresholds:
   - Click **Edit** next to the relevant threshold rule.
   - Set the **Warning** percentage (recommended: 75–80%).
   - Set the **Critical** percentage (recommended: 85–90%).
   - Set the **Forecast Alert** horizon — receive an alert N days before projected exhaustion (recommended: 30 days).
   - Click **Save**.
4. Thresholds can be set globally or overridden per array.

**Forecast-based alerts:**

1. Navigate to **AIOps → Settings → Forecast Alerts**.
2. Enable **Capacity Exhaustion Forecast** alerts.
3. Set the forecast horizon (e.g. alert when an array is projected to reach 90% capacity within 30 days).
4. Assign notification channels to the forecast alert rule.

---

## Validate Telemetry and Recommendations

Run through the following before declaring setup complete.

**Telemetry validation:**

- **AIOps → Infrastructure** — all expected arrays are listed with a health score
- Performance charts show data points from the last 24 hours
- Capacity widgets show values consistent with the array management UI (within 5%)
- No arrays show **Data Collection Error** status

**Recommendations validation:**

- Navigate to **AIOps → Recommendations** — at least capacity recommendations are visible if arrays have >90 days of data
- Open one recommendation and verify all detail fields (resource, impact, action, confidence) are populated
- Export the recommendation list and confirm the CSV download completes successfully

**Alerts validation:**

- Temporarily lower a capacity threshold below the current utilisation of a test array to trigger a test alert
- Confirm the notification email or webhook is received
- Restore the threshold to operational value

**Access validation:**

- Log in with a non-admin account and confirm the user sees only the arrays and dashboards they have been granted access to
