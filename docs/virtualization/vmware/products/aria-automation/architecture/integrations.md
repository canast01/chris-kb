---
tags:
  - architecture
  - aria-automation
  - vmware
---
# Aria Automation — Integrations

*Applies to: VMware Aria 8.x*
![Aria Automation — Integrations](../../../../../assets/virtualization-vmware-aria-automation-architecture-integrati.svg)

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


```text title="Expected output"
{
  "id": "ca-8f2e9c1d-7b4a-4e2f-9a3c-5d1b8e7f2a4c",
  "name": "vcenter-prod",
  "description": "Production vCenter",
  "cloudAccountType": "vsphere",
  "hostName": "vcenter.example.com",
  "username": "svc-vra@vsphere.local",
  "dcId": "onprem",
  "createdAt": "2024-01-15T10:32:47.123Z",
  "updatedAt": "2024-01-15T10:32:47.123Z",
  "links": {
    "self": "/iaas/api/cloud-accounts/ca-8f2e9c1d-7b4a-4e2f-9a3c-5d1b8e7f2a4c"
  }
}

[
  {
    "id": "ca-8f2e9c1d-7b4a-4e2f-9a3c-5d1b8e7f2a4c",
    "name": "vcenter-prod",
    "cloudAccountType": "vsphere",
    "hostName": "vcenter.example.com"
  },
  {
    "id": "ca-3a7f1c9e-2b5d-4a8f-6e1c-9d3a2b7f5e8c",
    "name": "vcenter-dr",
    "cloudAccountType": "vsphere",
    "hostName": "vcenter-dr.example.com"
  }
]

(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Set `acceptSelfSignedCertificate` to `true` in the JSON payload or use `-k` flag (already present; verify vCenter certificate chain is valid). |
    | `{"message":"Unauthorized","statusCode":401}` | Ensure `$TOKEN` is set to a valid bearer token by running `TOKEN=$(curl -sk -X POST https://<vra-fqdn>/csp/gateway/api/tokens -d 'username=<user>&password=<pass>')` first. |
    | `{"message":"Invalid cloud account type","statusCode":400}` | Verify the endpoint URL is correct (`/iaas/api/cloud-accounts-vsphere` not `/cloud-accounts`) and the vCenter hostname is reachable from the Aria Automation appliance. |
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

```text title="Expected output"
{
  "id": "source-8f4c2a91-7e3d-4b9c-a1f2-9d8e7c6b5a4f",
  "name": "ServiceNow-Prod",
  "typeId": "com.vmware.pscoe.library.catalog.servicenow",
  "config": {
    "url": "https://example.service-now.com",
    "clientId": "<oauth-client-id>"
  },
  "createdDate": "2024-01-15T14:32:18.456Z",
  "lastUpdatedDate": "2024-01-15T14:32:18.456Z",
  "status": "CREATED"
}
{
  "statusCode": 200,
  "message": "Connection test successful",
  "details": {
    "responseTime": "342ms",
    "authenticated": true,
    "apiVersion": "v2.1"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the vRA certificate into your system's trusted CA store. |
    | `{"error":"Invalid token","statusCode":401}` | Verify the Bearer token is valid and not expired by checking `echo $TOKEN` and regenerating from vRA authentication endpoint if needed. |
    | `{"error":"Invalid typeId","statusCode":400}` | Confirm the ServiceNow integration typeId matches your vRA version by checking available source types in the catalog API documentation. |
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

## See also

- [Aria Automation — How It Works](../how-it-works/)
- [Aria Automation — Deploy](../../deploy/)
