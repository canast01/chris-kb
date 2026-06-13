---
tags:
  - ansible
  - deployment
search:
  boost: 1.5
---
# Ansible — Environment Setup

<div class="kb-summary">
Step-by-step guide to installing Ansible, configuring inventory and SSH authentication, testing connectivity, and running your first playbook.

*Applies to: Ansible 2.14+*
</div>

```text
┌───────────────────────────────────── Ansible — Environment Setup ─────────────────────────────────────┐
│                                                                                                       │
│   Agentless automation: controller pushes tasks over SSH (Linux) or WinRM (Windows)                   │
│   Control node: Linux/macOS with Python 3.8+; managed nodes need no additional agent                  │
│   Install: pip3 install ansible  OR  dnf install ansible  OR  apt install ansible                     │
│   Verify: ansible --version; check Python interpreter and core collection versions                    │
│                                                                                                       │
│   Inventory setup                                                                                     │
│   Create /etc/ansible/hosts or project-local inventory.ini / inventory.yml                            │
│   Group hosts: [webservers], [dbservers], [prod], [dev]; nest groups with :children                   │
│   Define variables: ansible_host, ansible_user, ansible_port, ansible_become=true                     │
│   Test: ansible all -m ping -i inventory.ini  (all hosts should return pong)                          │
│                                                                                                       │
│   SSH authentication                                                                                  │
│   Generate key: ssh-keygen -t ed25519 -C ansible-ctrl; push with ssh-copy-id                          │
│   Config: ansible_ssh_private_key_file in inventory or ssh_config Host block                          │
│   Disable password auth on managed nodes: PasswordAuthentication no in sshd_config                    │
│                                                                                                       │
│   First playbook                                                                                      │
│   Structure: hosts → vars → tasks; each task has name + module + arguments                            │
│   Dry run first: ansible-playbook site.yml -i inventory.ini --check --diff                            │
│   Run subsets: --tags deploy  /  --skip-tags debug  /  --limit webservers                             │
│                                                                                                       │
│   Physical infrastructure                                                                             │
│   Controller: any Linux VM or jump host; TCP 22 open to all managed nodes                             │
│   Windows targets require WinRM (5985 HTTP / 5986 HTTPS) and PS remoting enabled                      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   playbook     = YAML automation definition; lists hosts, vars, and tasks in order                    │
│   inventory    = host file (INI/YAML); groups, host vars, connection params                           │
│   module       = reusable Ansible task unit (package, file, service, template)                        │
│   role         = structured directory: tasks/, handlers/, templates/, vars/                           │
│   become       = sudo/runas privilege escalation; configured per task or play                         │
│   handler      = task triggered by notify; runs once at end of play regardless of count               │
│   vault        = ansible-vault encryption for secrets inside playbooks and var files                  │
│   idempotent   = same playbook applied twice leaves system in identical desired state                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install Ansible

Install Ansible using the package manager appropriate for your control node OS, or via Python pip for a version-flexible install.

```bash
# Python pip (any OS, latest Ansible)
pip3 install ansible

# RHEL / CentOS / Fedora
dnf install ansible

# Debian / Ubuntu
apt install ansible
```

Verify the installation:

```bash
ansible --version
```

Confirm the output shows the Ansible version, Python version, and the path to the active configuration file.

## Configure Inventory File

The inventory file tells Ansible which hosts to manage and how to group them. Use either the default system-wide location or a project-level file.

```bash
# System-wide inventory
/etc/ansible/hosts

# Project-level inventory (recommended)
inventory/hosts.yml
```

Example `inventory/hosts.yml`:

```yaml
all:
  children:
    webservers:
      hosts:
        web01.example.com:
        web02.example.com:
    dbservers:
      hosts:
        db01.example.com:
          ansible_user: dbadmin
```

Verify the inventory parses correctly:

```bash
ansible-inventory --list -i inventory/
```

## Configure SSH Key Authentication

Ansible connects to managed hosts over SSH. Key-based authentication is required — password authentication should not be used in production.

```bash
# Generate a dedicated key pair for Ansible
ssh-keygen -t ed25519 -C "ansible" -f ~/.ssh/id_ed25519

# Copy the public key to each managed host
ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@web01.example.com
ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@web02.example.com
ssh-copy-id -i ~/.ssh/id_ed25519.pub ansible@db01.example.com
```

Test connectivity after key distribution:

```bash
ansible all -m ping -i inventory/
```

All hosts should return `"pong"`.

## Configure ansible.cfg

Create an `ansible.cfg` in your project directory. Settings here override the system-wide defaults and are picked up automatically when you run Ansible from the project root.

```ini
[defaults]
inventory          = inventory/
remote_user        = ansible
private_key_file   = ~/.ssh/id_ed25519
host_key_checking  = False
retry_files_enabled = False
stdout_callback    = yaml

[privilege_escalation]
become       = True
become_method = sudo
become_user  = root
```

Confirm the active config file is picked up:

```bash
ansible --version | grep "config file"
```

## Test Connectivity

Run the built-in `ping` module against all hosts to confirm SSH access, Python availability, and inventory correctness:

```bash
ansible all -m ping -i inventory/
```

Expected output for each host:

```yaml
web01.example.com | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

If any host fails, check: SSH key distribution, firewall rules on port 22, `remote_user` in `ansible.cfg`, and that Python 3 is installed on the managed host.

## Install Required Collections and Roles

Ansible Galaxy hosts community collections and roles. Install what your playbooks need before first run.

```bash
# Install collections
ansible-galaxy collection install community.vmware vmware.vmware_rest community.general

# Install roles
ansible-galaxy role install geerlingguy.apache geerlingguy.mysql
```

Pin versions for reproducible environments using a `requirements.yml` file:

```yaml
collections:
  - name: community.vmware
    version: ">=4.0.0"
  - name: vmware.vmware_rest
    version: ">=3.0.0"

roles:
  - name: geerlingguy.apache
    version: "3.2.0"
```

Install from requirements file:

```bash
ansible-galaxy collection install -r requirements.yml
ansible-galaxy role install -r requirements.yml
```

Verify installed collections:

```bash
ansible-galaxy collection list
```

## Configure Ansible Vault for Secrets

Never store plaintext passwords or API keys in playbooks or inventory. Use Ansible Vault to encrypt sensitive values.

```bash
# Create an encrypted secrets file
ansible-vault create group_vars/all/vault.yml
```

Add secrets in the editor that opens:

```yaml
vault_db_password: "SuperSecretPassword123"
vault_api_key: "abc123xyz"
```

Reference vault variables in playbooks or other variable files:

```yaml
db_password: "{{ vault_db_password }}"
```

Run playbooks with vault decryption:

```bash
# Prompt for vault password at runtime
ansible-playbook -i inventory/ site.yml --ask-vault-pass

# Use a vault password file (store outside the repo)
ansible-playbook -i inventory/ site.yml --vault-password-file ~/.vault_pass
```

## Run First Playbook

Always run with `--check` (dry run) before applying changes to production.

```bash
# Dry run — shows what would change, makes no changes
ansible-playbook -i inventory/ site.yml --check

# Apply changes
ansible-playbook -i inventory/ site.yml

# Limit to a single host for initial testing
ansible-playbook -i inventory/ site.yml --limit web01.example.com

# Verbose output for troubleshooting
ansible-playbook -i inventory/ site.yml -v
```

Confirm the play recap shows `failed=0` and `unreachable=0` before considering the run successful.

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation
