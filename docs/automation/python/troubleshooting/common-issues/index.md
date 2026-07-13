---
tags:
  - python
  - troubleshooting
search:
  boost: 1.5
description: "Common Issues reference covering Python Error Triage Flow, API and Network Timeouts, Common Errors Reference."
---
# Python Automation — Common Issues

<div class="kb-summary">
Common Issues reference covering Python Error Triage Flow, API and Network Timeouts, Common Errors Reference.

*Applies to: Python 3.x*
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
python_error_triage_flow: "Python Error Triage Flow" {shape: rectangle}
api_and_network_timeouts: "API and Network Timeouts" {shape: rectangle}
common_errors_reference: "Common Errors Reference" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> python_error_triage_flow: investigate
symptom -> api_and_network_timeouts: investigate
symptom -> common_errors_reference: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
python_error_triage_flow -> resolution
api_and_network_timeouts -> resolution
common_errors_reference -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "Python Error Triage Flow\n— source venv/bin/activate" {shape: rectangle}
R2: "Python Error Triage Flow\n— pip install package in active venv" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Common Errors Reference\n— set REQUESTS_CA_BUNDLE to corp CA" {shape: rectangle}
R4: "Common Errors Reference\n— pass verify= with cert bundle path" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "API and Network Timeouts\n— fix firewall or proxy settings" {shape: rectangle}
R6: "API and Network Timeouts\n— set timeout= in requests.get call" {shape: rectangle}
B4: "B4" {shape: rectangle}
R7: "Common Errors Reference\n— chmod or chown output directory" {shape: rectangle}
B5: "B5" {shape: rectangle}
R8: "Common Errors Reference\n— print resp.text before resp.json" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
B4 -> R7
B5 -> R8
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

```d2
direction: right

error: "Script Error / Failure" {shape: rectangle}
errType: "Error type?" {shape: rectangle}
checkVenv: "Is correct venv\nactivated?" {shape: rectangle}
activateVenv: "source venv/bin/activate\nthen pip install" {shape: rectangle}
reinstall: "pip install <package>\nin active venv" {shape: rectangle}
checkToken: "API token\nexpired or revoked?" {shape: rectangle}
rotateToken: "Regenerate token\nin target system" {shape: rectangle}
checkNetwork: "curl -v <api_url>\nfrom automation host" {shape: rectangle}
fixFW: "Fix firewall /\nproxy settings" {shape: rectangle}
checkResp: "print(resp.text" {shape: rectangle}
updateParsing: "Update parsing logic\nto match new schema" {shape: rectangle}
checkPath: "ls -la on output\ndirectory" {shape: rectangle}
fixPerms: "chmod / chown\noutput directory" {shape: rectangle}

error -> errType
errType -> checkVenv
checkVenv -> activateVenv
checkVenv -> reinstall
errType -> checkToken
checkToken -> rotateToken
errType -> checkNetwork
checkNetwork -> fixFW
errType -> checkResp
checkResp -> updateParsing
errType -> checkPath
checkPath -> fixPerms
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
