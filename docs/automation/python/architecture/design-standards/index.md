---
tags:
  - architecture
  - python
---
# Python — Design Standards

```python
from __future__ import annotations  # enables forward references in Python 3.9

from pathlib import Path
from typing import Any

import requests

def fetch_widget(name: str, timeout: int = 30) -> dict[str, Any]:
    """Fetch a widget by name from the API."""
    resp = requests.get(f"https://api.example.com/widgets/{name}", timeout=timeout)
    resp.raise_for_status()
    return resp.json()

def process_widgets(
    widget_names: list[str],
    output_path: Path,
    *,
    dry_run: bool = False,
) -> int:
    """Process a list of widgets and write results. Returns count processed."""
    results: list[dict[str, Any]] = []
    for name in widget_names:
        data = fetch_widget(name)
        results.append(data)

    if not dry_run:
        output_path.write_text(str(results))

    return len(results)
```

```python
import structlog

log = structlog.get_logger()

def deploy_widget(name: str, env: str) -> None:
    log = structlog.get_logger().bind(widget=name, env=env)

    log.info("deployment_started")
    try:
        # ... deploy logic ...
        log.info("deployment_complete", duration_ms=342)
    except Exception as exc:
        log.error("deployment_failed", error=str(exc), exc_info=True)
        raise
```
```json
{"event": "deployment_started", "widget": "widget-42", "env": "prod", "timestamp": "2026-05-08T14:22:01Z", "level": "info"}
{"event": "deployment_complete", "widget": "widget-42", "env": "prod", "duration_ms": 342, "timestamp": "2026-05-08T14:22:01.342Z", "level": "info"}
```
```python
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout

class WidgetNotFoundError(Exception):
    """Raised when the requested widget does not exist."""

class WidgetAPIError(Exception):
    """Raised when the widget API returns an unexpected error."""

def fetch_widget(name: str) -> dict:
    try:
        resp = requests.get(
            f"https://api.example.com/widgets/{name}",
            timeout=30,
        )
        if resp.status_code == 404:
            raise WidgetNotFoundError(f"Widget '{name}' not found")
        resp.raise_for_status()
        return resp.json()

    except WidgetNotFoundError:
        raise  # re-raise domain exceptions unchanged

    except HTTPError as exc:
        raise WidgetAPIError(
            f"API returned {exc.response.status_code} for widget '{name}'"
        ) from exc

    except (ConnectionError, Timeout) as exc:
        raise WidgetAPIError(
            f"Network error fetching widget '{name}': {exc}"
        ) from exc
```
```text
# requirements.txt — pin exact versions for reproducibility
requests==2.31.0
boto3==1.34.55
pydantic==2.5.3
structlog==24.1.0

# requirements-dev.txt
-r requirements.txt
pytest==8.0.2
mypy==1.8.0
black==24.2.0
ruff==0.3.2
```
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict
      - id: detect-private-key

  - repo: https://github.com/psf/black
    rev: 24.2.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.2
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - types-requests
          - pydantic
```
```bash
# Install hooks (run once per clone)
pip install pre-commit
pre-commit install

# Run against all files manually
pre-commit run --all-files

# Update hook versions
pre-commit autoupdate
```
```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "S",    # flake8-bandit (security)
    "T20",  # flake8-print (no print statements)
]
ignore = ["S101"]  # allow assert in tests

[tool.ruff.lint.per-file-ignores]
"tests/*" = ["S", "T20"]
```
```python
# tests/conftest.py
import pytest
import responses  # pip install responses

@pytest.fixture
def widget_api_url() -> str:
    return "https://api.example.com"

@pytest.fixture
def mock_widget_response() -> dict:
    return {"name": "widget-01", "state": "Active", "priority": 5}
```
```python
# tests/test_api.py
import pytest
import responses as rsps

from widget_automation.api import fetch_widget, WidgetNotFoundError, WidgetAPIError

@rsps.activate
def test_fetch_widget_success(mock_widget_response):
    rsps.add(rsps.GET, "https://api.example.com/widgets/widget-01",
             json=mock_widget_response, status=200)

    result = fetch_widget("widget-01")

    assert result["name"] == "widget-01"
    assert result["state"] == "Active"

@rsps.activate
def test_fetch_widget_not_found():
    rsps.add(rsps.GET, "https://api.example.com/widgets/missing",
             json={"error": "not found"}, status=404)

    with pytest.raises(WidgetNotFoundError, match="missing"):
        fetch_widget("missing")

@rsps.activate
def test_fetch_widget_api_error():
    rsps.add(rsps.GET, "https://api.example.com/widgets/widget-01",
             json={"error": "server error"}, status=500)

    with pytest.raises(WidgetAPIError):
        fetch_widget("widget-01")
```
```toml
# pytest configuration (pyproject.toml)
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```
```bash
# Run tests
pytest

# With coverage
pytest --cov=src --cov-report=term-missing --cov-report=xml

# Run specific test file
pytest tests/test_api.py -v

# Run tests matching a name pattern
pytest -k "test_fetch"
```


```text title="Expected output"
============================= test session starts ==============================
platform linux -- Python 3.11.7, pytest-8.0.1, py-1.13.0, pluggy-1.2.0
rootdir: /home/devops/project, configfile: pytest.ini, testpaths: tests
collected 42 items

tests/test_api.py .................................. [ 71%]
tests/test_utils.py .......... [100%]

============================== 42 passed in 2.34s ==============================

---------- coverage: platform linux-gnu, pytest-8.0.1, coverage-7.2.0 ----------
Name                      Stmts   Miss  Cover   Missing
-----------------------------------------------------------
src/api.py                   156     12    92%    45-47, 89-91
src/utils.py                  84      3    96%    112
src/config.py                 42      0   100%
-----------------------------------------------------------
TOTAL                        282     15    95%

tests/test_api.py::test_fetch_user PASSED                                 [ 33%]
tests/test_api.py::test_fetch_posts PASSED                                [ 66%]
tests/test_api.py::test_fetch_comments PASSED                             [100%]

3 passed in 0.87s
```

!!! warning "Common errors"
    **`ERROR: file not found: tests/test_api.py`** — Verify the test file path matches your project structure and run from the repository root directory.
    **`ModuleNotFoundError: No module named 'pytest'`** — Install pytest with `pip install pytest pytest-cov` before running tests.
    **`FAILED tests/test_api.py::test_fetch - AssertionError: assert None == 'expected_value'`** — Review the failing test assertion and ensure the code under test returns the expected value.
---

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## See also

- [Python — Deploy](../../deploy/)
