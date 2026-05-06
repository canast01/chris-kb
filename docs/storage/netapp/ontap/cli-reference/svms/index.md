# SVMs

> Part of the [NetApp ONTAP CLI Reference](../).

---

## SVMs (Storage Virtual Machines)

```bash
# List / status
vserver show
vserver show -vserver <svm>
vserver show -fields vserver,type,state,allowed-protocols

# Create / delete
vserver create -vserver <svm> -rootvolume <vol> -aggregate <aggr> -rootvolume-security-style unix
vserver delete -vserver <svm>

# Modify protocols
vserver modify -vserver <svm> -allowed-protocols nfs,cifs,iscsi
vserver show-protocols
```
