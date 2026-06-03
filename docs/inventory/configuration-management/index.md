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

```text
┌───────────────────────────── Inventory — Configuration Management (CMDB) ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       CMDB: central record of CIs (hardware, software, services) and their relationships      │   │
│   │      CI relationships: server hosts VM → VM runs app → app depends on DB; impact analysis     │   │
│   │       Change linkage: every change ticket updates affected CI state; audit trail in CMDB      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                CI Attributes                 │  │               CI Relationships              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │              Name, class, owner              │  │              Hosts / hosted on              │   │
│   │           Status (active/retired)            │  │             Depends on / used by            │   │
│   │            Location, environment             │  │            Connects to / cluster            │   │
│   │             OS, software version             │  │             Impact analysis path            │   │
│   │            Change/incident links             │  │             Business service map            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CI           = Configuration Item; any entity tracked in CMDB with attributes and history          │
│    CI class     = Type of CI (Server, VM, Application, Network Device, Database, etc.)                │
│    Relationship = Typed link between CIs; powers impact analysis and dependency maps                  │
│    Impact analysis= Determine what is affected by a CI failure or change using relationships          │
│    Discovery    = Automated CMDB population from network scanning or cloud APIs                       │
│    Reconciliation= Compare discovered data vs CMDB; find stale or missing records                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
