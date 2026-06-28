---
tags:
  - security
  - servicenow
---
# ServiceNow Access Control

```text

---

```d2
direction: down

auth: "ServiceNow\nAuthentication" {shape: rectangle}
access_control_lists_acls: "Access Control Lists (ACLs)" {shape: rectangle}
resources: Protected Resources {shape: cylinder}

auth -> access_control_lists_acls: grants
access_control_lists_acls -> resources: access
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Access Control Lists (ACLs)

ACLs define who can perform which operations on which data. Navigate to: System Security → Access Control (ACL).

### ACL Structure

```

```yaml
Name:       <operation>_<table>_<field>
Operation:  read, write, create, delete, execute
Object:     Table name (e.g., incident, change_request)
Name:       * (all fields) or specific field name
Type:       record (row-level) or field-level
```
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
```javascript
// Name: read_sys_user.salary
// Operation: read
// Table: sys_user
// Field: salary
// Roles: hr_admin, admin

// Condition:
gs.hasRole('hr_admin') || gs.hasRole('admin')
```
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
```javascript
// Verify domain separation is active
gs.getProperty('glide.sys.domain.access_check') === 'true'
```
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
```javascript
// Create a custom minimal role for an integration
// System Definition → Roles → New
// Name: svc_monitoring_role
// Contains roles: (none)

// Then create ACLs granting only what this role needs:
// read incident: role = svc_monitoring_role
// read sys_user: role = svc_monitoring_role (name, email fields only)
```
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

---

## See also

- [Servicenow — Authentication](../authentication/)
- [Servicenow — Hardening](../hardening/)
- [Servicenow — Encryption](../encryption/)
