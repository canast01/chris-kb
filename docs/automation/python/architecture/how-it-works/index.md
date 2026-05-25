# Python Automation — How It Works

Python is the dominant language for infrastructure automation, data pipelines, and API integration in modern enterprise environments. This page covers architecture patterns, runtime models, and execution strategies for production Python automation.

---

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

---

## Virtual Environments

Every automation project must use a virtual environment. Global `pip install` is prohibited in production.

| Tool | Lock file | Dependency groups | Build/publish | Best for |
|---|---|---|---|---|
| `venv` + `pip` | `requirements.txt` (manual) | No | No | Simple scripts |
| `pipenv` | `Pipfile.lock` | dev vs default | No | Application projects |
| `poetry` | `poetry.lock` | Multiple groups | Yes | Packages and services |

```bash
# venv
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# poetry
poetry new my-automation
poetry add requests boto3 pydantic
poetry add --group dev pytest black mypy
poetry run python main.py
```

---

## Package Management

```toml
[tool.poetry.dependencies]
python = "^3.11"
requests = "^2.31"
boto3 = "^1.34"
pydantic = "^2.5"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
black = "^24.0"
mypy = "^1.8"
ruff = "^0.3"
```

---

## Script Execution Models

```python
#!/usr/bin/env python3
import argparse
import sys
import logging

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("widget_name")
    parser.add_argument("--env", choices=["dev", "staging", "prod"], default="dev")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()

def main() -> int:
    args = parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    log = logging.getLogger(__name__)
    log.info("Deploying widget %s to %s", args.widget_name, args.env)
    if args.dry_run:
        log.info("Dry run — no changes applied")
        return 0
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

---

## Async Patterns

Use `asyncio` when automation involves high concurrency (many API calls, multiple SSH connections).

| Scenario | Use asyncio? |
|---|---|
| Many concurrent HTTP/API calls | Yes |
| Multiple SSH connections in parallel | Yes (with `asyncssh`) |
| CPU-bound data processing | No — use `multiprocessing` |
| Simple sequential script | No — adds unnecessary complexity |

```python
import asyncio
import aiohttp

async def fetch_widget(session, name, semaphore):
    async with semaphore:
        async with session.get(f"/api/widgets/{name}") as resp:
            resp.raise_for_status()
            return await resp.json()

async def fetch_all(names):
    sem = asyncio.Semaphore(10)
    async with aiohttp.ClientSession(base_url="https://api.example.com") as s:
        return await asyncio.gather(*[fetch_widget(s, n, sem) for n in names])
```

---

## Containerisation with Docker

```dockerfile
FROM python:3.12-slim
RUN useradd --system --create-home automation
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root
COPY --chown=automation:automation . .
USER automation
ENTRYPOINT ["python", "-m", "widget_automation"]
```

---

## Project Layout

```text
widget-automation/
├── pyproject.toml
├── poetry.lock
├── Dockerfile
├── .env.example
├── src/
│   └── widget_automation/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── config.py
│       ├── api.py
│       └── utils.py
└── tests/
    ├── conftest.py
    ├── test_api.py
    └── test_config.py
```
