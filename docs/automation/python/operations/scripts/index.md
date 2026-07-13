---
tags:
  - operations
  - python
description: "Scripts reference covering Purpose, Windows Python Environment Setup Flow."
---
# Python Automation — Scripts

<div class="kb-summary">
Scripts reference covering Purpose, Windows Python Environment Setup Flow.

*Applies to: Python 3.x*
</div>

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Purpose

Use this page for practical Python scripts, field-tested commands, known issues, and operational notes.

## Windows Python Environment Setup Flow

```d2
direction: right

checkPython: "Check Python 3\ninstalled in PATH" {shape: rectangle}
createVenv: "Create venv\n(python -m venv" {shape: rectangle}
installPython: "Install Python 3\nfrom python.org" {shape: rectangle}
activateVenv: "Activate venv\n(Scripts\\activate" {shape: rectangle}
installPkgs: "Install packages\n(pip install" {shape: rectangle}
runScript: "Run Python Script\n(python script.py" {shape: rectangle}
deactivate: "Deactivate venv" {shape: rectangle}

checkPython -> createVenv
checkPython -> installPython
installPython -> createVenv
createVenv -> activateVenv
activateVenv -> installPkgs
installPkgs -> runScript
runScript -> deactivate
```

**What you should see**

The script steps through 5 numbered stages printed in yellow. If Python is missing it prints installation instructions and stops. Otherwise it creates the virtual environment, installs all six packages, then tests each import and prints a colour-coded summary table showing the package name, OK/FAIL status, and installed version. A green "SUCCESS" message confirms everything is ready.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Python — Procedures](../procedures/)
- [Python — CLI Reference](../cli-reference/)
- [Python — Health Checks](../health-checks/)
