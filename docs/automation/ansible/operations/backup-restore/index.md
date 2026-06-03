```bash
# Ensure remote is current
git push origin main
git push origin --tags

# Mirror to secondary backup remote
git remote add backup git@backup-gitlab.example.com:ansible/infrastructure.git
git push backup --mirror
```

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
```bash
# On the AWX/AAP server
awx-manage dumpdata --natural-foreign --natural-primary \
  -e sessions -e admin \
  > /tmp/awx-dump-$(date +%F).json

scp /tmp/awx-dump-$(date +%F).json backup-server:/backups/awx/
```
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
```bash
# Push secrets to HashiCorp Vault
ansible-vault view group_vars/prod/vault.yml | \
  while IFS=': ' read -r key value; do
    vault kv put secret/ansible/prod/$key value="$value"
  done
```
```bash
# Generate new password file
openssl rand -base64 32 > ~/.ansible_vault_pass_new

# Rekey all vault files
find . -name "vault.yml" -exec ansible-vault rekey \
  --new-vault-password-file ~/.ansible_vault_pass_new {} \;

mv ~/.ansible_vault_pass_new ~/.ansible_vault_pass
```
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
```bash
#!/bin/bash
# Run monthly to verify backup integrity
cd /opt/ansible-project

git ls-remote backup HEAD && echo "PASS: Git backup remote reachable"
test -f /backups/ansible/ssh/latest/ansible_ed25519 && echo "PASS: SSH key backup present"
ansible-vault view group_vars/prod/vault.yml > /dev/null && echo "PASS: Vault decryption OK"
test -f /backups/awx/awx-backup-$(date -d yesterday +%F).json && echo "PASS: AWX backup found"
```
