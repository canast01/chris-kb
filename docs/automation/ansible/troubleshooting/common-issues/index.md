# Ansible — Common Issues

> Part of the [Ansible Troubleshooting](../) reference.

---

## Verbose Mode and Debug

Increasing verbosity is the first step when a playbook behaves unexpectedly.

```bash
# One level: task results
ansible-playbook site.yml -v

# Two levels: input/output data
ansible-playbook site.yml -vv

# Three levels: connection details
ansible-playbook site.yml -vvv

# Four levels: everything including SSH negotiation
ansible-playbook site.yml -vvvv

# Debug a specific task inline
- name: Show variable value
  ansible.builtin.debug:
    var: my_variable

- name: Show formatted message
  ansible.builtin.debug:
    msg: "Host is {{ inventory_hostname }}, OS is {{ ansible_os_family }}"
```

## Unreachable Hosts

```bash
# Test SSH connectivity directly
ssh -i ~/.ssh/id_rsa -p 22 user@host

# Test with Ansible ping module
ansible -i inventory/ all -m ping

# Check SSH config used by Ansible
ansible -i inventory/ web01 -m setup -a "filter=ansible_default_ipv4" -vvv

# Common fixes
# Wrong user — set in inventory or ansible.cfg
ansible_user=ubuntu

# Wrong SSH key
ansible_ssh_private_key_file=~/.ssh/deploy_key

# Host key checking causing failures
export ANSIBLE_HOST_KEY_CHECKING=False
# or in ansible.cfg:
# [defaults]
# host_key_checking = False
```

## Sudo and Privilege Escalation Failures

| Error | Likely cause | Fix |
|---|---|---|
| `sudo: a password is required` | No NOPASSWD in sudoers | Add `NOPASSWD` or use `--ask-become-pass` |
| `incorrect sudo password` | Wrong become password | Run with `-K` flag |
| `sudo: command not found` | sudo not installed | Install sudo or use `become_method: su` |
| `Failed to set permissions on the temporary files` | sudoers restricts `SETENV` | Add `SETENV` to sudoers entry |

```bash
# Prompt for become password interactively
ansible-playbook site.yml --ask-become-pass

# Specify become method
- name: Run as root
  become: true
  become_method: sudo
  become_user: root
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
