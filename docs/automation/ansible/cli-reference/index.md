# Ansible CLI Reference

Commonly used Ansible commands for running playbooks, managing inventory, and working with roles and vault.

---

## ansible (Ad-Hoc)

```bash
# Ping all hosts
ansible all -i inventory.ini -m ping

# Run shell command
ansible all -i inventory.ini -m shell -a "uptime"
ansible all -i inventory.ini -m command -a "hostname"

# Copy a file
ansible all -i inventory.ini -m copy -a "src=file.txt dest=/tmp/file.txt"

# Install package
ansible all -i inventory.ini -m package -a "name=curl state=present" --become

# Gather facts
ansible all -i inventory.ini -m setup
ansible all -i inventory.ini -m setup -a "filter=ansible_distribution*"

# Target specific groups or hosts
ansible webservers -i inventory.ini -m ping
ansible 'web*' -i inventory.ini -m ping
ansible 'all:!db' -i inventory.ini -m ping
```

---

## ansible-playbook

```bash
# Run a playbook
ansible-playbook playbook.yml
ansible-playbook -i inventory.ini playbook.yml

# Dry run (check mode)
ansible-playbook playbook.yml --check
ansible-playbook playbook.yml --check --diff

# Limit to specific hosts / groups
ansible-playbook playbook.yml --limit webservers
ansible-playbook playbook.yml --limit host1,host2

# Extra variables
ansible-playbook playbook.yml -e "env=prod"
ansible-playbook playbook.yml -e "@vars.yml"

# Tags
ansible-playbook playbook.yml --tags deploy
ansible-playbook playbook.yml --skip-tags cleanup
ansible-playbook playbook.yml --list-tags

# Step through tasks
ansible-playbook playbook.yml --step
ansible-playbook playbook.yml --start-at-task "task name"

# Verbosity
ansible-playbook playbook.yml -v
ansible-playbook playbook.yml -vvv

# Become / privilege escalation
ansible-playbook playbook.yml --become
ansible-playbook playbook.yml --become-user root

# List tasks / hosts
ansible-playbook playbook.yml --list-tasks
ansible-playbook playbook.yml --list-hosts
```

---

## ansible-inventory

```bash
# List all hosts
ansible-inventory -i inventory.ini --list
ansible-inventory -i inventory.ini --graph

# Show a host's vars
ansible-inventory -i inventory.ini --host <hostname>

# YAML output
ansible-inventory -i inventory.ini --list --yaml
```

---

## ansible-galaxy

```bash
# Install role
ansible-galaxy install <author>.<role>
ansible-galaxy install -r requirements.yml

# Install collection
ansible-galaxy collection install <namespace>.<collection>
ansible-galaxy collection install -r requirements.yml

# List installed roles / collections
ansible-galaxy list
ansible-galaxy collection list

# Init new role
ansible-galaxy init <role_name>

# Search
ansible-galaxy search <keyword>
ansible-galaxy role info <author>.<role>
```

---

## ansible-vault

```bash
# Create encrypted file
ansible-vault create secrets.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml

# Decrypt
ansible-vault decrypt secrets.yml

# View without decrypting to disk
ansible-vault view secrets.yml

# Edit in place
ansible-vault edit secrets.yml

# Encrypt a string inline
ansible-vault encrypt_string 'mysecret' --name 'db_password'

# Rekey (change password)
ansible-vault rekey secrets.yml

# Run playbook with vault
ansible-playbook playbook.yml --ask-vault-pass
ansible-playbook playbook.yml --vault-password-file ~/.vault_pass
```

---

## ansible-lint

```bash
# Lint a playbook
ansible-lint playbook.yml

# Lint a role
ansible-lint roles/myrole/

# List rules
ansible-lint --list-rules

# Skip specific rules
ansible-lint playbook.yml --skip-list rule-id-1,rule-id-2
```

---

## ansible-doc

```bash
# Show module documentation
ansible-doc copy
ansible-doc package
ansible-doc yum

# List all available modules
ansible-doc -l

# Filter by type
ansible-doc -t connection -l
ansible-doc -t lookup -l
```

---

## ansible-config

```bash
# Show current config
ansible-config view
ansible-config dump

# Show non-default settings
ansible-config dump --only-changed

# List all config options
ansible-config list
```

---

## Common Patterns

```bash
# Test connectivity before running
ansible all -m ping && ansible-playbook site.yml

# Run with SSH key
ansible-playbook playbook.yml --private-key ~/.ssh/id_ed25519

# Use specific user
ansible-playbook playbook.yml -u admin

# Force fact gathering
ansible-playbook playbook.yml --force-handlers

# Serial execution (rolling)
# In playbook: serial: 1 or serial: "25%"

# Forks (parallel tasks)
ansible-playbook playbook.yml -f 20
```
