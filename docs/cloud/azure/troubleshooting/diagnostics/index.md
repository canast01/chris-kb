---
tags:
  - azure
  - troubleshooting
search:
  boost: 1.5
description: "Azure diagnostic commands: check account and subscription context with az cli, diagnose VM boot and network issues with Network Watcher, query Activity..."
---
# Azure — Diagnostics

<div class="kb-summary">
Azure diagnostic commands: check account and subscription context with az cli, diagnose VM boot and network issues with Network Watcher, query Activity Log for recent changes, run Log Analytics KQL queries, inspect Key Vault access, and collect resource diagnostic data for Microsoft support.

*Applies to: Microsoft Azure — all core IaaS services*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "az vm get-instance-view\nCheck power state and agent health" {shape: rectangle}
D: "az network nic show-effective-nsg\nFind deny rule" {shape: rectangle}
E: "az monitor activity-log list\nFind the change event" {shape: rectangle}
F: "az vm boot-diagnostics get-boot-log\nRead serial console output" {shape: rectangle}
G: "Log Analytics KQL\nHeartbeat or custom table" {shape: rectangle}
H: "az keyvault show\nCheck access policies and firewall" {shape: rectangle}
I: "I" {shape: rectangle}
J: "az vm start --name vm -g rg\nVerify billing and quota" {shape: rectangle}
K: "az vm run-command invoke\nRun ipconfig or hostname" {shape: rectangle}
L: "L" {shape: rectangle}
M: "az network nsg rule update\nor add allow rule with lower priority" {shape: rectangle}
N: "az network nic show-effective-route-table\nBlackhole route?" {shape: rectangle}
O: "Review change: who, what, when\nRoll back if recent deployment" {shape: rectangle}
P: "Boot error in serial log\nCheck disk, kernel panic, fstab" {shape: rectangle}
Q: "KQL: Heartbeat | where TimeGenerated > ago 1h\nCount by Computer" {shape: rectangle}
R: "Check RBAC vs access policies\nCheck network ACLs on Key Vault" {shape: rectangle}
S: "Collect resource diag\naz vm boot-diagnostics get-boot-log" {shape: rectangle}
T: "Open Azure support request\nportal.azure.com → Help + support" {shape: rectangle}
A: "Azure Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
L -> M
L -> N
E -> O
F -> P
G -> Q
H -> R
J -> S
K -> S
M -> S
N -> S
O -> S
P -> S
Q -> S
R -> S
S -> T
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_verify_subscription_context: "Step 1 — Verify subscription context" {shape: rectangle}
step_2_check_vm_state_and_health: "Step 2 — Check VM state and health" {shape: rectangle}
step_3_read_boot_diagnostics: "Step 3 — Read boot diagnostics" {shape: rectangle}
step_4_check_nsg_and_routing: "Step 4 — Check NSG and routing" {shape: rectangle}
step_5_check_activity_log_for_recent: "Step 5 — Check Activity Log for recent changes" {shape: rectangle}
step_6_query_log_analytics: "Step 6 — Query Log Analytics" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_verify_subscription_context: investigate
symptom -> step_2_check_vm_state_and_health: investigate
symptom -> step_3_read_boot_diagnostics: investigate
symptom -> step_4_check_nsg_and_routing: investigate
symptom -> step_5_check_activity_log_for_recent: investigate
symptom -> step_6_query_log_analytics: investigate
step_1_verify_subscription_context -> resolution
step_2_check_vm_state_and_health -> resolution
step_3_read_boot_diagnostics -> resolution
step_4_check_nsg_and_routing -> resolution
step_5_check_activity_log_for_recent -> resolution
step_6_query_log_analytics -> resolution
```

## Before you begin

- **Access:** Verify your Azure CLI is logged in and targeting the correct subscription before running any commands
- **Gather first:** the affected VM name and resource group, the specific error (HTTP error code, SSH failure, application error), and the approximate time the issue started
- **Scope:** confirm whether the issue affects a single VM, a VNet, a subscription, or appears in the Azure Service Health dashboard (platform incident)
- **Check Azure Status first:** visit status.azure.com — if the region is degraded, customer-side investigation is limited until Microsoft resolves the platform issue

---

## Step 1 — Verify subscription context

```bash
# Confirm which account and subscription are active
az account show
# Check: id (subscription ID), name, state (Enabled), tenantId

# List all subscriptions accessible to this identity
az account list -o table

# Switch to the correct subscription
az account set --subscription "<subscription-name-or-id>"

# Verify access to the affected resource group
az group show -n <rg-name>
# Error "ResourceGroupNotFound" = wrong subscription; error 403 = insufficient RBAC
```


```text title="Expected output"
{
  "id": "12a4b5c6-7890-1234-5678-90abcdef1234",
  "name": "Production-Subscription",
  "state": "Enabled",
  "tenantId": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "isDefault": true,
  "user": {
    "name": "admin@contoso.onmicrosoft.com",
    "type": "user"
  }
}
Name                          CloudName    SubscriptionId                        TenantId                              State    
------------------------------  -----------  ------------------------------------  ------------------------------------  -------
Production-Subscription      AzureCloud   12a4b5c6-7890-1234-5678-90abcdef1234  a1b2c3d4-e5f6-7890-1234-567890abcdef  Enabled
Development-Subscription     AzureCloud   98f7e6d5-c4b3-2109-8765-4321fedcba09  a1b2c3d4-e5f6-7890-1234-567890abcdef  Enabled
Legacy-Subscription          AzureCloud   55aa44bb-33cc-2211-0099-8877665544ff  a1b2c3d4-e5f6-7890-1234-567890abcdef  Enabled
{
  "id": "/subscriptions/12a4b5c6-7890-1234-5678-90abcdef1234/resourceGroups/prod-rg-eastus",
  "name": "prod-rg-eastus",
  "type": "Microsoft.Resources/resourceGroups",
  "location": "eastus",
  "tags": {
    "environment": "production",
    "owner": "platform-team"
  },
  "properties": {
    "provisioningState": "Succeeded"
  }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceGroupNotFound` | Verify you are in the correct subscription using `az account set --subscription "<id>"` and confirm the resource group name spelling. |
    | `Authorization failed for template deployment. Insufficient privileges to complete the operation.` | Request elevated RBAC permissions (Contributor or Owner role) for the target subscription from your Azure administrator. |
---

## Step 2 — Check VM state and health

```bash
# Get VM power state and guest agent / extension status
az vm get-instance-view --name <vm-name> -g <rg> -o json
# Key fields:
#   statuses[].displayStatus: "VM running" (expected) or "VM stopped" / "VM deallocated"
#   extensions[].statuses[].displayStatus: "Provisioning succeeded" (expected)
#   extensions[].statuses[].message: extension error detail if failed

# Start a stopped VM
az vm start --name <vm-name> -g <rg>

# List extensions and their statuses
az vm extension list --vm-name <vm-name> -g <rg> -o table

# Run a command on the VM via Azure guest agent (no SSH or RDP needed)
az vm run-command invoke --command-id RunShellScript \
  --name <vm-name> -g <rg> \
  --scripts "df -h && ip addr show && ss -tulnp | grep LISTEN"
# Use RunPowerShellScript for Windows VMs:
# --scripts "Get-Service | Where-Object Status -eq Stopped"
```


```text title="Expected output"
{
  "statuses": [
    {
      "code": "ProvisioningState/succeeded",
      "level": "Info",
      "displayStatus": "Provisioning succeeded"
    },
    {
      "code": "PowerState/running",
      "level": "Info",
      "displayStatus": "VM running"
    }
  ],
  "extensions": [
    {
      "name": "Microsoft.Compute.CustomScriptExtension",
      "statuses": [
        {
          "code": "ProvisioningState/succeeded",
          "displayStatus": "Provisioning succeeded",
          "message": "Enable succeeded: [0] Finished executing command"
        }
      ]
    },
    {
      "name": "Microsoft.Azure.Security.Monitoring.AzureSecurityLinuxAgent",
      "statuses": [
        {
          "code": "ProvisioningState/succeeded",
          "displayStatus": "Provisioning succeeded"
        }
      ]
    }
  ]
}
Request successfully processed. VM 'prod-web-01' started.
NAME                                          PUBLISHER                                    VERSION  AUTO_UPGRADE_MINOR_VERSION
Microsoft.Compute.CustomScriptExtension      Microsoft.Compute                            1.10     False
Microsoft.Azure.Security.Monitoring.AzureSecurityLinuxAgent  Microsoft.Azure.Security  2.15     True
Filesystem     Size  Used Avail Use% Mounted on
/dev/sda1       30G  8.2G   21G  28% /
inet 10.42.3.187/24 brd 10.42.3.255 scope global eth0
LISTEN  tcp  0  0 0.0.0.0:22  0.0.0.0:*  root/sshd
LISTEN  tcp  0  0 0.0.0.0:443  0.0.0.0:*  root/nginx
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `(ResourceNotFound) The Resource 'Microsoft.Compute/virtualMachines/<vm-name>' under resource group '<rg>' was not found.` | Verify the VM name and resource group name are correct and the VM exists in the target subscription. |
    | `(AuthorizationFailed) The client '<user-id>' with object id '<object-id>' does not have authorization to perform action 'Microsoft.Compute/virtualMachines/read' over scope '/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Compute/virtualMachines/<vm-name>'.` | Ensure your Azure account has at least Reader role on the resource group or VM. |
    | `(VMExtensionProvisioningError) Enable failed for extension 'CustomScriptExtension' with message 'Handler status failed with exitCode: 1 StdErr: /bin/bash: line 1: df: command not found'.` | Verify the script commands are available on the target OS and the guest agent is running; check VM logs via `az vm boot-diagnostics get-boot-log`. |
---

## Step 3 — Read boot diagnostics

Boot diagnostics captures the VM's serial console output — available even when the OS is unresponsive or crashed.

```bash
# Get the serial console log (text)
az vm boot-diagnostics get-boot-log --name <vm-name> -g <rg>
# Look for:
#   Kernel panic: system crashed; check disk or memory
#   Starting: normal boot sequence
#   GRUB error / fstab error: disk or volume mount failed
#   cloud-init: cloud-init failure (SSH key injection, disk resize)

# Enable boot diagnostics if not already enabled (requires storage account)
az vm boot-diagnostics enable --name <vm-name> -g <rg> \
  --storage "https://<sa-name>.blob.core.windows.net"

# Get boot diagnostics screenshot (PNG of the VM console)
az vm boot-diagnostics get-boot-log-uri --name <vm-name> -g <rg>
```


```text title="Expected output"
{
  "consoleLogBlob": "https://diagstorage.blob.core.windows.net/bootdiagnostics-myvm-abc123/myvm.serialconsole.log",
  "value": "[    0.000000] Linux version 5.10.0-28-generic (buildd@lcy02-amd64-030) (gcc-10 (Debian 10.2.1-6) 10.2.1 20210110, GNU ld (GNU Binutils for Debian) 2.35.2) #30-Ubuntu SMP Tue Apr 18 12:12:47 UTC 2023 (Ubuntu 5.10.0-28.30-generic 5.10.104)\n[    0.000000] Command line: BOOT_IMAGE=/boot/vmlinuz-5.10.0-28-generic root=UUID=a1b2c3d4-e5f6-7890-abcd-ef1234567890 ro quiet splash\n[    0.000000] KERNEL supported cpus:\n[    0.000000]   Intel GenuineIntel\n[    0.000000]   AMD AuthenticAMD\n[    0.000000]   Hygon HygonGenuine\n[    0.000000]   Centaur CentaurHauls\n[    0.000000]   zhaoxin   Shanghai\n[    0.000000] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'\n[    0.000000] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'\n[    0.000000] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'\n[    0.000000] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256\n[    0.000000] x86/fpu: Enabled xstate features 0x7: 'SSE registers' 'AVX registers' 'x87 floating point registers'\n[    0.000000] BIOS-provided physical RAM map:\n[    0.000000] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable\n[    0.000000] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved\n..."
}

Boot diagnostics enabled on VM 'myvm' in resource group 'prod-rg'.

{
  "consoleScreenshotBlobUri": "https://diagstorage.blob.core.windows.net/bootdiagnostics-myvm-abc123/myvm.screenshot.bmp"
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ResourceNotFound: The Resource 'Microsoft.Compute/virtualMachines/myvm' under resource group 'prod-rg' was not found.` | Verify the VM name and resource group name are correct using `az vm list -g <rg>`. |
    | `StorageAccountNotFound: The storage account 'diagstorage' was not found in the current subscription.` | Ensure the storage account exists in |
---

## Step 4 — Check NSG and routing

```bash
# Show effective NSG rules applied to a VM's NIC
az network nic show-effective-nsg --name <nic-name> -g <rg>
# Columns: name, protocol, sourcePort, destinationPort, access (Allow/Deny), priority
# Look for: a Deny rule that matches the traffic you expect to be allowed

# Get the NIC name if unknown
az network nic list --query "[?virtualMachine.id contains '${VM_NAME}'].{name: name, rg: resourceGroup}" -o table

# Test connectivity from a source VM to a destination
az network watcher test-connectivity \
  --source-resource <source-vm-resource-id> \
  --dest-address <destination-ip-or-fqdn> \
  --dest-port 443
# Returns: connectionStatus (Reachable/Unreachable), hop-by-hop path, and latency

# Show effective routes on a NIC (to find blackhole routes)
az network nic show-effective-route-table --name <nic-name> -g <rg> -o table
# Look for: nextHopType = None (blackhole); addressPrefix matching your destination

# Start a packet capture on a VM (requires Network Watcher extension on VM)
az network watcher packet-capture create \
  --vm <vm-name> -g <rg> \
  --name diag-capture \
  --storage-account <sa-name> \
  --filters '[{"protocol":"TCP","localIPAddress":"","localPort":"","remoteIPAddress":"","remotePort":"443"}]'
```


```text title="Expected output"
$ az network nic show-effective-nsg --name nic-prod-vm01 -g rg-network
Name                            Protocol    SourcePort    DestinationPort    Access    Priority
──────────────────────────────  ──────────  ────────────  ─────────────────  ────────  ──────────
AllowHTTPS                      Tcp         *             443                Allow     100
DenyAllInbound                  *           *             *                  Deny      65000
AllowSSH                        Tcp         *             22                 Allow     110

$ az network nic list --query "[?virtualMachine.id contains 'prod-vm01'].{name: name, rg: resourceGroup}" -o table
Name              Rg
────────────────  ──────────────
nic-prod-vm01     rg-network
nic-prod-vm01-2   rg-network

$ az network watcher test-connectivity --source-resource /subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-network/providers/Microsoft.Compute/virtualMachines/source-vm --dest-address 10.2.1.50 --dest-port 443
ConnectionStatus    Hops                                                          AvgLatencyInMs
──────────────────  ────────────────────────────────────────────────────────────  ────────────────
Reachable           [{"address":"10.1.0.1","id":"0","resourceId":"","nextHopId":"1","previousHopId":"","issues":[]}]    12

$ az network nic show-effective-route-table --name nic-prod-vm01 -g rg-network -o table
Source    State    AddressPrefix      NextHopType       NextHopIpAddress
────────  ───────  ─────────────────  ────────────────  ──────────────────
Default   Active   10.0.0.0/16        VnetLocal
Default   Active   10.2.0.0/16        VirtualAppliance  10.1.0.4
Default   Active   0.0.0.0/0          Internet
User      Active   192.168.0.0/16     None

$ az network watcher packet-capture create --vm prod-vm01 -g rg-network --name diag-capture --storage-account sadiag2024 --filters '[{"protocol":"TCP","localIPAddress":"","localPort":"","remoteIPAddress":"","remotePort":"443"}]'
{
  "bytesPerPacket": 0,
  "etag": "W/\"a1b2c3d4-e5f6-7890-abcd-ef1234567890\"",
  "filters": [
    {
      "localIPAddress": "",
      "localPort": "",
      "protocol": "TCP",
      "remoteIPAddress": "",
      "remotePort": "443"
    }
  ],
  "id": "/subscriptions/12345678-1234-1234-1234-123456789012/resourceGroups/rg-network/providers/Microsoft.Network/networkWatchers/NetworkWatcher_eastus/packetCaptures/diag-capture",
  "name": "
```
---

## Step 5 — Check Activity Log for recent changes

```bash
# Last 50 events in the subscription (sorted by most recent)
az monitor activity-log list --max-events 50 \
  --query '[*].[eventTimestamp,level,operationName.localizedValue,resourceGroupName,status.localizedValue]' \
  -o table

# Filter by resource group and time window
az monitor activity-log list \
  --resource-group <rg> \
  --start-time "2026-06-15T08:00:00Z" \
  --end-time   "2026-06-15T12:00:00Z" \
  --query '[*].[eventTimestamp,caller,operationName.localizedValue,status.localizedValue]' \
  -o table

# Filter for failed operations only
az monitor activity-log list --resource-group <rg> --max-events 100 \
  --query '[?status.value==`Failed`].[eventTimestamp,caller,operationName.localizedValue,properties.statusCode]' \
  -o table

# Look for: who made a change (caller), what operation (operationName), when (eventTimestamp)
# Common patterns: NSG rule updates, VM extensions deployed/failed, scale events
```


```text title="Expected output"
EventTimestamp                    Level      OperationName                ResourceGroup      Status
2026-06-15T11:47:23.456789Z      Information Microsoft.Compute/virtualMachines/write vm-prod-rg      Succeeded
2026-06-15T11:32:15.123456Z      Warning    Microsoft.Network/networkSecurityGroups/securityRules/write network-rg      Succeeded
2026-06-15T11:15:42.789012Z      Error      Microsoft.Compute/virtualMachines/extensions/write vm-prod-rg      Failed
2026-06-15T10:58:09.345678Z      Information Microsoft.Storage/storageAccounts/write storage-rg      Succeeded
2026-06-15T10:42:33.901234Z      Information Microsoft.Sql/servers/databases/write db-rg      Succeeded
...

EventTimestamp                    Caller                         OperationName                Status
2026-06-15T09:23:11.567890Z      user@contoso.com               Microsoft.Network/networkSecurityGroups/securityRules/write Succeeded
2026-06-15T09:15:44.234567Z      automation-svc@contoso.onmicrosoft.com Microsoft.Compute/virtualMachines/restart/action Succeeded

EventTimestamp                    Caller                         OperationName                StatusCode
2026-06-15T11:15:42.789012Z      devops-agent@contoso.onmicrosoft.com Microsoft.Compute/virtualMachines/extensions/write 409
2026-06-15T10:22:18.456789Z      user@contoso.com               Microsoft.Authorization/roleAssignments/write 403
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `The subscription has no activity logs matching the specified criteria.` | Verify the time window is correct and the resource group exists; activity logs are retained for 90 days. |
    | `Invalid query string: [?status.value==\`Failed\`]` | Use `status.localizedValue=='Failed'` instead of `status.value==\`Failed\`` in the JMESPath query. |
    | `ResourceGroupNotFound: Resource group '<rg>' could not be found.` | Replace `<rg>` with an actual resource group name from your subscription using `az group list`. |
---

## Step 6 — Query Log Analytics

```kusto
// VM heartbeat — find VMs that stopped reporting (may indicate crash or agent failure)
Heartbeat
| summarize LastSeen = max(TimeGenerated) by Computer
| where LastSeen < ago(5m)
| order by LastSeen asc

// Failed Windows logins (brute force indicator)
SecurityEvent
| where EventID == 4625
| summarize count() by Account, IpAddress, Computer
| order by count_ desc

// NSG denied flows (requires NSG flow logs enabled)
AzureNetworkAnalytics_CL
| where SubType_s == "FlowLog" and FlowStatus_s == "D"
| project TimeGenerated, SrcIP_s, DestIP_s, DestPort_d, NSGName_s, NSGRule_s
| order by TimeGenerated desc

// VM CPU and memory (requires Azure Monitor agent)
Perf
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

---

## Step 7 — Check Key Vault access

```bash
# Verify Key Vault is accessible and show its state
az keyvault show --name <kv-name> -o json
# Check: properties.provisioningState = Succeeded; properties.enableSoftDelete = true

# List access policies (RBAC-disabled vaults)
az keyvault show --name <kv-name> \
  --query 'properties.accessPolicies[].{objectId:objectId,permissions:permissions}' -o table

# Check Key Vault firewall rules
az keyvault show --name <kv-name> --query 'properties.networkAcls' -o json
# If networkAcls.defaultAction = Deny: the caller's IP must be in ipRules or bypass = AzureServices

# Check RBAC permissions for a specific principal (RBAC-enabled vaults)
az role assignment list --scope "/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.KeyVault/vaults/<kv>" \
  --assignee <object-id-or-upn> -o table

# Test reading a secret from the Key Vault
az keyvault secret show --vault-name <kv-name> --name <secret-name>
# Error 403 = RBAC or access policy missing; Error 404 = secret does not exist
```


```text title="Expected output"
{
  "id": "/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001",
  "location": "eastus",
  "name": "prod-kv-001",
  "properties": {
    "accessPolicies": [],
    "enableSoftDelete": true,
    "enablePurgeProtection": true,
    "provisioningState": "Succeeded",
    "sku": {
      "family": "A",
      "name": "standard"
    },
    "tenantId": "72f988bf-86f1-41af-91ab-2d7cd011db47",
    "networkAcls": {
      "bypass": "AzureServices",
      "defaultAction": "Deny",
      "ipRules": [
        {
          "value": "203.0.113.45"
        }
      ],
      "virtualNetworkRules": []
    }
  }
}

ObjectId                             Permissions
-----------------------------------  -----------------------------------------------
a1b2c3d4-e5f6-7890-abcd-ef1234567890  {keys: [get, list], secrets: [get, list]}
b2c3d4e5-f6a7-8901-bcde-f12345678901  {keys: [get, list, create], secrets: [get, list]}

RoleAssignmentId                                                          RoleDefinitionName              Scope
------------------------------------------------------------------------  ------------------------------  -----------------------------------------------
/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/providers/Microsoft.Authorization/roleAssignments/abc12345-def6-7890-ghij-klmnopqrstuv  Key Vault Secrets User         /subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001
/subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/providers/Microsoft.Authorization/roleAssignments/def67890-ghi1-2345-ijkl-mnopqrstuvwx  Key Vault Administrator        /subscriptions/12a34b56-c789-0d12-e345-f67890abcdef/resourceGroups/prod-rg/providers/Microsoft.KeyVault/vaults/prod-kv-001

{
  "attributes": {
    "created": 1704067200,
    "enabled": true,
    "expires": null,
    "notBefore": null,
    "recoveryLevel": "Recoverable+Purgeable",
    "updated": 1704067200
  },
  "id": "https://prod-kv-001.vault.azure.net/secrets/db-password/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "name": "db-password",
  "value": "***"
}
```

!!! warning "Common errors"
    **`
---

## Log locations

| Source | Command / Location | What to look for |
|---|---|---|
| Boot diagnostics | `az vm boot-diagnostics get-boot-log` | OS crash, fstab, kernel panic |
| Activity Log | `az monitor activity-log list` | Recent changes: NSG rules, deployments |
| VM guest OS | `az vm run-command invoke` or SSH | Application errors, OS-level issues |
| Log Analytics | KQL via portal or `az monitor log-analytics query` | Heartbeat, security events, performance |
| NSG flow logs | `AzureNetworkAnalytics_CL` in Log Analytics | Denied flows, source/destination |
| Azure Service Health | `az monitor service-health alert list` | Platform-level incidents |

---

## See also

- [Azure — Common Issues](../common-issues/)
- [Azure — Escalation](../escalation/)
- [Azure — Health Checks](../../operations/health-checks/)

## Verify resolution

- `az vm get-instance-view` shows `displayStatus: VM running` and guest agent `Provisioning succeeded`
- `az network watcher test-connectivity` returns `connectionStatus: Reachable` for the previously failing path
- Log Analytics `Heartbeat` query shows the VM appearing with `TimeGenerated` within the last 5 minutes
- The original application error does not recur for 15 minutes after the fix
- Activity Log shows no new Failed operations on the affected resource after the fix
