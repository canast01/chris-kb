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
