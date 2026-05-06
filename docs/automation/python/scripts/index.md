# Scripts

## Purpose

Use this page for practical Python Scripts notes, checks, troubleshooting, commands, change notes, and field references.

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful commands

Add tested commands here.

## Known issues

Add known issues here as they come up.

---

## Windows: Run Python Scripts from Command Prompt (CMD Batch)

Checks for Python, creates a virtual environment, installs common infrastructure packages, and runs a specified Python script with environment variables pre-set. Suitable for running any of the scripts in this KB from a Windows machine without needing to install packages globally.

~~~bat
@echo off
REM run-py-script.bat
REM Usage: Edit the variables below, then double-click or run from Command Prompt.
REM        The script you want to run must be in the same folder as this .bat file,
REM        or provide a full path in PY_SCRIPT below.

setlocal enabledelayedexpansion

REM -----------------------------------------------------------------------
REM EDIT THESE VALUES
REM -----------------------------------------------------------------------
set PY_SCRIPT=your_script.py
set VENV_DIR=C:\venvs\kb-scripts

REM Infrastructure environment variables — change to match your environment
set FA_HOST=192.168.1.100
set FA_API_TOKEN=your-token-here
set AWS_ACCESS_KEY_ID=your-access-key
set AWS_SECRET_ACCESS_KEY=your-secret-key
set AWS_DEFAULT_REGION=us-east-1
REM -----------------------------------------------------------------------

echo.
echo === Python Script Runner ===
echo Script   : %PY_SCRIPT%
echo Venv     : %VENV_DIR%
echo.

REM --- Step 1: Check Python is installed ---
echo [1/5] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH.
    echo        Download and install Python 3 from https://python.org/downloads/
    echo        During install, check "Add Python to PATH".
    pause
    exit /b 1
)
python --version
echo Python found.
echo.

REM --- Step 2: Create virtual environment if it doesn't exist ---
echo [2/5] Setting up virtual environment at %VENV_DIR%...
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating new virtual environment...
    python -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created.
) else (
    echo Virtual environment already exists, skipping creation.
)
echo.

REM --- Step 3: Activate the virtual environment ---
echo [3/5] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
echo Activated.
echo.

REM --- Step 4: Install required packages ---
echo [4/5] Installing/updating packages...
pip install --quiet --upgrade pip
pip install py-pure-client pyVmomi requests netapp-ontap paramiko boto3
if errorlevel 1 (
    echo ERROR: Package installation failed.
    pause
    exit /b 1
)
echo Packages installed.
echo.

REM --- Step 5: Run the script ---
echo [5/5] Running %PY_SCRIPT%...
echo.
python "%PY_SCRIPT%"
set SCRIPT_RC=%errorlevel%

echo.
if %SCRIPT_RC% equ 0 (
    echo Script completed successfully.
) else (
    echo Script exited with code %SCRIPT_RC%.
)

deactivate
pause
endlocal
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows PC with Python 3.8 or later installed (download from python.org)
- The Python script you want to run saved to your Desktop or a folder you know
- Network access to any infrastructure hosts referenced in the script

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC (search in the Start menu)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `run-py-script.bat` and save it to the same folder as your Python script (e.g. your Desktop)

**Step 2 — Fill in your details**

Open the file and change these values near the top:

| Variable | What to enter | Where to find it |
|---|---|---|
| `PY_SCRIPT` | Filename of the Python script to run | The `.py` file in the same folder |
| `VENV_DIR` | Folder path for the virtual environment | Keep default `C:\venvs\kb-scripts` or change it |
| `FA_HOST` | IP address of your FlashArray | FlashArray management interface IP |
| `FA_API_TOKEN` | API token for FlashArray auth | FlashArray GUI → System → API Tokens |
| `AWS_ACCESS_KEY_ID` | AWS access key ID | AWS IAM → Security credentials |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key | AWS IAM → Security credentials |
| `AWS_DEFAULT_REGION` | AWS region code (e.g. `us-east-1`) | Your AWS console region selector |

Remove or ignore any variables your specific script does not use.

**Step 3 — Open a terminal**

Open Command Prompt: press `Windows key`, type `cmd`, press Enter.

**Step 4 — Run the script**

```
cd C:\Users\YourName\Desktop
run-py-script.bat
```

Or simply double-click the `run-py-script.bat` file in File Explorer.

**What you should see**

The script prints numbered progress steps (1/5 through 5/5), installs packages on first run (subsequent runs skip this if already installed), then prints the output of your Python script. A "Script completed successfully." message appears at the end if the script exits cleanly. The window pauses so you can read the output before it closes.

---

## Windows: Python Environment Setup (PowerShell)

One-time setup script that verifies Python 3 is installed, creates a virtual environment in your Documents folder, installs common infrastructure packages, and validates that each key package imports correctly. Run this once before using any Python scripts in this KB.

~~~powershell
# setup-python-env.ps1
# Run once to set up your Python environment on Windows.
# Usage: Right-click → Run with PowerShell  (or see step-by-step guide below)

#Requires -Version 5.1

$ErrorActionPreference = "Stop"

$VenvPath = Join-Path $env:USERPROFILE "Documents\kb-venv"
$Packages = @(
    "py-pure-client",
    "pyVmomi",
    "requests",
    "netapp-ontap",
    "paramiko",
    "boto3"
)

Write-Host ""
Write-Host "=== Python Environment Setup ===" -ForegroundColor Cyan
Write-Host "Virtual environment: $VenvPath"
Write-Host ""

# --- Step 1: Check for Python 3 ---
Write-Host "[1/5] Checking for Python 3..." -ForegroundColor Yellow
$pythonCmd = $null

foreach ($cmd in @("python", "python3")) {
    try {
        $ver = & $cmd --version 2>&1
        if ($ver -match "Python 3\.") {
            $pythonCmd = $cmd
            Write-Host "Found: $ver (command: $cmd)" -ForegroundColor Green
            break
        }
    } catch { }
}

if (-not $pythonCmd) {
    Write-Host ""
    Write-Host "ERROR: Python 3 is not installed or not in PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "To install Python 3, run the following command in a terminal:" -ForegroundColor Yellow
    Write-Host "  winget install Python.Python.3" -ForegroundColor White
    Write-Host ""
    Write-Host "Or download manually from https://python.org/downloads/" -ForegroundColor White
    Write-Host "During install, check 'Add Python to PATH'." -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# --- Step 2: Create virtual environment ---
Write-Host ""
Write-Host "[2/5] Setting up virtual environment..." -ForegroundColor Yellow

if (Test-Path (Join-Path $VenvPath "Scripts\Activate.ps1")) {
    Write-Host "Virtual environment already exists at $VenvPath, skipping creation." -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment at $VenvPath..."
    & $pythonCmd -m venv $VenvPath
    Write-Host "Virtual environment created." -ForegroundColor Green
}

# --- Step 3: Activate virtual environment ---
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
$activateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
. $activateScript
Write-Host "Activated." -ForegroundColor Green

# --- Step 4: Install packages ---
Write-Host ""
Write-Host "[4/5] Installing packages..." -ForegroundColor Yellow
python -m pip install --quiet --upgrade pip
foreach ($pkg in $Packages) {
    Write-Host "  Installing $pkg..."
    python -m pip install --quiet $pkg
}
Write-Host "All packages installed." -ForegroundColor Green

# --- Step 5: Test imports ---
Write-Host ""
Write-Host "[5/5] Testing package imports..." -ForegroundColor Yellow

$importTests = @{
    "py-pure-client" = "import purestorage"
    "pyVmomi"        = "import pyVmomi"
    "boto3"          = "import boto3"
    "requests"       = "import requests"
    "paramiko"       = "import paramiko"
    "netapp-ontap"   = "import netapp_ontap"
}

$results = @()
foreach ($entry in $importTests.GetEnumerator()) {
    $pkg  = $entry.Key
    $stmt = $entry.Value
    try {
        $output = python -c $stmt 2>&1
        if ($LASTEXITCODE -eq 0) {
            $results += [PSCustomObject]@{ Package = $pkg; Status = "OK"; Version = (python -c "import importlib.metadata; print(importlib.metadata.version('$pkg'))" 2>$null) }
        } else {
            $results += [PSCustomObject]@{ Package = $pkg; Status = "FAIL"; Version = "-" }
        }
    } catch {
        $results += [PSCustomObject]@{ Package = $pkg; Status = "FAIL"; Version = "-" }
    }
}

# --- Summary ---
Write-Host ""
Write-Host "=== Installed Package Summary ===" -ForegroundColor Cyan
Write-Host ("{0,-20} {1,-10} {2}" -f "Package", "Status", "Version")
Write-Host ("-" * 50)
foreach ($r in $results) {
    $color = if ($r.Status -eq "OK") { "Green" } else { "Red" }
    Write-Host ("{0,-20} {1,-10} {2}" -f $r.Package, $r.Status, $r.Version) -ForegroundColor $color
}

$failed = $results | Where-Object { $_.Status -ne "OK" }
Write-Host ""
if ($failed) {
    Write-Host "WARNING: $($failed.Count) package(s) failed to import. Review errors above." -ForegroundColor Red
} else {
    Write-Host "SUCCESS: All packages imported successfully." -ForegroundColor Green
    Write-Host "Your Python environment is ready. Activate it with:" -ForegroundColor White
    Write-Host "  . `"$activateScript`"" -ForegroundColor White
}

Write-Host ""
Read-Host "Press Enter to exit"
~~~

#### How to run this script — step by step

**Before you start — what you need**
- A Windows PC (Windows 10 or later)
- Internet access to download packages from PyPI
- Administrator rights are not required, but PowerShell must be able to run scripts (the guide covers this)

**Step 1 — Save the file**

1. Open **Notepad** on your Windows PC (search in the Start menu)
2. Copy the entire code block above
3. Click **File → Save As**
4. Set "Save as type" to **All Files**
5. Name it `setup-python-env.ps1` and save it to your Desktop

**Step 2 — Fill in your details**

This script uses sensible defaults. The only value you may want to change is the virtual environment path:

| Variable | What to enter | Where to find it |
|---|---|---|
| `$VenvPath` | Folder where the virtual environment is created | Defaults to `Documents\kb-venv` — change if you prefer a different location |

**Step 3 — Open a terminal**

Press `Windows key`, type `PowerShell`, right-click **Windows PowerShell**, and select **Run as Administrator**.

**Step 4 — Allow scripts to run**

In the PowerShell window, paste and press Enter:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

**Step 5 — Run the script**

```
cd C:\Users\YourName\Desktop
.\setup-python-env.ps1
```

**What you should see**

The script steps through 5 numbered stages printed in yellow. If Python is missing it prints installation instructions and stops. Otherwise it creates the virtual environment, installs all six packages, then tests each import and prints a colour-coded summary table showing the package name, OK/FAIL status, and installed version. A green "SUCCESS" message confirms everything is ready.
