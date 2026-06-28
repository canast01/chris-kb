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




```d2
direction: right

hub: "Aria Automation\nOperations" {shape: hexagon}
vracli_appliance_management: "vracli — Appliance Management" {shape: rectangle}
kubectl_kubernetes_diagnostics: "kubectl — Kubernetes Diagnostics" {shape: rectangle}
rest_api_authentication_and_token: "REST API — Authentication and Token" {shape: rectangle}
rest_api_deployments: "REST API — Deployments" {shape: rectangle}
rest_api_blueprints_and_catalog: "REST API — Blueprints and Catalog" {shape: rectangle}
rest_api_projects_and_cloud_accounts: "REST API — Projects and Cloud Accounts" {shape: rectangle}

hub -> vracli_appliance_management
hub -> kubectl_kubernetes_diagnostics
hub -> rest_api_authentication_and_token
hub -> rest_api_deployments
hub -> rest_api_blueprints_and_catalog
hub -> rest_api_projects_and_cloud_accounts
```

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

### Cluster Management (3-Node HA)

```bash
# Show cluster node status
vracli cluster status

# Add a second/third node to form HA cluster
vracli cluster join --master-node <master-ip> --join-token <token>

# Get join token from master node
vracli cluster token
```

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

- [Aria Automation — Operational Procedures](procedures/)
- [Aria Automation — Scripts Reference](scripts/)
- [Aria Automation — Health Checks](health-checks/)

## Verify

- **vracli status --all** returns green for all services
- **kubectl get pods -n prelude** shows all pods in `Running` state
- **API test:** `curl -s -H "Authorization: Bearer $TOKEN" "$VRA/iaas/api/zones" | jq '.totalElements'` returns a number
