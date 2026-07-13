---
tags:
  - python
  - troubleshooting
search:
  boost: 1.5
description: "Python diagnostic commands: read the full traceback, trace imports with python3 -v, step through code with pdb, enable DEBUG logging, profile CPU with..."
---
# Python Automation — Diagnostics

<div class="kb-summary">
Python diagnostic commands: read the full traceback, trace imports with python3 -v, step through code with pdb, enable DEBUG logging, profile CPU with py-spy, and isolate environment issues with pip and venv inspection.

*Applies to: Python 3.x*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "Read last frame of traceback\nIdentify file and line number" {shape: rectangle}
D: "python3 -v script.py\nTrace import search" {shape: rectangle}
E: "Add breakpoint or\nlogging.debug statements" {shape: rectangle}
F: "py-spy top --pid pid\nIdentify hot function" {shape: rectangle}
G: "G" {shape: rectangle}
H: "python3 -m pdb script.py\nStep through to error line" {shape: rectangle}
I: "Fix and test" {shape: rectangle}
J: "python3 -c import sys; print sys.path\nCheck venv activation" {shape: rectangle}
K: "K" {shape: rectangle}
L: "pip install package\nor activate correct venv" {shape: rectangle}
M: "pip install package==version" {shape: rectangle}
N: "Check if blocking on I/O\nor CPU-bound tight loop" {shape: rectangle}
A: "Python Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
G -> H
G -> I
D -> J
K -> L
K -> M
E -> H
F -> N
H -> I
L -> I
M -> I
N -> I
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_read_and_capture_the_full_tra: "Step 1 — Read and capture the full traceback" {shape: rectangle}
step_2_check_the_python_environment: "Step 2 — Check the Python environment" {shape: rectangle}
step_3_trace_import_failures: "Step 3 — Trace import failures" {shape: rectangle}
step_4_interactive_debugging_with_pd: "Step 4 — Interactive debugging with pdb" {shape: rectangle}
step_5_enable_structured_debug_loggi: "Step 5 — Enable structured DEBUG logging" {shape: rectangle}
step_6_profile_cpu_and_memory: "Step 6 — Profile CPU and memory" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_read_and_capture_the_full_tra: investigate
symptom -> step_2_check_the_python_environment: investigate
symptom -> step_3_trace_import_failures: investigate
symptom -> step_4_interactive_debugging_with_pd: investigate
symptom -> step_5_enable_structured_debug_loggi: investigate
symptom -> step_6_profile_cpu_and_memory: investigate
step_1_read_and_capture_the_full_tra -> resolution
step_2_check_the_python_environment -> resolution
step_3_trace_import_failures -> resolution
step_4_interactive_debugging_with_pd -> resolution
step_5_enable_structured_debug_loggi -> resolution
step_6_profile_cpu_and_memory -> resolution
```

## Before you begin

- **Access:** the same user / environment that runs the failing script; do not debug as root if the script runs as a service user
- **Gather first:** the full traceback (copy from stderr, not just the last line), the Python version (`python3 --version`), and whether the issue is in a venv or system Python
- **Scope:** confirm whether the issue is reproducible on demand, intermittent, or environment-specific (only on a specific server / venv)
- **Do not guess:** the last line of a traceback is the exception and message; the second-to-last frame is where in your code it originated — read both before changing anything

---

## Step 1 — Read and capture the full traceback

```bash
# Run the failing script and capture both stdout and stderr
python3 script.py 2>&1 | tee /tmp/python-error-$(date +%F-%H%M).txt

# If the script is already logging, find the log file
grep -n "Traceback\|Error\|Exception" /var/log/myapp/app.log | tail -50
```

```python
# In your except block — log the full traceback including cause chain
import logging
import traceback

try:
    risky_operation()
except Exception as exc:
    logging.exception("risky_operation failed: %s", exc)
    # logging.exception automatically appends the traceback
    # Alternative: explicit traceback capture
    tb = traceback.format_exc()
    print(tb, file=sys.stderr)
```

**Reading a traceback:**
- The **bottom line** is the exception type and message (what failed)
- The frame **just above** it is the exact file and line number in your code where the exception originated
- Work **upward** through the frames to see the call chain that led there

---

## Step 2 — Check the Python environment

```bash
# Confirm which Python interpreter is active
which python3
python3 --version
# Expected: the interpreter in your venv, not /usr/bin/python3

# Check if a venv is activated
echo $VIRTUAL_ENV
# Expected: path to your venv directory; empty = not in a venv

# List installed packages and versions
pip list
pip list --outdated

# Check for dependency conflicts
pip check
# Expected: No broken requirements
# Problem: "package X has requirement Y>=Z, but you have Y W"

# Show where a specific package is installed
pip show requests
# Shows: Name, Version, Location, Requires, Required-by
```


```text title="Expected output"
/home/devuser/myproject/.venv/bin/python3
Python 3.11.7
/home/devuser/myproject/.venv
Package                Version
pip                    24.0
setuptools             68.2.2
requests               2.31.0
urllib3                2.1.0
certifi                2023.7.22
charset-normalizer     3.3.2
idna                   3.6
...
Package                Version Latest Type
urllib3                2.1.0   2.2.1  patch
certifi                2023.7.22 2024.2.2 minor

No broken requirements found.
Name: requests
Version: 2.31.0
Summary: Python HTTP for Humans.
Home-page: https://requests.readthedocs.io
Author: Kenneth Reitz
Location: /home/devuser/myproject/.venv/lib/python3.11/site-packages
Requires: charset-normalizer, idna, urllib3, certifi
Required-by:
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `which: python3: not found` | Activate your virtual environment with `source /path/to/venv/bin/activate` before running which. |
    | `WARNING: pip is being invoked by an old script wrapper` | Upgrade pip with `python3 -m pip install --upgrade pip` to use the modern invocation method. |
    | `ERROR: pip's dependency resolver does not currently take into account all the packages that are installed` | Run `pip install --upgrade pip setuptools` to resolve resolver conflicts with older tool versions. |
---

## Step 3 — Trace import failures

```bash
# Verbose import tracing — shows every module load attempt
python3 -v script.py 2>&1 | grep -i "import\|error\|not found" | head -100

# Check the module search path (where Python looks for modules)
python3 -c "import sys; print('\n'.join(sys.path))"
# Expected: venv site-packages first; then system site-packages

# Test if a specific module can be imported
python3 -c "import requests; print('requests', requests.__version__)"
# Problem: ModuleNotFoundError → not installed in this interpreter/venv

# Find where a module is installed
python3 -c "import requests; print(requests.__file__)"
```

```python
# Programmatically diagnose a missing module at runtime
import importlib.util

def check_module(name):
    spec = importlib.util.find_spec(name)
    if spec:
        print(f"{name}: found at {spec.origin}")
    else:
        print(f"{name}: NOT FOUND in sys.path")

check_module("requests")
check_module("netapp_ontap")
```

---

## Step 4 — Interactive debugging with pdb

```bash
# Launch script under pdb (stops at first line)
python3 -m pdb script.py

# Key pdb commands:
#   n         — execute next line (step over)
#   s         — step into function call
#   c         — continue until next breakpoint or error
#   p <expr>  — print value of expression (e.g., p my_dict)
#   pp <expr> — pretty-print (for dicts/lists)
#   l         — list 11 lines around current position
#   where     — print full call stack
#   q         — quit pdb

# Post-mortem debugging — inspect state at crash without re-running
python3 -c "
import pdb, traceback
try:
    import script   # replace with your module
except Exception:
    traceback.print_exc()
    pdb.post_mortem()
"
```

```python
# Drop a breakpoint at a specific line in your code (3.7+)
def process_item(item):
    result = transform(item)
    breakpoint()   # execution stops here; drops into pdb
    return result
```

---

## Step 5 — Enable structured DEBUG logging

```python
import logging

# Enable DEBUG logging for the current session
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S"
)

# Log at each severity level
logging.debug("variable value: %s", my_var)
logging.info("operation started")
logging.warning("unexpected state: %s", state)
logging.error("operation failed: %s", exc)
logging.exception("full traceback logged automatically above this line")
```

```bash
# Enable DEBUG for a script from the command line without changing code
PYTHONLOGLEVEL=DEBUG python3 script.py 2>&1 | tee /tmp/debug.log

# Enable development mode (ResourceWarning, asyncio debug, malloc debug)
python3 -X dev script.py

# Treat all warnings as errors (catches deprecation before it becomes a break)
python3 -W error script.py
```


```text title="Expected output"
DEBUG:root:Initializing application context
DEBUG:root:Loading configuration from /etc/app/config.yaml
DEBUG:root:Connecting to database at postgres://db-prod-01.internal:5432/appdb
DEBUG:root:Authentication token validated for user: admin@example.com
DEBUG:root:Starting request handler on 0.0.0.0:8080
INFO:root:Application ready
DEBUG:root:Processing request id=a7f3c2e1-9b4d-11ed-b1d4-0242ac120002
DEBUG:root:Query execution time: 234ms
Output written to /tmp/debug.log
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `PYTHONLOGLEVEL: command not found` | Use `export PYTHONLOGLEVEL=DEBUG` or set it inline as `PYTHONLOGLEVEL=DEBUG python3 script.py` (ensure no typo in variable name). |
    | `ResourceWarning: unclosed file <_io.TextIOWrapper name='/tmp/debug.log'>` | Add explicit `close()` calls or use context managers (`with open()`) in your Python script to properly release file handles. |
    | `DeprecationWarning: ... is deprecated and will be removed in Python 3.13` | Update the deprecated function call to its recommended replacement before the next Python version release, or suppress the warning with `-W ignore::DeprecationWarning` if the dependency hasn't updated yet. |
---

## Step 6 — Profile CPU and memory

```bash
# Install py-spy (system-wide or in venv)
pip install py-spy

# Attach to a running Python process and show live CPU profile
py-spy top --pid <pid>
# Shows: function name, file, line, % CPU — updates every second

# Record a flamegraph of a script run
py-spy record -o /tmp/profile.svg -- python3 script.py
# Open profile.svg in a browser — wide bars = hot paths

# Memory profiling (line-by-line)
pip install memory_profiler
python3 -m memory_profiler script.py
# Shows: memory used per line; look for lines with large increments
```


```text title="Expected output"
Collecting py-spy
  Downloading py-spy-0.3.14-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (3.8 MB)
Installing collected packages: py-spy
Successfully installed py-spy-0.3.14

py-spy top --pid 8472
  %CPU  Function (filename:lineno)
  45.2  process_batch (etl_worker.py:127)
  18.7  json.loads (json/decoder.py:337)
  12.4  database_insert (models.py:89)
   8.1  _thread_lock (threading.py:512)
   6.3  sleep (time.py:45)
  Sampling... (Ctrl+C to stop)

py-spy record -o /tmp/profile.svg -- python3 script.py
Wrote flamegraph to /tmp/profile.svg

Collecting memory_profiler
  Downloading memory_profiler-0.61.0-py3-none-any.whl (31 kB)
Installing collected packages: memory_profiler
Successfully installed memory_profiler-0.61.0

python3 -m memory_profiler script.py
Line #    Mem usage    Increment  Occurrences   Line Contents
     1   38.2 MiB      0.0 MiB           1   @profile
     2   38.3 MiB      0.1 MiB           1   def load_data(filepath):
    45   156.8 MiB    118.5 MiB           1       data = json.load(f)
    47   157.2 MiB      0.4 MiB           1       return data
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Permission denied: py-spy requires elevated privileges to attach to process <pid>` | Run `py-spy top --pid <pid>` with `sudo` or ensure the user owns the target process. |
    | `ModuleNotFoundError: No module named 'memory_profiler'` | Add `@profile` decorator to the function you want to analyze, or reinstall with `pip install memory_profiler` in the correct environment. |
    | `py-spy: could not attach to process <pid>: No such process` | Verify the PID is correct with `ps aux | grep python` before running py-spy. |
---

## Step 7 — Collect diagnostics for escalation

```bash
# All-in-one diagnostic snapshot
{
  echo "=== Python version ==="
  python3 --version
  echo "=== Virtual env ==="
  echo "VIRTUAL_ENV=$VIRTUAL_ENV"
  echo "=== Installed packages ==="
  pip list
  echo "=== Dependency check ==="
  pip check
  echo "=== sys.path ==="
  python3 -c "import sys; print('\n'.join(sys.path))"
  echo "=== Error output ==="
  python3 script.py 2>&1 || true
} > /tmp/python-diag-$(date +%F-%H%M).txt
```


```text title="Expected output"
=== Python version ===
Python 3.11.8
=== Virtual env ===
VIRTUAL_ENV=/home/admin/venv
=== Installed packages ===
Package            Version
------------------ ---------
certifi            2024.2.2
charset-normalizer 3.3.2
click              8.1.7
flask              3.0.0
requests           2.31.0
urllib3            2.1.0
... (12 more packages)
=== Dependency check ===
No broken requirements found.
=== sys.path ===
/home/admin/venv/lib/python3.11/site-packages
/usr/lib/python3.11
/usr/lib/python3.11/lib-dynload
/usr/local/lib/python3.11/dist-packages
=== Error output ===
Traceback (most recent call last):
  File "script.py", line 12, in <module>
    import requests
ModuleNotFoundError: No module named 'requests'
Diagnostic snapshot saved to /tmp/python-diag-2024-01-15-1432.txt
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ModuleNotFoundError: No module named '<package>'` | Activate the virtual environment with `source /path/to/venv/bin/activate` and run `pip install <package>`. |
    | `VIRTUAL_ENV=` (empty output)` | Activate the virtual environment before running diagnostics, or the wrong Python interpreter is being used. |
    | `pip: command not found` | Install pip with `python3 -m ensurepip --upgrade` or use `python3 -m pip` instead of `pip`. |
---

## Log locations

| Source | Location | What to look for |
|---|---|---|
| Script stderr | `python3 script.py 2>&1 \| tee /tmp/err.txt` | Traceback, exception type |
| App log file | `/var/log/<appname>/<appname>.log` | logging.error/exception output |
| systemd journal | `journalctl -u <service> --since "1 hour ago"` | Service crash events |
| pdb session | Interactive terminal | Variable state at error line |

---

## See also

- [Python — Common Issues](../common-issues/)
- [Python — Escalation](../escalation/)
- [Python — Health Checks](../../operations/health-checks/)

## Verify resolution

- The original exception no longer occurs when running the same input
- `pip check` shows no broken requirements
- DEBUG logging shows expected state at each step without errors
- If the fix was environment-related: confirm the venv is activated in the service unit or cron job that runs the script in production
