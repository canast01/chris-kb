---
tags:
  - pure
  - security
description: "FlashBlade access control: pureadmin, role-based management (array_admin, ops_admin, readonly), AD/LDAP group mapping, and API token scoping."
---
# FlashBlade — Access Control

<div class="kb-summary">
FlashBlade access control: `pureadmin`, role-based management (`array_admin`, `ops_admin`, `readonly`), AD/LDAP group mapping, and API token scoping.

*Applies to: FlashBlade Purity//FB 4.x*
</div>
![FlashBlade — Access Control](../../../../../assets/storage-pure-flashblade-security-access-control.svg)

---

This page covers Purity//FB role-based access control (RBAC), NFS export policy access control, S3 bucket policies, SMB share permissions, and the principle of least privilege applied to FlashBlade operations.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Admin RBAC

Purity//FB uses role-based access control with the following built-in roles:

| Role | Permissions | Use Case |
|---|---|---|
| `array_admin` | Full administrative access including system configuration, user management, network, and protocol settings | Array administrators responsible for full platform management; restrict to named senior engineers only |
| `storage_admin` | Manage filesystems, buckets, snapshots, and replication; cannot modify system or user configuration | Storage operations team creating and managing data resources; backup tool service accounts |
| `ops_admin` | Read access plus ability to acknowledge and resolve alerts; cannot modify configuration | Operations centre staff performing monitoring and alert response |
| `readonly` | Read-only access to all configuration and status information | Auditors, capacity planners, monitoring integrations using read-only queries |

**Principle of least privilege:** assign the minimum role required. Backup service accounts need `storage_admin` to create and delete snapshots; monitoring tools reading metrics need only `readonly`. No service account should hold `array_admin` unless it explicitly needs to manage users or system configuration.

```bash
# List all users and their assigned roles
purefb admin list

# Create a user with the minimum required role
purefb admin create --name svc-veeam --role storage_admin
purefb admin create --name svc-monitoring --role readonly

# Change a user's role
purefb admin update --name s.jones --role storage_admin

# List AD/LDAP group-to-role mappings
purefb admin list --groups
```


```text title="Expected output"
Name                Role              Source
svc-backup          storage_admin     local
svc-monitoring      readonly          local
s.jones             org_admin         local
admin               system_admin      local
Created user 'svc-veeam' with role 'storage_admin'
Created user 'svc-monitoring' with role 'readonly'
Updated user 's.jones' role to 'storage_admin'
Name                  Role              DN
backup-admins        storage_admin     cn=backup-admins,ou=groups,dc=corp,dc=local
monitoring-ro        readonly          cn=monitoring-ro,ou=groups,dc=corp,dc=local
security-team        org_admin         cn=security-team,ou=groups,dc=corp,dc=local
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: User 'svc-veeam' already exists` | Check existing users with `purefb admin list` and use a unique name or delete the existing user first. |
    | `Error: Invalid role 'storage_adm'. Valid roles are: system_admin, org_admin, storage_admin, readonly` | Correct the role name spelling in the `--role` parameter. |
    | `Error: LDAP/AD not configured` | Configure directory services with `purefb directoryservice create` before attempting to list group mappings. |
---

## NFS Export Policy Access Control

NFS export policies on FlashBlade control which clients can mount a filesystem and what operations they are permitted to perform. Export policies are applied per-filesystem and support multiple rules — each rule matches a client source (IP or CIDR) and defines the permissions for that source.

### Export Policy Rule Components

| Parameter | Values | Description |
|---|---|---|
| Client source | IP, CIDR, or `*` | Which hosts can mount; use CIDR ranges; avoid `*` in production |
| Access permission | `rw`, `ro` | Read-write or read-only |
| Root squash | `root_squash`, `no_root_squash` | Map root (UID 0) from the client to the anonymous UID to prevent root privilege escalation |
| UID/GID mapping | Requires LDAP | UID 0 from the client is mapped to nobody unless `no_root_squash` is set |

### Configure NFS Export Rules

```bash
# Restrict to a specific subnet with root squash (production standard)
purefb filesystem update \
    --name prod-ml-training-data \
    --nfs-rules "10.0.1.0/24(rw,root_squash)"

# Multiple rules — GPU cluster gets RW, monitoring subnet gets RO
purefb filesystem update \
    --name prod-ml-training-data \
    --nfs-rules "10.0.1.0/24(rw,root_squash):10.0.5.0/24(ro)"

# Backup server gets its own rule with no_root_squash (Veeam requirement)
purefb filesystem update \
    --name prod-veeam-daily \
    --nfs-rules "10.0.10.50/32(rw,no_root_squash)"

# Verify the current export rules on a filesystem
purefb filesystem list --name prod-ml-training-data
```


```text title="Expected output"
Filesystem prod-ml-training-data updated successfully.
NFS rules applied: 10.0.1.0/24(rw,root_squash)

Filesystem prod-ml-training-data updated successfully.
NFS rules applied: 10.0.1.0/24(rw,root_squash):10.0.5.0/24(ro)

Filesystem prod-veeam-daily updated successfully.
NFS rules applied: 10.0.10.50/32(rw,no_root_squash)

Name                      Size      Nfs-Rules                                    Protocol  Snapshot-Dir
prod-ml-training-data     2.5TB     10.0.1.0/24(rw,root_squash):10.0.5.0/24(ro)  nfsv3     enabled
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Filesystem 'prod-ml-training-data' not found` | Verify the filesystem name matches exactly with `purefb filesystem list` and check for typos. |
    | `Error: Invalid NFS rule syntax 'rw,root_squash'` | Ensure NFS rules follow the format `subnet/mask(option1,option2)` with parentheses and no spaces inside the rule definition. |
    | `Error: CIDR block 10.0.10.50/32 overlaps with existing rule` | Use a non-overlapping subnet or remove the conflicting rule before applying the new one. |
### Export Policy Best Practices

| Requirement | Configuration |
|---|---|
| Lock down production filesystems | Use specific CIDR ranges — never `*` in production |
| Prevent root privilege escalation via NFS | Always use `root_squash` unless the application explicitly requires `no_root_squash` (e.g., Veeam backup servers) |
| Read-only for consumer workloads | Use `ro` for analytics or monitoring clients that only read data |
| Separate backup from production mounts | Create dedicated filesystems for backup workloads so production clients cannot mount the backup target |
| Enforce NFSv4.1 for sensitive data | NFSv4.1 supports Kerberos (`sec=krb5p`) for authentication and encryption — use it for regulated workloads |

---

## S3 Bucket Access Control

FlashBlade S3 access control uses a two-layer model: object store accounts own buckets and define tenant isolation, and per-user access keys provide the S3 API credentials. Bucket policies add fine-grained access rules on top of the account model.

### Object Store Account Model

![FlashBlade — Access Control — Diagram](../../../../../assets/storage-pure-flashblade-security-access-control-diagram.svg)

### Create Accounts, Users, and Access Keys

```bash
# Create an object store account (tenant namespace)
purefb object-store-account create --name ml-platform

# Create a user under the account
purefb object-store-user create \
    --name svc-training-pipeline \
    --account ml-platform

# Create an access key for the user
purefb object-store-access-key create \
    --user svc-training-pipeline/ml-platform
# Output includes access_key_id and secret_access_key — save the secret immediately

# List all object store accounts
purefb object-store-account list

# List all users and their accounts
purefb object-store-user list

# List all access keys (secrets are not shown after creation)
purefb object-store-access-key list
```


```text title="Expected output"
Object store account created: ml-platform
Object store user created: svc-training-pipeline
Access key created for svc-training-pipeline/ml-platform
  access_key_id: 00a1b2c3d4e5f6g7h8i9
  secret_access_key: wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY

Name                 Account         Created
ml-platform          ml-platform     2024-01-15T09:23:44Z
default              default         2023-11-02T14:12:10Z

Name                          Account         Created
svc-training-pipeline         ml-platform     2024-01-15T09:24:12Z
admin                         default         2023-11-02T14:15:33Z

Access Key ID                 User                              Account         Created
00a1b2c3d4e5f6g7h8i9         svc-training-pipeline            ml-platform     2024-01-15T09:24:58Z
a9b8c7d6e5f4g3h2i1j0         admin                             default         2023-11-02T14:16:05Z
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: object store account 'ml-platform' already exists` | Use `purefb object-store-account list` to verify the account name is unique, or delete the existing account first with `purefb object-store-account delete --name ml-platform`. |
    | `Error: user 'svc-training-pipeline' already exists in account 'ml-platform'` | Verify the username with `purefb object-store-user list --account ml-platform` and use a different name or delete the existing user. |
    | `Error: failed to connect to FlashBlade management interface` | Ensure the FlashBlade array is reachable and you are authenticated with `purefb login` or check your `PUREFB_HOST` and `PUREFB_API_TOKEN` environment variables. |
### Rotate an S3 Access Key

S3 access keys do not expire automatically. Rotate them on a defined schedule:

```bash
# Step 1 — Create a new access key for the user
purefb object-store-access-key create --user svc-training-pipeline/ml-platform
# Note the new key ID and secret

# Step 2 — Update the new key in the consuming application/service
# (update AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in the application config)

# Step 3 — Verify the new key works
aws s3 ls s3://prod-ml-training-data \
    --endpoint-url https://<fb-s3-vip>/ \
    # (using new key credentials)

# Step 4 — Delete the old access key
purefb object-store-access-key delete \
    --name <old_access_key_id>
```


```text title="Expected output"
Created access key for user svc-training-pipeline/ml-platform
Access Key ID: 0a1b2c3d4e5f6g7h8i9j
Secret Access Key: wX+yZ/aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3
(no output — command completes silently)
2024-01-15T14:32:18Z    s3://prod-ml-training-data
                           PRE training-datasets/
                           PRE model-checkpoints/
                           PRE validation-splits/
2024-01-15T14:32:19Z    s3://prod-ml-training-data/training-datasets/imagenet-v2.tar.gz
2024-01-15T14:32:19Z    s3://prod-ml-training-data/training-datasets/cifar-100.tar.gz
Deleted access key: 0a1b2c3d4e5f6g7h
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: access key not found for user svc-training-pipeline/ml-platform` | Verify the user exists in Pure FlashBlade with `purefb user list` and confirm the user path is correct. |
    | `An error occurred (InvalidAccessKeyId) when calling the ListBucket operation: The Access Key Id you provided does not exist in our records.` | Ensure the new access key credentials were correctly copied to the application config and the old key was not deleted before the new one was fully propagated (wait 30 seconds). |
    | `Error: access key <old_access_key_id> not found` | Confirm the exact access key ID with `purefb object-store-access-key list --user svc-training-pipeline/ml-platform` before deletion. |
### Bucket Policies

Bucket policies provide IAM-style access control rules on a per-bucket basis. Use bucket policies when multiple accounts or users need different levels of access to the same bucket.

```bash
# Apply an S3 bucket policy (JSON policy document)
purefb bucket access-policy update \
    --name prod-ml-training-data \
    --policy '{
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {"AWS": ["arn:aws:iam:::user/svc-training-pipeline/ml-platform"]},
          "Action": ["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:ListBucket"],
          "Resource": ["arn:aws:s3:::prod-ml-training-data/*",
                       "arn:aws:s3:::prod-ml-training-data"]
        },
        {
          "Effect": "Allow",
          "Principal": {"AWS": ["arn:aws:iam:::user/svc-analytics-reader/ml-platform"]},
          "Action": ["s3:GetObject","s3:ListBucket"],
          "Resource": ["arn:aws:s3:::prod-ml-training-data/*",
                       "arn:aws:s3:::prod-ml-training-data"]
        }
      ]
    }'

# View the current bucket policy
purefb bucket access-policy list --name prod-ml-training-data
```


```text title="Expected output"
Bucket policy updated successfully.
Name: prod-ml-training-data
Policy Version: 2012-10-17
Statements: 2
Last Modified: 2024-01-15T14:32:47Z

Name: prod-ml-training-data
Policy:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": ["arn:aws:iam:::user/svc-training-pipeline/ml-platform"]},
      "Action": ["s3:GetObject","s3:PutObject","s3:DeleteObject","s3:ListBucket"],
      "Resource": ["arn:aws:s3:::prod-ml-training-data/*","arn:aws:s3:::prod-ml-training-data"]
    },
    {
      "Effect": "Allow",
      "Principal": {"AWS": ["arn:aws:iam:::user/svc-analytics-reader/ml-platform"]},
      "Action": ["s3:GetObject","s3:ListBucket"],
      "Resource": ["arn:aws:s3:::prod-ml-training-data/*","arn:aws:s3:::prod-ml-training-data"]
    }
  ]
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid JSON in policy document` | Validate the JSON syntax using `jq . <<< '<policy>'` before applying, or escape quotes properly with backslashes. |
    | `Error: Bucket 'prod-ml-training-data' not found` | Verify the bucket exists with `purefb bucket list` and confirm the name matches exactly. |
    | `Error: Principal ARN format invalid` | Ensure IAM user ARNs follow the correct format `arn:aws:iam::ACCOUNT-ID:user/USERNAME` with a valid account ID in the third field. |
**S3 access control best practices:**

| Requirement | Implementation |
|---|---|
| Least privilege for S3 consumers | Grant only the operations required — `s3:GetObject` and `s3:ListBucket` for readers; add `s3:PutObject` and `s3:DeleteObject` only for writers |
| Isolate application namespaces | Create a separate object store account per application team — bucket names and users do not cross account boundaries |
| Rotate access keys regularly | 90-day rotation schedule for all S3 access keys; revoke immediately on service account decommissioning |
| No wildcard principal grants | Avoid `"Principal": "*"` (public access) on production buckets |

---

## SMB Share Permissions

FlashBlade SMB shares use a combination of filesystem-level NFS/POSIX permissions and Windows-style share-level permissions backed by Active Directory. AD join is required for SMB access.

### Create an SMB Share

```bash
# Enable SMB on a filesystem and create a share
purefb filesystem update \
    --name prod-analytics-share \
    --smb-enabled true

purefb smb-share create \
    --name PROD-ANALYTICS \
    --filesystem prod-analytics-share

# Verify the share is created
purefb smb-share list
```


```text title="Expected output"
Filesystem prod-analytics-share updated.
SMB share PROD-ANALYTICS created successfully.
Name                  Filesystem              Protocol  Path
PROD-ANALYTICS        prod-analytics-share    SMB       /prod-analytics-share
SHARED-REPORTS        financial-data          SMB       /financial-data
BACKUP-ARCHIVE        archive-vol-01          SMB       /archive-vol-01
TEMP-WORKSPACE        temp-storage            SMB       /temp-storage
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Filesystem 'prod-analytics-share' not found` | Verify the filesystem name exists with `purefb filesystem list` and correct any typos. |
    | `Error: SMB is not enabled on filesystem 'prod-analytics-share'` | Ensure the filesystem update command completes successfully before attempting to create the SMB share. |
    | `Error: SMB share 'PROD-ANALYTICS' already exists` | Use a different share name or delete the existing share with `purefb smb-share delete --name PROD-ANALYTICS` first. |
### Share-Level Access Control

SMB share-level permissions are configured in the Windows environment using the share's security descriptor. From a Windows host with appropriate AD credentials:

```powershell
# Grant an AD group Full Control on the share
$sharePath = "\\fb-smb-vip\PROD-ANALYTICS"
$acl = Get-Acl -Path $sharePath

$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "EXAMPLE\Storage-Admins",
    "FullControl",
    "ContainerInherit,ObjectInherit",
    "None",
    "Allow"
)
$acl.SetAccessRule($rule)
Set-Acl -Path $sharePath -AclObject $acl

# Grant read-only access to a broader group
$readRule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "EXAMPLE\Analytics-Users",
    "Read",
    "ContainerInherit,ObjectInherit",
    "None",
    "Allow"
)
$acl.SetAccessRule($readRule)
Set-Acl -Path $sharePath -AclObject $acl
```

**SMB encryption:** Enable SMB 3.0 in-transit encryption per share to protect data in transit between Windows clients and FlashBlade:

```bash
purefb smb-share update \
    --name PROD-ANALYTICS \
    --smb-encryption-mode required
```


```text title="Expected output"
SMB share 'PROD-ANALYTICS' updated successfully.
Encryption mode: required
Applied to: 2 connected clients
Clients will reconnect within 30 seconds.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: SMB share 'PROD-ANALYTICS' not found` | Verify the share name matches exactly (case-sensitive) using `purefb smb-share list`. |
    | `Error: Invalid encryption mode 'required'. Valid modes: disabled, preferred, required` | Use one of the three valid encryption modes; note that 'required' may disconnect clients using older SMB versions. |
---

## Audit Logging

All administrative actions performed via the Purity//FB GUI, CLI, or REST API are recorded in the audit log with the username, source IP address, timestamp, and the specific operation performed.

```bash
# View recent audit entries
purefb audit list

# Filter by user
purefb audit list --filter "user='s.jones'"

# Filter by action type (e.g., filesystem operations)
purefb audit list --filter "operation_name='filesystem'"

# Export audit log (full history)
purefb audit export
```


```text title="Expected output"
Timestamp                    User      Action                 Resource              Status
2024-01-15T14:32:18Z        admin     login                  system                success
2024-01-15T14:35:42Z        s.jones   filesystem_write       /data/projects        success
2024-01-15T14:36:01Z        s.jones   filesystem_read        /data/projects/file1  success
2024-01-15T14:37:15Z        m.patel   policy_modify          replication_policy    success
2024-01-15T14:38:22Z        s.jones   filesystem_delete      /data/archive/old     success

Timestamp                    User      Action                 Resource              Status
2024-01-15T14:35:42Z        s.jones   filesystem_write       /data/projects        success
2024-01-15T14:36:01Z        s.jones   filesystem_read        /data/projects/file1  success
2024-01-15T14:38:22Z        s.jones   filesystem_delete      /data/archive/old     success

Timestamp                    User      Action                 Resource              Status
2024-01-15T14:35:42Z        s.jones   filesystem_write       /data/projects        success
2024-01-15T14:36:01Z        s.jones   filesystem_read        /data/projects/file1  success
2024-01-15T14:38:22Z        s.jones   filesystem_delete      /data/archive/old     success

Export started. Output file: audit_export_20240115_143900.csv
Exporting 47293 audit entries...
Export completed successfully.
File location: /var/log/purity/audit_export_20240115_143900.csv
File size: 12.4 MB
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Authentication failed. Invalid credentials or session expired.` | Re-authenticate using `purefb login` with valid admin credentials. |
    | `Error: Invalid filter syntax. Expected format: --filter "field='value'"` | Verify filter field names match audit schema (e.g., `user`, `operation_name`, `resource`) and use single quotes around values. |
    | `Error: Insufficient permissions. User role does not have audit read access.` | Grant the user the Audit Reader or Admin role via the FlashBlade management interface. |
**Forward audit logs off-array** to prevent tampering and to maintain a persistent audit trail:

```bash
# Configure TLS syslog (preferred for integrity)
purefb syslog create --uri tls://siem.example.com:6514 siem-tls

# UDP syslog (fallback)
purefb syslog create --uri udp://siem.example.com:514 siem-udp

# Verify syslog destinations
purefb syslog list
```


```text title="Expected output"
Creating syslog destination siem-tls...
Syslog destination siem-tls created successfully.
Creating syslog destination siem-udp...
Syslog destination siem-udp created successfully.
Name          URI                              Severity  Facility
siem-tls      tls://siem.example.com:6514      all       local0
siem-udp      udp://siem.example.com:514       all       local0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused to siem.example.com:6514` | Verify the SIEM server hostname/IP is reachable and the syslog service is listening on the specified port. |
    | `Error: Syslog destination 'siem-tls' already exists` | Remove the existing destination with `purefb syslog delete siem-tls` before recreating it. |
    | `Error: Invalid URI scheme 'tls'. Valid schemes are: udp, tcp` | Confirm your FlashBlade firmware supports TLS syslog (requires Purity 3.0+); use `tcp://` as an alternative if TLS is unavailable. |
Configure SIEM alerts for the following audit events:
- Multiple failed login attempts from the same source IP (brute force indicator)
- API token creation or deletion — especially outside business hours
- Filesystem or bucket permission changes
- Snapshot eradication events
- SafeMode modification attempts

---

## Access Control Review Checklist

Run this review quarterly and before any security audit:

```bash
# List all admin accounts and roles — look for unexpected accounts or over-provisioned roles
purefb admin list

# List all API tokens — confirm each has a documented owner
purefb admin apitoken list

# List AD/LDAP group-to-role mappings — verify group membership in AD separately
purefb admin list --groups

# List all object store accounts and users
purefb object-store-account list
purefb object-store-user list

# List all access keys — follow up on keys with old creation dates
purefb object-store-access-key list

# List SMB shares and confirm share-level permissions are current
purefb smb-share list

# List filesystems with NFS export rules — check for wildcard (*) source entries
purefb filesystem list
```


```text title="Expected output"
Name                    Role            Created                 
admin                   System Admin     2024-01-15T08:22:14Z    
svc-backup              System Admin     2023-11-02T14:51:33Z    
audit-user              Read Only        2024-02-20T09:15:47Z    
Name                    Created                 Expires                 
token_a7f2c9e1          2024-02-15T10:33:22Z    2025-02-15T10:33:22Z   
token_b4d8f6k2          2024-01-08T16:45:11Z    2025-01-08T16:45:11Z   
Group Name              Role            
storage-admins         System Admin     
backup-operators       Operator        
Name                    Account ID                          
prod-s3-account         a1b2c3d4-e5f6-47g8-h9i0-j1k2l3m4n5o6
dev-s3-account          f7g8h9i0-j1k2-43l3-m4n5-o6p7q8r9s0t1
Name                    Account                 Created                 
obj-user-prod           prod-s3-account         2024-01-22T11:08:55Z    
obj-user-dev            dev-s3-account          2024-02-10T13:42:19Z    
Name                    Account                 Created                 
AKIA7M9N2P4Q5R6S7T8U    prod-s3-account         2023-09-14T07:19:33Z    
AKIA2K3L4M5N6O7P8Q9R    dev-s3-account          2024-02-18T15:27:44Z    
Name                    Exported                Protocol            
share-finance           true                    SMB                 
share-engineering       true                    SMB                 
Name                    Size            Exported            
fs-prod-data            2.5TB           true                
fs-archive              8.2TB           true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `purefb: command not found` | Install the Pure Storage FlashBlade CLI tools or ensure the purefb binary is in your PATH. |
    | `Error: Authentication failed` | Verify your FlashBlade credentials are configured via `purefb login` or environment variables. |
    | `Error: Permission denied` | Confirm your admin account has sufficient role privileges to list the requested resource type. |
| Check | Expected State | Action if Unexpected |
|---|---|---|
| No `array_admin` service accounts | Only named human admins hold this role | Downgrade service account roles to `storage_admin` or lower |
| No wildcard `*` NFS export rules on production filesystems | All production exports use specific CIDR ranges | Update export rules to restrict source IP |
| All S3 access keys have a documented owner | Every key maps to an active service or person | Revoke unaccounted keys immediately |
| No AD group mappings to accounts that no longer exist in AD | Groups are still valid in AD directory | Remove stale group mappings |
| Audit logs are flowing to SIEM | SIEM shows recent FlashBlade audit events | Check syslog configuration and SIEM ingestion |

---

## See also

- [FlashBlade — Authentication](../authentication/)
- [FlashBlade — Hardening](../hardening/)
- [FlashBlade — Encryption](../encryption/)
