---
tags:
  - ansible
  - operations
---
# Ansible — Install & Upgrade

```bash
dnf install -y epel-release
dnf install -y ansible-core    # minimal, no bundled collections
# or
dnf install -y ansible         # full community package

ansible --version
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 19 Dec 2024 02:45:22 PM UTC.
Dependencies resolved.
================================================================================
 Package                    Architecture    Version              Repository
================================================================================
Installing:
 epel-release               noarch          9-7.el9              @System
Complete!
Last metadata expiration check: 0:00:01 ago on Thu 19 Dec 2024 02:45:55 PM UTC.
Dependencies resolved.
================================================================================
 Package                    Architecture    Version              Repository
================================================================================
Installing:
 ansible-core               x86_64          2.15.8-1.el9         epel
 python3-jinja2             x86_64          3.0.1-2.el9          appstream
 python3-markupsafe         x86_64          2.1.1-1.el9          appstream
Complete!
ansible [core 2.15.8]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/root/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  python version = 3.11.7 (main, Dec 19 2024, 14:22:33) [GCC 13.2.0]
```

!!! warning "Common errors"
    **`Error: Unable to find a match: ansible-core`** — Run `dnf install -y epel-release` first to enable the EPEL repository.
    **`Error: Package dnf-plugins-core-4.0.21-1.el9.noarch requires python3-dnf(x86-64) = 4.0.21-1.el9, but none of the providers can be installed`** — Run `dnf update -y` to resolve dependency conflicts before installing packages.
```bash
ansible-galaxy collection install -r requirements.yml
ansible-galaxy role install -r requirements.yml

# Project-local (isolates from system installs)
ansible-galaxy collection install -r requirements.yml -p ./collections/

# Force upgrade
ansible-galaxy collection install -r requirements.yml --upgrade
```
```yaml
# requirements.yml
---
collections:
  - name: community.vmware
    version: ">=4.3.0"
  - name: amazon.aws
    version: ">=8.0.0"
  - name: community.hashi_vault
    version: ">=6.2.0"
  - name: ansible.posix
    version: ">=1.5.4"
  - name: servicenow.itsm
    version: ">=2.5.0"
roles:
  - name: geerlingguy.docker
    version: "7.1.0"
```
```bash
# Check Python exists
ansible -i inventory/ web01 -m ansible.builtin.raw -a "which python3"

# Install Python if missing (raw doesn't need Python)
ansible -i inventory/ web01 -m ansible.builtin.raw \
  -a "dnf install -y python3" --become
```
```powershell
# On Windows target — enable WinRM
$url = "https://raw.githubusercontent.com/ansible/ansible/devel/examples/scripts/ConfigureRemotingForAnsible.ps1"
Invoke-WebRequest $url -OutFile $env:temp\ConfigureRemotingForAnsible.ps1
powershell.exe -ExecutionPolicy ByPass -File $env:temp\ConfigureRemotingForAnsible.ps1
```
```bash
pip install pywinrm
ansible -i inventory/ winhost -m ansible.windows.win_ping \
  -e "ansible_connection=winrm ansible_winrm_transport=ntlm"
```

```text title="Expected output"
Collecting pywinrm
  Downloading pywinrm-0.4.4-py2.py3-none-any.whl (44 kB)
     |████████████████████████████████| 44 kB 2.3 MB/s
Collecting pyspnego>=0.1.5 (from pywinrm)
  Downloading pyspnego-0.10.2-py3-none-any.whl (148 kB)
     |████████████████████████████████| 148 kB 5.1 MB/s
Installing collected packages: pyspnego, pywinrm
Successfully installed pyspnego-0.10.2 pywinrm-0.4.4

winhost | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

!!! warning "Common errors"
    **`ERROR! Unexpected failure during module execution.`** — Ensure WinRM is enabled on the target Windows host with `Enable-PSRemoting -Force` and verify the firewall allows port 5985 (HTTP) or 5986 (HTTPS).
    **`fatal: [winhost]: UNREACHABLE! => {"msg": "ntlm: HTTPSConnectionPool(host='winhost', port=5986): Max retries exceeded"}`** — Verify DNS resolution for the hostname, check network connectivity to the Windows host, and confirm the correct `ansible_host` IP address in your inventory file.
    **`ERROR! the playbook: inventory/ does not exist`** — Ensure the inventory directory path is correct and contains valid inventory files (e.g., `hosts.ini` or `hosts.yml`).
```bash
# Review release notes first
# https://github.com/ansible/ansible/blob/devel/changelogs/

# Upgrade in venv
source /opt/ansible/bin/activate
pip install --upgrade ansible-core==2.17.3

# Verify collections still compatible
ansible-galaxy collection list
ansible-playbook --syntax-check site.yml

# Check for deprecated syntax
ansible-lint site.yml

# Test against staging first
ansible-playbook -i inventory/staging/ site.yml --check
ansible-playbook -i inventory/staging/ site.yml
```

```text title="Expected output"
(/opt/ansible) $ pip install --upgrade ansible-core==2.17.3
Collecting ansible-core==2.17.3
  Downloading ansible-core-2.17.3.tar.gz (12.4 MB)
Installing collected packages: ansible-core
  Attempting uninstall: ansible-core
    Found existing installation: ansible-core==2.16.5
    Uninstalling ansible-core-2.16.5...
Successfully installed ansible-core-2.17.3

(/opt/ansible) $ ansible-galaxy collection list

Collection                    Version
----------------------------- -------
ansible.netcommon             6.1.0
ansible.posix                 1.5.4
community.general             8.2.0
community.vmware              4.1.0
kubernetes.core               3.0.1

(/opt/ansible) $ ansible-playbook --syntax-check site.yml
playbook: site.yml

(/opt/ansible) $ ansible-lint site.yml
Passed with 0 warnings

(/opt/ansible) $ ansible-playbook -i inventory/staging/ site.yml --check
PLAY [Configure web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-staging-01]
ok: [web-staging-02]

TASK [Install packages] ********************************************************
changed: [web-staging-01]
changed: [web-staging-02]

PLAY RECAP *********************************************************************
web-staging-01             : ok=8 changed=2 unreachable=0 failed=0
web-staging-02             : ok=8 changed=2 unreachable=0 failed=0

(/opt/ansible) $ ansible-playbook -i inventory/staging/ site.yml
PLAY [Configure web servers] ***************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-staging-01]
ok: [web-staging-02]

TASK [Install packages] ********************************************************
changed: [web-staging-01]
changed: [web-staging-02]

PLAY RECAP *********************************************************************
web-staging-01             : ok=8 changed=3 unreachable=0 failed=0
web-staging-02             : ok=8 changed=3 unreachable=0 failed=0
```

!!! warning "Common errors"
    **`ERROR! Unexpected Exception: No module named 'jinja2'`** — Run `pip install jinja2` in the venv before upgrading ansible-core.
    **`[WARNING]: Skipping unknown variable 'ansible_python_interpreter'`** — Update deprecated variable names in inventory or group_vars to use `ansible_python_executable` instead.
    **`fatal: [web-staging-01]: FAILED! => {"msg": "Timeout waiting for privilege escalation prompt."}`** — Ensure staging inventory has correct `ansible_become_pass` or SSH key permissions for the staging user.
```bash
grep -r "include:"          playbooks/ roles/   # → include_tasks
grep -r "always_run:"       playbooks/ roles/   # → check_mode: false
grep -r "sudo:"             playbooks/ roles/   # → become
grep -rE "^\s+\w+:\s*\|"   roles/              # bare module names
```

```text title="Expected output"
playbooks/deploy.yml:5:    - include: tasks/pre-flight.yml
playbooks/deploy.yml:12:    - include: common/setup.yml
roles/webserver/tasks/main.yml:8:    - include: ssl-config.yml
roles/database/handlers/main.yml:3:    - include: restart-db.yml
playbooks/legacy/bootstrap.yml:22:    - include: roles/monitoring/tasks/check.yml
playbooks/deploy.yml:18:      always_run: yes
roles/webserver/tasks/main.yml:45:      always_run: true
playbooks/maintenance.yml:9:      always_run: no
roles/app/tasks/deploy.yml:33:        sudo: yes
roles/database/tasks/main.yml:7:        sudo: no
roles/webserver/tasks/ssl.yml:12:        sudo: true
roles/app/handlers/main.yml:28:      shell: |
roles/monitoring/tasks/check.yml:15:      command: |
```

!!! warning "Common errors"
    **`grep: roles/: No such file or directory`** — Ensure you run this command from the Ansible project root directory where both `playbooks/` and `roles/` directories exist.
    **`No matches found`** — If the grep returns no output, your playbooks may already be using Ansible 2.3+ syntax (include_tasks, check_mode, become); verify by checking a sample playbook manually.
```bash
# Install AWX Operator
kubectl apply -k github.com/ansible/awx-operator/config/default?ref=2.19.1

# Deploy AWX instance
cat <<EOF | kubectl apply -f -
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx-prod
  namespace: awx
spec:
  service_type: LoadBalancer
  admin_email: ansible-admin@example.com
  projects_persistence: true
  projects_storage_size: 20Gi
EOF

# Get admin password
kubectl get secret awx-prod-admin-password \
  -o jsonpath="{.data.password}" | base64 --decode
```

```text title="Expected output"
namespace/awx created
serviceaccount/awx-operator-controller-manager created
role.rbac.authorization.k8s.io/awx-operator-leader-election-role created
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding created
clusterrole.rbac.authorization.k8s.io/awx-operator-manager-role created
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-manager-rolebinding created
deployment.apps/awx-operator-controller-manager created
awx.awx.ansible.com/awx-prod created
ansible-admin-p4s9w2k1x7
```

!!! warning "Common errors"
    **`error: the server doesn't have a resource type "awx" in group "awx.ansible.com"`** — Ensure the AWX Operator CRD is fully deployed by waiting for the operator pod to be ready with `kubectl wait --for=condition=ready pod -l control-plane=controller-manager -n awx-operator-system --timeout=300s`.
    **`Error from server (NotFound): secrets "awx-prod-admin-password" not found`** — Wait for the AWX instance to finish initializing (typically 2-3 minutes) before retrieving the secret; check status with `kubectl get awx -n awx`.
    **`error: unable to recognize "STDIN": no matches for kind "AWX" in version "awx.ansible.com/v1beta1"`** — Verify the operator deployment completed successfully and the CRD is registered with `kubectl get crd | grep awx`.
```bash
# Update operator version — instance CR stays unchanged
kubectl apply -k github.com/ansible/awx-operator/config/default?ref=<new_version>
kubectl rollout status deployment/awx-prod -n awx
```

```text title="Expected output"
namespace/awx created
serviceaccount/awx-operator-controller-manager created
role.rbac.authorization.k8s.io/awx-operator-leader-election-role created
rolebinding.rbac.authorization.k8s.io/awx-operator-leader-election-rolebinding created
clusterrole.rbac.authorization.k8s.io/awx-operator-manager-role created
clusterrolebinding.rbac.authorization.k8s.io/awx-operator-manager-rolebinding created
deployment.apps/awx-operator-controller-manager configured
Waiting for deployment spec update to be observed...
Waiting for deployment "awx-prod" rollout to finish: 1 old replicas pending termination...
Waiting for deployment "awx-prod" rollout to finish: 0 of 2 updated replicas are available...
deployment "awx-prod" successfully rolled out
```

!!! warning "Common errors"
    **`error: unable to recognize "github.com/awx-operator/config/default?ref=<new_version>": no matches for kind "Kustomization" in version "kustomize.config.k8s.io/v1beta1"`** — Ensure the kustomization.yaml file exists in the remote repository and the ref parameter points to a valid git tag or branch.
    **`error: timed out waiting for the condition`** — Check pod events with `kubectl describe pod -n awx` and verify sufficient cluster resources; the rollout may be blocked by image pull errors or resource constraints.
```bash
# Create service account
useradd -r -s /bin/bash -m -d /home/ansible ansible

# Generate key
sudo -u ansible ssh-keygen -t ed25519 \
  -C "ansible-control@$(hostname)" \
  -f /home/ansible/.ssh/ansible_ed25519 -N ""

# Distribute to managed nodes
ansible all -i inventory/ -m ansible.posix.authorized_key \
  -a "user=ansible key={{ lookup('file', '/home/ansible/.ssh/ansible_ed25519.pub') }}" \
  --become --user root
```

```d2
direction: right

plan: "Plan" {shape: oval}
verify: "Verify" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> verify
verify -> validate
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ansible — Deploy](../../deploy/)
