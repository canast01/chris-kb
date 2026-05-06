# Aria Operations Integration

The vCenter adapter is the primary integration source, providing VM, host, cluster, and datastore metrics. NSX management packs extend visibility to network overlays, logical routers, and edge nodes. Storage adapters (Pure Storage, Dell EMC, NetApp) bring array-level performance and capacity data into Aria Operations for correlated infrastructure views. Outbound integrations include ServiceNow for alert-to-ticket creation and Slack/Teams webhook notifications for critical alerts. Aria Logs integration enables log correlation alongside performance anomalies.

| Integration | Type | Purpose |
|---|---|---|
| vCenter Adapter | Inbound | VM, host, cluster, datastore metrics |
| NSX Management Pack | Inbound | Network overlay visibility |
| Pure Storage MP | Inbound | Array performance and capacity |
| Dell EMC MP | Inbound | Dell storage metrics |
| NetApp MP | Inbound | NetApp storage metrics |
| ServiceNow | Outbound | Alert-to-incident ticketing |
| Slack / Teams Webhook | Outbound | Critical alert notifications |
| Aria Logs | Bidirectional | Log correlation with performance data |
