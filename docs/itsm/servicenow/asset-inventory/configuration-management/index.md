---
tags:
  - servicenow
---
# Inventory — Configuration Management (CMDB)

```bash
# Run playbook against all servers to enforce baseline
ansible-playbook -i inventory/ site.yml --check   # dry-run first
ansible-playbook -i inventory/ site.yml

# Run against specific host group
ansible-playbook -i inventory/ site.yml --limit webservers

# Check for drift (report only, no changes)
ansible-playbook -i inventory/ baseline-check.yml --check --diff

# Show facts (current config state)
ansible -i inventory/ all -m setup -a "filter=ansible_distribution*"
```


```text title="Expected output"
PLAY [Enforce baseline configuration] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [web-prod-01.internal]
ok: [web-prod-02.internal]
ok: [db-prod-01.internal]
ok: [app-prod-03.internal]

TASK [Install required packages] ***********************************************
changed: [web-prod-01.internal]
changed: [web-prod-02.internal]
ok: [db-prod-01.internal]
ok: [app-prod-03.internal]

TASK [Configure firewall rules] ************************************************
changed: [web-prod-01.internal]
ok: [web-prod-02.internal]
ok: [db-prod-01.internal]
ok: [app-prod-03.internal]

PLAY RECAP *********************************************************************
web-prod-01.internal       : ok=12  changed=2    unreachable=0    failed=0
web-prod-02.internal       : ok=12  changed=1    unreachable=0    failed=0
db-prod-01.internal        : ok=12  changed=0    unreachable=0    failed=0
app-prod-03.internal       : ok=12  changed=0    unreachable=0    failed=0

PLAY [Check baseline compliance] ***********************************************
TASK [Verify SSH configuration] ************************************************
--- before
+++ after
@@ -15,3 +15,3 @@
 PermitRootLogin no
-PasswordAuthentication yes
+PasswordAuthentication no
 PubkeyAuthentication yes

PLAY RECAP *********************************************************************
All hosts passed baseline check with 1 drift detected on web-prod-01.internal
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /etc/ansible/inventory/ as an inventory source`** — Verify inventory file exists and is readable with `ls -la inventory/` and check file permissions.
    **`fatal: [web-prod-01.internal]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH key is loaded with `ssh-add ~/.ssh/id_rsa` and the target host has your public key in `~/.ssh/authorized_keys`.
    **`ERROR! the playbook: site.yml could not be found`** — Confirm playbook exists in current directory with `ls -la *.yml` and verify the working directory matches your documentation path.
```bash
# Detect package changes from baseline (RPM systems)
rpm -Va | grep -v "^......G"   # filter cosmetic warnings
# Common output: S5.. = size/hash changed; M = mode changed

# Detect changed config files
rpm -Va --nomtime /etc/ | awk '$1 ~ /[5cS]/ {print $2}'

# Track file changes with AIDE (Advanced Intrusion Detection Environment)
aide --init    # initialise baseline
aide --check   # compare against baseline
```
```powershell
# Compare installed features vs baseline
Get-WindowsFeature | Where-Object { $_.Installed -eq $true } | Select-Object Name | Sort-Object Name > current-features.txt
# diff against saved baseline

# Check for policy deviations
secedit /export /cfg current-policy.cfg
# diff against approved baseline policy

# DSC configuration check (pull server)
Test-DscConfiguration -Detailed
```
```bash
# ServiceNow CMDB update via REST API (example)
curl -s -X PATCH \
  -H "Authorization: Basic <base64-credentials>" \
  -H "Content-Type: application/json" \
  -d '{"os_version":"RHEL 9.3"}' \
  "https://<instance>.service-now.com/api/now/table/cmdb_ci_server/<sys_id>"
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
