# ServiceNow — Access Control


<div class="kb-summary">
ServiceNow access control is enforced through Access Control Lists (ACLs), Roles, Groups, and data segmentation. The model is additive — access is denied by default unless an ACL explicitly grants it.
</div>

---

## Access Control Architecture

```text
┌────────────────────────────────────── ServiceNow Access Control ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      ACL Evaluation Order                                     │   │
│   │            Deny-all default → explicit allow rules → role check → condition script            │   │
│   │                     Evaluated: table ACL → field ACL → row-level condition                    │   │
│   │                      Operations: read / write / create / delete / execute                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                Role Hierarchy                │                                                    │
│   │             admin (full access)              │                                                    │
│   │             itil (service desk)              │                                                    │
│   │          catalog (service catalog)           │                                                    │
│   │          approver_user (approvals)           │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │              Group-Based Access             │   │
│                                                     │           Users assigned to groups          │   │
│                                                     │            Groups assigned roles            │   │
│                                                     │              LDAP/AD group sync             │   │
│                                                     │          Dynamic groups via script          │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · LDAP servers for group sync · IdP for SSO role mapping                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ACL        = Access Control List; rule on table/field controlling who can do what                    │
│  Role       = named permission set; assigned to users or groups                                       │
│  itil       = core service management role; access to incidents, problems, changes                    │
│  admin      = full platform access; should be restricted to named individuals                         │
│  Group      = collection of users; roles assigned at group level for scale                            │
│  Condition  = ACL script returning true/false; allows row-level access logic                          │
│  Deny-all   = ServiceNow default; nothing accessible unless explicitly permitted                      │
│  LDAP sync  = imports group membership from AD; keeps ServiceNow roles in sync                        │
│  Row-level  = ACL condition evaluating current record fields; per-record access                       │
│  execute    = ACL operation type for scripts and UI actions                                           │
│  catalog    = role for self-service portal; can order items, view own requests                        │
│  approver   = role enabling approval tasks; does not grant broader ITSM access                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── ServiceNow Access Control ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      ACL Evaluation Order                                     │   │
│   │            Deny-all default → explicit allow rules → role check → condition script            │   │
│   │                     Evaluated: table ACL → field ACL → row-level condition                    │   │
│   │                      Operations: read / write / create / delete / execute                     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                Role Hierarchy                │                                                    │
│   │             admin (full access)              │                                                    │
│   │             itil (service desk)              │                                                    │
│   │          catalog (service catalog)           │                                                    │
│   │          approver_user (approvals)           │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │              Group-Based Access             │   │
│                                                     │           Users assigned to groups          │   │
│                                                     │            Groups assigned roles            │   │
│                                                     │              LDAP/AD group sync             │   │
│                                                     │          Dynamic groups via script          │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · LDAP servers for group sync · IdP for SSO role mapping                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ACL        = Access Control List; rule on table/field controlling who can do what                    │
│  Role       = named permission set; assigned to users or groups                                       │
│  itil       = core service management role; access to incidents, problems, changes                    │
│  admin      = full platform access; should be restricted to named individuals                         │
│  Group      = collection of users; roles assigned at group level for scale                            │
│  Condition  = ACL script returning true/false; allows row-level access logic                          │
│  Deny-all   = ServiceNow default; nothing accessible unless explicitly permitted                      │
│  LDAP sync  = imports group membership from AD; keeps ServiceNow roles in sync                        │
│  Row-level  = ACL condition evaluating current record fields; per-record access                       │
│  execute    = ACL operation type for scripts and UI actions                                           │
│  catalog    = role for self-service portal; can order items, view own requests                        │
│  approver   = role enabling approval tasks; does not grant broader ITSM access                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

// List members of a group
var groupName = 'SNOW-Administrators';
var groupRecord = new GlideRecord('sys_user_group');
groupRecord.addQuery('name', groupName);
groupRecord.query();
if (groupRecord.next()) {
    var memberRec = new GlideRecord('sys_user_grmember');
    memberRec.addQuery('group', groupRecord.sys_id);
    memberRec.query();
    while (memberRec.next()) {
        gs.info(memberRec.user.name + ' (' + memberRec.user.user_name + ')');
    }
}
```text

---

## Access Control Lists (ACLs)

ACLs define who can perform which operations on which data. Navigate to: System Security → Access Control (ACL).

### ACL Structure

```yaml
Name:       <operation>_<table>_<field>
Operation:  read, write, create, delete, execute
Object:     Table name (e.g., incident, change_request)
Name:       * (all fields) or specific field name
Type:       record (row-level) or field-level
```

### Example ACL Configurations

**Restrict delete on Incidents to admins only:**

```javascript
// ACL Rule
// Name: delete_incident
// Operation: delete
// Table: incident
// Active: true
// Roles: admin, itil_admin

// Condition (Script):
(function() {
    return gs.hasRole('admin') || gs.hasRole('itil_admin');
})()
```

**Field-level ACL — hide salary field from non-HR:**

```javascript
// Name: read_sys_user.salary
// Operation: read
// Table: sys_user
// Field: salary
// Roles: hr_admin, admin

// Condition:
gs.hasRole('hr_admin') || gs.hasRole('admin')
```

**Record-level ACL — users can only see their own requests:**

```javascript
// Name: read_sc_request (self-only)
// Operation: read
// Table: sc_request
// Condition script:
(function() {
    return current.requested_for == gs.getUserID() ||
           gs.hasRole('itil') ||
           gs.hasRole('admin');
})()
```

### Auditing ACLs

```javascript
// Script to list all ACLs granting admin access
var aclRec = new GlideRecord('sys_security_acl');
aclRec.addQuery('admin_overrides', true);
aclRec.query();
while (aclRec.next()) {
    gs.info('ACL: ' + aclRec.name + ' | Operation: ' + aclRec.operation);
}

// List ACLs with no role restriction (potentially open)
var openAcl = new GlideRecord('sys_security_acl');
openAcl.addNullQuery('roles');
openAcl.addQuery('active', true);
openAcl.query();
while (openAcl.next()) {
    gs.info('OPEN ACL: ' + openAcl.name + ' | ' + openAcl.operation);
}
```

---

## Data Segmentation

### Company / Domain Separation

For multi-tenant or multi-company instances, use domain separation:

- System Properties → `glide.sys.domain.access_check` = `true`
- Each record belongs to a domain
- Users in a domain can only see records in their domain (and parent domains)

```javascript
// Verify domain separation is active
gs.getProperty('glide.sys.domain.access_check') === 'true'
```

### Assignment Group Visibility

Restrict which assignment groups can be seen by non-admins:

```javascript
// ACL on sys_user_group — restrict group visibility
// Only return groups where the user is a member or the group is marked public
(function() {
    if (gs.hasRole('itil_admin') || gs.hasRole('admin')) return true;
    var member = new GlideRecord('sys_user_grmember');
    member.addQuery('user', gs.getUserID());
    member.addQuery('group', current.sys_id);
    member.query();
    return member.hasNext();
})()
```

---

## Privileged Access Management

### Elevated Privilege Workflow

For temporary admin access:

1. User submits SC Request: "Temporary Admin Access"
2. Manager + Security approves
3. Automated workflow adds user to `SNOW-Temp-Admins` group
4. Scheduled job removes from group after approved duration
5. All actions during temp access session logged to audit table

```javascript
// Scheduled job: Remove expired temp admin access
var tempAdmin = new GlideRecord('sys_user_grmember');
tempAdmin.addQuery('group.name', 'SNOW-Temp-Admins');
tempAdmin.addQuery('u_expiry_date', '<', new GlideDateTime());
tempAdmin.query();
while (tempAdmin.next()) {
    gs.info('Removing temp admin: ' + tempAdmin.user.name);
    tempAdmin.deleteRecord();
}
```

---

## Integration Access Control

### REST API Access by External Systems

| System | Role | Table Access | Method |
|---|---|---|---|
| Monitoring tool | Custom `svc_monitoring` | `incident` read | OAuth 2.0 |
| CMDB sync tool | Custom `svc_cmdb_sync` | `cmdb_ci_*` write | OAuth 2.0 |
| Change management UI | Custom `svc_change_api` | `change_request` read | OAuth 2.0 |
| Backup tool | Custom `svc_backup` | Read-only all | mTLS |

```javascript
// Create a custom minimal role for an integration
// System Definition → Roles → New
// Name: svc_monitoring_role
// Contains roles: (none)

// Then create ACLs granting only what this role needs:
// read incident: role = svc_monitoring_role
// read sys_user: role = svc_monitoring_role (name, email fields only)
```

---

## Access Review

### Quarterly Access Review Script

```javascript
// Run in Script Editor — export admin group membership
var report = [];
var adminGroup = new GlideRecord('sys_user_grmember');
adminGroup.addQuery('group.name', 'SNOW-Administrators');
adminGroup.orderBy('user.name');
adminGroup.query();
while (adminGroup.next()) {
    report.push({
        user: adminGroup.user.user_name.toString(),
        name: adminGroup.user.name.toString(),
        email: adminGroup.user.email.toString(),
        lastLogin: adminGroup.user.last_login.toString(),
        active: adminGroup.user.active.toString()
    });
}
gs.info(JSON.stringify(report, null, 2));
```

**Review checklist:**

- [ ] Admin group membership matches approved list
- [ ] No inactive users in any role-bearing group
- [ ] Service account roles are still necessary and minimal
- [ ] Temp access groups are empty (no expired grants remain)
- [ ] OAuth applications are still active integrations
- [ ] ACLs with `admin_overrides=true` are documented and justified
- [ ] Domain separation is active (if multi-company)
- [ ] MID Server account has only required roles

---

## Related Pages

- [ServiceNow — Authentication](../authentication/index.md)
- [ServiceNow — Encryption](../encryption/index.md)
- [ServiceNow — Hardening](../hardening/index.md)
