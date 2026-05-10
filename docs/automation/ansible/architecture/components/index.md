# Ansible Components Deep Dive

This page covers the full set of Ansible building blocks — inventory, playbooks, roles, tasks, handlers, variables, facts, modules, plugins, collections, and vault — with enough detail to design and maintain a production automation project.

## Inventory

The inventory defines which hosts Ansible manages and how they are grouped. Ansible supports two formats for static inventories.

### INI Format

```ini
# inventory/hosts
[webservers]
web01.prod.example.com
web02.prod.example.com ansible_port=2222

[databases]
db01.prod.example.com ansible_user=dbadmin

[loadbalancers]
lb01.prod.example.com

[prod:children]
webservers
databases
loadbalancers

[prod:vars]
ansible_ssh_private_key_file=~/.ssh/prod_rsa
ntp_server=ntp.prod.example.com
```

### YAML Format

```yaml
# inventory/hosts.yml
all:
  children:
    prod:
      children:
        webservers:
          hosts:
            web01.prod.example.com:
            web02.prod.example.com:
              ansible_port: 2222
        databases:
          hosts:
            db01.prod.example.com:
              ansible_user: dbadmin
      vars:
        ntp_server: ntp.prod.example.com
```

### Dynamic Inventory

Dynamic inventory plugins query external APIs and generate the host list at runtime:

| Plugin | Source | Install |
|---|---|---|
| `amazon.aws.aws_ec2` | AWS EC2 instances | `amazon.aws` collection |
| `azure.azcollection.azure_rm` | Azure VMs | `azure.azcollection` |
| `community.vmware.vmware_vm_inventory` | vSphere VMs | `community.vmware` |
| `kubernetes.core.k8s` | Kubernetes pods | `kubernetes.core` |
| `community.docker.docker_containers` | Docker containers | `community.docker` |

```yaml
# inventory/aws_ec2.yml — dynamic AWS inventory
plugin: amazon.aws.aws_ec2
regions:
  - eu-west-1
  - us-east-1
filters:
  instance-state-name: running
  "tag:Environment": production
keyed_groups:
  - key: tags.Role
    prefix: role
  - key: placement.region
    prefix: region
hostnames:
  - private-dns-name
compose:
  ansible_host: private_ip_address
```

## Playbooks and Plays

A playbook is a YAML file containing one or more plays. A play maps hosts to an ordered list of tasks.

```yaml
# site.yml
---
- name: Configure load balancers           # play name
  hosts: loadbalancers                     # target group
  gather_facts: true
  become: true
  vars:
    haproxy_maxconn: 4096
  pre_tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600
  roles:
    - common
    - haproxy
  post_tasks:
    - name: Verify haproxy is listening
      ansible.builtin.wait_for:
        port: 80
        timeout: 10
```

### Play Keywords

| Keyword | Purpose |
|---|---|
| `hosts` | Target pattern — group name, host name, or wildcard |
| `become` | Enable privilege escalation for the entire play |
| `gather_facts` | Whether to run the setup module at play start |
| `vars` | Play-level variable definitions |
| `vars_files` | Load variables from external YAML files |
| `pre_tasks` | Tasks that run before roles |
| `roles` | Roles to include |
| `tasks` | Inline tasks (instead of or in addition to roles) |
| `post_tasks` | Tasks that run after roles and tasks |
| `handlers` | Handlers defined at play scope |
| `serial` | Number or percentage of hosts to run at once |
| `max_fail_percentage` | Fail the play if this fraction of hosts fail |
| `any_errors_fatal` | Abort all hosts if any host fails |

## Tasks

Tasks are the individual automation actions within a play. Each task calls a module with arguments.

```yaml
tasks:
  - name: Install nginx package
    ansible.builtin.package:
      name: nginx
      state: present
    tags:
      - packages
      - nginx

  - name: Deploy nginx vhost config
    ansible.builtin.template:
      src: nginx_vhost.conf.j2
      dest: /etc/nginx/conf.d/app.conf
      owner: root
      group: root
      mode: '0644'
    notify: Restart nginx
    tags:
      - config
      - nginx

  - name: Ensure nginx is started and enabled
    ansible.builtin.service:
      name: nginx
      state: started
      enabled: true
```

### Task Control Keywords

| Keyword | Purpose |
|---|---|
| `when` | Conditional — task runs only if expression is true |
| `loop` | Iterate task over a list of items |
| `register` | Capture task output into a variable |
| `ignore_errors` | Continue playbook even if this task fails |
| `failed_when` | Custom failure condition |
| `changed_when` | Custom changed condition |
| `notify` | Trigger a handler name when task reports changed |
| `become` | Override privilege escalation for this task |
| `no_log` | Suppress task output from logs |
| `delegate_to` | Run task on a different host |
| `run_once` | Run task only once regardless of host count |
| `retries` / `until` / `delay` | Retry loop until condition met |

```yaml
- name: Wait for application to respond
  ansible.builtin.uri:
    url: "http://{{ ansible_host }}:8080/health"
    status_code: 200
  register: health_result
  until: health_result.status == 200
  retries: 12
  delay: 5
```

## Handlers

Handlers are tasks that run only once per play, triggered when notified by a changed task. Multiple tasks can notify the same handler; it only executes once at play end.

```yaml
# roles/nginx/handlers/main.yml
---
- name: Restart nginx
  ansible.builtin.service:
    name: nginx
    state: restarted

- name: Reload nginx
  ansible.builtin.service:
    name: nginx
    state: reloaded

- name: Reload systemd
  ansible.builtin.systemd:
    daemon_reload: true
```

!!! warning "Handler execution order"
    Handlers always execute after all tasks in the play complete, in the order they are defined — not the order they were notified. Use `meta: flush_handlers` to force immediate handler execution mid-play.

## Variables

Ansible uses a layered variable system with a defined precedence order (highest wins):

| Priority | Source |
|---|---|
| 1 (lowest) | `defaults/main.yml` in a role |
| 2 | Inventory file or dynamic inventory group vars |
| 3 | `group_vars/all` files |
| 4 | `group_vars/<groupname>` files |
| 5 | `host_vars/<hostname>` files |
| 6 | Host facts / `set_fact` |
| 7 | `vars/main.yml` in a role |
| 8 | Play `vars:` block |
| 9 | Task `vars:` block |
| 10 | `include_vars` task |
| 11 | `register` output |
| 12 (highest) | `--extra-vars` on command line |

```yaml
# group_vars/webservers/main.yml
nginx_worker_processes: auto
nginx_worker_connections: 1024
app_port: 8080

# host_vars/web01.prod.example.com/main.yml
nginx_worker_connections: 2048  # override for this host only
```

### Variable Naming Conventions

```yaml
# Use snake_case
nginx_worker_processes: auto        # good
nginxWorkerProcesses: auto          # bad — camelCase

# Prefix role vars with role name to avoid collisions
nginx_log_dir: /var/log/nginx       # good
log_dir: /var/log/nginx             # bad — too generic

# Prefix vault variables
vault_db_password: !vault |         # encrypted value
  $ANSIBLE_VAULT;1.2;AES256
  ...

db_password: "{{ vault_db_password }}"  # plaintext reference
```

## Facts

Facts are variables automatically gathered by the `setup` module at the start of each play. They describe the managed node's current state.

```bash
# View all facts for a host
ansible web01.prod.example.com -m ansible.builtin.setup

# Filter facts by prefix
ansible web01.prod.example.com -m ansible.builtin.setup -a "filter=ansible_os*"
```

Commonly used facts:

| Fact Variable | Value Example |
|---|---|
| `ansible_distribution` | `RedHat`, `Ubuntu`, `Debian` |
| `ansible_distribution_major_version` | `9`, `22`, `12` |
| `ansible_os_family` | `RedHat`, `Debian` |
| `ansible_architecture` | `x86_64`, `aarch64` |
| `ansible_hostname` | `web01` |
| `ansible_fqdn` | `web01.prod.example.com` |
| `ansible_default_ipv4.address` | `10.0.1.100` |
| `ansible_memtotal_mb` | `16040` |
| `ansible_processor_vcpus` | `8` |

### Custom Facts

Deploy custom fact scripts to managed nodes:

```bash
# /etc/ansible/facts.d/app.fact (must be executable, output JSON)
#!/bin/bash
echo '{"version": "2.3.1", "environment": "prod"}'
```

Access as `ansible_local.app.version`.

### Disabling Fact Gathering

```yaml
- name: Quick play — no facts needed
  hosts: all
  gather_facts: false
  tasks:
    - name: Echo hostname
      ansible.builtin.debug:
        msg: "Running on {{ inventory_hostname }}"
```

## Modules

Modules are the actionable units Ansible executes. Core modules in `ansible.builtin`:

| Module | Purpose |
|---|---|
| `ansible.builtin.package` | OS-agnostic package management |
| `ansible.builtin.service` | Manage services |
| `ansible.builtin.template` | Render Jinja2 templates to files |
| `ansible.builtin.copy` | Copy files to managed nodes |
| `ansible.builtin.file` | Manage file permissions and state |
| `ansible.builtin.user` | Manage OS users |
| `ansible.builtin.group` | Manage OS groups |
| `ansible.builtin.command` | Run commands (not idempotent) |
| `ansible.builtin.shell` | Run shell commands (not idempotent) |
| `ansible.builtin.uri` | HTTP requests |
| `ansible.builtin.get_url` | Download files |
| `ansible.builtin.lineinfile` | Manage individual lines in files |
| `ansible.builtin.blockinfile` | Manage blocks of text in files |
| `ansible.builtin.cron` | Manage cron jobs |
| `ansible.builtin.systemd` | Manage systemd units |
| `ansible.builtin.debug` | Print debug messages |
| `ansible.builtin.assert` | Fail if condition not true |
| `ansible.builtin.wait_for` | Wait for condition |
| `ansible.builtin.set_fact` | Set variables dynamically |
| `ansible.builtin.include_tasks` | Dynamically include task files |
| `ansible.builtin.import_tasks` | Statically import task files |

!!! note "Use fully qualified module names (FQCN)"
    Always use the full `namespace.collection.module` format. Short names like `copy:` are deprecated and will not work with future ansible-core versions. FQCN also prevents ambiguity when multiple collections provide a module with the same short name.

## Plugins

### Connection Plugins

```yaml
# Specify connection type per host
[network_devices]
router01 ansible_connection=network_cli ansible_network_os=cisco.ios.ios
switch01 ansible_connection=httpapi ansible_network_os=arista.eos.eos

# Use local connection for API-based modules
[aws_resources]
localhost ansible_connection=local
```

### Lookup Plugins

Lookup plugins retrieve data from external sources at template evaluation time:

```yaml
vars:
  # Read a file on the control node
  ssl_cert: "{{ lookup('ansible.builtin.file', '/etc/ssl/certs/app.crt') }}"

  # Read from environment variable
  deploy_env: "{{ lookup('ansible.builtin.env', 'DEPLOY_ENV') }}"

  # Fetch secret from HashiCorp Vault
  db_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/db password=field') }}"

  # Generate a random password
  temp_password: "{{ lookup('ansible.builtin.password', '/tmp/passfile length=20 chars=ascii_letters,digits') }}"
```

### Callback Plugins

```ini
# ansible.cfg
[defaults]
stdout_callback = yaml       # cleaner human output
bin_ansible_callbacks = True

[callback_yaml]
result_format = yaml
```

## Collections

Collections bundle related content with versioned dependencies:

```yaml
# requirements.yml
---
collections:
  - name: ansible.posix
    version: ">=1.5.0"
  - name: community.vmware
    version: "4.0.0"
  - name: amazon.aws
    version: ">=7.0.0"
  - name: community.general
    version: ">=8.0.0"
  - name: community.hashi_vault
    version: ">=6.0.0"

roles:
  - name: geerlingguy.nginx
    version: "3.2.0"
```

```bash
# Install all requirements
ansible-galaxy collection install -r requirements.yml
ansible-galaxy role install -r requirements.yml

# Install to a project-local path
ansible-galaxy collection install -r requirements.yml -p ./collections/
```

## Vault

Ansible Vault provides AES-256 encryption for sensitive data stored in YAML files or as inline encrypted strings.

```bash
# Encrypt an existing file
ansible-vault encrypt group_vars/prod/vault.yml

# Encrypt a single string value
ansible-vault encrypt_string 'supersecret' --name 'vault_db_password'

# View encrypted file content
ansible-vault view group_vars/prod/vault.yml

# Edit encrypted file in place
ansible-vault edit group_vars/prod/vault.yml

# Rotate the vault password
ansible-vault rekey group_vars/prod/vault.yml
```

```yaml
# group_vars/prod/vault.yml (encrypted)
vault_db_password: "prod-db-secret"
vault_api_token: "xyz-abc-123"

# group_vars/prod/main.yml (plaintext — references vault vars)
db_password: "{{ vault_db_password }}"
api_token: "{{ vault_api_token }}"
```

See the [Vault Encryption](../../security/encryption/) page for full coverage of vault IDs, CI/CD integration, and external secrets integration.
