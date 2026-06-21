---
tags:
  - aria-networks
  - networking
---
# Aria Networks Cheat Sheet

<div class="kb-summary">
Top-10 Aria Networks (vRNI) REST API calls for network entity queries, path analysis, flow data, and event management.
</div>
![Aria Networks Cheat Sheet](../../assets/reference-cheat-sheets-aria-networks.svg)




## REST API

```bash
BASE="https://vrni/api/ni"

# Authenticate (get token)
TOKEN=$(curl -sk -X POST $BASE/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@local","password":"VMware1!","domain":{"domain_type":"LOCAL"}}' \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")
HDR="-H \"Authorization: NetworkInsight $TOKEN\" -H \"Content-Type: application/json\""

# Entity queries
curl -sk $HDR "$BASE/entities/problems" | python3 -m json.tool             # active problems
curl -sk $HDR -X POST "$BASE/search" \
  -d '{"query":"vm where name = myvm"}' | python3 -m json.tool             # entity search

# Path analysis
curl -sk $HDR -X POST "$BASE/micro-seg/paths" \
  -d '{"source":{"entity":{"entity_id":"<src-id>"}},"destination":{"entity":{"entity_id":"<dst-id>"}}}' \
  | python3 -m json.tool

# Flows
curl -sk $HDR -X POST "$BASE/groups/flows" \
  -d '{"time_range":{"start_time":1700000000,"end_time":1700003600}}' \
  | python3 -m json.tool

# Data sources
curl -sk $HDR "$BASE/data-sources/vcenters" | python3 -m json.tool         # vCenter sources
curl -sk $HDR "$BASE/data-sources/nsxv-managers" | python3 -m json.tool    # NSX sources
```

## See also

- [Aria Networks Procedures](../../virtualization/vmware/aria-operations-for-networks/operations/procedures/)
- [Aria Networks Troubleshooting](../../virtualization/vmware/aria-operations-for-networks/troubleshooting/common-issues/)
