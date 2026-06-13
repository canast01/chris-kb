---
tags:
  - ansible
  - security
---
# Ansible — Hardening

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
```text
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
```bash
# Force TLS 1.2+ on AWX web service
# /etc/tower/conf.d/tls.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 63072000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
```
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
```bash
# Restrict by source IP using authorized_keys options
# /home/ansible/.ssh/authorized_keys
from="10.0.50.10",no-agent-forwarding,no-X11-forwarding,no-port-forwarding ssh-ed25519 AAAA... ansible-control@prod
```
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

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

