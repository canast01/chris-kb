# Python Automation — Diagnostics

## Python Diagnostics Workflow

```mermaid
graph LR
    symptom["Symptom or\nUnexpected Output"]
    enableDebug["Enable DEBUG logging\n(logging.basicConfig)"]
    checkLogs["Inspect log file\nfor traceback"]
    pdbBreak["Add breakpoint()\nor python3 -m pdb"]
    inspectVars["Inspect variables\n(p var in pdb)"]
    verboseImport["python3 -v script.py\n(trace imports)"]
    checkSysPath["python3 -c \"import sys;\nprint(sys.path)\""]
    devMode["python3 -X dev\n(extra warnings)"]
    resolved["Root cause\nidentified"]

    symptom --> enableDebug
    enableDebug --> checkLogs
    checkLogs -->|Traceback found| pdbBreak
    pdbBreak --> inspectVars
    inspectVars --> resolved
    checkLogs -->|Import error| verboseImport
    verboseImport --> checkSysPath
    checkSysPath --> resolved
    checkLogs -->|Warnings| devMode
    devMode --> resolved
```

```bash
# Run with pdb from the command line — breaks at first line
python3 -m pdb script.py

# Post-mortem: inspect state after an unhandled exception
python3 -c "
import pdb, traceback
try:
    exec(open('script.py').read())
except Exception:
    traceback.print_exc()
    pdb.post_mortem()
"
```

## Structured Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s'
)
log = logging.getLogger(__name__)

log.debug("Connecting to %s", host)
log.info("Processing %d records", len(records))
log.warning("Rate limit approaching: %d requests remaining", remaining)
log.error("Failed to connect: %s", error)
log.exception("Unhandled exception")   # includes full traceback
```

## Import and Module Diagnostics

```bash
# Verbose import tracing — shows every import as it happens
python3 -v script.py 2>&1 | grep -i "import"

# Verbose import errors — find why a module is missing
python3 -v script.py 2>&1 | grep -i "error\|fail\|not found"

# Check if a module is importable
python3 -c "import netapp_ontap; print('OK')"

# Find where a module is installed
python3 -c "import netapp_ontap; print(netapp_ontap.__file__)"
```

```python
# Diagnose an import issue at runtime
import importlib.util
spec = importlib.util.find_spec('requests')
print(spec.origin if spec else "Not found")
```

## Runtime Inspection

```bash
# Confirm which Python and packages are active
which python
python --version
pip list

# Show sys.path — where Python looks for modules
python3 -c "import sys; print('\n'.join(sys.path))"

# Development mode — extra warnings and fault handler
python3 -X dev script.py
```

## Diagnostics Reference

| Tool | Command | Use case |
|---|---|---|
| pdb | `python3 -m pdb script.py` | Interactive step-through debugging |
| breakpoint() | Add `breakpoint()` in code | Drop into pdb at a specific line |
| logging | `logging.basicConfig(level=logging.DEBUG)` | Structured timestamped output |
| verbose imports | `python3 -v script.py` | Trace every import |
| dev mode | `python3 -X dev script.py` | Extra warnings and fault handler |
| pip show | `pip show <package>` | Confirm installed version and location |
