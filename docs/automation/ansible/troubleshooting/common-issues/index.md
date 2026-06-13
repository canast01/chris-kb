---
tags:
  - ansible
  - troubleshooting
search:
  boost: 1.5
---
# Ansible — Common Issues


<div class="kb-summary">
Part of the [Ansible Troubleshooting](../index.md) reference.

*Applies to: Ansible 2.14+*
</div>

---

## Diagnostic Flow

```mermaid
graph TD
    S([What is the symptom?]) --> B1{SSH connection\nrefused?}
    S --> B2{Module or\ncollection not found?}
    S --> B3{Privilege\nescalation failed?}
    S --> B4{Variable\nundefined?}
    S --> B5{Playbook not\nidempotent?}
    B1 -->|Yes| D1{sshd running\non target?}
    D1 -->|No| R1[SSH Connection Issues\n— start sshd / open port 22]
    D1 -->|Yes| R2[Inventory and Vault Issues\n— check ansible_host / firewall]
    B2 -->|Yes| D2{Collection in\nrequirements.yml?}
    D2 -->|No| R3[Common Module Errors\n— ansible-galaxy collection install]
    D2 -->|Yes| R4[Common Module Errors\n— rebuild EE image for AWX]
    B3 -->|Yes| D3{NOPASSWD in\nsudoers?}
    D3 -->|No| R5[SSH and Become Issues\n— add NOPASSWD or --ask-become-pass]
    D3 -->|Yes| R6[Fact Gathering Issues\n— verify become_user]
    B4 -->|Yes| R7[Common Module Errors\n— use -vvv and register debug]
    B5 -->|Yes| R8[Common Module Errors\n— ansible-playbook --check --diff]
    classDef section fill:#1e3a5f,color:#fff,stroke:#1e3a5f
    classDef decision fill:#15803d,color:#fff,stroke:#15803d
    classDef start fill:#7c3aed,color:#fff,stroke:#7c3aed
    class R1,R2,R3,R4,R5,R6,R7,R8 section
    class B1,B2,B3,B4,B5,D1,D2,D3 decision
    class S start
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

```mermaid
flowchart TD
    failure["Playbook Failure\nor Unexpected Result"]
    failure --> checkSSH["Can you SSH manually\nto the target host?"]
    checkSSH -->|No| fixSSH["Fix SSH: key, user,\nport, firewall"]
    checkSSH -->|Yes| checkBecome["Does become/sudo\nwork on target?"]
    checkBecome -->|No| fixSudo["Add NOPASSWD to sudoers\nor use --ask-become-pass"]
    checkBecome -->|Yes| addVerbose["Re-run with -vvv\nfor connection details"]
    addVerbose --> checkInventory["Is the host listed\nin the inventory?"]
    checkInventory -->|No| fixInventory["Add host to inventory\nor fix dynamic source"]
    checkInventory -->|Yes| checkVault["Are Vault secrets\ndecryptable?"]
    checkVault -->|No| fixVault["Provide correct vault\npassword / file"]
    checkVault -->|Yes| checkModule["Is the required\ncollection installed?"]
    checkModule -->|No| installCol["ansible-galaxy collection install\n<namespace.collection>"]
    checkModule -->|Yes| resolved["Examine task output\n& register debug"]
```
```text
┌─────────────────────────────────────── Ansible — Common Issues ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Most frequent Ansible failures: SSH, Python errors, Vault decrypt, module not found      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    Issue: UNREACHABLE — SSH connection refused or timed out                   │   │
│   │               Cause A: SSH service stopped on target → fix: start sshd on target              │   │
│   │           Cause B: firewall blocking port 22 → fix: open port 22 in host/network FW           │   │
│   │         Cause C: wrong ansible_host or ansible_port → fix: correct inventory variable         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Issue: Vault decryption failed                                │   │
│   │           Cause A: wrong password → fix: verify vault password; check vault_id label          │   │
│   │         Cause B: wrong vault_id → fix: pass --vault-id prod@prompt if using vault IDs         │   │
│   │      Cause C: AWX vault credential missing → fix: re-add vault credential to job template     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Issue: module not found / collection missing                         │   │
│   │    Fix: ansible-galaxy collection install <namespace.collection> or add to requirements.yml   │   │
│   │               Fix: rebuild EE image with collection included if running via AWX               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
