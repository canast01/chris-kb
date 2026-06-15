---
tags:
  - architecture
  - python
---
# Python Automation — Architecture

<div class="kb-summary">
Cross-platform automation language with virtual environment isolation, poetry/venv dependency management, asyncio for concurrent API calls, and Docker container execution; targets cloud APIs, infrastructure APIs, SSH, and databases.

*Applies to: Python 3.x*
</div>

```text
┌────────────────────────── Python Automation Architecture — venv and asyncio ──────────────────────────┐
│                                                                                                       │
│  Virtual environment isolation via venv/poetry; asyncio for concurrent API calls;                     │
│  Docker container execution; targets cloud APIs, infrastructure, SSH, databases.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Environment and Dependencies         │  │               Execution Models              │   │
│   │            venv: stdlib isolation            │  │           Script: python script.py          │   │
│   │            poetry: lock + publish            │  │         asyncio: event loop + await         │   │
│   │         pyproject.toml: PEP 517/518          │  │       ThreadPoolExecutor: I/O parallel      │   │
│   │        requirements.txt: pip install         │  │          Docker: container per job          │   │
│   │          pip: PyPI package manager           │  │         Lambda: serverless function         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  asyncio enables 100s of concurrent API calls in one thread; no GIL block on I/O.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Target APIs                  │  │             Quality and Testing             │   │
│   │       Cloud: boto3, azure-sdk, gcloud        │  │          mypy: static type checking         │   │
│   │      Infra: pyVmomi, paramiko, netmiko       │  │          pytest: unit + integration         │   │
│   │       REST: httpx (async) or requests        │  │              ruff: fast linter              │   │
│   │       DB: psycopg2, pymongo, redis-py        │  │               black: formatter              │   │
│   │           SSH: paramiko, asyncssh            │  │            pre-commit: gate hooks           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Linux host or container (Python 3.11+); API targets require network access;                          │
│  Docker daemon for container execution; outbound HTTPS to PyPI/cloud APIs.                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  venv          = virtual environment; isolated Python + packages per project                          │
│  poetry        = dependency manager with lock file; pyproject.toml based                              │
│  asyncio       = stdlib event loop; await suspends coroutine until I/O ready                          │
│  GIL           = Global Interpreter Lock; one thread runs Python bytecode                             │
│  httpx         = async-capable HTTP client; drop-in alternative to requests                           │
│  pyVmomi       = VMware vSphere Python SDK; wraps SOAP API                                            │
│  boto3         = AWS SDK for Python; all AWS service clients                                          │
│  paramiko      = SSH client library; exec_command for remote automation                               │
│  mypy          = static type checker; enforces type annotations                                       │
│  pytest        = test framework; fixtures, parametrize, plugins                                       │
│  pyproject.toml= PEP 517/518 build and metadata config file                                           │
│  ruff          = fast Rust-based linter; replaces flake8/isort/pyflakes                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Python Architecture](../../../assets/python-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>venv/poetry, execution models, asyncio patterns, Docker containerisation, project layout.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Virtual Environment Tools

| Tool | Lock file | Dependency groups | Build/publish | Best for |
|---|---|---|---|---|
| `venv` + `pip` | `requirements.txt` (manual) | No | No | Simple scripts |
| `pipenv` | `Pipfile.lock` | dev vs default | No | Application projects |
| `poetry` | `poetry.lock` | Multiple groups | Yes | Packages and services |

## Architecture Model

