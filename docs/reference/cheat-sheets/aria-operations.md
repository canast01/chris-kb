---
tags:
  - aria-operations
  - monitoring
---
# Aria Operations Cheat Sheet

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

## See also

- [Aria Operations Procedures](../../../virtualization/vmware/aria-operations/operations/procedures/)
- [Aria Operations Troubleshooting](../../../virtualization/vmware/aria-operations/troubleshooting/common-issues/)
