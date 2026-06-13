---
tags:
  - azure
  - troubleshooting
search:
  boost: 1.5
---
# Azure — Diagnostics


<div class="kb-summary">
Diagnostic commands, log locations, and data collection procedures.
</div>
```text
┌────────────────────────────── Cloud Azure Troubleshooting — Diagnostics ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Azure diagnostics: log collection, health checks, and performance analysis          │   │
│   │          Tools: management CLI, REST API, vendor support bundle, and system event log         │   │
│   │          Performance: check I/O latency, throughput, queue depth, and cache hit rate          │   │
│   │       Collect support bundle before contacting vendor support to reduce time-to-resolve       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify issue → collect logs → run diagnostics → analyse → resolve                                │
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
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Cloud Azure Troubleshooting infrastructure · management network · monitoring             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Cloud Azure Troubleshooting platform overview and core concepts               │
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
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
