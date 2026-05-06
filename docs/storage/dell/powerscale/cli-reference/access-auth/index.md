# Access Zones & Authentication

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

## Access Zones

```bash
# List zones
isi zone zones list
isi zone zones view <zone_name>

# Create / delete zone
isi zone zones create <zone_name> --path /ifs/<path>
isi zone zones delete <zone_name>

# Modify zone
isi zone zones modify <zone_name> --add-auth-providers <provider>
```

## Authentication & Users

```bash
# Auth providers
isi auth providers list
isi auth providers ad list
isi auth providers ad view <provider_name>

# Join AD domain
isi auth ads create --name <domain> --user <admin_user> --password <password>

# Local users and groups
isi auth users list
isi auth users view <username>
isi auth users create --name <username> --password <password>
isi auth users delete <username>
isi auth groups list
isi auth groups view <group_name>

# Map rules
isi auth mappings rules list
```
