---
tags:
  - ansible
  - troubleshooting
search:
  boost: 1.5
---
# Ansible — Diagnostics

<div class="kb-summary">
Ansible diagnostic commands: progressively increase verbosity with -v to -vvvv, inspect variables with ansible.builtin.debug, test SSH connectivity, run ad-hoc modules, clear stale fact cache, query AWX/AAP job failures via REST API, and diagnose common module errors.

*Applies to: Ansible 2.14+; AWX / Ansible Automation Platform 2.x*
</div>

```d2
direction: right

B: "B" {shape: rectangle}
C: "--syntax-check first\nThen ansible host -m ping -vvv" {shape: rectangle}
D: "Add debug var=varname task\nRun with -v to see task result" {shape: rectangle}
E: "ansible-playbook --list-hosts\nCheck inventory and -l limit" {shape: rectangle}
F: "ansible-inventory --list\nCheck group_vars and host_vars" {shape: rectangle}
G: "GET /api/v2/jobs/ID/stdout\nCheck event log for task result" {shape: rectangle}
H: "ANSIBLE_DEBUG=1 playbook\nProfile with callback_plugins" {shape: rectangle}
I: "I" {shape: rectangle}
J: "ssh -vvv to confirm key loaded\ndeploy public key if missing" {shape: rectangle}
K: "Test TCP 22 with nc -zv\nCheck firewall and sshd service" {shape: rectangle}
L: "ansible -m raw -a which python3\nInstall Python on target" {shape: rectangle}
M: "Check NOPASSWD sudoers\nVerify ansible_become_password" {shape: rectangle}
N: "ansible-playbook --check --diff\nSee what would change without applying" {shape: rectangle}
O: "Check -i inventory path and ansible.cfg\nVerify host/group name spelling" {shape: rectangle}
P: "ansible web01 -m setup -a filter=ansible_network*\nInspect all host facts" {shape: rectangle}
Q: "kubectl logs -n awx -l app.kubernetes.io/name=task\nCheck AWX task pod errors" {shape: rectangle}
R: "R" {shape: rectangle}
A: "Ansible Issue" {shape: rectangle}

B -> C
B -> D
B -> E
B -> F
B -> G
B -> H
I -> J
I -> K
I -> L
I -> M
D -> N
E -> O
F -> P
G -> Q
K -> R
L -> R
M -> R
N -> R
O -> R
P -> R
Q -> R
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_validate_playbook_and_invento: "Step 1 — Validate playbook and inventory" {shape: rectangle}
step_2_test_connectivity: "Step 2 — Test connectivity" {shape: rectangle}
step_3_increase_verbosity: "Step 3 — Increase verbosity" {shape: rectangle}
step_4_inspect_variables_and_facts: "Step 4 — Inspect variables and facts" {shape: rectangle}
step_5_dry_run_and_diff: "Step 5 — Dry run and diff" {shape: rectangle}
step_6_awx_aap_job_diagnostics: "Step 6 — AWX / AAP job diagnostics" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_validate_playbook_and_invento: investigate
symptom -> step_2_test_connectivity: investigate
symptom -> step_3_increase_verbosity: investigate
symptom -> step_4_inspect_variables_and_facts: investigate
symptom -> step_5_dry_run_and_diff: investigate
symptom -> step_6_awx_aap_job_diagnostics: investigate
step_1_validate_playbook_and_invento -> resolution
step_2_test_connectivity -> resolution
step_3_increase_verbosity -> resolution
step_4_inspect_variables_and_facts -> resolution
step_5_dry_run_and_diff -> resolution
step_6_awx_aap_job_diagnostics -> resolution
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node access; AWX admin credentials if using AWX/AAP
- **Gather first:** the exact error message (full FAILED output block, not just the summary), the affected host or group, the task name, and whether this worked previously
- **Scope:** confirm whether the issue affects one host, one task, one playbook, or all Ansible runs

---

## Step 1 — Validate playbook and inventory

```bash
# Check YAML syntax without executing
ansible-playbook site.yml --syntax-check
# Expected: no output (success); any output = syntax error with file and line number

# Confirm which hosts would be targeted
ansible-playbook site.yml -i inventory/ --list-hosts
# Shows: the exact host list Ansible would connect to; check for typos or wrong groups

# Show all inventory hosts and groups in YAML format
ansible-inventory -i inventory/ --list --yaml | head -100

# Confirm ansible.cfg is being read (shows active config)
ansible --version
# Shows: config file location, python version, and module search path

# Check a single host's variable values
ansible web01 -i inventory/ -m debug -a "var=hostvars['web01']"
```

---

## Step 2 — Test connectivity

```bash
# Ping module — tests SSH, Python, and Ansible module execution
ansible web01 -i inventory/ -m ping
# Expected: "pong"
# Problem: UNREACHABLE or FAILED → proceed to SSH debug

# Test raw SSH as ansible user (bypasses Ansible entirely)
ssh -i ~/.ssh/ansible_ed25519 -o BatchMode=yes ansible@web01.example.com "echo OK"

# Verbose SSH debug (look for key exchange and auth method)
ssh -vvv -i ~/.ssh/ansible_ed25519 ansible@web01.example.com

# Test Python on target (common issue on minimal installs)
ansible web01 -i inventory/ -m raw -a "which python3; python3 --version"

# Test sudo escalation works
ansible web01 -i inventory/ -m command -a "id" --become
# Expected: uid=0(root) or the become_user

# Test TCP 22 reachability
nc -zv web01.example.com 22
```

---

## Step 3 — Increase verbosity

Each level adds more detail:

```bash
# -v = task results (show returned values)
ansible-playbook site.yml -i inventory/ -v

# -vv = show task input parameters
ansible-playbook site.yml -i inventory/ -vv

# -vvv = show SSH connection negotiation (use for connection failures)
ansible-playbook site.yml -i inventory/ -vvv

# -vvvv = add Python module transfer trace (very verbose; for module loading issues)
ansible-playbook site.yml -i inventory/ -vvvv

# Maximum debug (Ansible internal debug messages)
ANSIBLE_DEBUG=1 ansible-playbook site.yml -i inventory/ 2>&1 | tee ansible-debug.txt

# Step through interactively (prompts before each task)
ansible-playbook site.yml -i inventory/ --step
```

---

## Step 4 — Inspect variables and facts

```yaml
# Add this task inside the play to print a specific variable
- name: Debug variable value
  ansible.builtin.debug:
    var: nginx_port

# Print multiple variables together
- name: Debug connection context
  ansible.builtin.debug:
    msg: |
      Host: {{ inventory_hostname }}
      IP: {{ ansible_host }}
      User: {{ ansible_user }}
      OS: {{ ansible_distribution }} {{ ansible_distribution_major_version }}
      Python: {{ ansible_python_interpreter }}

# Dump all variables for a host (very verbose)
- name: Dump all variables
  ansible.builtin.debug:
    var: hostvars[inventory_hostname]
```

```bash
# From command line — gather all OS facts for a host
ansible web01 -i inventory/ -m ansible.builtin.setup

# Filter facts by prefix
ansible web01 -i inventory/ -m ansible.builtin.setup -a "filter=ansible_network*"
ansible web01 -i inventory/ -m ansible.builtin.setup -a "filter=ansible_os_family"

# Clear stale fact cache if using caching
rm -rf /tmp/ansible_facts/
ansible-playbook site.yml --flush-cache
```

---

## Step 5 — Dry run and diff

```bash
# Dry run — show what tasks would change without applying
ansible-playbook site.yml -i inventory/ --check

# Diff mode — show content changes (for file, template, copy tasks)
ansible-playbook site.yml -i inventory/ --check --diff

# Limit to a subset of hosts for safe dry-run testing
ansible-playbook site.yml -i inventory/ --check --limit web01
```

---

## Step 6 — AWX / AAP job diagnostics

```bash
# Get job stdout from AWX via REST API
AWX_TOKEN="<your-awx-api-token>"
JOB_ID=1234

curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/jobs/$JOB_ID/stdout/?format=txt" | tail -100

# Get per-task event log (most detailed — shows every task result)
curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/jobs/$JOB_ID/job_events/?page_size=50" \
  | python3 -c "
import json,sys
for e in json.load(sys.stdin).get('results', []):
    if e.get('failed'):
        print('FAILED task:', e.get('task',''), '|', e.get('host_name',''))
        print('  msg:', str(e.get('event_data',{}).get('res',{}).get('msg',''))[:200])
"

# List recently failed AWX jobs
curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/jobs/?status=failed&page_size=10" \
  | python3 -c "
import json,sys
for j in json.load(sys.stdin).get('results', []):
    print(j.get('id'), '|', j.get('name',''), '|', j.get('finished',''))
"

# AWX pod logs (for AWX issues, not playbook failures)
kubectl logs -n awx -l app.kubernetes.io/name=task --tail=100
```

---

## Step 7 — Collect full debug output for escalation

```bash
# Capture everything — stdout, stderr, verbose output
ANSIBLE_DEBUG=1 ansible-playbook site.yml -i inventory/ \
  -l web01 -vvvv 2>&1 | tee ansible-debug-$(date +%Y%m%d-%H%M).txt

# Include ansible version and environment info
ansible --version >> ansible-debug-$(date +%Y%m%d-%H%M).txt

# Confirm what's in ansible.cfg (mask any passwords before sharing)
ansible-config dump --only-changed

# For AWX: export job events from the UI
# Job → Events tab → Export (downloads CSV of all task events)
```

---

## Common error patterns

| Error | Likely Cause | Fix |
|---|---|---|
| `UNREACHABLE! Connection refused` | SSH not running on target | Start sshd; check firewall rule for TCP 22 |
| `FAILED! Permission denied (publickey)` | SSH key not deployed | Deploy public key to `authorized_keys` |
| `MODULE FAILURE — python not found` | No Python on target | `ansible -m raw -a "dnf install -y python3"` |
| `[WARNING] No inventory was parsed` | Wrong inventory path | Check `-i` flag or `inventory` in ansible.cfg |
| `Timeout waiting for privilege escalation` | sudo requires password | Add `NOPASSWD` to sudoers for the ansible user |
| `Vault encrypted file, but no vault secret found` | Missing vault password | `--ask-vault-pass` or check `vault_password_file` |
| `msg: Invalid/incorrect password` | Wrong become password | Check `ansible_become_password` in host_vars |
| `conflicting action statements` | YAML parse error in task | Check task indentation and key names |

---

## Log locations

```bash
# Enable persistent Ansible logging (add to ansible.cfg)
# [defaults]
# log_path = /var/log/ansible/ansible.log

# Grep for all failures across the log
grep "FAILED\|UNREACHABLE\|ERROR" /var/log/ansible/ansible.log

# Count failures by host to find problematic targets
grep "FAILED" /var/log/ansible/ansible.log | \
  grep -oP 'FAILED \[.*?\]' | sort | uniq -c | sort -rn
```

---

## See also

- [Ansible — Common Issues](../common-issues/)
- [Ansible — Escalation](../escalation/)

## Verify resolution

- `ansible <host> -m ping` returns `pong` for all previously unreachable hosts
- Re-run the failing playbook with `--check --diff` — confirm the tasks that were failing now show expected changes or no-change
- `GET /api/v2/jobs/?status=failed&page_size=5` shows no new failures after the fix
- The workflow or schedule that was failing completes successfully with exit code 0
