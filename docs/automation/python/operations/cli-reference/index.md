---
tags:
  - operations
  - python
description: "CLI Reference reference covering Python Script Execution Pipeline, Package Management (pip), Common Infrastructure Packages, Environment Variables..."
---
# Python Automation — CLI Reference

<div class="kb-summary">
CLI Reference reference covering Python Script Execution Pipeline, Package Management (pip), Common Infrastructure Packages, Environment Variables, Running Scripts and 3 more sections.

*Applies to: Python 3.x*
</div>

## Before you begin

- **Access:** Python 3.10+ installed on the control host; `pip` or `pipx` available
- **Timing:** safe to run at any time — all commands below are read-only unless noted
- **Dependencies:** virtual environment activated (`source venv/bin/activate`) before running scripts

---

## Python Script Execution Pipeline

```d2
direction: right

readEnv: "Read Environment\n(os.environ / .env" {shape: rectangle}
parseArgs: "Parse CLI Args\n(argparse" {shape: rectangle}
loadConfig: "Load Config\n(YAML / JSON / INI" {shape: rectangle}
runScript: "Run Script Logic\n(main function" {shape: rectangle}
exportOutput: "Export Output\n(CSV / JSON / Excel" {shape: rectangle}
sendReport: "Send Report\n(email / webhook" {shape: rectangle}
logResult: "Log Result\n(file / syslog" {shape: rectangle}

readEnv -> parseArgs
parseArgs -> loadConfig
loadConfig -> runScript
runScript -> exportOutput
exportOutput -> sendReport
runScript -> logResult
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


```text title="Expected output"
Collecting requests
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Collecting paramiko
  Downloading paramiko-3.4.0-py3-none-any.whl (225 kB)
Collecting boto3
  Downloading boto3-1.28.85-py3-none-any.whl (135 kB)
Collecting pyVmomi
  Downloading pyVmomi-8.0.1.0-py3-none-any.whl (512 kB)
Collecting netapp-ontap
  Downloading netapp-ontap-9.13.0-py3-none-any.whl (1.2 MB)
Collecting py-pure-client
  Downloading py-pure-client-1.28.0-py3-none-any.whl (89 kB)
Collecting python-dotenv
  Downloading python-dotenv-1.0.0-py3-none-any.whl (19 kB)
Collecting pyyaml
  Downloading PyYAML-6.0.1-cp311-cp311-linux_x86_64.whl (733 kB)
Collecting ansible-core
  Downloading ansible-core-2.15.5-py3-none-any.whl (2.1 MB)
...
Successfully installed requests-2.31.0 paramiko-3.4.0 boto3-1.28.85 pyVmomi-8.0.1.0 netapp-ontap-9.13.0 py-pure-client-1.28.0 python-dotenv-1.0.0 PyYAML-6.0.1 ansible-core-2.15.5 cryptography-41.0.7 jinja2-3.1.2 markupsafe-2.1.3 urllib3-2.1.0 botocore-1.31.85 s3transfer-0.7.0 six-1.16.0 pycryptodome-3.19.0 bcrypt-4.1.1 cffi-1.16.0 pynacl-1.5.0
```

!!! warning "Common errors"
    **`ERROR: Could not find a version that satisfies the requirement netapp-ontap`** — Verify the package name is correct (it may be `netapp-lib` or require a private PyPI index) and check your pip index configuration.
    **`error: Microsoft Visual C++ 14.0 or greater is required`** — Install the Microsoft C++ Build Tools or use a pre-built wheel; on Linux/macOS this typically indicates a missing development headers package like `python3-dev`.
    **`ERROR: pip's dependency resolver does not currently take into account all the packages that are installed`** — This is a warning about conflicting transitive dependencies; verify the installation succeeded and test imports to confirm functionality.
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


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`KeyError: 'API_KEY'`** — Use `os.environ.get("API_KEY", "default")` instead of `os.environ["API_KEY"]` to provide a fallback value.
    **`FileNotFoundError: [Errno 2] No such file or directory: '.env'`** — Ensure the `.env` file exists in the script's working directory or specify the full path in `load_dotenv("/path/to/.env")`.
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


```text title="Expected output"
$ python3 script.py
Starting operation...
Processing complete. Duration: 2.34s

$ python3 script.py --host 10.0.0.1 --port 443 --verbose
[2024-01-15 14:23:45] INFO: Connecting to 10.0.0.1:443
[2024-01-15 14:23:46] DEBUG: TLS handshake successful
[2024-01-15 14:23:47] INFO: Request completed with status 200
[2024-01-15 14:23:47] INFO: Operation finished in 1.82s

$ python3 -m mypackage.script
Initializing module...
Task executed successfully

$ curl -s https://api.example.com/data | python3 parse.py
Parsed 847 records
Average response time: 124ms
Export written to output.csv

$ python3 -m json.tool data.json
{
  "version": "2.1.4",
  "timestamp": "2024-01-15T14:23:47Z",
  "servers": [
    {
      "hostname": "web-prod-01",
      "ip": "10.0.1.42",
      "status": "healthy"
    }
  ],
  "total_count": 12
}

$ curl -s https://api.example.com/status | python3 -m json.tool
{
  "cluster_status": "operational",
  "nodes_online": 8,
  "uptime_hours": 720,
  "last_check": "2024-01-15T14:23:51Z"
}
```

!!! warning "Common errors"
    **`python3: No such file or directory`** — Use `python` instead if Python 3 is the default, or verify Python 3 is installed with `which python3`.
    **`ModuleNotFoundError: No module named 'mypackage'`** — Ensure the package is in PYTHONPATH or install it with `pip install -e .` from the package directory.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Verify the API endpoint is returning valid JSON and check the curl response with `curl -s https://api.example.com/status | head -c 200`.
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


```text title="Expected output"
> /home/admin/script.py(1)<module>()
-> import requests
(Pdb) 

# (no output — command completes silently until breakpoint() is hit)

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/home/admin/script.py", line 42, in fetch_data
    response = api_client.get(endpoint)
KeyError: 'api_key'
> /home/admin/script.py(42)fetch_data()
-> response = api_client.get(endpoint)
(Pdb) 

# python3 -v output (truncated):
# installing zipimport hook
# installed zipimport hook
# # installing setuptools
# # installed setuptools
# # installing pkg_resources
# # installed pkg_resources
# # search sys.path for netapp_ontap
# # trying /usr/lib/python3.9/site-packages/netapp_ontap
# # trying /usr/lib/python3.9/site-packages/netapp_ontap.py
# # trying /usr/lib/python3.9/site-packages/netapp_ontap.pyc
# # trying /usr/lib/python3.9/site-packages/netapp_ontap/__init__.py
# # trying /usr/lib/python3.9/site-packages/netapp_ontap/__init__.pyc
# # zipimport: found 14 objects matching 'netapp_ontap'
# ...

OK

/usr/local/lib/python3.9/site-packages/netapp_ontap/__init__.py
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'netapp_ontap'`** — Install the missing module with `pip3 install netapp-ontap` or verify the correct package name.
    **`(Pdb) command not found`** — Ensure you are inside the pdb interactive session; type `help` to see available commands or `c` to continue execution.
    **`SyntaxError: invalid syntax`** — Check that `breakpoint()` is only used in Python 3.7+; for earlier versions, use `import pdb; pdb.set_trace()` instead.
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


```text title="Expected output"
certifi==2024.2.2
charset-normalizer==3.3.2
idna==3.6
netapp-ontap==22.11.0
paramiko==3.4.0
pyyaml==6.0.1
requests==2.31.0
boto3==1.34.0
botocore==1.34.27
jmespath==1.0.1
s3transfer==0.7.0
urllib3==2.1.0
Created virtual environment at venv-test
Collecting requests==2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
Installing collected packages: certifi, charset-normalizer, idna, urllib3, requests, boto3, paramiko, netapp-ontap, pyyaml
Successfully installed requests-2.31.0 boto3-1.34.0 paramiko-3.4.0 netapp-ontap-22.11.0 pyyaml-6.0.1
All imports OK
```

!!! warning "Common errors"
    **`ERROR: Could not find a version that satisfies the requirement netapp-ontap==22.11.0`** — Verify the package name and version exist on PyPI, or use a version available in your organization's private repository.
    **`ModuleNotFoundError: No module named 'requests'`** — Ensure pip install completed successfully and the virtual environment is activated before running the import test.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Python — Procedures](../procedures/)
- [Python — Scripts](../scripts/)
- [Python — Health Checks](../health-checks/)
