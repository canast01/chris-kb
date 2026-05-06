# CloudIQ Troubleshooting

Common CloudIQ issues relate to SCG connectivity, stale telemetry, API authentication failures, and health score delays after firmware changes.

| Issue | Cause | Resolution |
|---|---|---|
| System missing from CloudIQ | SCG connectivity failure or system not onboarded | Check SCG status and logs; verify firewall allows outbound to `cloudiq.dell.com:443` |
| Stale telemetry / old last-seen | SCG service hung or network interruption | Restart SCG telemetry service from SCG admin UI; verify SCG-to-array connectivity |
| API authentication failure (401) | Client secret rotated but scripts not updated | Update `client_secret` in secrets manager; redeploy scripts |
| Health score calculation delay | Firmware upgrade recently completed | Allow 2-4 hours for health score recalculation post-upgrade |
| Alerts not routing to PagerDuty | Webhook URL changed or notification rule misconfigured | Re-validate notification rule in CloudIQ Settings > Notifications |
