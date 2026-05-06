# ansible-inventory

> Part of the [Ansible CLI Reference](../).

---

```bash
# List all hosts
ansible-inventory -i inventory.ini --list
ansible-inventory -i inventory.ini --graph

# Show a host's vars
ansible-inventory -i inventory.ini --host <hostname>

# YAML output
ansible-inventory -i inventory.ini --list --yaml
```
