---
tags:
  - python
  - troubleshooting
search:
  boost: 1.5
---
# Python Automation — Common Issues


<div class="kb-summary">
Common Issues reference covering Python Error Triage Flow, API and Network Timeouts, Common Errors Reference.

*Applies to: Python 3.x*
</div>
![Python Automation — Common Issues](../../../../assets/automation-python-troubleshooting-common-issues-index.svg)


## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{ModuleNotFound\nError?}
    S --> B2{SSL certificate\nverify failed?}
    S --> B3{Connection\ntimeout?}
    S --> B4{Permission\ndenied?}
    S --> B5{JSON decode\nerror?}
    B1 -->|Yes| D1{Correct venv\nactivated?}
    D1 -->|No| R1[Python Error Triage Flow\n— source venv/bin/activate]
    D1 -->|Yes| R2[Python Error Triage Flow\n— pip install package in active venv]
    B2 -->|Yes| D2{Corporate\nproxy in use?}
    D2 -->|Yes| R3[Common Errors Reference\n— set REQUESTS_CA_BUNDLE to corp CA]
    D2 -->|No| R4[Common Errors Reference\n— pass verify= with cert bundle path]
    B3 -->|Yes| D3{API reachable\nfrom host?}
    D3 -->|No| R5[API and Network Timeouts\n— fix firewall or proxy settings]
    D3 -->|Yes| R6[API and Network Timeouts\n— set timeout= in requests.get call]
    B4 -->|Yes| R7[Common Errors Reference\n— chmod or chown output directory]
    B5 -->|Yes| R8[Common Errors Reference\n— print resp.text before resp.json]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class B1,B2,B3,B4,B5,D1,D2,D3 decision
    class S start
```

---

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Python Error Triage Flow

```mermaid
flowchart TD
    error["Script Error / Failure"]
    error --> errType{"Error type?"}
    errType -->|ModuleNotFoundError| checkVenv["Is correct venv\nactivated?"]
    checkVenv -->|No| activateVenv["source venv/bin/activate\nthen pip install"]
    checkVenv -->|Yes| reinstall["pip install <package>\nin active venv"]
    errType -->|401 Unauthorized| checkToken["API token\nexpired or revoked?"]
    checkToken -->|Yes| rotateToken["Regenerate token\nin target system"]
    errType -->|ConnectionError\nTimeout| checkNetwork["curl -v <api_url>\nfrom automation host"]
    checkNetwork -->|Blocked| fixFW["Fix firewall /\nproxy settings"]
    errType -->|JSONDecodeError| checkResp["print(resp.text)\ncheck content-type"]
    checkResp --> updateParsing["Update parsing logic\nto match new schema"]
    errType -->|PermissionError| checkPath["ls -la on output\ndirectory"]
    checkPath --> fixPerms["chmod / chown\noutput directory"]
```


## API and Network Timeouts

```python
import requests

# Always set a timeout — default is None (hangs forever)
try:
    resp = requests.get('https://api.example.com/data',
                        timeout=(5, 30))  # (connect, read) seconds
    resp.raise_for_status()
except requests.exceptions.ConnectTimeout:
    print("Connection timed out — check host and port")
except requests.exceptions.ReadTimeout:
    print("Server accepted connection but response took too long")
except requests.exceptions.ConnectionError as e:
    print(f"Network error: {e}")
```

## Common Errors Reference

| Error | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` | Package not installed or wrong venv active | `pip install <pkg>` in correct venv |
| `PermissionError` | Script lacks write access to a path | Use a writable path or run with elevated privileges |
| `JSONDecodeError` | API returned non-JSON (e.g. HTML error page) | Check `resp.text` before calling `resp.json()` |
| `KeyError` | Dict key doesn't exist | Use `.get()` with a default; check API response schema |
| `AttributeError: NoneType` | Function returned None unexpectedly | Add None check; review return values |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Untrusted cert or missing CA bundle | Pass `verify='/path/to/ca-bundle.crt'` or update certifi |

```python
# Check what an API actually returned before parsing
resp = requests.get(url, timeout=10)
print(resp.status_code, resp.headers.get('Content-Type'))
print(resp.text[:500])   # first 500 chars
resp.raise_for_status()
data = resp.json()
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Python — Diagnostics](../diagnostics/)
- [Python — Escalation](../escalation/)
- [Python — Health Checks](../../operations/health-checks/)
