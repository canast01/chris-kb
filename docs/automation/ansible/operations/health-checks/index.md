---
tags:
  - ansible
  - operations
description: "Health Checks reference covering Inventory Health, Connectivity, Vault and Secrets, AWX / Automation Platform."
---
# Ansible — Health Checks

<div class="kb-summary">
Health Checks reference covering Inventory Health, Connectivity, Vault and Secrets, AWX / Automation Platform.

*Applies to: Ansible 2.14+*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
connectivity: "Connectivity" {shape: rectangle}
vault_and_secrets: "Vault and Secrets" {shape: rectangle}
awx_automation_platform: "AWX / Automation Platform" {shape: rectangle}
ansible_health_check_flow: "Ansible Health Check Flow" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> connectivity
connectivity -> vault_and_secrets
vault_and_secrets -> awx_automation_platform
awx_automation_platform -> ansible_health_check_flow
ansible_health_check_flow -> verify
verify -> generate_report
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```bash
# 1. Ansible version
ansible --version

# 2. Inventory check — verify host count
ansible-inventory --list -i <inventory> | python3 -m json.tool | grep -c "hosts"

# 3. Connectivity test — should return empty (no failures)
ansible all -i <inventory> -m ping --one-line | grep -v "SUCCESS"

# 4. Vault status — test decrypt
ansible-vault view <encrypted-file> --vault-password-file <vault-pass>

# 5. Role syntax check
ansible-playbook --syntax-check <playbook.yml>

# 6. AWX/AAP job queue — review recent failures (if using Tower/AAP)
awx jobs list --status failed --count 20

# 7. Facts gather test
ansible <host> -m setup -a 'filter=ansible_distribution' -i <inventory>

# 8. Collection versions
ansible-galaxy collection list
```


```text title="Expected output"
ansible 2.10.17
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules']
  python version = 3.9.13
2
host1.prod.local | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
host2.prod.local | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
db-primary.internal | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
Vault password:
---
- hosts: all
  roles:
    - common
    - monitoring
  tasks:
    - name: Health check
      debug: msg="OK"

Play name: Health check | Syntax OK
id     name                                    status    created              elapsed
==     ====                                    ======    =======              =======
1247   Deploy webservers - prod-us-east-1      failed    2024-01-15T09:22Z    00:04:32
1246   Backup validation - daily-sync           failed    2024-01-15T08:15Z    00:02:18
1245   Config audit - compliance-check          failed    2024-01-15T07:30Z    00:01:45
host1.prod.local | SUCCESS => {
    "ansible_facts": {
        "ansible_distribution": "Ubuntu"
    }
}
# Collection        Version
ansible.posix      1.5.4
ansible.windows    1.14.0
community.general  7.2.1
community.mysql    3.8.0
```

!!! warning "Common errors"
    **`ansible-inventory: error: unrecognized arguments: -i <inventory>`** — Replace `<inventory>` with actual inventory path (e.g., `-i /etc/ansible/hosts` or `-i inventory/production/`).
    **`ERROR! Decryption failed`** — Verify vault password file exists and contains correct password, or use `--ask-vault-pass` instead of `--vault-password-file`.
    **`ERROR! the playbook: <playbook.yml> could not be found`** — Confirm playbook path is correct and file exists in current working directory or use absolute path.
**Count hosts per group**

```bash
ansible-inventory --list -i <inventory> | python3 -m json.tool | grep -c "hosts"
```


```text title="Expected output"
3
```

!!! warning "Common errors"
    **`ansible-inventory: command not found`** — Install ansible with `pip install ansible` or `apt install ansible`.
    **`No such file or directory`** — Verify the inventory file path exists and use the correct `-i` flag syntax (e.g., `-i ./hosts` or `-i /etc/ansible/hosts`).
**Validate inventory syntax**

```bash
ansible-inventory --list -i <inventory> --yaml
```


```text title="Expected output"
all:
  children:
    ungrouped: {}
    webservers:
      hosts:
        web01.prod.internal:
          ansible_host: 192.168.1.42
          ansible_user: deploy
          ansible_port: 22
        web02.prod.internal:
          ansible_host: 192.168.1.43
          ansible_user: deploy
          ansible_port: 22
    databases:
      hosts:
        db01.prod.internal:
          ansible_host: 192.168.2.10
          ansible_user: dbadmin
          ansible_port: 3306
    monitoring:
      hosts:
        monitor01.prod.internal:
          ansible_host: 192.168.3.5
          ansible_user: monitor
          ansible_port: 22
  vars:
    ansible_become: true
    ansible_become_method: sudo
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse <inventory> as an inventory source`** — Verify the inventory file path is correct and the file exists in the current directory or use an absolute path.
    **`[ERROR]: Unable to parse <inventory> as YAML`** — Check that the inventory file is valid YAML with proper indentation and syntax using `yamllint <inventory>`.
    **`[WARNING]: No inventory was parsed`** — Ensure the inventory file contains at least one host or group definition; an empty file will produce this warning.
**Check for unreachable hosts in a dry run**

```bash
ansible all -i <inventory> -m ping --one-line 2>&1 | grep -E "UNREACHABLE|FAILED"
```


```text title="Expected output"
web-prod-01 | SUCCESS => {"ansible_facts": {"discovered_interpreter_python": "/usr/bin/python3"}, "ping": "pong"}
db-backup-02 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 10.42.18.55 port 22: Connection timed out",
    "unreachable": true
}
cache-node-03 | FAILED! => {
    "msg": "Aborting, target uses selinux without python selinux bindings installed",
    "failed": true
}
lb-secondary-04 | SUCCESS => {"ping": "pong"}
```

!!! warning "Common errors"
    **`Failed to connect to the host via ssh: ssh: connect to host 10.42.18.55 port 22: Connection timed out`** — Verify the target host is online, SSH port 22 is open, and network connectivity exists from the Ansible control node.
    **`Aborting, target uses selinux without python selinux bindings installed`** — Install the `python3-selinux` package on the target host or disable SELinux enforcement temporarily.
    **`Permission denied (publickey,password)`** — Ensure the SSH key specified in the inventory or ansible.cfg is correct and the target host has the public key in `~/.ssh/authorized_keys`.
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Host count per group | Matches expected | Investigate additions or removals |
| No parse errors | Clean `--list` output | Fix syntax in inventory file |
| Dynamic inventory plugin | Returns current data | Check plugin credentials and API connectivity |
| Group variable files | Present and readable | Fix permissions or missing files |

---

## Connectivity

SSH connectivity must be confirmed before any playbook run. Unreachable hosts cause partial execution and can leave managed systems in an inconsistent state.

**Ping all hosts**

```bash
ansible all -i <inventory> -m ping
```


```text title="Expected output"
node-web-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
node-web-02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
node-db-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
node-cache-01 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 10.42.8.15 port 22: Connection timed out",
    "unreachable": true
}
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse <inventory> as an inventory source`** — Verify the inventory file path is correct and readable with `cat <inventory>`.
    **`fatal: [node-web-01]: UNREACHABLE! => ... Connection refused`** — Ensure SSH is running on the target host and the control node has network connectivity and correct SSH keys configured.
    **`[ERROR]: Inventory parsing failed: expected key=value pairs`** — Check that the inventory file uses valid INI or YAML syntax with proper host definitions.
**Ping a specific group**

```bash
ansible <group> -i <inventory> -m ping
```


```text title="Expected output"
web-server-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
web-server-02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
db-server-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
cache-server-01 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 10.2.14.87 port 22: Connection timed out",
    "unreachable": true
}
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse <inventory> as an inventory source`** — Verify the inventory file path is correct and readable with `cat <inventory>`.
    **`fatal: [<hostname>]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh"}`** — Confirm SSH connectivity to the host with `ssh -vvv <hostname>` and verify the host is online and port 22 is open.
    **`[ERROR]: Syntax Error while loading YAML from <inventory>`** — Check the inventory file for YAML formatting errors using `ansible-inventory -i <inventory> --list`.
**Test with verbose output to see SSH details**

```bash
ansible all -i <inventory> -m ping -vvv 2>&1 | grep -E "SSH|ESTABLISH|FAILED"
```


```text title="Expected output"
<192.168.1.10> ESTABLISH SSH connection for user=ansible
<192.168.1.11> ESTABLISH SSH connection for user=ansible
<192.168.1.12> ESTABLISH SSH connection for user=ansible
<192.168.1.15> FAILED! => {
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 192.168.1.15 port 22: Connection refused"
}
<192.168.1.20> ESTABLISH SSH connection for user=ansible
<192.168.1.21> ESTABLISH SSH connection for user=ansible
```

!!! warning "Common errors"
    **`Failed to connect to the host via ssh: ssh: connect to host <IP> port 22: Connection refused`** — Verify the target host is running and SSH daemon is listening on port 22, or check firewall rules blocking the connection.
    **`Permission denied (publickey,password)`** — Ensure the SSH key specified in ansible.cfg or -u flag exists and has correct permissions (600), and the public key is in the target's ~/.ssh/authorized_keys.
    **`[Errno -2] Name or service not known`** — Verify the hostname in your inventory file resolves correctly by running `getent hosts <hostname>` or use IP addresses instead.
**Check SSH key and user**

```bash
ansible all -i <inventory> -m command -a "whoami" --become
```


```text title="Expected output"
node1.prod | SUCCESS | rc=0 >>
root

node2.prod | SUCCESS | rc=0 >>
root

node3.staging | SUCCESS | rc=0 >>
root

db-primary.prod | SUCCESS | rc=0 >>
root

cache-01.prod | SUCCESS | rc=0 >>
root
```

!!! warning "Common errors"
    **`fatal: [node1.prod]: FAILED! => {"msg": "Missing sudo password, unable to continue. Disable 'require_tty' in sudoers or set the 'ANSIBLE_SUDO_FLAGS' environment variable (default -H -S -n -u %s)."}`** — Add `-k` flag to prompt for sudo password or configure passwordless sudo in sudoers with `NOPASSWD`.
    
    **`fatal: [node2.prod]: FAILED! => {"msg": "Unable to parse /etc/ansible/hosts as an inventory source"}`** — Verify the inventory file path is correct and readable with `cat <inventory>` before running the command.
**Verify Python interpreter on managed nodes**

```bash
ansible all -i <inventory> -m command -a "python3 --version"
```


```text title="Expected output"
node-web-01 | CHANGED | rc=0 >>
Python 3.11.7

node-web-02 | CHANGED | rc=0 >>
Python 3.10.12

node-db-01 | CHANGED | rc=0 >>
Python 3.9.18

node-cache-01 | CHANGED | rc=0 >>
Python 3.11.7

node-app-03 | FAILED | rc=127 >>
/bin/sh: 1: python3: not found
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory`** — Verify the inventory file path is correct and readable with `cat <inventory>`.
    **`fatal: [node-app-03]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh"}`** — Ensure SSH connectivity to all hosts with `ansible all -i <inventory> -m ping` and verify SSH keys/credentials are configured.
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Ping response | `pong` for all hosts | Check SSH keys, firewall, and host availability |
| SSH key authentication | No password prompts | Add or rotate SSH keys |
| Python interpreter | Python 3.x present | Install Python 3 on managed node |
| Become (sudo) | No privilege errors | Check sudoers configuration on target |

---

## Vault and Secrets

Ansible Vault encrypts sensitive variables. Confirm that vault-encrypted files can be decrypted and that vault passwords are accessible to the automation process.

**Test vault decryption**

```bash
ansible-vault view <encrypted-file> --vault-password-file <vault-pass>
```


```text title="Expected output"
---
# Ansible vault file contents
db_password: "p@ssw0rd_prod_2024"
api_key: "sk-proj-abc123def456ghi789jkl"
ssl_cert_path: "/etc/ssl/certs/prod.crt"
redis_host: "redis-prod-01.internal"
redis_port: 6379
backup_s3_bucket: "company-backups-prod"
slack_webhook_url: "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"
---
```

!!! warning "Common errors"
    **`Decryption failed`** — Verify the vault password file exists and contains the correct password used to encrypt the file.
    **`[Errno 2] No such file or directory: '<encrypted-file>'`** — Confirm the encrypted file path is correct and the file exists in the current directory or provide an absolute path.
    **`[Errno 13] Permission denied: '<vault-pass>'`** — Ensure the vault password file is readable by the current user with `chmod 600 <vault-pass>`.
**Verify vault-encrypted variable is readable in a playbook context**

```bash
ansible all -i <inventory> -m debug -a "var=<vault_variable>" --vault-password-file <vault-pass>
```


```text title="Expected output"
prod-web-01 | SUCCESS => {
    "vault_variable": "db_password_prod_2024"
}
prod-web-02 | SUCCESS => {
    "vault_variable": "db_password_prod_2024"
}
prod-db-01 | SUCCESS => {
    "vault_variable": "db_password_prod_2024"
}
staging-web-01 | SUCCESS => {
    "vault_variable": "db_password_prod_2024"
}
staging-db-01 | SUCCESS => {
    "vault_variable": "db_password_prod_2024"
}

PLAY RECAP *********************************************************************
prod-web-01                : ok=1    changed=0    unreachable=0    failed=0
prod-web-02                : ok=1    changed=0    unreachable=0    failed=0
prod-db-01                 : ok=1    changed=0    unreachable=0    failed=0
staging-web-01             : ok=1    changed=0    unreachable=0    failed=0
staging-db-01              : ok=1    changed=0    unreachable=0    failed=0
```

!!! warning "Common errors"
    **`ERROR! Decryption failed`** — Verify the vault password file is correct and matches the vault that encrypted the variable.
    **`fatal: [prod-web-01]: FAILED! => {"msg": "The variable <vault_variable> is undefined"}`** — Ensure the variable name is spelled correctly and exists in your group_vars or host_vars encrypted files.
    **`[Errno 2] No such file or directory: '<inventory>'`** — Provide the correct path to your inventory file (e.g., `inventory/production.ini` or `inventory/hosts.yml`).
**Re-key vault file (rotate vault password)**

```bash
ansible-vault rekey <encrypted-file> --vault-password-file <old-vault-pass> --new-vault-password-file <new-vault-pass>
```


```text title="Expected output"
Rekey successful
```

!!! warning "Common errors"
    **`Decryption failed`** — Verify the old vault password file is correct and the encrypted file hasn't been corrupted.
    **`[Errno 2] No such file or directory: '<old-vault-pass>'`** — Ensure the old vault password file path is absolute or relative to your current working directory, and the file exists.
    **`[Errno 13] Permission denied: '<new-vault-pass>'`** — Make sure the new vault password file is readable (chmod 600) and owned by the user running ansible-vault.
**List all vault-encrypted files in the project**

```bash
grep -rl '\$ANSIBLE_VAULT' . --include="*.yml" --include="*.yaml"
```


```text title="Expected output"
./roles/database/defaults/main.yml
./roles/security/vars/encrypted.yml
./roles/monitoring/group_vars/production.yml
./roles/networking/host_vars/router-01.yml
./playbooks/deploy-prod.yml
./inventories/staging/group_vars/webservers.yml
```

!!! warning "Common errors"
    **`grep: (standard input): No such file or directory`** — Ensure the command is run from the Ansible project root directory where YAML files exist.
    **`grep: ./roles: No such file or directory`** — Verify the directory structure exists; if running in a different location, provide the correct path to the Ansible project.
**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Vault decrypt | No errors | Check vault password file path and permissions |
| Vault password file | Readable by automation user | Fix file permissions (`chmod 600`) |
| Encrypted variables in playbook | Resolve correctly at runtime | Confirm `--vault-password-file` path or `ANSIBLE_VAULT_PASSWORD_FILE` env var |
| Vault password rotation | Completed on schedule | Re-key all encrypted files after rotation |

---

## AWX / Automation Platform

AWX (open source) and Red Hat Ansible Automation Platform (AAP) provide a centralised job scheduler, RBAC, and credential store. Health checks here focus on service availability and job queue status.

**List recent failed jobs**

```bash
awx jobs list --status failed --count 20
```


```text title="Expected output"
id     name                                    organization  status   created              modified
====   ====                                    ============  ======   =======              ========
1847   Deploy-WebServers-Prod                  Engineering   failed   2024-01-15 14:32:18  2024-01-15 14:35:22
1843   Database-Backup-Daily                   Operations    failed   2024-01-15 13:45:00  2024-01-15 13:47:15
1841   Network-Config-Sync                     Infrastructure failed   2024-01-15 12:20:33  2024-01-15 12:22:51
1839   SSL-Certificate-Renewal                 Security      failed   2024-01-15 11:15:44  2024-01-15 11:18:09
1837   Patch-Management-Weekly                 Operations    failed   2024-01-14 22:00:05  2024-01-14 22:03:42
1835   DNS-Update-Batch                        Infrastructure failed   2024-01-14 20:15:22  2024-01-14 20:17:38
1833   Container-Registry-Cleanup              DevOps        failed   2024-01-14 18:45:11  2024-01-14 18:47:29
1831   Firewall-Rule-Deploy                    Security      failed   2024-01-14 16:30:00  2024-01-14 16:32:44

(Showing 8 of 20 failed jobs)
```

!!! warning "Common errors"
    **`Error: The provided token is invalid or expired`** — Re-authenticate with `awx login` using valid credentials.
    **`Error: No such option: --status`** — Verify AWX CLI version supports the `--status` flag; update with `pip install --upgrade awx-cli`.
    **`Error: Connection refused to http://localhost:8052`** — Ensure AWX controller is running and accessible; check `awx config host` points to correct URL.
**List running jobs**

```bash
awx jobs list --status running
```


```text title="Expected output"
id     name                                    organization  status    created              modified
====   ====                                    ============  ======    =======              ========
1247   Deploy-WebServers-Prod                  Engineering   running   2024-01-15 09:23:14  2024-01-15 09:45:22
1248   Database-Backup-Daily                   Operations    running   2024-01-15 09:30:05  2024-01-15 09:31:18
1249   Network-Config-Sync                     Infrastructure running   2024-01-15 09:42:33  2024-01-15 09:43:01
1250   Security-Patch-Staging                  Security      running   2024-01-15 09:44:12  2024-01-15 09:44:55
```

!!! warning "Common errors"
    **`Error: The server could not be reached`** — Verify AWX/Tower is running and accessible, then check your AWX_HOST and AWX_VERIFY_SSL environment variables.
    **`Error: Invalid OAuth2 token`** — Re-authenticate using `awx login` with valid credentials for your AWX instance.
    **`Error: You do not have permission to perform this action`** — Ensure your AWX user account has the "System Auditor" or "Admin" role to view job status.
**Check AWX service pods (Kubernetes deployment)**

```bash
kubectl get pods -n awx
```


```text title="Expected output"
NAME                                               READY   STATUS    RESTARTS   AGE
awx-operator-controller-manager-7d4f8c9b5-kxm2j   1/1     Running   0          45d
awx-postgres-13-0                                  1/1     Running   2          45d
awx-redis-0                                        1/1     Running   1          45d
awx-web-deployment-5f8b9c2a-lmn9p                 1/1     Running   3          44d
awx-task-deployment-6g7h2d3e-pqr4s                1/1     Running   2          44d
awx-ee-default-execution-environment-pull-xyzab   0/1     ImagePullBackOff   0          2m
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "pods" on API group ""`** — Verify the Kubernetes cluster is accessible with `kubectl cluster-info` and check your kubeconfig context.
    **`Error from server (Forbidden): pods is forbidden: User "system:serviceaccount:default:default" cannot list resource "pods" in API group "" in the namespace "awx"`** — Ensure your service account has RBAC permissions by applying the appropriate ClusterRole and ClusterRoleBinding for pod listing.
All pods should show `Running` status. Pods in `CrashLoopBackOff` or `Error` state require immediate investigation.

**Check AWX capacity (forks headroom)**

```bash
awx instances list
```


```text title="Expected output"
id     hostname                    instance_group  cpu_explanation                          enabled  capacity  version
1      awx-controller-01.prod      default         8 vCPU, 16 GB RAM                        true     40        21.12.0
2      awx-controller-02.prod      default         8 vCPU, 16 GB RAM                        true     40        21.12.0
3      awx-execution-01.prod       execution       16 vCPU, 32 GB RAM                       true     100       21.12.0
4      awx-execution-02.prod       execution       16 vCPU, 32 GB RAM                       true     100       21.12.0
5      awx-hybrid-01.prod          hybrid          4 vCPU, 8 GB RAM                         false    20        21.12.0

(Showing 5 of 5 instances)
```

!!! warning "Common errors"
    **`Error: The server could not be reached`** — Verify the AWX API endpoint is accessible and the AWX service is running with `systemctl status awx`.
    **`Error: Invalid credentials or authentication token`** — Ensure your AWX authentication token is valid by checking `awx config` and re-authenticating with `awx login`.
    **`Error: command not found: awx`** — Install the AWX CLI tool with `pip install awxkit` or verify it is in your PATH.
Review the `capacity` and `consumed_capacity` fields. High consumption indicates a need to scale the instance group.

**Review credential expiry**

In the AWX/AAP UI, navigate to **Resources → Credentials** and check for credentials with upcoming expiry dates (API tokens, SSH keys, cloud credentials).

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Failed job rate | <5% over 7 days | Investigate recurring failures |
| AWX pods | All `Running` | Restart failing pods; check logs |
| Instance capacity | <80% consumed | Scale instance group or reduce concurrent jobs |
| Credential expiry | >30 days remaining | Rotate and update credentials |
| Job queue depth | Low, clearing quickly | Add capacity if queue persists |

---

## Ansible Health Check Flow
> Part of the [Ansible Operations](../index.md) reference.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ansible — Procedures](../procedures/)
- [Ansible — CLI Reference](../cli-reference/)
- [Ansible — Common Issues](../../troubleshooting/common-issues/)
