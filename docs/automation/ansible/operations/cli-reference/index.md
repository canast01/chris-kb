---
tags:
  - ansible
  - operations
description: "Ansible CLI reference: ansible, ansible-playbook, ansible-vault, ansible-galaxy, ansible-inventory, and ansible-doc command syntax with common flags."
---
# Ansible — CLI Reference

<div class="kb-summary">
Ansible CLI reference: `ansible`, `ansible-playbook`, `ansible-vault`, `ansible-galaxy`, `ansible-inventory`, and `ansible-doc` command syntax with common flags.

*Applies to: Ansible 2.14+*
</div>

> Part of the [Ansible Operations](../index.md) reference.

Ansible is an agentless automation tool — it connects to remote hosts over SSH and runs tasks defined in YAML playbooks. There's nothing to install on the managed hosts. The control node (where you run `ansible` and `ansible-playbook`) needs Python and the Ansible package.

> Install with `pip install ansible` or your distro's package manager. Requires SSH access to managed hosts and a valid inventory file.

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Control Node and Inventory Topology

```d2
direction: right

controlNode: "Control Node\n(ansible + python" {shape: rectangle}
inventoryFile: "Inventory\n(INI / YAML / Dynamic" {shape: rectangle}
vaultSecrets: "Vault Secrets\n(ansible-vault" {shape: rectangle}
galaxyRoles: "Galaxy Roles\n& Collections" {shape: rectangle}
groupWeb: "Group: webservers\nweb01, web02" {shape: rectangle}
groupDB: "Group: dbservers\ndb01, db02" {shape: rectangle}
groupNet: "Group: network_devices\nrouter01" {shape: rectangle}
web01: "web01" {shape: rectangle}
web02: "web02" {shape: rectangle}
db01: "db01" {shape: rectangle}
db02: "db02" {shape: rectangle}
router01: "router01" {shape: rectangle}

controlNode -> inventoryFile
controlNode -> vaultSecrets
controlNode -> galaxyRoles
inventoryFile -> groupWeb
inventoryFile -> groupDB
inventoryFile -> groupNet
groupWeb -> web01
groupWeb -> web02
groupDB -> db01
groupDB -> db02
groupNet -> router01
```

---

## ansible-playbook

Run a playbook against an inventory. Playbooks are YAML files that define a sequence of tasks. Use check mode to preview changes before applying them.

```bash
# Run a playbook
ansible-playbook playbook.yml
ansible-playbook -i inventory.ini playbook.yml

# Dry run (check mode)
ansible-playbook playbook.yml --check
ansible-playbook playbook.yml --check --diff

# Limit to specific hosts / groups
ansible-playbook playbook.yml --limit webservers
ansible-playbook playbook.yml --limit host1,host2

# Extra variables
ansible-playbook playbook.yml -e "env=prod"
ansible-playbook playbook.yml -e "@vars.yml"

# Tags
ansible-playbook playbook.yml --tags deploy
ansible-playbook playbook.yml --skip-tags cleanup
ansible-playbook playbook.yml --list-tags

# Step through tasks
ansible-playbook playbook.yml --step
ansible-playbook playbook.yml --start-at-task "task name"

# Verbosity
ansible-playbook playbook.yml -v
ansible-playbook playbook.yml -vvv

# Become / privilege escalation
ansible-playbook playbook.yml --become
ansible-playbook playbook.yml --become-user root

# List tasks / hosts
ansible-playbook playbook.yml --list-tasks
ansible-playbook playbook.yml --list-hosts
```


```text title="Expected output"
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web01.prod.local]
ok: [web02.prod.local]
ok: [db01.prod.local]

TASK [Install nginx] ***********************************************************
changed: [web01.prod.local]
changed: [web02.prod.local]
skipped: [db01.prod.local]

TASK [Start nginx service] *****************************************************
ok: [web01.prod.local]
ok: [web02.prod.local]
skipped: [db01.prod.local]

PLAY RECAP *********************************************************************
web01.prod.local           : ok=3    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
web02.prod.local           : ok=3    changed=1    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0
db01.prod.local            : ok=1    changed=0    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! the playbook: playbook.yml could not be found` | Verify the playbook file exists in the current directory or provide the full path with `-i` for inventory. |
    | `fatal: [host1]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey,password)."}` | Ensure SSH keys are configured correctly and the ansible_user has proper permissions in the inventory file. |
    | `ERROR! Syntax Error while loading YAML from "playbook.yml"` | Fix YAML indentation and syntax errors in the playbook file using a YAML linter. |
---

## ansible-inventory

Inspect your inventory — list all hosts, view group membership, and show variables assigned to specific hosts. Essential for debugging inventory plugin configurations.

```bash
# List all hosts and groups in JSON
ansible-inventory -i inventory.ini --list

# Tree view of groups and hosts
ansible-inventory -i inventory.ini --graph

# Show all variables for a specific host
ansible-inventory -i inventory.ini --host <hostname>

# YAML output (easier to read than JSON)
ansible-inventory -i inventory.ini --list --yaml
```


```text title="Expected output"
{
    "_meta": {
        "hostvars": {
            "web01.prod.local": {
                "ansible_host": "192.168.1.45",
                "ansible_user": "deploy",
                "env": "production"
            },
            "db01.prod.local": {
                "ansible_host": "192.168.1.50",
                "ansible_user": "deploy",
                "env": "production"
            }
        }
    },
    "all": {
        "children": ["ungrouped", "webservers", "databases"]
    },
    "webservers": {
        "hosts": ["web01.prod.local", "web02.prod.local"]
    },
    "databases": {
        "hosts": ["db01.prod.local"]
    }
}

@all:
  |--@ungrouped:
  |--@webservers:
  |  |--web01.prod.local
  |  |--web02.prod.local
  |--@databases:
     |--db01.prod.local

ansible_host: 192.168.1.45
ansible_user: deploy
env: production
region: us-east-1

all:
  children:
  - ungrouped
  - webservers
  - databases
webservers:
  hosts:
  - web01.prod.local
  - web02.prod.local
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `[WARNING]: Unable to parse inventory.ini as an inventory source` | Verify the inventory file path is correct and the file exists in the current directory or provide an absolute path with `-i /path/to/inventory.ini`. |
    | `[ERROR]: Unable to find host <hostname> in inventory` | Ensure the hostname matches exactly (case-sensitive) and exists in the inventory file; use `--graph` first to list all available hosts. |
---

## ansible-galaxy

Install and manage roles and collections from Ansible Galaxy (the community hub) or private Automation Hub.

```bash
# Install role
ansible-galaxy install <author>.<role>
ansible-galaxy install -r requirements.yml

# Install collection
ansible-galaxy collection install <namespace>.<collection>
ansible-galaxy collection install -r requirements.yml

# List installed roles / collections
ansible-galaxy list
ansible-galaxy collection list

# Init new role
ansible-galaxy init <role_name>

# Search
ansible-galaxy search <keyword>
ansible-galaxy role info <author>.<role>
```


```text title="Expected output"
Starting galaxy role install process
- downloading role from https://galaxy.ansible.com/api/v1/roles/?owner__username=<author>&name=<role>/
- extracting <author>.<role> to /home/ansible/.ansible/roles/<author>.<role>
- <author>.<role> was installed successfully

Process install dependency 'geerlingguy.java'
- downloading role from https://galaxy.ansible.com/api/v1/roles/?owner__username=geerlingguy&name=java/
- extracting geerlingguy.java to /home/ansible/.ansible/roles/geerlingguy.java
- geerlingguy.java was installed successfully

Starting galaxy collection install process
- downloading collection from https://galaxy.ansible.com/download/community-general-7.2.0.tar.gz
- extracting community.general to /home/ansible/.ansible/collections/ansible_collections/community/general
- community.general (version 7.2.0) was installed successfully

# /home/ansible/.ansible/roles:
- geerlingguy.apache, 3.4.2
- geerlingguy.java, 2.1.0
- geerlingguy.mysql, 4.2.1

# /home/ansible/.ansible/collections/ansible_collections:
Collection        Version
community.general 7.2.0
ansible.posix     1.5.1
community.aws     6.1.0

- Role <role_name> was created successfully
  /home/ansible/roles/<role_name>/defaults/main.yml
  /home/ansible/roles/<role_name>/handlers/main.yml
  /home/ansible/roles/<role_name>/tasks/main.yml
  /home/ansible/roles/<role_name>/templates/
  /home/ansible/roles/<role_name>/vars/main.yml

Found 12 roles matching 'nginx':
 Name                                     Description
 geerlingguy.nginx                        Installs and configures nginx web server
 jdauphant.nginx                          Nginx role for Debian/Ubuntu/CentOS
 bennojoy.nginx                           Installs and configures nginx
 ...

Role Info
 id: 45821
 name: nginx
 namespace: geerlingguy
 description: Installs and configures nginx web server on Linux.
 download_count: 2847291
 versions_url: https://galaxy.ansible.com/api/v2/roles/45821/versions/
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! the specified requirements file (requirements.yml) does not exist` | Verify the requirements.yml file exists in the current directory or provide the full path with `-r /path/to/requirements.yml`. |
    | `ERROR! - the collection community.general:99.0.0 cannot be found on any of the configured sources` | Check the collection version exists on Ansible Galaxy and correct the version constraint in requirements.yml. |
    | `ERROR! role definition must contain a 'src' key` | Ensure each role in requirements.yml has a properly formatted entry with at minimum a `src:` field (e.g., `src: geerlingguy.nginx`). |
---

## ansible-vault

Encrypt sensitive data (passwords, API keys, certificates) in playbooks and variable files. Vault-encrypted content can be stored safely in version control.

```bash
# Create encrypted file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml

# Decrypt
ansible-vault decrypt secrets.yml

# View without decrypting to disk
ansible-vault view secrets.yml

# Edit in place
ansible-vault edit secrets.yml

# Encrypt a string inline
ansible-vault encrypt_string 'mysecret' --name 'db_password'

# Rekey (change password)
ansible-vault rekey secrets.yml

# Run playbook with vault
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```


```text title="Expected output"
New Vault password: 
Confirm New Vault password: 
Encryption successful
Encryption successful
Decryption successful
---BEGIN ENCRYPTED FILE---
$ANSIBLE_VAULT;1.1;AES256;filter_default
66386d343962643662666439313966643966643966643966643966643966643966643966643966
64396664396664396664396664396664396664396664396664396664396664396664396664396664
39666439666439666439666439666439666439666439666439666439666439666439666439666439
---END ENCRYPTED FILE---
db_password: !vault |
  $ANSIBLE_VAULT;1.1;AES256;filter_default
  66386d343962643662666439313966643966643966643966643966643966643966643966643966
  64396664396664396664396664396664396664396664396664396664396664396664396664396664
Rekeying /home/ansible/secrets.yml
New Vault password: 
Confirm New Vault password: 
Rekey successful
PLAY [all] *********************************************************************
TASK [setup] *******************************************************************
ok: [web-01.prod.local]
ok: [db-01.prod.local]
TASK [Deploy application] ******************************************************
ok: [web-01.prod.local]
changed: [db-01.prod.local]
PLAY RECAP *********************************************************************
web-01.prod.local          : ok=2    changed=0    unreachable=0    failed=0
db-01.prod.local           : ok=2    changed=1    unreachable=0    failed=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Vault password: Decryption failed` | Ensure you're entering the correct vault password that was used when the file was encrypted. |
    | `ERROR! Decryption failed (no vault secrets were found that could decrypt /path/to/secrets.yml)` | Provide the vault password via `--ask-vault-pass` or `--vault-password-file` when running the playbook. |
    | `[Errno 13] Permission denied: '/home/user/.vault_pass'` | Ensure the vault password file has read permissions (`chmod 600 ~/.vault_pass`) and is owned by the correct user. |
---

## Tools, Lint & Config

Supporting tools for code quality, documentation, and configuration inspection.

### ansible-lint

Checks playbooks and roles for best-practice violations and common mistakes. Run before committing playbook changes.

```bash
# Lint a playbook
ansible-lint playbook.yml

# Lint a role
ansible-lint roles/myrole/

# List rules
ansible-lint --list-rules

# Skip specific rules
ansible-lint playbook.yml --skip-list rule-id-1,rule-id-2
```


```text title="Expected output"
Passed with max profile: basic
Examining playbook.yml of type playbook
Passed: 0 warning(s), 0 error(s)

Examining roles/myrole/ of type role
Passed: 0 warning(s), 0 error(s)

id     title                                    description
------  ----------------------------------------  -----------------------------------------------
E101   syntax-error                             Ansible syntax error
E102   unexpected-jinja2                        Unexpected Jinja2 variable or filter
E103   undefined-var                            Undefined variable
E201   trailing-spaces                          Trailing spaces
E202   missing-newline-at-end-of-file           Missing newline at end of file
...

Examining playbook.yml of type playbook
Passed: 0 warning(s), 0 error(s)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ansible-lint: command not found` | Install ansible-lint with `pip install ansible-lint` or your package manager. |
    | `[Errno 2] No such file or directory: 'playbook.yml'` | Verify the playbook path is correct and the file exists in your current working directory. |
    | `invalid choice: 'rule-id-1' (choose from 'E101', 'E102', ...)` | Use valid rule IDs from `ansible-lint --list-rules` output when specifying the skip-list. |
### ansible-doc

Browse built-in module documentation from the command line — no browser needed.

```bash
# Show module documentation
ansible-doc copy
ansible-doc package
ansible-doc yum

# List all available modules
ansible-doc -l

# Filter by type
ansible-doc -t connection -l
ansible-doc -t lookup -l
```


```text title="Expected output"
> FILE: copy

NAME
  copy - Copy files to remote hosts

DESCRIPTION
  The `copy' module copies files from the local or remote machine to a location on the remote machine.

OPTIONS (= is mandatory):
  - backup
        Create a backup file including the timestamp information so you can get
        the original file back if you somehow clobbered it incorrectly.
        [default: False]
  - content
        When used instead of `src', sets the contents of a file directly to the
        specified value.
  - dest
        Remote absolute path where the file should be copied to. This can be either
        a file or directory.
        [type: path] [Required]

> FILE: package

NAME
  package - Generic OS package manager

DESCRIPTION
  Installs, upgrade and removes packages using the underlying OS package manager.

OPTIONS (= is mandatory):
  - name
        Package name, or a list of package names, to install, upgrade, or remove.
        [type: list] [Required]
  - state
        Whether to install (`present'), remove (`absent') a package, upgrade
        (`latest') or set to a specific version.
        [default: present]

> FILE: yum

NAME
  yum - Manages packages with the yum package manager

DESCRIPTION
  Installs, upgrades, downgrades, removes, and lists packages and groups with the
  `yum' package manager.

OPTIONS (= is mandatory):
  - name
        A package name or package specifier with version, like `name-1.0'.
        [type: list] [Required]
  - state
        Whether to install (`present', `latest'), or remove (`absent') a package.
        [default: present]

Ansible 2.10.8 (core 2.10.8)

---

Ansible built-in modules (2.10.8):

acl                                                  Sets and retrieves file ACL information.
add_host                                            Add a host to the in-memory inventory.
apt                                                 Manages apt-packages.
assemble                                            Assemble configuration files from fragments.
assert                                              Asserts given expressions are true.
async_status                                        Obtain status of asynchronous task.
...

---

CONNECTION PLUGINS (2.10.8):

local                                               execute on controller
paramiko_ssh                                        Run tasks via python ssh (paramiko)
psrp                                                Run tasks over Microsoft PowerShell Remoting Protocol
ssh                                                 connect via ssh client binary
...

LOOKUP PLUGINS (2.10.8):

config                                              Lookup current Ansible configuration values
csvfile                                             read data from a CSV file
dict                                                Returns an item from a dictionary
env                                                 Read the value of environment variables
file                                                read file contents
first_found                                         return first file found from list
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `[WARNING]: Ansible is being run in a world writable /tmp directory.` | Run ansible-doc from a non-world-writable directory or set ANSIBLE_LIBRARY to a secure path. |
    | `ERROR! No module named 'ansible'` | Install Ansible using `pip install ansible` or your system package manager. |
    | `[ERROR]: module not found in configured module paths` | Ensure the module exists by running `ansible-doc -l` to verify it's available in your Ansible |
### ansible-config

Inspect Ansible's effective configuration — useful when troubleshooting unexpected behavior.

```bash
# Show current config
ansible-config view
ansible-config dump

# Show non-default settings
ansible-config dump --only-changed

# List all config options
ansible-config list
```


```text title="Expected output"
# ansible-config view
[defaults]
host_key_checking = False
inventory = /etc/ansible/hosts
roles_path = /etc/ansible/roles:/usr/share/ansible/roles
log_path = /var/log/ansible.log
forks = 10
timeout = 10
gathering = smart

# ansible-config dump
ACTION_WARNINGS(default) = True
AGENTLESS_MANAGER_TIMEOUT(default) = 0
ALLOW_WORLD_READABLE_TMPFILES(default) = False
ANSIBLE_LIBRARY(default) = /usr/share/ansible/plugins/modules
ANSIBLE_PLUGINS(default) = /usr/share/ansible/plugins
CACHE_PLUGIN(default) = memory
CACHE_PLUGIN_CONNECTION(default) = 
CACHE_PLUGIN_PREFIX(default) = ansible_facts
...

# ansible-config dump --only-changed
HOST_KEY_CHECKING(/etc/ansible/ansible.cfg) = False
INVENTORY(/etc/ansible/ansible.cfg) = /etc/ansible/hosts
FORKS(/etc/ansible/ansible.cfg) = 10
LOG_PATH(/etc/ansible/ansible.cfg) = /var/log/ansible.log

# ansible-config list
ACTION_WARNINGS:
  default: true
  description: By default Ansible will issue a warning when received from a task action
  env: [ANSIBLE_ACTION_WARNINGS]
  ini:
  - {key: action_warnings, section: defaults}
  type: boolean
  version_added: '2.5'
AGENTLESS_MANAGER_TIMEOUT:
  default: 0
  description: Number of seconds to wait for async tasks to finish
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ansible-config: command not found` | Install ansible with `pip install ansible` or `apt install ansible`. |
    | `Error: config file does not exist at /etc/ansible/ansible.cfg` | Create the config file or set `ANSIBLE_CONFIG` environment variable to point to a valid configuration file. |
### Common Patterns

```bash
# Test connectivity before running
ansible all -m ping && ansible-playbook site.yml

# Run with SSH key
ansible-playbook playbook.yml --private-key ~/.ssh/id_ed25519

# Use specific user
ansible-playbook playbook.yml -u admin

# Parallel execution (default is 5 forks)
ansible-playbook playbook.yml -f 20

# CI/CD pattern
ansible-playbook playbook.yml \
  -i inventory.ini \
  --vault-password-file ~/.vault_pass \
  --check --diff
```


```text title="Expected output"
host1 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
host2 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
host3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}

PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [host1]
ok: [host2]
ok: [host3]

TASK [Example task] ************************************************************
changed: [host1]
changed: [host2]
changed: [host3]

PLAY RECAP *********************************************************************
host1                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
host2                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
host3                      : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: [host1]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}` | Verify the SSH key path is correct and the public key is installed on target hosts with `ssh-copy-id -i ~/.ssh/id_ed25519.pub user@host`. |
    | `ERROR! Vault password file not found at ~/.vault_pass` | Create the vault password file with `echo 'your-password' > ~/.vault_pass && chmod 600 ~/.vault_pass` or use `--ask-vault-pass` instead. |
    | `fatal: [host2]: FAILED! => {"msg": "The following modules failed to execute: setup"}` | Ensure Python 3 is installed on all target hosts and the `ansible_python_interpreter` is correctly set in inventory if using a non-standard path. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ansible — Procedures](../procedures/)
- [Ansible — Scripts](../scripts/)
- [Ansible — Health Checks](../health-checks/)
