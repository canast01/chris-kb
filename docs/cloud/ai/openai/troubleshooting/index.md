---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# OpenAI API — Troubleshooting


<div class="kb-summary">
Troubleshooting reference covering Error Code Reference, Rate Limit Troubleshooting, Token Limit Issues, Authentication Issues, Timeout and Latency and 3 more sections.

*Applies to: OpenAI API*
</div>
```text
┌───────────────────────────── Ai Openai Troubleshooting — Troubleshooting ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Openai troubleshooting: structured diagnostic process for common issues            │   │
│   │         Start with health dashboard, then check recent changes, then review event logs        │   │
│   │        Collect support bundle before contacting vendor support to accelerate resolution       │   │
│   │         Escalation matrix: L1 → L2 → vendor support based on severity and SLA targets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check health → review changes → examine logs → diagnose → resolve                                  │
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
│    Physical: Ai Openai Troubleshooting infrastructure · management network · monitoring               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Openai             = Ai Openai Troubleshooting platform overview and core concepts                 │
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
