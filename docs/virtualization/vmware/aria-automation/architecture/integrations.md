---
tags:
  - architecture
  - aria-automation
  - vmware
---
# Aria Automation — Integrations

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
```text
┌─────────────────────────────────── Aria Automation — Integrations ────────────────────────────────────┐
│                                                                                                       │
│  Aria Automation integrates with identity, monitoring, ITSM, and cloud endpoints.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Identity & SSO Integrations          │  │         Infrastructure Integrations         │   │
│   │         vIDM/Workspace ONE: SAML SSO         │  │      vCenter: VM/network/storage prov.      │   │
│   │       Active Directory via LDAP/LDAPS        │  │       NSX-T: segment + security group       │   │
│   │      SCIM group sync for project roles       │  │         AWS/Azure/GCP cloud accounts        │   │
│   │        MFA enforced via vIDM policies        │  │       Terraform Cloud/Enterprise IaaC       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Operational and ITSM integrations close the loop between provisioning and governance.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              ITSM / Governance               │  │                Observability                │   │
│   │       ServiceNow: CMDB + request sync        │  │      Aria Operations: cost+health data      │   │
│   │       Jira: ticket creation on deploy        │  │       CloudWatch / Azure Monitor hooks      │   │
│   │       Salt/Puppet/Ansible config mgmt        │  │      Aria Ops for Logs: vRA audit logs      │   │
│   │        REST API: custom integrations         │  │       Webhooks: event broker endpoints      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance VMs · AD servers · NSX managers · vCenter · cloud region endpoints                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vIDM             = VMware Identity Manager; provides SSO and MFA for vRA and Aria suite              │
│  SCIM             = System for Cross-domain Identity Management; syncs groups from AD to vIDM         │
│  LDAP integration = vRA reads AD groups to map project members and roles                              │
│  NSX-T segment    = Logical network created by vRA during VM provisioning via NSX API                 │
│  Cloud account    = vRA connection record holding credentials for a specific cloud endpoint           │
│  IaaC integration = Terraform Cloud/Enterprise workspace managed from vRA catalog                     │
│  ServiceNow plugin= vRA plugin syncing deployments and change records to ServiceNow CMDB              │
│  ABX webhook      = ABX action that POSTs JSON to external URL on resource lifecycle event            │
│  Config mgmt      = Ansible/Salt/Puppet bootstrap run as post-deploy ABX or Orchestrator wf           │
│  REST API         = vRA public API (swagger at /vco/api); used for all automation integrations        │
│  Event broker     = vRA pub-sub system; publishes events to subscribed ABX or Orchestrator wf         │
│  Cost integration = Aria Operations cost data surfaced in vRA to show estimated spend per item        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
```text
Infrastructure > Connections > Cloud Accounts  — check green status for all vCenter and NSX accounts
Infrastructure > Connections > Integrations    — check all integration endpoints are reachable
```
