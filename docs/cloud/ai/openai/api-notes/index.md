---
tags:
  - openai
  - ai
description: "Practical notes on authenticating to the OpenAI API, working with rate limits, counting tokens, handling errors, and choosing the right API endpoint."
---
# OpenAI API Notes

<div class="kb-summary">
Practical notes on authenticating to the OpenAI API, working with rate limits, counting tokens, handling errors, and choosing the right API endpoint.

*Applies to: OpenAI API*
</div>

```d2
direction: down

authentication: "Authentication" {shape: rectangle}
rate_limits: "Rate Limits" {shape: rectangle}
token_counting: "Token Counting" {shape: rectangle}
error_codes: "Error Codes" {shape: rectangle}
retry_with_exponential_backoff: "Retry with Exponential Backoff" {shape: rectangle}
choosing_the_right_model: "Choosing the Right Model" {shape: rectangle}

authentication -> rate_limits: uses
rate_limits -> token_counting: uses
token_counting -> error_codes: uses
error_codes -> retry_with_exponential_backoff: uses
retry_with_exponential_backoff -> choosing_the_right_model: uses
```

## Authentication

```bash
# Set API key in environment (never hardcode)
export OPENAI_API_KEY="sk-..."

# Test authentication
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | jq '.data[].id' | head -10
```

```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# For org-scoped billing
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    organization="org-xxxxxxxxxxxx"
)
```

Use project API keys (prefixed `sk-proj-`) for new integrations — they scope access to a specific project and support finer-grained permissions.

## Rate Limits

OpenAI enforces rate limits in tokens per minute (TPM) and requests per minute (RPM) per model. Limits vary by tier.

| Tier | RPM (GPT-4o) | TPM (GPT-4o) | Notes |
|---|---|---|---|
| Free | 3 | 40,000 | Development only |
| Tier 1 | 500 | 200,000 | $5+ spent |
| Tier 2 | 5,000 | 2,000,000 | $50+ spent |
| Tier 3 | 5,000 | 5,000,000 | $100+ spent |
| Tier 4 | 10,000 | 10,000,000 | $250+ spent |
| Tier 5 | 10,000 | 30,000,000 | $1,000+ spent |

Rate limit info is returned in response headers:

```bash
curl -i https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o-mini","messages":[{"role":"user","content":"Hi"}]}' \
  2>&1 | grep -i "x-ratelimit"
```


```text title="Expected output"
HTTP/2 200
x-ratelimit-limit-requests: 10000
x-ratelimit-limit-tokens: 2000000
x-ratelimit-remaining-requests: 9999
x-ratelimit-remaining-tokens: 1999994
x-ratelimit-reset-requests: 6s
x-ratelimit-reset-tokens: 1m23s
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.openai.com`** — Verify network connectivity and DNS resolution with `nslookup api.openai.com` or check firewall/proxy settings.
    **`HTTP/2 401 Unauthorized`** — Confirm `$OPENAI_API_KEY` is set correctly with `echo $OPENAI_API_KEY` and verify the key hasn't been revoked in your OpenAI account.
    **`HTTP/2 429 Too Many Requests`** — Wait for the duration specified in `x-ratelimit-reset-requests` header before retrying, or upgrade your API plan.
## Token Counting

Estimate token counts before sending requests to avoid `context_length_exceeded` errors.

```python
import tiktoken

def count_tokens(messages: list[dict], model: str = "gpt-4o") -> int:
    enc = tiktoken.encoding_for_model(model)
    tokens = 0
    for msg in messages:
        tokens += 4  # per-message overhead
        for key, value in msg.items():
            tokens += len(enc.encode(str(value)))
            if key == "name":
                tokens -= 1  # name field saves one token
    tokens += 2  # reply primer
    return tokens

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
print(count_tokens(messages))  # ~28 tokens
```

## Error Codes

| HTTP Status | Error Type | Meaning | Action |
|---|---|---|---|
| 400 | `invalid_request_error` | Bad request body | Fix the request |
| 401 | `authentication_error` | Invalid API key | Check key, not expired |
| 403 | `permission_error` | Org/project restriction | Check API key scope |
| 429 | `rate_limit_error` | TPM or RPM exceeded | Retry with backoff |
| 500 | `api_error` | OpenAI server error | Retry with backoff |
| 503 | `api_unavailable` | Service unavailable | Retry later |

## Retry with Exponential Backoff

```python
import time, random
from openai import OpenAI, RateLimitError, APIError

client = OpenAI()

def call_with_retry(messages, model="gpt-4o", max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages
            )
        except RateLimitError:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Waiting {wait:.1f}s (attempt {attempt+1})")
            time.sleep(wait)
        except APIError as e:
            if e.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
    raise RuntimeError("Max retries exceeded")
```

## Choosing the Right Model

| Model | Context | Best For | Cost (input/output per 1M) |
|---|---|---|---|
| gpt-4o | 128K | Complex reasoning, vision | $2.50 / $10.00 |
| gpt-4o-mini | 128K | Simple tasks, high volume | $0.15 / $0.60 |
| o1 | 200K | Deep reasoning, math | $15.00 / $60.00 |
| o3-mini | 200K | Fast reasoning tasks | $1.10 / $4.40 |
| text-embedding-3-large | 8K | Embeddings (3072 dims) | $0.13 |
| text-embedding-3-small | 8K | Embeddings (1536 dims) | $0.02 |
