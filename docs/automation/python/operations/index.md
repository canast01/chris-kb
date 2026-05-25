# Python Automation — Operations


```
┌───────────────────────────────────────── Python — Operations ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Python operations: venv management, package updates, test runs, script deployment       │   │
│   │  Day-to-day: activate venv, install/update deps, run pytest, lint with ruff, type-check mypy  │   │
│   │    Deployment: copy scripts to target or install as package; use entry_points for CLI tools   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Environment Operations            │  │              Package Operations             │   │
│   │            python3 -m venv .venv             │  │       pip install -r requirements.txt       │   │
│   │          source .venv/bin/activate           │  │             pip list --outdated             │   │
│   │         .venv/Scripts/activate (Win)         │  │           pip install -U <package>          │   │
│   │            deactivate (exit venv)            │  │           pip-compile (pip-tools)           │   │
│   │           python -m pytest tests/            │  │           safety check (CVE scan)           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    pip-tools    = pip-compile pins transitive deps; pip-sync installs exactly the lock file   │   │
│   │              safety       = checks installed packages against known CVE database              │   │
│   │        entry_points = pyproject.toml: [project.scripts] my-tool = "mypackage.cli:main"        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Python CLI commands, pip, virtual environments, and debugging.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Job monitoring, health checks, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Job scheduling, automation procedures, and reporting.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Python version management, package installation, and upgrades.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Script backup and environment restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for infrastructure operations.</span>
</a>

</div>
