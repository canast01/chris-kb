---
tags:
  - aria-automation
  - automation
---
# Aria Automation Cheat Sheet

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

## See also

- [Aria Automation Procedures](../../virtualization/vmware/aria-automation/operations/procedures/)
- [Aria Automation Troubleshooting](../../virtualization/vmware/aria-automation/troubleshooting/common-issues/)
