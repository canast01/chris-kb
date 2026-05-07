# NFS

> Part of the NetApp ONTAP CLI Reference.
## NFS Service

```bash
# Show NFS configuration per SVM
vserver nfs show
vserver nfs show -vserver <svm>

# Enable NFS on an SVM
vserver nfs create -vserver <svm> -v3 enabled -v4.0 enabled -v4.1 enabled

# Modify NFS version settings
vserver nfs modify -vserver <svm> -v4.1 enabled
```

## Export Policies

```bash
# List export policies
vserver export-policy show
vserver export-policy show -vserver <svm>

# Create an export policy
vserver export-policy create -vserver <svm> -policyname <name>

# Delete an export policy
vserver export-policy delete -vserver <svm> -policyname <name>
```

## Export Rules

```bash
# List rules for a policy
vserver export-policy rule show
vserver export-policy rule show -vserver <svm> -policyname <name>

# Create a rule (allow subnet read-write with SYS auth)
vserver export-policy rule create \
    -vserver <svm> \
    -policyname <name> \
    -ruleindex 1 \
    -clientmatch <cidr_or_ip> \
    -rorule sys \
    -rwrule sys \
    -superuser sys

# Delete a rule
vserver export-policy rule delete -vserver <svm> -policyname <name> -ruleindex <n>
```

## Assign Policy to Volume

```bash
volume modify -vserver <svm> -volume <vol> -policy <export-policy>
```

## NFS Client Verification

```bash
# Test if a specific client IP can access the export
vserver nfs check-client -vserver <svm> -client-ip <ip>
```

## Connected NFS Clients

```bash
nfs connected-client show -vserver <svm>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Mount fails — permission denied | Export rule client match | Verify CIDR includes client IP |
| NFSv4 ID mapping fails | LDAP/DNS | Configure `idmapping` service |
| Mount hangs | LIF reachable | Ping NFS LIF; check routing |
| Root squash blocking writes | Superuser setting | Set `-superuser sys` if intentional root access needed |
