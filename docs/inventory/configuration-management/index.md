# Configuration Management

Track, baseline, and enforce system configurations across infrastructure to prevent drift and maintain compliance.

## Configuration Baseline

A baseline defines the approved, known-good state for a system type. Any deviation is drift.

| System Type | Baseline Elements |
|---|---|
| Linux server | OS version, installed packages, kernel parameters (`sysctl`), SSH config, sudoers |
| Windows server | OS version, installed features, security policy, registry keys, local group policy |
| Network device | Firmware version, interface config, ACLs, NTP/syslog config |
| Kubernetes node | kubelet config, CRI version, kernel parameters, OS image version |

## Ansible — Configuration Enforcement

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

## Azure Policy — Resource Compliance

```bash
# List non-compliant resources
az policy state list \
  --filter "complianceState eq 'NonCompliant'" \
  --query '[*].{Resource:resourceId,Policy:policyDefinitionName}' -o table

# Trigger compliance re-scan
az policy state trigger-scan --subscription <sub-id>
```

## Drift Detection — Linux

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

## Drift Detection — Windows

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

## CMDB — Update After Changes

Every infrastructure change must be reflected in the CMDB:

| Change | CMDB Update Required |
|---|---|
| OS patching | Update OS version field |
| New package installed | Add to software inventory |
| IP address change | Update IP, DNS records |
| VM resize | Update CPU/RAM fields |
| New server added | Create new CI with all attributes |
| Decommission | Mark CI as retired; update relationships |

```bash
# ServiceNow CMDB update via REST API (example)
curl -s -X PATCH \
  -H "Authorization: Basic <base64-credentials>" \
  -H "Content-Type: application/json" \
  -d '{"os_version":"RHEL 9.3"}' \
  "https://<instance>.service-now.com/api/now/table/cmdb_ci_server/<sys_id>"
```

## Compliance Checklist

- [ ] All servers in scope have a defined baseline in Ansible / DSC
- [ ] Baseline enforcement playbook ran this week; no unresolved drift
- [ ] AWS Config rules showing < 5% non-compliant resources
- [ ] Azure Policy compliance > 95% at subscription scope
- [ ] CMDB CI records updated after all changes in last 30 days
- [ ] Unauthorized package or config changes investigated and resolved

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Ansible playbook shows many changed tasks | Drift since last run? Manual changes? | Review changed items; re-apply baseline; document approved exceptions |
| AWS Config rule non-compliant | Rule logic vs actual config | Review resource config; remediate or create exception |
| CMDB stale for many CIs | No automated discovery? | Enable AWS Config / Azure Resource Graph auto-discovery integration |
| DSC configuration failing | Module version mismatch? Pull server unreachable? | Check DSC log: `Get-DscConfigurationStatus -All` |
