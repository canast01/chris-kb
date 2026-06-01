# Azure OpenAI Monitoring


<div class="kb-summary">
Azure OpenAI integrates with Azure Monitor for metrics, logs, and alerting. Monitoring covers request volume, latency, token usage, error rates, and content filtering events.
</div>
```
┌───────────────────────────────────── Ai Azure Openai Monitoring ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Azure Openai: Ai Azure Openai Monitoring platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                   Management: Ai Azure Openai Monitoring management console                   │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
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
│    Physical: Ai Azure Openai Monitoring infrastructure · management network · monitoring              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure Openai       = Ai Azure Openai Monitoring platform overview and core concepts                │
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
