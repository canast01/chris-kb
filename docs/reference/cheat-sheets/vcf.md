---
tags:
  - vcf
  - operations
---
# VCF Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 VCF commands for SDDC Manager operations, workload domains, LCM upgrades, and password management via REST API and CLI.
</div>
![VCF Cheat Sheet](../../assets/reference-cheat-sheets-vcf.svg)

## SDDC Manager REST API

```bash
BASE="https://sddc-mgr"
# Get bearer token
TOKEN=$(curl -sk -X POST $BASE/v1/tokens \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"VMware1!"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['accessToken'])")

AUTH="Authorization: Bearer $TOKEN"

# Workload domains
curl -sk -H "$AUTH" $BASE/v1/domains | python3 -m json.tool          # list domains
curl -sk -H "$AUTH" $BASE/v1/domains/<id> | python3 -m json.tool     # domain detail

# Hosts
curl -sk -H "$AUTH" $BASE/v1/hosts | python3 -m json.tool            # commissioned hosts
curl -sk -H "$AUTH" $BASE/v1/hosts?status=UNASSIGNED | python3 -m json.tool  # free hosts

# LCM bundles and upgrades
curl -sk -H "$AUTH" $BASE/v1/bundles | python3 -m json.tool          # available bundles
curl -sk -H "$AUTH" $BASE/v1/upgrades | python3 -m json.tool         # upgrade history

# Cluster operations
curl -sk -H "$AUTH" $BASE/v1/clusters | python3 -m json.tool         # all clusters
```


```text title="Expected output"
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkBsb2NhbCIsImV4cCI6MTcwOTMxNjgwMH0.x7kQ9mZ2pL8vN3qR5sT1uW4yA6bC9dE2fG3hI4jK5lM",
  "expiresIn": 3600
}
{
  "elements": [
    {
      "id": "domain-1",
      "name": "primary-domain",
      "status": "HEALTHY"
    },
    {
      "id": "domain-2",
      "name": "secondary-domain",
      "status": "HEALTHY"
    }
  ]
}
{
  "elements": [
    {
      "id": "host-001",
      "fqdn": "esx-01.lab.local",
      "status": "ASSIGNED",
      "ipAddress": "192.168.1.45"
    },
    {
      "id": "host-002",
      "fqdn": "esx-02.lab.local",
      "status": "ASSIGNED",
      "ipAddress": "192.168.1.46"
    }
  ]
}
{
  "elements": [
    {
      "id": "host-003",
      "fqdn": "esx-03.lab.local",
      "status": "UNASSIGNED",
      "ipAddress": "192.168.1.47"
    }
  ]
}
{
  "elements": [
    {
      "id": "bundle-8.0.1",
      "version": "8.0.1",
      "releaseDate": "2024-02-15"
    },
    {
      "id": "bundle-8.0.2",
      "version": "8.0.2",
      "releaseDate": "2024-03-10"
    }
  ]
}
{
  "elements": [
    {
      "id": "upgrade-1",
      "fromVersion": "7.0.3",
      "toVersion": "8.0.1",
      "status": "COMPLETED",
      "completedAt": "2024-01-20T14:32:00Z"
    }
  ]
}
{
  "elements": [
    {
      "id": "cluster-primary",
      "name": "primary-cluster",
      "domainId": "domain-1",
      "status": "HEALTHY",
      "hostCount": 3
    },
    {
      "id": "cluster-secondary",
      "name": "secondary-cluster",
      "domainId": "domain-2",
      "status": "HEALTHY",
      "hostCount": 2
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification (already present in example; ensure curl supports `-k` on your system).
    **`jq: parse error
## Password management (SDDC Manager appliance SSH)

```bash
vcf-password-ops --getpassword --component VCENTER --account root
vcf-password-ops --rotatepassword --component VCENTER --account root
```


```text title="Expected output"
Password for root account in VCENTER component:
Vc0mpl3x!P@ssw0rd2024

Rotating password for root account in VCENTER component...
Password rotation initiated. Rotation ID: a7f3c2e1-9b4d-4f8a-b2c9-d5e8f1a3b6c9
Waiting for rotation to complete...
Password rotation completed successfully.
New password has been synced to all dependent services.
Rotation completed at 2024-01-15T14:32:18Z
```

!!! warning "Common errors"
    **`Error: Component 'VCENTER' not found in configuration`** — Verify the component name matches your VCF deployment (use `vcf-password-ops --listcomponents` to see available options).
    **`Error: Authentication failed. Insufficient permissions to rotate password`** — Ensure your user account has the VCENTER_ADMIN role or equivalent credentials configured in the VCF environment.
## See also

- [VCF Operations](../../../virtualization/vmware/products/vmware-cloud-foundation/operations/procedures/)
- [VCF Troubleshooting](../../../virtualization/vmware/products/vmware-cloud-foundation/troubleshooting/common-issues/)
