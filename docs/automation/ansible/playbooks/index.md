# Ansible Playbooks

## Playbook Structure

A playbook is a YAML file containing one or more plays. Each play targets hosts and defines tasks.

```yaml
# site.yml
---
- name: Configure web servers
  hosts: webservers
  become: true
  gather_facts: true
  vars:
    app_port: 8080

  pre_tasks:
    - name: Update apt cache
      ansible.builtin.apt:
        update_cache: true
        cache_valid_time: 3600

  tasks:
    - name: Install nginx
      ansible.builtin.apt:
        name: nginx
        state: present

    - name: Start and enable nginx
      ansible.builtin.service:
        name: nginx
        state: started
        enabled: true

  handlers:
    - name: Reload nginx
      ansible.builtin.service:
        name: nginx
        state: reloaded
```

## Tasks, Handlers, and Notify

Handlers run once at the end of a play, triggered by `notify`. They are deduplicated even if notified multiple times.

```yaml
tasks:
  - name: Deploy nginx config
    ansible.builtin.template:
      src: nginx.conf.j2
      dest: /etc/nginx/nginx.conf
      owner: root
      mode: '0644'
    notify: Reload nginx

  - name: Deploy vhost config
    ansible.builtin.template:
      src: vhost.conf.j2
      dest: /etc/nginx/sites-enabled/app.conf
    notify: Reload nginx      # handler only runs once

handlers:
  - name: Reload nginx
    ansible.builtin.service:
      name: nginx
      state: reloaded
```

## Loops and Conditionals

```yaml
tasks:
  - name: Install required packages
    ansible.builtin.apt:
      name: "{{ item }}"
      state: present
    loop:
      - git
      - curl
      - unzip

  - name: Create app users
    ansible.builtin.user:
      name: "{{ item.name }}"
      groups: "{{ item.groups }}"
    loop:
      - { name: appuser, groups: www-data }
      - { name: deploy,  groups: sudo }

  - name: Only restart on RedHat
    ansible.builtin.service:
      name: httpd
      state: restarted
    when: ansible_os_family == "RedHat"

  - name: Skip if already done
    ansible.builtin.command: /opt/setup.sh
    when: not setup_done | default(false)
```

## Tags

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

## Running Playbooks

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
