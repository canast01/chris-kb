---
tags:
  - azure
  - ai
---
# Azure OpenAI Monitoring

<div class="kb-summary">
Azure OpenAI integrates with Azure Monitor for metrics, logs, and alerting. Monitoring covers request volume, latency, token usage, error rates, and content filtering events.

*Applies to: Azure OpenAI*
</div>

```d2
direction: right

azure_monitor_metrics: "Azure Monitor Metrics" {shape: rectangle}
key_metrics: "Key Metrics" {shape: rectangle}
diagnostic_logs: "Diagnostic Logs" {shape: rectangle}
log_analytics_queries: "Log Analytics Queries" {shape: rectangle}
content_filtering_logs: "Content Filtering Logs" {shape: rectangle}
alerts: "Alerts" {shape: rectangle}

azure_monitor_metrics -> key_metrics
key_metrics -> diagnostic_logs
diagnostic_logs -> log_analytics_queries
log_analytics_queries -> content_filtering_logs
content_filtering_logs -> alerts
```

## Azure Monitor Metrics

Metrics are available under the Cognitive Services resource type in Azure Monitor. No configuration is needed — metrics stream automatically.

```bash
# Get request count over the last hour using az CLI
az monitor metrics list \
  --resource "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource" \
  --metric "AzureOpenAIRequests" \
  --interval PT5M \
  --start-time $(date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --aggregation Total \
  --output table
```


```text title="Expected output"
Name                 Aggregation    ResourceId                                                                                          StartTime              EndTime                Value
-------------------  -----------    ---------------------------------------------------------------------------------------------------------  ---------------------  ---------------------  -------
AzureOpenAIRequests  Total          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource  2024-01-15T14:32:00Z   2024-01-15T14:37:00Z   142
AzureOpenAIRequests  Total          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource  2024-01-15T14:37:00Z   2024-01-15T14:42:00Z   156
AzureOpenAIRequests  Total          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource  2024-01-15T14:42:00Z   2024-01-15T14:47:00Z   128
AzureOpenAIRequests  Total          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource  2024-01-15T14:47:00Z   2024-01-15T14:52:00Z   171
AzureOpenAIRequests  Total          /subscriptions/a1b2c3d4-e5f6-7890-abcd-ef1234567890/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource  2024-01-15T14:52:00Z   2024-01-15T14:57:00Z   149
...
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource '/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource' could not be found.`** — Replace SUB_ID with your actual subscription ID and verify the resource group and account names exist.
    **`AuthorizationFailed: The client 'user@example.com' with object id 'xxx' does not have authorization to perform action 'Microsoft.Insights/metrics/read' over scope '/subscriptions/...'.`** — Assign the "Monitoring Reader" role to your user or service principal on the Azure OpenAI resource.
## Key Metrics

| Metric Name | Unit | Description |
|---|---|---|
| `AzureOpenAIRequests` | Count | Total API requests |
| `AzureOpenAISuccessfulRequests` | Count | Requests with 2xx response |
| `AzureOpenAIThrottledRequests` | Count | Requests rejected with 429 |
| `AzureOpenAIGeneratedTokens` | Count | Output tokens generated |
| `AzureOpenAIPromptTokens` | Count | Input tokens consumed |
| `AzureOpenAIServerErrors` | Count | 5xx errors |
| `AzureOpenAIFineTunedModelRequests` | Count | Requests to fine-tuned models |

Filter by `DeploymentName` dimension to get per-deployment breakdowns.

## Diagnostic Logs

Enable diagnostic settings to send request logs to a Log Analytics workspace or storage account.

```bash
az monitor diagnostic-settings create \
  --name aoai-logs \
  --resource "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource" \
  --workspace "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.OperationalInsights/workspaces/my-law" \
  --logs '[
    {"category":"Audit","enabled":true},
    {"category":"RequestResponse","enabled":true}
  ]' \
  --metrics '[{"category":"AllMetrics","enabled":true}]'
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/resourcegroups/my-rg/providers/microsoft.cognitiveservices/accounts/my-aoai-resource/diagnosticsettings/aoai-logs",
  "identity": null,
  "kind": null,
  "location": null,
  "name": "aoai-logs",
  "properties": {
    "logs": [
      {
        "category": "Audit",
        "categoryGroup": null,
        "enabled": true,
        "retentionPolicy": {
          "days": 0,
          "enabled": false
        }
      },
      {
        "category": "RequestResponse",
        "categoryGroup": null,
        "enabled": true,
        "retentionPolicy": {
          "days": 0,
          "enabled": false
        }
      }
    ],
    "metrics": [
      {
        "category": "AllMetrics",
        "enabled": true,
        "retentionPolicy": {
          "days": 0,
          "enabled": false
        }
      }
    ],
    "workspaceId": "/subscriptions/a1b2c3d4-e5f6-4a5b-9c8d-7e6f5a4b3c2d/resourcegroups/my-rg/providers/microsoft.operationalinsights/workspaces/my-law"
  },
  "resourceGroup": "my-rg",
  "type": "Microsoft.Insights/diagnosticSettings"
}
```

!!! warning "Common errors"
    **`ResourceNotFound: The resource '/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource' could not be found.`** — Verify the subscription ID, resource group name, and Azure OpenAI resource name are correct using `az cognitiveservices account list -g my-rg`.
    **`InvalidResourceId: The provided resource ID is malformed or does not exist.`** — Ensure the workspace resource ID path uses correct casing and that the Log Analytics Workspace exists in the same subscription using `az monitor log-analytics workspace list -g my-rg`.
    **`BadRequest: Invalid JSON in logs or metrics parameter.`** — Validate JSON syntax by removing trailing commas and ensuring all quotes are properly escaped; test with `echo '[{"category":"Audit","enabled":true}]' | jq .` before running the command.
`RequestResponse` logs capture model, deployment, token counts, latency, and status for every request.

## Log Analytics Queries

```kusto
// Top deployments by token usage in the last 24 hours
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| where OperationName == "ChatCompletions_Create"
| summarize
    TotalPromptTokens = sum(toint(properties_s_prompt_tokens_d)),
    TotalCompletionTokens = sum(toint(properties_s_completion_tokens_d)),
    RequestCount = count()
  by DeploymentId = properties_s_deployment_id_s
| order by TotalCompletionTokens desc

// Error rate by deployment
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| summarize
    Total = count(),
    Errors = countif(ResultType == "Failed")
  by DeploymentId = properties_s_deployment_id_s
| extend ErrorRate = round(100.0 * Errors / Total, 2)
```

## Content Filtering Logs

When content filtering blocks a request, a `content_filter_result` field appears in the log entry. Query for filter events:

```kusto
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.COGNITIVESERVICES"
| where properties_s_finish_reason_s == "content_filter"
| project TimeGenerated, DeploymentId = properties_s_deployment_id_s,
          Category = properties_s_content_filter_category_s,
          Severity = properties_s_content_filter_severity_s
| order by TimeGenerated desc
```

## Alerts

```bash
# Alert when throttled requests exceed 50 in 5 minutes
az monitor metrics alert create \
  --name "aoai-throttle-alert" \
  --resource-group my-rg \
  --scopes "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource" \
  --condition "total AzureOpenAIThrottledRequests > 50" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action "/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.Insights/actionGroups/pagerduty-ag"
```


```text title="Expected output"
{
  "id": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-rg/providers/Microsoft.Insights/metricAlerts/aoai-throttle-alert",
  "location": "global",
  "name": "aoai-throttle-alert",
  "resourceGroup": "my-rg",
  "type": "Microsoft.Insights/metricAlerts",
  "description": null,
  "enabled": true,
  "scopes": [
    "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource"
  ],
  "evaluationFrequency": "PT1M",
  "windowSize": "PT5M",
  "criteria": {
    "allOf": [
      {
        "name": "AzureOpenAIThrottledRequests",
        "metricName": "AzureOpenAIThrottledRequests",
        "operator": "GreaterThan",
        "threshold": 50.0,
        "timeAggregation": "Total"
      }
    ],
    "odata.type": "Microsoft.Azure.Monitor.MultipleResourceMultipleMetricCriteria"
  },
  "actions": [
    {
      "actionGroupId": "/subscriptions/a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d/resourceGroups/my-rg/providers/Microsoft.Insights/actionGroups/pagerduty-ag"
    }
  ]
}
```

!!! warning "Common errors"
    **`ResourceNotFound : The resource '/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource' could not be found.`** — Replace `SUB_ID` with your actual subscription ID and verify the Azure OpenAI resource name matches exactly.
    **`InvalidParameter : The metric 'AzureOpenAIThrottledRequests' is not supported for this resource type.`** — Verify the metric name is correct by running `az monitor metrics list-definitions --resource /subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.CognitiveServices/accounts/my-aoai-resource`.
    **`ResourceNotFound : The action group '/subscriptions/SUB_ID/resourceGroups/my-rg/providers/Microsoft.Insights/actionGroups/pagerduty-ag' does not exist.`** — Create the action group first with `az monitor action-group create` or verify the name and subscription ID are correct.