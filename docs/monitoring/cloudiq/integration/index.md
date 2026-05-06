# CloudIQ Integration

CloudIQ collects telemetry from all Dell platforms via Secure Connect Gateway. External integrations extend CloudIQ data and alerts into broader operational toolsets.

| Integration | Method | Purpose |
|---|---|---|
| PowerMax, PowerStore, Unity, PowerScale, Data Domain | SCG telemetry (native) | Health, capacity, and performance data |
| ServiceNow | Webhook from CloudIQ alert rules | Auto-ticket on CRITICAL alerts |
| Slack / Teams | Webhook notification | Real-time alert notifications to ops channel |
| Splunk / Grafana | CloudIQ REST API poller | Fleet health and capacity dashboards |
| Aria Operations | CloudIQ management pack | VMware + Dell storage correlation |
| Email | CloudIQ notification rules | WARNING alert distribution to team |
