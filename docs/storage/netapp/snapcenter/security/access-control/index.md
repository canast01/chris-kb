---
tags:
  - netapp
  - security
---
# SnapCenter — Access Control


<div class="kb-summary">
Part of the [SnapCenter Security](../index.md) reference.
</div>
```text
┌───────────────────────────────── NetApp SnapCenter — Access Control ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        SnapCenter access control: RBAC roles, least-privilege, and access audit logging       │   │
│   │        Roles: admin (full), operator (read/modify), read-only (view); map to AD groups        │   │
│   │       Authentication: local accounts, LDAP/AD integration, and MFA for privileged users       │   │
│   │          Audit: log all admin actions; review access logs monthly; rotate credentials         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Identify user → assign role → enforce MFA → audit → review quarterly                               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Server           │  │          Windows VM         │  │       Central control       │   │
│   │           Plug-in           │  │          Host agent         │  │        App-consistent       │   │
│   │            Policy           │  │       Schedule/retain       │  │         Backup rule         │   │
│   │        Resource group       │  │       Grouped targets       │  │        Shared policy        │   │
│   │           Recovery          │  │       Volume/LUN/file       │  │       Granular restore      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Role       │   Permissions    │       Scope       │       Auth       │   Review cycle   │   │
│   │      Admin       │    Full CRUD     │       Global      │   MFA required   │     Monthly      │   │
│   │     Operator     │   Read/modify    │      Assigned     │   MFA required   │    Quarterly     │   │
│   │    Read-only     │    View only     │      Assigned     │     Password     │    Quarterly     │   │
│   │   Service acct   │     API only     │    Specific API   │    Token/cert    │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SnapCenter Server (Windows) · ONTAP clusters · plug-in hosts · application servers       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapCenter         = NetApp backup orchestration; coordinates app-consistent snapshots via plug-ins│
│    Plug-in            = host-side agent; quiesces application before snapshot: SQL, Oracle, VMware    │
│    Resource group     = set of resources sharing a backup policy and schedule in SnapCenter           │
│    Policy             = SnapCenter object defining snapshot frequency, retention, and replication t...│
│    App-consistent     = snapshot taken after DB quiesce; guarantees crash-consistent recovery         │
│    Clone lifecycle    = SnapCenter clone: create from snapshot, provision to host, then delete        │
│    FlexClone          = underlying ONTAP technology; SnapCenter clone maps to an ONTAP FlexClone      │
│    Vault policy       = SnapCenter policy that also replicates snapshots to SnapVault destination     │
│    Mirror policy      = SnapCenter policy that replicates snapshots via SnapMirror to DR cluster      │
│    RBAC               = SnapCenter role-based access; Admin, Backup Operator, Restore Operator roles  │
│    SMF                = SnapCenter MySQL database storing job history, policies, and resource configs │
│    SnapCenter API     = REST API on port 8143; full feature coverage for automation workflows         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## RBAC

SnapCenter implements role-based access control at the application level, layered on top of ONTAP-level permissions.

### Built-in Roles

| Role | Access Level |
|---|---|
| SnapCenter Admin | Full access — all operations, settings, user management |
| Infrastructure Admin | Storage connections, hosts, plugins — no backup/restore operations |
| Application Backup and Clone Admin | Create/modify policies, resource groups, run backups, clones, restores |
| Backup and Clone Viewer | Read-only view of jobs, backups, resource groups — no modifications |

### Custom Roles

Create custom roles to delegate specific operations to application teams:

```powershell
# Create a custom role
Add-SmRole -RoleName "Oracle-Restore-Only" -Description "Oracle DBA can restore and clone only"

# Add permissions to the role
Set-SmRole -RoleName "Oracle-Restore-Only" -AllowedOperations "RestoreFromBackup","Clone"

# Assign an AD user to the role
Add-SmUser -UserName "domain\ora-dba01" -RoleName "Oracle-Restore-Only"
```

Assign RBAC at the resource or resource-group level — a user can be granted access to specific resource groups without seeing all resources in SnapCenter.

## ONTAP Service Account Security

SnapCenter connects to ONTAP using credentials stored in the SnapCenter Credential Store. Best practices:

```bash
# On ONTAP — create a dedicated SnapCenter service account with minimum permissions
security login role create -role sc-backup-role -cmddirname "DEFAULT" -access none -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "volume" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "snapshot" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "snapmirror" -access all -vserver <admin-svm>
security login role create -role sc-backup-role -cmddirname "lun" -access all -vserver <admin-svm>

# Create the service account
security login create -username svc-snapcenter -application ontapi -authmethod password -role sc-backup-role -vserver <admin-svm>
security login create -username svc-snapcenter -application http -authmethod password -role sc-backup-role -vserver <admin-svm>
```

## Audit Logging

- All SnapCenter user operations (login, job trigger, policy change, restore, clone) are written to the audit log
- Access audit log: Settings → Settings → Audit Logs in the GUI, or query via REST API
- Export audit logs to a SIEM: configure syslog forwarding from the Windows Server (use Windows Event Forwarding or a Splunk/Elastic agent on the SnapCenter Server)
- Audit log tampering protection: SnapCenter 6.1+ signs audit log entries with a hash chain for integrity verification
