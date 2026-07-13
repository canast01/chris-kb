---
tags:
  - aria-automation
  - automation
description: "Top-10 Aria Automation (vRA) commands for deployment lifecycle, ABX actions, and catalog management via REST API and vra-cli."
---
# Aria Automation Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 Aria Automation (vRA) commands for deployment lifecycle, ABX actions, and catalog management via REST API and vra-cli.
</div>
![Aria Automation Cheat Sheet](../../assets/reference-cheat-sheets-aria-automation.svg)

## vra-cli

```bash
vra-cli login --server vra.lab.local --username configadmin --password VMware1!
vra-cli get deployment                         # list all deployments
vra-cli get deployment --name myapp            # deployment detail
vra-cli get catalog-item                       # available catalog items
vra-cli get cloud-account                      # cloud accounts (vCenter, AWS, etc.)
vra-cli get project                            # projects and members
```


```text title="Expected output"
Successfully authenticated to vra.lab.local
Deployment ID: deploy-a4f2c8e9-1b3d-4e7f-9c2a-5d6e7f8g9h0i | Name: webapp-prod | Status: ACTIVE | Owner: configadmin
Deployment ID: deploy-b5g3d9f0-2c4e-5f8g-0d3b-6e7f8g9h0i1j | Name: database-cluster | Status: ACTIVE | Owner: sysadmin
Deployment ID: deploy-c6h4e0g1-3d5f-6g9h-1e4c-7f8g9h0i1j2k | Name: cache-layer | Status: PROVISIONING | Owner: configadmin
...
Deployment: myapp | Status: ACTIVE | Created: 2024-01-15T09:32:15Z | Last Modified: 2024-01-18T14:22:08Z | Resources: 12
Catalog Item: CentOS-8-Template | Type: Machine | Status: PUBLISHED | Project: IT-Operations
Catalog Item: Windows-Server-2022 | Type: Machine | Status: PUBLISHED | Project: IT-Operations
Catalog Item: Ubuntu-22.04-LTS | Type: Machine | Status: PUBLISHED | Project: IT-Operations
...
Cloud Account: vCenter-Primary | Type: vSphere | Region: us-west-1 | Status: CONNECTED
Cloud Account: AWS-Production | Type: AWS | Region: us-east-1 | Status: CONNECTED
Cloud Account: Azure-Dev | Type: Azure | Region: eastus | Status: DISCONNECTED
...
Project: IT-Operations | Members: 8 | Owner: configadmin | Status: ACTIVE
Project: Development | Members: 5 | Owner: devlead | Status: ACTIVE
Project: Finance-Systems | Members: 3 | Owner: financeadmin | Status: ACTIVE
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unable to connect to vra.lab.local:443 - connection refused` | Verify the vRA server hostname/IP is correct and the service is running with `systemctl status vra-server`. |
    | `Error: Authentication failed - Invalid credentials` | Confirm the username and password are correct; check if the account is locked or expired in vRA's identity provider. |
    | `Error: No deployments found - insufficient permissions` | Ensure the configadmin user has the appropriate project membership or global admin role assigned in vRA. |
## REST API

```bash
BASE="https://vra"

# Get API token
TOKEN=$(curl -sk -X POST $BASE/csp/gateway/am/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"configadmin","password":"VMware1!"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
HDR="-H \"Authorization: Bearer $TOKEN\""

# Deployments
curl -sk $HDR $BASE/deployment/api/deployments | python3 -m json.tool      # all deployments
curl -sk $HDR $BASE/deployment/api/deployments/<id>/resources | python3 -m json.tool

# Delete a deployment
curl -sk $HDR -X DELETE $BASE/deployment/api/deployments/<id>

# Blueprints
curl -sk $HDR $BASE/blueprint/api/blueprints | python3 -m json.tool        # all blueprints

# Cloud zones
curl -sk $HDR $BASE/iaas/api/cloud-accounts | python3 -m json.tool         # cloud accounts
curl -sk $HDR $BASE/iaas/api/zones | python3 -m json.tool                  # cloud zones
```


```text title="Expected output"
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjb25maWdhZG1pbiIsImlhdCI6MTcwMjQyMzQ1MiwiZXhwIjoxNzAyNTA5ODUyfQ.a3B9mK2lQ8vN5xY7zJ1wP4rT6sU9vW2xA5bC8dE3fG4"
}
{
  "content": [
    {
      "id": "deployment-001-abc123",
      "name": "prod-web-tier",
      "status": "CREATE_SUCCESSFUL",
      "createdAt": "2024-01-12T08:34:22Z"
    },
    {
      "id": "deployment-002-def456",
      "name": "staging-db-cluster",
      "status": "CREATE_SUCCESSFUL",
      "createdAt": "2024-01-11T15:22:10Z"
    }
  ],
  "totalElements": 2
}
{
  "content": [
    {
      "id": "resource-vm-001",
      "name": "web-server-01",
      "type": "Cloud.Machine",
      "state": "ACTIVE"
    },
    {
      "id": "resource-net-001",
      "name": "prod-network",
      "type": "Cloud.Network",
      "state": "ACTIVE"
    }
  ]
}
{
  "content": [
    {
      "id": "blueprint-prod-001",
      "name": "wordpress-deployment",
      "status": "PUBLISHED",
      "createdAt": "2024-01-10T12:45:33Z"
    },
    {
      "id": "blueprint-staging-002",
      "name": "lamp-stack",
      "status": "PUBLISHED",
      "createdAt": "2024-01-09T09:12:15Z"
    }
  ],
  "totalElements": 2
}
{
  "content": [
    {
      "id": "account-aws-prod",
      "name": "AWS Production",
      "type": "aws",
      "enabled": true
    },
    {
      "id": "account-vsphere-lab",
      "name": "vSphere Lab",
      "type": "vsphere",
      "enabled": true
    }
  ]
}
{
  "content": [
    {
      "id": "zone-us-east-1",
      "name": "us-east-1",
      "cloudAccountId": "account-aws-prod",
      "placementPolicy": "DEFAULT"
    },
    {
      "id": "zone-vsphere-dc1",
      "name": "datacenter-1",
      "cloudAccountId": "account-vsphere-lab",
      "placementPolicy": "DEFAULT"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command |
## See also

- [Aria Automation Procedures](../../../virtualization/vmware/products/aria-automation/operations/procedures/)
- [Aria Automation Troubleshooting](../../../virtualization/vmware/products/aria-automation/troubleshooting/common-issues/)
