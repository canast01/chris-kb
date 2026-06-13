---
tags:
  - azure
  - security
---
# Azure — Hardening


<div class="kb-summary">
Azure hardening applies the principle of least privilege, reduces the attack surface, and enforces security configuration standards across subscriptions, resource groups, and individual resources.
</div>
```text
┌────────────────────────────── Cloud Azure Security — Security Hardening ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Azure hardening: disable unused protocols, enforce encryption, restrict access        │   │
│   │         Network: dedicated storage VLAN; restrict management access to jump hosts only        │   │
│   │        Auth: disable default accounts; enforce password complexity and rotation policy        │   │
│   │         Audit: forward syslog to SIEM; alert on privilege escalation and failed logins        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Baseline config → disable unused → enforce MFA → enable logging → audit                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Area       │     Control      │      Standard     │      Verify      │    Frequency     │   │
│   │     Accounts     │ Disable defaults │  No default creds │   Login audit    │      Deploy      │   │
│   │    Protocols     │  Disable unused  │   TLS 1.2+ only   │    Port scan     │     Monthly      │   │
│   │       MFA        │ Enforce all admi │   TOTP/hardware   │    Auth logs     │    Continuous    │   │
│   │     Logging      │ SIEM forwarding  │  All admin events │   SIEM alerts    │      Daily       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Security infrastructure · management network · monitoring                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Security platform overview and core concepts                      │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Microsoft Defender for Cloud

Defender for Cloud is the primary security posture dashboard. It aggregates recommendations, assigns a Secure Score, and provides threat detection.

```bash
# Enable Defender for Cloud on a subscription (free tier — CSPM only)
az security auto-provisioning-setting update \
  --name mma \
  --auto-provision On

# Enable Defender plans (paid) for specific resource types
az security pricing create --name VirtualMachines --tier Standard
az security pricing create --name StorageAccounts --tier Standard
az security pricing create --name SqlServers --tier Standard
az security pricing create --name AppServices --tier Standard
az security pricing create --name Containers --tier Standard

# List all Defender plan states
az security pricing list --output table

# Get current Secure Score
az security secure-score list --output table
```

### Unhealthy Recommendations

```bash
# List all unhealthy security recommendations
az security assessment list \
  --query "[?status.code=='Unhealthy']" \
  --output table

# Get details on a specific recommendation
az security assessment show \
  --name <assessment-name> \
  --assessed-resource-id <resource-id>

# Export all recommendations to JSON for remediation tracking
az security assessment list --output json > security-assessments-$(date +%Y%m%d).json
```

---

## Network Security Groups

NSGs filter traffic at the subnet or NIC level. Apply NSGs to subnets (preferred) rather than individual NICs.

```bash
# Create an NSG
az network nsg create \
  --name nsg-appsubnet \
  --resource-group <rg-name> \
  --location <region>

# Add a rule — allow HTTPS inbound from a specific CIDR
az network nsg rule create \
  --nsg-name nsg-appsubnet \
  --resource-group <rg-name> \
  --name Allow-HTTPS-Inbound \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 10.0.0.0/8 \
  --destination-port-ranges 443

# Deny all other inbound (explicit deny — NSGs have implicit deny but make it explicit for auditing)
az network nsg rule create \
  --nsg-name nsg-appsubnet \
  --resource-group <rg-name> \
  --name Deny-All-Inbound \
  --priority 4000 \
  --direction Inbound \
  --access Deny \
  --protocol '*' \
  --source-address-prefixes '*' \
  --destination-port-ranges '*'

# Associate NSG with a subnet
az network vnet subnet update \
  --vnet-name <vnet-name> \
  --name <subnet-name> \
  --resource-group <rg-name> \
  --network-security-group nsg-appsubnet

# List effective NSG rules on a NIC (what actually applies including inheritance)
az network nic list-effective-nsg \
  --name <nic-name> \
  --resource-group <rg-name>
```

### NSG Flow Logs

Enable flow logs for all production NSGs. Required for security investigations and network anomaly detection.

```bash
# Create a storage account for NSG flow logs
az storage account create \
  --name <sa-nsgflowlogs> \
  --resource-group <rg-name> \
  --sku Standard_LRS

# Enable NSG flow logs (version 2 includes traffic analytics)
az network watcher flow-log create \
  --name flowlog-nsg-appsubnet \
  --resource-group <rg-name> \
  --nsg <nsg-resource-id> \
  --storage-account <sa-resource-id> \
  --enabled true \
  --format JSON \
  --log-version 2 \
  --retention 90 \
  --traffic-analytics true \
  --workspace <log-analytics-workspace-id>
```

---

## Just-In-Time VM Access

JIT VM access blocks management ports (RDP/SSH) by default and opens them only for approved requests with time limits.

```bash
# Enable JIT on a VM
az security jit-policy create \
  --resource-group <rg-name> \
  --location <region> \
  --vm-name <vm-name> \
  --ports '[
    {
      "number": 22,
      "protocol": "TCP",
      "allowedSourceAddressPrefix": "*",
      "maxRequestAccessDuration": "PT3H"
    },
    {
      "number": 3389,
      "protocol": "TCP",
      "allowedSourceAddressPrefix": "*",
      "maxRequestAccessDuration": "PT3H"
    }
  ]'

# Request JIT access (opens port for 2 hours from your IP)
az security jit-policy initiate \
  --resource-group <rg-name> \
  --vm-name <vm-name> \
  --vm-requests '[
    {
      "virtualMachineResourceId": "<vm-resource-id>",
      "ports": [
        {
          "number": 22,
          "allowedSourceAddressPrefix": "<your-ip>/32",
          "endTimeUtc": "2024-01-01T12:00:00.0000000Z",
          "duration": "PT2H"
        }
      ]
    }
  ]'
```

---

## Azure Policy for Security

Azure Policy enforces configuration standards automatically and audits for drift.

```bash
# List all built-in security policies
az policy definition list \
  --query "[?policyType=='BuiltIn' && contains(displayName, 'Security')]" \
  --output table

# Assign a built-in policy: require TLS 1.2 on storage accounts
az policy assignment create \
  --name "require-tls12-storage" \
  --display-name "Require TLS 1.2 on Storage Accounts" \
  --policy "fe83a0eb-a853-422d-aac2-1bffd182c5d0" \
  --scope "/subscriptions/<sub-id>" \
  --enforcement-mode Default

# Assign CIS Microsoft Azure Foundations Benchmark initiative
az policy assignment create \
  --name "cis-azure-benchmark" \
  --display-name "CIS Microsoft Azure Foundations Benchmark" \
  --policy-set-definition "612b5213-9160-4969-8578-1518bd2a000c" \
  --scope "/subscriptions/<sub-id>"

# Get policy compliance state
az policy state summarize \
  --subscription <sub-id> \
  --output table

# Get non-compliant resources for a specific assignment
az policy state list \
  --policy-assignment <assignment-id> \
  --filter "complianceState eq 'NonCompliant'" \
  --output table
```

---

## Resource Locks

Resource locks prevent accidental deletion or modification of critical resources.

```bash
# Apply a delete lock to a resource group
az lock create \
  --name lock-prod-rg \
  --resource-group <rg-name> \
  --lock-type CanNotDelete \
  --notes "Production resource group — cannot delete without removing lock"

# Apply a read-only lock (prevents modification)
az lock create \
  --name lock-prod-vnet-readonly \
  --resource-group <rg-name> \
  --resource-type Microsoft.Network/virtualNetworks \
  --resource-name <vnet-name> \
  --lock-type ReadOnly

# List all locks in a subscription
az lock list --output table

# Remove a lock
az lock delete \
  --name lock-prod-rg \
  --resource-group <rg-name>
```

Apply `CanNotDelete` locks to all production resource groups, key vaults, virtual networks, and storage accounts that hold critical data.

---

## Defender for Servers — Hardening

When Defender for Servers (Plan 2) is enabled, it provides:
- Microsoft Defender Vulnerability Management (MDVM) for OS and application CVE scanning
- File Integrity Monitoring (FIM) — alerts on changes to critical system files
- Adaptive Application Controls — allowlist for running processes
- OS security baseline assessment (CIS benchmarks)

```bash
# Check vulnerability assessment findings for a VM
az security va sql scans list \
  --server-name <server> \
  --database-name <db> \
  --resource-group <rg-name>

# Get endpoint protection status on VMs
az security assessment list \
  --query "[?contains(displayName, 'endpoint protection')]" \
  --output table
```

---

## Security Baseline Hardening Checklist

| Control | Azure Implementation | Status Check |
|---|---|---|
| MFA enforced for all users | Conditional Access policy | `az rest --url graph.microsoft.com/v1.0/identity/conditionalAccess/policies` |
| Legacy auth blocked | Conditional Access → block legacy clients | Same as above |
| No standing Owner assignments | PIM eligible assignments only | `az role assignment list --all --query "[?roleDefinitionName=='Owner']"` |
| JIT VM access | Defender for Cloud → JIT | `az security jit-policy list` |
| NSG flow logs | All production NSGs | `az network watcher flow-log list` |
| Key Vault purge protection | Enabled on all vaults | `az keyvault list --query "[?properties.enablePurgeProtection!=true]"` |
| Storage HTTPS only | All storage accounts | `az storage account list --query "[?enableHttpsTrafficOnly!=true]"` |
| Storage TLS 1.2+ | All storage accounts | `az storage account list --query "[?minimumTlsVersion!='TLS1_2']"` |
| Defender for Cloud enabled | All subscriptions | `az security auto-provisioning-setting list` |
| Diagnostic settings | All critical resources | `az monitor diagnostic-settings list` |
| No public storage blobs | All storage accounts | `az storage account list --query "[?allowBlobPublicAccess==true]"` |

```bash
# Quick hardening audit — find storage accounts with HTTP allowed or public access
az storage account list --output json | python3 -c "
import json, sys
accounts = json.load(sys.stdin)
for a in accounts:
    issues = []
    if not a.get('enableHttpsTrafficOnly'): issues.append('HTTP allowed')
    if a.get('allowBlobPublicAccess'): issues.append('public blob access')
    if a.get('minimumTlsVersion','') != 'TLS1_2': issues.append('TLS < 1.2')
    if issues:
        print(f'{a[\"name\"]}: {\", \".join(issues)}')
"
```
