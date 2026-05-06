# Security & Users

> Part of the [NetApp ONTAP CLI Reference](../).

---

## Security & Users

```bash
# Logins
security login show
security login show -vserver <svm>
security login create -username <user> -application ssh -authentication-method password -role admin -vserver <svm>
security login delete -username <user> -application ssh -vserver <svm>
security login password -username <user> -vserver <svm>
security login lock -username <user> -vserver <svm>
security login unlock -username <user> -vserver <svm>

# Roles
security login role show
security login role create -role <name> -vserver <svm> -cmddirname DEFAULT -access none

# Certificates
security certificate show
security certificate show -vserver <svm>
security certificate install -vserver <svm> -type server
security certificate generate-csr -common-name <cn> -size 2048 -country US -state <state> -locality <city> -organization <org>
```
