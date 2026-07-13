---
tags:
  - troubleshooting
search:
  boost: 1.5
description: "Troubleshooting reference covering Error Code Reference, Rate Limit Troubleshooting, Token Limit Issues, Authentication Issues, Timeout and Latency and 3..."
---
# OpenAI API — Troubleshooting

<div class="kb-summary">
Troubleshooting reference covering Error Code Reference, Rate Limit Troubleshooting, Token Limit Issues, Authentication Issues, Timeout and Latency and 3 more sections.

*Applies to: OpenAI API*
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
error_code_reference: "Error Code Reference" {shape: rectangle}
rate_limit_troubleshooting: "Rate Limit Troubleshooting" {shape: rectangle}
token_limit_issues: "Token Limit Issues" {shape: rectangle}
authentication_issues: "Authentication Issues" {shape: rectangle}
timeout_and_latency: "Timeout and Latency" {shape: rectangle}
content_filtering_refusals: "Content Filtering / Refusals" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> error_code_reference: investigate
symptom -> rate_limit_troubleshooting: investigate
symptom -> token_limit_issues: investigate
symptom -> authentication_issues: investigate
symptom -> timeout_and_latency: investigate
symptom -> content_filtering_refusals: investigate
error_code_reference -> resolution
rate_limit_troubleshooting -> resolution
token_limit_issues -> resolution
authentication_issues -> resolution
timeout_and_latency -> resolution
content_filtering_refusals -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Error Code Reference

| HTTP code | Error type | Meaning | Fix |
|---|---|---|---|
| `401` | `invalid_api_key` | API key wrong or revoked | Verify key in platform.openai.com → API Keys |
| `429` | `rate_limit_exceeded` | Too many requests or tokens per minute | Back off and retry with exponential backoff |
| `429` | `insufficient_quota` | Billing limit reached | Add payment method / increase limit |
| `500` | `server_error` | OpenAI-side error | Retry with backoff; check status.openai.com |
| `503` | `engine_overloaded` | High load on OpenAI infrastructure | Retry with backoff |
| `400` | `context_length_exceeded` | Input exceeds model token limit | Truncate input or use a model with larger context |
| `400` | `invalid_request_error` | Malformed request body | Check JSON structure and required fields |

## Rate Limit Troubleshooting

```python
import openai, time, random

def call_with_backoff(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            return openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
        except openai.RateLimitError as e:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Retry {attempt+1}/{max_retries} in {wait:.1f}s")
            time.sleep(wait)
    raise RuntimeError("Max retries exceeded")
```

```bash
# Check your current tier limits
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -w "\nHTTP %{http_code}\n"

# RPM / TPM limits are shown in response headers on rate-limited calls:
# x-ratelimit-limit-requests: 500
# x-ratelimit-remaining-requests: 0
# x-ratelimit-reset-requests: 1s
```


```text title="Expected output"
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4-turbo",
      "object": "model",
      "created": 1704067755,
      "owned_by": "openai-internal"
    },
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai"
    },
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677649963,
      "owned_by": "openai-internal"
    }
  ]
}
HTTP 200
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: api.openai.com` | Verify network connectivity and DNS resolution with `nslookup api.openai.com` or check firewall/proxy settings. |
    | `{"error":{"message":"Incorrect API key provided. You passed an empty string as an API key.","type":"invalid_request_error"}}` | Ensure `$OPENAI_API_KEY` environment variable is set with `export OPENAI_API_KEY=sk-...` before running the command. |
    | `{"error":{"message":"You exceeded your current quota, please check your plan and billing settings.","type":"insufficient_quota"}}` | Check your OpenAI account billing status and upgrade your plan or add a payment method at https://platform.openai.com/account/billing/overview. |
Rate limit tiers are linked to usage spend. Limits increase automatically as cumulative API spend grows.

## Token Limit Issues

```python
import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")

def count_tokens(text: str) -> int:
    return len(enc.encode(text))

def truncate_to_limit(text: str, max_tokens: int = 100_000) -> str:
    tokens = enc.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
    return enc.decode(tokens)
```

| Model | Context window | Notes |
|---|---|---|
| gpt-4o | 128k tokens | ~96k words |
| gpt-4o-mini | 128k tokens | Cheaper; lower capability |
| gpt-4-turbo | 128k tokens | |
| gpt-3.5-turbo | 16k tokens | Legacy |
| o1, o3 | 200k tokens | Reasoning models |

## Authentication Issues

```bash
# Test key validity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
# 200 = valid; 401 = invalid key

# Common causes of auth failure:
# 1. Trailing whitespace in the key env var
echo -n "$OPENAI_API_KEY" | wc -c    # should be 51 chars for sk-... keys

# 2. Key belongs to a different org — set org header if needed
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: org-XXXXXXXXXX"

# 3. Key scope too narrow — verify permissions in platform.openai.com
```


```text title="Expected output"
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4-turbo",
      "object": "model",
      "created": 1694767490,
      "owned_by": "openai-dev"
    },
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai"
    },
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677649963,
      "owned_by": "openai-dev"
    }
  ]
}
51
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4-turbo",
      "object": "model",
      "created": 1694767490,
      "owned_by": "openai-dev"
    },
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai"
    },
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677649963,
      "owned_by": "openai-dev"
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `{"error":{"message":"Incorrect API key provided. You passed an empty string as an API key, but a string with 20+ characters was expected: . You can find your API key at https://platform.openai.com/account/api-keys.","type":"invalid_request_error","param":null,"code":"invalid_api_key"}}` | Verify `$OPENAI_API_KEY` is set with `echo "$OPENAI_API_KEY"` and reload your shell session if recently added to `.bashrc` or `.env`. |
    | `{"error":{"message":"You exceeded your current quota, please check your plan and billing settings.","type":"insufficient_quota","param":null,"code":"insufficient_quota"}}` | Check your OpenAI account billing status and ensure your payment method is valid at platform.openai.com/account/billing/overview. |
    | `{"error":{"message":"The organization ID provided in the request does not match the organization ID the API key belongs to.","type":"invalid_request_error","param":null,"code":"invalid_organization"}}` | Verify the `OpenAI-Organization` header matches your actual org ID from platform.openai.com/account/org-settings, or remove the header if using a personal API key. |
## Timeout and Latency

```python
import openai

client = openai.OpenAI(timeout=60.0)   # seconds; default is 600

# For long generations, use streaming to avoid timeout
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

Typical response times (p50):
- gpt-4o-mini: 1–5s for short responses
- gpt-4o: 3–30s depending on output length
- o1/o3: 10–120s (reasoning models think before responding)

## Content Filtering / Refusals

The API may return a response with `finish_reason: content_filter` when the output was blocked, or the message may contain a refusal.

```python
response = client.chat.completions.create(...)
choice = response.choices[0]

if choice.finish_reason == "content_filter":
    print("Response blocked by content policy")
elif choice.message.refusal:
    print(f"Model refused: {choice.message.refusal}")
else:
    print(choice.message.content)
```

## Checking OpenAI Status

```bash
# API status page
# https://status.openai.com

# Programmatic check
curl -s https://status.openai.com/api/v2/status.json \
  | python3 -c "import sys,json; s=json.load(sys.stdin); print(s['status']['description'])"
```


```text title="Expected output"
All Systems Operational
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (6) Could not resolve host: status.openai.com` | Verify network connectivity and DNS resolution with `ndig status.openai.com` or check if your firewall/proxy is blocking access to status.openai.com. |
    | `json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)` | The API endpoint returned empty or invalid JSON; try `curl -s https://status.openai.com/api/v2/status.json` alone to inspect the raw response. |
## Common Issues Reference

| Symptom | Cause | Fix |
|---|---|---|
| Responses cut off mid-sentence | `max_tokens` too low | Increase `max_tokens` or remove the parameter |
| Same response every time | `temperature=0` | Increase temperature for more variation |
| Ignores system prompt | Model instruction following varies | Be explicit; use "You must..." phrasing; test with different models |
| JSON output malformed | Model doesn't always produce valid JSON | Use `response_format={"type": "json_object"}` (gpt-4o+ only) |
| High latency on first call | Cold start / connection setup | Reuse `openai.OpenAI()` client instance across calls |
| `KeyError: 'content'` in code | Message content is `None` when content_filter fires | Always check `finish_reason` before accessing `.content` |

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Api Notes](../api-notes/)
- [Automation Use Cases](../automation-use-cases/)
- [Prompt Patterns](../prompt-patterns/)
- [Security Review](../security-review/)
- [OpenAI — Overview](../)
