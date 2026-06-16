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
┌───────────────────────────────────────────── OpenAI API ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Cloud LLM API — chat completions, embeddings, rate-limited per usage tier           │   │
│   │                          Protocols: HTTPS (TCP 443) to api.openai.com                         │   │
│   │                      Management: platform.openai.com dashboard / API keys                     │   │
│   │           API request -> Rate limit check -> Model inference -> Response -> Billing           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Access           │  │       API key / org ID      │  │     Per-project scoping     │   │
│   │             Tier            │  │          Usage tier         │  │    RPM/TPM scale w/ spend   │   │
│   │            Models           │  │     GPT-4o, GPT-4, etc.     │  │     Deprecation schedule    │   │
│   │           Billing           │  │         Token-based         │  │    Prompt+completion tok.   │   │
│   │            Status           │  │      status.openai.com      │  │   Check before deep debug   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │ Chat Completions │ Text generation  │       HTTPS       │     API key      │   Most common    │   │
│   │    Embeddings    │Vector generation │       HTTPS       │     API key      │   Used for RAG   │   │
│   │   Rate headers   │ Quota visibility │    HTTPS resp.    │       N/A        │  x-ratelimit-*   │   │
│   │    Batch API     │ Async bulk req.  │       HTTPS       │     API key      │   24h, cheaper   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: N/A — fully managed SaaS API, no customer-operated infrastructure                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  API key        = secret credential authenticating requests to the OpenAI API                         │
│  RPM/TPM        = Requests/Tokens Per Minute; the two rate limit dimensions                           │
│  Context window = max tokens (prompt+completion) a model can process at once                          │
│  Token          = sub-word text unit; billing and limits are measured in tokens                       │
│  Tier           = usage tier unlocked by cumulative spend, raises RPM/TPM                             │
│  Backoff        = retry strategy doubling wait time after each 429/500                                │
│  Deprecation    = OpenAI retires older models on a published schedule                                 │
│  Embedding      = vector representation of text for semantic search/RAG                               │
│  Batch API      = async bulk endpoint, discounted pricing, ~24h SLA                                   │
│  Function call  = model output structured to invoke a defined tool                                    │
│  Streaming      = token-by-token response via server-sent events                                      │
│  Org ID         = organization identifier scoping billing across API keys                             │
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
