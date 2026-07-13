---
tags:
  - aria-operations
  - monitoring
description: "Top-10 Aria Operations (vROps) commands for alerts, metrics, policy management, and adapter status via REST API."
---
# Aria Operations Cheat Sheet

*Applies to: All products*

<div class="kb-summary">
Top-10 Aria Operations (vROps) commands for alerts, metrics, policy management, and adapter status via REST API.
</div>
![Aria Operations Cheat Sheet](../../assets/reference-cheat-sheets-aria-operations.svg)

## REST API (curl examples)

```bash
BASE="https://vrops/suite-api/api"
AUTH="-u admin:VMware1!"

# Token auth (preferred)
TOKEN=$(curl -sk $AUTH -X POST $BASE/auth/token/acquire \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"VMware1!","authSource":"LOCAL"}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
HDR="-H \"Authorization: vRealizeOpsToken $TOKEN\""

# Alerts
curl -sk $AUTH "$BASE/alerts?activeOnly=true" | python3 -m json.tool      # active alerts
curl -sk $AUTH "$BASE/alerts/<alert-id>" | python3 -m json.tool           # alert detail
curl -sk $AUTH -X PATCH "$BASE/alerts/action/dismiss" \
  -d '{"alertIds":["<id>"]}' -H "Content-Type: application/json"          # dismiss alert

# Resources
curl -sk $AUTH "$BASE/resources?resourceKind=VirtualMachine" | python3 -m json.tool  # all VMs
curl -sk $AUTH "$BASE/resources/<id>/stats?statKey=cpu|usage_average" | python3 -m json.tool

# Adapters
curl -sk $AUTH "$BASE/adapters" | python3 -m json.tool                    # adapter instances
curl -sk $AUTH -X POST "$BASE/adapters/<id>/monitoringstate/start"        # start adapter
```


```text title="Expected output"
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImlhdCI6MTcwOTMxNjU0MiwiZXhwIjoxNzA5MzIwMTQyfQ.x7kL9mN2pQrS5tUvWxYzAbCdEfGhIjKlMnOpQrStUv"
}
{
  "pageInfo": {
    "totalCount": 3,
    "pageSize": 100,
    "startIndex": 0
  },
  "alerts": [
    {
      "id": "alert-12345",
      "alertDefinitionId": "AlertDef-CPU-High",
      "resourceId": "res-vm-prod-01",
      "severity": "CRITICAL",
      "startDate": 1709316542000,
      "cancelDate": null,
      "message": "CPU usage is above 90%"
    },
    {
      "id": "alert-12346",
      "alertDefinitionId": "AlertDef-Memory-High",
      "resourceId": "res-vm-prod-02",
      "severity": "WARNING",
      "startDate": 1709315000000,
      "message": "Memory usage is above 85%"
    }
  ]
}
{
  "pageInfo": {
    "totalCount": 24,
    "pageSize": 100
  },
  "resourceList": [
    {
      "identifier": "res-vm-prod-01",
      "resourceName": "prod-web-server-01",
      "resourceKind": "VirtualMachine",
      "resourceStatus": "STARTED",
      "creationTime": 1708900000000
    },
    {
      "identifier": "res-vm-prod-02",
      "resourceName": "prod-db-server-01",
      "resourceKind": "VirtualMachine",
      "resourceStatus": "STARTED"
    }
  ]
}
{
  "statsList": [
    {
      "statKey": "cpu|usage_average",
      "timestamps": [1709316300000, 1709316600000],
      "values": [78.5, 82.3]
    }
  ]
}
{
  "pageInfo": {
    "totalCount": 2
  },
  "adapterInstancesList": [
    {
      "id": "adapter-vcenter-01",
      "adapterKindKey": "VMware vCenter Adapter",
      "name": "vCenter-Prod",
      "state": "STARTED"
    },
    {
      "id": "adapter-nsxt-01",
      "adapterKindKey": "NSX-T Adapter",
      "name": "NSX-T-Prod",
      "state": "STOPPED"
    }
  ]
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present
## See also

- [Aria Operations Procedures](../../../virtualization/vmware/products/aria-operations/operations/procedures/)
- [Aria Operations Troubleshooting](../../../virtualization/vmware/products/aria-operations/troubleshooting/common-issues/)
