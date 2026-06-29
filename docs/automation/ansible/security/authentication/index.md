---
tags:
  - ansible
  - security
---
# Ansible — Authentication

```bash
# ED25519 — preferred (faster, smaller, equally secure)
ssh-keygen -t ed25519 -C "ansible-control@prod" -f ~/.ssh/ansible_ed25519 -N ""

# RSA 4096 — for legacy systems that don't support Ed25519
ssh-keygen -t rsa -b 4096 -C "ansible-control@prod" -f ~/.ssh/ansible_rsa -N ""
```


```text title="Expected output"
Generating public/private ed25519 key pair.
Your identification has been saved in /home/ansible/.ssh/ansible_ed25519
Your public key has been saved in /home/ansible/.ssh/ansible_ed25519.pub
The key fingerprint is:
SHA256:7mK9pL2qR8vN3xJ5wB1cD4eF6gH9iK0lM2nO4pQ5rS ansible-control@prod
The key's randomart image is:
+--[ED25519 256]--+
|        .o.      |
|       o.o .     |
|      . o + .    |
|       . B o     |
|        S * .    |
+----[SHA256]-----+
Generating public/private rsa key pair.
Your identification has been saved in /home/ansible/.ssh/ansible_rsa
Your public key has been saved in /home/ansible/.ssh/ansible_rsa.pub
The key fingerprint is:
SHA256:4aB9cD2eF5gH8iJ1kL3mN6oP9qR2sT5uV7wX0yZ3aB ansible-control@prod
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Ensure the public key is added to `~/.ssh/authorized_keys` on target hosts with correct permissions (644 for the file, 700 for ~/.ssh directory).
    **`Permissions 0644 for '/home/ansible/.ssh/ansible_ed25519' are too open.`** — Run `chmod 600 ~/.ssh/ansible_ed25519` to restrict private key permissions to the owner only.
```bash
pip install pywinrm[kerberos]   # domain-joined hosts
pip install pywinrm              # NTLM / basic
```
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
```bash
awx users create \
  --username breakglass-admin \
  --password "$BREAKGLASS_PASS" \
  --is_superuser true \
  --conf.host https://awx.example.com \
  --conf.token "$AWX_TOKEN"
```

```text title="Expected output"
id: 42
username: breakglass-admin
first_name: 
last_name: 
email: 
is_active: true
is_staff: false
is_superuser: true
last_login: null
date_joined: 2024-01-15T09:47:22.341829Z
ldap_dn: 
created: 2024-01-15T09:47:22.341829Z
modified: 2024-01-15T09:47:22.341829Z
```

!!! warning "Common errors"
    **`Error: The provided token is invalid or expired`** — Regenerate the AWX API token using `awx login` or create a new token in the AWX web UI under User Settings > Tokens.
    **`Error: Failed to connect to https://awx.example.com`** — Verify the AWX host is reachable and correct the `--conf.host` URL; check network connectivity and DNS resolution.
    **`Error: username already exists`** — Choose a different username or delete the existing user with `awx users delete --username breakglass-admin` before recreating.
```bash
echo "vault-password-here" > ~/.ansible_vault_pass
chmod 600 ~/.ansible_vault_pass
```
```ini
# ansible.cfg
[defaults]
vault_password_file = ~/.ansible_vault_pass
```
```bash
#!/bin/bash
vault kv get -field=password secret/ansible/vault-password
```
```ini
[defaults]
vault_password_file = ~/.get_vault_pass.sh
```
```bash
ansible-playbook site.yml \
  --vault-id prod@~/.vault_pass_prod \
  --vault-id staging@~/.vault_pass_staging
```

```text title="Expected output"
[WARNING]: Ansible is being run in a world writable directory (/home/admin/playbooks), ignoring it as an unsafe location.
[WARNING]: Unable to parse /etc/ansible/hosts as an YAML file: Expecting value: line 1 column 1 (char 0)

PLAY [all] *********************************************************************

TASK [Gathering Facts] *********************************************************
ok: [web-prod-01.example.com]
ok: [web-staging-01.example.com]
ok: [db-prod-01.example.com]

PLAY RECAP *********************************************************************
web-prod-01.example.com        : ok=12   changed=3    unreachable=0    failed=0
web-staging-01.example.com     : ok=11   changed=2    unreachable=0    failed=0
db-prod-01.example.com         : ok=10   changed=2    unreachable=0    failed=0
```

!!! warning "Common errors"
    **`ERROR! Vault password file /home/admin/.vault_pass_prod is not readable by the current user`** — Ensure the vault password file exists and has read permissions (chmod 600 ~/.vault_pass_prod).
    **`ERROR! Decryption failed (no vault secrets were found that could decrypt)`** — Verify the vault ID label matches the encrypted variable in the playbook and the correct password file is being used.
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

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "User / Service" as USR
participant "Ansible" as SVC
participant "Identity Provider\n(LDAP / OIDC / AD)" as IDP
participant "Token / Session Store" as TOKEN

USR -> SVC: Authentication request
SVC -> IDP: Validate credentials
IDP --> SVC: Identity confirmed
SVC -> TOKEN: Issue session token
TOKEN --> SVC: Token granted
SVC --> USR: Access allowed

@enduml
```

## Before you begin

- **Access:** SSH key or service account with sudo on managed hosts; Ansible control node
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Ansible — Access Control](../access-control/)
- [Ansible — Hardening](../hardening/)
- [Ansible — Encryption](../encryption/)
