---
tags:
  - ansible
  - operations
description: "Ansible automation scripts: wrapper scripts for playbook execution, dynamic inventory queries, vault-encrypted credential injection, and CI/CD pipeline..."
---
# Ansible — Scripts

<div class="kb-summary">
Ansible automation scripts: wrapper scripts for playbook execution, dynamic inventory queries, vault-encrypted credential injection, and CI/CD pipeline integration patterns.

*Applies to: Ansible 2.14+*
</div>

---

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Secret Rotation Workflow

```d2
direction: right

trigger: "Trigger\n(manual / schedule" {shape: rectangle}
backup: "Backup current\nvault file" {shape: rectangle}
generate: "Generate new\npassword (openssl" {shape: rectangle}
encrypt: "ansible-vault\nencrypt_string" {shape: rectangle}
updateVars: "Update\ndb_secrets.yml" {shape: rectangle}
runPlaybook: "Run push-db-secret.yml\n(ansible-playbook" {shape: rectangle}
success: "Success:\nRotation complete" {shape: rectangle}
rollback: "Rollback:\nRestore backup" {shape: rectangle}

trigger -> backup
backup -> generate
generate -> encrypt
encrypt -> updateVars
updateVars -> runPlaybook
runPlaybook -> success
runPlaybook -> rollback
```

**What you should see**

Ansible connects to each server in sequence and runs disk, load, and service checks. Each check prints a warning if thresholds are exceeded. At the end, a summary aggregates the results for all servers. If any servers are unreachable, they are flagged as UNREACHABLE.

---

## Rolling Update Playbook

Update a web application fleet one host at a time without downtime: drain from the load balancer, stop, update, start, health-check, and re-add. Stops immediately on first failure.

```yaml
---
# rolling-update.yml
# Usage: ansible-playbook rolling-update.yml -i inventory/hosts.yml
#        -e "app_package=myapp app_version=2.3.1 lb_api_url=http://lb.example.com/api lb_token=TOKEN"

- name: Rolling Application Update
  hosts: web_servers
  serial: 1
  max_fail_percentage: 0
  gather_facts: true

  vars:
    app_package:      "{{ app_package }}"
    app_version:      "{{ app_version }}"
    app_service:      "myapp"
    health_check_url: "http://{{ ansible_host }}:8080/health"
    health_check_retries: 10
    health_check_delay:   5
    lb_api_url:       "{{ lb_api_url }}"
    lb_token:         "{{ lb_token }}"
    drain_timeout:    30

  tasks:

    - name: Drain host from load balancer
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/drain"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
          Content-Type: "application/json"
        body_format: json
        body:
          state: "drain"
        status_code: [200, 202]
      delegate_to: localhost
      register: drain_result

    - name: Wait for active connections to drop
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/connections"
        method: GET
        headers:
          Authorization: "Bearer {{ lb_token }}"
        return_content: true
      register: conn_check
      until: (conn_check.json.active_connections | int) == 0
      retries: "{{ (drain_timeout / 5) | int }}"
      delay: 5
      delegate_to: localhost
      ignore_errors: true

    - name: Stop application service
      systemd:
        name: "{{ app_service }}"
        state: stopped
      become: true

    - name: Update application package
      package:
        name: "{{ app_package }}={{ app_version }}"
        state: present
      become: true
      register: package_update

    - name: Start application service
      systemd:
        name: "{{ app_service }}"
        state: started
        enabled: true
      become: true

    - name: Health check application endpoint
      uri:
        url: "{{ health_check_url }}"
        method: GET
        status_code: 200
        return_content: true
      register: health_check
      until: health_check.status == 200
      retries: "{{ health_check_retries }}"
      delay: "{{ health_check_delay }}"
      delegate_to: localhost

    - name: Re-add host to load balancer
      uri:
        url: "{{ lb_api_url }}/backends/{{ inventory_hostname }}/drain"
        method: POST
        headers:
          Authorization: "Bearer {{ lb_token }}"
          Content-Type: "application/json"
        body_format: json
        body:
          state: "active"
        status_code: [200, 202]
      delegate_to: localhost

    - name: Report update result for this host
      debug:
        msg: "{{ inventory_hostname }}: updated to {{ app_version }}, health OK, back in LB."
```

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on Linux or WSL
- SSH access to your web servers
- A load balancer with an API that supports draining/activating backends (the URLs in the playbook must match your LB's API)
- The application packaged as a system package that can be installed with `apt`/`yum`

**Step 1 — Save the file**

1. Open your WSL terminal
2. Create the file: `nano rolling-update.yml`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save

**Step 2 — Fill in your details**

Most values are passed on the command line with `-e`. Update defaults in the `vars:` section as needed:

| Variable | What to enter | Where to find it |
|---|---|---|
| `app_service` | The systemd service name for your app | Run `systemctl list-units` on your server |
| `health_check_url` | The URL to check that your app is healthy | Your app's health endpoint |
| `drain_timeout` | Seconds to wait for connections to drain | Default: `30` |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook rolling-update.yml -i inventory/hosts.yml \
  -e "app_package=myapp app_version=2.3.1 lb_api_url=http://lb.example.com/api lb_token=YOUR_TOKEN"
```


```text title="Expected output"
PLAY [web_servers] *************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-prod-01.example.com]
ok: [web-prod-02.example.com]
ok: [web-prod-03.example.com]

TASK [Check current app version] ***********************************************
ok: [web-prod-01.example.com] => {"version": "2.2.5"}
ok: [web-prod-02.example.com] => {"version": "2.2.5"}
ok: [web-prod-03.example.com] => {"version": "2.2.5"}

TASK [Drain connections from load balancer] ************************************
ok: [web-prod-01.example.com]
ok: [web-prod-02.example.com]
ok: [web-prod-03.example.com]

TASK [Install myapp version 2.3.1] *********************************************
changed: [web-prod-01.example.com]
changed: [web-prod-02.example.com]
changed: [web-prod-03.example.com]

TASK [Verify service health] ***************************************************
ok: [web-prod-01.example.com]
ok: [web-prod-02.example.com]
ok: [web-prod-03.example.com]

TASK [Re-enable in load balancer] **********************************************
ok: [web-prod-01.example.com]
ok: [web-prod-02.example.com]
ok: [web-prod-03.example.com]

PLAY RECAP *********************************************************************
web-prod-01.example.com : ok=6 changed=1 unreachable=0 failed=0
web-prod-02.example.com : ok=6 changed=1 unreachable=0 failed=0
web-prod-03.example.com : ok=6 changed=1 unreachable=0 failed=0
```

!!! warning "Common errors"
    **`fatal: [web-prod-02.example.com]: FAILED! => {"msg": "The conditional check 'lb_token is defined' failed because one of the variables is undefined: lb_token"}`** — Replace `YOUR_TOKEN` with an actual token value or pass it via `-e "lb_token=<actual_token>"`.
    **`[WARNING]: Unable to parse inventory/hosts.yml as an inventory source`** — Verify the inventory file path is correct relative to the current directory and the YAML syntax is valid.
    **`fatal: [web-prod-01.example.com]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH keys are configured correctly and the ansible user has passwordless SSH access to all target hosts.
**What you should see**

Ansible processes one server at a time. For each server you see: drain request, wait for connections to drop, service stop, package update, service start, health check (retries until 200 OK), then re-add to LB. If any step fails the playbook stops completely — no other servers are touched.

---

## Inventory Validation Playbook

Verify that every inventory host meets baseline configuration requirements: SSH access, Python, sudoers, required packages, hostname, NTP sync, and DNS resolution.

```yaml
---
# inventory-validate.yml
# Usage: ansible-playbook inventory-validate.yml -i inventory/hosts.yml

- name: Inventory Validation
  hosts: all
  gather_facts: true
  become: true

  vars:
    required_packages:
      - python3
      - curl
      - rsync
      - sudo
    ntp_service: "chronyd"   # or "ntp" depending on distro

  tasks:

    - name: Verify SSH connection
      ping:
      register: ssh_check

    - name: Verify Python is installed
      command: python3 --version
      register: python_check
      changed_when: false
      failed_when: false

    - name: Verify sudo access
      command: sudo -n true
      register: sudo_check
      changed_when: false
      failed_when: false

    - name: Check required packages
      package_facts:
        manager: auto

    - name: Flag missing packages
      set_fact:
        missing_packages: >-
          {{
            required_packages |
            reject('in', ansible_facts.packages.keys()) |
            list
          }}

    - name: Verify hostname matches inventory name
      set_fact:
        hostname_match: "{{ ansible_hostname == inventory_hostname.split('.')[0] }}"

    - name: Check NTP synchronisation
      command: "timedatectl show --property=NTPSynchronized --value"
      register: ntp_sync
      changed_when: false
      failed_when: false

    - name: Verify DNS resolution
      command: "getent hosts {{ inventory_hostname }}"
      register: dns_check
      changed_when: false
      failed_when: false
      delegate_to: localhost

    # Build per-host result
    - name: Compile validation results
      set_fact:
        validation_result:
          host:              "{{ inventory_hostname }}"
          ssh:               "{{ 'PASS' if ssh_check is defined else 'FAIL' }}"
          python:            "{{ 'PASS' if python_check.rc == 0 else 'FAIL' }}"
          sudo:              "{{ 'PASS' if sudo_check.rc == 0 else 'FAIL' }}"
          required_packages: "{{ 'PASS' if missing_packages | length == 0 else 'FAIL: missing ' + missing_packages | join(',') }}"
          hostname_match:    "{{ 'PASS' if hostname_match else 'FAIL (got ' + ansible_hostname + ')' }}"
          ntp_sync:          "{{ 'PASS' if ntp_sync.stdout == 'yes' else 'FAIL' }}"
          dns:               "{{ 'PASS' if dns_check.rc == 0 else 'FAIL' }}"

    - name: Print per-host validation table
      debug:
        msg:
          - "Host      : {{ validation_result.host }}"
          - "SSH       : {{ validation_result.ssh }}"
          - "Python    : {{ validation_result.python }}"
          - "Sudo      : {{ validation_result.sudo }}"
          - "Packages  : {{ validation_result.required_packages }}"
          - "Hostname  : {{ validation_result.hostname_match }}"
          - "NTP       : {{ validation_result.ntp_sync }}"
          - "DNS       : {{ validation_result.dns }}"

    - name: Persist results to controller
      set_fact:
        validation_result: "{{ validation_result }}"
      delegate_to: localhost
      delegate_facts: true

- name: Validation Summary
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Identify non-compliant hosts
      set_fact:
        non_compliant: >-
          {{
            groups['all'] |
            map('extract', hostvars) |
            selectattr('validation_result', 'defined') |
            selectattr('validation_result.ssh', 'ne', 'PASS') |
            map(attribute='validation_result.host') |
            list
          }}

    - name: Print non-compliant summary
      debug:
        msg: "Non-compliant hosts: {{ non_compliant }}"

    - name: Fail if any non-compliant hosts
      fail:
        msg: "Validation failed for: {{ non_compliant | join(', ') }}"
      when: non_compliant | length > 0
```

### How to run this script — step by step

**Before you start — what you need**
- Ansible installed on Linux or WSL
- SSH access to all the hosts in your inventory
- Your Ansible user must have sudo rights on the remote hosts

**Step 1 — Save the file**

1. Open your WSL terminal
2. Create the file: `nano inventory-validate.yml`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save

**Step 2 — Fill in your details**

Update the `vars:` section to match your environment:

| Variable | What to enter | Where to find it |
|---|---|---|
| `required_packages` | List of packages every server must have | Your organisation's baseline requirements |
| `ntp_service` | Name of your NTP service | `chronyd` on RHEL/CentOS, `ntp` on older Debian |

**Step 3 — Open the right terminal**

- **For .yml (Ansible):** Needs Linux or WSL. Open your WSL terminal.

**Step 4 — Run it**

```bash
cd ~
ansible-playbook inventory-validate.yml -i inventory/hosts.yml
```


```text title="Expected output"
PLAY [Validating Ansible Inventory] ****************************

TASK [Gathering Facts] *****************************************
ok: [web-prod-01.internal]
ok: [web-prod-02.internal]
ok: [db-primary.internal]
ok: [db-replica.internal]

TASK [Check inventory syntax] **********************************
ok: [web-prod-01.internal] => {
    "msg": "Inventory validation passed"
}

TASK [Validate host connectivity] ******************************
ok: [web-prod-01.internal]
ok: [web-prod-02.internal]
ok: [db-primary.internal]
ok: [db-replica.internal]

PLAY RECAP *****************************************************
web-prod-01.internal       : ok=3    changed=0    unreachable=0    failed=0
web-prod-02.internal       : ok=3    changed=0    unreachable=0    failed=0
db-primary.internal        : ok=3    changed=0    unreachable=0    failed=0
db-replica.internal        : ok=3    changed=0    unreachable=0    failed=0
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory: 'inventory/hosts.yml'`** — Verify the inventory file path is correct relative to your current working directory or use an absolute path with `-i`.
    **`ERROR! Syntax Error while loading YAML from 'inventory-validate.yml'`** — Check the playbook YAML syntax for indentation errors or invalid key-value pairs using `ansible-playbook --syntax-check inventory-validate.yml`.
    **`fatal: [web-prod-01.internal]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh"}`** — Ensure SSH keys are configured correctly and the target hosts are reachable; verify with `ssh -v <hostname>` first.
**What you should see**

For each host in your inventory, a table is printed showing PASS or FAIL for each check: SSH, Python, sudo, required packages, hostname, NTP, and DNS. At the end, a list of non-compliant hosts is shown. The playbook fails (exits non-zero) if any hosts fail the SSH check.

---

## Secret Rotation with Vault (Bash + Ansible)

Bash wrapper that generates a new database password, encrypts it into an Ansible Vault file, runs the playbook to push it to the database and app servers, and rolls back if the playbook fails.

```bash
#!/usr/bin/env bash
# rotate-db-secret.sh
# Usage: VAULT_PASSWORD_FILE=<path> DB_VARS_FILE=<path> ./rotate-db-secret.sh
#
# Requires: ansible, ansible-vault, openssl, python3

set -euo pipefail

VAULT_PASSWORD_FILE="${VAULT_PASSWORD_FILE:?VAULT_PASSWORD_FILE is required}"
DB_VARS_FILE="${DB_VARS_FILE:-vars/db_secrets.yml}"
PLAYBOOK="${PLAYBOOK:-playbooks/push-db-secret.yml}"
INVENTORY="${INVENTORY:-inventory/hosts.yml}"
BACKUP_FILE="/tmp/db_secrets_backup_$(date +%Y%m%d%H%M%S).yml"
LOGFILE="/var/log/secret-rotation-$(date +%Y%m%d-%H%M%S).log"

log() {
    local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $*"
    echo "${msg}"
    echo "${msg}" >> "${LOGFILE}"
}

log "=== Database Secret Rotation ==="
log "Vars file : ${DB_VARS_FILE}"
log "Playbook  : ${PLAYBOOK}"

# --- Step 1: Backup current vault file ---
log "Step 1: Backing up current vars file to ${BACKUP_FILE}..."
cp "${DB_VARS_FILE}" "${BACKUP_FILE}"

# --- Step 2: Generate new password ---
log "Step 2: Generating new database password..."
NEW_PASSWORD=$(openssl rand -base64 32 | tr -d '=+/' | cut -c1-24)
log "New password generated (not logged)."

# --- Step 3: Encrypt new password with Ansible Vault ---
log "Step 3: Encrypting new password with Ansible Vault..."
ENCRYPTED_VALUE=$(ansible-vault encrypt_string \
    --vault-password-file "${VAULT_PASSWORD_FILE}" \
    --stdin-name "db_password" <<< "${NEW_PASSWORD}")

# Update the vars file: replace the db_password line with new encrypted value.
python3 - <<EOF
import re, sys

with open('${DB_VARS_FILE}', 'r') as f:
    content = f.read()

new_content = re.sub(
    r'^db_password:.*?(?=^\w|\Z)',
    '',
    content,
    flags=re.MULTILINE | re.DOTALL
)

new_content = new_content.rstrip('\n') + '\n' + '''${ENCRYPTED_VALUE}''' + '\n'

with open('${DB_VARS_FILE}', 'w') as f:
    f.write(new_content)

print("Vars file updated.")
EOF

log "Vars file updated with new encrypted password."

# --- Step 4: Run Ansible playbook to push new password ---
log "Step 4: Running Ansible playbook to push new password..."
if ansible-playbook \
    --vault-password-file "${VAULT_PASSWORD_FILE}" \
    -i "${INVENTORY}" \
    -e "db_password=${NEW_PASSWORD}" \
    "${PLAYBOOK}" 2>&1 | tee -a "${LOGFILE}"; then
    log "Playbook succeeded. Secret rotation complete."
    log "Backup of old vars: ${BACKUP_FILE}"
else
    # --- Step 5: Rollback on failure ---
    log "ERROR: Playbook failed. Rolling back vars file from backup..."
    cp "${BACKUP_FILE}" "${DB_VARS_FILE}"
    log "Rollback complete. Old vars file restored."
    log "MANUAL ACTION REQUIRED: The database password was NOT successfully rotated."
    log "  Review playbook errors above and investigate before retrying."
    exit 1
fi
```


```text title="Expected output"
[2024-01-15 14:32:18] === Database Secret Rotation ===
[2024-01-15 14:32:18] Vars file : vars/db_secrets.yml
[2024-01-15 14:32:18] Playbook  : playbooks/push-db-secret.yml
[2024-01-15 14:32:18] Step 1: Backing up current vars file to /tmp/db_secrets_backup_20240115143218.yml...
[2024-01-15 14:32:18] Step 2: Generating new database password...
[2024-01-15 14:32:18] New password generated (not logged).
[2024-01-15 14:32:18] Step 3: Encrypting new password with Ansible Vault...
[2024-01-15 14:32:19] Vars file updated.
[2024-01-15 14:32:19] Vars file updated with new encrypted password.
[2024-01-15 14:32:19] Step 4: Running Ansible playbook to push new password...
[2024-01-15 14:32:22] PLAY [all] *********************************************************************
[2024-01-15 14:32:23] TASK [Update database password on primary] *************************************
[2024-01-15 14:32:25] changed: [db-primary-01.prod.local]
[2024-01-15 14:32:26] changed: [db-replica-01.prod.local]
[2024-01-15 14:32:27] PLAY RECAP *********************************************************************
[2024-01-15 14:32:27] db-primary-01.prod.local : ok=1 changed=1 unreachable=0 failed=0
[2024-01-15 14:32:27] db-replica-01.prod.local : ok=1 changed=1 unreachable=0 failed=0
[2024-01-15 14:32:27] Playbook succeeded. Secret rotation complete.
[2024-01-15 14:32:27] Backup of old vars: /tmp/db_secrets_backup_20240115143218.yml
```

!!! warning "Common errors"
    **`VAULT_PASSWORD_FILE is required`** — Set the environment variable before running: `export VAULT_PASSWORD_FILE=/path/to/vault/password`
    **`No such file or directory: vars/db_secrets.yml`** — Verify the DB_VARS_FILE path exists or set it explicitly: `DB_VARS_FILE=path/to/file ./rotate-db-secret.sh`
    **`ERROR! the playbook: playbooks/push-db-secret.yml could not be found`** — Confirm the PLAYBOOK path is correct and relative to your working directory, or set it explicitly: `PLAYBOOK=correct/path.yml ./rotate-db-secret.sh`
### How to run this script — step by step

**Before you start — what you need**
- Ansible and Ansible Vault installed on Linux or WSL
- `openssl` available (already installed on most Linux systems)
- A vault password file (a plain text file containing just the vault password)
- An existing Ansible Vault-encrypted vars file with a `db_password:` entry
- A playbook that applies the new password to your database servers

**Step 1 — Save the file**

1. Open your WSL terminal
2. Create the file: `nano rotate-db-secret.sh`
3. Paste the code, then press `Ctrl+X`, `Y`, `Enter` to save
4. Make it executable: `chmod +x rotate-db-secret.sh`

**Step 2 — Fill in your details**

| Variable | What to enter | Where to find it |
|---|---|---|
| `VAULT_PASSWORD_FILE` | Path to the file containing your Ansible Vault password | Wherever you store it securely |
| `DB_VARS_FILE` | Path to your encrypted vars file | Your Ansible project directory |
| `PLAYBOOK` | Path to the playbook that applies the new password | Your Ansible project directory |
| `INVENTORY` | Path to your inventory file | Your Ansible project directory |

**Step 3 — Open the right terminal**

- **For .sh (Bash):** Open your WSL terminal (Git Bash also works).

**Step 4 — Run it**

```bash
export VAULT_PASSWORD_FILE=/path/to/vault-password.txt
export DB_VARS_FILE=vars/db_secrets.yml
export PLAYBOOK=playbooks/push-db-secret.yml
bash rotate-db-secret.sh
```


```text title="Expected output"
Vault password file found at /path/to/vault-password.txt
Loading database variables from vars/db_secrets.yml
Executing playbook: playbooks/push-db-secret.yml
PLAY [all] *********************************************************************
TASK [Gathering Facts] *********************************************************
ok: [db-prod-01.internal]
ok: [db-prod-02.internal]
TASK [Rotate database credentials] *********************************************
changed: [db-prod-01.internal]
changed: [db-prod-02.internal]
PLAY RECAP *********************************************************************
db-prod-01.internal        : ok=2    changed=1    unreachable=0    failed=0
db-prod-02.internal        : ok=2    changed=1    unreachable=0    failed=0
Secret rotation completed successfully at 2024-01-15T09:42:17Z
```

!!! warning "Common errors"
    **`No such file or directory`** — Verify the vault password file path exists and is readable with `ls -l /path/to/vault-password.txt`.
    **`vars/db_secrets.yml: No such file or directory`** — Ensure you are running the script from the correct working directory (typically the Ansible project root) where the vars/ subdirectory exists.
    **`ERROR! Decryption failed`** — Check that the vault password file contains the correct decryption key and matches the vault ID used to encrypt the secrets file.
**What you should see**

Step-by-step log messages showing: backup created, new password generated, password encrypted with Ansible Vault, vars file updated, playbook running. If the playbook succeeds you see a success message. If the playbook fails, the old vars file is automatically restored from backup and the script exits with an error so you can investigate.

---

## Windows: Run Ansible Playbooks from Windows via WSL (CMD Batch)

Ansible does not run natively on Windows. This batch file uses WSL (Windows Subsystem for Linux) to run your Ansible playbooks without leaving Windows.

```batch
@echo off
REM ansible-run.bat
REM Runs an Ansible playbook via WSL from Windows.

set PLAYBOOK=playbook.yml
set INVENTORY=inventory.ini
set EXTRA_VARS=

echo === Ansible Playbook Runner (via WSL) ===
echo Playbook  : %PLAYBOOK%
echo Inventory : %INVENTORY%
echo.

wsl --status >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: WSL is not installed or not running.
    pause
    exit /b 1
)

if "%EXTRA_VARS%"=="" (
    wsl ansible-playbook /mnt/c/Users/%USERNAME%/Desktop/%PLAYBOOK% -i /mnt/c/Users/%USERNAME%/Desktop/%INVENTORY%
) else (
    wsl ansible-playbook /mnt/c/Users/%USERNAME%/Desktop/%PLAYBOOK% -i /mnt/c/Users/%USERNAME%/Desktop/%INVENTORY% -e "%EXTRA_VARS%"
)

if %errorlevel% equ 0 (
    echo.
    echo Playbook completed successfully.
) else (
    echo.
    echo Playbook FAILED. Check the output above for errors.
)

pause
```

---

## Windows: Ansible Inventory Ping Test (PowerShell + WSL)

Test that Ansible can reach all hosts in your inventory by running `ansible all -m ping` via WSL from PowerShell. Shows a count of successful and failed hosts.

```powershell
# ansible-ping-test.ps1
param(
    [Parameter(Mandatory)]
    [string]$InventoryFile
)

function ConvertTo-WslPath {
    param([string]$WindowsPath)
    $path = $WindowsPath.Replace('\', '/')
    if ($path -match '^([A-Za-z]):(.*)') {
        $drive = $Matches[1].ToLower()
        $rest  = $Matches[2]
        return "/mnt/$drive$rest"
    }
    return $path
}

$wslInventoryPath = ConvertTo-WslPath -WindowsPath $InventoryFile

Write-Host "`n=== Ansible Inventory Ping Test ===" -ForegroundColor Cyan
Write-Host "Inventory (Windows): $InventoryFile"
Write-Host "Inventory (WSL)    : $wslInventoryPath`n"

$output = wsl ansible all -m ping -i $wslInventoryPath 2>&1
$output | ForEach-Object { Write-Host $_ }

$successCount = ($output | Select-String "SUCCESS").Count
$failedCount  = ($output | Select-String "FAILED|UNREACHABLE").Count

Write-Host "`n--- Results ---" -ForegroundColor Cyan
Write-Host "Hosts reachable : $successCount" -ForegroundColor Green
if ($failedCount -gt 0) {
    Write-Host "Hosts failed    : $failedCount" -ForegroundColor Red
} else {
    Write-Host "Hosts failed    : $failedCount" -ForegroundColor Green
}

if ($failedCount -gt 0) {
    Write-Host "`nSome hosts failed. Check SSH keys and network connectivity." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nAll hosts reachable." -ForegroundColor Green
```

---

## Daily Check Script

Check that scheduled Ansible jobs ran successfully. Reads the last Ansible log file for failures, pings all hosts in inventory, and counts reachable vs unreachable hosts.

```bash
#!/bin/bash
# ansible_daily_check.sh — Check Ansible automation health
INVENTORY="${INVENTORY_FILE:-/etc/ansible/hosts}"
ANSIBLE_LOG="${ANSIBLE_LOG_PATH:-/var/log/ansible.log}"
FAIL=0

check() { local l="$1"; shift; "$@" &>/dev/null && echo "[OK] $l" || { echo "[FAIL] $l"; FAIL=$((FAIL+1)); }; }

echo "=== Ansible Daily Check — $(date) ==="
check "Ansible installed" ansible --version
check "Inventory valid" ansible-inventory -i "$INVENTORY" --list

echo "Pinging inventory hosts..."
RESULT=$(ansible all -i "$INVENTORY" -m ping --one-line 2>/dev/null || true)
UNREACHABLE=$(echo "$RESULT" | grep -c "UNREACHABLE" || true)
SUCCESS=$(echo "$RESULT" | grep -c "SUCCESS" || true)
echo "  Reachable: $SUCCESS  |  Unreachable: $UNREACHABLE"
[[ $UNREACHABLE -gt 0 ]] && { echo "[FAIL] $UNREACHABLE host(s) unreachable"; FAIL=$((FAIL+1)); } || echo "[OK] All hosts reachable"

if [[ -f "$ANSIBLE_LOG" ]]; then
  RECENT_FAILS=$(tail -100 "$ANSIBLE_LOG" | grep -c "FAILED!" || true)
  [[ $RECENT_FAILS -gt 0 ]] && { echo "[WARN] $RECENT_FAILS FAILED task(s) in recent log"; } || echo "[OK] No recent task failures in log"
fi

echo ""; echo "Daily check: $FAIL failure(s)"
[[ $FAIL -gt 0 ]] && exit 2 || exit 0
```


```text title="Expected output"
=== Ansible Daily Check — Wed Jan 15 09:42:17 UTC 2025 ===
[OK] Ansible installed
[OK] Inventory valid
Pinging inventory hosts...
  Reachable: 12  |  Unreachable: 2
[FAIL] 2 host(s) unreachable
[WARN] 3 FAILED task(s) in recent log

Daily check: 1 failure(s)
```

!!! warning "Common errors"
    **`[FAIL] Inventory valid`** — Verify the inventory file path in `INVENTORY_FILE` environment variable or `/etc/ansible/hosts` exists and has correct syntax.
    **`ansible: command not found`** — Install Ansible with `pip install ansible` or `apt-get install ansible` depending on your package manager.
    **`Permission denied: '/var/log/ansible.log'`** — Ensure the script runs with sufficient privileges or adjust `ANSIBLE_LOG_PATH` to a readable log location.
---

## Incident Triage Script

Captures a full Ansible environment snapshot to a timestamped file for incident investigation.

```bash
#!/bin/bash
# ansible_incident_triage.sh — Capture Ansible environment snapshot for triage
INVENTORY="${INVENTORY_FILE:-/etc/ansible/hosts}"
ANSIBLE_LOG="${ANSIBLE_LOG_PATH:-/var/log/ansible.log}"
PLAYBOOK_DIR="${PLAYBOOK_DIR:-/etc/ansible/playbooks}"
OUTFILE="/tmp/ansible_triage_$(date +%Y%m%d_%H%M%S).txt"

{
  echo "=== Ansible Incident Triage — $(date) ==="
  echo ""
  echo "--- Ansible Version ---"
  ansible --version 2>&1
  echo ""
  echo "--- Inventory Host List ---"
  ansible-inventory -i "$INVENTORY" --list 2>&1 || ansible all -i "$INVENTORY" --list-hosts 2>&1
  echo ""
  echo "--- Last 100 Lines of Ansible Log ($ANSIBLE_LOG) ---"
  if [[ -f "$ANSIBLE_LOG" ]]; then
    tail -100 "$ANSIBLE_LOG"
  else
    echo "Log file not found: $ANSIBLE_LOG"
  fi
  echo ""
  echo "--- Host Connectivity (ansible ping) ---"
  ansible all -i "$INVENTORY" -m ping --one-line 2>&1 || true
  echo ""
  echo "--- Playbooks in \$PLAYBOOK_DIR ($PLAYBOOK_DIR) ---"
  if [[ -d "$PLAYBOOK_DIR" ]]; then
    find "$PLAYBOOK_DIR" -name "*.yml" -o -name "*.yaml" 2>/dev/null | sort
  else
    echo "Playbook directory not found: $PLAYBOOK_DIR"
  fi
  echo ""
  echo "--- Installed Collections ---"
  ansible-galaxy collection list 2>&1
  echo ""
  echo "--- Installed Roles ---"
  ansible-galaxy role list 2>&1
  echo ""
  echo "=== Triage complete ==="
} | tee "$OUTFILE"

echo ""
echo "Triage output saved to: $OUTFILE"
```


```text title="Expected output"
=== Ansible Incident Triage — Thu Jan 16 14:32:45 UTC 2025 ===

--- Ansible Version ---
ansible [core 2.15.3]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.11/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.11.7 (main, Dec 19 2024, 20:14:01) [GCC 11.4.0]

--- Inventory Host List ---
{
  "all": {
    "hosts": ["web-prod-01", "web-prod-02", "db-primary", "db-replica", "cache-01"],
    "vars": {}
  }
}

--- Last 100 Lines of Ansible Log (/var/log/ansible.log) ---
2025-01-16 14:28:12,456 p=18742 u=ansible | TASK [common : Install base packages] ***
2025-01-16 14:28:45,123 p=18742 u=ansible | FAILED - RETRYING: Wait for port 5432 (attempt 2 of 3)
2025-01-16 14:29:03,891 p=18742 u=ansible | ok: [db-primary] => (item=postgresql-client)
2025-01-16 14:29:15,234 p=18742 u=ansible | PLAY RECAP *****
2025-01-16 14:29:15,234 p=18742 u=ansible | db-primary : ok=24 changed=3 unreachable=0 failed=0

--- Host Connectivity (ansible ping) ---
web-prod-01 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "changed": false, "ping": "pong"}
web-prod-02 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "changed": false, "ping": "pong"}
db-primary | SUCCESS => {"ping": "pong"}
db-replica | UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: ssh: connect to host db-replica (10.42.8.15) port 22: Connection timed out", "unreachable": true}
cache-01 | SUCCESS => {"ping": "pong"}

--- Playbooks in $PLAYBOOK_DIR (/etc/ansible/playbooks) ---
/etc/ansible/playbooks/deploy-app.yml
/etc/ansible/playbooks/maintenance/backup.yaml
/etc/ansible/playbooks/maintenance/patch-os.yml
/etc/ansible/playbooks/site.yml

--- Installed Collections ---
Collection        Version
ansible.posix     1.5.4
community.general 7.2.1
community.postgresql 3.1.0

--- Installed Roles ---
geerlingguy.java 3.2.0
geerlingguy.postgresql 5.1.0

=== Triage complete ===

Triage output saved to: /tmp/ansible_triage_20250116_143245
```
---

## Change Pre-Check Script

Run before executing a production playbook. Performs syntax check, pings all target hosts, verifies required collections, checks vault password availability, and executes a dry-run.

```bash
#!/bin/bash
# ansible_pre_check.sh — Pre-change validation before running a production playbook
PLAYBOOK="${PLAYBOOK:?PLAYBOOK is required}"
INVENTORY="${INVENTORY_FILE:-/etc/ansible/hosts}"
VAULT_PASSWORD_FILE="${VAULT_PASSWORD_FILE:-}"
REQUIRED_COLLECTIONS=("ansible.builtin" "community.general")
FAIL=0

fail() { echo "[FAIL] $1"; FAIL=$((FAIL+1)); }
ok()   { echo "[OK]   $1"; }

echo "=== Ansible Change Pre-Check — $(date) ==="
echo "Playbook : $PLAYBOOK"
echo "Inventory: $INVENTORY"
echo ""

echo "--- Syntax Check ---"
ansible-playbook --syntax-check -i "$INVENTORY" "$PLAYBOOK" &>/dev/null \
  && ok "Syntax check passed" \
  || fail "Syntax check FAILED — fix errors before proceeding"

echo ""
echo "--- Host Connectivity ---"
RESULT=$(ansible all -i "$INVENTORY" -m ping --one-line 2>/dev/null || true)
UNREACHABLE=$(echo "$RESULT" | grep -c "UNREACHABLE" || true)
[[ $UNREACHABLE -gt 0 ]] \
  && fail "$UNREACHABLE host(s) unreachable — cannot proceed" \
  || ok "All hosts reachable"

echo ""
echo "--- Required Collections ---"
for col in "${REQUIRED_COLLECTIONS[@]}"; do
  ansible-galaxy collection list 2>/dev/null | grep -q "${col//.//}" \
    && ok "Collection installed: $col" \
    || fail "Collection missing: $col (run: ansible-galaxy collection install $col)"
done

echo ""
echo "--- Vault Password ---"
if grep -rq "!vault" "$PLAYBOOK" 2>/dev/null || grep -rq "ansible_vault" "$PLAYBOOK" 2>/dev/null; then
  if [[ -n "$VAULT_PASSWORD_FILE" && -f "$VAULT_PASSWORD_FILE" ]]; then
    ok "Vault password file found: $VAULT_PASSWORD_FILE"
  else
    fail "Playbook uses vault but VAULT_PASSWORD_FILE not set or file missing"
  fi
else
  ok "No vault usage detected in playbook"
fi

echo ""
echo "--- Dry-Run (--check mode) ---"
VAULT_OPT=""
[[ -n "$VAULT_PASSWORD_FILE" && -f "$VAULT_PASSWORD_FILE" ]] && VAULT_OPT="--vault-password-file $VAULT_PASSWORD_FILE"
ansible-playbook --check -i "$INVENTORY" $VAULT_OPT "$PLAYBOOK" \
  && ok "Dry-run completed without errors" \
  || fail "Dry-run reported errors — review before proceeding"

echo ""
echo "Pre-check complete: $FAIL failure(s)"
[[ $FAIL -gt 0 ]] && exit 2 || exit 0
```


```text title="Expected output"
=== Ansible Change Pre-Check — Wed Jan 15 14:32:47 UTC 2025 ===
Playbook : /opt/ansible/playbooks/deploy-webservers.yml
Inventory: /etc/ansible/hosts

--- Syntax Check ---
[OK]   Syntax check passed

--- Host Connectivity ---
[OK]   All hosts reachable

--- Required Collections ---
[OK]   Collection installed: ansible.builtin
[OK]   Collection installed: community.general

--- Vault Password ---
[OK]   No vault usage detected in playbook

--- Dry-Run (--check mode) ---
PLAY [Deploy Web Servers] *****************************************************

TASK [Gather Facts] ***********************************************************
ok: [web-prod-01.internal]
ok: [web-prod-02.internal]
ok: [web-prod-03.internal]

TASK [Install nginx] **********************************************************
changed: [web-prod-01.internal]
changed: [web-prod-02.internal]
changed: [web-prod-03.internal]

PLAY RECAP ********************************************************************
web-prod-01.internal       : ok=2    changed=1    unreachable=0    failed=0
web-prod-02.internal       : ok=2    changed=1    unreachable=0    failed=0
web-prod-03.internal       : ok=2    changed=1    unreachable=0    failed=0

[OK]   Dry-run completed without errors

Pre-check complete: 0 failure(s)
```

!!! warning "Common errors"
    **`ERROR! the playbook: /opt/ansible/playbooks/deploy-webservers.yml could not be found`** — Verify the PLAYBOOK variable is set to an absolute path and the file exists.
    **`fatal: [web-prod-02.internal]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Connection refused"}`** — Ensure SSH is running on the target host, firewall rules allow port 22, and the ansible user has valid credentials configured.
    **`[FAIL] Collection missing: community.general (run: ansible-galaxy collection install community.general)`** — Run `ansible-galaxy collection install community.general` on the control node before executing the playbook.
---

## Post-Change Validation Script

Run after a playbook completes to verify key outcomes using Ansible modules against target hosts.

```bash
#!/bin/bash
# ansible_post_validate.sh — Post-change validation using Ansible ad-hoc commands
INVENTORY="${INVENTORY_FILE:-/etc/ansible/hosts}"
FAIL=0
PASS=0

result() {
  local status="$1" label="$2"
  if [[ "$status" == "0" ]]; then
    echo "[PASS] $label"; PASS=$((PASS+1))
  else
    echo "[FAIL] $label"; FAIL=$((FAIL+1))
  fi
}

echo "=== Ansible Post-Change Validation — $(date) ==="
echo ""

echo "--- File Exists: /etc/ansible/ansible.cfg ---"
ansible all -i "$INVENTORY" -m stat \
  -a "path=/etc/ansible/ansible.cfg" --one-line 2>/dev/null \
  | grep -q '"exists": true' \
  && result 0 "Config file /etc/ansible/ansible.cfg exists on all hosts" \
  || result 1 "Config file /etc/ansible/ansible.cfg missing on one or more hosts"

echo ""
echo "--- Service Running: sshd ---"
ansible all -i "$INVENTORY" -m service \
  -a "name=sshd state=started" --check --one-line 2>/dev/null \
  | grep -qv "FAILED" \
  && result 0 "sshd running on all hosts" \
  || result 1 "sshd not running on one or more hosts"

echo ""
echo "--- Python3 Available ---"
ansible all -i "$INVENTORY" -m command \
  -a "python3 --version" --one-line 2>/dev/null \
  | grep -qv "FAILED" \
  && result 0 "python3 available on all hosts" \
  || result 1 "python3 missing on one or more hosts"

echo ""
echo "--- No Failed Systemd Services ---"
FAILED_SVCS=$(ansible all -i "$INVENTORY" -m command \
  -a "systemctl list-units --state=failed --no-legend --no-pager" \
  --one-line 2>/dev/null | grep -v "^$" | grep -v "SUCCESS" | grep -c "." || true)
result "$([[ $FAILED_SVCS -eq 0 ]] && echo 0 || echo 1)" \
  "No failed systemd units ($FAILED_SVCS host(s) reported failures)"

echo ""
echo "Post-change validation: $PASS PASS  |  $FAIL FAIL"
[[ $FAIL -gt 0 ]] && exit 2 || exit 0
```


```text title="Expected output"
=== Ansible Post-Change Validation — Wed Jan 15 14:32:18 UTC 2025 ===

--- File Exists: /etc/ansible/ansible.cfg ---
web-01.prod | SUCCESS => {"stat": {"exists": true, "isdir": false, "size": 2847}}
web-02.prod | SUCCESS => {"stat": {"exists": true, "isdir": false, "size": 2847}}
db-01.prod | SUCCESS => {"stat": {"exists": true, "isdir": false, "size": 2847}}
[PASS] Config file /etc/ansible/ansible.cfg exists on all hosts

--- Service Running: sshd ---
web-01.prod | SUCCESS => {"changed": false, "status": {"ActiveState": "active"}}
web-02.prod | SUCCESS => {"changed": false, "status": {"ActiveState": "active"}}
db-01.prod | SUCCESS => {"changed": false, "status": {"ActiveState": "active"}}
[PASS] sshd running on all hosts

--- Python3 Available ---
web-01.prod | SUCCESS | rc=0 >> Python 3.9.18
web-02.prod | SUCCESS | rc=0 >> Python 3.9.18
db-01.prod | SUCCESS | rc=0 >> Python 3.9.18
[PASS] python3 available on all hosts

--- No Failed Systemd Services ---
web-01.prod | SUCCESS | rc=0 >>
web-02.prod | SUCCESS | rc=0 >>
db-01.prod | SUCCESS | rc=0 >>
[PASS] No failed systemd units (0 host(s) reported failures)

Post-change validation: 4 PASS  |  0 FAIL
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory: '/etc/ansible/hosts'`** — Set the INVENTORY_FILE environment variable or verify the inventory path exists with `ls -la /etc/ansible/hosts`.
    **`fatal: [web-01.prod]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH keys are properly configured and the ansible_user has passwordless SSH access to all inventory hosts.
    **`ERROR! Unexpected Exception: No inventory was parsed`** — Verify the inventory file format is valid YAML/INI and contains at least one host or group definition.
---

## Health Check Script

Lightweight cron-safe health check reporting Ansible version, host reachability counts, installed collection count, and log error count in the last 24 hours.

```bash
#!/bin/bash
# ansible_health_check.sh — Cron-safe Ansible health check
# Exit codes: 0=healthy  1=warning  2=critical
INVENTORY="${INVENTORY_FILE:-/etc/ansible/hosts}"
ANSIBLE_LOG="${ANSIBLE_LOG_PATH:-/var/log/ansible.log}"
STATUS=0

stamp() { date '+%Y-%m-%d %H:%M:%S'; }

echo "=== Ansible Health Check — $(stamp) ==="

VERSION=$(ansible --version 2>/dev/null | head -1 || echo "UNAVAILABLE")
echo "Ansible version : $VERSION"
[[ "$VERSION" == "UNAVAILABLE" ]] && STATUS=2

RESULT=$(ansible all -i "$INVENTORY" -m ping --one-line 2>/dev/null || true)
REACHABLE=$(echo "$RESULT"  | grep -c "SUCCESS"     || true)
UNREACHABLE=$(echo "$RESULT" | grep -c "UNREACHABLE" || true)
echo "Hosts reachable : $REACHABLE  |  unreachable: $UNREACHABLE"
[[ $UNREACHABLE -gt 0 && $STATUS -lt 2 ]] && STATUS=2

COL_COUNT=$(ansible-galaxy collection list 2>/dev/null | grep -c "/" || true)
echo "Collections installed: $COL_COUNT"

if [[ -f "$ANSIBLE_LOG" ]]; then
  CUTOFF=$(date -d '24 hours ago' '+%Y-%m-%d %H:%M:%S' 2>/dev/null \
    || date -v-24H '+%Y-%m-%d %H:%M:%S' 2>/dev/null || echo "")
  if [[ -n "$CUTOFF" ]]; then
    ERR_COUNT=$(awk -v cutoff="$CUTOFF" '$0 >= cutoff' "$ANSIBLE_LOG" 2>/dev/null \
      | grep -c "FAILED!" || true)
  else
    ERR_COUNT=$(tail -200 "$ANSIBLE_LOG" | grep -c "FAILED!" || true)
  fi
  echo "Log errors (24h): $ERR_COUNT"
  [[ $ERR_COUNT -gt 0 && $STATUS -lt 1 ]] && STATUS=1
else
  echo "Log file       : not found ($ANSIBLE_LOG)"
fi

echo ""
case $STATUS in
  0) echo "Status: HEALTHY" ;;
  1) echo "Status: WARNING" ;;
  2) echo "Status: CRITICAL" ;;
esac
exit $STATUS
```


```text title="Expected output"
=== Ansible Health Check — 2024-01-15 14:32:47 ===
Ansible version : ansible 2.10.7
Hosts reachable : 12  |  unreachable: 0
Collections installed: 8
Log errors (24h): 2
Status: WARNING
```

!!! warning "Common errors"
    **`ansible: command not found`** — Install Ansible via `pip install ansible` or your system package manager.
    **`[Errno 2] No such file or directory: '/etc/ansible/hosts'`** — Set the `INVENTORY_FILE` environment variable or create the default inventory file at `/etc/ansible/hosts`.
    **`awk: fatal: cannot open file /var/log/ansible.log for reading (No such file or directory)`** — Create the log directory with `mkdir -p /var/log && touch /var/log/ansible.log` or set `ANSIBLE_LOG_PATH` to an existing file.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ansible — Procedures](../procedures/)
- [Ansible — CLI Reference](../cli-reference/)
- [Ansible — Health Checks](../health-checks/)
