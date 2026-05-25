# Aria Automation — Integrations

```text
┌─────────────────────────────────────────────────────────────┐
│          Aria Automation Integration Topology               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│              ┌──────────────────────────────┐               │
│              │   Aria Automation            │               │
│              │   (VIDM SSO)                 │               │
│              └──┬──────┬───────┬────────┬───┘               │
│                 │      │       │        │                   │
│          vCenter│    NSX│  Git  │ Ansible│                  │
│                 │      │  SCM  │ Tower  │                   │
│                 ▼      ▼       ▼        ▼                   │
│  ┌──────────┐ ┌─────┐ ┌─────┐ ┌──────────────────────┐      │
│  │ vCenter  │ │ NSX │ │Git  │ │ Ansible Tower / AWX  │      │
│  │ :443     │ │:443 │ │:443 │ │  job templates       │      │
│  │ Cloud    │ │Cloud│ │Blue-│ │  post-provision       │     │
│  │ Account  │ │Acct │ │print│ │  config              │      │
│  └──────────┘ └─────┘ └─────┘ └──────────────────────┘      │
│                                                             │
│  Optional integrations:                                     │
│  ServiceNow ── approval workflows ── ITSM change requests   │
│  HashiCorp Vault ── secrets at deploy time                  │
│  ABX (Python/Node.js/PS) ── custom event-driven actions     │
└─────────────────────────────────────────────────────────────┘
```

## Overview

Aria Automation integrates with external systems via Cloud Accounts, Integrations, and ABX (Action-Based eXtensibility). Integrations extend blueprints with ITSM workflows, configuration management, and source control.

## vCenter Cloud Account (Compute Integration)

Aria Automation connects to vCenter Server as a **cloud account** to discover compute resources, networks, and storage, and to provision VMs.

- Go to **Infrastructure > Connections > Cloud Accounts > Add Cloud Account > vCenter**.
- Provide the vCenter FQDN and a service account with the required vCenter permissions (at minimum: create/delete VMs, read datastores and networks).
- After adding, configure **Cloud Zones** to define which clusters/hosts are available to specific projects.

```bash
# Add vCenter cloud account via API
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/cloud-accounts-vsphere \
  -H "Content-Type: application/json" \
  -d '{
    "name": "vcenter-prod",
    "description": "Production vCenter",
    "hostName": "vcenter.example.com",
    "acceptSelfSignedCertificate": false,
    "username": "svc-vra@vsphere.local",
    "password": "<password>",
    "dcId": "onprem"
  }'

# List configured cloud accounts
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/cloud-accounts \
  | python3 -m json.tool

# Trigger data collection refresh
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/iaas/api/cloud-accounts/<account-id>/data-collection"
```

---

## NSX Cloud Account (Network Integration)

Add NSX Manager as a cloud account to allow Aria Automation to provision NSX segments, security groups, and load balancers as part of deployments.

- Go to **Infrastructure > Connections > Cloud Accounts > Add Cloud Account > NSX-T**.
- Provide the NSX Manager FQDN and service account credentials.
- NSX cloud account links to the vCenter cloud account for overlay topology.

```bash
# Associate NSX with an existing vCenter cloud account
curl -sk -X PATCH -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/cloud-accounts-vsphere/<account-id> \
  -H "Content-Type: application/json" \
  -d '{
    "nsxHostName": "nsx-manager.example.com",
    "nsxUsername": "admin",
    "nsxPassword": "<password>"
  }'

# List NSX network segments visible to vRA
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/fabric-networks \
  | python3 -m json.tool
```

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

```bash
# Add GitHub integration
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/integrations \
  -H "Content-Type: application/json" \
  -d '{
    "integrationType": "github",
    "name": "github-blueprints",
    "config": {
      "url": "https://github.com/example-org/vra-blueprints",
      "token": "<personal-access-token>",
      "branch": "main"
    }
  }'

# Sync blueprints from GitHub
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/blueprint/api/integrations/<integration-id>/sync"
```

---

## ServiceNow (Approval Workflows)

The **Aria Automation ITSM Integration plugin** for ServiceNow enables approval workflows where deployment requests in Aria Automation create ServiceNow change requests or approval tickets.

- Requires deployment of the Aria Automation for Service Brokers plugin in ServiceNow.
- Configure the integration endpoint in Aria Automation: **Infrastructure > Connections > Integrations > Service Broker ITSM**.
- Map project-level approval policies to ServiceNow workflow rules.

```bash
# Add ServiceNow ITSM integration
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/catalog/api/admin/sources \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ServiceNow-Prod",
    "typeId": "com.vmware.pscoe.library.catalog.servicenow",
    "config": {
      "url": "https://example.service-now.com",
      "clientId": "<oauth-client-id>",
      "clientSecret": "<oauth-secret>"
    }
  }'

# Test ServiceNow connectivity
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/admin/sources/<source-id>/test"
```

---

## Ansible Tower / AWX (Configuration Management)

Aria Automation integrates with Ansible Tower (or AWX) to trigger Ansible job templates during or after VM provisioning, enabling day-1 OS configuration.

- Go to **Infrastructure > Connections > Integrations > Ansible Tower**.
- Provide the Tower URL and API credentials.
- In Cloud Templates, use the `Ansible` resource type or call Tower via an Orchestrator workflow to execute a job template post-provisioning.

```bash
# Add Ansible integration
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/pipeline/api/integrations \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ANSIBLE",
    "name": "ansible-prod",
    "properties": {
      "hostName": "ansible-tower.example.com",
      "username": "admin",
      "password": "<password>",
      "acceptSelfSignedCertificate": false
    }
  }'
```

Use Ansible in a blueprint via an ABX action or pipeline stage:

```yaml
resources:
  Cloud_Ansible_1:
    type: Cloud.Ansible
    properties:
      host: ${resource.Cloud_vSphere_Machine_1.address}
      osType: linux
      account: ansible-prod
      inventoryFile: /inventories/prod.ini
      playbooks:
        provision:
          - /playbooks/configure-base.yml
        deprovision:
          - /playbooks/decommission.yml
```

---

## HashiCorp Vault (Secrets Management)

Aria Automation can retrieve secrets from HashiCorp Vault instead of storing them in property groups.

- Configure the Vault integration endpoint in Aria Automation.
- Reference Vault secrets in blueprints using the secret reference syntax.
- Vault token or AppRole authentication is supported.

---

## Integration Health Summary

```bash
# List all integrations and their status
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/pipeline/api/integrations \
  | python3 -m json.tool | grep -E '"name"|"status"'

# Check cloud account data collection status
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/data-collector-registrations \
  | python3 -m json.tool
```

Verify all integration endpoint connections regularly:

```text
Infrastructure > Connections > Cloud Accounts  — check green status for all vCenter and NSX accounts
Infrastructure > Connections > Integrations    — check all integration endpoints are reachable
```
