# Aria Automation — Integration

## vCenter Cloud Account (Compute Integration)

Aria Automation connects to vCenter Server as a **cloud account** to discover compute resources, networks, and storage, and to provision VMs.

- Go to **Infrastructure > Connections > Cloud Accounts > Add Cloud Account > vCenter**.
- Provide the vCenter FQDN and a service account with the required vCenter permissions (at minimum: create/delete VMs, read datastores and networks).
- After adding, configure **Cloud Zones** to define which clusters/hosts are available to specific projects.

---

## NSX Cloud Account (Network Integration)

Add NSX Manager as a cloud account to allow Aria Automation to provision NSX segments, security groups, and load balancers as part of deployments.

- Go to **Infrastructure > Connections > Cloud Accounts > Add Cloud Account > NSX-T**.
- Provide the NSX Manager FQDN and service account credentials.
- NSX cloud account links to the vCenter cloud account for overlay topology.

---

## Active Directory / LDAP (User Authentication)

User authentication is handled by **VMware Workspace ONE Access (vIDM)**, which is deployed as part of the Aria Automation appliance or as a standalone service.

- Configure the LDAP/AD directory sync in Workspace ONE Access.
- Users and groups sync to Workspace ONE Access; assign them to Aria Automation projects via the Aria Automation UI (**Infrastructure > Administration > Projects > Users**).
- Supports SAML 2.0 federated identity for enterprise SSO.

---

## GitHub / GitLab (Pipeline SCM)

Aria Automation Pipelines integrates with Git repositories for pipeline trigger (push/PR events) and blueprint/template version control.

- Go to **Pipelines > Endpoints > Add Endpoint > GitHub** or **GitLab**.
- Provide repository URL and a personal access token with repo read/write permissions.
- Configure webhooks in the Git repository to trigger pipelines on push events.

---

## ServiceNow (Approval Workflows)

The **Aria Automation ITSM Integration plugin** for ServiceNow enables approval workflows where deployment requests in Aria Automation create ServiceNow change requests or approval tickets.

- Requires deployment of the Aria Automation for Service Brokers plugin in ServiceNow.
- Configure the integration endpoint in Aria Automation: **Infrastructure > Connections > Integrations > Service Broker ITSM**.
- Map project-level approval policies to ServiceNow workflow rules.

---

## Ansible Tower / AWX (Configuration Management)

Aria Automation integrates with Ansible Tower (or AWX) to trigger Ansible job templates during or after VM provisioning, enabling day-1 OS configuration.

- Go to **Infrastructure > Connections > Integrations > Ansible Tower**.
- Provide the Tower URL and API credentials.
- In Cloud Templates, use the `Ansible` resource type or call Tower via an Orchestrator workflow to execute a job template post-provisioning.

---

## HashiCorp Vault (Secrets Management)

Aria Automation can retrieve secrets from HashiCorp Vault instead of storing them in property groups.

- Configure the Vault integration endpoint in Aria Automation.
- Reference Vault secrets in blueprints using the secret reference syntax.
- Vault token or AppRole authentication is supported.

---

## Integration Endpoint Health

Verify all integration endpoint connections regularly:

```
Infrastructure > Connections > Cloud Accounts  — check green status for all vCenter and NSX accounts
Infrastructure > Connections > Integrations    — check all integration endpoints are reachable
```
