# Aria Automation — Common Issues

## Blueprint Validation Errors

```bash
# Validate a blueprint via API
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  https://<vra-fqdn>/blueprint/api/blueprints/validate \
  -H "Content-Type: application/json" \
  -d @./blueprint-payload.json

# Check YAML syntax locally
python3 -c "import yaml,sys; yaml.safe_load(open('blueprint.yaml'))" \
  && echo "YAML OK" || echo "YAML syntax error"
```

| Error | Cause | Fix |
|---|---|---|
| `Resource type not found` | Typo in resource type or cloud account not linked | Verify resource type and cloud account association |
| `Required property missing` | Mandatory field omitted | Add required property from schema reference |
| `Circular dependency` | Resource A depends on B which depends on A | Remove circular `${resource...}` reference |
| `Flavor not found` | Flavor mapping missing for cloud zone | Add flavor mapping in Infrastructure > Flavor Mappings |
| `Image not found` | Image mapping missing | Add image mapping in Infrastructure > Image Mappings |

## Cloud Account Connectivity Failure

1. Test network connectivity from appliance to vCenter/NSX management plane
2. Confirm service account credentials have not expired
3. Re-validate cloud account in Aria Automation UI
4. Check logs: `kubectl logs -n prelude -l app=vra-nginx`
