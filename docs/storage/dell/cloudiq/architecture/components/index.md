# CloudIQ — Components

| Component | Location | Role |
|---|---|---|
| CloudIQ SaaS Platform | Dell-hosted cloud | Analytics engine, health scoring, capacity forecasting, alert generation |
| CloudIQ Web Dashboard | Browser (SaaS) | Primary operator interface for health, alerts, capacity, and performance views |
| CloudIQ REST API | Dell-hosted (`cloudiq.dell.com`) | Programmatic access to all CloudIQ data; used for automation and integrations |
| Secure Connect Gateway (SCG) | On-premises (virtual appliance) | Collects telemetry from registered Dell devices and forwards it to CloudIQ over HTTPS |
| Registered storage systems | On-premises | PowerMax, PowerStore, PowerScale, Unity, VPLEX, Data Domain, etc.; each registered to SCG |
| API client credentials | CloudIQ → Settings | OAuth2 `client_id` / `client_secret` for REST API access |
