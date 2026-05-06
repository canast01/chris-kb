# SMB Shares

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# List shares
isi smb shares list
isi smb shares view <share_name>

# Create share
isi smb shares create <share_name> /ifs/<path>

# Modify share
isi smb shares modify <share_name> --description "<text>"

# Delete share
isi smb shares delete <share_name>

# Share permissions
isi smb shares permission list <share_name>
isi smb shares permission create <share_name> --authority <domain\\user> --permission-type allow --permission full

# SMB settings
isi smb settings global view
isi smb settings service view

# Sessions
isi smb sessions list
```
