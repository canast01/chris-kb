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

```d2
direction: right

plan: "Plan" {shape: oval}
install_ansible: "Install Ansible" {shape: rectangle}
configure_inventory_file: "Configure Inventory File" {shape: rectangle}
configure_ssh_key_authentication: "Configure SSH Key Authentication" {shape: rectangle}
configure_ansiblecfg: "Configure ansible.cfg" {shape: rectangle}
test_connectivity: "Test Connectivity" {shape: rectangle}
install_required_collections_and_rol: "Install Required Collections and Roles" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_ansible
install_ansible -> configure_inventory_file
configure_inventory_file -> configure_ssh_key_authentication
configure_ssh_key_authentication -> configure_ansiblecfg
configure_ansiblecfg -> test_connectivity
test_connectivity -> install_required_collections_and_rol
install_required_collections_and_rol -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Ansible 101 — Episode 1: Introduction to Ansible](https://www.youtube.com/watch?v=goclfp6a2IQ){ .md-button }
<!-- /video-link -->

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


```text title="Expected output"
Collecting ansible
  Downloading ansible-2.10.7-py3-none-any.whl (24.3 MB)
     |████████████████████████████████| 24.3 MB 2.3 MB/s
Collecting jinja2>=2.11
  Downloading Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting PyYAML>=5.3.1
  Downloading PyYAML-6.0-cp39-cp39-linux_x86_64.whl (615 kB)
Installing collected packages: MarkupSafe, jinja2, PyYAML, ansible
Successfully installed ansible-2.10.7 jinja2-3.1.2 PyYAML-6.0 MarkupSafe-2.1.1
```

!!! warning "Common errors"
    **`ERROR: Could not find a version that satisfies the requirement ansible`** — Ensure pip3 is up to date with `pip3 install --upgrade pip` and check your internet connection.
    **`error: externally-managed-environment × This environment is externally managed`** — Use `pip3 install --break-system-packages ansible` or create a Python virtual environment with `python3 -m venv ~/ansible-env && source ~/ansible-env/bin/activate`.
Verify the installation:

```bash
ansible --version
```


```text title="Expected output"
ansible 2.10.7
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  module cache = /root/.ansible/cache/ansible_plugins
  executable location = /usr/bin/ansible
  python version = 3.9.13 (default, Nov 14 2022, 09:47:41) [GCC 9.4.0]
```

!!! warning "Common errors"
    **`ansible: command not found`** — Install Ansible using `pip install ansible` or your system package manager.
    **`WARNING: Ansible is being run in a world writable /tmp directory`** — Run Ansible from a non-world-writable directory or set `ANSIBLE_LOCAL_TEMP` to a secure location.
Confirm the output shows the Ansible version, Python version, and the path to the active configuration file.

## Configure Inventory File

The inventory file tells Ansible which hosts to manage and how to group them. Use either the default system-wide location or a project-level file.

```bash
# System-wide inventory
/etc/ansible/hosts

# Project-level inventory (recommended)
inventory/hosts.yml
```


```text title="Expected output"
(no output — these are file path references only)
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /etc/ansible/hosts as an inventory source`** — Verify the file exists and is readable with `cat /etc/ansible/hosts` or `ls -l /etc/ansible/hosts`.
    **`[ERROR]: Unable to find inventory file at inventory/hosts.yml`** — Ensure you are running ansible from the project root directory and the file path is correct with `ls -la inventory/hosts.yml`.
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


```text title="Expected output"
{
  "_meta": {
    "hostvars": {
      "web-prod-01.example.com": {
        "ansible_host": "10.42.1.15",
        "ansible_user": "deploy",
        "environment": "production"
      },
      "web-prod-02.example.com": {
        "ansible_host": "10.42.1.16",
        "ansible_user": "deploy",
        "environment": "production"
      },
      "db-primary.example.com": {
        "ansible_host": "10.42.2.8",
        "ansible_user": "dbadmin",
        "environment": "production"
      }
    }
  },
  "all": {
    "children": [
      "ungrouped",
      "webservers",
      "databases"
    ]
  },
  "webservers": {
    "hosts": [
      "web-prod-01.example.com",
      "web-prod-02.example.com"
    ]
  },
  "databases": {
    "hosts": [
      "db-primary.example.com"
    ]
  }
}
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse inventory/hosts as an YAML source`** — Verify inventory file syntax with `ansible-inventory --list -i inventory/hosts --yaml` or check for YAML formatting errors.
    **`[ERROR]: Unable to find inventory file or directory`** — Ensure the `inventory/` directory exists and contains valid inventory files (hosts, *.yml, or *.yaml).
    **`[WARNING]: No inventory was parsed`** — Confirm at least one inventory file exists in the directory and is readable with `ls -la inventory/`.
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


```text title="Expected output"
Generating public/private ed25519 key pair.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/admin/.ssh/id_ed25519
Your public key has been saved in /home/admin/.ssh/id_ed25519.pub
The key fingerprint is:
SHA256:7kJ9mN2pQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWx ansible
The key's randomart image is:
+--[ED25519 256]--+
|    .o.          |
|   o .+          |
|  . o .+         |
+----[SHA256]-----+
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/admin/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to ssh to host "web01.example.com" with user "ansible"
/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed. -- if you trust this host, type "yes"
Permission denied (publickey,password).
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/admin/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to ssh to host "web02.example.com" with user "ansible"
Number of key(s) added: 1
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/admin/.ssh/id_ed25519.pub"
/usr/bin/ssh-copy-id: INFO: attempting to ssh to ssh to host "db01.example.com" with user "ansible"
Number of key(s) added: 1
```

!!! warning "Common errors"
    **`Permission denied (publickey,password).`** — Ensure the `ansible` user exists on the target host and password authentication is enabled, or pre-stage the public key manually in `~ansible/.ssh/authorized_keys`.
    **`ssh: Could not resolve hostname web01.example.com`** — Verify DNS resolution or replace hostnames with IP addresses in the ssh-copy-id commands.
Test connectivity after key distribution:

```bash
ansible all -m ping -i inventory/
```


```text title="Expected output"
prod-web-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
prod-web-02 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
prod-db-01 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
staging-app-01 | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: connect to host 10.2.14.87 port 22: Connection timed out",
    "unreachable": true
}
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /etc/ansible/hosts as an inventory source`** — Verify the inventory file path is correct and readable; use `-i inventory/hosts` if the file is named explicitly.
    **`fatal: [prod-web-01]: FAILED! => {"msg": "Missing sudo password"}`** — Add `--ask-become-pass` flag or configure passwordless sudo in your inventory file with `ansible_become_password`.
    **`[prod-db-01]: UNREACHABLE! => ... Connection timed out`** — Check network connectivity and SSH access to the host; verify firewall rules allow port 22 and the host is online.
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


```text title="Expected output"
config file = /etc/ansible/ansible.cfg
```

!!! warning "Common errors"
    **`ansible: command not found`** — Install Ansible using `pip install ansible` or your system package manager.
    **`config file = None`** — Create `/etc/ansible/ansible.cfg` or set the `ANSIBLE_CONFIG` environment variable to point to a valid config file.
## Test Connectivity

Run the built-in `ping` module against all hosts to confirm SSH access, Python availability, and inventory correctness:

```bash
ansible all -m ping -i inventory/
```


```text title="Expected output"
web01.prod.local | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
web02.prod.local | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
db01.prod.local | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
```

!!! warning "Common errors"
    **`[Errno 2] No such file or directory: 'inventory/'`** — Verify the inventory directory path exists and contains valid inventory files (hosts, hosts.yml, etc.).
    **`fatal: [web01.prod.local]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Ensure SSH public key is deployed to target hosts and the ansible_user/ansible_private_key_file is correctly configured in your inventory.
    **`[WARNING]: Unable to parse inventory/hosts as an inventory source`** — Check that inventory files are properly formatted YAML/INI and contain valid host definitions with required connection parameters.
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


```text title="Expected output"
Starting galaxy collection install process
Process install dependency map
Starting collection download of 'community.vmware:3.9.0' from https://galaxy.ansible.com
Downloading collection from https://galaxy.ansible.com/download/community-vmware-3.9.0.tar.gz
Installing 'community.vmware:3.9.0' to '/home/ansible/.ansible/collections/ansible_collections/community/vmware'
community.vmware:3.9.0 was installed successfully
Starting collection download of 'vmware.vmware_rest:2.3.1' from https://galaxy.ansible.com
Installing 'vmware.vmware_rest:2.3.1' to '/home/ansible/.ansible/collections/ansible_collections/vmware/vmware_rest'
vmware.vmware_rest:2.3.1 was installed successfully
Starting collection download of 'community.general:7.2.0' from https://galaxy.ansible.com
Installing 'community.general:7.2.0' to '/home/ansible/.ansible/collections/ansible_collections/community/general'
community.general:7.2.0 was installed successfully
- downloading role 'apache', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-apache/archive/3.4.0.tar.gz
- extracting geerlingguy.apache to /home/ansible/.ansible/roles/geerlingguy.apache
geerlingguy.apache (3.4.0) was installed successfully
- downloading role 'mysql', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-mysql/archive/4.2.1.tar.gz
- extracting geerlingguy.mysql to /home/ansible/.ansible/roles/geerlingguy.mysql
geerlingguy.mysql (4.2.1) was installed successfully
```

!!! warning "Common errors"
    **`ERROR! Failed to download the collection community.vmware from https://galaxy.ansible.com: HTTP Error 403: Forbidden`** — Verify your Ansible Galaxy API token is valid and has collection download permissions, or check if the collection name/version exists.
    **`ERROR! the specified role geerlingguy.apache was not found in /home/ansible/.ansible/roles:/usr/share/ansible/roles:/etc/ansible/roles`** — Ensure you have internet connectivity and the GitHub repository is accessible, or manually download the role tarball and extract it to your roles directory.
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


```text title="Expected output"
Starting galaxy collection install process
Process install dependency map
Starting collection download of 'community.general:5.8.0' from https://galaxy.ansible.com/download/community-general-5.8.0.tar.gz
Downloading community.general to /home/ansible/.ansible/collections/ansible_collections/community/general
community.general (5.8.0) was installed successfully
Starting collection download of 'ansible.posix:1.4.0' from https://galaxy.ansible.com/download/ansible-posix-1.4.0.tar.gz
Downloading ansible.posix to /home/ansible/.ansible/collections/ansible_collections/ansible/posix
ansible.posix (1.4.0) was installed successfully
Starting galaxy role install process
- downloading role 'nginx', owned by geerlingguy
- downloading role from https://github.com/geerlingguy/ansible-role-nginx/archive/3.9.0.tar.gz
- extracting geerlingguy.nginx to /home/ansible/.ansible/roles/geerlingguy.nginx
- geerlingguy.nginx (3.9.0) was installed successfully
```

!!! warning "Common errors"
    **`ERROR! the file requirements.yml does not exist`** — Verify the requirements.yml file exists in the current directory or provide the full path with `-r /path/to/requirements.yml`.
    **`ERROR! Failed to download the collection at 'community.general:5.8.0' from galaxy.ansible.com`** — Check your internet connectivity and ensure the collection version exists; try `ansible-galaxy collection list` to see what's already installed.
Verify installed collections:

```bash
ansible-galaxy collection list
```


```text title="Expected output"
# /home/ansible/.ansible/collections/ansible_collections
Collection                    Version
----------------------------- -------
amazon.aws                    5.2.0
ansible.netcommon             5.1.2
ansible.posix                 3.1.1
community.general             6.4.0
community.mysql               3.7.1
kubernetes.core               2.4.0
...
```

!!! warning "Common errors"
    **`[WARNING]: Unable to parse /home/ansible/.ansible/collections/ansible_collections as an installed collection`** — Ensure the collections directory exists and has proper read permissions with `chmod 755 ~/.ansible/collections/ansible_collections`.
    **`[ERROR]: Ansible collections not found in expected paths`** — Install collections using `ansible-galaxy collection install -r requirements.yml` or verify `ANSIBLE_COLLECTIONS_PATHS` environment variable is set correctly.
## Configure Ansible Vault for Secrets

Never store plaintext passwords or API keys in playbooks or inventory. Use Ansible Vault to encrypt sensitive values.

```bash
# Create an encrypted secrets file
ansible-vault create group_vars/all/vault.yml
```


```text title="Expected output"
New Vault password: 
Confirm Vault password: 
(no output — file created and opened in editor)
```

!!! warning "Common errors"
    **`ansible-vault: command not found`** — Install Ansible with `pip install ansible` or your system package manager.
    **`[Errno 2] No such file or directory: 'group_vars/all'`** — Create the directory structure first with `mkdir -p group_vars/all`.
    **`Error: editor not set`** — Set your default editor with `export EDITOR=vim` before running the command.
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


```text title="Expected output"
Vault password: 
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-01.prod.internal]
ok: [db-01.prod.internal]
ok: [cache-01.prod.internal]

TASK [Install base packages] ***************************************************
changed: [web-01.prod.internal]
changed: [db-01.prod.internal]
changed: [cache-01.prod.internal]

TASK [Configure application] ***************************************************
ok: [web-01.prod.internal]
ok: [db-01.prod.internal]
ok: [cache-01.prod.internal]

PLAY RECAP *********************************************************************
web-01.prod.internal       : ok=3    changed=1    unreachable=0    failed=0
db-01.prod.internal        : ok=3    changed=1    unreachable=0    failed=0
cache-01.prod.internal     : ok=3    changed=1    unreachable=0    failed=0
```

!!! warning "Common errors"
    **`ERROR! Decryption failed (no vault password supplied?)`** — Provide the correct vault password when prompted or ensure the vault password file exists and contains the correct password.
    **`ERROR! Unable to read the vault password file (~/.vault_pass): [Errno 2] No such file or directory`** — Create the vault password file at `~/.vault_pass` with appropriate permissions (`chmod 600`).
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


```text title="Expected output"
PLAY [Deploy application stack] ************************************************************

TASK [Gathering Facts] ******************************************************************
ok: [web01.example.com]
ok: [web02.example.com]
ok: [db01.example.com]

TASK [Install required packages] ********************************************************
changed: [web01.example.com]
changed: [web02.example.com]
ok: [db01.example.com]

TASK [Deploy application code] **********************************************************
changed: [web01.example.com]
changed: [web02.example.com]

TASK [Restart services] *****************************************************************
changed: [web01.example.com]
changed: [web02.example.com]
ok: [db01.example.com]

PLAY RECAP ******************************************************************************
web01.example.com          : ok=4    changed=3    unreachable=0    failed=0    skipped=0
web02.example.com          : ok=4    changed=3    unreachable=0    failed=0    skipped=0
db01.example.com           : ok=3    changed=0    unreachable=0    failed=0    skipped=1
```

!!! warning "Common errors"
    **`fatal: [web01.example.com]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}`** — Verify SSH key permissions (chmod 600) and that the key is added to ssh-agent or specified via ansible_ssh_private_key_file in inventory.
    **`ERROR! Unable to parse /path/to/inventory/ as an inventory source`** — Ensure the inventory directory contains valid YAML/INI files with proper syntax and that the path is relative to your playbook location.
    **`fatal: [web02.example.com]: FAILED! => {"msg": "The following modules failed to execute: apt"}`** — Confirm the target hosts have sudo privileges configured for the ansible user or add become: yes to the playbook tasks.
Confirm the play recap shows `failed=0` and `unreachable=0` before considering the run successful.

---

## Verify

- Confirm the service or component is running and reachable
- Check management UI for any errors or warnings
- Run a basic functional test (login, read, write) to confirm end-to-end operation

---

## See also

- [Ansible — Procedures](../operations/procedures/)
- [Ansible — Common Issues](../troubleshooting/common-issues/)
- [Ansible — How It Works](../architecture/how-it-works/)
