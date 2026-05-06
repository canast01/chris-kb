# Certificates Integration

Venafi TPP or TLS Protect Cloud provides centralised lifecycle automation across all certificate types, acting as the policy and workflow layer above individual CAs. Microsoft ADCS serves as the enterprise CA backend for internal certificates. HashiCorp Vault PKI secrets engine issues short-lived certificates for service-to-service authentication in zero-trust architectures.

Kubernetes cert-manager automates certificate issuance and renewal for in-cluster workloads, integrating with ADCS, Vault, or Let's Encrypt as issuers. Let's Encrypt ACME handles automated issuance for public-facing services. ServiceNow manages certificate request approval workflows. Monitoring integrations (Datadog, Prometheus, Aria Operations) provide expiry alerting dashboards.

| Integration | Purpose |
|---|---|
| Venafi TPP / VaaS | Centralised lifecycle automation and policy enforcement |
| Microsoft ADCS | Internal enterprise CA backend |
| HashiCorp Vault PKI | Short-lived certs for service-to-service mTLS |
| Kubernetes cert-manager | In-cluster automated certificate management |
| Let's Encrypt ACME | Public-facing service certificate automation |
| ServiceNow | Certificate request approval workflow |
| Monitoring (Datadog / Prometheus) | Expiry alerting and compliance dashboards |
