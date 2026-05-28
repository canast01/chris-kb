# Ansible — Hardening

> Part of the [Ansible Security](../index.md) reference.

## Control Node Hardening

### OS Baseline

```bash
# Dedicated control node — no shared use
# RHEL/Rocky 9 minimal install

# Apply CIS baseline (Level 2 recommended)
ansible-playbook -i localhost, cis-rhel9.yml

# Disable unnecessary services
systemctl disable --now bluetooth avahi-daemon cups rpcbind

# Configure firewall — allow only required ports
firewall-cmd --permanent --set-default-zone=drop
firewall-cmd --permanent --add-service=ssh
firewall-cmd --reload

# Restrict SSH access
cat > /etc/ssh/sshd_config.d/hardening.conf <<EOF
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers ansible sre-operator
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no
EOF
systemctl reload sshd
```
┌───────────────────────────────────────── Ansible — Hardening ─────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Harden Ansible control node and AWX to reduce attack surface and block unauthorised use    │   │
│   │    Control node: restrict SSH access, pin package versions, run in isolated network segment   │   │
│   │      AWX: HTTPS only, MFA, LDAP groups, session timeout, disable API browsable UI in prod     │   │
│   │          Playbook hygiene: no_log on secrets, FQCN for all modules, lint before merge         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Control Node Hardening            │  │                AWX Hardening                │   │
│   │          OS hardened baseline (CIS)          │  │            HTTPS only, valid cert           │   │
│   │         SSH: AllowUsers ansible only         │  │           MFA + LDAP group mapping          │   │
│   │        Pip packages pinned + audited         │  │           Session timeout: 30 min           │   │
│   │            Outbound 22/5986 only             │  │        Disable local accounts (prod)        │   │
│   │     ansible.cfg: host_key_checking=True      │  │          Kubernetes network policy          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     host_key_checking = True prevents connecting to hosts not in known_hosts; blocks MITM     │   │
│   │        Network policy    = Kubernetes NetworkPolicy restricting AWX pod ingress/egress        │   │
│   │    CIS baseline      = Centre for Internet Security hardening guide for the control node OS   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Known Hosts Management

```bash
# Pre-populate known_hosts — never use StrictHostKeyChecking=no
ansible all -i inventory/ -m ansible.builtin.known_hosts \
  -a "name={{ inventory_hostname }} key={{ lookup('pipe', 'ssh-keyscan -t ed25519 ' + inventory_hostname) }}"

# Or populate via playbook before first run
- name: Scan and register host keys
  ansible.builtin.known_hosts:
    name: "{{ item }}"
    key: "{{ lookup('pipe', 'ssh-keyscan -t ed25519 ' + item) }}"
    state: present
  loop: "{{ groups['all'] }}"
  delegate_to: localhost
```

## AWX / AAP Hardening

### Network Exposure

```bash
# Restrict AWX ingress — only allow from known CIDRs
# Kubernetes NetworkPolicy example
cat <<EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: awx-ingress-restrict
  namespace: awx
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: awx-web
  policyTypes:
    - Ingress
  ingress:
    - from:
        - ipBlock:
            cidr: 10.0.0.0/8    # internal only
      ports:
        - protocol: TCP
          port: 8052
EOF
```

### TLS Configuration

```bash
# Force TLS 1.2+ on AWX web service
# /etc/tower/conf.d/tls.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```

### Session and Token Security

```yaml
# AWX Settings → System
AWX_PROOT_ENABLED: true           # job isolation
AWX_PROOT_HIDE_PATHS:             # prevent job access to control filesystem
  - /etc/passwd
  - /home
  - /root
  - /var/lib/awx/projects         # prevent cross-project access

SESSION_COOKIE_AGE: 1800          # 30 min session timeout
OAUTH2_PROVIDER:
  ACCESS_TOKEN_EXPIRE_SECONDS: 31536000
  REFRESH_TOKEN_EXPIRE_SECONDS: 2628000
```

### Execution Environment Isolation

Execution Environments (EEs) run Ansible inside containers, preventing control node filesystem access from job runs:

```yaml
# AWX job template — always assign an EE
execution_environment: "Default EE"   # or custom validated EE

# Build minimal custom EE
# execution-environment.yml
---
version: 3
base_image: registry.redhat.io/ansible-automation-platform-24/ee-minimal-rhel9:latest

dependencies:
  galaxy:
    collections:
      - name: community.vmware
        version: ">=4.3.0"
  python:
    - PyVmomi==8.0.2

additional_build_steps:
  append_final:
    - RUN pip install --no-cache-dir hvac  # HashiCorp Vault client
```

## Managed Node Hardening

### Sudoers Lockdown

```bash
# /etc/sudoers.d/ansible — restrict to required commands only
ansible ALL=(root) NOPASSWD: \
  /usr/bin/dnf update -y, \
  /usr/bin/dnf install -y *, \
  /usr/bin/systemctl start *, \
  /usr/bin/systemctl stop *, \
  /usr/bin/systemctl restart *, \
  /usr/bin/systemctl reload *

# Disable requiretty for ansible (needed for pipelining)
Defaults:ansible !requiretty
```

### SSH Restrictions for ansible Account

```bash
# Restrict by source IP using authorized_keys options
# /home/ansible/.ssh/authorized_keys
from="10.0.50.10",no-agent-forwarding,no-X11-forwarding,no-port-forwarding ssh-ed25519 AAAA... ansible-control@prod
```

## Secrets Management Hardening

```yaml
# Enforce no_log on all credential-touching tasks
- name: Configure application secrets
  ansible.builtin.template:
    src: app-secrets.conf.j2
    dest: /etc/app/secrets.conf
    owner: app
    group: app
    mode: '0600'
  no_log: true

# Validate no plaintext secrets in playbook output
# Add to CI pipeline
- name: Scan for leaked secrets in job output
  ansible.builtin.command:
    cmd: grep -r "password\|secret\|token" /var/log/ansible/
  register: secret_scan
  failed_when: secret_scan.rc == 0
  changed_when: false
```

## Compliance Scanning

```yaml
# Run OpenSCAP scan as part of Ansible playbook
- name: Run CIS benchmark scan
  ansible.builtin.command:
    cmd: >
      oscap xccdf eval
      --profile xccdf_org.ssgproject.content_profile_cis_server_l2
      --results /tmp/oscap-results.xml
      --report /tmp/oscap-report.html
      /usr/share/xml/scap/ssg/content/ssg-rhel9-ds.xml
  register: oscap_result
  failed_when: oscap_result.rc not in [0, 2]
  changed_when: false

- name: Fetch report
  ansible.builtin.fetch:
    src: /tmp/oscap-report.html
    dest: "reports/{{ inventory_hostname }}-cis-{{ ansible_date_time.date }}.html"
    flat: true
```

## Hardening Checklist

| Item | Control | Check |
|---|---|---|
| Control node dedicated | No shared use | `last` — only ansible/admins |
| SSH key auth only | `PasswordAuthentication no` | `sshd -T | grep password` |
| StrictHostKeyChecking on | `host_key_checking = True` | ansible.cfg |
| No plaintext secrets in repo | All in Vault | `git grep -i password` |
| no_log on sensitive tasks | Present on all cred tasks | Code review |
| AWX TLS enforced | HTTPS only | curl -I http:// returns 301 |
| EE isolation enabled | Job template EE assigned | AWX UI |
| Audit logging active | log_path set | ansible.cfg |
| sudo scoped by command | sudoers file reviewed | `visudo -c` |
| Regular vault password rotation | Scheduled quarterly | Runbook |
