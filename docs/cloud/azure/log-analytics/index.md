# Log Analytics

Azure Log Analytics — workspace for collecting, querying, and alerting on logs from Azure and on-premises sources.
## Key Concepts

| Concept | Description |
|---|---|
| Workspace | Central repository for log data |
| KQL | Kusto Query Language — used to query log data |
| Data source | Diagnostic settings, agents, connectors feeding data in |
| Sentinel | Microsoft SIEM/SOAR built on Log Analytics |
| Saved queries | Reusable KQL queries stored in the workspace |
| Workspace transformation | Filter/transform data before ingestion |

## Common Azure CLI Commands

```bash
# List Log Analytics workspaces
az monitor log-analytics workspace list \
  --query '[*].{Name:name,RG:resourceGroup,Location:location,RetentionDays:retentionInDays}' -o table

# Run a KQL query from CLI
az monitor log-analytics query \
  -w <workspace-id> \
  --analytics-query "Heartbeat | summarize count() by Computer | sort by count_ desc | take 10"

# Show workspace details
az monitor log-analytics workspace show -g <rg> -n <workspace-name>
```

## Key KQL Queries

**Heartbeat — check which agents reported recently:**
```kql
Heartbeat
| where TimeGenerated > ago(1h)
| summarize LastHeartbeat=max(TimeGenerated) by Computer
| where LastHeartbeat < ago(15m)
| order by LastHeartbeat asc
```

**Find errors across all logs:**
```kql
search "error" or "ERROR"
| where TimeGenerated > ago(1h)
| project TimeGenerated, Type, _ResourceId, Computer, Message=tostring(split($table, " "))
| sort by TimeGenerated desc
| take 100
```

**VM performance — CPU over 80%:**
```kql
Perf
| where ObjectName == "Processor" and CounterName == "% Processor Time"
| where CounterValue > 80
| summarize avg(CounterValue) by Computer, bin(TimeGenerated, 5m)
| sort by TimeGenerated desc
```

**Disk free space alerts:**
```kql
Perf
| where ObjectName == "LogicalDisk" and CounterName == "% Free Space"
| where CounterValue < 20
| summarize min(CounterValue) by Computer, InstanceName
```

**Security events — failed logons:**
```kql
SecurityEvent
| where EventID == 4625
| summarize FailedLogons=count() by Account, Computer, bin(TimeGenerated, 1h)
| sort by FailedLogons desc
```

**Azure activity — who deleted what:**
```kql
AzureActivity
| where OperationNameValue has "delete" and ActivityStatusValue == "Success"
| project TimeGenerated, Caller, OperationNameValue, ResourceGroup, Resource
| sort by TimeGenerated desc
```

## Create Alert Rule from Query

```bash
# Create a scheduled alert rule (30-min check, alert if >10 results)
az monitor scheduled-query create \
  -g <rg> \
  -n "High-CPU-Alert" \
  --scopes /subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.OperationalInsights/workspaces/<workspace> \
  --condition "count > 10" \
  --condition-query "Perf | where CounterName == '% Processor Time' and CounterValue > 80" \
  --evaluation-frequency 5m \
  --window-size 30m \
  --severity 2 \
  --action-groups <action-group-id>
```

## Data Retention

```bash
# Set workspace retention (max 730 days for hot storage; archive beyond)
az monitor log-analytics workspace update \
  -g <rg> -n <workspace-name> \
  --retention-time 90
```

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Missing data from a VM | Agent running? | Check MMA or AMA agent status; verify workspace ID and key |
| Query returns no results | Table exists? | Run `search *` to confirm data is present; check time range |
| High ingestion costs | Top tables by volume | `Usage | summarize sum(Quantity) by DataType | sort by sum_Quantity desc` |
| Alert not firing | Threshold correct? | Test query in portal; verify evaluation window covers the event window |
