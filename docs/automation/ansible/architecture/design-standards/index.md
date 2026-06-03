# Ansible — Standards


<div class="kb-summary">
> Part of the [Ansible Architecture](../index.md) reference.
</div>

## Project Layout

```text
┌───────────────────────────────────── Ansible — Design Standards ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible design standards enforce consistency, security, and maintainability across playbooks │   │
│   │      Rules: no bare variables, no hardcoded credentials, roles over monolithic playbooks      │   │
│   │           Lint with ansible-lint; molecule for role testing; yamllint for formatting          │   │
│   │           All secrets in Vault or AWX credential store — never in plain text in repo          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Repo and File Structure            │  │               Coding Standards              │   │
│   │         inventories/prod/, staging/          │  │         Name all tasks descriptively        │   │
│   │      roles/ at repo root or collection       │  │           Use FQCN for all modules          │   │
│   │          group_vars/ and host_vars/          │  │       Tag tasks: --tags deploy,config       │   │
│   │      playbooks/ top-level entry points       │  │        Use become only when required        │   │
│   │       .ansible-lint, .yamllint configs       │  │        Validate with check mode first       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FQCN          = Fully Qualified Collection Name; e.g. ansible.builtin.copy not just copy   │   │
│   │     ansible-lint  = static analysis for playbooks and roles; enforces best-practice rules     │   │
│   │    molecule      = role testing framework; creates instances, converges, verifies, destroys   │   │
│   │      yamllint      = YAML syntax and style linter; catches indentation and quoting errors     │   │
│   │become        = privilege escalation (sudo); apply at task level, not play level where possible│   │
│   │          no_log: true  = suppress task output for tasks handling passwords or secrets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Ansible — Design Standards ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible design standards enforce consistency, security, and maintainability across playbooks │   │
│   │      Rules: no bare variables, no hardcoded credentials, roles over monolithic playbooks      │   │
│   │           Lint with ansible-lint; molecule for role testing; yamllint for formatting          │   │
│   │           All secrets in Vault or AWX credential store — never in plain text in repo          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Repo and File Structure            │  │               Coding Standards              │   │
│   │         inventories/prod/, staging/          │  │         Name all tasks descriptively        │   │
│   │      roles/ at repo root or collection       │  │           Use FQCN for all modules          │   │
│   │          group_vars/ and host_vars/          │  │       Tag tasks: --tags deploy,config       │   │
│   │      playbooks/ top-level entry points       │  │        Use become only when required        │   │
│   │       .ansible-lint, .yamllint configs       │  │        Validate with check mode first       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FQCN          = Fully Qualified Collection Name; e.g. ansible.builtin.copy not just copy   │   │
│   │     ansible-lint  = static analysis for playbooks and roles; enforces best-practice rules     │   │
│   │    molecule      = role testing framework; creates instances, converges, verifies, destroys   │   │
│   │      yamllint      = YAML syntax and style linter; catches indentation and quoting errors     │   │
│   │become        = privilege escalation (sudo); apply at task level, not play level where possible│   │
│   │          no_log: true  = suppress task output for tasks handling passwords or secrets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── Ansible — Design Standards ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible design standards enforce consistency, security, and maintainability across playbooks │   │
│   │      Rules: no bare variables, no hardcoded credentials, roles over monolithic playbooks      │   │
│   │           Lint with ansible-lint; molecule for role testing; yamllint for formatting          │   │
│   │           All secrets in Vault or AWX credential store — never in plain text in repo          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Repo and File Structure            │  │               Coding Standards              │   │
│   │         inventories/prod/, staging/          │  │         Name all tasks descriptively        │   │
│   │      roles/ at repo root or collection       │  │           Use FQCN for all modules          │   │
│   │          group_vars/ and host_vars/          │  │       Tag tasks: --tags deploy,config       │   │
│   │      playbooks/ top-level entry points       │  │        Use become only when required        │   │
│   │       .ansible-lint, .yamllint configs       │  │        Validate with check mode first       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    FQCN          = Fully Qualified Collection Name; e.g. ansible.builtin.copy not just copy   │   │
│   │     ansible-lint  = static analysis for playbooks and roles; enforces best-practice rules     │   │
│   │    molecule      = role testing framework; creates instances, converges, verifies, destroys   │   │
│   │      yamllint      = YAML syntax and style linter; catches indentation and quoting errors     │   │
│   │become        = privilege escalation (sudo); apply at task level, not play level where possible│   │
│   │          no_log: true  = suppress task output for tasks handling passwords or secrets         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Module Standards

### Always Use FQCN

```yaml
# Correct
ansible.builtin.package:
community.vmware.vmware_guest:
amazon.aws.ec2_instance:

# Incorrect — short names are deprecated
package:
vmware_guest:
```

### Prefer Declarative Over Imperative

```yaml
# Declarative — idempotent
- name: Ensure nginx is installed
  ansible.builtin.package:
    name: nginx
    state: present

# Imperative — avoid unless no module exists
- name: Install nginx
  ansible.builtin.command:
    cmd: yum install -y nginx
  args:
    creates: /usr/sbin/nginx  # idempotency guard required
```

### shell/command Rules

```yaml
# Always add changed_when or creates/removes guards
- name: Initialize app database
  ansible.builtin.command:
    cmd: /opt/app/bin/db-init
    creates: /opt/app/.db-initialized
  changed_when: true

- name: Get app version (read-only)
  ansible.builtin.command:
    cmd: /opt/app/bin/app --version
  register: app_version
  changed_when: false
  check_mode: false
```

## Variable Management

### Vault File Structure

```yaml
# group_vars/prod/vault.yml (encrypted)
vault_db_password: "prod-db-pass"
vault_api_key: "prod-api-key"

# group_vars/prod/main.yml (plaintext references)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
```

### Precedence Design Rules

| Layer | When to Use |
|---|---|
| `role/defaults/main.yml` | Safe defaults, always overridable |
| `group_vars/all/` | Org-wide settings (NTP, DNS, log servers) |
| `group_vars/<group>/` | Per-environment or per-tier settings |
| `host_vars/<host>/` | Host-specific overrides — use sparingly |
| `--extra-vars` | CI/CD inject version numbers, run IDs |

## Error Handling

```yaml
- name: Deploy application
  block:
    - name: Pull container image
      community.docker.docker_image:
        name: "myapp:{{ deploy_version }}"
        source: pull
    - name: Start container
      community.docker.docker_container:
        name: myapp
        image: "myapp:{{ deploy_version }}"
        state: started
  rescue:
    - name: Alert on failure
      community.general.slack:
        token: "{{ vault_slack_token }}"
        channel: "#alerts"
        msg: "Deployment failed on {{ inventory_hostname }}"
  always:
    - name: Clean up temp files
      ansible.builtin.file:
        path: /tmp/deploy_{{ deploy_version }}.tar.gz
        state: absent
```

## Tags

```yaml
# Standard taxonomy
tags:
  - packages    # installs/removes
  - config      # config file changes
  - service     # service restarts
  - security    # security tasks
  - never       # skip by default (risky tasks)

# Usage
# ansible-playbook site.yml --tags packages,config
# ansible-playbook site.yml --tags never --limit web01
```

## Testing with Molecule

```bash
molecule test           # full cycle
molecule converge       # apply playbook
molecule verify         # run assertions
molecule login          # SSH into instance
```

## Code Review Checklist

| Item | Check |
|---|---|
| All modules use FQCN | `ansible.builtin.` prefix |
| No plaintext secrets | None in task args |
| Vault vars prefixed `vault_` | `vault_db_password` pattern |
| Tasks have meaningful names | Not just module names |
| Idempotency verified | Second run: `changed=0` |
| `no_log: true` on sensitive tasks | Credential tasks suppressed |
| `changed_when` on command/shell | Not left at default |
| Check mode compatible | `--check` doesn't error |
