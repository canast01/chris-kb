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
