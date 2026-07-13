---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Common Issues

*Applies to: VMware Aria 8.x*
![Aria Automation — Common Issues](../../../../../assets/virtualization-vmware-aria-automation-troubleshooting-common.svg)

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


```text title="Expected output"
{
  "valid": true,
  "errors": [],
  "warnings": [
    "Resource 'Cloud_vSphere_Machine' uses deprecated property 'cpuCount'; migrate to 'cpuCores'"
  ],
  "blueprintId": "d4c8f2a1-7b3e-4f9c-a2d1-8e5c3b9f1a2d",
  "validationTime": "2024-01-15T09:42:33.847Z"
}
YAML OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl command (already present) or import the vRA server's CA certificate into your system trust store. |
    | `jq: parse error: Invalid JSON text at line 1` | Verify the API response is valid JSON by testing the endpoint directly with `curl -sk ... | head -c 500` to check for HTML error pages or authentication failures. |
    | `FileNotFoundError: [Errno 2] No such file or directory: 'blueprint.yaml'` | Ensure you are in the correct working directory and the blueprint.yaml file exists with `ls -la blueprint.yaml`. |
```bash
# View ABX action execution logs via UI
# Extensibility → Actions → select action → Last Runs → view details

# Via API
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://vra-prod-01.example.local/abx/api/resources/action-runs?limit=10" | \
  jq '.content[] | {id: .id, status: .status, error: .errorMessage}'
```

```text title="Expected output"
{
  "id": "action-run-8f4a2c91-7e3b-4d6f-a1b2-9c5e3d7f2a1b",
  "status": "FAILED",
  "error": "Timeout waiting for external service response after 30s"
}
{
  "id": "action-run-7d3b1c9a-5e2f-4a8c-b9d1-2e6f3c8a1d5b",
  "status": "COMPLETED",
  "error": null
}
{
  "id": "action-run-6c2a0b8f-4d1e-3f9b-a8c0-1d5e2b7a0c4a",
  "status": "FAILED",
  "error": "Authentication failed: invalid credentials for target system"
}
{
  "id": "action-run-5b1a9a7e-3c0d-2e8a-97bf-0c4d1a6b9f3a",
  "status": "COMPLETED",
  "error": null
}
{
  "id": "action-run-4a0a8a6d-2b9c-1d7a-86ae-9b3c0a5a8e2a",
  "status": "IN_PROGRESS",
  "error": null
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to skip certificate verification, or import the vRA certificate into your system's trusted store. |
    | `jq: parse error: Unexpected end of JSON input` | Verify the `$TOKEN` variable is set correctly with `echo $TOKEN` and ensure the vRA API endpoint is responding with valid JSON. |
    | `"error": "Unauthorized"` | Regenerate the API token in vRA under Administration → API tokens and ensure it has the appropriate ABX action read permissions. |
```bash
# Verify VIDM health from Aria Automation appliance
curl -sk https://vidm.example.local/SAAS/API/1.0/REST/system/health
# Expected: {"status": "UP"}

# Check VIDM integration in VAMI
# VAMI (https://vra-prod-01.example.local:5480) → Services → Identity Provider
```

```text title="Expected output"
{"status":"UP","timestamp":"2024-01-15T09:47:32.123Z","components":{"database":"UP","cache":"UP","ldap":"UP"},"version":"8.10.2.1234"}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add the `-k` flag to skip certificate verification, or import the VIDM certificate into your system's trusted store. |
    | `curl: (7) Failed to connect to vidm.example.local port 443: Connection refused` | Verify VIDM is running and accessible on the network; check firewall rules and DNS resolution with `nslookup vidm.example.local`. |
    | `{"status":"DOWN","components":{"database":"DOWN"}}` | Restart the VIDM database service or check VIDM logs at `/var/log/vidm/` for underlying service failures. |
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
R5: "Check IPAM Endpoint Connectivity · Verify IP Pool\nCapacity\n→ Provisioning Failures" {shape: rectangle}
R6: "Check Approval Policy · Notify Approver · Check\nOrchestrator Endpoint\n→ Integration Failures" {shape: rectangle}
D3: "D3" {shape: rectangle}
R7: "Check Project and Catalog Sharing Settings\n→ Diagnostic Steps" {shape: rectangle}
R8: "Run Blueprint Validator · Fix Syntax Errors\n→ Diagnostic Steps" {shape: rectangle}
R9: "Increase ABX Action Timeout · Review Action\nExecution Logs\n→ Integration Failures" {shape: rectangle}

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
