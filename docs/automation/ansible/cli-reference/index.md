# Ansible CLI Reference

Ansible is an agentless automation tool — it connects to remote hosts over SSH and runs tasks defined in YAML playbooks. There's nothing to install on the managed hosts. The control node (where you run `ansible` and `ansible-playbook`) needs Python and the Ansible package.

> Install with `pip install ansible` or your distro's package manager. Requires SSH access to managed hosts and a valid inventory file.

---

## ansible (Ad-Hoc)

Run a single module directly against hosts without writing a playbook. Useful for quick checks, one-off operations, and testing connectivity before running a full playbook.

```bash
# Test SSH connectivity and Python availability
ansible all -i inventory.ini -m ping

# Run a shell command on all hosts
ansible all -i inventory.ini -m shell -a "uptime"
ansible all -i inventory.ini -m command -a "hostname"

# Copy a file to all hosts
ansible all -i inventory.ini -m copy -a "src=file.txt dest=/tmp/file.txt"

# Install a package (requires privilege escalation)
ansible all -i inventory.ini -m package -a "name=curl state=present" --become

# Gather facts (system info) from all hosts
ansible all -i inventory.ini -m setup
ansible all -i inventory.ini -m setup -a "filter=ansible_distribution*"

# Target specific groups or hosts
ansible webservers -i inventory.ini -m ping
ansible 'web*' -i inventory.ini -m ping         # wildcard host pattern
ansible 'all:!db' -i inventory.ini -m ping      # all except db group
```

---

## ansible-playbook

Run a playbook against an inventory. Playbooks are YAML files that define a sequence of tasks. Use check mode to preview changes before applying them.

```bash
# Run a playbook
ansible-playbook playbook.yml
ansible-playbook -i inventory.ini playbook.yml

# Dry run (check mode — no changes made)
ansible-playbook playbook.yml --check
ansible-playbook playbook.yml --check --diff    # also show what would change

# Limit to specific hosts or groups
ansible-playbook playbook.yml --limit webservers
ansible-playbook playbook.yml --limit host1,host2

# Pass extra variables
ansible-playbook playbook.yml -e "env=prod"
ansible-playbook playbook.yml -e "@vars.yml"    # from a file

# Tags (run or skip specific tasks)
ansible-playbook playbook.yml --tags deploy
ansible-playbook playbook.yml --skip-tags cleanup
ansible-playbook playbook.yml --list-tags

# Step-by-step execution
ansible-playbook playbook.yml --step
ansible-playbook playbook.yml --start-at-task "task name"

# Verbosity (add more -v for more detail)
ansible-playbook playbook.yml -v
ansible-playbook playbook.yml -vvv

# Privilege escalation
ansible-playbook playbook.yml --become
ansible-playbook playbook.yml --become-user root

# List tasks and hosts without running
ansible-playbook playbook.yml --list-tasks
ansible-playbook playbook.yml --list-hosts
```

---

## ansible-inventory

Inspect your inventory — list all hosts, view group membership, and show variables assigned to specific hosts. Essential for debugging inventory plugin configurations.

```bash
# List all hosts and groups in JSON
ansible-inventory -i inventory.ini --list

# Tree view of groups and hosts
ansible-inventory -i inventory.ini --graph

# Show all variables for a specific host
ansible-inventory -i inventory.ini --host <hostname>

# YAML output (easier to read than JSON)
ansible-inventory -i inventory.ini --list --yaml
```

---

## ansible-galaxy

Install and manage roles and collections from Ansible Galaxy (the community hub) or private Automation Hub. Roles are reusable task collections; collections package roles, modules, and plugins together.

```bash
# Install a role
ansible-galaxy install <author>.<role>
ansible-galaxy install -r requirements.yml         # from a requirements file

# Install a collection
ansible-galaxy collection install <namespace>.<collection>
ansible-galaxy collection install -r requirements.yml

# List installed roles and collections
ansible-galaxy list
ansible-galaxy collection list

# Create a new role skeleton
ansible-galaxy init <role_name>

# Search and get info
ansible-galaxy search <keyword>
ansible-galaxy role info <author>.<role>
```

---

## ansible-vault

Encrypt sensitive data (passwords, API keys, certificates) in playbooks and variable files. Vault-encrypted content can be stored safely in version control.

```bash
# Create a new encrypted file
ansible-vault create secrets.yml

# Encrypt an existing file
ansible-vault encrypt secrets.yml

# Decrypt (produces plaintext on disk)
ansible-vault decrypt secrets.yml

# View without decrypting to disk
ansible-vault view secrets.yml

# Edit in place (opens editor, saves encrypted)
ansible-vault edit secrets.yml

# Encrypt a single string (for embedding in YAML)
ansible-vault encrypt_string 'mysecret' --name 'db_password'

# Change the vault password
ansible-vault rekey secrets.yml

# Run a playbook that uses vault-encrypted files
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```

---

## Tools, Lint & Config

Supporting tools for code quality, documentation, and configuration inspection.

### ansible-lint

Checks playbooks and roles for best-practice violations and common mistakes. Run before committing playbook changes.

```bash
ansible-lint playbook.yml
ansible-lint roles/myrole/
ansible-lint --list-rules
ansible-lint playbook.yml --skip-list rule-id-1,rule-id-2
```

### ansible-doc

Browse built-in module documentation from the command line — no browser needed.

```bash
ansible-doc copy
ansible-doc package
ansible-doc yum
ansible-doc -l                  # list all available modules
ansible-doc -t connection -l    # list connection plugins
ansible-doc -t lookup -l        # list lookup plugins
```

### ansible-config

Inspect Ansible's effective configuration — useful when troubleshooting unexpected behavior.

```bash
ansible-config view                  # show config file in use
ansible-config dump                  # show all settings and their values
ansible-config dump --only-changed   # show only non-default settings
ansible-config list                  # list all config options with descriptions
```

### Common Patterns

```bash
# Test connectivity before running
ansible all -m ping && ansible-playbook site.yml

# Run with a specific SSH key
ansible-playbook playbook.yml --private-key ~/.ssh/id_ed25519

# Use a specific remote user
ansible-playbook playbook.yml -u admin

# Parallel execution (default is 5 forks)
ansible-playbook playbook.yml -f 20

# CI/CD pattern
ansible-playbook playbook.yml \
  -i inventory.ini \
  --vault-password-file ~/.vault_pass \
  --check --diff
```
