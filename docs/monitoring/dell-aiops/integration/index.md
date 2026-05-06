# Dell AIOps Integration

CloudIQ is the primary telemetry source for Dell AIOps — all Dell storage systems must be registered in CloudIQ and reporting via the Secure Connect Gateway. ServiceNow integration creates change requests or incidents for high-priority AI recommendations, enabling ITSM workflow management. Aria Operations integration via the Dell CloudIQ management pack correlates storage health and anomaly data with VMware workload performance for end-to-end visibility. Email and webhook notifications are configured in CloudIQ for immediate alerting on Critical recommendations.

| Integration | Direction | Purpose |
|---|---|---|
| CloudIQ / SCG | Inbound | Storage telemetry and health data |
| ServiceNow ITSM | Outbound | Recommendation-driven change/incident ticketing |
| Aria Operations | Bidirectional | Correlated VMware + Dell storage visibility |
| Email Notifications | Outbound | Critical/High recommendation alerts |
| Webhook (Teams/Slack) | Outbound | Real-time recommendation notifications |
