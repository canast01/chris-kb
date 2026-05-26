# Aria Automation — Common Issues

## Blueprint Validation Errors

```bash
# Validate a blueprint via API before publishing
TOKEN=<your-token>
curl -sk -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  "https://vra-prod-01.example.local/blueprint/api/blueprints/validate" \
  -d @./blueprint-payload.json | jq '.'

# Check YAML syntax locally before submitting
python3 -c "import yaml,sys; yaml.safe_load(open('blueprint.yaml'))" \
  && echo "YAML OK" || echo "YAML syntax error"
```

| Error | Cause | Fix |
|---|---|---|
| `Resource type not found` | Typo in resource type or cloud account not linked to project | Verify resource type and cloud account → cloud zone → project association |
| `Required property missing` | Mandatory field omitted in the template | Add the required property from the schema reference |
| `Circular dependency` | Resource A depends on B which depends on A | Remove circular `${resource...}` binding |
| `Flavor not found` | Flavor mapping missing for the target cloud zone | Add flavor mapping: **Infrastructure → Configure → Flavor Mappings** |
| `Image not found` | Image mapping missing for cloud zone | Add image mapping: **Infrastructure → Configure → Image Mappings** |
| `Network profile not found` | No network profile matched to the cloud zone | Create a network profile and associate it with the cloud zone |
| `Cloud zone quota exceeded` | Project CPU/memory/VM limit reached | Increase project quota or delete unused deployments |

---

## Cloud Account Connectivity Failure

Symptoms: cloud account shows a red/warning indicator; new deployments fail at the "Provisioning" stage.

```bash
# Test vCenter reachability from Aria Automation appliance
ssh root@vra-prod-01.example.local
curl -sk -o /dev/null -w "%{http_code}" \
  https://vcenter-prod.example.local/rest/com/vmware/cis/session
# 401 = reachable but auth needed (expected)
# 000 = unreachable (DNS, firewall, or vCenter down)

# Check for expired service account password
kubectl logs -n prelude -l app=iaas-gateway --tail=200 | \
  grep -i "invalid credentials\|401\|authentication"

# Test NSX connectivity
curl -sk -o /dev/null -w "%{http_code}" \
  https://nsx-mgr-01.example.local/api/v1/transport-nodes
```

Resolution:
1. Reset the service account password in vCenter/NSX/AD
2. **Infrastructure → Connections → Cloud Accounts → Edit → update credentials → Validate**
3. If validation fails still: check certificate trust — the Aria Automation appliance must trust the vCenter/NSX certificate CA

---

## Deployment Stuck in "Creating" or "Deleting"

Symptoms: a deployment stays in `CREATE_INPROGRESS` or `DELETE_INPROGRESS` for more than 30 minutes.

```bash
# Check the deployment event log (UI)
# Deployments → select deployment → History tab → review events

# Check IaaS Gateway logs
kubectl logs -n prelude -l app=iaas-gateway --tail=300 | grep -i "error\|timeout\|fail"

# Check vCenter tasks (the deployment may have completed in vCenter but Aria Automation lost the callback)
# vCenter → Recent Tasks → filter by Aria Automation service account name
```

If the VM was created in vCenter but the deployment is stuck:
- Do not delete the VM from vCenter directly — this orphans the deployment record
- Use **Deployments → select deployment → Actions → Force Delete** to reconcile

---

## ABX Action Failing

```bash
# View ABX action execution logs via UI
# Extensibility → Actions → select action → Last Runs → view details

# Via API
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/abx/api/resources/action-runs?limit=10" | \
  jq '.content[] | {id: .id, status: .status, error: .errorMessage}'
```

Common ABX failures:

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Python dependency not listed in requirements | Add to the requirements field in the action definition |
| `Timeout` | Action ran longer than 5 minutes (default timeout) | Increase timeout in action settings; optimise the script |
| `Connection refused` | External endpoint not reachable from the ABX execution environment | Check network rules; use outbound proxy if required |
| `KeyError on inputs` | Required input not passed by the event broker | Check event broker subscription payload and input mapping |

---

## Authentication Failures (VIDM)

When users cannot log into Aria Automation:

```bash
# Verify VIDM health from Aria Automation appliance
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# Expected: {"status": "UP"}

# Check VIDM integration in VAMI
# VAMI (https://vra-prod-01.example.local:5480) → Services → Identity Provider
```

Common causes:
- VIDM certificate changed — update the trusted certificate in Aria Automation
- VIDM admin password rotated — re-register VIDM in VAMI
- AD connector in VIDM failed — check VIDM connector service and AD LDAPS connectivity

---

## Kubernetes Pod Failures

When a microservice pod is crash-looping:

```bash
# Identify failing pods
kubectl get pods --all-namespaces | grep -v "Running\|Completed"

# Get events for the failing pod
kubectl describe pod -n prelude <pod-name> | grep -A 20 "Events:"

# View pod logs (current and previous instance)
kubectl logs -n prelude <pod-name>
kubectl logs -n prelude <pod-name> --previous

# Restart a deployment (as last resort — pods should self-heal)
kubectl rollout restart deployment/<deployment-name> -n prelude
```

Persistent pod failures are typically caused by:
- Disk full on the appliance: `df -h` — check `/` and `/var`
- PostgreSQL database issues: check `kubectl logs -n prelude -l app=postgres`
- RabbitMQ queue overflow: check `kubectl logs -n prelude -l app=rabbitmq`
