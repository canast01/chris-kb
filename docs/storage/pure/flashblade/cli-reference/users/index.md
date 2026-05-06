# Users & Authentication

> Part of the [Pure FlashBlade CLI Reference](../).

---

## Users & Authentication

```bash
# Admin users
purefb admin show
purefb admin create --name <user> --role array_admin
purefb admin update --name <user> --password <pass>

# API tokens
purefb api-client show
purefb api-client create --name <client_name> --role array_admin

# Directory services (LDAP/AD)
purefb directory-service show
```
