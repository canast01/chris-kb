---
tags:
  - ansible
  - operations
description: "Ansible operational procedures: deploying playbooks, managing inventory sources, rotating vault passwords, and promoting changes from dev to production..."
---
# Ansible — Procedures

<div class="kb-summary">
Ansible operational procedures: deploying playbooks, managing inventory sources, rotating vault passwords, and promoting changes from dev to production environments.

*Applies to: Ansible 2.14+*
</div>

---

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

- [ ] Playbook tested in staging environment or validated with `--check` mode
- [ ] Inventory validated — `--list-hosts` confirms correct target scope
- [ ] Vault secrets are accessible (vault password file or prompt configured)
- [ ] `--limit` flag set to scope the run to the correct host group or pattern
- [ ] Rollback playbook or manual revert procedure documented
- [ ] `--tags` or `--skip-tags` configured if running a subset of tasks
- [ ] Syntax check passes: `ansible-playbook site.yml --syntax-check`

| Item | Status | Notes |
|---|---|---|
| Staging / check-mode run | | Pass / Fail |
| Inventory scope (`--limit`) | | Host group or pattern |
| Vault access confirmed | | Yes / No |
| Rollback procedure | | Link to runbook |
| Syntax check | | Pass / Fail |

## Incident Triage

- [ ] Re-run the playbook with `-v` (verbose) or `-vvv` (very verbose) to capture detailed output
- [ ] Test SSH connectivity to the failing target host manually
- [ ] Validate `become`/sudo access on the target host
- [ ] Check the inventory source — confirm the failing host is listed and reachable
- [ ] Confirm the correct Python interpreter is available on the target
- [ ] Review Ansible log file if logging is configured (`log_path` in ansible.cfg)
- [ ] Check if a Vault-encrypted variable file failed to decrypt
- [ ] Confirm no module or collection version mismatch between control node and requirements

| Question | Answer |
|---|---|
| Is the target host reachable via SSH? | `ssh -i <key> user@host` |
| Does become/sudo work? | `ansible <host> -m shell -a "id" --become` |
| Is the Vault password accessible? | Check vault password file/env var |
| Is the inventory returning the host? | `ansible <group> --list-hosts` |
| Is the correct Python available? | `ansible_python_interpreter` set? |

## Maintenance Window

1. Disable AWX/Tower scheduled jobs or comment out cron entries for the affected playbooks during the window.
2. Notify team of the maintenance window and the scope of playbook changes.
3. Take a snapshot or backup of configuration files on target hosts if the playbook makes destructive changes.
4. Run the playbook with `--check` immediately before the window to confirm expected task list.
5. Execute the playbook with `--limit` scoped to the target group; monitor output.
6. If a failure occurs mid-run, stop and execute the rollback playbook or manual revert.
7. Re-enable AWX/Tower scheduled jobs or cron entries after successful completion.
8. Confirm idempotency with a follow-up `--check` run.

## Post-Change Validation

- [ ] Re-run the playbook in `--check` mode — confirm zero tasks report changes (idempotent)
- [ ] Full re-run produces no unexpected changes on any host
- [ ] Target service or application is healthy and responding
- [ ] AWX/Tower scheduled jobs re-enabled and showing green on next run
- [ ] Ansible log or AWX job output shows no errors or warnings
- [ ] Inventory still returns the expected host count for all groups
- [ ] Vault-encrypted variables still decrypt successfully

## Ansible Tower / AWX Job Launch Sequence

```d2
direction: right

operator: "Operator\n(User / API / Schedule" {shape: rectangle}
jobTemplate: "Job Template\n(playbook + inventory + creds" {shape: rectangle}
awxQueue: "AWX/Tower\nJob Queue" {shape: rectangle}
awxExecutor: "AWX Executor\n(container/fork" {shape: rectangle}
inventorySource: "Inventory Source\n(dynamic sync" {shape: rectangle}
vaultCreds: "Vault / Machine\nCredentials" {shape: rectangle}
managed: "Managed Hosts\n(SSH" {shape: rectangle}
jobHistory: "Job History\n& Artifacts" {shape: rectangle}

operator -> jobTemplate
jobTemplate -> awxQueue
awxQueue -> awxExecutor
awxExecutor -> inventorySource
awxExecutor -> vaultCreds
awxExecutor -> managed
awxExecutor -> jobHistory
```

### Tags

Tags let you selectively run subsets of tasks without editing the playbook.

```yaml
tasks:
  - name: Install packages
    ansible.builtin.apt:
      name: "{{ item }}"
      state: present
    loop: "{{ packages }}"
    tags:
      - packages
      - install

  - name: Deploy config
    ansible.builtin.template:
      src: app.conf.j2
      dest: /etc/app/app.conf
    tags:
      - config
      - deploy
```

```bash
# Run only tasks tagged 'config'
ansible-playbook site.yml --tags config

# Skip tasks tagged 'packages'
ansible-playbook site.yml --skip-tags packages

# List all tags in a playbook
ansible-playbook site.yml --list-tags

# Dry-run (check mode)
ansible-playbook site.yml --check --diff
```


```text title="Expected output"
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web01.prod.local]
ok: [web02.prod.local]
ok: [db01.prod.local]

TASK [Apply configuration] *****************************************************
changed: [web01.prod.local]
changed: [web02.prod.local]
ok: [db01.prod.local]

PLAY RECAP *********************************************************************
web01.prod.local           : ok=8    changed=2    unreachable=0    failed=0
web02.prod.local           : ok=8    changed=2    unreachable=0    failed=0
db01.prod.local            : ok=7    changed=0    unreachable=0    failed=0

playbook: site.yml
  play #1 (all): all	TAGS: []
    tasks:
      config	TAGS: [config]
      deploy	TAGS: [deploy]
      packages	TAGS: [packages]
      security	TAGS: [config,security]

[CHECK] [DRY RUN] will change: [web01.prod.local]
changed: [web01.prod.local] (dry run)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! Unable to parse site.yml as an Ansible YAML file.` | Validate YAML syntax with `ansible-playbook site.yml --syntax-check` and fix indentation or quote issues. |
    | `fatal: [web01.prod.local]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}` | Verify SSH key permissions are 600, the correct key is in `~/.ssh/`, and the remote user matches the inventory definition. |
    | `ERROR! the playbook: site.yml could not be found` | Ensure `site.yml` exists in the current working directory or provide the full path with `ansible-playbook /path/to/site.yml`. |
### Running Playbooks

| Flag | Purpose |
|---|---|
| `-i inventory/` | Specify inventory path |
| `--limit web01` | Target a subset of hosts |
| `--check` | Dry run, no changes made |
| `--diff` | Show file diffs on changes |
| `-v / -vvv` | Increase verbosity |
| `--start-at-task "name"` | Resume from a specific task |
| `--tags / --skip-tags` | Filter by tag |
| `-e "key=value"` | Pass extra variables |

```bash
# Standard run
ansible-playbook -i inventory/ site.yml

# Limit to one host with verbose output
ansible-playbook -i inventory/ site.yml --limit web01 -vv

# Run only deploy-tagged tasks on production
ansible-playbook -i inventory/ site.yml --tags deploy --limit production
```


```text title="Expected output"
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web01]
ok: [web02]
ok: [db01]

TASK [Install packages] ********************************************************
changed: [web01]
changed: [web02]
ok: [db01]

TASK [Configure services] ******************************************************
ok: [web01]
ok: [web02]
ok: [db01]

PLAY RECAP *********************************************************************
web01                      : ok=12   changed=3    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
web02                      : ok=12   changed=3    unreachable=0    failed=0    skipped=2    rescued=0    ignored=0
db01                       : ok=11   changed=0    unreachable=0    failed=0    skipped=3    rescued=0    ignored=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `[WARNING]: Unable to parse /etc/ansible/inventory/ as an inventory source` | Verify the inventory directory path exists and contains valid inventory files (hosts, hosts.yml, or hosts.ini). |
    | `fatal: [web01]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}` | Ensure SSH keys are properly configured and the ansible_user has passwordless SSH access to all target hosts. |
    | `ERROR! tag(s) not found in /path/to/site.yml: ['deploy']` | Verify the tag name matches exactly (case-sensitive) and exists in at least one task within the playbook. |
## Roles

Roles provide a standardised way to organise tasks, variables, files, and templates.

```bash
roles/
  nginx/
    tasks/
      main.yml        # entry point — all tasks
    handlers/
      main.yml        # handlers referenced by tasks
    templates/
      nginx.conf.j2   # Jinja2 templates
    files/
      index.html      # static files to copy
    vars/
      main.yml        # high-priority role vars
    defaults/
      main.yml        # low-priority defaults (overridable)
    meta/
      main.yml        # role metadata and dependencies
    README.md
```


```text title="Expected output"
roles/
├── nginx/
│   ├── tasks/
│   │   └── main.yml
│   ├── handlers/
│   │   └── main.yml
│   ├── templates/
│   │   └── nginx.conf.j2
│   ├── files/
│   │   └── index.html
│   ├── vars/
│   │   └── main.yml
│   ├── defaults/
│   │   └── main.yml
│   ├── meta/
│   │   └── main.yml
│   └── README.md
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal: [localhost]: FAILED! => {"msg": "Unable to retrieve file contents"}` | Verify the template or file path exists in the correct subdirectory (templates/ or files/) and is readable by the Ansible user. |
    | `ERROR! the role 'nginx' was not found in /etc/ansible/roles:/usr/share/ansible/roles` | Add the roles/ directory to the `roles_path` setting in ansible.cfg or ensure the playbook references the correct relative path with `roles_path: ./roles`. |
    | `fatal: [localhost]: FAILED! => {"msg": "Undefined variable"}` | Check that variables referenced in tasks are defined in either vars/main.yml, defaults/main.yml, or passed via -e flags; verify variable names match exactly (case-sensitive). |
Create a skeleton with `ansible-galaxy`:

```bash
ansible-galaxy role init roles/nginx
```


```text title="Expected output"
- Role roles/nginx was created successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! The directory roles/nginx already exists. You can use --force to overwrite` | Run `ansible-galaxy role init roles/nginx --force` to recreate the role structure. |
    | `ERROR! 'roles' directory does not exist in /path/to/project` | Create the roles directory first with `mkdir -p roles` before running the command. |
### defaults and vars

`defaults/main.yml` holds low-priority variables that callers can override. `vars/main.yml` holds higher-priority values not intended to be overridden.

```yaml
# roles/nginx/defaults/main.yml
nginx_port: 80
nginx_worker_processes: auto
nginx_keepalive_timeout: 65
nginx_log_dir: /var/log/nginx

# roles/nginx/vars/main.yml
nginx_pid_file: /run/nginx.pid
nginx_conf_dir: /etc/nginx
```

### meta and Dependencies

The `meta/main.yml` file declares role metadata and dependencies that Ansible resolves before running the role.

```yaml
# roles/nginx/meta/main.yml
galaxy_info:
  author: your_name
  description: Install and configure nginx
  license: MIT
  min_ansible_version: "2.12"
  platforms:
    - name: Ubuntu
      versions:
        - "22.04"
        - "24.04"

dependencies:
  - role: common
    vars:
      common_packages:
        - curl
        - ca-certificates
```

### Using Roles in Playbooks

```yaml
# site.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  roles:
    - common
    - role: nginx
      vars:
        nginx_port: 443
    - role: certbot
      when: ssl_enabled | default(true)
```

Roles can also be called as tasks with `ansible.builtin.include_role`:

```yaml
tasks:
  - name: Apply nginx role conditionally
    ansible.builtin.include_role:
      name: nginx
    vars:
      nginx_port: 8080
    when: install_nginx | default(true)
```

### Ansible Galaxy

| Command | Purpose |
|---|---|
| `ansible-galaxy role install geerlingguy.nginx` | Install a role from Galaxy |
| `ansible-galaxy role install -r requirements.yml` | Install from requirements file |
| `ansible-galaxy role list` | List installed roles |
| `ansible-galaxy role remove geerlingguy.nginx` | Remove a role |
| `ansible-galaxy role init roles/myrole` | Scaffold a new role |

```yaml
# requirements.yml
roles:
  - name: geerlingguy.nginx
    version: "3.2.0"
  - name: geerlingguy.postgresql
    version: "3.4.1"
collections:
  - name: community.general
    version: ">=8.0.0"
```

```bash
# Install all requirements
ansible-galaxy install -r requirements.yml

# Install to a specific path
ansible-galaxy role install -r requirements.yml -p roles/
```


```text title="Expected output"
Starting galaxy role install process
- downloading role from https://galaxy.ansible.com/api/v1/roles/?owner__username=geerlingguy&name=docker
- extracting geerlingguy.docker to /home/ansible/.ansible/roles/geerlingguy.docker
- geerlingguy.docker (4.2.1) was installed successfully
- downloading role from https://galaxy.ansible.com/api/v1/roles/?owner__username=geerlingguy&name=java
- extracting geerlingguy.java to /home/ansible/.ansible/roles/geerlingguy.java
- geerlingguy.java (3.1.0) was installed successfully
- downloading role from https://galaxy.ansible.com/api/v1/roles/?owner__username=geerlingguy&name=postgresql
- extracting geerlingguy.postgresql to roles/geerlingguy.postgresql
- geerlingguy.postgresql (5.0.2) was installed successfully
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! the file requirements.yml does not exist, or it is not readable` | Verify the requirements.yml file exists in the current directory and check file permissions with `ls -la requirements.yml`. |
    | `ERROR! - the specified path does not exist. Please check the path and try again.` | Create the target roles directory first with `mkdir -p roles/` before running the install command. |
## Inventory

### INI Format Inventory

The simplest inventory format uses INI-style grouping with hosts and optional inline variables.

```ini
# inventory/hosts.ini

[webservers]
web01.example.com
web02.example.com ansible_port=2222

[dbservers]
db01.example.com ansible_user=admin
db02.example.com

[production:children]
webservers
dbservers

[webservers:vars]
http_port=80
nginx_version=1.24
```

### YAML Format Inventory

YAML inventory is more expressive and suits complex nested group hierarchies.

```yaml
# inventory/hosts.yml
all:
  children:
    webservers:
      hosts:
        web01.example.com:
          ansible_port: 22
        web02.example.com:
          ansible_port: 2222
      vars:
        http_port: 80
    dbservers:
      hosts:
        db01.example.com:
          ansible_user: admin
        db02.example.com:
      vars:
        db_port: 5432
```

### Dynamic Inventory

Dynamic inventory plugins pull host data from external sources at runtime.

```bash
# Install the AWS collection
ansible-galaxy collection install amazon.aws

# Preview dynamic inventory output
ansible-inventory -i inventory/aws_ec2.yml --list

# Show as tree
ansible-inventory -i inventory/aws_ec2.yml --graph

# Run playbook against dynamic inventory
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - eu-west-1
filters:
  instance-state-name: running
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role
hostnames:
  - private-ip-address
```

### host_vars and group_vars

Variable files scoped to individual hosts or groups, loaded automatically by Ansible.

```bash
# Recommended directory layout
inventory/
  hosts.yml
  host_vars/
    web01.example.com/
      main.yml        # host-specific vars
      vault.yml       # encrypted secrets
  group_vars/
    webservers/
      main.yml        # applied to all webservers
      vault.yml       # encrypted group secrets
    all/
      main.yml        # applied to every host
```

```yaml
# inventory/group_vars/webservers/main.yml
nginx_worker_processes: auto
nginx_keepalive_timeout: 65
ssl_certificate: /etc/ssl/certs/web.crt
```

### Grouping Strategies

| Pattern | Syntax example | Purpose |
|---|---|---|
| Static group | `[webservers]` | Manually listed hosts |
| Child group | `[prod:children]` | Group that contains other groups |
| Inline group vars | `[web:vars]` | Variables applied to group |
| Range expansion | `web[01:05]` | Generates web01 through web05 |
| Regex match | `~web\d+\.example\.com` | Pattern-matched host names |

### Inventory Commands

```bash
# List all hosts
ansible-inventory -i inventory/ --list

# Show tree structure
ansible-inventory -i inventory/ --graph

# Test connectivity for all hosts
ansible -i inventory/ all -m ping

# Run ad-hoc command on a group
ansible -i inventory/ webservers -m shell -a "uptime"

# Inspect variables for one host
ansible-inventory -i inventory/ --host web01.example.com

# Check which groups a host belongs to
ansible -i inventory/ --list-hosts webservers
```


```text title="Expected output"
{
  "all": {
    "hosts": {
      "web01.example.com": {"ansible_host": "10.42.1.15", "env": "prod"},
      "web02.example.com": {"ansible_host": "10.42.1.16", "env": "prod"},
      "db01.example.com": {"ansible_host": "10.42.2.8", "env": "prod"},
      "db02.example.com": {"ansible_host": "10.42.2.9", "env": "prod"}
    },
    "children": ["webservers", "databases"]
  },
  "_meta": {"hostvars": {...}}
}

@all:
  |--@ungrouped:
  |--@webservers:
  |  |--web01.example.com
  |  |--web02.example.com
  |--@databases:
  |  |--db01.example.com
  |  |--db02.example.com

web01.example.com | SUCCESS => {"ping": "pong"}
web02.example.com | SUCCESS => {"ping": "pong"}
db01.example.com | SUCCESS => {"ping": "pong"}
db02.example.com | SUCCESS => {"ping": "pong"}

web01.example.com | CHANGED | rc=0 >>
 10:24:33 up 187 days, 3:42, 2 users, load average: 0.18, 0.22, 0.19
web02.example.com | CHANGED | rc=0 >>
 10:24:34 up 156 days, 12:15, 1 user, load average: 0.41, 0.38, 0.35

{
  "ansible_host": "10.42.1.15",
  "env": "prod",
  "ansible_user": "deploy",
  "ansible_port": 22
}

  hosts (2):
    web01.example.com
    web02.example.com
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `[WARNING]: Unable to parse inventory/hosts as an YAML source` | Verify inventory file syntax with `ansible-inventory -i inventory/ --list` and check for YAML formatting errors. |
    | `fatal: [web01.example.com]: UNREACHABLE! => {"msg": "Failed to connect to the host via ssh: Permission denied (publickey)."}` | Ensure SSH key is loaded with `ssh-add` and the `ansible_user` variable matches the remote account. |
    | `[WARNING]: Could not match supplied host pattern, ignoring: webservers` | Confirm the group name exists in your inventory with `ansible-inventory -i inventory/ --graph` and verify spelling. |
## Variables

### Variable Precedence

Ansible resolves variable conflicts using a strict precedence order. Higher numbers win.

| Priority | Source |
|---|---|
| 1 (lowest) | `defaults/main.yml` in a role |
| 2 | Inventory group_vars/all |
| 3 | Inventory group_vars/groupname |
| 4 | Inventory host_vars/hostname |
| 5 | Play `vars:` block |
| 6 | `vars_files:` |
| 7 | `include_vars` |
| 8 | `set_fact` / `register` |
| 9 | `vars/main.yml` in a role |
| 10 (highest) | `-e` / `--extra-vars` on CLI |

### Defining and Using Variables

```yaml
# In a play vars block
- hosts: webservers
  vars:
    app_port: 8080
    app_user: webapp
    deploy_dir: /opt/app

  tasks:
    - name: Create deploy directory
      ansible.builtin.file:
        path: "{{ deploy_dir }}"
        owner: "{{ app_user }}"
        state: directory
        mode: '0755'
```

### extra-vars at Runtime

Extra vars passed on the command line override everything else.

```bash
# Simple key=value pairs
ansible-playbook site.yml -e "app_env=production app_version=2.1.0"

# JSON string for complex data
ansible-playbook site.yml -e '{"app_port": 9090, "debug": true}'

# From a vars file
ansible-playbook site.yml -e @vars/prod.yml
```


```text title="Expected output"
PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-01.prod.internal]
ok: [web-02.prod.internal]
ok: [db-01.prod.internal]

TASK [Deploy application] ******************************************************
changed: [web-01.prod.internal]
changed: [web-02.prod.internal]
skipped: [db-01.prod.internal]

TASK [Verify deployment] *******************************************************
ok: [web-01.prod.internal]
ok: [web-02.prod.internal]
ok: [db-01.prod.internal]

PLAY RECAP *********************************************************************
web-01.prod.internal       : ok=3    changed=1    unreachable=0    failed=0
web-02.prod.internal       : ok=3    changed=1    unreachable=0    failed=0
db-01.prod.internal        : ok=2    changed=0    unreachable=0    failed=0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ERROR! Syntax Error while loading YAML from string: mapping values are not allowed here` | Escape special characters in key=value pairs or wrap the entire `-e` argument in single quotes. |
    | `ERROR! Unable to parse as an inventory source: /path/to/vars/prod.yml` | Verify the vars file path is correct and use `@vars/prod.yml` with the `@` symbol to load from file. |
    | `fatal: [web-01.prod.internal]: FAILED! => {"msg": "Unexpected templating type error occurred on '{{ app_version }}': string indices must be integers"}` | Ensure variable names in the playbook match exactly those passed via `-e` (case-sensitive). |
### Register and Facts

`register` captures a task's output as a variable for use in subsequent tasks.

```yaml
- name: Get current kernel version
  ansible.builtin.command: uname -r
  register: kernel_version

- name: Show kernel
  ansible.builtin.debug:
    msg: "Kernel: {{ kernel_version.stdout }}"

- name: Reboot if kernel changed
  ansible.builtin.reboot:
  when: kernel_version.stdout != expected_kernel
```

Ansible facts are automatically gathered variables about managed hosts:

```yaml
- name: Show OS details
  ansible.builtin.debug:
    msg: "{{ ansible_distribution }} {{ ansible_distribution_version }}"

- name: Set timezone based on datacenter
  ansible.builtin.timezone:
    name: "Europe/Athens"
  when: ansible_hostname | regex_search('^dc1')
```

### Vault Variables

Sensitive values should be stored in encrypted vault files rather than plaintext.

```bash
# Create an encrypted vars file
ansible-vault create group_vars/all/vault.yml

# Edit an existing vault file
ansible-vault edit group_vars/all/vault.yml

# Encrypt a single value for inline use
ansible-vault encrypt_string 'mypassword' --name 'db_password'
```

```yaml
# group_vars/all/vault.yml (encrypted at rest)
vault_db_password: "s3cr3tpassword"
vault_api_key: "abc123xyz"

# group_vars/all/main.yml (plaintext, references vault vars)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
```

### set_fact and Variable Manipulation

```yaml
- name: Build versioned artifact name
  ansible.builtin.set_fact:
    artifact_name: "app-{{ app_version }}-{{ ansible_date_time.date }}.tar.gz"

- name: Combine default and custom config
  ansible.builtin.set_fact:
    final_config: "{{ default_config | combine(custom_config, recursive=True) }}"

- name: Filter list of packages
  ansible.builtin.set_fact:
    required_packages: "{{ all_packages | select('match', '^python') | list }}"
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ansible — Health Checks](../health-checks/)
- [Ansible — CLI Reference](../cli-reference/)
- [Ansible — Common Issues](../../troubleshooting/common-issues/)
