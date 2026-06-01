# Aria Automation — Common Issues


<div class="kb-summary">
Common Issues reference covering Blueprint Validation Errors, Deployment Stuck in "Creating" or "Deleting", ABX Action Failing, Authentication Failures (VIDM), Kubernetes Pod Failures.
</div>

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
┌─────────────────────────────────── Aria Automation — Common Issues ───────────────────────────────────┐
│                                                                                                       │
│  Common vRA issues: failed requests, data collection errors, SSO failures, Orchestrator faults.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Provisioning Failures             │  │             Integration Failures            │   │
│   │       Network: NSX segment not created       │  │       vIDM SSO: cert mismatch/expired       │   │
│   │      Storage: no datastore match policy      │  │       Cloud acct: data collect failed       │   │
│   │      Quota exceeded: project limit hit       │  │      Orchestrator: endpoint unreachable     │   │
│   │      Template invalid: YAML syntax err       │  │       ABX timeout: action >5 min fails      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Check deployment events tab and pod logs for root cause before escalating.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Diagnostic Steps               │  │                 Quick Fixes                 │   │
│   │     Deployment events tab: error detail      │  │      YAML error: vRA template validator     │   │
│   │      kubectl logs <pod>: service error       │  │       SSO: re-import vIDM cert in VAMI      │   │
│   │      Cloud acct: check data collect log      │  │     Quota: increase or reassign project     │   │
│   │      vracli status: find failed service      │  │       ABX: increase timeout in action       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliance · kubectl (k3s) · Postgres · vIDM · NSX manager · vCenter                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Deployment events = vRA timeline of provisioning steps; shows which step and why it failed           │
│  Data collection   = vRA polling cloud endpoints; failure means stale or missing resource list        │
│  NSX segment fail  = vRA cannot create network; check NSX account connection and permissions          │
│  Storage policy    = Placement rule matching VM to datastore; fails if no datastore matches           │
│  Quota exceeded    = Project hit CPU/mem/count limit; admin must raise quota or delete unused         │
│  YAML validation   = vRA cloud template syntax check; run in template editor before publish           │
│  ABX timeout       = Default 5-minute action limit; increase for long-running tasks                   │
│  vIDM cert mismatch= TLS cert on vIDM does not match SAN expected by vRA; update VAMI                 │
│  Orch endpoint     = Aria Orchestrator endpoint registered in vRA; must be reachable on 443           │
│  Pod log           = kubectl logs <pod-name> -n prelude; per-microservice diagnostic output           │
│  vracli status     = Summary health; find which service is failing before diving into pods            │
│  Cloud acct log    = vRA data collection history; shows timestamps and errors per account             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```sql

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
