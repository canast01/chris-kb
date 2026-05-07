# Ansible Variables

## Variable Precedence

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

## Defining and Using Variables

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

## extra-vars at Runtime

Extra vars passed on the command line override everything else.

```bash
# Simple key=value pairs
ansible-playbook site.yml -e "app_env=production app_version=2.1.0"

# JSON string for complex data
ansible-playbook site.yml -e '{"app_port": 9090, "debug": true}'

# From a vars file
ansible-playbook site.yml -e @vars/prod.yml
```

## Register and Facts

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

## Vault Variables

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

## set_fact and Variable Manipulation

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
