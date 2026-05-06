# Python CLI Reference

> Part of the [Python](../) reference.

---

## Python CLI Flags

Quick reference for commonly used interpreter flags.

| Flag | Purpose |
|---|---|
| `-c "code"` | Execute a Python statement inline |
| `-m module` | Run a library module as a script (e.g. `-m venv`, `-m pip`) |
| `-i` | Inspect: drop into REPL after script execution |
| `-v` | Verbose: show every import as it happens |
| `-vv` | Extra-verbose: show more detail on each import |
| `-O` | Optimise: remove assert statements and `__debug__` code |
| `-u` | Unbuffered stdout/stderr (useful in pipelines and containers) |
| `-W error` | Turn warnings into errors |
| `-X dev` | Development mode: extra warnings, fault handler, memory checks |
| `-B` | Do not write `.pyc` bytecode files |
| `--version` | Print Python version and exit |

```bash
# Check Python version
python3 --version
python --version       # may be Python 2 on some systems — check!

# Run a script
python3 script.py

# Run a script and drop into REPL after (inspect variables)
python3 -i script.py

# Run a module
python3 -m http.server 8080
python3 -m json.tool < data.json

# Execute a one-liner
python3 -c "import sys; print(sys.version)"
python3 -c "import platform; print(platform.node())"

# Verbose import tracing (troubleshoot missing modules)
python3 -v script.py 2>&1 | grep -i "import"

# Development mode (extra warnings + fault handler)
python3 -X dev script.py
```

---

## Virtual Environments

Always use a virtual environment for infrastructure scripts to avoid polluting the system Python.

```bash
# Create a virtual environment named "venv" in the current directory
python3 -m venv venv

# Activate (Linux / macOS)
source venv/bin/activate

# Activate (Windows — Command Prompt)
venv\Scripts\activate.bat

# Activate (Windows — PowerShell)
venv\Scripts\Activate.ps1

# Confirm active venv
which python        # Linux/macOS — should show venv/bin/python
Get-Command python  # Windows PowerShell

# Deactivate
deactivate

# Delete the environment
rm -rf venv
```

---

## Package Management (pip)

```bash
# Install a package
pip install requests

# Install a specific version
pip install netapp-ontap==22.11.0

# Install from requirements file
pip install -r requirements.txt

# Upgrade a package
pip install --upgrade boto3

# Uninstall
pip uninstall paramiko -y

# List installed packages
pip list

# List outdated packages
pip list --outdated

# Show details for a package (version, location, dependencies)
pip show pyVmomi

# Export current environment to requirements file
pip freeze > requirements.txt

# Install packages without cache (useful in CI or disk-constrained environments)
pip install --no-cache-dir -r requirements.txt

# Install in user space (no venv, no sudo)
pip install --user ansible
```

---

## Common Infrastructure Packages

| Package | Install | Purpose |
|---|---|---|
| `requests` | `pip install requests` | HTTP client for REST APIs |
| `paramiko` | `pip install paramiko` | SSH client for automation |
| `boto3` | `pip install boto3` | AWS SDK (S3, EC2, etc.) |
| `pyVmomi` | `pip install pyVmomi` | VMware vSphere API (Python) |
| `netapp-ontap` | `pip install netapp-ontap` | NetApp ONTAP REST API SDK |
| `py-pure-client` | `pip install py-pure-client` | Pure Storage FlashArray/FlashBlade/Pure1 SDK |
| `ansible` | `pip install ansible` | Ansible automation engine |
| `ansible-core` | `pip install ansible-core` | Ansible core only (lighter) |
| `python-dotenv` | `pip install python-dotenv` | Load `.env` files into environment |
| `pyyaml` | `pip install pyyaml` | YAML parsing |
| `jinja2` | `pip install jinja2` | Templating engine |
| `cryptography` | `pip install cryptography` | TLS, keys, certificates |
| `urllib3` | `pip install urllib3` | HTTP library (used by requests) |

```bash
# Install a typical infra automation environment
pip install requests paramiko boto3 pyVmomi netapp-ontap py-pure-client \
  python-dotenv pyyaml ansible-core
```

---

## Environment Variables

```bash
# Pass environment variables to a Python script
API_KEY=mykey python3 script.py

# Read in Python
import os
api_key = os.environ["API_KEY"]                     # raises if missing
api_key = os.environ.get("API_KEY", "default")      # safe with fallback

# Using .env file (python-dotenv)
# .env file:
#   API_KEY=mykey
#   API_URL=https://api.example.com

from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("API_KEY")
```

---

## Running Scripts

```bash
# Standard run
python3 script.py

# Pass arguments
python3 script.py --host 10.0.0.1 --port 443 --verbose

# Run as a module (script lives in a package)
python3 -m mypackage.script

# Pipe JSON into a script
curl -s https://api.example.com/data | python3 parse.py

# One-liner to pretty-print JSON from a file
python3 -m json.tool data.json

# One-liner to pretty-print JSON from curl
curl -s https://api.example.com/status | python3 -m json.tool
```

---

## Debugging

```bash
# Run with pdb (Python debugger) — breaks at first line
python3 -m pdb script.py

# Embed a breakpoint in code (Python 3.7+)
# Add to your script:
breakpoint()     # drops into pdb at this line

# Post-mortem: inspect state after an unhandled exception
python3 -c "
import pdb, traceback
try:
    exec(open('script.py').read())
except Exception:
    traceback.print_exc()
    pdb.post_mortem()
"

# Verbose import errors (find why a module is missing)
python3 -v script.py 2>&1 | grep -i "error\|fail\|not found"

# Check if a module is importable
python3 -c "import netapp_ontap; print('OK')"

# Find where a module is installed
python3 -c "import netapp_ontap; print(netapp_ontap.__file__)"
```

### Logging vs print

```python
# Prefer logging over print() for production scripts
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

logger.info("Connecting to %s", host)
logger.warning("Capacity above 90%%")
logger.error("Connection failed: %s", err)

# Enable debug level via environment
import os
level = logging.DEBUG if os.environ.get("DEBUG") else logging.INFO
logging.basicConfig(level=level)
```

---

## Windows-Specific

On Windows, the Python Launcher (`py`) is the preferred way to invoke Python when multiple versions are installed.

```powershell
# Check installed versions
py -0

# Run with a specific version
py -3 script.py
py -3.11 script.py

# Invoke pip via the launcher (avoids PATH conflicts)
py -3 -m pip install requests
py -3 -m pip list

# Create venv
py -3 -m venv venv

# Activate venv (PowerShell)
.\venv\Scripts\Activate.ps1

# If script execution is blocked, allow PS scripts (run as admin once)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate venv (cmd.exe)
venv\Scripts\activate.bat
```

### Common Windows Issues

```powershell
# python not found — use py instead
py script.py

# pip not found — use module syntax
py -m pip install requests

# SSL errors on corporate proxy
py -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org requests

# Behind proxy
$env:HTTPS_PROXY = "http://proxy.example.com:8080"
py -m pip install requests

# Line endings causing issues (scripts from Linux)
# In Git, set: git config --global core.autocrlf input
```

---

## requirements.txt Best Practices

```bash
# Pin exact versions for reproducible deployments
pip freeze > requirements.txt

# Or maintain a hand-crafted file with minimum versions:
# requirements.txt
# requests>=2.31.0
# netapp-ontap>=22.11.0
# boto3>=1.34.0
# paramiko>=3.4.0
# pyyaml>=6.0.1

# Separate dev dependencies
pip freeze > requirements-dev.txt   # full dev environment
# Keep requirements.txt lean for production

# Install and test in a clean venv
python3 -m venv venv-test
source venv-test/bin/activate
pip install -r requirements.txt
python3 -c "import requests, boto3, paramiko; print('All imports OK')"
deactivate
rm -rf venv-test
```
