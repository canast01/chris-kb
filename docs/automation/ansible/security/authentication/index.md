# Ansible — Authentication


<div class="kb-summary">
> Part of the [Ansible Security](../index.md) reference.
</div>

## SSH Authentication (Linux Targets)

SSH with public key authentication is the default and recommended transport for Linux managed nodes.

### Key Generation

```bash
# ED25519 — preferred (faster, smaller, equally secure)
ssh-keygen -t ed25519 -C "ansible-control@prod" -f ~/.ssh/ansible_ed25519 -N ""

# RSA 4096 — for legacy systems that don't support Ed25519
ssh-keygen -t rsa -b 4096 -C "ansible-control@prod" -f ~/.ssh/ansible_rsa -N ""
```
┌────────────────────────────────────── Ansible — Authentication ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible uses SSH key authentication for Linux targets and WinRM/Kerberos for Windows targets │   │
│   │  Service account per environment: ansible-prod, ansible-dev — no shared personal credentials  │   │
│   │AWX stores credentials encrypted (AES-256); injected at runtime — never written to disk on host│   │
│   │         AWX login: LDAP/AD or SAML SSO; local accounts only for break-glass scenarios         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Linux (SSH)                  │  │               Windows (WinRM)               │   │
│   │         SSH private key in AWX cred          │  │        Kerberos (domain-joined hosts)       │   │
│   │         Service account on each host         │  │         NTLM fallback for workgroup         │   │
│   │         Strict host key checking on          │  │           WinRM HTTPS (port 5986)           │   │
│   │      Rotate annually or on staff change      │  │      ansible_winrm_transport: kerberos      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ WinRM          = Windows Remote Management; Microsoft implementation of WS-Management protocol│   │
│   │      Kerberos    = network auth protocol; Windows domain auth; requires domain membership     │   │
│   │   SSH agent      = key agent; AWX injects private key into SSH agent process at job runtime   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Ansible — Authentication ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Ansible uses SSH key authentication for Linux targets and WinRM/Kerberos for Windows targets │   │
│   │  Service account per environment: ansible-prod, ansible-dev — no shared personal credentials  │   │
│   │AWX stores credentials encrypted (AES-256); injected at runtime — never written to disk on host│   │
│   │         AWX login: LDAP/AD or SAML SSO; local accounts only for break-glass scenarios         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Linux (SSH)                  │  │               Windows (WinRM)               │   │
│   │         SSH private key in AWX cred          │  │        Kerberos (domain-joined hosts)       │   │
│   │         Service account on each host         │  │         NTLM fallback for workgroup         │   │
│   │         Strict host key checking on          │  │           WinRM HTTPS (port 5986)           │   │
│   │      Rotate annually or on staff change      │  │      ansible_winrm_transport: kerberos      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ WinRM          = Windows Remote Management; Microsoft implementation of WS-Management protocol│   │
│   │      Kerberos    = network auth protocol; Windows domain auth; requires domain membership     │   │
│   │   SSH agent      = key agent; AWX injects private key into SSH agent process at job runtime   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## WinRM Authentication (Windows Targets)

```bash
pip install pywinrm[kerberos]   # domain-joined hosts
pip install pywinrm              # NTLM / basic
```

| Transport | Use Case | Security |
|---|---|---|
| `kerberos` | Domain-joined hosts | Strong — no credential on wire |
| `ntlm` | Workgroup / non-domain | Acceptable with HTTPS |
| `certificate` | Service accounts | Strong — no password |
| `basic` | Lab only | Weak — avoid in production |

```yaml
# group_vars/windows/main.yml
ansible_connection: winrm
ansible_winrm_transport: kerberos
ansible_winrm_scheme: https
ansible_winrm_server_cert_validation: validate
ansible_port: 5986
```

```bash
# Get Kerberos ticket before running playbook
kinit svc-ansible@EXAMPLE.COM
ansible -i inventory/ windows_hosts -m ansible.windows.win_ping
```

## AWX / AAP Authentication

### LDAP / Active Directory

```yaml
# AWX Settings → Authentication → LDAP
LDAP Server URI: ldaps://dc01.example.com:636
LDAP Bind DN: CN=svc-awx-ldap,OU=ServiceAccounts,DC=example,DC=com
LDAP Bind Password: <vault secret>
LDAP User Search:
  - OU=Users,DC=example,DC=com
  - SCOPE_SUBTREE
  - (sAMAccountName=%(user)s)
LDAP Group Search:
  - OU=Groups,DC=example,DC=com
  - SCOPE_SUBTREE
  - (objectClass=group)
LDAP User Attribute Map:
  first_name: givenName
  last_name: sn
  email: mail
LDAP Organization Map:
  IT Infrastructure:
    admins: CN=AWX-Admins,OU=Groups,DC=example,DC=com
    users: CN=AWX-Users,OU=Groups,DC=example,DC=com
```

### SAML SSO (Okta / Azure AD)

```yaml
# AWX Settings → Authentication → SAML
SAML Service Provider Entity ID: https://awx.example.com/sso/metadata/saml/
SAML IdP URL: https://example.okta.com/app/ansible/sso/saml
SAML ACS URL: https://awx.example.com/sso/complete/saml/
SAML Organization Attribute Mapping:
  IT Infra:
    admins: ["awx-admins"]
    users: ["awx-users"]
```

### Local Break-glass Account

```bash
awx users create \
  --username breakglass-admin \
  --password "$BREAKGLASS_PASS" \
  --is_superuser true \
  --conf.host https://awx.example.com \
  --conf.token "$AWX_TOKEN"
```

## Vault Authentication for Secrets

### Password File

```bash
echo "vault-password-here" > ~/.ansible_vault_pass
chmod 600 ~/.ansible_vault_pass
```

```ini
# ansible.cfg
[defaults]
vault_password_file = ~/.ansible_vault_pass
```

### Vault Password Script (from HashiCorp Vault)

```bash
#!/bin/bash
vault kv get -field=password secret/ansible/vault-password
```

```ini
[defaults]
vault_password_file = ~/.get_vault_pass.sh
```

### Multiple Vault IDs

```bash
ansible-playbook site.yml \
  --vault-id prod@~/.vault_pass_prod \
  --vault-id staging@~/.vault_pass_staging
```

## HashiCorp Vault — AppRole Auth

```bash
vault auth enable approle
vault write auth/approle/role/ansible \
  token_policies="ansible-policy" \
  secret_id_ttl=24h \
  token_ttl=1h

ROLE_ID=$(vault read -field=role_id auth/approle/role/ansible/role-id)
SECRET_ID=$(vault write -field=secret_id -f auth/approle/role/ansible/secret-id)
export VAULT_ROLE_ID="$ROLE_ID"
export VAULT_SECRET_ID="$SECRET_ID"
```

```yaml
vars:
  db_password: "{{ lookup('community.hashi_vault.hashi_vault',
    'secret/data/prod/db:password',
    auth_method='approle',
    role_id=lookup('env','VAULT_ROLE_ID'),
    secret_id=lookup('env','VAULT_SECRET_ID')) }}"
```

## SSH Bastion / Jump Host

```ini
[ssh_connection]
ssh_args = -C -o ControlMaster=auto -o ControlPersist=60s \
           -o ProxyJump=bastion.example.com
```

```yaml
# host_vars/web01.prod.example.com/main.yml
ansible_ssh_common_args: >-
  -o ProxyJump=bastion.example.com
  -o StrictHostKeyChecking=yes
```
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
