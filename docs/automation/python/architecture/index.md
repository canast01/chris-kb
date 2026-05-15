# Python Automation — Architecture

<div class="kb-summary">
Cross-platform automation language with virtual environment isolation, poetry/venv dependency management, asyncio for concurrent API calls, and Docker container execution; targets cloud APIs, infrastructure APIs, SSH, and databases.
</div>

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

```mermaid
flowchart TD
    A([Script / Service entrypoint]) --> B[Virtual Environment\nvenv / poetry / pipenv]
    B --> C[Application Code]
    C --> D[Standard Library\nos, pathlib, subprocess, logging]
    C --> E[Third-Party Libraries\nrequests, boto3, paramiko, pydantic]
    C --> F[Internal Packages\nshared utilities, config loaders]
    D & E & F --> G{Execution Target}
    G --> H[Cloud APIs\nAWS / Azure / GCP]
    G --> I[Infrastructure APIs\nvSphere / NetBox / Vault]
    G --> J[Databases\nPostgreSQL / SQLite / Redis]
    G --> K[File Systems & OS\nlocal / NFS / S3]
    G --> L[Remote Hosts\nSSH via paramiko / fabric]
    style B fill:#1565c0,color:#fff
    style C fill:#2e7d32,color:#fff
```
