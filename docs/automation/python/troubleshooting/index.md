# Python Automation — Troubleshooting



<div class="kb-summary">
Python Automation — Troubleshooting reference.
</div>

```
┌────────────────────────────────────── Python — Troubleshooting ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Python troubleshooting: import errors, type errors, dependency conflicts, API auth failures  │   │
│   │      First step: check python3 --version and which python3 to confirm correct interpreter     │   │
│   │       Enable verbose traceback: PYTHONTRACEMALLOC=1 or python3 -X tracemalloc script.py       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │             Diagnostic Commands             │   │
│   │             ModuleNotFoundError              │  │              pip show <module>              │   │
│   │        ImportError: version conflict         │  │          pip check (dep conflicts)          │   │
│   │        AttributeError on AWS response        │  │           python3 -m pdb script.py          │   │
│   │       botocore.exceptions.ClientError        │  │      print(json.dumps(resp, indent=2))      │   │
│   │        SSL: CERTIFICATE_VERIFY_FAILED        │  │    python -c "import ssl; ssl.SSLContext"   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    pip check       = verifies installed package compatibility; reports broken requirements    │   │
│   │  which python3   = shows which interpreter is active; must point to venv bin/ in active venv  │   │
│   │  ClientError     = boto3 API error; check error["Error"]["Code"] for specific AWS error code  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Python — Troubleshooting ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Python troubleshooting: import errors, type errors, dependency conflicts, API auth failures  │   │
│   │      First step: check python3 --version and which python3 to confirm correct interpreter     │   │
│   │       Enable verbose traceback: PYTHONTRACEMALLOC=1 or python3 -X tracemalloc script.py       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Common Issues                 │  │             Diagnostic Commands             │   │
│   │             ModuleNotFoundError              │  │              pip show <module>              │   │
│   │        ImportError: version conflict         │  │          pip check (dep conflicts)          │   │
│   │        AttributeError on AWS response        │  │           python3 -m pdb script.py          │   │
│   │       botocore.exceptions.ClientError        │  │      print(json.dumps(resp, indent=2))      │   │
│   │        SSL: CERTIFICATE_VERIFY_FAILED        │  │    python -c "import ssl; ssl.SSLContext"   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    pip check       = verifies installed package compatibility; reports broken requirements    │   │
│   │  which python3   = shows which interpreter is active; must point to venv bin/ in active venv  │   │
│   │  ClientError     = boto3 API error; check error["Error"]["Code"] for specific AWS error code  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Environment errors, import failures, and API timeouts.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Debugging tools, logging, and runtime inspection.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>When and how to escalate unresolved issues.</span>
</a>

</div>
