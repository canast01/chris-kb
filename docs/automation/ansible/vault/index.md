# Ansible Vault

## Encrypting Files and Values

Vault encrypts sensitive data at rest. Any YAML file or string value can be encrypted.

```bash
# Encrypt a new file (opens editor)
ansible-vault create secrets.yml

# Encrypt an existing plaintext file
ansible-vault encrypt group_vars/all/vault.yml

# Decrypt to plaintext (use with care)
ansible-vault decrypt group_vars/all/vault.yml

# View encrypted file without decrypting on disk
ansible-vault view group_vars/all/vault.yml

# Edit encrypted file in place
ansible-vault edit group_vars/all/vault.yml

# Re-encrypt with a new password
ansible-vault rekey group_vars/all/vault.yml
```

## Vault IDs and Multiple Passwords

Vault IDs let you use different passwords for different secrets within the same project.

```bash
# Create a vault with a named ID
ansible-vault create --vault-id dev@prompt secrets/dev.yml
ansible-vault create --vault-id prod@~/.vault_pass_prod secrets/prod.yml

# Run playbook supplying multiple vault passwords
ansible-playbook site.yml \
  --vault-id dev@prompt \
  --vault-id prod@~/.vault_pass_prod

# Store password in a file (restrict permissions)
echo "mysecretpassword" > ~/.vault_pass
chmod 600 ~/.vault_pass

# Reference password file in ansible.cfg
# [defaults]
# vault_password_file = ~/.vault_pass
```

## Inline Encrypted Strings

Encrypt individual values to embed directly in plaintext YAML files.

```bash
# Generate an encrypted inline string
ansible-vault encrypt_string 'db_password_value' \
  --name 'vault_db_password' \
  --vault-id prod@~/.vault_pass_prod
```

This outputs a block you paste directly into a vars file:

```yaml
# group_vars/all/main.yml
vault_db_password: !vault |
  $ANSIBLE_VAULT;1.2;AES256;prod
  33626536396435663839316562313065353933303664663134303863633266643263
  ...
```

## Vault in CI/CD Integration

| Method | How it works | When to use |
|---|---|---|
| File on runner | Password file written by CI secret | Simple pipelines |
| Environment variable | `ANSIBLE_VAULT_PASSWORD_FILE` or `ANSIBLE_VAULT_IDENTITY_LIST` | CI with secret masking |
| Vault ID with script | Custom script fetches password from secrets manager | HashiCorp Vault / AWS Secrets Manager |

```yaml
# GitHub Actions example
- name: Write vault password
  run: echo "${{ secrets.VAULT_PASSWORD }}" > ~/.vault_pass && chmod 600 ~/.vault_pass

- name: Run playbook
  run: ansible-playbook -i inventory/ site.yml
  env:
    ANSIBLE_VAULT_PASSWORD_FILE: ~/.vault_pass
```

## Recommended Vault File Layout

```bash
group_vars/
  all/
    main.yml        # plaintext — references vault_ prefixed vars
    vault.yml       # encrypted — stores vault_ prefixed values
  webservers/
    main.yml
    vault.yml
host_vars/
  db01.example.com/
    main.yml
    vault.yml       # host-specific secrets
```

```yaml
# Plaintext main.yml references vault values by convention
db_password: "{{ vault_db_password }}"
api_key:     "{{ vault_api_key }}"

# Encrypted vault.yml holds the real values
vault_db_password: "realpassword123"
vault_api_key:     "abc-xyz-456"
```

## Common Vault Commands Quick Reference

```bash
# Decrypt and show a vault file
ansible-vault view group_vars/all/vault.yml --vault-id @prompt

# Check if a file is encrypted
head -1 group_vars/all/vault.yml
# Should start with: $ANSIBLE_VAULT;1.1;AES256

# Run playbook and prompt for vault password
ansible-playbook site.yml --ask-vault-pass

# Run with password file
ansible-playbook site.yml --vault-password-file ~/.vault_pass
```
