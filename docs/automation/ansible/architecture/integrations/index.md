# Ansible — Integrations


<div class="kb-summary">
> Part of the [Ansible Architecture](../index.md) reference.
</div>

## VMware vSphere

The `community.vmware` collection automates vSphere, ESXi, vCenter, vSAN, and NSX-T.

```bash
ansible-galaxy collection install community.vmware
pip install PyVmomi vsphere-automation-sdk-python
```
```text
┌─────────────────────────────────────── Ansible — Integrations ────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Ansible integrates with CI/CD pipelines, secrets managers, ITSM tools, and cloud platforms  │   │
│   │  AWX REST API is the primary integration point for triggering playbooks from external systems │   │
│   │   Dynamic inventory plugins connect to AWS, vSphere, Netbox, GCP, Azure for live host lists   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            CI/CD            │  │           Secrets           │  │      Inventory Sources      │   │
│   │     GitHub Actions → AWX    │  │       HashiCorp Vault       │  │        AWS EC2 plugin       │   │
│   │     GitLab CI → AWX API     │  │         CyberArk PAM        │  │        VMware vSphere       │   │
│   │    Jenkins → AWX webhook    │  │     AWX credential types    │  │        Netbox plugin        │   │
│   │   Webhook triggers in AWX   │  │    Ansible Vault (static)   │  │       OpenStack plugin      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Dynamic inventory = script or plugin that queries an external source for host lists at runtime│   │
│   │ Webhook trigger   = AWX can receive HTTP webhooks from GitHub/GitLab to auto-run job templates│   │
│   │         Credential type = AWX pluggable credential; SSH keys, API tokens, Vault tokens        │   │
│   │   Netbox            = open-source DCIM/IPAM; Ansible inventory plugin pulls live device list  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

## HashiCorp Vault

```bash
ansible-galaxy collection install community.hashi_vault
pip install hvac
```

```yaml
vars:
  db_password: "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/prod/db:password') }}"
  api_token:   "{{ lookup('community.hashi_vault.hashi_vault', 'secret/data/api:token') }}"
```

!!! tip "Prefer Vault over Ansible Vault for enterprise"
    HashiCorp Vault provides dynamic secrets, audit logs, lease expiry, and fine-grained policies. For production environments with many teams, it scales better than static Ansible Vault files.

## GitHub Actions / Jenkins

```yaml
# .github/workflows/deploy.yml
- name: Run Ansible playbook
  run: |
    ansible-playbook -i inventory/prod/ site.yml \
      --extra-vars "version=${{ github.sha }}"
  env:
    ANSIBLE_HOST_KEY_CHECKING: "False"
    ANSIBLE_VAULT_PASSWORD_FILE: ~/.vault_pass
```

```groovy
// Jenkins Pipeline
withCredentials([sshUserPrivateKey(credentialsId: 'ansible-key', keyFileVariable: 'KEY')]) {
  sh "ansible-playbook -i inventory/prod/ site.yml --private-key $KEY"
}
```

## ServiceNow ITSM

```bash
ansible-galaxy collection install servicenow.itsm
```

```yaml
- name: Open change request
  servicenow.itsm.change_request:
    instance:
      host: https://example.service-now.com
      username: "{{ snow_user }}"
      password: "{{ snow_password }}"
    state: new
    type: standard
    short_description: "Automated patching — {{ ansible_date_time.date }}"
    assignment_group: "Linux Operations"
  register: change_request

- name: Close change request
  servicenow.itsm.change_request:
    instance:
      host: https://example.service-now.com
      username: "{{ snow_user }}"
      password: "{{ snow_password }}"
    sys_id: "{{ change_request.record.sys_id }}"
    state: closed
    close_code: successful
    close_notes: "Completed successfully"
```

## Network Devices — Cisco / Arista / Juniper

```ini
# inventory
[ios_routers]
router01 ansible_host=10.0.0.1 ansible_network_os=cisco.ios.ios ansible_connection=network_cli

[eos_switches]
switch01 ansible_host=10.0.1.1 ansible_network_os=arista.eos.eos ansible_connection=httpapi ansible_httpapi_use_ssl=true
```

```yaml
- name: Backup IOS running config
  cisco.ios.ios_config:
    backup: true
    backup_options:
      dir_path: /srv/ansible/network-backups/
      filename: "{{ inventory_hostname }}-{{ ansible_date_time.date }}.cfg"
```

## Windows Active Directory

```yaml
- name: Create AD computer object
  community.windows.win_domain_computer:
    name: "{{ inventory_hostname_short }}"
    dns_hostname: "{{ ansible_fqdn }}"
    ou: "OU=Servers,DC=example,DC=com"
    state: present
  delegate_to: dc01.example.com

- name: Join Linux host to AD
  ansible.builtin.command:
    cmd: "realm join --user={{ ad_join_user }} {{ ad_domain }}"
  environment:
    PASSWD: "{{ ad_join_password }}"
  no_log: true
```

## Monitoring — Prometheus / Nagios

```yaml
- name: Schedule Nagios downtime before maintenance
  community.general.nagios:
    action: downtime
    start: "{{ ansible_date_time.epoch }}"
    minutes: 60
    host: "{{ inventory_hostname }}"
    services: all
    author: ansible
    comment: "Automated maintenance window"
```

## Integration Matrix

| Platform | Collection | Auth Method |
|---|---|---|
| VMware vSphere | `community.vmware` | Username/password or session token |
| AWS | `amazon.aws` | IAM role / access keys |
| Azure | `azure.azcollection` | Service principal / managed identity |
| HashiCorp Vault | `community.hashi_vault` | AppRole / Kubernetes / LDAP |
| ServiceNow | `servicenow.itsm` | Basic auth / OAuth |
| Cisco IOS | `cisco.ios` | SSH / enable password |
| Arista EOS | `arista.eos` | HTTPS API |
| Juniper JunOS | `junipernetworks.junos` | SSH / NETCONF |
| Windows AD | `community.windows` | WinRM / Kerberos |
