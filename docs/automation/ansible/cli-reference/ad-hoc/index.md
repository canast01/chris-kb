# ansible (Ad-Hoc)

> Part of the [Ansible CLI Reference](../).

---

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
