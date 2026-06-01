# Ansible — Install & Upgrade


<div class="kb-summary">
> Part of the [Ansible Operations](../index.md) reference.
</div>

## Version Reference

| Component | Current Stable | Notes |
|---|---|---|
| ansible-core | 2.17.x | Python 3.10+ required |
| ansible (community) | 10.x | Bundles ansible-core 2.17 + collections |
| AWX | 24.x | Open-source upstream |
| AAP (Red Hat) | 2.5 | Supported enterprise product |

## Control Node Installation

### RHEL / Rocky Linux 9

```bash
dnf install -y epel-release
dnf install -y ansible-core    # minimal, no bundled collections
# or
dnf install -y ansible         # full community package

ansible --version
```
```
┌───────────────────────────────────── Ansible — Install & Upgrade ─────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Ansible core: install via pip (recommended) or OS package manager; pin version in requirements│   │
│   │   AWX: deployed on Kubernetes via the AWX Operator; upgrade by updating operator CRD version  │   │
│   │ Collections: install via ansible-galaxy; pin in requirements.yml for reproducible environments│   │
│   │       Execution envs: built with ansible-builder; push to registry; update AWX EE config      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Install Ansible Core             │  │             Upgrade AWX Operator            │   │
│   │         python3 -m venv ansible-env          │  │          1. Edit kustomization.yaml         │   │
│   │        pip install ansible-core==2.17        │  │         2. Set newTag: <new-version>        │   │
│   │       pip install -r requirements.txt        │  │            3. kubectl apply -k .            │   │
│   │        ansible-galaxy install -r reqs        │  │            4. Monitor pod rollout           │   │
│   │          ansible --version (verify)          │  │       5. Verify UI login, run test job      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     ansible-builder = tool to create EE container images; reads execution-environment.yml     │   │
│   │   AWX Operator    = Kubernetes operator managing AWX deployment lifecycle; CRD-driven config  │   │
│   │requirements.yml= collections/roles dependency file; ansible-galaxy install -r requirements.yml│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

## Install Collections and Roles

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

## Managed Node Prerequisites

### Linux

```bash
# Check Python exists
ansible -i inventory/ web01 -m ansible.builtin.raw -a "which python3"

# Install Python if missing (raw doesn't need Python)
ansible -i inventory/ web01 -m ansible.builtin.raw \
  -a "dnf install -y python3" --become
```

| OS | Python | Notes |
|---|---|---|
| RHEL / Rocky 8+ | python3 built-in | Auto-detected |
| Ubuntu 20.04+ | python3 built-in | Auto-detected |
| Network devices | Not required | Modules run on control node |
| RHEL 7 | python 2.7 | EOL — upgrade if possible |

### Windows

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

## Upgrade Procedure

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

### Deprecated Patterns to Fix Before Upgrading

```bash
grep -r "include:"          playbooks/ roles/   # → include_tasks
grep -r "always_run:"       playbooks/ roles/   # → check_mode: false
grep -r "sudo:"             playbooks/ roles/   # → become
grep -rE "^\s+\w+:\s*\|"   roles/              # bare module names
```

## AWX on Kubernetes

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

### AWX Upgrade

```bash
# Update operator version — instance CR stays unchanged
kubectl apply -k github.com/ansible/awx-operator/config/default?ref=<new_version>
kubectl rollout status deployment/awx-prod -n awx
```

## SSH Key Setup

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

## Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| `ansible: command not found` | Not on PATH | `source /opt/ansible/bin/activate` |
| `UNREACHABLE — Connection refused` | SSH not running | Check sshd and firewall |
| `FAILED! Permission denied (publickey)` | Key not deployed | Deploy with root credentials first |
| `No module named 'ansible'` | Wrong Python | Verify virtualenv activation |
| `Collection not found` | Not installed | `ansible-galaxy collection install -r requirements.yml` |
