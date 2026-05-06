# Azure Integration

On-premises connectivity to Azure is delivered via ExpressRoute for dedicated private circuits or VPN Gateway as a backup path, with BGP route exchange into the hub Virtual Network. Hybrid identity is synchronised from on-premises Active Directory to Entra ID using Azure AD Connect, with Password Hash Sync or Pass-Through Authentication depending on the security requirements. GitHub Actions pipelines authenticate to Azure using OIDC federation with a service principal or managed identity, eliminating the need for long-lived client secrets, and Terraform remote state is stored in Azure Blob Storage with state-file locking via blob leases.

| Integration | Method | Notes |
|---|---|---|
| On-premises network | ExpressRoute (primary) + VPN Gateway (failover) | BGP into hub VNet via Virtual Network Gateway |
| Active Directory | Azure AD Connect with PHS or PTA | Seamless SSO enabled for domain-joined devices |
| Monitoring | Azure Monitor + Log Analytics → Sentinel or Splunk | Diagnostic settings on all resources; DCR-based collection |
| CI/CD | GitHub Actions + OIDC → Azure service principal | Federated credentials; no client secret rotation required |
| Terraform | Remote state in Azure Blob Storage (backend "azurerm") | Separate storage account per environment; versioning enabled |
| Backup | Azure Backup with Recovery Services vault | Cross-region restore enabled for production vaults |
