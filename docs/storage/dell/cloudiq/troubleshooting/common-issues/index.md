# CloudIQ — Common Issues

> Part of the [CloudIQ](../../) reference.

---

| Symptom | Likely Cause | Action |
|---|---|---|
| System not reporting in CloudIQ | SCG connectivity broken or SupportAssist disabled on the array | Check SCG status page; verify `dsagw` service is running; confirm the managed system has SupportAssist enabled |
| Health score dropped suddenly | Hardware fault detected or capacity threshold breached | Open the system in CloudIQ and review the alert detail panel; correlate with array-side alerts |
| API authentication failure | Client secret expired or incorrect client ID used | Rotate API credentials in CloudIQ Settings > API Access; update automation scripts with new secret |
| Capacity forecast showing incorrect trend | Insufficient historical data for regression model | CloudIQ requires approximately 30 days of data for a stable forecast; wait for data accumulation |
| Alert not routing to email or webhook | Notification rule misconfigured or recipient address invalid | Review notification rules under CloudIQ Settings > Notifications; send a test notification to confirm routing |
| System visible but no performance data | Array-side performance data collection not enabled | Verify on the array that performance statistics collection is active; check SCG telemetry logs |
| SCG shows systems as unregistered | SCG was re-deployed or system was manually deregistered | Re-register the system with SCG; confirm the SCG is associated with the correct CloudIQ account |
