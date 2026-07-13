---
tags:
  - aria-suite-lifecycle
  - operations
description: "Top-10 Aria Suite Lifecycle (LCM) REST API calls for product installation, upgrades, locker management, and certificate operations."
---
# Aria Suite Lifecycle Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 Aria Suite Lifecycle (LCM) REST API calls for product installation, upgrades, locker management, and certificate operations.
</div>
![Aria Suite Lifecycle Cheat Sheet](../../assets/reference-cheat-sheets-aria-suite-lifecycle.svg)

## REST API

```bash
BASE="https://lcm/lcm/api"
AUTH="-u admin@local:VMware1!"

# Environments
curl -sk $AUTH $BASE/v2/environments | python3 -m json.tool                # all environments
curl -sk $AUTH "$BASE/v2/environments/<env-id>" | python3 -m json.tool     # environment detail

# Products in an environment
curl -sk $AUTH "$BASE/v2/environments/<env-id>/products" | python3 -m json.tool

# Locker (credential store)
curl -sk $AUTH $BASE/v2/locker/passwords | python3 -m json.tool            # stored passwords
curl -sk $AUTH $BASE/v2/locker/certificates | python3 -m json.tool         # stored certs
curl -sk $AUTH $BASE/v2/locker/licenses | python3 -m json.tool             # stored licenses

# Certificates
curl -sk $AUTH -X POST $BASE/v2/locker/certificates/import \
  -H "Content-Type: application/json" \
  -d '{"alias":"my-cert","certificateChain":"-----BEGIN CERTIFICATE-----\n..."}' # import cert

# Upgrades
curl -sk $AUTH $BASE/v2/lcm/upgrades | python3 -m json.tool                # upgrade tasks
curl -sk $AUTH $BASE/v2/lcm/request/<req-id> | python3 -m json.tool        # request status

# Requests (track async ops)
curl -sk $AUTH $BASE/v2/requests | python3 -m json.tool                    # all recent requests
```


```text title="Expected output"
{
  "elements": [
    {
      "id": "env-5f8c2a1b-9e4d-47c3-b2f1-8d6e3c9a1f2b",
      "name": "Production",
      "status": "READY",
      "datacenterName": "DC-East-01"
    },
    {
      "id": "env-7a3d1c9f-2e5b-41a8-c6d2-9f4a2b8e5c3d",
      "name": "Staging",
      "status": "READY",
      "datacenterName": "DC-West-02"
    }
  ],
  "pageInfo": {
    "pageNumber": 1,
    "pageSize": 20,
    "totalElements": 2
  }
}
{
  "id": "env-5f8c2a1b-9e4d-47c3-b2f1-8d6e3c9a1f2b",
  "name": "Production",
  "status": "READY",
  "products": [
    "vSphere",
    "vSAN",
    "NSX-T"
  ],
  "createdDate": "2024-01-15T08:32:14Z"
}
{
  "elements": [
    {
      "productName": "vSphere",
      "version": "8.0.1",
      "status": "INSTALLED"
    },
    {
      "productName": "vSAN",
      "version": "8.0.0",
      "status": "INSTALLED"
    }
  ]
}
{
  "elements": [
    {
      "id": "pwd-a1b2c3d4e5f6",
      "alias": "vcenter-root",
      "username": "root",
      "createdDate": "2024-01-10T14:22:05Z"
    }
  ]
}
{
  "elements": [
    {
      "id": "cert-9f8e7d6c5b4a",
      "alias": "wildcard-local",
      "issuer": "CN=Local CA",
      "expirationDate": "2025-12-31T23:59:59Z"
    }
  ]
}
{
  "elements": [
    {
      "id": "lic-xyz789",
      "productName": "vSphere",
      "licenseKey": "XXXXX-XXXXX-XXXXX-XXXXX-XXXXX",
      "status": "VALID"
    }
  ]
}
{
  "requestId": "req-import-cert-20240215-001",
  "status": "COMPLETED",
  "message": "Certificate imported successfully"
}
{
  "elements": [
    {
      "id": "upg-task-001",
      "sourceVersion": "7.0.3",
      "targetVersion": "8.0.1",
      "status": "COMPLETED",
      "completedDate": "2024-02-10T16:45:22Z"
    }
  ]
}
```
## See also

- [Aria Suite Lifecycle Procedures](../../../virtualization/vmware/products/aria-suite-lifecycle/operations/procedures/)
- [Aria Suite Lifecycle Troubleshooting](../../../virtualization/vmware/products/aria-suite-lifecycle/troubleshooting/common-issues/)
