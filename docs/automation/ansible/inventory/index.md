# Ansible Inventory

## INI Format Inventory

The simplest inventory format uses INI-style grouping with hosts and optional inline variables.

```ini
# inventory/hosts.ini

[webservers]
web01.example.com
web02.example.com ansible_port=2222

[dbservers]
db01.example.com ansible_user=admin
db02.example.com

[production:children]
webservers
dbservers

[webservers:vars]
http_port=80
nginx_version=1.24
```

## YAML Format Inventory

YAML inventory is more expressive and suits complex nested group hierarchies.

```yaml
# inventory/hosts.yml
all:
  children:
    webservers:
      hosts:
        web01.example.com:
          ansible_port: 22
        web02.example.com:
          ansible_port: 2222
      vars:
        http_port: 80
    dbservers:
      hosts:
        db01.example.com:
          ansible_user: admin
        db02.example.com:
      vars:
        db_port: 5432
```

## Dynamic Inventory

Dynamic inventory plugins pull host data from external sources at runtime.

```bash
# Install the AWS collection
ansible-galaxy collection install amazon.aws

# Preview dynamic inventory output
ansible-inventory -i inventory/aws_ec2.yml --list

# Show as tree
ansible-inventory -i inventory/aws_ec2.yml --graph

# Run playbook against dynamic inventory
ansible-playbook -i inventory/aws_ec2.yml site.yml
```

```yaml
# inventory/aws_ec2.yml
plugin: amazon.aws.aws_ec2
regions:
  - eu-west-1
filters:
  instance-state-name: running
  tag:Environment: production
keyed_groups:
  - key: tags.Role
    prefix: role
hostnames:
  - private-ip-address
```

## host_vars and group_vars

Variable files scoped to individual hosts or groups, loaded automatically by Ansible.

```bash
# Recommended directory layout
inventory/
  hosts.yml
  host_vars/
    web01.example.com/
      main.yml        # host-specific vars
      vault.yml       # encrypted secrets
  group_vars/
    webservers/
      main.yml        # applied to all webservers
      vault.yml       # encrypted group secrets
    all/
      main.yml        # applied to every host
```

```yaml
# inventory/group_vars/webservers/main.yml
nginx_worker_processes: auto
nginx_keepalive_timeout: 65
ssl_certificate: /etc/ssl/certs/web.crt
```

## Grouping Strategies

| Pattern | Syntax example | Purpose |
|---|---|---|
| Static group | `[webservers]` | Manually listed hosts |
| Child group | `[prod:children]` | Group that contains other groups |
| Inline group vars | `[web:vars]` | Variables applied to group |
| Range expansion | `web[01:05]` | Generates web01 through web05 |
| Regex match | `~web\d+\.example\.com` | Pattern-matched host names |

## Inventory Commands

```bash
# List all hosts
ansible-inventory -i inventory/ --list

# Show tree structure
ansible-inventory -i inventory/ --graph

# Test connectivity for all hosts
ansible -i inventory/ all -m ping

# Run ad-hoc command on a group
ansible -i inventory/ webservers -m shell -a "uptime"

# Inspect variables for one host
ansible-inventory -i inventory/ --host web01.example.com

# Check which groups a host belongs to
ansible -i inventory/ --list-hosts webservers
```
