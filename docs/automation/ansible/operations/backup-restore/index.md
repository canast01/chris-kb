# Ansible — Backup & Restore


<div class="kb-summary">
> Part of the [Ansible Operations](../index.md) reference.
</div>

## What to Back Up

| Item | Location | Method |
|---|---|---|
| Playbooks, roles, collections | Git repository | Git push to remote |
| Inventory + group_vars / host_vars | Git repository | Git push to remote |
| Vault-encrypted secrets | Git repository | Safe to commit encrypted |
| ansible.cfg, requirements.yml | Git repository | Git push to remote |
| AWX job templates / credentials | AWX DB | Tower CLI export |
| SSH private keys | Control node filesystem | Vault secret + rsync |
| Custom callback plugins | Git repository | Git push to remote |

## Git Repository Backup (Primary)

Everything needed to reproduce the automation must be in Git. The repo is the source of truth.

```bash
# Ensure remote is current
git push origin main
git push origin --tags

# Mirror to secondary backup remote
git remote add backup git@backup-gitlab.example.com:ansible/infrastructure.git
git push backup --mirror
```text
┌───────────────────────────────────── Ansible — Backup & Restore ──────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Ansible backup: the source of truth is the git repository — playbooks, roles, inventory, vars │   │
│   │   AWX state: export via awx CLI or AWX API; includes job templates, credentials, inventories  │   │
│   │  Restore: re-deploy AWX (Kubernetes operator or RPM), re-import exported objects, reconfigure │   │
│   │    Critical: Vault password must be stored out-of-band (password manager, HSM) — not in git   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               What to Back Up                │  │                Restore Steps                │   │
│   │        Git repo (all automation code)        │  │           1. Redeploy AWX instance          │   │
│   │         AWX export: awx export --all         │  │      2. Import AWX objects from export      │   │
│   │        Vault password (offline safe)         │  │          3. Restore Vault password          │   │
│   │          AWX PostgreSQL DB snapshot          │  │        4. Verify job template runs OK       │   │
│   │       Execution environment OCI images       │  │       5. Test connectivity to targets       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   awx CLI     = command-line client for AWX API; awx export --all dumps all objects to JSON   │   │
│   │     AWX DB      = PostgreSQL database; stores job history, credentials (encrypted), config    │   │
│   │     Vault PW    = Ansible Vault password; if lost, all vault-encrypted vars are unreadable    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## AWX / AAP Export

### awx-manage

```bash
# On the AWX/AAP server
awx-manage dumpdata --natural-foreign --natural-primary \
  -e sessions -e admin \
  > /tmp/awx-dump-$(date +%F).json

scp /tmp/awx-dump-$(date +%F).json backup-server:/backups/awx/
```

### AWX CLI

```bash
pip install awxkit

# Export all objects
awx export --all --output awx-backup-$(date +%F).json \
  --conf.host https://awx.example.com \
  --conf.token "$AWX_TOKEN"

# Export specific types
awx export --job_templates --output job_templates.json
awx export --credentials --output credentials.json  # values are $encrypted$
awx export --inventory --output inventories.json
```

### Via Playbook

```yaml
- name: Export AWX job templates
  hosts: localhost
  gather_facts: false
  collections: [ansible.controller]
  tasks:
    - name: Export all job templates
      ansible.controller.export:
        job_templates: "all"
      register: export_data

    - name: Write export file
      ansible.builtin.copy:
        content: "{{ export_data | to_nice_json }}"
        dest: "/backups/awx/job-templates-{{ ansible_date_time.date }}.json"
```

## Vault Secrets Backup

Ansible Vault files are encrypted — safe in Git. For disaster recovery, also store decrypted values in HashiCorp Vault:

```bash
# Push secrets to HashiCorp Vault
ansible-vault view group_vars/prod/vault.yml | \
  while IFS=': ' read -r key value; do
    vault kv put secret/ansible/prod/$key value="$value"
  done
```

### Rotate Vault Password

```bash
# Generate new password file
openssl rand -base64 32 > ~/.ansible_vault_pass_new

# Rekey all vault files
find . -name "vault.yml" -exec ansible-vault rekey \
  --new-vault-password-file ~/.ansible_vault_pass_new {} \;

mv ~/.ansible_vault_pass_new ~/.ansible_vault_pass
```

## Restore Procedures

### Restore Control Node from Scratch

```bash
# 1. Install ansible-core
dnf install -y epel-release ansible-core

# 2. Restore SSH keys
mkdir -p /home/ansible/.ssh && chmod 700 /home/ansible/.ssh
scp backup-server:/backups/ansible/ssh/latest/* /home/ansible/.ssh/
chown -R ansible: /home/ansible/.ssh && chmod 600 /home/ansible/.ssh/*

# 3. Clone project
git clone git@github.com:example/ansible-infrastructure.git /opt/ansible-project

# 4. Install dependencies
cd /opt/ansible-project
ansible-galaxy collection install -r requirements.yml -p ./collections/
ansible-galaxy role install -r requirements.yml

# 5. Verify
ansible all -i inventory/production/ -m ansible.builtin.ping
ansible-vault view group_vars/prod/vault.yml
```

### Restore AWX from Database Backup

```bash
# Kubernetes AWX operator
kubectl scale deployment awx-prod -n awx --replicas=0
kubectl exec -n awx awx-prod-postgres-0 -- \
  psql -U awx -d awx -f /tmp/awx-dump.sql
kubectl scale deployment awx-prod -n awx --replicas=1

# Re-import job templates if needed
awx import < awx-backup.json \
  --conf.host https://awx.example.com \
  --conf.token "$AWX_TOKEN"
```

## RTO / RPO

| Scenario | RTO | RPO | Method |
|---|---|---|---|
| Control node failure | 30 min | 0 (Git) | New VM + clone + restore SSH keys |
| Accidental playbook deletion | 5 min | 0 | `git checkout HEAD -- path/to/file` |
| Vault password lost | 1 hr | Last backup | Restore from HashiCorp Vault |
| AWX DB corruption | 2 hr | 24 hr | Restore PostgreSQL dump |
| Full site disaster | 4 hr | 24 hr | Provision new control node + AWX |

## Backup Validation

```bash
#!/bin/bash
# Run monthly to verify backup integrity
cd /opt/ansible-project

git ls-remote backup HEAD && echo "PASS: Git backup remote reachable"
test -f /backups/ansible/ssh/latest/ansible_ed25519 && echo "PASS: SSH key backup present"
ansible-vault view group_vars/prod/vault.yml > /dev/null && echo "PASS: Vault decryption OK"
test -f /backups/awx/awx-backup-$(date -d yesterday +%F).json && echo "PASS: AWX backup found"
```
