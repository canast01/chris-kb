---
tags:
  - ansible
  - security
---
# Ansible — Encryption

<div class="kb-summary">
Ansible encryption: `ansible-vault encrypt`, `encrypt_string`, vault ID configuration, KMS-backed vault password files, and in-transit SSH encryption settings.

*Applies to: Ansible 2.14+*
</div>

```d2
direction: down

ansible_vault: "Ansible Vault" {shape: rectangle}
tls_certificate_management: "TLS Certificate Management" {shape: rectangle}
ssh_transport_encryption: "SSH Transport Encryption" {shape: rectangle}
sensitive_task_output: "Sensitive Task Output" {shape: rectangle}
encryption_standards_summary: "Encryption Standards Summary" {shape: rectangle}

ansible_vault -> tls_certificate_management: hardens
tls_certificate_management -> ssh_transport_encryption: hardens
ssh_transport_encryption -> sensitive_task_output: hardens
sensitive_task_output -> encryption_standards_summary: hardens
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Ansible Vault

Ansible Vault encrypts sensitive data at rest using AES-256-CBC. Encrypted content lives alongside plaintext YAML in the same repository — safely committed to Git.

```d2
direction: right

plainSecret: "Plaintext Secret\n(password / API key" {shape: rectangle}
vaultEncrypt: "ansible-vault\nencrypt_string" {shape: rectangle}
vcKeyFile: "Vault Password File\n(~/.vault_pass" {shape: rectangle}
vaultFile: "vault.yml\n(encrypted at rest" {shape: rectangle}
mainYml: "group_vars/all/main.yml\n(references vault_ vars" {shape: rectangle}
playbook: "Playbook\n(uses db_password" {shape: rectangle}
managedHost: "Managed Host" {shape: rectangle}

plainSecret -> vaultEncrypt
vcKeyFile -> vaultEncrypt
vaultEncrypt -> vaultFile
vaultFile -> mainYml
mainYml -> playbook
vcKeyFile -> playbook
playbook -> managedHost
```

### Recommended Layout

```text
group_vars/
└── prod/
    ├── main.yml    # plaintext — references vault_ vars
    └── vault.yml   # encrypted — actual secret values
```

```yaml
# vault.yml (encrypted)
vault_db_password: "prod-db-pass"
vault_api_key: "sk-prod-abc123"

# main.yml (plaintext)
db_password: "{{ vault_db_password }}"
api_key: "{{ vault_api_key }}"
```

### Multiple Vault IDs

```bash
# Encrypt per environment
ansible-vault encrypt group_vars/prod/vault.yml --vault-id prod@~/.vault_pass_prod
ansible-vault encrypt group_vars/staging/vault.yml --vault-id staging@~/.vault_pass_staging

# Run with multiple IDs
ansible-playbook site.yml \
  --vault-id prod@~/.vault_pass_prod \
  --vault-id staging@~/.vault_pass_staging
```

### CI/CD Integration

| Method | How | When |
|---|---|---|
| File on runner | CI writes secret to temp file | Simple pipelines |
| Environment variable | `ANSIBLE_VAULT_PASSWORD_FILE` | CI with secret masking |
| Script | Fetches password from secrets manager at runtime | HashiCorp Vault / AWS Secrets Manager |

```yaml
# GitHub Actions
- name: Write vault password
  run: echo "${{ secrets.VAULT_PASSWORD }}" > ~/.vault_pass && chmod 600 ~/.vault_pass

- name: Run playbook
  run: ansible-playbook -i inventory/ site.yml
  env:
    ANSIBLE_VAULT_PASSWORD_FILE: ~/.vault_pass
```

## TLS Certificate Management

```yaml
- name: Generate ECC private key
  community.crypto.openssl_privatekey:
    path: /etc/ssl/private/app.key
    type: ECC
    curve: secp384r1
    mode: '0640'

- name: Generate CSR
  community.crypto.openssl_csr:
    path: /etc/ssl/csr/app.csr
    privatekey_path: /etc/ssl/private/app.key
    common_name: "{{ ansible_fqdn }}"
    subject_alt_name: "DNS:{{ ansible_fqdn }}"

- name: Deploy cert from HashiCorp Vault PKI
  community.hashi_vault.hashi_vault:
    path: pki/issue/web-role
    method: POST
    data:
      common_name: "{{ ansible_fqdn }}"
      ttl: "720h"
  register: vault_cert
  no_log: true

- name: Write certificate and key
  ansible.builtin.copy:
    content: "{{ item.content }}"
    dest: "{{ item.dest }}"
    mode: "{{ item.mode }}"
  loop:
    - content: "{{ vault_cert.data.data.certificate }}"
      dest: /etc/ssl/certs/app.crt
      mode: '0644'
    - content: "{{ vault_cert.data.data.private_key }}"
      dest: /etc/ssl/private/app.key
      mode: '0640'
  no_log: true
```

## SSH Transport Encryption

```ini
# ansible.cfg — enforce strong ciphers
[ssh_connection]
ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s \
           -o Ciphers=chacha20-poly1305@openssh.com,aes256-gcm@openssh.com \
           -o MACs=hmac-sha2-256-etm@openssh.com \
           -o KexAlgorithms=curve25519-sha256
```

## Sensitive Task Output

```yaml
# Suppress output for tasks handling secrets
- name: Set database password
  ansible.builtin.command:
    cmd: "mysql -u root -e \"ALTER USER 'app'@'%' IDENTIFIED BY '{{ db_password }}';\""
  no_log: true
  changed_when: true
```

## Encryption Standards Summary

| Data Category | Method |
|---|---|
| Secrets at rest (vars files) | Ansible Vault AES-256-CBC |
| SSH transport | Ed25519 keys + AES-256-GCM |
| WinRM transport | HTTPS TLS 1.2+ |
| TLS certificates | ECC P-384 or RSA 4096 |
| AWX credential storage | AES-256 (Django Fernet) |
| HashiCorp Vault secrets | AES-256-GCM (Transit engine) |

---

## See also

- [Ansible — Hardening](../hardening/)
- [Ansible — Authentication](../authentication/)
- [Ansible — Access Control](../access-control/)
