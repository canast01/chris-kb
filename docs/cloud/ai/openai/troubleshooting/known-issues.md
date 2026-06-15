---
tags:
  - troubleshooting
  - openai
  - cloud
  - ai
  - known-issues
---
# OpenAI API — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known OpenAI API bugs, error codes, and workarounds covering rate limits, API errors, and model availability.

*Applies to: OpenAI API (platform.openai.com)*
</div>

```text
┌─────────────────────────────────────────── Cloud Ai Openai ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  Ai: Cloud Ai Openai platform                                 │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                         Management: Cloud Ai Openai management console                        │   │
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
│    Physical: Cloud Ai Openai infrastructure · management network · monitoring                         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Ai                 = Cloud Ai Openai platform overview and core concepts                           │
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


## Before you begin

- OpenAI errors appear in API responses as JSON with `error.code` and `error.message`.
- Check `status.openai.com` for service-level incidents before debugging.
- Rate limit headers: `x-ratelimit-remaining-requests`, `x-ratelimit-remaining-tokens`.

## Rate Limits

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| 429 `rate_limit_exceeded` | Too many requests | Exceeded RPM or TPM limit for your tier | Implement exponential backoff; upgrade API tier; use request batching |
| 429 `insufficient_quota` | API quota exhausted | Monthly usage limit reached | Add credits to OpenAI account; upgrade plan |

## API Errors

| Error Code | Description | Cause | Fix |
|---|---|---|---|
| 400 `context_length_exceeded` | Prompt too long for model | Token count exceeds model context window | Truncate prompt; use chunking; switch to model with larger context |
| 401 `invalid_api_key` | API key invalid | Wrong key or key revoked | Regenerate API key in platform.openai.com → API Keys |
| 500 `internal_server_error` | OpenAI server error | Transient service issue | Retry with backoff; check status.openai.com |
| 503 `engine_overloaded` | Model capacity saturated | High demand period | Retry with exponential backoff; use alternate model |

## Model Availability

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Model deprecated — API returning `model_not_found` | All | Model retired by OpenAI | Update model parameter to supported version; check deprecation schedule | N/A |

## See also

- [OpenAI — Common Issues](common-issues.md)
