---
tags:
  - netapp
  - security
description: "Access Control reference covering RBAC Scope Model, RBAC, Custom Roles, User Login Management, Audit Logging."
---
# ONTAP — Access Control

<div class="kb-summary">
Access Control reference covering RBAC Scope Model, RBAC, Custom Roles, User Login Management, Audit Logging.

*Applies to: ONTAP 9.x*
</div>
![ONTAP — Access Control](../../../../../assets/storage-netapp-ontap-security-access-control.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## RBAC Scope Model

```d2
direction: right

cluster: "Cluster\n(admin SVM" {shape: rectangle}
clusterAdmin: "Full cluster\nadministration" {shape: rectangle}
clusterRO: "Read-only\ncluster view" {shape: rectangle}
svm1: "SVM: prod-nas" {shape: rectangle}
svmFull: "Full SVM admin\n(protocols, volumes, LIFs" {shape: rectangle}
svmBackup: "Snapshot + SnapMirror\nonly" {shape: rectangle}
svmRO: "Read-only\nSVM view" {shape: rectangle}
svm2: "SVM: prod-san" {shape: rectangle}
customRole: "Minimum privilege\nservice account\n(monitoring, backup" {shape: rectangle}
user1: "admin account" {shape: rectangle}
user2: "vsadmin / svc account" {shape: rectangle}
note: "Custom roles override built-in roles\nAlways apply least-privilege principle" {shape: rectangle}

cluster -> clusterAdmin
cluster -> clusterRO
svm1 -> svmFull
svm1 -> svmBackup
svm1 -> svmRO
svm2 -> customRole
user1 -> cluster
user2 -> svm1
svm1 -> svm2
```

## RBAC

ONTAP has two RBAC scopes: **cluster-level** (managed by the `admin` account) and **SVM-level** (managed by `vsadmin` accounts within a specific SVM). Built-in roles:

| Role | Scope | Access Level |
|---|---|---|
| `admin` | Cluster | Full cluster administration — all commands |
| `readonly` | Cluster | Read-only cluster view — no configuration changes |
| `vsadmin` | SVM | Full SVM administration within one SVM |
| `vsadmin-readonly` | SVM | Read-only view of one SVM |
| `vsadmin-backup` | SVM | Snapshot and SnapMirror operations within one SVM |
| `vsadmin-snaplock` | SVM | SnapLock volume administration within one SVM |
| `vsadmin-protocol` | SVM | Protocol configuration (NFS, CIFS, iSCSI) within one SVM |

## Custom Roles

Create custom roles with minimum required permissions for automation service accounts:

```bash
# Create a custom read-only monitoring role
security login role create -role monitor-role -cmddirname "DEFAULT" -access none
security login role create -role monitor-role -cmddirname "version" -access readonly
security login role create -role monitor-role -cmddirname "volume show" -access readonly
security login role create -role monitor-role -cmddirname "snapmirror show" -access readonly

# Create a service account using the custom role
security login create -username svc-monitor -application ssh -authmethod publickey -role monitor-role
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: "monitor-role" already exists.` | Delete the existing role first with `security login role delete -role monitor-role` or use a different role name. |
    | `Error: Command directory "snapmirror show" not found.` | Verify the exact command directory name using `security login role show -role admin` and use the correct command path (e.g., `snapmirror` instead of `snapmirror show`). |
    | `Error: User "svc-monitor" already exists.` | Remove the existing user with `security login delete -username svc-monitor -application ssh` before recreating it. |
## User Login Management

```bash
# List all login accounts
security login show
security login show -vserver <svm>

# Create a user (SSH + password auth)
security login create \
    -username <user> \
    -application ssh \
    -authentication-method password \
    -role admin \
    -vserver <svm>

# Delete a user
security login delete -username <user> -application ssh -vserver <svm>

# Change password
security login password -username <user> -vserver <svm>

# Lock / unlock an account
security login lock -username <user> -vserver <svm>
security login unlock -username <user> -vserver <svm>
```


```text title="Expected output"
cluster1::> security login show
Vserver: cluster1
                                                 Authentication
User/Group                 Application Method    Role Name
------------------------   -----------  --------  ----------
admin                      console      password  admin
admin                      http         password  admin
admin                      ontapi       password  admin
admin                      ssh          password  admin
diag                       console      password  diag
diag                       http         password  diag
diag                       ontapi       password  diag
diag                       ssh          password  diag
...

cluster1::> security login show -vserver svm_prod
Vserver: svm_prod
                                                 Authentication
User/Group                 Application Method    Role Name
------------------------   -----------  --------  ----------
vsadmin                    ssh          password  vsadmin
backup_user                ssh          password  backup
...

cluster1::> security login create -username netops_user -application ssh -authentication-method password -role admin -vserver svm_prod
Please enter a password for user 'netops_user':
Please confirm the password:
(no output — command completes silently)

cluster1::> security login password -username netops_user -vserver svm_prod
Please enter a password for user 'netops_user':
Please confirm the password:
(no output — command completes silently)

cluster1::> security login lock -username netops_user -vserver svm_prod
(no output — command completes silently)

cluster1::> security login unlock -username netops_user -vserver svm_prod
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: "netops_user" does not exist.` | Verify the username exists with `security login show` before attempting to modify or delete it. |
    | `Error: Role "admin" does not exist for Vserver "svm_prod".` | Use `security login role show -vserver svm_prod` to list valid roles and specify an existing role name. |
    | `Error: This operation is not permitted: User "admin" cannot be locked.` | Built-in system accounts cannot be locked; only custom user accounts can be locked for security purposes. |
## Audit Logging

**Admin action auditing**: All CLI, API, and System Manager operations by authenticated users are captured in the ONTAP audit log:

```bash
# View recent administrative audit events
security audit log show
security audit log show -user admin -time-range 24h
```


```text title="Expected output"
Vserver     User      Ip Address      Event                           Result
----------- --------- --------------- ------------------------------- -------
cluster1    admin     192.168.1.50    login                           success
cluster1    admin     192.168.1.50    set advanced-privilege          success
cluster1    admin     192.168.1.50    storage aggregate show           success
cluster1    admin     192.168.1.50    volume create                    success
cluster1    admin     192.168.1.50    security audit log show          success
cluster1    admin     192.168.1.50    logout                           success

Vserver     User      Ip Address      Event                           Result Time
----------- --------- --------------- ------------------------------- ------- -------------------------
cluster1    admin     192.168.1.50    login                           success 2024-01-15 14:32:18 -05:00
cluster1    admin     192.168.1.50    volume snapshot create          success 2024-01-15 13:47:22 -05:00
cluster1    admin     192.168.1.50    security ssl modify              success 2024-01-15 12:15:09 -05:00
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command not found: security audit log show` | Verify you are connected to a NetApp ONTAP cluster (not a different storage system) using `system node show`. |
    | `Error: Access denied. Insufficient privileges to view audit logs` | Ensure your user account has admin or audit-admin role by running `security login show -user <username>`. |
**File access auditing via ONTAP Audit Framework**: Captures NFS and SMB file access events to an EVTX audit log on a designated NAS volume:

```bash
# Configure SVM-level file access auditing
vserver audit create -vserver <svm> -destination /audit_logs -events file-ops,cifs-logon-logoff
vserver audit enable -vserver <svm>
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: "audit" is not a recognized command.` | Ensure you are connected to the ONTAP cluster management interface and have sufficient privileges; use `security audit` instead of `vserver audit` depending on your ONTAP version. |
    | `Error: destination "/audit_logs" does not exist` | Create the audit log destination directory first using `volume create -vserver <svm> -volume audit_logs -aggregate <aggr> -size 10GB` or specify an existing path. |
    | `Error: vserver <svm> does not exist or access is denied` | Verify the SVM name is correct and you have cluster administrator or SVM administrator credentials with audit permissions. |
**FPolicy for file access control and monitoring**: FPolicy intercepts file operations and can send them to an external FPolicy server (DLP, ransomware detection, archiving):

```bash
# Show FPolicy configuration
fpolicy show
fpolicy policy show
fpolicy policy scope show
```


```text title="Expected output"
Vserver         Policy Name                    Event
-----------     -------------------------------- --------
svm-prod        ransomware-protection          file-create
svm-prod        ransomware-protection          file-write
svm-prod        data-audit                     file-access
svm-dev         basic-monitoring               file-create
svm-dev         basic-monitoring               file-delete

Vserver         Policy Name          Status    Scope Name
-----------     -------------------- --------- --------------------
svm-prod        ransomware-protection enabled  prod-shares
svm-prod        data-audit           enabled   audit-scope
svm-dev         basic-monitoring     disabled  dev-scope

Vserver         Policy Name          Scope Name       Volumes
-----------     -------------------- --------------- ----------------
svm-prod        ransomware-protection prod-shares     vol_data_01, vol_data_02
svm-prod        data-audit           audit-scope     vol_audit
svm-dev         basic-monitoring     dev-scope       vol_dev_01
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command not found: fpolicy` | Ensure you are connected to a NetApp ONTAP cluster with admin privileges and run the command from the ONTAP CLI, not the local shell. |
    | `Error: This operation is not permitted: insufficient privileges` | Verify your user account has the "security" or "admin" role assigned in ONTAP. |
---

## See also

- [Ontap — Authentication](../authentication/)
- [Ontap — Hardening](../hardening/)
- [Ontap — Encryption](../encryption/)
