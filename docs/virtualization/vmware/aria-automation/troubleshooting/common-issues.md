---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Common Issues

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
```text
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

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1[Blueprint deployment failed]
    S --> B2[Cloud account unreachable]
    S --> B3[IPAM allocation error]
    S --> B4[Approval workflow stuck]
    S --> B5[Catalog item not visible]
    S --> B6[ABX action timeout]

    B1 --> D1{Network or\nstorage failure?}
    D1 -->|Network| R1[Check NSX Segment Creation · Verify NSX Account Perms\n→ Provisioning Failures]
    D1 -->|Storage| R2[Check Storage Policy Match · Datastore Capacity\n→ Provisioning Failures]

    B2 --> D2{Data collection\nerror?}
    D2 -->|Yes| R3[Trigger Manual Data Sync · Check Cloud Acct Log\n→ Integration Failures]
    D2 -->|No| R4[Check vIDM SSO Cert · Re-import in VAMI\n→ Integration Failures]

    B3 --> R5[Check IPAM Endpoint Connectivity · Verify IP Pool Capacity\n→ Provisioning Failures]

    B4 --> R6[Check Approval Policy · Notify Approver · Check Orchestrator Endpoint\n→ Integration Failures]

    B5 --> D3{Entitlement or\nYAML error?}
    D3 -->|Entitlement| R7[Check Project and Catalog Sharing Settings\n→ Diagnostic Steps]
    D3 -->|YAML| R8[Run Blueprint Validator · Fix Syntax Errors\n→ Diagnostic Steps]

    B6 --> R9[Increase ABX Action Timeout · Review Action Execution Logs\n→ Integration Failures]

    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8,R9 section
    class D1,D2,D3 decision
    class S start
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

- [Aria Automation — Diagnostics](diagnostics/)
- [Aria Automation — Escalation](escalation/)
- [Aria Automation — Health Checks](../operations/health-checks/)

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
