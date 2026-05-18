# Azure — Diagnostics

```
┌──────────────────────────────────────────────────────────────┐
│               Azure Diagnostics — Data Sources                 │
└──────────────────────────────────────────────────────────────┘

  Resource Under Investigation
            │
  ┌─────────┴──────────────────────────────────────────────┐
  │                                                         │
  ▼                     ▼                    ▼             ▼
┌──────────────┐  ┌───────────────┐  ┌─────────────┐  ┌──────────┐
│ Activity Log │  │Resource Health│  │  Network    │  │  Log     │
│ (control     │  │(is the        │  │  Watcher    │  │Analytics │
│  plane ops)  │  │ resource up?) │  │ (NSG/routes │  │(Insights,│
│              │  │               │  │  + capture) │  │ KQL)     │
└──────┬───────┘  └───────┬───────┘  └──────┬──────┘  └────┬─────┘
       └──────────────────┴─────────────────┴──────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  Correlate findings  │
                         │  → root cause        │
                         └──────────────────────┘
```

> Diagnostic commands, log locations, and data collection procedures.

---

## VM Diagnostics

```bash
# Boot diagnostics (serial console log)
az vm boot-diagnostics get-boot-log --name <vm-name> -g <rg>

# Instance view — power state, extensions, disks
az vm get-instance-view --name <vm-name> -g <rg> --output json

# Effective NSG rules on a NIC
az network nic show-effective-nsg --name <nic-name> -g <rg>

# Effective routes on a NIC
az network nic show-effective-route-table --name <nic-name> -g <rg>

# Network Watcher — test connectivity
az network watcher test-connectivity \
  --source-resource <source-vm-id> \
  --dest-address <destination-ip> --dest-port 443

# Packet capture
az network watcher packet-capture create \
  --vm <vm-name> -g <rg> --name my-capture --storage-account <sa>
```

## Activity Log

```bash
# Last 50 events
az monitor activity-log list --max-events 50 \
  --query '[*].[eventTimestamp,level,operationName.localizedValue,status.localizedValue]' \
  -o table

# Filter by resource group and time window
az monitor activity-log list \
  --resource-group <rg> \
  --start-time <start-utc> \
  --end-time <end-utc> \
  --output json
```

## Log Analytics Queries

```kusto
-- VM heartbeat (last seen)
Heartbeat
| summarize LastSeen = max(TimeGenerated) by Computer
| where LastSeen < ago(5m)

-- Failed logins
SecurityEvent
| where EventID == 4625
| summarize count() by Account, IpAddress

-- NSG denied flows
AzureNetworkAnalytics_CL
| where SubType_s == "FlowLog" and FlowStatus_s == "D"
| project TimeGenerated, SrcIP_s, DestIP_s, DestPort_d, NSGName_s, NSGRule_s
```

## Key Vault Diagnostics

```bash
# Check Key Vault accessibility
az keyvault show --name <kv-name> --query 'properties.provisioningState'

# List access policies
az keyvault show --name <kv-name> --query 'properties.accessPolicies'

# Check firewall rules
az keyvault show --name <kv-name> --query 'properties.networkAcls'
```
