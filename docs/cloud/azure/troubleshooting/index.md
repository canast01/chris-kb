# Azure — Troubleshooting

```
┌─────────────────────────────────── Azure Troubleshooting Overview ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Azure Troubleshooting — Common Issues, Diagnostics, and Escalation              │   │
│   │     Common issues: VM unreachable · NSG blocking · RBAC access denied · Storage auth error    │   │
│   │   Diagnostics: Boot diagnostics · Serial Console · Network Watcher · Activity Log · Monitor   │   │
│   │ Tools: az CLI describe · Azure portal diagnostics · Connection Troubleshoot · Resource Health │   │
│   │   Escalation: Azure Support cases; collect sub ID, region, resource ID, error, and timeframe  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Common issues guide investigation · Diagnostics locate root cause                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Common Issues        │  │         Diagnostics         │  │          Escalation         │   │
│   │      VM: RDP/SSH fails      │  │    Boot diagnostics: log    │  │     Sub ID + resource ID    │   │
│   │      NSG: port blocked      │  │     Serial Console: OOB     │  │      Error + timestamp      │   │
│   │     RBAC: access denied     │  │    Network Watcher: path    │  │     Severity: Crit/High     │   │
│   │      Storage: 403 auth      │  │    Activity Log: who/when   │  │    Sev A: production down   │   │
│   │     DNS: resolution fail    │  │    Resource Health: state   │  │     Premium support: TAM    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Identify symptom → collect diagnostics (logs, Network Watcher, health) → resolve or escalate       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │     Escalation    │    CLI Tools     │   Portal Tools   │   │
│   │    VM: no RDP    │  Boot diag log   │    Sev A: call    │    az vm list    │ Resource Health  │   │
│   │  NSG: miss rule  │  Serial console  │   Sub ID + error  │  az network nsg  │   Net Watcher    │   │
│   │   RBAC: denied   │   Activity Log   │    Premium: TAM   │  az role assign  │    Boot Diag     │   │
│   │   Storage: 403   │   Net Watcher    │    Collect: all   │  az storage ls   │  Diagn settings  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure VM host fabric · Azure networking SDN · Microsoft Support infrastructure                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Boot Diagnostics  = Captures VM serial console log and screenshot; diagnoses non-starting VMs        │
│  Serial Console    = Out-of-band terminal access to VM; works when RDP/SSH unreachable                │
│  Network Watcher   = Diagnoses connectivity; Connection Troubleshoot traces hop-by-hop path           │
│  Connection Troubleshoot= Network Watcher tool; tests TCP reachability from source VM to destination  │
│  Resource Health   = Per-resource health history; shows Azure platform events affecting the resource  │
│  Activity Log      = Control-plane audit; search for who made a change and when in the last 90 days   │
│  NSG flow logs     = Accepted/denied traffic metadata; route to Log Analytics for KQL queries         │
│  Severity A case   = Production down; 24/7 response; phone callback + online case together            │
│  Severity B case   = Degraded function; business-hours response; online case sufficient               │
│  TAM               = Technical Account Manager; named Microsoft contact for Premier/Unified support   │
│  RBAC denied       = Check Activity Log for the 403; look for missing role or wrong scope             │
│  Storage 403       = Check access key vs SAS vs RBAC; check firewall rules and private endpoint config│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Known failure modes, symptoms, causes, and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands, log locations, and data collection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>What to collect before opening a support case and how to engage Microsoft support.</span>
</a>

</div>

## VM Connectivity Issues

```bash
# 1. Check effective NSG rules on the NIC
az network nic show-effective-nsg --name <nic-name> -g <rg> | \
    jq '.effectiveNetworkSecurityGroups[].effectiveSecurityRules[] | select(.access=="Deny")'

# 2. Check effective routes on the NIC
az network nic show-effective-route-table --name <nic-name> -g <rg>

# 3. Use Network Watcher to test connectivity
az network watcher test-connectivity \
    --source-resource <source-vm-id> \
    --dest-address <destination-ip> --dest-port 443

# 4. Packet capture on NIC
az network watcher packet-capture create \
    --vm <vm-name> -g <rg> --name my-capture --storage-account <sa>
```

Common causes:
- NSG deny rule at NIC level (NIC NSG takes precedence over Subnet NSG)
- User-defined route sending traffic to wrong next hop
- Azure Firewall blocking traffic between hub and spoke
- Service endpoint not configured on subnet (for PaaS services)

## NSG Troubleshooting

```bash
# Check if traffic is allowed by NSG
az network watcher check-nsg-flow --direction Inbound \
    --protocol TCP --local 10.0.0.4 --local-port 443 \
    --remote 10.1.0.10 --remote-port 52000 \
    --nsg <nsg-id>
# Output: access = Allow or Deny, with matching rule name

# View NSG flow logs (query Log Analytics)
# Workspace → Logs:
AzureNetworkAnalytics_CL
| where SubType_s == "FlowLog"
| where FlowStatus_s == "D"   // Denied flows
| where DestIP_s == "<target-ip>"
| project TimeGenerated, SrcIP_s, DestIP_s, DestPort_d, NSGName_s, NSGRule_s
```

## Azure AD Authentication Errors

```bash
# Check token issuance via Entra ID sign-in logs
az monitor activity-log list --correlation-id <correlation-id>

# Via Entra ID portal: Monitor → Sign-in logs → filter by app/user
# Look for: failure reason, conditional access policy that blocked sign-in

# Check service principal credential expiry
az ad sp credential list --id <sp-object-id>

# If federated credential issue (OIDC):
az ad app federated-credential list --id <app-id>
```

Common causes:
- Conditional Access policy blocking (no MFA, non-compliant device, suspicious location)
- Service principal client secret expired
- Missing API permission or admin consent not granted

## Azure Storage Access Denied

```bash
# Check storage firewall rules
az storage account show -n <storage-account> --query 'networkRuleSet'

# Check role assignments on storage account
az role assignment list --scope <storage-account-resource-id>

# Test access via SAS token
az storage blob download --account-name <sa> --container-name <container> \
    --name <blob> --file /tmp/test --sas-token "<sas>"

# Check if data plane access uses Entra ID or key-based auth
# Key-based access can be disabled in Shared Key authorization:
az storage account show -n <sa> --query 'allowSharedKeyAccess'
```

## AKS Pod Not Starting

```bash
# Get pod description and events
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | tail -20

# Check node resource pressure
kubectl describe node <node-name> | grep -A 5 "Conditions:"
kubectl top nodes

# Image pull error
kubectl get events -n <namespace> | grep "Failed to pull"
# Check Azure Container Registry firewall if using private ACR:
az acr show --name <acr-name> --query 'networkRuleSet'

# DNS resolution in pod (network policy blocking?)
kubectl run test-pod --rm -i --image=busybox -- nslookup kubernetes.default
```

## App Service 502/503

1. Azure Portal → App Service → Diagnose and solve problems → Availability and Performance
2. Check App Service Plan metrics: CPU %, Memory % (Metrics blade)
3. Review application logs: App Service → App Service Logs → enable File System logging
4. Check health probe configuration: App Service → Health Check — confirm probe returning 200

```bash
# Check App Service Plan scale out status
az appservice plan show --name <plan-name> -g <rg> \
    --query 'properties.numberOfWorkers'

# Manual scale up (if throttled)
az appservice plan update --name <plan-name> -g <rg> --sku P2V3
```
