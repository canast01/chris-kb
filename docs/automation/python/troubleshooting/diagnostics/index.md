# Python Automation — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Python Diagnostics Workflow, Structured Logging, Import and Module Diagnostics, Runtime Inspection, Diagnostics Reference.
</div>

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

```text
┌──────────────────────────────────────── Python — Diagnostics ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Python diagnostic sequence: reproduce → inspect traceback → pdb debug → add logging      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Error Analysis                │  │                 Debug Tools                 │   │
│   │    Read full traceback (last line first)     │  │           python3 -m pdb script.py          │   │
│   │       traceback.print_exc() in except        │  │             breakpoint() in code            │   │
│   │       logging.exception("msg") logs tb       │  │           ipdb (IPython debugger)           │   │
│   │          pip check (dep conflicts)           │  │          py-spy top (CPU profiler)          │   │
│   │       python3 -W error to catch warns        │  │           memory_profiler (memory)          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    breakpoint()   = built-in (3.7+); drops into pdb at that line; n=next, c=continue, p var   │   │
│   │       py-spy         = sampling profiler; py-spy top --pid <pid>; no code changes needed      │   │
│   │   -W error       = treat warnings as errors; catches deprecation warnings before they break   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
