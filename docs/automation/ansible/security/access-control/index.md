---
tags:
  - ansible
  - security
description: "Ansible access control: SSH key management, service account scoping, sudo privilege restriction, and RBAC controls for AWX/Automation Controller job..."
---
# Ansible — Access Control

<div class="kb-summary">
Ansible access control: SSH key management, service account scoping, sudo privilege restriction, and RBAC controls for AWX/Automation Controller job templates.

*Applies to: Ansible 2.14+*
</div>

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## AWX / AAP RBAC Model

Ansible Automation Platform enforces role-based access control at the organization, team, and object level.

```d2
direction: right

ORG: "Organization" {shape: rectangle}
TEAM: "Teams" {shape: rectangle}
USER: "Users" {shape: rectangle}
CRED: "Credentials" {shape: rectangle}
INV: "Inventories" {shape: rectangle}
PROJ: "Projects" {shape: rectangle}
JT: "Job Templates" {shape: rectangle}
ROLE: "Role Assignment\nAdmin / Execute / Use / Read" {shape: rectangle}

ORG -> TEAM
TEAM -> USER
ORG -> CRED
ORG -> INV
ORG -> PROJ
ORG -> JT
USER -> ROLE
```

### Sudoers — Scope Privilege Escalation

```bash
# /etc/sudoers.d/ansible
# Allow ansible user to sudo only specific commands (preferred)
ansible ALL=(root) NOPASSWD: /usr/bin/dnf, /usr/bin/yum, /usr/bin/apt-get, \
  /usr/bin/systemctl, /usr/sbin/service

# If full sudo required, restrict to specific hosts only via sudoers
# Avoid: ansible ALL=(ALL) NOPASSWD: ALL
```

```yaml
# Enforce become only on tasks that need it — not globally
- name: Install packages (needs root)
  ansible.builtin.package:
    name: nginx
    state: present
  become: true

- name: Check app status (no escalation needed)
  ansible.builtin.command:
    cmd: /opt/app/bin/status
  become: false
```

## Inventory Access Controls

```yaml
# Limit playbook runs to specific groups
ansible-playbook site.yml --limit webservers
ansible-playbook site.yml --limit "prod:&webservers"   # prod AND webservers
ansible-playbook site.yml --limit "all:!databases"     # exclude databases

# In AWX — set inventory source limits per job template
# Job Template → "Limit" field → "webservers"
```

## Credential Isolation

AWX never exposes credential values to job runs — the automation controller injects them as environment variables or files inside an isolated execution environment.

```yaml
# Bad — plaintext credential in vars
db_password: "mysecret"

# Good — credential injected by AAP at runtime
# SSH credentials: injected as SSH_AUTH_SOCK / private key file
# Cloud credentials: injected as AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
# Custom credentials: injected per credential type input fields
```

### Custom Credential Types

```json
// Input configuration (what fields to collect)
{
  "fields": [
    {"id": "api_token", "label": "API Token", "secret": true, "type": "string"},
    {"id": "api_url",   "label": "API URL",   "secret": false, "type": "string"}
  ]
}

// Injector configuration (how to expose in job)
{
  "env": {
    "MY_APP_TOKEN": "{{ api_token }}",
    "MY_APP_URL":   "{{ api_url }}"
  }
}
```

## Audit and Compliance

```bash
# AWX activity stream — full audit log
curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/activity_stream/?page_size=50" \
  | python3 -m json.tool

# Filter by user
curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/activity_stream/?actor__username=jsmith"

# Job history — who ran what, when, against which hosts
curl -H "Authorization: Bearer $AWX_TOKEN" \
  "https://awx.example.com/api/v2/jobs/?launched_by__username=jsmith&page_size=20"
```


```text title="Expected output"
{
  "count": 247,
  "next": "https://awx.example.com/api/v2/activity_stream/?page=2&page_size=50",
  "previous": null,
  "results": [
    {
      "id": 1024,
      "timestamp": "2024-01-15T14:32:18.456789Z",
      "actor": {
        "id": 12,
        "username": "jsmith",
        "first_name": "John",
        "last_name": "Smith"
      },
      "action": "create",
      "object1_type": "job",
      "object1_id": 5847,
      "summary_fields": {
        "job": {
          "id": 5847,
          "name": "Deploy-Prod-Web",
          "status": "successful"
        }
      }
    },
    {
      "id": 1023,
      "timestamp": "2024-01-15T13:18:42.123456Z",
      "actor": {"id": 12, "username": "jsmith"},
      "action": "update",
      "object1_type": "credential",
      "object1_id": 89
    }
  ]
}
{
  "count": 18,
  "results": [
    {
      "id": 5847,
      "name": "Deploy-Prod-Web",
      "launched_by": "jsmith",
      "created": "2024-01-15T14:32:18.456789Z",
      "status": "successful",
      "hosts_processed": 12,
      "hosts_failed": 0
    },
    {
      "id": 5821,
      "name": "Deploy-Prod-Web",
      "launched_by": "jsmith",
      "created": "2024-01-14T09:15:33.789012Z",
      "status": "successful",
      "hosts_processed": 12,
      "hosts_failed": 0
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl or configure proper CA certificates in your AWX instance. |
    | `{"detail":"Invalid token","status":401}` | Verify `$AWX_TOKEN` is set correctly with `echo $AWX_TOKEN` and regenerate it from AWX Settings > Users if expired. |
    | `curl: (7) Failed to connect to awx.example.com port 443: Connection refused` | Confirm AWX service is running with `systemctl status awx` and verify the hostname/port in your curl command. |
| Audit Event | AWX Log Location |
|---|---|
| Job launch | Activity stream + job events |
| Credential use | Activity stream |
| User login | Activity stream + system logs |
| RBAC change | Activity stream |
| Inventory update | Activity stream |

---

## See also

- [Ansible — Authentication](../authentication/)
- [Ansible — Hardening](../hardening/)
- [Ansible — Encryption](../encryption/)
