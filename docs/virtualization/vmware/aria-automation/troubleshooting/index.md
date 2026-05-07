# Aria Automation — Troubleshooting

## Blueprint Validation Errors

Blueprint validation errors appear in the Design canvas or via the API response. Most are YAML syntax errors, missing required inputs, or invalid resource property values.

```bash
# Validate a blueprint via API
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/validate \
  -H "Content-Type: application/json" \
  -d @./blueprint-payload.json

# Check blueprint content for YAML issues locally
python3 -c "import yaml,sys; yaml.safe_load(open('blueprint.yaml'))" \
  && echo "YAML OK" || echo "YAML syntax error"

# Get blueprint validation details
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/blueprint/api/blueprints/<blueprint-id>/versions/<version>/validate" \
  | python3 -m json.tool
```

Common blueprint validation errors:

| Error | Cause | Fix |
|---|---|---|
| `Resource type not found` | Typo in resource type or cloud account not linked | Verify resource type and cloud account association |
| `Required property missing` | Mandatory field omitted | Add required property from schema reference |
| `Circular dependency` | Resource A depends on B which depends on A | Remove circular `${resource...}` reference |
| `Invalid expression` | Bad `${}` interpolation syntax | Check expression against schema; use `${input.x}` |
| `Flavor not found` | Flavor mapping missing for cloud zone | Add flavor mapping in Infrastructure > Flavor Mappings |
| `Image not found` | Image mapping missing | Add image mapping in Infrastructure > Image Mappings |

## Deployment Failures

```bash
# Get deployment failure details
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/<deployment-id>/events?eventTypes=FAILED" \
  | python3 -m json.tool

# Check Aria Automation application logs
ssh root@<vra-appliance>
tail -200 /var/log/vra/vco-server/app.log | grep -i "error\|exception"
tail -200 /var/log/vra/catalog-service/app.log | grep -i "error\|exception"

# Check the provisioning service log
tail -200 /var/log/vra/provisioning/app.log | grep -i "error\|failed"
```

Log file locations:

| Log | Path | Service |
|---|---|---|
| Catalog service | `/var/log/vra/catalog-service/app.log` | Service Catalog |
| Provisioning | `/var/log/vra/provisioning/app.log` | VM provisioning |
| vRO (Orchestrator) | `/var/log/vro/app.log` | Workflow engine |
| IAaaS (cloud proxy) | `/var/log/vra-iaas/agent.log` | On-prem cloud proxy |
| Gateway | `/var/log/vra/gateway/app.log` | API gateway |

## Integration Issues

```bash
# Test vCenter cloud account connectivity
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/iaas/api/cloud-accounts/<account-id>/test"

# Refresh data collection for a cloud account
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/iaas/api/cloud-accounts/<account-id>/data-collection"

# Check cloud proxy status (on-prem environments)
curl -sk -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/iaas/api/data-collector-registrations \
  | python3 -m json.tool | grep -E '"status"|"name"'

# Check cloud proxy logs on the proxy VM
ssh root@<cloud-proxy-vm>
tail -200 /opt/vmware/tocata/agent/logs/agent.log | grep -i "error\|disconnect"
```

## vRO Workflow Failures

When ABX actions or vRO workflow integrations fail, check the Orchestrator logs:

```bash
# Check vRO workflow run status
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/vco/api/workflows/<workflow-id>/executions/<execution-id>" \
  | python3 -m json.tool

# Get workflow execution log
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/vco/api/workflows/<workflow-id>/executions/<execution-id>/logs" \
  | python3 -m json.tool

# List failed workflow runs from the last 24h
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/vco/api/workflows/executions?status=failed&maxResult=50" \
  | python3 -m json.tool
```

## Common Deployment Error Patterns

| Symptom | Root Cause | Resolution |
|---|---|---|
| VM stuck in `Provisioning` > 30 min | vCenter task hung or cloud proxy offline | Check vCenter tasks; restart cloud proxy |
| `Flavor not found` during deploy | Flavor mapping not set for cloud zone | Add mapping in Infrastructure |
| Network resource fails with `no available IPs` | IP range exhausted in NSX or IPAM | Expand IP range or release unused IPs |
| Snapshot day-2 action fails | VM has existing snapshot limit hit | Remove old snapshots; default VMware limit is 31 |
| `Authentication failed` in ABX action | Secret expired in Action runtime | Rotate secret in Cloud Assembly > ABX > Secrets |

## Support Bundle Collection

```bash
# Generate Aria Automation support bundle
/var/lib/vra/support/collect-support-data.sh --output /tmp/

# Collect specific service logs
/var/lib/vra/support/collect-support-data.sh \
  --services catalog,provisioning,vro \
  --since "2026-05-06 00:00" \
  --output /tmp/

ls -lh /tmp/vra-support-*.zip
```
