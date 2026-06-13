---
tags:
  - dell
  - security
---
# PowerStore — Access Control


<div class="kb-summary">
Access Control reference covering Role-Based Access Control, User Account Management, Host Access Control, NFS Export Access Control, SMB Share Access Control and 1 more sections.

*Applies to: PowerStore 3.x*
</div>
```text
┌────────────────────────────────── Dell PowerStore — Access Control ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        PowerStore access control: RBAC roles, least-privilege, and access audit logging       │   │
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
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
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
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Role-Based Access Control

PowerStore uses a role-based access control model. Every user (local or LDAP-mapped) is assigned exactly one role. Roles are non-cumulative — a user has the permissions of their assigned role and nothing more.

| Role | Permissions | Intended Users |
|---|---|---|
| Administrator | Full access: create, modify, delete all resources; manage users, roles, certificates, networking; view all data | Storage lead, storage architect |
| StorageOperator | Provision and manage storage resources (volumes, hosts, NAS, snapshots, replication); cannot manage users or system security settings | Storage operations engineers |
| VMOperator | Create and manage vVols and storage containers for VMware; limited scope to VMware-related resources only | VMware administrators |
| Viewer | Read-only access to all storage resource data; cannot create, modify, or delete anything | Monitoring tools, application owners, capacity reviewers |
| SecurityAdmin | Manage certificates, LDAP configuration, audit logs, and security settings; cannot manage storage resources | Security team |

### Applying Least Privilege

Design service accounts and user accounts with the minimum role needed:

| Use Case | Role | Rationale |
|---|---|---|
| Day-to-day provisioning (storage team) | StorageOperator | Provision and manage without security or user management access |
| Read-only monitoring scripts | Viewer | No write access; cannot introduce configuration drift |
| VMware vCenter plugin (storage admin function) | Administrator | vCenter integration requires full API access |
| VMware vCenter plugin (VMware team) | VMOperator | Scoped to vVols management only |
| Veeam / backup integration | StorageOperator | Needs snapshot create/delete; no security access |
| Ansible/Terraform automation | StorageOperator or Administrator | Administrator only if you need to create LDAP config or users via IaC |
| LDAP and certificate management | SecurityAdmin | Dedicated security role; isolates from storage operations |

```bash
# Create a local user account with StorageOperator role (for a service account)
curl -k -X POST "https://<mgmt-ip>/api/rest/user/local" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "svc-veeam",
    "password": "<password>",
    "role_name": "StorageOperator",
    "is_built_in": false
  }'

# Create a read-only monitoring account
curl -k -X POST "https://<mgmt-ip>/api/rest/user/local" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "svc-monitoring",
    "password": "<password>",
    "role_name": "Viewer",
    "is_built_in": false
  }'
```

## User Account Management

### Audit All User Accounts

```bash
# List all local user accounts and their roles
curl -k -X GET "https://<mgmt-ip>/api/rest/user/local?select=name,role_name,is_built_in,is_default_password" \
  -H "DELL-EMC-TOKEN: <token>"

# List LDAP group-to-role mappings
curl -k -X GET "https://<mgmt-ip>/api/rest/ldap_domain_role_mapping" \
  -H "DELL-EMC-TOKEN: <token>"
```

Perform a quarterly review of all user accounts:

- [ ] No accounts using the default password (`is_default_password: true`)
- [ ] All service accounts have clearly named purposes
- [ ] No service accounts with `Administrator` role where `StorageOperator` would suffice
- [ ] All human user accounts are LDAP-mapped (not local), except the break-glass admin
- [ ] Break-glass admin password is stored in PAM vault, not known to individuals

### Remove a Stale Service Account

```bash
# List accounts to identify the stale one
curl -k -X GET "https://<mgmt-ip>/api/rest/user/local?select=id,name,role_name" \
  -H "DELL-EMC-TOKEN: <token>"

# Delete the stale account
curl -k -X DELETE "https://<mgmt-ip>/api/rest/user/local/<user-id>" \
  -H "DELL-EMC-TOKEN: <token>"
```

## Host Access Control

### Host and Host Group Isolation

PowerStore maps volumes to hosts via host objects and host groups. Access control at the storage layer depends on correct host configuration:

- **One host object per physical host**: never share a host object between unrelated servers
- **Host groups for clusters**: ESXi cluster members share a host group; all cluster members see the same volumes
- **Host group isolation by security zone**: production and dev/test host groups must never share volumes

```bash
# List all host-to-volume mappings
curl -k -X GET "https://<mgmt-ip>/api/rest/host_volume_mapping?select=host_id,volume_id,logical_unit_number" \
  -H "DELL-EMC-TOKEN: <token>"

# Audit: find any volume mapped to more than one host group
# (potential cross-zone access — should only occur for intentionally shared volumes)
curl -k -X GET "https://<mgmt-ip>/api/rest/host_volume_mapping?select=volume_id,host_id" \
  -H "DELL-EMC-TOKEN: <token>" | python3 -c "
import sys, json
from collections import defaultdict
data = json.load(sys.stdin)
vol_hosts = defaultdict(list)
for m in data:
    vol_hosts[m['volume_id']].append(m['host_id'])
for vol, hosts in vol_hosts.items():
    if len(hosts) > 1:
        print(f'Volume {vol} is mapped to {len(hosts)} hosts: {hosts}')
"
```

### Fibre Channel Access Control

For FC-attached hosts, access control depends on correct SAN zoning in addition to PowerStore host objects. PowerStore only presents a volume to a host if both conditions are met:

1. The host's WWN is in the PowerStore host object (initiator registered)
2. The host's WWN is zoned to the PowerStore target port in the SAN fabric

Verify zoning is correct for each host:

```bash
# On Brocade FC switch — verify zone membership
# switch:admin> zoneshow "ZONE_LON01-ESX01_PSTORE01"

# On Cisco MDS FC switch
# switch# show zoneset active

# Confirm PowerStore target port WWNs
curl -k -X GET "https://<mgmt-ip>/api/rest/fc_port?select=name,wwn,current_speed,node_id" \
  -H "DELL-EMC-TOKEN: <token>"
```

### iSCSI CHAP Authentication

For iSCSI-attached hosts, enforce CHAP authentication to prevent unauthorised iSCSI initiators from connecting.

```bash
# Configure mutual CHAP on an iSCSI host in PowerStore
curl -k -X PATCH "https://<mgmt-ip>/api/rest/host_initiator/<initiator-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "chap_mutual_username": "host-chap-username",
    "chap_mutual_password": "<chap-password-min-12-chars>"
  }'
```

On the Linux iSCSI initiator:

```bash
# /etc/iscsi/iscsid.conf — enable CHAP
node.session.auth.authmethod = CHAP
node.session.auth.username = host-chap-username
node.session.auth.password = <chap-password>

# For mutual CHAP (PowerStore authenticates to the host)
node.session.auth.username_in = <target-chap-username>
node.session.auth.password_in = <target-chap-password>
```

## NFS Export Access Control

NFS exports are controlled by host IP allow lists in the PowerStore NFS export configuration. Always specify the narrowest set of allowed hosts:

```bash
# Review NFS export access rules
curl -k -X GET "https://<mgmt-ip>/api/rest/nfs_export?select=name,rw_hosts,ro_hosts,no_access_hosts" \
  -H "DELL-EMC-TOKEN: <token>"

# Restrict an NFS export to specific subnet (update existing export)
curl -k -X PATCH "https://<mgmt-ip>/api/rest/nfs_export/<export-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "rw_hosts": [{"ip": "192.168.20.0", "prefix_length": 24}],
    "ro_hosts": [],
    "no_access_hosts": [],
    "min_security": "sys"
  }'
```

NFS export security levels:

| Security Level | Description | Use |
|---|---|---|
| `sys` | Standard Unix UID/GID-based access; no encryption | Standard for trusted internal networks |
| `krb5` | Kerberos authentication; no integrity or encryption | Authenticates client identity |
| `krb5i` | Kerberos with integrity checking | Prevents packet tampering |
| `krb5p` | Kerberos with full encryption | Maximum security; impacts performance |

## SMB Share Access Control

SMB shares use Windows ACLs. Share-level permissions are configured in PowerStore; file-level ACLs are managed via standard Windows tools (Security tab, icacls, PowerShell).

```bash
# Review SMB shares
curl -k -X GET "https://<mgmt-ip>/api/rest/smb_share?select=name,path,filesystem_id,is_continuous_availability_enabled" \
  -H "DELL-EMC-TOKEN: <token>"
```

Best practices:

- Grant `Full Control` share permission to the `Domain Admins` group and `Change` or `Read` to named groups — never grant `Full Control` to `Everyone`
- Use AD security groups for share access, not individual user accounts
- Enable Continuous Availability (CA) for shares hosting Hyper-V VMs or SQL Server data on SMB 3.x

## Access Review Checklist (Quarterly)

| Check | Action |
|---|---|
| All local accounts reviewed | Confirm no unused local accounts; rotate service account passwords |
| All LDAP group mappings reviewed | Confirm group-to-role mappings are current; remove stale groups |
| Service account roles reviewed | Confirm no service account has Administrator where StorageOperator suffices |
| Host objects reviewed | Confirm no host objects contain stale initiators from decommissioned servers |
| Host group memberships reviewed | Confirm production and dev/test host groups are properly separated |
| NFS export access reviewed | Confirm all exports restrict access to the intended subnets |
| SMB share permissions reviewed | Confirm no shares grant access to `Everyone` or `Authenticated Users` with write |
| Volume mappings reviewed | Confirm no cross-zone volume mappings exist between production and non-production hosts |

---

## See also

- [Powerstore — Authentication](authentication/)
- [Powerstore — Hardening](hardening/)
- [Powerstore — Encryption](encryption/)
