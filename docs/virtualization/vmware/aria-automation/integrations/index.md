# Aria Automation — Integrations

## Overview

Aria Automation integrates with external systems via Cloud Accounts, Integrations, and ABX (Action-Based eXtensibility). Integrations extend blueprints with ITSM workflows, configuration management, and source control.

## vCenter Integration (Cloud Account)

vCenter is added as a Cloud Account in Aria Automation to enable VM provisioning on vSphere.

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

## NSX Integration

NSX is linked to the vCenter cloud account and enables overlay networking in blueprints.

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

## GitHub Integration

GitHub integration enables blueprint source control and CI/CD-driven updates.

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

## Ansible Integration

Ansible integration runs playbooks as part of blueprint provisioning workflows.

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

## ServiceNow Integration

| Configuration Item | Value |
|---|---|
| Integration type | ITSM |
| Protocol | REST API (OAuth 2.0) |
| ServiceNow version | Rome / San Diego / Tokyo+ |
| Auto-approval source | ServiceNow approval workflow |
| Ticket type | RITM (Requested Item) |

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
