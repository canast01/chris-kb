# CloudIQ Architecture

Dell CloudIQ is a cloud-native AIOps monitoring platform collecting telemetry from Dell storage, servers, and networking via Secure Connect Gateway (SCG). CloudIQ presents health scores, capacity forecasts, anomaly detection, and performance baselines through a web dashboard and REST API. The SCG virtual appliance is deployed on-premises and acts as the sole outbound telemetry relay — all communication to CloudIQ is outbound HTTPS with no inbound firewall rules required.

| Component | Role |
|---|---|
| CloudIQ Cloud | SaaS platform hosted by Dell |
| Secure Connect Gateway (SCG) | On-premises virtual appliance; collects and relays telemetry |
| CloudIQ Dashboard | Web UI for health scores, alerts, capacity, anomalies |
| CloudIQ REST API | Programmatic access to fleet data, alerts, capacity |
