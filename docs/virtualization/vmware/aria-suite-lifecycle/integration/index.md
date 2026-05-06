# Aria Suite Lifecycle Integration

LCM's integration hub is Workspace ONE Access (VIDM), which provides SSO and RBAC for all Aria products; the VIDM appliance is registered during initial LCM setup and must remain reachable for product deployments to succeed. vCenter integration is required for LCM to deploy and manage OVA-based appliances — a dedicated service account with minimum `Virtual Machine Power User` role on the target cluster is recommended. NSX-T integration is configured per-environment to enable segment creation for deployed products, and SMTP is configured under LCM Settings > SMTP to send upgrade and certificate alert notifications.

| Integration | Purpose | Required Credential |
|---|---|---|
| Workspace ONE Access (VIDM) | SSO and identity for all Aria products | VIDM admin account |
| vCenter Server | OVA deployment, VM management | vCenter service account |
| NSX-T Manager | Network segment provisioning | NSX admin or operator account |
| SMTP / Mail Relay | Upgrade and alert notifications | SMTP relay credentials (if auth required) |
| NFS Server | Binary repository for bundles | NFS mount (no auth — network-level access control) |
| Proxy Server | Outbound internet for bundle downloads | Proxy credentials (if authenticated proxy) |
