# Python Automation

<div class="kb-summary">
Python infrastructure automation knowledge base covering virtual environment management, dependency tooling, asyncio concurrency patterns, Docker containerisation, CLI script design, and integration with cloud and infrastructure APIs.
</div>

```
┌────────────────────────── Python — Infrastructure Scripting and Automation ───────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Python: dominant language for infrastructure automation, API integration, and data processing │   │
│   │     Virtual environments: isolate dependencies per project; venv (stdlib) or conda/poetry     │   │
│   │    Key infra libraries: boto3 (AWS), paramiko (SSH), requests (HTTP), fabric (remote exec)    │   │
│   │     Testing: pytest for unit and integration tests; mock with unittest.mock or pytest-mock    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │     venv + pip + poetry     │  │      Script management      │  │     Secrets: not in code    │   │
│   │      Library ecosystem      │  │       Package updates       │  │       Dependency audit      │   │
│   │      Type hints + mypy      │  │      pytest test suite      │  │      bandit static scan     │   │
│   │       Standard modules      │  │        CI integration       │  │       Input validation      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     venv          = built-in virtual env; python3 -m venv .venv; source .venv/bin/activate    │   │
│   │               pip           = package installer; pip install -r requirements.txt              │   │
│   │    Poetry        = dependency management with lock file; pyproject.toml; poetry add/install   │   │
│   │            boto3         = AWS SDK for Python; session, client, resource interfaces           │   │
│   │   paramiko      = SSH2 protocol library; SSHClient, SFTPClient; used for remote command exec  │   │
│   │          requests      = HTTP library; Session, get/post/put; urllib3 under the hood          │   │
│   │         fabric        = SSH command execution framework; built on Paramiko; task-based        │   │
│   │          pytest        = testing framework; fixtures, parametrize, plugins ecosystem          │   │
│   │   mypy          = static type checker; reads type hints; catches type errors before runtime   │   │
│   │         ruff          = fast Python linter and formatter; replaces flake8/black/isort         │   │
│   │     bandit        = security-focused linter; detects common vulnerabilities in Python code    │   │
│   │       pyproject.toml= modern project config file; defines metadata, deps, tool settings       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, scripts, procedures, and job monitoring.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, and secure coding practices.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
