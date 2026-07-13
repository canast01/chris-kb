---
tags:
  - deployment
  - python
search:
  boost: 1.5
---
# Python Automation — Environment Setup

This guide covers installing Python, isolating dependencies with a virtual environment,
managing packages, loading secrets safely, integrating with VS Code, and wiring a CI
pipeline before running your first automation scripts.

---

```d2
direction: right

plan: "Plan" {shape: oval}
install_python: "Install Python" {shape: rectangle}
create_a_project_virtual_environment: "Create a Project Virtual Environment" {shape: rectangle}
install_project_dependencies: "Install Project Dependencies" {shape: rectangle}
configure_environment_variables: "Configure Environment Variables" {shape: rectangle}
set_up_ide_integration_vs_code: "Set Up IDE Integration (VS Code)" {shape: rectangle}
configure_a_ci_pipeline_for_python_s: "Configure a CI Pipeline for Python Scripts" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_python
install_python -> create_a_project_virtual_environment
create_a_project_virtual_environment -> install_project_dependencies
install_project_dependencies -> configure_environment_variables
configure_environment_variables -> set_up_ide_integration_vs_code
set_up_ide_integration_vs_code -> configure_a_ci_pipeline_for_python_s
configure_a_ci_pipeline_for_python_s -> validate
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install Python

**Linux (RHEL/Fedora/Rocky)**

```bash
sudo dnf install python3 python3-pip
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 14 Nov 2024 09:47:22 AM UTC.
Dependencies resolved.
================================================================================
 Package                    Architecture       Version              Repository
================================================================================
Installing:
 python3                    x86_64             3.11.7-1.fc39        fedora
 python3-pip                x86_64             23.3.1-1.fc39        fedora
Installing dependencies:
 python3-libs               x86_64             3.11.7-1.fc39        fedora
 libffi                     x86_64             3.4.4-1.fc39         fedora
 openssl-libs               x86_64             1:3.0.7-1.fc39       fedora

Transaction Summary
================================================================================
Install  5 Packages

Total download size: 48 M
Installed size: 156 M
Is this ok? [y/N]: y
Downloading Packages:
[1/5] python3-11.7-1.fc39.x86_64.rpm          100% |████████| 48 M  2.3 MB/s
Running transaction check
Transaction test succeeded.
Running transaction
  Installing : libffi-3.4.4-1.fc39.x86_64                                  1/5
  Installing : openssl-libs-3.0.7-1.fc39.x86_64                            2/5
  Installing : python3-libs-3.11.7-1.fc39.x86_64                           3/5
  Installing : python3-3.11.7-1.fc39.x86_64                                4/5
  Installing : python3-pip-23.3.1-1.fc39.x86_64                            5/5
Verifying        : python3-3.11.7-1.fc39.x86_64                            1/5
Verifying        : python3-pip-23.3.1-1.fc39.x86_64                        2/5

Complete!
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: This command has to be run with superuser privileges (see sudo).` | Ensure you have sudo access or run the command as root; verify with `sudo -l`. |
    | `Error: Failed to synchronize cache for repo 'fedora'` | Check network connectivity and verify your DNF repository configuration with `sudo dnf repolist`. |
**Linux (Debian/Ubuntu)**

```bash
sudo apt install python3 python3-pip
```


```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
python3 is already the newest version (3.10.12-1~20.04.1).
python3-pip is already the newest version (20.0.2-5ubuntu1.9).
0 upgraded, 0 newly installed, 0 removed.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)` | Run the command with `sudo` or ensure your user has appropriate sudo privileges. |
    | `E: Unable to locate package python3-pip` | Update your package lists with `sudo apt update` before attempting installation. |
**macOS**

```bash
brew install python
```


```text title="Expected output"
==> Downloading https://ghcr.io/v2/homebrew/core/python/manifests/3.12.1
==> Downloading https://ghcr.io/v2/homebrew/core/python/blobs/sha256:a1b2c3d4e5f6
==> Downloading /usr/local/Cellar/python/3.12.1/bin/python3
==> Pouring python--3.12.1.arm64_monterey.bottle.tar.gz
==> Caveats
Python has been installed as
  /usr/local/bin/python3

Unversioned symlinks `python`, `python-config`, `pip` etc. will be installed into
  /usr/local/opt/python/libexec/bin

==> Summary
🍺  /usr/local/Cellar/python/3.12.1: 3,258 files, 62.8MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: python: already installed` | Run `brew upgrade python` to update to the latest version, or `brew uninstall python` first if you need a clean reinstall. |
    | `Error: The following directories are not writable by your user: /usr/local/Cellar` | Run `sudo chown -R $(whoami) /usr/local/Cellar` to fix Homebrew permissions. |
**Windows**

```powershell
winget install Python.Python.3
```

**Verify**

```bash
python3 --version
pip3 --version
```


```text title="Expected output"
Python 3.11.7
pip 23.2.1 from /usr/lib/python3.11/site-packages/pip (python 3.11)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: python3` | Install Python 3 using your package manager (e.g., `apt install python3` on Ubuntu or `brew install python3` on macOS). |
    | `command not found: pip3` | Install pip3 by running `apt install python3-pip` on Ubuntu or `brew install python3` on macOS, or upgrade Python to include pip. |
On Linux/macOS always use `python3`/`pip3` to avoid invoking a system Python 2
interpreter.

---

## Create a Project Virtual Environment

A virtual environment isolates project dependencies from the system Python and from
other projects. Always create one before installing packages.

```bash
python3 -m venv .venv
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Command 'python3' not found` | Install Python 3 using your package manager (e.g., `apt install python3` on Ubuntu or `brew install python3` on macOS). |
    | `Error: [Errno 13] Permission denied: '.venv'` | Ensure the current directory is writable and you have sufficient permissions; try running from a different location or use `sudo` if necessary. |
**Activate** — Linux/macOS: `source .venv/bin/activate` —
Windows PowerShell: `.venv\Scripts\Activate.ps1`

Upgrade pip after activation:

```bash
pip install --upgrade pip
```


```text title="Expected output"
Requirement already satisfied: pip in /usr/local/lib/python3.11/site-packages (24.0)
Collecting pip
  Downloading pip-24.2.1-py3-none-any.whl (1.8 MB)
     |████████████████████████████████| 1.8 MB 2.3 MB/s
Installing collected packages: pip
  Attempting uninstall: pip 24.0
    Found existing installation: records 24.0
    Uninstalling pip-24.0...
    Successfully uninstalled pip-24.0
Successfully installed pip-24.2.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied` | Run the command with `sudo` or use `pip install --user --upgrade pip` to install in user directory. |
    | `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed` | This is a warning; upgrade pip again or use `pip install --upgrade --force-reinstall pip` to resolve dependency conflicts. |
Add `.venv/` to `.gitignore` so the directory is not committed to version control.

---

## Install Project Dependencies

```bash
# From a requirements file
pip install -r requirements.txt

# Or individually
pip install requests boto3 azure-identity paramiko pyyaml
```


```text title="Expected output"
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting boto3
  Downloading boto3-1.28.85-py3-none-any.whl (135 kB)
Collecting azure-identity
  Downloading azure-identity-1.14.0-py3-none-any.whl (156 kB)
Collecting paramiko
  Downloading paramiko-3.3.1-py3-none-any.whl (220 kB)
Collecting pyyaml
  Downloading PyYAML-6.0.1-cp311-cp311-linux_x86_64.whl (705 kB)
Installing collected packages: requests, boto3, azure-identity, paramiko, pyyaml
Successfully installed requests-2.31.0 boto3-1.28.85 azure-identity-1.14.0 paramiko-3.3.1 pyyaml-6.0.1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR: Could not find a version that satisfies the requirement requests` | Verify your pip index is accessible and the package name is spelled correctly. |
    | `ERROR: Could not open requirements.txt` | Ensure the requirements.txt file exists in the current directory and you have read permissions. |
    | `error: Microsoft Visual C++ 14.0 or greater is required` | Install the Microsoft C++ Build Tools or use a pre-built wheel for your Python version. |
| Package | Purpose |
|---|---|
| `requests` | HTTP client for REST API calls |
| `boto3` | AWS SDK |
| `azure-identity` | Azure authentication |
| `paramiko` | SSH client for remote execution |
| `pyyaml` | YAML parsing |
| `python-dotenv` | Load `.env` into environment variables |

Freeze dependencies after installing:

```bash
pip freeze > requirements.txt
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pip: command not found` | Ensure Python and pip are installed, or use `python3 -m pip freeze > requirements.txt` if pip is not in PATH. |
    | `Permission denied` | Run the command in a directory where you have write permissions, or use `sudo pip freeze > requirements.txt` if necessary. |
---

## Configure Environment Variables

Store credentials in a `.env` file and load them at runtime — never hard-code them
in source files.

```bash
# .env
VCENTER_HOST=vcenter.corp.local
VCENTER_USER=automation@corp.local
VCENTER_PASS=changeme
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: .env: command not found` | Create the `.env` file first with `touch .env` or use a text editor like `nano .env`. |
    | `Permission denied` | Ensure the `.env` file has read permissions by running `chmod 600 .env`. |
Install and use `python-dotenv`:

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()

vcenter_host = os.getenv("VCENTER_HOST")
```

Add `.env` to `.gitignore` immediately:

```bash
echo ".env" >> .gitignore
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: .gitignore: Permission denied` | Ensure the file has write permissions with `chmod 644 .gitignore` or run the command from a directory where you have write access. |
    | `bash: .gitignore: No such file or directory` | Create the `.gitignore` file first with `touch .gitignore` before appending to it. |
In production, inject secrets from a secrets manager (HashiCorp Vault, AWS Secrets
Manager, GitHub Actions secrets) rather than shipping a `.env` file.

---

## Set Up IDE Integration (VS Code)

1. Install the **Python** extension (`ms-python.python`).
2. Open the Command Palette (`Ctrl+Shift+P`) → **Python: Select Interpreter** →
   choose the `.venv` interpreter.

Install linting and formatting tools, then reference them in `.vscode/settings.json`:

```bash
pip install black ruff
```

```json
{
    "editor.formatOnSave": true,
    "python.formatting.provider": "black",
    "python.linting.ruffEnabled": true
}
```

---

## Configure a CI Pipeline for Python Scripts

Create `.github/workflows/python.yml`:

```yaml
name: Python CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install --upgrade pip && pip install -r requirements.txt
      - run: ruff check .
      - run: python -m pytest
```

Add the `test` job as a required status check under **Settings → Branches → Branch
protection rules** to block merges when tests fail.

Pass secrets via GitHub Actions secrets: `env: VCENTER_HOST: ${{ secrets.VCENTER_HOST }}`.

---

## Validate the Environment

```bash
# Python version
python3 --version

# Installed packages
pip list

# Import check
python3 -c "import requests; print(requests.__version__)"

# Env variable load
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('VCENTER_HOST'))"

# Run first script
python3 scripts/hello.py
```


```text title="Expected output"
Python 3.11.7
Package            Version
------------------ ---------
certifi            2024.2.2
charset-normalizer 3.3.2
idna                3.6
python-dotenv      1.0.0
requests           2.31.0
urllib3            2.1.0
...
2.31.0
vcenter.prod.internal
Hello from deployment script
Initialized connection pool with 4 workers
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ModuleNotFoundError: No module named 'requests'` | Run `pip install requests` to install the missing dependency. |
    | `FileNotFoundError: [Errno 2] No such file or directory: 'scripts/hello.py'` | Verify the script path is correct and run the command from the project root directory. |
    | `KeyError: 'VCENTER_HOST'` | Ensure the `.env` file exists in the current directory and contains the `VCENTER_HOST` variable. |
| Check | Expected |
|---|---|
| `python3 --version` | Python 3.10 or later |
| `pip list` | All packages from `requirements.txt` listed |
| `import requests` | Prints version without `ModuleNotFoundError` |
| `load_dotenv()` check | Prints value from `.env`, not `None` |
| First script | Runs without import or missing-variable errors |

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Python — Procedures](../operations/procedures/)
- [Python — Common Issues](../troubleshooting/common-issues/)
- [Python — How It Works](../architecture/how-it-works/)
