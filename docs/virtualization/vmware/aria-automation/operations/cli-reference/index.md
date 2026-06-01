# Aria Automation — CLI Reference


<div class="kb-summary">
CLI Reference reference covering vracli (Appliance CLI), Kubernetes (On-Premises Appliance), PowerShell (PowervRA Module), Useful Log Paths.
</div>

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
┌─────────────────────────────────── Aria Automation — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│  vRA is operated via REST API, vracli, and VAMI; no traditional SSH-heavy CLI.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            vracli (appliance CLI)            │  │         REST API (primary interface)        │   │
│   │        vracli status: service health         │  │        POST /csp/gateway/am/api/login       │   │
│   │        vracli certificate: cert mgmt         │  │       GET /deployment/api/deployments       │   │
│   │           vracli vidm: vIDM config           │  │        POST /blueprint/api/blueprints       │   │
│   │         vracli proxy: proxy settings         │  │            GET /catalog/api/items           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Service and log commands run on the vRA appliance via SSH as root.                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Service Management              │  │                Log Locations                │   │
│   │         systemctl status vra-cluster         │  │             /var/log/vmware/vra/            │   │
│   │         kubectl get pods -n prelude          │  │          journalctl -u vra-cluster          │   │
│   │        kubectl logs <pod> -n prelude         │  │         /var/log/vmware/vlcm/ (LCM)         │   │
│   │       vracli status --all (full check)       │  │        kubectl logs <pod> -n prelude        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA Linux appliance VMs · internal Kubernetes (k3s/Rancher) · Postgres · vIDM VM                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vracli            = Appliance CLI shipped with vRA; manages certs, vIDM config, proxy, NTP           │
│  prelude namespace  = Kubernetes namespace where vRA microservices run inside the appliance           │
│  kubectl           = Kubernetes CLI; used on vRA appliance to inspect pods and logs                   │
│  REST API          = Primary programmatic interface; all UI actions use the same API underneath       │
│  Bearer token      = JWT returned by /csp/gateway/am/api/login; passed as Authorization header        │
│  Swagger UI        = /vco/api/docs (Orchestrator) and /automation-ui/api/docs (vRA) for REST docs     │
│  vracli status     = Reports health of each microservice; green/red output per service                │
│  systemctl         = Linux service manager; vra-cluster is main managed service                       │
│  journalctl        = Linux log viewer; use -u vra-cluster for appliance startup logs                  │
│  VAMI              = Web-based appliance management at :5480; configure network/NTP/proxy             │
│  ABX CLI           = No dedicated CLI; ABX actions tested via vRA UI Run or REST trigger              │
│  Orchestrator CLI  = vco-controlcenter at :8283 for Orchestrator admin and log download               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
