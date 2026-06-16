---
tags:
  - troubleshooting
  - python
  - automation
  - known-issues
---
# Python (Automation Scripts) — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known Python scripting bugs, error codes, and workarounds covering virtual environments, dependency management, SSL, and REST API integrations.

*Applies to: Python 3.10 / 3.12 for infrastructure automation scripts*
</div>

```text
┌────────────────────────────────────── Python Automation Scripts ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Python 3.10/3.12 scripts for infrastructure automation and REST API integration        │   │
│   │          Protocols: HTTPS (requests/urllib3) · SSH (paramiko/fabric) · SNMP (pysnmp)          │   │
│   │            Management: venv per project / pip / requirements.txt or pyproject.toml            │   │
│   │          venv activate -> pip install -> script run -> API/SSH call -> target system          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Isolation          │  │      venv / virtualenv      │  │       Per-project deps      │   │
│   │           Packages          │  │          pip / PyPI         │  │     requirements.txt pin    │   │
│   │            Trust            │  │     CA bundle / certifi     │  │  Internal CA often missing  │   │
│   │         HTTP client         │  │       requests / httpx      │  │       Timeout, retries      │   │
│   │         Remote exec         │  │      paramiko / fabric      │  │     SSH key or password     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │     requests     │  REST API calls  │       HTTPS       │Bearer/Basic/cert │  Uses OS trust   │   │
│   │     paramiko     │  SSH automation  │        SSH        │   Key/password   │ Pure-Python SSH2 │   │
│   │       venv       │  Dep. isolation  │        N/A        │       N/A        │ One per project  │   │
│   │       pip        │ Package install  │   HTTPS to PyPI   │ Token (priv idx) │   Pin versions   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: automation/jump host running scripts - target APIs/SSH endpoints over network              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  venv           = isolated Python environment with its own interpreter + package set                  │
│  pip            = Python package installer; reads requirements.txt or pyproject.toml                  │
│  certifi        = Python package bundling Mozilla CA certs used as a trust fallback                   │
│  SSLCertVerif.  = error raised when a server cert chain is not in the trust store                     │
│  requests       = most common Python HTTP client library for REST automation                          │
│  paramiko       = pure-Python SSHv2 library used for remote command execution                         │
│  Timeout        = max wait for a connect/read; unset defaults can hang indefinitely                   │
│  update-ca-trust= RHEL command to add a CA cert to the OS-wide trust store                            │
│  site-packages  = directory where pip installs packages for an interpreter/venv                       │
│  JSONDecodeError= raised when a response body is not valid JSON (often an HTML error page)            │
│  Distributed Seg. Proc. = backup-specific DSP; unrelated term seen in some integration logs           │
│  Idempotency    = property where re-running a script produces the same end state safely               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Always use virtual environments (`venv`) for isolation — avoid system Python for scripts.
- `pip list --outdated` to identify stale dependencies causing compatibility issues.
- SSL verification errors are common in internal environments with self-signed certs.

## SSL and Certificates

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `SSLCertVerificationError: certificate verify failed` | All | Target using self-signed or private CA cert not in system trust | Add CA cert to system bundle; or pass `verify=/path/to/ca.crt` in requests | N/A |
| `requests.exceptions.SSLError` on internal API call | All | Python `requests` using OS trust store; internal CA not trusted | Export CA cert; add to OS trust: `update-ca-trust` (RHEL) / `update-ca-certificates` (Ubuntu) | N/A |

## Virtual Environments

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `ModuleNotFoundError` after package install | All | Package installed to system Python, not active venv | Activate venv: `source venv/bin/activate`; reinstall package | N/A |
| `pip: command not found` inside venv | Python 3.10 | venv created without pip | Recreate venv: `python -m venv --clear venv` | N/A |

## REST API Integration

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `ConnectionRefusedError: [Errno 111] Connection refused` | All | Target service not listening or port blocked | Verify service is running; check port with `nc -zv <host> <port>` | N/A |
| `requests.exceptions.Timeout` on large API responses | All | Default timeout too short (requests default: None = infinite on connect, but blocked by server) | Set explicit timeout: `requests.get(url, timeout=30)` | N/A |
| `json.decoder.JSONDecodeError` parsing API response | All | API returning HTML error page instead of JSON (e.g., 503) | Check `response.status_code` before parsing; log `response.text` for debugging | N/A |

## See also

- [Python — Common Issues](common-issues.md)
- [Ansible — Known Issues](../../ansible/troubleshooting/known-issues/)
- [Terraform — Known Issues](../../terraform/troubleshooting/known-issues/)
