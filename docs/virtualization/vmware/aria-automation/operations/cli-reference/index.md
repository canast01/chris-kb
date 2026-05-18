# Aria Automation — CLI Reference

```
┌─────────────────────────────────────────────────────────────┐
│          Aria Automation CLI: vracli Command Tree           │
├──────────────────────────┬──────────────────────────────────┤
│  vracli (appliance CLI)  │  kubectl (Kubernetes layer)      │
├──────────────────────────┼──────────────────────────────────┤
│ vracli status            │ kubectl get pods -n prelude      │
│ vracli version           │ kubectl logs <pod> -n prelude    │
│ vracli cluster health    │ kubectl describe pod <pod>       │
│ vracli backup list       │ kubectl get events -n prelude    │
│ vracli backup start      │ kubectl rollout restart          │
│ vracli backup status     │   deployment/<name> -n prelude   │
│ vracli restore list      │                                  │
│ vracli restore start     │ kubectl get svc -n prelude       │
│ vracli certificate list  │ kubectl get secrets -n prelude   │
│ vracli certificate import│                                  │
│ vracli support-bundle    │  REST API base:                  │
│ vracli software-update   │  /csp/gateway/am/api/login       │
│   install --file <pak>   │  /iaas/api/  /deployment/api/   │
│                          │  /blueprint/api/                 │
└──────────────────────────┴──────────────────────────────────┘
```

## vracli (Appliance CLI)

SSH to the Aria Automation appliance and use `vracli` for appliance-level management.

| Command | Description |
|---|---|
| `vracli status` | Show health status of all Aria Automation services |
| `vracli version` | Display the installed Aria Automation version |
| `vracli certificate list` | List installed TLS certificates |
| `vracli certificate import --cert /path/cert.pem --key /path/key.pem` | Import a new TLS certificate |
| `vracli proxy` | View or configure proxy settings |

---

## Kubernetes (On-Premises Appliance)

The Aria Automation appliance runs workloads in a Kubernetes cluster. The namespace for Aria Automation services is `prelude`.

```bash
# List all pods in the prelude namespace
kubectl get pods -n prelude

# Check pod logs
kubectl logs <pod-name> -n prelude

# Describe a pod (events, resource limits)
kubectl describe pod <pod-name> -n prelude

# List services
kubectl get svc -n prelude
```

---

## REST API

Base URL: `https://<aria-automation-fqdn>/iaas/api/`

### Authentication

Obtain an access token (using a Workspace ONE Access / vIDM account):

```bash
curl -s -X POST "https://<aria-auto>/csp/gateway/am/api/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "user@domain", "password": "password"}' | jq '.access_token'
```

Set the token as a variable:

```bash
TOKEN="<access_token>"
```

### Deployments

```bash
# List all deployments
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<aria-auto>/deployment/api/deployments" | jq '.content[]|.name,.id,.status'

# Get a specific deployment
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<aria-auto>/deployment/api/deployments/<deployment-id>"

# Delete a deployment
curl -s -X DELETE -H "Authorization: Bearer $TOKEN" \
  "https://<aria-auto>/deployment/api/deployments/<deployment-id>"
```

### Cloud Templates (Blueprints)

```bash
# List all blueprints
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://<aria-auto>/blueprint/api/blueprints" | jq '.content[]|.name,.id'
```

---

## PowerShell (PowervRA Module)

Install the module: `Install-Module -Name PowervRA`

```powershell
# Connect to Aria Automation
Connect-VRAServer -Server aria-auto.domain.com -Credential (Get-Credential)

# List all deployments
Get-VRADeployment

# Get a specific deployment
Get-VRADeployment -Name "my-deployment"

# Create a new deployment from a catalog item
New-VRADeployment -CatalogItemName "My Catalog Item" -DeploymentName "test-01" -ProjectName "My Project"

# Remove a deployment
Remove-VRADeployment -Id "<deployment-id>"
```

---

## Useful Log Paths

| Log | Path on Appliance |
|---|---|
| Service logs (all components) | `/services-logs/` |
| Kubernetes pod logs | `kubectl logs <pod> -n prelude` |
| Appliance syslog | `/var/log/` |
