# Quotas

> Part of the [NetApp ONTAP CLI Reference](../).

---

## Quotas

```bash
volume quota show
volume quota report -vserver <svm> -volume <vol>
volume quota on -vserver <svm> -volume <vol>
volume quota off -vserver <svm> -volume <vol>
volume quota resize -vserver <svm> -volume <vol>
volume quota policy rule show -vserver <svm>
volume quota policy rule create -vserver <svm> -policy-name default -type user -target "" -volume <vol> -disk-limit <size>
```
