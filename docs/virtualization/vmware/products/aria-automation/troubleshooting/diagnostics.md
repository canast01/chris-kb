---
tags:
  - aria-automation
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Aria Automation — Diagnostics

<div class="kb-summary">
Aria Automation diagnostic commands: query failed deployments and requests via REST API, inspect Kubernetes pod logs with kubectl, check PostgreSQL health, diagnose ABX action failures, and collect the LCM support bundle for VMware cases.

*Applies to: VMware Aria Automation 8.x (vRealize Automation)*
</div>
![Aria Automation — Diagnostics](../../../../../assets/virtualization-vmware-aria-automation-troubleshooting-diagno.svg)

```d2
direction: right

B: "B" {shape: rectangle}
C: "GET /deployment/api/deployments\nFilter by status=FAILED" {shape: rectangle}
D: "GET /catalog/api/requests\nFilter by requestState=FAILED" {shape: rectangle}
E: "vRA UI → Extensibility → Action Runs\nCheck stderr and error code" {shape: rectangle}
F: "kubectl logs -n prelude\nLook for Java exceptions" {shape: rectangle}
G: "Check vIDM connectivity\nGET /csp/gateway/am/api/login" {shape: rectangle}
H: "GET /deployment/api/deployments/id/events\nRead FAILED event message" {shape: rectangle}
I: "I" {shape: rectangle}
J: "Check vCenter Cloud Account\nvRA → Infrastructure → Cloud Accounts" {shape: rectangle}
K: "Validate blueprint YAML\nCheck resource property types" {shape: rectangle}
L: "Check IP range in vRA\nvRA → Infrastructure → Networks" {shape: rectangle}
M: "GET /catalog/api/requests/id/events\nRead error detail" {shape: rectangle}
N: "Check ABX action code\nVerify inputs and environment vars" {shape: rectangle}
O: "kubectl logs -n prelude pod-name --tail=200\nFilter for ERROR and Exception" {shape: rectangle}
P: "curl -sk vIDM-URL/SAAS/API/1.0/auth/token\nTest vIDM API" {shape: rectangle}
Q: "Collect support bundle\nLCM logscraper or VAMI bundle" {shape: rectangle}
R: "Open VMware SR\nmysupport.vmware.com" {shape: rectangle}
A: "Aria Automation Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
C -> H
I -> J
I -> K
I -> L
D -> M
E -> N
F -> O
G -> P
J -> Q
K -> Q
L -> Q
M -> Q
N -> Q
O -> Q
P -> Q
Q -> R
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_get_an_api_token: "Step 1 — Get an API token" {shape: rectangle}
step_2_check_failed_deployments: "Step 2 — Check failed deployments" {shape: rectangle}
step_3_check_catalog_request_status: "Step 3 — Check catalog request status" {shape: rectangle}
step_4_inspect_kubernetes_pod_logs: "Step 4 — Inspect Kubernetes pod logs" {shape: rectangle}
step_5_check_postgresql_database_hea: "Step 5 — Check PostgreSQL database health" {shape: rectangle}
step_6_check_abx_action_failures: "Step 6 — Check ABX action failures" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_get_an_api_token: investigate
symptom -> step_2_check_failed_deployments: investigate
symptom -> step_3_check_catalog_request_status: investigate
symptom -> step_4_inspect_kubernetes_pod_logs: investigate
symptom -> step_5_check_postgresql_database_hea: investigate
symptom -> step_6_check_abx_action_failures: investigate
step_1_get_an_api_token -> resolution
step_2_check_failed_deployments -> resolution
step_3_check_catalog_request_status -> resolution
step_4_inspect_kubernetes_pod_logs -> resolution
step_5_check_postgresql_database_hea -> resolution
step_6_check_abx_action_failures -> resolution
```

## Before you begin

- **Access:** vRA admin role; SSH to the vRA appliance(s); kubectl access (kubeconfig on the appliance at `/root/.kube/config`)
- **Gather first:** the deployment ID or catalog request ID, the error message shown in the vRA UI, the cloud account or endpoint involved, and whether the issue started after a version upgrade or configuration change
- **Scope:** confirm whether the issue affects one deployment, one blueprint, one cloud account, or all vRA requests
- **API auth:** get a Bearer token first — most diagnostic steps below require an authenticated API call

---

## Step 1 — Get an API token

```bash
# Authenticate to vRA via vIDM (standard method)
TOKEN=$(curl -sk -X POST "https://<vra-fqdn>/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"<admin-user>","password":"<password>","domain":"vsphere.local"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['cspAuthToken'])")

echo $TOKEN
# Expected: long JWT string; empty = auth failed

# Verify the token works
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/iaas/api/about" | python3 -m json.tool
# Expected: version info JSON with buildNumber and controllerVersion
```


```text title="Expected output"
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbkB2c3BoZXJlLmxvY2FsIiwiaWF0IjoxNjk4NzY1NDMyLCJleHAiOjE2OTg3NjkwMzIsImlzcyI6Imh0dHBzOi8vdnJhLWZxZG4uY29ycC5sb2NhbC9jc3AvZ2F0ZXdheSIsImF1ZCI6WyJjc3AiXX0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
{
  "buildNumber": "8.10.1.0-20231031",
  "controllerVersion": "8.10.1",
  "productName": "VMware Aria Automation",
  "releaseVersion": "8.10.1",
  "timestamp": "2023-10-31T14:23:45.123Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example; if error persists, verify vRA appliance certificate is valid).
    **`jq: error (at <stdin>:0): Cannot index object with string "cspAuthToken"`** — Verify credentials are correct and domain is set to `vsphere.local`; check vIDM is reachable and user account is not locked.
    **`curl: (7) Failed to connect to <vra-fqdn> port 443: Connection refused`** — Confirm vRA FQDN is correct and vRA appliance is running; check network connectivity and firewall rules allow port 443.
---

## Step 2 — Check failed deployments

```bash
# List all failed deployments
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments?status=FAILED" \
  | python3 -c "
import json,sys
data = json.load(sys.stdin)
for d in data.get('content', []):
    print(d['name'], '|', d['status'], '|', d.get('lastRequest', {}).get('completionDetails',''))
"

# Get full detail for a specific deployment
DEPLOY_ID="<deployment-id>"
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/$DEPLOY_ID" \
  | python3 -m json.tool

# Get deployment event log (full audit trail for what happened step by step)
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/$DEPLOY_ID/events" \
  | python3 -c "
import json,sys
for e in json.load(sys.stdin).get('content', []):
    print(e.get('timestamp',''), e.get('eventType',''), e.get('message','')[:120])
"

# Filter events to only FAILED type
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/deployment/api/deployments/$DEPLOY_ID/events?eventTypes=FAILED" \
  | python3 -m json.tool
```


```text title="Expected output"
web-app-prod | FAILED | Resource allocation timeout after 300 seconds
db-cluster-02 | FAILED | vSphere API connection refused on host esx-04.corp.local
legacy-app-test | FAILED | Blueprint validation failed: missing required input 'environment'

{
  "id": "deployment-a7f3c2e1-9b4d-4f8a-b2d1-5e8c9a3f7d2b",
  "name": "web-app-prod",
  "status": "FAILED",
  "createdAt": "2024-01-15T14:32:18.000Z",
  "lastRequest": {
    "id": "request-b8e4d3f2-0c5e-5g9b-c3e2-6f9d0b4g8e3c",
    "status": "FAILED",
    "completionDetails": "Resource allocation timeout after 300 seconds",
    "completedAt": "2024-01-15T14:37:22.000Z"
  },
  "inputs": {
    "environment": "production",
    "cpu_count": 4,
    "memory_gb": 16
  }
}

2024-01-15T14:32:18.123Z DEPLOYMENT_REQUESTED Deployment request submitted by admin@corp.local
2024-01-15T14:32:25.456Z RESOURCE_ALLOCATION_STARTED Attempting to allocate 4 vCPU and 16GB memory from cluster-prod
2024-01-15T14:35:10.789Z RESOURCE_ALLOCATION_FAILED vSphere cluster-prod returned error: insufficient free memory on hosts
2024-01-15T14:35:11.012Z DEPLOYMENT_FAILED Deployment failed due to resource constraints; check vSphere capacity

{
  "content": [
    {
      "timestamp": "2024-01-15T14:35:10.789Z",
      "eventType": "FAILED",
      "message": "vSphere cluster-prod returned error: insufficient free memory on hosts esx-01, esx-02, esx-03",
      "severity": "ERROR"
    }
  ],
  "totalElements": 1
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the VRA certificate into your system CA bundle.
    **`jq: command not found`** — Install python3-json or use `python3 -m json.tool` instead of piping to jq for JSON formatting.
    **`Authorization: Bearer $TOKEN: command not found`** — Ensure `$TOKEN` variable is set by running `TOKEN=$(curl -sk -u admin:password "https://<vra-fqdn>/iaas/api/login" | grep -o '"token":"[^"]*' | cut -d'"' -f4)` first.
---

## Step 3 — Check catalog request status

```bash
# List failed catalog requests
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests?requestState=FAILED&size=20" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin).get('content', []):
    print(r.get('id','')[:8], '|', r.get('requestedByDisplay',''), '|', r.get('reason',''))
"

# Get full detail for a specific request
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests/<request-id>" \
  | python3 -m json.tool

# Get request event log
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/catalog/api/requests/<request-id>/events" \
  | python3 -m json.tool
```


```text title="Expected output"
a7f2c1e4 | john.smith@corp.local | Insufficient vSphere cluster resources
b3e9d2f1 | sarah.jones@corp.local | Network policy violation detected
c5a1b8e7 | mike.brown@corp.local | Storage quota exceeded for project-prod
d9f4c2a6 | lisa.wang@corp.local | Blueprint validation failed: missing required input
e2b7f5d3 | admin@corp.local | vCenter connection timeout

{
  "id": "a7f2c1e4-9b3c-4d2e-8f1a-7c5e2b9d4a1f",
  "requestedByDisplay": "john.smith@corp.local",
  "requestState": "FAILED",
  "reason": "Insufficient vSphere cluster resources",
  "requestedOn": 1698765432000,
  "completedOn": 1698765892000,
  "blueprint": "CentOS-8-Standard",
  "catalogItemId": "5f2a8c1b-3e4d-9f7a-2c1b-8e5d3a9f2c1b"
}

{
  "content": [
    {
      "eventType": "REQUEST_FAILED",
      "message": "vSphere cluster 'prod-cluster-01' has insufficient CPU resources",
      "timestamp": 1698765892000
    },
    {
      "eventType": "RESOURCE_ALLOCATION_ERROR",
      "message": "Requested 8 vCPU but only 2 available",
      "timestamp": 1698765891000
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip SSL verification, or import the VRA certificate into your system's trusted CA store.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Verify the `$TOKEN` variable is set correctly with a valid bearer token and the VRA API endpoint is reachable.
    **`"reason": ""`** — Check the request events endpoint for detailed error messages, as some failures only populate the event log rather than the reason field.
---

## Step 4 — Inspect Kubernetes pod logs

```bash
# SSH to the vRA appliance
ssh root@<vra-appliance-ip>

# List all pods in the vRA namespace (all should be Running)
kubectl get pods -n prelude
# Problem: any pod in CrashLoopBackOff, Error, or Pending state

# Get logs for a specific failing pod
kubectl logs -n prelude <pod-name> --tail=200

# Follow logs in real time for a pod (Ctrl-C to stop)
kubectl logs -n prelude <pod-name> -f

# Get logs from all containers in a pod (for multi-container pods)
kubectl logs -n prelude <pod-name> --all-containers

# Filter for errors across all pods (runs kubectl exec or log aggregation)
kubectl logs -n prelude --selector app=catalog --tail=100 2>&1 | grep -i "error\|exception\|fail"

# Describe a pod in CrashLoopBackOff to get exit reason
kubectl describe pod -n prelude <pod-name>
# Look for: "Last State", "Reason", "Exit Code" in the output

# Check all pod resource consumption
kubectl top pods -n prelude 2>/dev/null || echo "metrics-server not available"
```


```text title="Expected output"
root@vra-appliance-01:~# kubectl get pods -n prelude
NAME                                    READY   STATUS    RESTARTS   AGE
catalog-service-7d4f8c9b2-kx9m2         1/1     Running   0          14d
identity-service-5b2c1a8f-9qr3p         1/1     Running   2          14d
orchestration-engine-6f8e2d5c-lmn7x     0/1     CrashLoopBackOff   12   2h
request-service-8a3b9e1f-pq2rs          1/1     Running   0          14d
approval-service-4c7d6b2e-uvwxy         1/1     Running   1          14d
...

root@vra-appliance-01:~# kubectl logs -n prelude orchestration-engine-6f8e2d5c-lmn7x --tail=200
2024-01-15T09:42:31.847Z ERROR [main] Failed to connect to database: Connection refused (localhost:5432)
2024-01-15T09:42:32.102Z ERROR [main] Retrying connection attempt 3/10
2024-01-15T09:42:35.456Z ERROR [main] Max retries exceeded, shutting down
Exception in thread "main" java.sql.SQLException: Cannot get a connection, pool error Timeout waiting for idle object

root@vra-appliance-01:~# kubectl describe pod -n prelude orchestration-engine-6f8e2d5c-lmn7x
Name:         orchestration-engine-6f8e2d5c-lmn7x
Namespace:    prelude
Status:       Running
Last State:     Terminated
  Reason:       ExitCode 1
  Exit Code:    1
  Started:      Mon, 15 Jan 2024 09:44:15Z
  Finished:     Mon, 15 Jan 2024 09:44:18Z
Restart Count:  12

root@vra-appliance-01:~# kubectl top pods -n prelude 2>/dev/null || echo "metrics-server not available"
NAME                                    CPU(m)   MEMORY(Mi)
catalog-service-7d4f8c9b2-kx9m2         145      512
identity-service-5b2c1a8f-9qr3p         89       384
request-service-8a3b9e1f-pq2rs          201      768
approval-service-4c7d6b2e-uvwxy         67       256
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pods"`** — Verify kubectl is configured correctly and you have access to the cluster with `kubectl cluster-info`.
    **`Unable to connect to the server: dial tcp: lookup <vra-appliance-ip>: no such host`** — Ensure the vRA appliance IP is correct and reachable, or use the FQDN instead of IP address.
    **`Error from server (NotFound): pods "<pod-name>" not found`** — Confirm the pod name is spelled correctly and exists in the prelude namespace with `kubectl get pods -n prelude`.
---

## Step 5 — Check PostgreSQL database health

```bash
# On the vRA appliance — connect to the Postgres database
psql -U postgres

# Check replication lag (if clustered vRA)
\c vcac
SELECT client_addr, state, sent_lsn, replay_lsn,
       (sent_lsn - replay_lsn) AS lag_bytes
FROM pg_stat_replication;

# Check for table bloat (dead tuples)
SELECT relname, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC LIMIT 20;

# Manually vacuum if autovacuum hasn't run
VACUUM ANALYZE public.*;

# Exit psql
\q
```


```text title="Expected output"
psql (12.13 (Debian 12.13-1.pgdg110+1))
Type "help" for help.

postgres=# \c vcac
You are now connected to database "vcac" as user "postgres".
vcac=# SELECT client_addr, state, sent_lsn, replay_lsn,
       (sent_lsn - replay_lsn) AS lag_bytes
FROM pg_stat_replication;
 client_addr |   state   |  sent_lsn  | replay_lsn | lag_bytes
-------------+-----------+------------+------------+-----------
 10.42.18.55 | streaming | 0/4A2B1F80 | 0/4A2B1F80 |         0
 10.42.18.56 | streaming | 0/4A2B1F80 | 0/4A2B1C00 |      1920
(2 rows)

vcac=# SELECT relname, n_dead_tup, last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC LIMIT 20;
       relname       | n_dead_tup |       last_autovacuum
---------------------+------------+------------------------
 request_state_log   |      87432 | 2024-01-15 03:22:14+00
 resource_action     |      34156 | 2024-01-15 02:18:07+00
 deployment_resource |      12847 | 2024-01-14 18:45:33+00
(3 rows)

vcac=# VACUUM ANALYZE public.*;
VACUUM
vcac=# \q
```

!!! warning "Common errors"
    **`psql: error: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL: Ident authentication failed for user "postgres"`** — Run the psql command directly on the vRA appliance or configure pg_hba.conf to allow password authentication.
    **`ERROR: permission denied for schema public`** — Connect as the vcac database owner instead: `psql -U vcac -d vcac` or grant appropriate privileges to the postgres user.
---

## Step 6 — Check ABX action failures

```bash
# Via vRA UI (most informative for ABX):
# Navigate to: Extensibility → Action Runs
# Filter by: Status = Failed; sort by Most Recent
# Click on a failed run → View Logs
# Look at: stdout, stderr, exit code, and inputs passed to the action

# Via API — list recent ABX action runs
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/abx/api/resources/action-runs?page=0&size=20&status=FAILED" \
  | python3 -c "
import json,sys
for r in json.load(sys.stdin).get('content', []):
    print(r.get('name',''), '|', r.get('status',''), '|', r.get('error','')[:100])
"

# Get detail for a specific action run
curl -sk -H "Authorization: Bearer $TOKEN" \
  "https://<vra-fqdn>/abx/api/resources/action-runs/<run-id>" \
  | python3 -m json.tool
```


```text title="Expected output"
my-provision-action | FAILED | Error: Timeout waiting for resource allocation after 300s
update-network-config | FAILED | NullPointerException in line 42: cannot read property 'ipAddress' of undefined
cleanup-vm-snapshot | FAILED | Permission denied: user lacks 'abx.action.execute' role
post-deployment-webhook | FAILED | Connection refused to https://webhook.example.com:8443

{
  "id": "run-12a4f8c9-3e2b-47d1-9f6a-2c8e5b1d4a7f",
  "name": "my-provision-action",
  "status": "FAILED",
  "createdAt": "2024-01-15T14:32:18.456Z",
  "completedAt": "2024-01-15T14:33:52.891Z",
  "actionId": "action-5c3b2a1f-8e9d-4c7b-a2f1-9d8c7b6a5e4f",
  "error": "Timeout waiting for resource allocation after 300s",
  "stdout": "Starting provisioning workflow...\nValidating input parameters...\nInitiating vSphere API call...",
  "stderr": "WARNING: Deprecated API endpoint used\nERROR: Timeout after 300000ms",
  "exitCode": 1,
  "inputs": {
    "cpuCount": 4,
    "memoryMB": 8192,
    "templateName": "ubuntu-20.04-base"
  }
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification, or import the vRA root CA into your system trust store.
    **`jq: command not found`** — Install `jq` with `apt-get install jq` or `yum install jq`, or use the Python JSON parser shown in the example instead.
    **`Authorization: Bearer $TOKEN: command not found`** — Ensure `$TOKEN` is set by running `TOKEN=$(curl -sk ... /api/login)` first, or use explicit token value in quotes.
---

## Step 7 — Collect support bundle

```bash
# Via LCM logscraper (recommended for full Aria Suite diagnostics)
# Navigate to: vRSLCM UI → Support → Logscraper
# Select: Aria Automation; time range; Generate Bundle
# Download the .zip file and attach to VMware SR

# Via VAMI (vRA appliance-level bundle)
# Browse to: https://<vra-appliance-ip>:5480
# Navigate to: Support → Generate Support Bundle
# Wait 5–15 minutes; download .gz file

# Via appliance CLI
ssh root@<vra-appliance-ip>
# Support bundle for vRA:
/var/log/vmware/vra/support-bundle.sh
# Output: /tmp/vra-support-<timestamp>.tar.gz

# Include in the VMware SR:
# - LCM logscraper bundle or VAMI bundle
# - Deployment ID or request ID that failed
# - vRA version: vRA UI → Administration → About
# - Timeline of the issue and any recent changes
```


```text title="Expected output"
root@vra-appliance-01:~# /var/log/vmware/vra/support-bundle.sh
Generating Aria Automation support bundle...
Collecting system logs...
Collecting vRA application logs...
Collecting database diagnostics...
Collecting network configuration...
Collecting certificate information...
Bundle generation in progress: [████████████████████] 100%
Support bundle created successfully.
Output file: /tmp/vra-support-20240115-143022.tar.gz
Bundle size: 487 MB
Timestamp: 2024-01-15 14:30:22 UTC
root@vra-appliance-01:~#
```

!!! warning "Common errors"
    **`/var/log/vmware/vra/support-bundle.sh: Permission denied`** — Run the command with `sudo` or ensure you are logged in as root user.
    **`/tmp: No space left on device`** — Free up disk space on the appliance (check with `df -h`) or specify an alternate output directory before running the script.
    **`support-bundle.sh: command not found`** — Verify the vRA appliance is fully deployed and the support tools are installed; check `/var/log/vmware/vra/` exists with `ls -la /var/log/vmware/vra/`.
---

## Log locations

| Component | Path / Command | What to look for |
|---|---|---|
| vRA micro-services | `kubectl logs -n prelude <pod-name>` | Java exceptions, API 500 errors |
| Appliance system | `/var/log/vmware/vra/` | Service startup failures |
| vRA cluster service | `journalctl -u vra-cluster -n 500` | Cluster join and startup events |
| ABX runs | vRA UI → Extensibility → Action Runs | ABX stderr, exit code, inputs |
| PostgreSQL | psql → `pg_stat_replication`, `pg_stat_user_tables` | Replication lag, dead tuples |

---

## See also

- [Aria Automation — Common Issues](../common-issues/)
- [Aria Automation — Escalation](../escalation/)

## Verify resolution

- `kubectl get pods -n prelude` shows all pods in `Running` state with no restarts in the last hour
- Trigger a test deployment of a simple blueprint — confirm it reaches `DEPLOYMENT_SUCCESSFUL` state
- `GET /deployment/api/deployments?status=FAILED` shows no new failures after the fix
- ABX test run completes with exit code 0 and expected output in Action Runs
