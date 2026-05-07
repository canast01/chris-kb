# Ansible Roles

## Role Directory Structure

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

Create a skeleton with `ansible-galaxy`:

```bash
ansible-galaxy role init roles/nginx
```

## defaults and vars

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

## meta and Dependencies

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

## Using Roles in Playbooks

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

## Ansible Galaxy

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
