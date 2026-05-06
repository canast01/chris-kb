# NFS

> Part of the [NetApp ONTAP CLI Reference](../).

---

## NFS

```bash
# NFS service
vserver nfs show
vserver nfs create -vserver <svm> -v3 enabled -v4.0 enabled -v4.1 enabled
vserver nfs modify -vserver <svm> -v4.1 enabled

# Export policies
vserver export-policy show
vserver export-policy show -vserver <svm>
vserver export-policy create -vserver <svm> -policyname <name>
vserver export-policy delete -vserver <svm> -policyname <name>

# Export rules
vserver export-policy rule show
vserver export-policy rule show -vserver <svm> -policyname <name>
vserver export-policy rule create -vserver <svm> -policyname <name> -ruleindex 1 -clientmatch <cidr> -rorule sys -rwrule sys -superuser sys
vserver export-policy rule delete -vserver <svm> -policyname <name> -ruleindex <n>

# Assign policy to volume
volume modify -vserver <svm> -volume <vol> -policy <export-policy>

# NFS client check
vserver nfs check-client -vserver <svm> -client-ip <ip>
```
