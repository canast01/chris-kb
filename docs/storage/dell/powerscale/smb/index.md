# PowerScale SMB

SMB share management, configuration, and troubleshooting on Dell PowerScale.

## Share Management

```bash
# List all SMB shares
isi smb shares list
isi smb shares list -v

# View a specific share
isi smb shares view <share_name>

# Create a share
isi smb shares create <share_name> /ifs/data/project1 \
    --description "Project 1 share" \
    --browsable yes \
    --allow-execute-always yes

# Modify a share
isi smb shares modify <share_name> --description "Updated description"
isi smb shares modify <share_name> --add-permissions 'user:<username>:allow:full'

# Delete a share
isi smb shares delete <share_name>
```

## Permissions

```bash
# View share permissions (ACL)
isi smb shares view <share_name> | grep -A 20 "Permission"

# Add a user with read permission
isi smb shares modify <share_name> \
    --add-permissions 'user:CORP\jsmith:allow:read'

# Add a group with change permission
isi smb shares modify <share_name> \
    --add-permissions 'group:CORP\fileusers:allow:change'

# Set full control for an admin group
isi smb shares modify <share_name> \
    --add-permissions 'group:CORP\storeadmins:allow:full'

# Remove a permission entry
isi smb shares modify <share_name> \
    --remove-permissions 'user:CORP\jsmith:allow:read'
```

## SMB Settings

```bash
# Global SMB settings (server configuration)
isi smb settings global view

# Per-share default settings
isi smb settings shares view

# SMB service status
isi services smb status

# Restart SMB service (with caution — disrupts active sessions)
isi services smb restart
```

## SMB Sessions and Open Files

```bash
# Active SMB sessions
isi smb sessions list

# Open files per session
isi smb openfiles list

# Disconnect a specific session
isi smb sessions delete <session_id>
```

## SMB Access Zones

```bash
# List shares in a specific access zone
isi smb shares list --zone Zone1

# Create share in a non-default access zone
isi smb shares create <share_name> /ifs/zone1/data \
    --zone Zone1
```

## Troubleshooting SMB

```bash
# Check SMB protocol stats
isi statistics protocol list --protocol smb2
isi statistics protocol list --protocol smb3

# Check for SMB errors in events
isi event events list | grep -i smb

# Verify AD authentication is working
isi auth status | grep -i "Active Directory\|joined"
isi auth ads list

# Check group memberships resolve correctly
isi auth users view <username>
isi auth groups view <groupname>

# Test access zone authentication
isi zone zones view <zone_name>
```

## SMB Auditing

```bash
# Enable SMB audit for a share
isi smb shares modify <share_name> --enable-oplock-audit yes

# View audit settings
isi audit settings global view
isi audit settings protocols view

# Enable protocol audit logging (SMB events to syslog)
isi audit settings protocols modify --audit-success create,delete,rename,set-security
```
