---
tags:
  - security
  - servicenow
---
# ServiceNow Hardening

```javascript
// Bulk verify critical properties via Script Editor
var criticalProps = {
  'glide.authenticate.sso.required': 'true',
  'glide.cookies.secure': 'true',
  'glide.cookies.httponly': 'true',
  'glide.http.ssl_check_cert': 'true',
  'glide.ui.escape_text': 'true'
};

Object.keys(criticalProps).forEach(function(prop) {
  var actual = gs.getProperty(prop);
  var expected = criticalProps[prop];
  var status = (actual === expected) ? 'OK' : 'FAIL';
  gs.info('[' + status + '] ' + prop + ': expected=' + expected + ' actual=' + actual);
});
```
```text
┌──────────────────────────────────────── ServiceNow Hardening ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │              Instance Hardening              │                                                    │
│   │            Disable unused plugins            │                                                    │
│   │           Remove demo/sample data            │                                                    │
│   │            Restrict public pages             │                                                    │
│   │          Set session timeout 30min           │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │              Network Hardening              │   │
│                                                     │            IP allowlist enforced            │   │
│                                                     │           Mutual TLS integrations           │   │
│                                                     │           Outbound firewall rules           │   │
│                                                     │             No direct DB access             │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │                User Hardening                │                                                    │
│   │            MFA all admin accounts            │                                                    │
│   │            Least-privilege roles             │                                                    │
│   │           Service accounts locked            │                                                    │
│   │           Dormant accounts purged            │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │               Change Hardening              │   │
│                                                     │         Update sets for all changes         │   │
│                                                     │           Dev→Test→Prod promotion           │   │
│                                                     │         Script review before deploy         │   │
│                                                     │          Business rule audit trail          │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS · WAF at edge · DDoS protection · SOC 24x7 monitoring                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Plugin      = optional capability; unused plugins expand attack surface unnecessarily                │
│  IP Allowlist= network policy restricting instance access to known source IP ranges                   │
│  Session timeout= auto-logout after inactivity; 30 minutes recommended for admin                      │
│  Update Set  = bundled configuration changes; promotes safely through environments                    │
│  Business Rule= server-side script triggered on record events; reviewed before deploy                 │
│  Least privilege= assign minimum roles required; no broad admin unless necessary                      │
│  mTLS        = mutual TLS; both client and server authenticate with certificates                      │
│  Demo data   = sample records shipped with plugins; must be removed in production                     │
│  Dormant acct= accounts inactive >90 days; disable then delete per policy                             │
│  WAF         = Web Application Firewall; blocks OWASP top-10 at ServiceNow edge                       │
│  ACL order   = deny-all default; explicit allow rules grant access to tables/fields                   │
│  Script review= security check of Business Rules/Client Scripts before promotion                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```javascript
// Verify that ServiceNow Store installs are disabled
gs.getProperty('com.snc.apps.enable_store')  // Should be 'false' for prod

// List all installed plugins
var plugins = new GlideRecord('v_plugin');
plugins.addQuery('active', true);
plugins.query();
while (plugins.next()) {
    gs.info('Plugin: ' + plugins.name + ' | ID: ' + plugins.id + ' | Version: ' + plugins.version);
}
```
```javascript
// Audit update sets deployed to production in last 30 days
var us = new GlideRecord('sys_update_set');
us.addQuery('state', 'complete');
us.addQuery('sys_updated_on', '>=', gs.daysAgoStart(30));
us.orderByDesc('sys_updated_on');
us.query();
while (us.next()) {
    gs.info('Update Set: ' + us.name + ' | By: ' + us.sys_updated_by + ' | On: ' + us.sys_updated_on);
}
```
```javascript
// BAD — vulnerable to GlideRecord injection
var query = "active=true^name=" + request.getParameter('name');
var gr = new GlideRecord('sys_user');
gr.addEncodedQuery(query);  // User-controlled input in query

// GOOD — use addQuery with explicit field binding
var name = request.getParameter('name');
if (name && /^[a-zA-Z0-9 \-\.]{1,100}$/.test(name)) {
    var gr = new GlideRecord('sys_user');
    gr.addQuery('name', name);   // Parameterised
    gr.query();
}
```
```javascript
// These APIs should be restricted in production — flag in code review:
// GlideRecord.deleteRecord() — destructive
// GlideSysAttachment.deleteAttachment() — destructive
// gs.executeNow() — immediate script execution
// new GlideHTTPClient() — outbound HTTP (SSRF risk if URL is user-controlled)

// Restrict: sys_script (Business Rules) — require admin to edit
// ACL: write sys_script — role: admin
// ACL: write sys_script_include — role: admin
```
```javascript
// Create a custom security audit entry
gs.securityAudit(
    'Custom security event',
    'Event details: ' + eventInfo,
    'tableName',
    recordSysId
);

// Query the security audit log
var auditRec = new GlideRecord('syslog_transaction');
auditRec.addQuery('category', 'security');
auditRec.addQuery('sys_created_on', '>=', gs.daysAgoStart(7));
auditRec.orderByDesc('sys_created_on');
auditRec.setLimit(100);
auditRec.query();
while (auditRec.next()) {
    gs.info(auditRec.sys_created_on + ' | ' + auditRec.user_name + ' | ' + auditRec.message);
}
```
```javascript
// Forward audit events to SIEM via outbound webhook
// Business Rule on syslog_transaction (after insert)
// Condition: category == 'security'

(function executeRule(current, previous) {
    var sm = new sn_ws.RESTMessageV2('SIEM-Webhook', 'send_event');
    sm.setHttpMethod('POST');
    sm.setRequestBody(JSON.stringify({
        timestamp: current.sys_created_on.toString(),
        user: current.user_name.toString(),
        event: current.message.toString(),
        category: current.category.toString(),
        source: 'servicenow'
    }));
    try {
        var response = sm.execute();
    } catch (ex) {
        gs.error('SIEM send failed: ' + ex.message);
    }
})(current, previous);
```
```javascript
// Add IP restriction for an integration endpoint
var ipRestrict = new GlideRecord('sys_ip_range');
ipRestrict.initialize();
ipRestrict.name = 'CMDB-Sync-Server';
ipRestrict.ip_address_start = '10.10.5.50';
ipRestrict.ip_address_end = '10.10.5.50';
ipRestrict.active = true;
ipRestrict.insert();
```
```javascript
// Verify basic auth is disabled for REST APIs
gs.getProperty('glide.basicauth.required')  // Should be 'false'

// Per REST API endpoint — disable basic auth
// System Web Services → Inbound → REST APIs
// Authentication: OAuth 2.0 required (not Basic)
```
```bash
# Run MID Server as a non-root service account
useradd -r -s /bin/false snow-mid
chown -R snow-mid:snow-mid /opt/servicenow/mid/

# MID Server config.xml — restrict to minimum required hosts
# <parameter name="mid.instance.url" value="https://<instance>.service-now.com"/>
# <parameter name="mid.capabilities" value="Scripting,Discovery,Integration"/>

# Firewall: MID Server outbound to ServiceNow only
iptables -A OUTPUT -p tcp --dport 443 \
  -d <instance>.service-now.com -j ACCEPT
iptables -A OUTPUT -j DROP

# Verify MID Server version is current
cat /opt/servicenow/mid/agent/glide-agent.properties | grep "build"
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Servicenow — Authentication](../authentication/)
- [Servicenow — Access Control](../access-control/)
- [Servicenow — Encryption](../encryption/)
