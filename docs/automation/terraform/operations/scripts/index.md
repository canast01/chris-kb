# Terraform — Scripts

## Purpose

Use this page for practical Terraform scripts, field-tested commands, known issues, and operational notes.

## Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident Notes

Capture:

- Symptom
- Start time
- Impact
- Workspace and environment
- Error message
- What changed
- What was checked
- Next action

## Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful Commands

Add tested commands here.

## Known Issues

Add known issues here as they come up.

---

## State Drift Detection (Bash)

Wrapper around `terraform plan` that detects configuration drift in a given workspace, parses the change summary, and alerts if drift is found. Suitable for scheduled execution.

~~~bash
#!/usr/bin/env bash
# tf-drift-detect.sh
# Usage: TF_DIR=<path> TF_WORKSPACE=<workspace> ./tf-drift-detect.sh
#
# Exit codes: 0=no drift, 1=drift detected or error

set -euo pipefail

TF_DIR="${TF_DIR:?TF_DIR is required}"
TF_WORKSPACE="${TF_WORKSPACE:-default}"
PLANFILE="/tmp/tfplan-$(date +%Y%m%d%H%M%S).out"
ALERT_WEBHOOK="${ALERT_WEBHOOK:-}"   # Optional: Slack/Teams webhook URL
LOGFILE="/var/log/tf-drift-$(date +%Y%m%d-%H%M%S).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

cleanup() { rm -f "${PLANFILE}" "${PLANFILE}.json"; }
trap cleanup EXIT

log "=== Terraform Drift Detection ==="
log "Directory : ${TF_DIR}"
log "Workspace : ${TF_WORKSPACE}"

cd "${TF_DIR}"

# --- Step 1: Select workspace ---
log "Step 1: Selecting workspace '${TF_WORKSPACE}'..."
terraform workspace select "${TF_WORKSPACE}" 2>&1 | tee -a "${LOGFILE}"

# --- Step 2: Init ---
log "Step 2: Running terraform init -reconfigure..."
terraform init -reconfigure -input=false 2>&1 | tee -a "${LOGFILE}"

# --- Step 3: Plan with detailed exit code ---
log "Step 3: Running terraform plan..."
set +e
terraform plan -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"
PLAN_RC=$?
set -e

# --- Step 4: Interpret exit code ---
case "${PLAN_RC}" in
    0)
        log "RESULT: No changes. Infrastructure matches configuration."
        exit 0
        ;;
    1)
        log "RESULT: ERROR — terraform plan encountered an error."
        exit 1
        ;;
    2)
        log "RESULT: DRIFT DETECTED — configuration changes exist."
        ;;
    *)
        log "RESULT: Unexpected plan exit code: ${PLAN_RC}"
        exit 1
        ;;
esac

# --- Step 5: Parse change summary ---
log "Step 5: Parsing resource change summary..."
terraform show -json "${PLANFILE}" > "${PLANFILE}.json"

SUMMARY=$(python3 - <<EOF
import json, sys

with open('${PLANFILE}.json') as f:
    plan = json.load(f)

changes = plan.get('resource_changes', [])
to_add     = [c['address'] for c in changes if 'create' in c.get('change', {}).get('actions', [])]
to_change  = [c['address'] for c in changes if 'update' in c.get('change', {}).get('actions', [])]
to_destroy = [c['address'] for c in changes if 'delete' in c.get('change', {}).get('actions', [])]

print(f"Add: {len(to_add)}, Change: {len(to_change)}, Destroy: {len(to_destroy)}")
print()
for r in to_add:
    print(f"  + {r}")
for r in to_change:
    print(f"  ~ {r}")
for r in to_destroy:
    print(f"  - {r}")
EOF
)

log "Change summary:"
echo "${SUMMARY}" | while IFS= read -r line; do log "  ${line}"; done

# --- Step 6: Send alert if webhook configured ---
if [[ -n "${ALERT_WEBHOOK}" ]]; then
    log "Step 6: Sending drift alert..."
    PAYLOAD=$(python3 -c "
import json
msg = 'Terraform drift detected in workspace ${TF_WORKSPACE} (${TF_DIR}):\n${SUMMARY}'
print(json.dumps({'text': msg}))
")
    curl -s -X POST -H "Content-Type: application/json" \
        -d "${PAYLOAD}" "${ALERT_WEBHOOK}" > /dev/null
    log "Alert sent to webhook."
fi

log "Log: ${LOGFILE}"
exit 1
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or macOS machine (or Windows with Git Bash installed from gitforwindows.org)
- Terraform installed and in your PATH (download from terraform.io/downloads)
- Python 3 installed (used inside the script to parse the plan JSON)
- A Terraform project directory with valid configuration files
- Optionally: a Slack or Teams webhook URL for drift alerts

**Step 1 — Save the file**

1. On Linux/macOS open a text editor, or on Windows open **Notepad**
2. Copy the entire code block above
3. Save it as `tf-drift-detect.sh`
4. On Linux/macOS make it executable: `chmod +x tf-drift-detect.sh`

**Step 2 — Fill in your details**

Set these environment variables before running (or export them in your shell):

| Variable | What to enter | Where to find it |
|---|---|---|
| `TF_DIR` | Full path to your Terraform project folder | The folder containing your `.tf` files |
| `TF_WORKSPACE` | Terraform workspace name | Run `terraform workspace list` in your project |
| `ALERT_WEBHOOK` | Slack or Teams incoming webhook URL | Slack/Teams app integration settings — leave blank to skip alerts |

**Step 3 — Open a terminal**

- **On Linux/macOS:** Open Terminal
- **On Windows:** Install Git for Windows (gitforwindows.org) then open Git Bash

**Step 4 — Run the script**

```
cd ~/Desktop
TF_DIR=/path/to/your/terraform TF_WORKSPACE=default ./tf-drift-detect.sh
```

**What you should see**

The script prints timestamped log lines as it selects the workspace, runs `terraform init`, and runs `terraform plan`. If no drift is found it prints `RESULT: No changes` and exits. If drift exists it prints a change summary listing resources to add (`+`), modify (`~`), or destroy (`-`), sends an alert if a webhook is configured, and exits with code 1. A log file is written to `/var/log/` with a timestamp in the name.

---

## Multi-Workspace Deploy Script (Bash)

Deploy Terraform across dev, staging, and prod workspaces in sequence. Prompts for approval before each workspace (unless auto-approve is configured for dev). Stops and alerts on any workspace failure.

~~~bash
#!/usr/bin/env bash
# tf-multi-workspace-deploy.sh
# Usage: TF_DIR=<path> ./tf-multi-workspace-deploy.sh [--destroy]
#
# Set AUTO_APPROVE_DEV=true to skip approval for dev workspace.

set -euo pipefail

TF_DIR="${TF_DIR:?TF_DIR is required}"
WORKSPACES=("dev" "staging" "prod")
AUTO_APPROVE_DEV="${AUTO_APPROVE_DEV:-false}"
DESTROY=false
LOGFILE="/var/log/tf-deploy-$(date +%Y%m%d-%H%M%S).log"

for arg in "$@"; do
    [[ "$arg" == "--destroy" ]] && DESTROY=true
done

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

alert_failure() {
    local ws="$1"
    log "ALERT: Deployment failed in workspace '${ws}'. Stopping pipeline."
    log "Review errors above and check state with: terraform workspace select ${ws} && terraform plan"
}

cd "${TF_DIR}"

log "=== Terraform Multi-Workspace Deploy ==="
log "Directory   : ${TF_DIR}"
log "Workspaces  : ${WORKSPACES[*]}"
${DESTROY} && log "MODE: DESTROY" || log "MODE: APPLY"

for WS in "${WORKSPACES[@]}"; do
    log ""
    log "--- Workspace: ${WS} ---"

    log "Selecting workspace '${WS}'..."
    terraform workspace select "${WS}" 2>&1 | tee -a "${LOGFILE}"

    log "Running terraform init..."
    terraform init -reconfigure -input=false 2>&1 | tee -a "${LOGFILE}"

    PLANFILE="/tmp/tfplan-${WS}-$(date +%Y%m%d%H%M%S).out"
    if ${DESTROY}; then
        log "Planning destroy for workspace '${WS}'..."
        terraform plan -destroy -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}" || true
    else
        log "Planning for workspace '${WS}'..."
        terraform plan -detailed-exitcode -input=false -out="${PLANFILE}" 2>&1 | tee -a "${LOGFILE}" || true
    fi

    AUTO_APPROVE=false
    if [[ "${WS}" == "dev" ]] && [[ "${AUTO_APPROVE_DEV}" == "true" ]]; then
        AUTO_APPROVE=true
        log "Auto-approve enabled for dev workspace."
    fi

    if ! ${AUTO_APPROVE}; then
        echo ""
        read -r -p "Apply changes for workspace '${WS}'? [yes/no]: " CONFIRM
        if [[ "${CONFIRM}" != "yes" ]]; then
            log "Skipped workspace '${WS}' by operator choice."
            rm -f "${PLANFILE}"
            continue
        fi
    fi

    if ${DESTROY}; then
        log "Running terraform destroy for workspace '${WS}'..."
        if ! terraform apply -destroy -auto-approve -input=false "${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"; then
            alert_failure "${WS}"
            exit 1
        fi
    else
        log "Running terraform apply for workspace '${WS}'..."
        if ! terraform apply -auto-approve -input=false "${PLANFILE}" 2>&1 | tee -a "${LOGFILE}"; then
            alert_failure "${WS}"
            exit 1
        fi
    fi

    rm -f "${PLANFILE}"
    log "Workspace '${WS}': SUCCESS"
done

log ""
log "=== All workspaces processed successfully. ==="
log "Log: ${LOGFILE}"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Linux or macOS machine (or Windows with Git Bash installed from gitforwindows.org)
- Terraform installed and in your PATH
- Three Terraform workspaces already created: `dev`, `staging`, `prod` (create with `terraform workspace new <name>`)
- A Terraform project directory with valid configuration files
- Operator access to approve changes interactively (or set `AUTO_APPROVE_DEV=true` to skip dev approval)

**Step 1 — Save the file**

1. Copy the entire code block above into a text editor
2. Save it as `tf-multi-workspace-deploy.sh`
3. Make it executable: `chmod +x tf-multi-workspace-deploy.sh`

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `TF_DIR` | Full path to your Terraform project folder | The folder containing your `.tf` files |
| `AUTO_APPROVE_DEV` | Set to `true` to skip manual approval for dev | Omit or set `false` for interactive approval |
| `--destroy` flag | Pass as argument to run a destroy instead of apply | Only use intentionally |

**Step 3 — Open a terminal**

- **On Linux/macOS:** Open Terminal
- **On Windows:** Install Git for Windows (gitforwindows.org) then open Git Bash

**Step 4 — Run the script**

```
cd ~/Desktop
TF_DIR=/path/to/your/terraform ./tf-multi-workspace-deploy.sh
```

To run a destroy instead:

```
TF_DIR=/path/to/your/terraform ./tf-multi-workspace-deploy.sh --destroy
```

**What you should see**

The script works through each workspace (dev, staging, prod) in order. For each workspace it prints a header, runs init and plan, then prompts `Apply changes for workspace '<name>'? [yes/no]:`. Type `yes` and press Enter to apply. If any workspace fails the script stops immediately and prints an alert with remediation instructions. A timestamped log file is written to `/var/log/` throughout.

---

## Windows: Terraform Plan and Apply (CMD Batch)

Automates the full Terraform workflow on Windows: checks for terraform.exe, runs init, validate, and plan, prompts for confirmation, applies if confirmed, and logs everything to a timestamped file.

~~~bat
@echo off
REM tf-plan-apply.bat
REM Usage: Edit the TF_DIR and TF_VAR_ values below, then run from Command Prompt.

setlocal enabledelayedexpansion

REM -----------------------------------------------------------------------
REM EDIT THESE VALUES
REM -----------------------------------------------------------------------
set TF_DIR=C:\terraform\my-project
set TF_WORKSPACE=default

REM Terraform variables — add or remove as needed for your project
set TF_VAR_region=us-east-1
set TF_VAR_environment=dev
set TF_VAR_app_name=myapp
REM -----------------------------------------------------------------------

for /f "tokens=1-6 delims=/:. " %%a in ("%date% %time%") do (
    set LOGFILE=%USERPROFILE%\Desktop\tf-apply-%%a%%b%%c-%%d%%e%%f.log
)

echo.
echo === Terraform Plan and Apply ===
echo Directory : %TF_DIR%
echo Workspace : %TF_WORKSPACE%
echo Log       : %LOGFILE%
echo.

echo [1/6] Checking for terraform.exe...
terraform -version >nul 2>&1
if errorlevel 1 (
    echo ERROR: terraform.exe not found in PATH.
    echo Download from https://terraform.io/downloads, extract to C:\Tools, add C:\Tools to PATH.
    pause
    exit /b 1
)
echo terraform found.
echo.

echo [2/6] Changing to project directory...
if not exist "%TF_DIR%" (
    echo ERROR: Directory not found: %TF_DIR%
    pause
    exit /b 1
)
cd /d "%TF_DIR%"
echo.

echo [3/6] Running terraform init...
terraform init -reconfigure -input=false 2>&1
if errorlevel 1 ( echo ERROR: terraform init failed. & pause & exit /b 1 )
echo.

echo [4/6] Running terraform validate...
terraform validate 2>&1
if errorlevel 1 ( echo ERROR: terraform validate failed. & pause & exit /b 1 )
echo.

echo [5/6] Running terraform plan...
terraform plan -out=tfplan.bin -input=false 2>&1
if errorlevel 1 ( echo ERROR: terraform plan failed. & pause & exit /b 1 )
echo.

echo [6/6] Review the plan output above.
set /p CONFIRM=Type YES to apply (anything else cancels): 
if /i "%CONFIRM%" neq "YES" (
    echo Apply cancelled.
    del tfplan.bin 2>nul
    pause
    exit /b 0
)

echo.
echo Applying...
terraform apply tfplan.bin 2>&1
del tfplan.bin 2>nul
if errorlevel 1 ( echo ERROR: terraform apply failed. & pause & exit /b 1 )

echo.
echo Apply complete.
pause
endlocal
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or later
- Terraform installed and available as `terraform.exe`
- AWS credentials set as environment variables or in `%USERPROFILE%\.aws\credentials`
- A Terraform project folder with your `.tf` configuration files

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC
2. Copy the entire code block above
3. Save as **All Files**, name it `tf-plan-apply.bat`, save to your Desktop

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `TF_DIR` | Full path to your Terraform project folder | The folder containing your `.tf` files |
| `TF_WORKSPACE` | Terraform workspace name (default `default`) | Run `terraform workspace list` in your project |
| `TF_VAR_region` | AWS region (e.g. `us-east-1`) | Your AWS console region |
| `TF_VAR_environment` | Environment name (e.g. `dev`, `prod`) | Your naming convention |
| `TF_VAR_app_name` | Your application name | Your internal naming convention |

**Step 3 — Run the script**

```
cd C:\Users\YourName\Desktop
tf-plan-apply.bat
```

**What you should see**

The script runs through 6 numbered steps. After the plan output you are prompted to type `YES` to apply. A log file is saved to your Desktop with a timestamp in the filename.

---

## Windows: Terraform State Audit (PowerShell)

Reads the current Terraform state, lists all resources with their type and provider, groups by resource type with counts, and flags tainted resources.

~~~powershell
# tf-state-audit.ps1
# Run from inside your Terraform project directory.
# Usage: cd C:\path\to\terraform\project ; .\tf-state-audit.ps1

#Requires -Version 5.1

$ErrorActionPreference = "Stop"
$Timestamp  = Get-Date -Format "yyyyMMdd-HHmmss"
$ReportFile = Join-Path $env:USERPROFILE "Desktop\tf-state-audit-$Timestamp.txt"

function Write-Report {
    param([string]$Line)
    Write-Host $Line
    Add-Content -Path $ReportFile -Value $Line
}

Write-Report "=== Terraform State Audit ==="
Write-Report "Run at  : $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Write-Report "Folder  : $(Get-Location)"
Write-Report ""

try {
    $tfVer = terraform -version 2>&1 | Select-Object -First 1
    Write-Report "Terraform : $tfVer"
} catch {
    Write-Host "ERROR: terraform not found in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "[1/4] Reading state with terraform show -json..." -ForegroundColor Yellow
$state = terraform show -json 2>&1 | ConvertFrom-Json

Write-Host "[2/4] Extracting resources..." -ForegroundColor Yellow
$resources = @()
if ($state.values.root_module.resources) { $resources += $state.values.root_module.resources }
if ($state.values.root_module.child_modules) {
    foreach ($m in $state.values.root_module.child_modules) {
        if ($m.resources) { $resources += $m.resources }
    }
}

if ($resources.Count -eq 0) {
    Write-Report "No resources found in state."
    exit 0
}

Write-Host "[3/4] Building resource list..." -ForegroundColor Yellow
Write-Report "=== All Resources ($($resources.Count) total) ==="
Write-Report ("{0,-60} {1,-35} {2}" -f "Address", "Type", "Provider")
Write-Report ("-" * 110)

$tainted = @()
foreach ($r in $resources) {
    Write-Report ("{0,-60} {1,-35} {2}" -f $r.address, $r.type, $r.provider_name)
    if ($r.tainted -eq $true) { $tainted += $r.address }
}

Write-Host "[4/4] Grouping by type..." -ForegroundColor Yellow
Write-Report ""
Write-Report "=== Resource Count by Type ==="
$resources | Group-Object -Property type | Sort-Object Count -Descending | ForEach-Object {
    Write-Report ("{0,-45} {1}" -f $_.Name, $_.Count)
}

Write-Report ""
Write-Report "=== Tainted Resources ==="
if ($tainted.Count -eq 0) {
    Write-Report "None."
} else {
    Write-Report "WARNING: $($tainted.Count) tainted resource(s) found."
    $tainted | ForEach-Object { Write-Report "  TAINTED: $_" }
}

Write-Report ""
Write-Report "Report saved to : $ReportFile"
Write-Host "Audit complete. Report: $ReportFile" -ForegroundColor Green
~~~

#### How to run this script — step by step

**Before you start — what you need**
- Windows 10 or later with Terraform installed and in your PATH
- A Terraform project directory where `terraform apply` has been run at least once

**Step 1 — Save the file**

Save the script as `tf-state-audit.ps1` in your Terraform project folder or Desktop.

**Step 2 — Open PowerShell and navigate to your Terraform project**

```
cd C:\path\to\your\terraform\project
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\tf-state-audit.ps1
```

**What you should see**

A table of all resources in state (address, type, provider), a count grouped by resource type, and a tainted resources section. A `.txt` report is saved to your Desktop.
