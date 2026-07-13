---
tags:
  - ansible
  - troubleshooting
search:
  boost: 1.5
description: "Ansible troubleshooting: unreachable hosts, privilege escalation failures, variable precedence conflicts, vault decryption errors, and module..."
---
# Ansible — Common Issues

<div class="kb-summary">
Ansible troubleshooting: unreachable hosts, privilege escalation failures, variable precedence conflicts, vault decryption errors, and module compatibility issues.

*Applies to: Ansible 2.14+*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
ansible_troubleshooting_decision_flo: "Ansible Troubleshooting Decision Flow" {shape: rectangle}
common_module_errors: "Common Module Errors" {shape: rectangle}
fact_gathering_issues: "Fact Gathering Issues" {shape: rectangle}
verify_resolution: "Verify resolution" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> ansible_troubleshooting_decision_flo: investigate
symptom -> common_module_errors: investigate
symptom -> fact_gathering_issues: investigate
symptom -> verify_resolution: investigate
diagnostic_flow -> resolution
ansible_troubleshooting_decision_flo -> resolution
common_module_errors -> resolution
fact_gathering_issues -> resolution
verify_resolution -> resolution
```

## Diagnostic Flow

```d2
direction: right

D1: "D1" {shape: rectangle}
R1: "SSH Connection Issues\n— start sshd / open port 22" {shape: rectangle}
R2: "Inventory and Vault Issues\n— check ansible_host / firewall" {shape: rectangle}
D2: "D2" {shape: rectangle}
R3: "Common Module Errors\n— ansible-galaxy collection install" {shape: rectangle}
R4: "Common Module Errors\n— rebuild EE image for AWX" {shape: rectangle}
D3: "D3" {shape: rectangle}
R5: "SSH and Become Issues\n— add NOPASSWD or --ask-become-pass" {shape: rectangle}
R6: "Fact Gathering Issues\n— verify become_user" {shape: rectangle}
B4: "B4" {shape: rectangle}
R7: "Common Module Errors\n— use -vvv and register debug" {shape: rectangle}
B5: "B5" {shape: rectangle}
R8: "Common Module Errors\n— ansible-playbook --check --diff" {shape: rectangle}
S: "What is the symptom?" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "B2" {shape: rectangle}
B3: "B3" {shape: rectangle}

D1 -> R1
D1 -> R2
D2 -> R3
D2 -> R4
D3 -> R5
D3 -> R6
B4 -> R7
B5 -> R8
```

---

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Ansible Troubleshooting Decision Flow

```d2
direction: right

failure: "Playbook Failure\nor Unexpected Result" {shape: rectangle}
checkSSH: "Can you SSH manually\nto the target host?" {shape: rectangle}
fixSSH: "Fix SSH: key, user,\nport, firewall" {shape: rectangle}
checkBecome: "Does become/sudo\nwork on target?" {shape: rectangle}
fixSudo: "Add NOPASSWD to sudoers\nor use --ask-become-pass" {shape: rectangle}
addVerbose: "Re-run with -vvv\nfor connection details" {shape: rectangle}
checkInventory: "Is the host listed\nin the inventory?" {shape: rectangle}
fixInventory: "Add host to inventory\nor fix dynamic source" {shape: rectangle}
checkVault: "Are Vault secrets\ndecryptable?" {shape: rectangle}
fixVault: "Provide correct vault\npassword / file" {shape: rectangle}
checkModule: "Is the required\ncollection installed?" {shape: rectangle}
installCol: "ansible-galaxy collection install\n<namespace.collection>" {shape: rectangle}

failure -> checkSSH
checkSSH -> fixSSH
checkSSH -> checkBecome
checkBecome -> fixSudo
checkBecome -> addVerbose
addVerbose -> checkInventory
checkInventory -> fixInventory
checkInventory -> checkVault
checkVault -> fixVault
checkVault -> checkModule
checkModule -> installCol
```

## Common Module Errors

```bash
# Module not found / collection missing
ansible-galaxy collection install community.general

# Verify collection is installed
ansible-galaxy collection list

# "Temporary failure in name resolution" during package install
# Usually a DNS issue on the managed host — test with:
ansible webservers -m shell -a "nslookup archive.ubuntu.com"

# "changed=0" but task should have changed — check idempotency logic
ansible-playbook site.yml --check --diff

# Register output to inspect what a command returns
- name: Check service status
  ansible.builtin.command: systemctl is-active nginx
  register: svc_result
  ignore_errors: true

- name: Show result
  ansible.builtin.debug:
    var: svc_result
```


```text title="Expected output"
Starting galaxy collection install process
Process install dependency map
Starting collection download of 'community.general:5.8.1' from https://galaxy.ansible.com/download/community-general-5.8.1.tar.gz
Downloading community.general from https://galaxy.ansible.com/download/community-general-5.8.1.tar.gz (8.92 MB)
Installing 'community.general:5.8.1' to '/home/ansible/.ansible/collections/ansible_collections/community/general'
community.general:5.8.1 was installed successfully

# Collection list output
Collection                    Version
----------------------------- -------
community.general            5.8.1
ansible.posix                1.4.0
community.aws                4.2.1

# DNS test output
Server:		10.0.2.3
Address:	10.0.2.3#53

Name:	archive.ubuntu.com
Address: 91.189.89.198

# Playbook check mode output
PLAY [all] *********************************************************************
TASK [Install nginx] ************************************************************
ok: [webserver01] => {
    "changed": false,
    "msg": "Condition already satisfied"
}

PLAY RECAP **********************************************************************
webserver01                : ok=1 changed=0 unreachable=0 failed=0

# Debug output for registered variable
TASK [Show result] **************************************************************
ok: [webserver01] => {
    "svc_result": {
        "changed": false,
        "cmd": "systemctl is-active nginx",
        "rc": 0,
        "stderr": "",
        "stdout": "active"
    }
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! couldn't resolve module/action 'community.general.xxx'. This often means this role or collection does not support this ansible_version` | Run `ansible-galaxy collection install community.general --upgrade` to ensure the latest compatible version is installed. |
    | `fatal: [webserver01]: FAILED! => {"msg": "Temporary failure in name resolution"}` | Verify DNS resolution on the managed host with `ansible webservers -m shell -a "cat /etc/resolv.conf"` and ensure nameservers are correctly configured. |
    | `fatal: [webserver01]: FAILED! => {"msg": "Unable to start action, could not load plugin"}` | Verify the collection is installed in the correct location with `ansible-galaxy collection list | grep community.general` and reinstall if missing. |
## Fact Gathering Issues

```bash
# Manually gather facts for a host
ansible -i inventory/ web01 -m setup

# Filter facts
ansible -i inventory/ web01 -m setup -a "filter=ansible_distribution*"

# Disable fact gathering to speed up playbooks that don't need them
- hosts: webservers
  gather_facts: false
```


```text title="Expected output"
web01 | SUCCESS => {
    "ansible_facts": {
        "ansible_all_ipv4_addresses": [
            "192.168.1.45",
            "10.0.0.12"
        ],
        "ansible_architecture": "x86_64",
        "ansible_bios_version": "1.2.3",
        "ansible_date_time": {
            "iso8601": "2024-01-15T14:32:18Z",
            "year": "2024"
        },
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_release": "22.04",
        "ansible_distribution_version": "22.04",
        "ansible_fqdn": "web01.internal.corp",
        "ansible_hostname": "web01",
        "ansible_kernel": "5.15.0-91-generic",
        "ansible_memtotal_mb": 8192,
        "ansible_processor_vcpus": 4,
        "ansible_selinux": {
            "status": "disabled"
        }
    },
    "changed": false
}

web01 | SUCCESS => {
    "ansible_facts": {
        "ansible_distribution": "Ubuntu",
        "ansible_distribution_release": "22.04",
        "ansible_distribution_version": "22.04"
    },
    "changed": false
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}` | Verify SSH key permissions (chmod 600 on private key) and that the key is added to the remote host's authorized_keys. |
    | `[WARNING]: Unable to parse /etc/ansible/inventory as an inventory source` | Check that the inventory/ directory exists and contains valid inventory files (hosts, hosts.yml, or hosts.yaml). |
    | `fatal: [web01]: FAILED! => {"msg": "The following modules failed to load: ansible.builtin.setup"}` | Ensure Python is installed on the target host and the ansible_python_interpreter variable is correctly configured if using a non-standard Python path. |
---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Ansible — Diagnostics](../diagnostics/)
- [Ansible — Escalation](../escalation/)
- [Ansible — Health Checks](../../operations/health-checks/)
