# Azure Troubleshooting

VM connectivity failures are diagnosed by checking NSG inbound/outbound rules at the subnet and NIC level, effective routes on the NIC, and Azure Firewall or NVA policy if traffic traverses a hub network. Azure Storage access-denied errors require checking the storage account firewall (allowed VNets and IPs), the caller's RBAC role assignment, and whether a SAS token has expired or has insufficient permissions. App Service 502/503 errors are most commonly caused by the App Service Plan running at capacity, a failed health check probe, or a dependency (database, Key Vault) timing out.

| Issue | First checks | Commands / Portal path |
|---|---|---|
| VM no connectivity | NSG effective rules, effective routes, Azure Firewall logs | `az network nic show-effective-nsg`, `az network watcher packet-capture` |
| Storage Access Denied | Storage firewall, RBAC role, SAS token expiry | `az storage account show --query networkRuleSet`, check IAM blade |
| App Service 502/503 | App Service Plan CPU/memory, health check config, app logs | App Service → Diagnose and solve problems → Availability |
| Key Vault throttling | Request rate (> 2000/10s for secrets), check metrics | Azure Monitor → Key Vault → Metrics → Service API hits |
| AKS pod not starting | Node resource pressure, image pull errors, NSG blocking egress | `kubectl describe pod`, `kubectl get events`, check ACR firewall |
