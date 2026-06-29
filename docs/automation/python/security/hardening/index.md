---
tags:
  - python
  - security
---
# Python Automation — Hardening

<div class="kb-summary">
Hardening reference covering Secure Script Development Checklist Flow, Dependency Management, File and Permission Security, Hardening Checklist.

*Applies to: Python 3.x*
</div>

```d2
direction: down

secure_script_development_checklist_: "Secure Script Development Checklist Flow" {shape: rectangle}
file_and_permission_security: "File and Permission Security" {shape: rectangle}
hardening_checklist: "Hardening Checklist" {shape: rectangle}

secure_script_development_checklist_ -> file_and_permission_security: hardens
file_and_permission_security -> hardening_checklist: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Secure Script Development Checklist Flow

```d2
direction: right

code: "Write Script Code" {shape: rectangle}
inputVal: "Validate all external\ninputs (regex / type" {shape: rectangle}
noEval: "Avoid eval() / exec()\nwith external data" {shape: rectangle}
subproc: "Use subprocess with\nlist args (no shell=True" {shape: rectangle}
secrets: "Load secrets from\nenv / secrets manager" {shape: rectangle}
pinDeps: "Pin dependencies\n(pip freeze" {shape: rectangle}
audit: "pip-audit:\ncheck for CVEs" {shape: rectangle}
filePerms: "Set file permissions\n(chmod 600 for secrets" {shape: rectangle}
noLogs: "Never log secrets\nor stack traces externally" {shape: rectangle}
ready: "Script ready\nfor production" {shape: rectangle}

code -> inputVal
inputVal -> noEval
noEval -> subproc
subproc -> secrets
secrets -> pinDeps
pinDeps -> audit
audit -> filePerms
filePerms -> noLogs
noLogs -> ready
```

## File and Permission Security

```python
import os
import stat

# Write sensitive files with restricted permissions
def write_secret_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)
    # Restrict to owner read/write only (600)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

# Check a file has safe permissions before reading
def safe_read(path: str) -> str:
    file_stat = os.stat(path)
    if file_stat.st_mode & (stat.S_IRWXG | stat.S_IRWXO):
        raise PermissionError(f"{path} is readable by group or others — tighten permissions")
    return open(path).read()
```

## Hardening Checklist

| Area | Practice |
|---|---|
| Secrets | Never hardcode; use env vars or secrets manager |
| Inputs | Validate and sanitise all external inputs |
| Dependencies | Pin versions; audit regularly with `pip-audit` |
| subprocess | Use list arguments; never `shell=True` with user input |
| eval/exec | Never use with untrusted data |
| File permissions | Restrict sensitive files to `600`; scripts to `700` |
| Logging | Never log secrets, tokens, or passwords |
| Error messages | Do not expose internal paths or stack traces to external callers |

---

## See also

- [Python — Authentication](../authentication/)
- [Python — Access Control](../access-control/)
- [Python — Encryption](../encryption/)
