# Pure1 Troubleshooting

Common Pure1 issues relate to array telemetry connectivity, stale data, and API rate limiting in automation scripts. Always verify the array's last-seen timestamp in Pure1 before investigating deeper connectivity issues.

| Issue | Cause | Resolution |
|---|---|---|
| Array not reporting in Pure1 | Outbound HTTPS blocked or array network misconfiguration | Check outbound HTTPS from array to `pure1.purestorage.com`; verify Purity network config (`purearray list --network`) |
| Stale data / old last-seen timestamp | Telemetry delay or array unreachable | Check array management network, confirm Purity is running, review array syslog for connectivity errors |
| API rate limiting (HTTP 429) | Too many API requests from scripts | Implement exponential backoff with jitter; reduce polling frequency |
| Missing arrays in dashboard | Array not registered or tag filter active | Verify array registration in Pure1; check active tag filters in dashboard view |
| Alert notifications not delivered | Notification rule misconfiguration | Review alert notification rules in Pure1 Settings > Notifications |
