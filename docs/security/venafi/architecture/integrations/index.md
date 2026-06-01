# Venafi — Integrations


<div class="kb-summary">
Venafi TPP integrates with Microsoft ADCS as the primary internal CA backend, with DigiCert and Entrust for external and public certificate issuance.
</div>

 HashiCorp Vault PKI secrets engine can be fronted by Venafi policy to enforce organisational standards on dynamically issued certificates. Kubernetes cert-manager uses the Venafi issuer plugin to request certificates from TPP or VaaS for workloads running in-cluster.

ServiceNow integration enables certificate request workflows via ITSM tickets, routing requests through approval before Venafi issues. SIEM integration is achieved via the Venafi Log Server forwarding audit events. A Terraform provider is available for certificate provisioning as part of infrastructure-as-code pipelines.

| Integration | Method | Purpose |
|---|---|---|
| Microsoft ADCS | CA driver in TPP | Internal certificate issuance |
| DigiCert / Entrust | CA driver in TPP | External / public certificate issuance |
| HashiCorp Vault PKI | Venafi policy enforcement layer | Standards enforcement on dynamic PKI |
| Kubernetes cert-manager | Venafi issuer plugin | In-cluster certificate provisioning |
| ServiceNow | REST API / workflow connector | Certificate request approval workflow |
| SIEM | Venafi Log Server syslog forwarding | Audit event centralisation |
| Terraform | Venafi Terraform provider | Certificate provisioning in IaC pipelines |
