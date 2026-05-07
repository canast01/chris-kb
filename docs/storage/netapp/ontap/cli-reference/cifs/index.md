# CIFS / SMB

> Part of the NetApp ONTAP CLI Reference.

## CIFS Server

```bash
# Show CIFS servers
vserver cifs show
vserver cifs show -vserver <svm>

# Create a CIFS server (requires AD join)
vserver cifs create -vserver <svm> -cifs-server <name> -domain <domain>

# Delete CIFS server
vserver cifs delete -vserver <svm>
```

## Shares

```bash
# List shares
vserver cifs share show
vserver cifs share show -vserver <svm>

# Create a share
vserver cifs share create -vserver <svm> -share-name <name> -path <path>

# Modify share comment
vserver cifs share modify -vserver <svm> -share-name <name> -comment <text>

# Delete a share
vserver cifs share delete -vserver <svm> -share-name <name>

# Show share permissions (ACL)
vserver cifs share access-control show -vserver <svm> -share <name>

# Set share permission
vserver cifs share access-control modify \
    -vserver <svm> -share <name> \
    -user-or-group <group> -permission Full_Control
```

## Sessions & Connections

```bash
# Show active CIFS sessions
vserver cifs session show
vserver cifs session show -vserver <svm>
vserver cifs session show -fields node,vserver,connection-count

# Show open files
vserver cifs session file show -vserver <svm>

# Disconnect a session
vserver cifs session close -node <node> -vserver <svm> \
    -session-id <id>
```

## CIFS Server Options

```bash
# Show SMB version settings
vserver cifs options show -vserver <svm>

# Enable SMB2/SMB3 (disable SMB1 for security)
vserver cifs options modify -vserver <svm> -smb1-enabled false
vserver cifs options modify -vserver <svm> -smb2-enabled true
```

## AD Connectivity

```bash
# Check CIFS server AD join status
vserver cifs show -vserver <svm> -fields ad-status

# Re-join AD (if domain join broken)
vserver cifs modify -vserver <svm> -domain <domain>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Share inaccessible | CIFS session / share exists | Verify share path and permissions |
| AD join broken | `ad-status` field | Re-join domain |
| SMB1 security risk | SMB options | Disable SMB1 |
| Session count high | `session show` | Investigate client behavior |
