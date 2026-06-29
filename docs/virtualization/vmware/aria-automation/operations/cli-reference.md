---
tags:
  - aria-automation
  - operations
  - cli
  - vracli
  - kubectl
  - vmware
---
# Aria Automation — CLI Reference

<div class="kb-summary">
Complete CLI reference for Aria Automation: vracli appliance management, kubectl microservice diagnostics, REST API authentication and resource operations, PowerVRA PowerShell module, Aria Orchestrator admin, and VAMI management.

*Applies to: Aria Automation 8.x*
</div>
![Aria Automation — CLI Reference](../../../../assets/virtualization-vmware-aria-automation-operations-cli-referen.svg)

## Before you begin

- **Access:** SSH to vRA appliance as `root`; REST API requires an Aria Automation admin account
- **kubectl:** available on the vRA appliance at `/usr/local/bin/kubectl` — no separate install needed
- **Token lifetime:** REST API bearer tokens expire after 8 hours; re-authenticate if commands return 401

---

## vracli — Appliance Management

`vracli` is installed on every Aria Automation appliance and manages appliance-level configuration.

### Status and Health

```bash
# Full health check — shows green/red per service
vracli status

# Detailed per-service status
vracli status --all

# Check version of vRA and all components
vracli version

# Wait for all services to become healthy (useful after reboot)
vracli status --wait
```


```text title="Expected output"
Service Status:
  vRA Portal                    [  OK  ]
  vRA Orchestrator              [  OK  ]
  vRA IaaS                       [  OK  ]
  vRA Catalog                    [  OK  ]
  PostgreSQL Database            [  OK  ]
  RabbitMQ Message Bus           [  OK  ]
  vRA Configuration              [  OK  ]

Service Status (Detailed):
  vRA Portal                    [  OK  ] - Running (PID: 4521, Memory: 1.2GB)
  vRA Orchestrator              [  OK  ] - Running (PID: 4389, Memory: 2.8GB)
  vRA IaaS                       [  OK  ] - Running (PID: 4156, Memory: 1.9GB)
  vRA Catalog                    [  OK  ] - Running (PID: 4712, Memory: 856MB)
  PostgreSQL Database            [  OK  ] - Running (PID: 3891, Memory: 3.4GB)
  RabbitMQ Message Bus           [  OK  ] - Running (PID: 3756, Memory: 512MB)
  vRA Configuration              [  OK  ] - Running (PID: 4023, Memory: 287MB)

VMware Aria Automation Version Information:
  vRA Core Version:             8.13.2.0
  vRA Orchestrator:             8.13.2.0
  vRA IaaS:                     8.13.2.0
  PostgreSQL:                   13.11
  RabbitMQ:                     3.11.8
  Build Number:                 22348901
  Release Date:                 2024-01-15

Waiting for all services to become healthy...
[████████████████████████████] 100% - All services healthy (elapsed: 47s)
```

!!! warning "Common errors"
    **`vracli: command not found`** — Ensure vRA is installed and `/opt/vmware/vra/bin` is in your PATH, or use the full path `/opt/vmware/vra/bin/vracli`.
    **`Error: Unable to connect to vRA service on localhost:5480`** — Verify vRA services are running with `systemctl status vra-*` and check network connectivity to the appliance.
    **`Timeout waiting for services after 300 seconds`** — Increase the wait timeout with `vracli status --wait --timeout 600` or investigate hung services with `vracli logs --service <service-name>`.
### Certificate Management

```bash
# Show current certificate info
vracli certificate ingress --show

# Generate a CSR for a custom certificate
vracli certificate ingress --generate --cn "vra.corp.local" \
  --org "Corp" --country "US"

# Import a signed certificate (PEM format)
vracli certificate ingress --import --certificate /tmp/vra.crt \
  --private-key /tmp/vra.key \
  --ca-cert /tmp/ca-chain.crt

# Trust an external CA certificate (for external vIDM, LDAP with TLS)
vracli certificate trust add /tmp/external-ca.crt
vracli certificate trust list
```


```text title="Expected output"
Current Certificate Information:
  Subject: CN=vra.corp.local, O=Corp, C=US
  Issuer: CN=vra.corp.local, O=Corp, C=US
  Valid From: 2024-01-15T10:23:45Z
  Valid Until: 2025-01-15T10:23:45Z
  Thumbprint: A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0

Certificate Signing Request generated successfully.
CSR saved to: /tmp/vra.csr
CN: vra.corp.local
Organization: Corp
Country: US

Certificate imported successfully.
Certificate chain validated.
Ingress certificate updated.
Service restart scheduled.

Trusted CA certificate added: external-ca.crt
Thumbprint: F9E8D7C6B5A4Z3Y2X1W0V9U8T7S6R5Q4P3O2N1M0

Trusted Certificates:
  1. external-ca.crt (Thumbprint: F9E8D7C6B5A4Z3Y2X1W0V9U8T7S6R5Q4P3O2N1M0)
  2. internal-root-ca.crt (Thumbprint: 1A2B3C4D5E6F7G8H9I0J1K2L3M4N5O6P7Q8R9S0)
```

!!! warning "Common errors"
    **`Error: Certificate file not found: /tmp/vra.crt`** — Verify the certificate file path exists and is readable with `ls -la /tmp/vra.crt`.
    **`Error: Private key validation failed - key does not match certificate`** — Ensure the private key and certificate were generated as a pair and use the correct files.
    **`Error: Certificate chain validation failed - untrusted root CA`** — Add the root CA certificate to the trust store first using `vracli certificate trust add` before importing the signed certificate.
### vIDM (Identity) Configuration

```bash
# Show current vIDM / identity source config
vracli vidm

# Configure external vIDM connection
vracli vidm config --host vidm.corp.local \
  --admin-user admin@vidm.local \
  --admin-password <pass>

# Re-sync vIDM groups
vracli vidm refresh
```


```text title="Expected output"
Current vIDM Configuration:
  Host: vidm.corp.local
  Admin User: admin@vidm.local
  Status: Connected
  Last Sync: 2024-01-15 14:32:18 UTC
  Synced Groups: 847
  Synced Users: 3,421

Configuring vIDM connection to vidm.corp.local...
✓ Connection test successful
✓ Admin credentials validated
✓ Configuration saved to /etc/vra/vidm-config.json
Configuration complete.

Refreshing vIDM groups and users...
✓ Sync started (Job ID: sync-2024-01-15-143645)
✓ Fetched 847 groups
✓ Fetched 3,421 users
✓ Updated 12 group memberships
Sync completed successfully in 45 seconds.
```

!!! warning "Common errors"
    **`Error: Unable to connect to vidm.corp.local:443 — Connection refused`** — Verify the vIDM host is reachable and the HTTPS port is open using `ping vidm.corp.local` and `telnet vidm.corp.local 443`.
    **`Error: Authentication failed for admin@vidm.local — Invalid credentials`** — Confirm the admin password is correct and the account has not been locked by running a manual login test against vIDM.
    **`Error: vracli: command not found`** — Ensure you are running this command on an Aria Automation appliance with vracli installed, or source the environment with `source /etc/profile.d/vra-cli.sh`.
### Proxy and Network

```bash
# Show current proxy configuration
vracli proxy

# Set HTTP proxy for outbound connections (cloud account sync, extension repo)
vracli proxy set --http "http://proxy.corp.local:8080" \
                 --https "http://proxy.corp.local:8080" \
                 --no-proxy "localhost,127.0.0.1,.corp.local"

# Remove proxy
vracli proxy clear

# Show NTP config
vracli ntp

# Set NTP servers
vracli ntp set --servers "ntp1.corp.local,ntp2.corp.local"
```


```text title="Expected output"
Current proxy configuration:
  HTTP Proxy: Not configured
  HTTPS Proxy: Not configured
  No Proxy: Not configured

Proxy configuration updated successfully.
HTTP Proxy: http://proxy.corp.local:8080
HTTPS Proxy: http://proxy.corp.local:8080
No Proxy: localhost,127.0.0.1,.corp.local

Proxy configuration cleared successfully.

Current NTP configuration:
  NTP Servers: 0.pool.ntp.org, 1.pool.ntp.org
  NTP Status: synchronized
  Last sync: 2024-01-15 14:32:18 UTC

NTP servers updated successfully.
NTP Servers: ntp1.corp.local, ntp2.corp.local
Configuration will take effect after service restart.
```

!!! warning "Common errors"
    **`Error: Invalid proxy URL format. Expected http:// or https://`** — Ensure the proxy URL includes the protocol scheme (http:// or https://) and valid hostname.
    **`Error: Unable to resolve NTP server 'ntp1.corp.local': Name or service not known`** — Verify NTP server hostnames are resolvable from the Aria Automation appliance and reachable on port 123.
    **`Error: vracli command not found`** — Ensure you are logged into the Aria Automation appliance via SSH or execute the command from the appliance's shell environment.
### Cluster Management (3-Node HA)

```bash
# Show cluster node status
vracli cluster status

# Add a second/third node to form HA cluster
vracli cluster join --master-node <master-ip> --join-token <token>

# Get join token from master node
vracli cluster token
```


```text title="Expected output"
Cluster Status:
  Node Name: vra-master-01.corp.local
  Node IP: 192.168.1.45
  Cluster Status: HEALTHY
  Node Status: LEADER
  Etcd Status: healthy
  Cluster Size: 1
  Last Heartbeat: 2024-01-15T14:32:18Z

Join Token Generated:
  Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJub2RlX2lkIjoiYjQ3ZjNhMmMtOWQxYi00ZTk4LWI5ZjItMzJhYzU1ZGY4YzFhIiwiZXhwaXJlc19hdCI6IjIwMjQtMDEtMTVUMTU6MzI6MThafQ.x4kJ9mL2pQrS8vN3wXyZ1aB5cD7eF9gH
  Expires: 2024-01-15T15:32:18Z
  Master Node: 192.168.1.45

Node vra-node-02 joining cluster:
  Status: IN_PROGRESS
  Progress: 85%
  Syncing etcd data...
```

!!! warning "Common errors"
    **`error: cluster join failed: invalid token or token expired`** — Regenerate a new token on the master node using `vracli cluster token` as tokens expire after one hour.
    **`error: unable to reach master node at <ip>: connection refused`** — Verify network connectivity and that the master node's vRA services are running with `vracli service status` on the master.
    **`error: node already part of a cluster`** — Reset the node to standalone state first by running `vracli cluster reset --force` before attempting to join a different cluster.
---

## kubectl — Kubernetes Diagnostics

All vRA microservices run as pods in the `prelude` Kubernetes namespace inside the appliance.

### Pod Status

```bash
# List all pods — healthy pods show Running/Completed, not CrashLoopBackOff/Error
kubectl get pods -n prelude

# Get detailed info on a failing pod (shows events and resource limits)
kubectl describe pod <pod-name> -n prelude

# Show pods with resource usage
kubectl top pods -n prelude
```


```text title="Expected output"
NAME                                    READY   STATUS    RESTARTS   AGE
aria-automation-api-7d4c9f2b1-kx9m2    1/1     Running   0          14d
aria-automation-ui-5b8e3a9c-jk2l4      1/1     Running   2          8d
aria-automation-db-init-job-abc123      0/1     Completed 0          12d
aria-automation-worker-2f6e8a1d-pq5r9  1/1     Running   0          3d
metrics-server-7c4d9b2e-mn8o3          1/1     Running   1          21d
aria-automation-cache-9k3l2m5n-vw6x7   0/1     CrashLoopBackOff 5   2h

NAME                                CPU(m)   MEMORY(Mi)
aria-automation-api-7d4c9f2b1-kx9m2    245      512
aria-automation-ui-5b8e3a9c-jk2l4      189      384
aria-automation-worker-2f6e8a1d-pq5r9  412      768
metrics-server-7c4d9b2e-mn8o3          78       156
aria-automation-cache-9k3l2m5n-vw6x7   0        0
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pods"`** — Verify the cluster context is set correctly with `kubectl config current-context` and the API server is accessible.
    **`error: metrics not available yet`** — Wait 1-2 minutes for metrics-server to initialize, then retry `kubectl top pods`.
    **`No resources found in namespace "prelude"`** — Confirm the namespace exists with `kubectl get namespaces` and Aria Automation is deployed in the correct namespace.
### Logs

```bash
# Stream logs for a specific pod
kubectl logs -f <pod-name> -n prelude

# Logs for a specific container within a pod
kubectl logs <pod-name> -c <container-name> -n prelude

# Previous container logs (if pod restarted — shows why it crashed)
kubectl logs --previous <pod-name> -n prelude

# Common pods to check on failures:
#   catalog-service      → catalog and request issues
#   provisioning         → deployment provisioning failures
#   event-broker         → subscription/notification issues
#   blueprint-api        → template and blueprint issues
#   abx-adapter          → ABX extensibility action issues
```


```text title="Expected output"
2024-01-15T14:32:18.456Z INFO [catalog-service] Starting catalog synchronization cycle
2024-01-15T14:32:19.123Z DEBUG [catalog-service] Fetched 47 items from vSphere endpoint
2024-01-15T14:32:20.789Z INFO [catalog-service] Catalog sync completed successfully in 1.2s
2024-01-15T14:32:21.045Z INFO [catalog-service] Publishing 12 new catalog items to message broker
2024-01-15T14:32:22.567Z DEBUG [catalog-service] Item ID: 8f4a2c91-7e3d-4b9a-a1c2-5d8e9f3b2a1c published
2024-01-15T14:32:23.890Z INFO [catalog-service] Catalog update cycle complete
```

!!! warning "Common errors"
    **`Error from server (NotFound): pods "<pod-name>" not found`** — Verify the pod name with `kubectl get pods -n prelude` and ensure you're querying the correct namespace.
    **`error: a container name must be specified for pod <pod-name>, choose one of: [catalog-service init-config]`** — Use `kubectl get pods <pod-name> -n prelude -o jsonpath='{.spec.containers[*].name}'` to list available containers and specify the correct one with `-c`.
    **`error: previous terminated container "<container-name>" in pod "<pod-name>" not found`** — The pod has not restarted yet; use regular `kubectl logs` without `--previous` to view current logs instead.
### Service and Config

```bash
# List all services
kubectl get svc -n prelude

# List config maps
kubectl get configmap -n prelude

# Get a specific config map
kubectl get configmap <name> -n prelude -o yaml

# Restart a pod (delete it — Kubernetes re-creates it automatically)
kubectl delete pod <pod-name> -n prelude
# ⚠ Only delete one pod at a time; do not delete multiple simultaneously
```


```text title="Expected output"
NAME                                TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
aria-automation-api                 ClusterIP   10.96.45.123     <none>        8080/TCP          45d
aria-automation-ui                  ClusterIP   10.96.67.89      <none>        443/TCP           45d
postgres-service                    ClusterIP   10.96.102.15     <none>        5432/TCP          45d
redis-cache                         ClusterIP   10.96.201.44     <none>        6379/TCP          45d
nginx-ingress-controller            LoadBalancer 10.96.12.78     192.168.1.50  80:30080/TCP,...  42d

NAME                           DATA   AGE
aria-automation-config         8      45d
aria-automation-secrets        5      45d
postgres-init-script           1      45d
nginx-config                   3      42d

apiVersion: v1
kind: ConfigMap
metadata:
  name: aria-automation-config
  namespace: prelude
data:
  api.properties: |
    server.port=8080
    database.url=jdbc:postgresql://postgres-service:5432/aria
  log.level: INFO
  max.connections: "100"

pod "aria-automation-api-7d4f9c2b1" deleted
```

!!! warning "Common errors"
    **`Error from server (NotFound): configmaps "<name>" not found`** — Verify the ConfigMap name with `kubectl get configmap -n prelude` and use the exact name from the NAME column.
    **`error: resource name may not be empty`** — Replace `<name>` and `<pod-name>` placeholders with actual resource names; do not run the command with angle brackets.
    **`Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:prelude:default" cannot delete resource "pods"`** — Ensure your kubectl user has sufficient RBAC permissions; contact your cluster administrator to grant `pods/delete` verb.
---

## REST API — Authentication and Token

All REST operations require a bearer token obtained from the identity service.

```bash
# Authenticate and get a token (store in TOKEN variable)
TOKEN=$(curl -s -X POST \
  "https://<aria-auto>/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"<pass>","domain":"System Domain"}' \
  | jq -r '.cspAuthToken')

echo "Token: ${TOKEN:0:20}..."

# Helper function — use in scripts
get_token() {
  curl -s -X POST \
    "https://${VRA_HOST}/csp/gateway/am/api/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"${VRA_USER}\",\"password\":\"${VRA_PASS}\",\"domain\":\"System Domain\"}" \
    | jq -r '.cspAuthToken'
}
```


```text title="Expected output"
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <aria-auto> port 443: Connection refused`** — Verify the Aria Automation hostname/IP in the URL and ensure the appliance is running and network accessible.
    **`jq: error (at <stdin>:1): Cannot index null with string "cspAuthToken"`** — Check that credentials are correct and the CSP gateway is responding; verify the JSON response contains `cspAuthToken` field using `curl -s ... | jq '.'` to inspect the full response.
    **`bash: jq: command not found`** — Install jq on the system with `apt-get install jq` (Debian/Ubuntu) or `yum install jq` (RHEL/CentOS).
---

## REST API — Deployments

```bash
VRA="https://<aria-auto>"

# List all deployments
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/deployment/api/deployments?size=50" \
  | jq '.content[] | {name, id, status, projectId}'

# Get a specific deployment
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/deployment/api/deployments/<deployment-id>" | jq .

# List resources in a deployment
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/deployment/api/deployments/<deployment-id>/resources" | jq '.content[].name'

# Delete a deployment
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "$VRA/deployment/api/deployments/<deployment-id>"
```


```text title="Expected output"
{
  "name": "prod-web-tier",
  "id": "deployment-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "status": "CREATE_SUCCESSFUL",
  "projectId": "project-x9y8z7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}
{
  "name": "dev-database-cluster",
  "id": "deployment-f7g8h9i0-j1k2-l3m4-n5o6-p7q8r9s0t1u2",
  "status": "CREATE_SUCCESSFUL",
  "projectId": "project-x9y8z7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}
{
  "name": "staging-app-server",
  "id": "deployment-m3n4o5p6-q7r8-s9t0-u1v2-w3x4y5z6a7b8",
  "status": "UPDATE_FAILED",
  "projectId": "project-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6"
}
...
{
  "name": "archive-legacy-vm",
  "id": "deployment-z9y8x7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4",
  "status": "DELETE_IN_PROGRESS",
  "projectId": "project-x9y8z7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4"
}

{
  "id": "deployment-a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6",
  "name": "prod-web-tier",
  "status": "CREATE_SUCCESSFUL",
  "projectId": "project-x9y8z7w6-v5u4-t3s2-r1q0-p9o8n7m6l5k4",
  "createdAt": "2024-01-15T09:23:47Z",
  "lastModifiedAt": "2024-01-15T09:45:12Z",
  "inputs": {
    "environment": "production",
    "instance_count": 3,
    "vm_memory_mb": 4096
  }
}

nginx-lb-01
nginx-lb-02
postgresql-primary
postgresql-replica-01
postgresql-replica-02
redis-cache-01
...

(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <aria-auto> port 443: Connection refused`** — Verify the VRA hostname is correct and the Aria Automation appliance is running and accessible on the network.
    **`{"status":401,"message":"Unauthorized"}`** — Ensure the $
---

## REST API — Blueprints and Catalog

```bash
# List all blueprints (cloud templates)
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/blueprint/api/blueprints" \
  | jq '.content[] | {name, id, status}'

# Get blueprint YAML content
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/blueprint/api/blueprints/<blueprint-id>/content" | jq -r '.content'

# List catalog items (self-service catalog)
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/catalog/api/items?size=50" \
  | jq '.content[] | {name, id, type}'

# Request a catalog item (create a deployment)
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "$VRA/catalog/api/items/<item-id>/request" \
  -d '{
    "deploymentName": "my-deployment",
    "projectId": "<project-id>",
    "inputs": {}
  }' | jq .
```


```text title="Expected output"
{
  "name": "Ubuntu-Web-Tier",
  "id": "blueprint-8f4a2c91-7e3d-4b6f-9a1c-2d5e8b3f7a9c",
  "status": "PUBLISHED"
}
{
  "name": "SQL-Database-Template",
  "id": "blueprint-c3e9f1b2-5a7d-4e2c-8f6a-1b9d3c7e5a2f",
  "status": "PUBLISHED"
}
{
  "name": "Kubernetes-Cluster",
  "id": "blueprint-2b6f8a1d-9c4e-7f3a-5b2c-8e1a9d6f4c3b",
  "status": "DRAFT"
}
...

formatVersion: 1
name: Ubuntu-Web-Tier
inputs:
  environment:
    type: string
    default: production
  instance_count:
    type: integer
    default: 2
resources:
  WebServer:
    type: Cloud.Machine
    properties:
      image: ubuntu-20.04-lts
      flavor: medium

{
  "name": "Deploy Ubuntu VM",
  "id": "item-5c8b2f9a-1d7e-4a3f-8c6b-9e2f5a1d7c4b",
  "type": "BLUEPRINT"
}
{
  "name": "Provision SQL Server",
  "id": "item-7a9f3c1e-6b2d-5f8a-4e9c-1b7d3a5f2c8e",
  "type": "BLUEPRINT"
}
{
  "name": "Request Storage Volume",
  "id": "item-2e4f7b9a-8c1d-3f5a-6b2e-9d1c4a7f3b5e",
  "type": "BLUEPRINT"
}

{
  "id": "request-9f2a7c1e-5b8d-4a3f-6e9c-2b1d7a5f8c3e",
  "status": "SUBMITTED",
  "deploymentName": "my-deployment",
  "projectId": "project-4c8f2b1a-9e3d-7f5a-1c6b-8d2e9a4f7c5b",
  "requestedBy": "admin@company.local",
  "requestedOn": "2024-01-15T14:32:18.456Z",
  "estimatedCompletionTime": "2024-01-15T14:47:18.456Z"
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to aria-automation.corp: Name or service not known`** — Verify the $VRA variable is set correctly with the full FQDN or IP address (e.g., `export VRA=https://aria-automation.corp:443`).
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API token in $TOKEN is valid and not expired; re-authenticate and regenerate the bearer token
---

## REST API — Projects and Cloud Accounts

```bash
# List projects
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/iaas/api/projects" \
  | jq '.content[] | {name, id}'

# List cloud accounts
curl -s -H "Authorization: Bearer $TOKEN" \
  "$VRA/iaas/api/cloud-accounts" \
  | jq '.content[] | {name, cloudAccountType, id}'

# Trigger data collection on a cloud account
curl -s -X POST -H "Authorization: Bearer $TOKEN" \
  "$VRA/iaas/api/cloud-accounts/<id>/schedule-data-collection"
```


```text title="Expected output"
{
  "name": "Production-Infra",
  "id": "1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p"
}
{
  "name": "Dev-Environment",
  "id": "2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q"
}
{
  "name": "vSphere-Account-01",
  "cloudAccountType": "vsphere",
  "id": "3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r"
}
{
  "name": "AWS-Primary",
  "cloudAccountType": "aws",
  "id": "4d5e6f7g-8h9i-0j1k-2l3m-4n5o6p7q8r9s"
}
{
  "name": "Azure-Secondary",
  "cloudAccountType": "azure",
  "id": "5e6f7g8h-9i0j-1k2l-3m4n-5o6p7q8r9s0t"
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to aria-automation.corp.local port 443: Connection refused`** — Verify the $VRA variable is set correctly and the Aria Automation appliance is running and accessible on the network.
    **`jq: parse error: Invalid JSON text at line 1`** — Check that the $TOKEN is valid and not expired; an invalid token returns HTML error pages instead of JSON.
    **`curl: (22) The requested URL returned error: 404 Not Found`** — Ensure the cloud account ID in the URL path is correct and the account still exists in the system.
---

## PowerVRA — PowerShell Module

```powershell
# Install
Install-Module -Name PowerVRA -Scope CurrentUser

# Connect
Connect-VRAServer -Server "aria-auto.corp.local" -Credential (Get-Credential)

# List deployments
Get-VRADeployment | Select-Object Name, Status, ProjectName | Format-Table

# Get a specific deployment
Get-VRADeployment -Name "my-deployment"

# Request a catalog item
New-VRADeployment -CatalogItemName "Ubuntu 22.04" `
                  -DeploymentName "web-prod-01" `
                  -ProjectName "Team-A"

# Delete a deployment
Remove-VRADeployment -Name "web-prod-01" -Confirm:$false

# Disconnect
Disconnect-VRAServer
```

---

## Aria Orchestrator — Admin Commands

Aria Orchestrator (vRO) is embedded in Aria Automation and accessible via its control center.

```bash
# vRO Control Center — browser URL
# https://<aria-auto>/vco/app   (Orchestrator UI)
# https://<aria-auto>:8283/vco-controlcenter  (Admin/logs)

# Orchestrator API Swagger docs
# https://<aria-auto>/vco/api/docs

# Download vRO server log from Control Center:
# vRO Control Center → Logs → Download Server Log

# REST API — list workflows
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<aria-auto>/vco/api/workflows?maxResult=20" \
  | jq '.link[] | .attributes[] | select(.name=="name") | .value'

# Run a workflow via REST
curl -s -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  "https://<aria-auto>/vco/api/workflows/<workflow-id>/executions" \
  -d '{"parameters": [{"name": "vmName", "type": "string", "value": {"string": {"value": "my-vm"}}}]}'
```


```text title="Expected output"
"Provision VM"
"Decommission VM"
"Configure Network"
"Backup VM"
"Health Check"
"Update Firmware"
"Generate Report"
...

{"id":"dde52f47-0a3c-4f2a-b8e1-7c9d3f1a2b4c","execution-state":"RUNNING","execution-id":"exec-20240115-001","start-time":"2024-01-15T14:32:18.000Z","parameters":[{"name":"vmName","type":"string","value":{"string":{"value":"my-vm"}}}]}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the Aria Automation CA certificate into your system trust store.
    **`jq: parse error: Cannot index string with string "attributes"`** — Verify the API response structure matches your jq filter by running `curl ... | jq '.'` first to inspect the actual JSON format.
    **`{"error":"Invalid token","error_description":"The access token expired"}`** — Regenerate the Bearer token by re-authenticating to Aria Automation's OAuth endpoint before retrying the API call.
---

## VAMI — Appliance Management Interface

VAMI is the browser-based appliance management UI at `https://<aria-auto>:5480`.

Key tasks available in VAMI:
- **Network configuration** — IP, DNS, NTP (also doable via vracli)
- **Time sync** — NTP status and synchronisation
- **SSL certificate** — view and replace the VAMI/appliance certificate
- **System** — reboot, shutdown, update vRA appliance patches
- **Monitor** — CPU, memory, disk usage of the appliance VM

```bash
# VAMI is a web UI — access from browser:
# https://<aria-auto>:5480
# Credentials: root / <appliance-root-password>
```

---

## See also

- [Aria Automation — Operational Procedures](../procedures/)
- [Aria Automation — Scripts Reference](../scripts/)
- [Aria Automation — Health Checks](../health-checks/)

## Verify

- **vracli status --all** returns green for all services
- **kubectl get pods -n prelude** shows all pods in `Running` state
- **API test:** `curl -s -H "Authorization: Bearer $TOKEN" "$VRA/iaas/api/zones" | jq '.totalElements'` returns a number
