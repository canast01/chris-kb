# File System & Quotas

> Part of the Dell PowerScale (Isilon) CLI Reference.
---

## File System — Directories

```bash
# Browse
ls /ifs/
ls -la /ifs/<path>

# Directory info
isi get /ifs/<path>
isi get -D /ifs/<path>

# Create directory
mkdir -p /ifs/<path>

# Permissions
chmod 755 /ifs/<path>
chown <user>:<group> /ifs/<path>
isi get -a /ifs/<path>
```

## Quotas

```bash
# List quotas
isi quota quotas list
isi quota quotas list --type directory
isi quota quotas list --path /ifs/<path>

# View quota details
isi quota quotas view --path /ifs/<path> --type directory

# Create quota
isi quota quotas create /ifs/<path> directory --hard-threshold <size>G --soft-threshold <size>G --advisory-threshold <size>G

# Modify quota
isi quota quotas modify --path /ifs/<path> --type directory --hard-threshold <size>G

# Delete quota
isi quota quotas delete --path /ifs/<path> --type directory

# Quota reports
isi quota reports list
isi quota reports create
```
