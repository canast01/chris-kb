---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Common Issues
![Aria Automation — Common Issues](../../../../assets/virtualization-vmware-aria-automation-troubleshooting-common.svg)

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

```bash
# View ABX action execution logs via UI
# Extensibility → Actions → select action → Last Runs → view details

# Via API
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/abx/api/resources/action-runs?limit=10" | \
  jq '.content[] | {id: .id, status: .status, error: .errorMessage}'
```
```bash
# Verify VIDM health from Aria Automation appliance
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# Expected: {"status": "UP"}

# Check VIDM integration in VAMI
# VAMI (https://vra-prod-01.example.local:5480) → Services → Identity Provider
```
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

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
B1: "Blueprint deployment failed" {shape: rectangle}
B2: "Cloud account unreachable" {shape: rectangle}
B3: "IPAM allocation error" {shape: rectangle}
B4: "Approval workflow stuck" {shape: rectangle}
B5: "Catalog item not visible" {shape: rectangle}
B6: "ABX action timeout" {shape: rectangle}
D1: "D1" {shape: rectangle}
R1: "Check NSX Segment Creation · Verify NSX Account Perms\n→ Provisioning Failures" {shape: rectangle}
R2: "Check Storage Policy Match · Datastore Capacity\n→ Provisioning Failures" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Trigger Manual Data Sync · Check Cloud Acct Log\n→ Integration Failures" {shape: rectangle}
R4: "Check vIDM SSO Cert · Re-import in VAMI\n→ Integration Failures" {shape: rectangle}
R5: "Check IPAM Endpoint Connectivity · Verify IP Pool Capacity\n→ Provisioning Failures" {shape: rectangle}
R6: "Check Approval Policy · Notify Approver · Check Orchestrator Endpoint\n→ Integration Failures" {shape: rectangle}
D3: "D3" {shape: rectangle}
R7: "Check Project and Catalog Sharing Settings\n→ Diagnostic Steps" {shape: rectangle}
R8: "Run Blueprint Validator · Fix Syntax Errors\n→ Diagnostic Steps" {shape: rectangle}
R9: "Increase ABX Action Timeout · Review Action Execution Logs\n→ Integration Failures" {shape: rectangle}

S -> B1
S -> B2
S -> B3
S -> B4
S -> B5
S -> B6
D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
B3 -> R5
B4 -> R6
D3 -> R7
D3 -> R8
B6 -> R9
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

---

## See also

- [Aria Automation — Diagnostics](../diagnostics/)
- [Aria Automation — Escalation](../escalation/)
- [Aria Automation — Health Checks](../../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
