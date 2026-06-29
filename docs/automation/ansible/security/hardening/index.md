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


```text title="Expected output"
PLAY [localhost] ***************************************************************

TASK [Gathering Facts] *********************************************************
ok: [localhost]

TASK [Apply CIS baseline controls] *********************************************
changed: [localhost] => (item=kernel_hardening)
changed: [localhost] => (localhost) => (item=file_permissions)
changed: [localhost] => (localhost) => (item=selinux_config)
changed: [localhost] => (localhost) => (item=audit_daemon)

PLAY RECAP *********************************************************************
localhost                  : ok=4 changed=4 unreachable=0 failed=0

Removed /etc/systemd/system/multi-user.target.wants/bluetooth.service.
Removed /etc/systemd/system/multi-user.target.wants/avahi-daemon.service.
Removed /etc/systemd/system/multi-user.target.wants/cups.service.
Removed /etc/systemd/system/multi-user.target.wants/rpcbind.service.

success
success
success

(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ERROR! the playbook: cis-rhel9.yml could not be found`** — Verify the playbook path is correct and exists in the current working directory or use an absolute path.
    **`Job for sshd.service failed because the control process exited with error code.`** — Check `/var/log/secure` for SSH config syntax errors and validate with `sshd -t` before reloading.
    **`FirewallD is not running.`** — Start the firewall service with `systemctl start firewalld` before applying permanent rules.
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

```text title="Expected output"
networkpolicy.networking.k8s.io/awx-ingress-restrict created
```

!!! warning "Common errors"
    **`error: unable to recognize "STDIN": no matches for kind "NetworkPolicy" in version "networking.k8s.io/v1"`** — Verify the Kubernetes cluster version supports networking.k8s.io/v1 (1.16+); use `kubectl api-resources | grep networkpolicies` to confirm availability.
    **`Error from server (Forbidden): networkpolicies.networking.k8s.io is forbidden: User "system:serviceaccount:default:deployer" cannot create resource "networkpolicies"`** — Grant the service account cluster-admin or network-admin RBAC role with `kubectl create clusterrolebinding awx-netpol-admin --clusterrole=admin --serviceaccount=awx:default`.
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`sudoers:1: syntax error near line 1`** — Remove the comment line; sudoers files cannot contain comments before the first rule, place comments after the first valid entry or use a separate documentation file.
    **`sudo: parse error in /etc/sudoers.d/ansible near line 3`** — Use `visudo -f /etc/sudoers.d/ansible` to validate syntax; the wildcard `*` in dnf install requires quoting as `/usr/bin/dnf install -y \*` or replace with specific package names.
    **`ansible: sorry, you must have a tty to run sudo`** — Ensure the `Defaults:ansible !requiretty` line is present and the file is validated with `visudo -f /etc/sudoers.d/ansible` before deployment.
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

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Ansible — Authentication](../authentication/)
- [Ansible — Access Control](../access-control/)
- [Ansible — Encryption](../encryption/)
