---
tags:
  - ansible
  - troubleshooting
search:
  boost: 1.5
description: "Ansible diagnostic commands: progressively increase verbosity with -v to -vvvv, inspect variables with ansible.builtin.debug, test SSH connectivity, run..."
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


```text title="Expected output"
playbook: site.yml

[webservers]
web01.prod.internal
web02.prod.internal
web03.prod.internal

[databases]
db01.prod.internal
db02.prod.internal

all:
  children:
    databases:
      hosts:
        db01.prod.internal:
          ansible_host: 10.42.8.15
          ansible_user: ansible
        db02.prod.internal:
          ansible_host: 10.42.8.16
          ansible_user: ansible
    webservers:
      hosts:
        web01.prod.internal:
          ansible_host: 10.42.8.10
          ansible_user: ansible
        web02.prod.internal:
          ansible_host: 10.42.8.11
          ansible_user: ansible
        web03.prod.internal:
          ansible_host: 10.42.8.12
          ansible_user: ansible
...

ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = [u'/home/ansible/.ansible/plugins/modules', u'/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3.8/site-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Nov 14 2022, 12:59:47) [GCC 9.4.0]

web01.prod.internal | SUCCESS => {
    "hostvars['web01']": {
        "ansible_host": "10.42.8.10",
        "ansible_user": "ansible",
        "environment": "production",
        "app_port": 8080
    }
}
```

!!! warning "Common errors"
    **`ERROR! Syntax Error while loading YAML.`** — Review the file at the line number provided in the error message for indentation, quotes, or bracket mismatches.
    **`[WARNING]: Unable to parse /etc/ansible/inventory/ as an inventory source`** — Verify the inventory path exists and is readable, or specify individual inventory files with `-i inventory/hosts.ini`.
    **`fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure the SSH key specified in ansible.cfg or `-e ansible_private_key_file=` is deployed to the target host's authorized_keys.
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


```text title="Expected output"
web01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
OK
OpenSSH_8.2p1 Ubuntu 4ubuntu0.7, OpenSSL 1.1.1f  31 Mar 2020
debug1: Reading configuration data /home/ansible/.ssh/config
debug1: Offering public key: /home/ansible/.ssh/ansible_ed25519 ED25519
debug1: Server accepts key: perm denied (publickey).
debug1: Authentications that can continue: publickey
Connection established.
web01 | SUCCESS | rc=0 >>
/usr/bin/python3
Python 3.9.13
web01 | SUCCESS | rc=0 >>
uid=0(root) gid=0(root) groups=0(root)
Connection to web01.example.com 22 port [tcp/ssh] succeeded!
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Verify the private key path matches the public key on the target and check file permissions with `ls -la ~/.ssh/ansible_ed25519` (should be 600).
    **`web01: name or service not known`** — Add the target hostname and IP to `/etc/hosts` or ensure DNS resolution is working with `nslookup web01.example.com`.
    **`ansible@web01: Permission denied`** — Confirm the ansible user exists on the target with `id ansible` and that the SSH key is in `/home/ansible/.ssh/authorized_keys`.
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


```text title="Expected output"
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-01.prod.local]
ok: [web-02.prod.local]
ok: [db-01.prod.local]

TASK [Install nginx] ***********************************************************
changed: [web-01.prod.local] => {"changed": true, "cmd": "apt-get install -y nginx", "rc": 0, "stderr": "", "stdout": "Reading package lists... Done\nBuilding dependency tree...\nSetting up nginx (1.18.0-6ubuntu14.3) ..."}
changed: [web-02.prod.local] => {"changed": true, "cmd": "apt-get install -y nginx", "rc": 0, "stderr": "", "stdout": "Reading package lists... Done\nBuilding dependency tree...\nSetting up nginx (1.18.0-6ubuntu14.3) ..."}
ok: [db-01.prod.local]

TASK [Start nginx service] *****************************************************
changed: [web-01.prod.local] => {"changed": true, "name": "nginx", "state": "started", "status": {...}}
changed: [web-02.prod.local] => {"changed": true, "name": "nginx", "state": "started", "status": {...}}

PLAY RECAP *********************************************************************
web-01.prod.local          : ok=3    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
web-02.prod.local          : ok=3    changed=2    unreachable=0    failed=0    skipped=0    ignored=0
db-01.prod.local           : ok=1    changed=0    unreachable=0    failed=0    skipped=0    ignored=0
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory: b'inventory/'`** — Verify the inventory directory path exists and contains valid inventory files (hosts, hosts.yml, or similar).
    **`fatal: [web-01.prod.local]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH keys are properly configured in `~/.ssh/` and the remote user has passwordless sudo access, or add `-u <username> -k` flags.
    **`ERROR! the playbook: site.yml could not be found`** — Confirm site.yml exists in the current working directory or provide the full path to the playbook file.
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


```text title="Expected output"
web01 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.1.42",
            "10.0.0.15"
        ],
        "ansible_architecture": "x86_64",
        "ansible_bios_version": "2.12.0",
        "ansible_date_time": {
            "iso8601": "2024-01-15T14:32:18Z",
            "year": "2024"
        },
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_version": "22.04",
        "ansible_fqdn": "web01.internal.corp",
        "ansible_hostname": "web01",
        "ansible_kernel": "5.15.0-89-generic",
        "ansible_memtotal_mb": 16384,
        "ansible_processor_vcpus": 8,
        "ansible_selinux": {
            "status": "disabled"
        }
    },
    "changed": false,
    "gathered_facts": true
}

web01 | SUCCESS => {
    "ansible_facts": {
        "ansible_network_interfaces": ["eth0", "eth1", "lo"],
        "ansible_default_ipv4": {
            "address": "192.168.1.42",
            "interface": "eth0"
        }
    },
    "changed": false
}

web01 | SUCCESS => {
    "ansible_facts": {
        "ansible_os_family": "Debian"
    },
    "changed": false
}

Playbook run took 0.45s
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /etc/ansible/hosts as an inventory source`** — Verify the inventory path with `-i inventory/` matches your directory structure and contains valid YAML or INI syntax.
    **`fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH key is loaded (`ssh-add ~/.ssh/id_rsa`) and the remote user has passwordless sudo configured or use `-u username -k` flags.
    **`ERROR! The inventory directory /tmp/ansible_facts/ does not exist`** — Create the cache directory first with `mkdir -p /tmp/ansible_facts/` before running playbooks with fact caching enabled.
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


```text title="Expected output"
PLAY [Deploy application stack] ************************************************************

TASK [Gathering Facts] ******************************************************************
ok: [web01]
ok: [web02]
ok: [db01]

TASK [Install required packages] ********************************************************
changed: [web01]
changed: [web02]
skipped: [db01]

TASK [Update application config] ********************************************************
--- before: /etc/app/config.yml
+++ after: /etc/app/config.yml
@@ -12,7 +12,7 @@
 log_level: info
-max_connections: 50
+max_connections: 100
 timeout: 30

changed: [web01]
changed: [web02]

TASK [Restart application service] ******************************************************
changed: [web01]
changed: [web02]
skipped: [db01]

PLAY RECAP ******************************************************************************
web01                      : ok=4    changed=3    unreachable=0    failed=0    skipped=0
web02                      : ok=4    changed=3    unreachable=0    failed=0    skipped=0
db01                       : ok=2    changed=0    unreachable=0    failed=0    skipped=2
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /etc/ansible/inventory/ as an inventory source`** — Verify the inventory path exists and contains valid YAML/INI files with proper syntax.
    **`fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH keys are configured correctly and the ansible_user has passwordless access to target hosts.
    **`ERROR! the playbook: site.yml could not be found`** — Confirm the playbook filename and path are correct relative to your current working directory.
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


```text title="Expected output"
TASK [Install required packages] ****
ok: [web-server-01] => {"changed": false}
TASK [Configure nginx] ****
ok: [web-server-01] => {"changed": true}
TASK [Restart nginx service] ****
ok: [web-server-01] => {"changed": true}

FAILED task: Deploy application | db-server-02
  msg: fatal: [db-server-02]: FAILED! => {"msg": "Timeout waiting for database connection"}
FAILED task: Validate schema | db-server-02
  msg: Connection refused on port 5432

1234 | Deploy-Production-v2.3 | 2024-01-15T14:32:18.123456Z
1233 | Backup-Daily-Routine | 2024-01-15T13:45:02.987654Z
1232 | Network-Config-Update | 2024-01-15T12:18:55.654321Z
1231 | Security-Patch-Apply | 2024-01-15T11:05:30.321098Z
1230 | Inventory-Sync | 2024-01-15T10:22:14.098765Z

awx-task-5d8c9f2b-7k4m2 awx-task [2024-01-15 14:32:18,456] awx.main.tasks INFO Task 1234 started
awx-task-5d8c9f2b-7k4m2 awx-task [2024-01-15 14:32:45,123] awx.main.tasks INFO Task 1234 completed successfully
awx-task-5d8c9f2b-7k4m2 awx-task [2024-01-15 14:33:02,789] awx.main.tasks INFO Task 1235 started
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or configure proper SSL certificates on the AWX server.
    **`{"detail":"Invalid token","status":401}`** — Verify the AWX_TOKEN is correct and has not expired by regenerating it in the AWX UI.
    **`error: the server doesn't have a resource type "logs"`** — Ensure kubectl is connected to the correct cluster and the awx namespace exists with `kubectl get ns awx`.
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


```text title="Expected output"
ANSIBLE_DEBUG=1 ansible-playbook site.yml -i inventory/ -l web01 -vvvv 2>&1 | tee ansible-debug-20240115-143022.txt
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  python version = 3.8.10 (default, Nov 14 2023, 12:59:47) [GCC 9.4.0]

<snip — verbose task execution output — 200+ lines>

TASK [web : Configure nginx] ****
task path: /opt/ansible/roles/web/tasks/main.yml:42
<HOST> EXEC /bin/sh -c 'echo ~ansible && sleep 0'
<HOST> EXEC /bin/sh -c 'echo ~ansible'
changed: [web01] => {
    "changed": true,
    "cmd": "systemctl restart nginx",
    "rc": 0,
    "stderr": "",
    "stdout": ""
}

PLAY RECAP *****
web01                      : ok=18   changed=3    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0

ansible --version
ansible 2.9.27
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  python version = 3.8.10 (default, Nov 14 2023, 12:59:47) [GCC 9.4.0]

ansible-config dump --only-changed
DEFAULT_HOST_LIST(/etc/ansible/ansible.cfg) = ['/opt/ansible/inventory/']
DEFAULT_ROLES_PATH(/etc/ansible/ansible.cfg) = ['/opt/ansible/roles']
DEFAULT_LOG_PATH(/etc/ansible/ansible.cfg) = /var/log/ansible.log
INJECT_FACTS_AS_VARS(/etc/ansible/ansible.cfg) = False
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory: 'inventory/'`** — Verify the inventory path is correct and relative to your working directory, or use an absolute path like `/opt/ansible/inventory/`.
    **`fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure the SSH key specified in `ansible_ssh_private_key_file` is readable and the public key is authorized on the target host.
    **`ERROR! the playbook: site.yml could not be found`** — Confirm `site.yml` exists in the current directory and check for typos in the filename.
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


```text title="Expected output"
FAILED - host1.prod.internal: TASK [Install security patches] => {"changed": false, "msg": "Package manager lock held by another process"}
UNREACHABLE - host2.staging.internal: Failed to connect via SSH (port 22)
ERROR - Timeout waiting for response from host3.prod.internal after 30s
FAILED - host1.prod.internal: TASK [Configure firewall rules] => {"rc": 1, "stderr": "Permission denied"}
FAILED - host4.dev.internal: TASK [Deploy application] => {"failed": true, "msg": "Insufficient disk space"}
UNREACHABLE - host2.staging.internal: Failed to connect via SSH (port 22)

      3 FAILED [host1.prod.internal]
      2 FAILED [host4.dev.internal]
      1 FAILED [host3.prod.internal]
      2 UNREACHABLE [host2.staging.internal]
```

!!! warning "Common errors"
    **`grep: /var/log/ansible/ansible.log: No such file or directory`** — Ensure the log_path directive is uncommented in ansible.cfg and the /var/log/ansible/ directory exists with write permissions.
    **`Permission denied`** — Run the grep command with sudo or verify that the current user has read access to /var/log/ansible/ansible.log.
    **`command not found: uniq`** — Install the coreutils package (apt-get install coreutils on Debian/Ubuntu or yum install coreutils on RHEL/CentOS).
---

## See also

- [Ansible — Common Issues](../common-issues/)
- [Ansible — Escalation](../escalation/)

## Verify resolution

- `ansible <host> -m ping` returns `pong` for all previously unreachable hosts
- Re-run the failing playbook with `--check --diff` — confirm the tasks that were failing now show expected changes or no-change
- `GET /api/v2/jobs/?status=failed&page_size=5` shows no new failures after the fix
- The workflow or schedule that was failing completes successfully with exit code 0
