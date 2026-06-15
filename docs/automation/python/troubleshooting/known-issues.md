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
┌────────────────────────────────── Automation Python Troubleshooting ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                       Python: Automation Python Troubleshooting platform                      │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                Management: Automation Python Troubleshooting management console               │   │
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
│    Physical: Automation Python Troubleshooting infrastructure · management network · monitoring       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Python             = Automation Python Troubleshooting platform overview and core concepts         │
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
