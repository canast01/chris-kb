# Venafi Architecture

Venafi Trust Protection Platform (TPP) consists of a Policy Server that handles certificate lifecycle management and CA integration, paired with Venafi Edge Proxy for network-agnostic certificate discovery. An optional Venafi Log Server aggregates audit and event data for SIEM forwarding. Venafi as a Service (VaaS / TLS Protect Cloud) provides the equivalent SaaS-delivered capability without on-premises infrastructure.

Venafi integrates natively with Microsoft ADCS, DigiCert, Entrust, and major public CAs as issuance backends, enabling policy-driven certificate requests regardless of CA type.

| Component | Role | Deployment |
|---|---|---|
| Policy Server | Lifecycle management, CA integration, policy enforcement | On-prem VM (primary + secondary) |
| Edge Proxy | Certificate discovery across network segments | On-prem lightweight agent |
| Log Server | Audit event aggregation and SIEM forwarding | On-prem VM or syslog target |
| VaaS / TLS Protect Cloud | SaaS alternative to TPP | Hosted by Venafi |
