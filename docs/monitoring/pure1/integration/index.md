# Pure1 Integration

Pure1 integrates natively with all Pure FlashArray and FlashBlade systems via outbound telemetry over HTTPS. External platform integrations extend Pure1 data into broader operational tooling.

| Integration | Method | Purpose |
|---|---|---|
| Pure FlashArray / FlashBlade | Outbound HTTPS telemetry (native) | Fleet health, capacity, performance data |
| Aria Operations | Pure Storage management pack | vROps dashboards with Pure array data |
| Splunk | Pure1 REST API poller | Capacity and alert events in Splunk |
| ServiceNow | Pure1 alert webhooks | Auto-ticket creation on CRITICAL alerts |
| Slack | Webhook from Pure1 alert rules | Real-time alert notifications to ops channel |
