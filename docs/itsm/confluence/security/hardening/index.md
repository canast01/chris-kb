---
tags:
  - confluence
  - security
---
# Confluence — Hardening

```yaml
Administrator account policy:
- Maximum 3–4 accounts in confluence-administrators
- All admin accounts use LDAP/SSO — no local admin accounts (except break-glass)
- One break-glass local admin account stored in PAM vault; reviewed monthly
- Admin accounts must not be shared — one account per person
- Admin accounts reviewed and recertified quarterly
- Admin sessions expire after 60–120 minutes (configure via session timeout)
```

```bash
# Verify user registration is disabled via REST
curl -u admin:password \
  "https://confluence.example.local/rest/api/settings/lookandfeel" \
  | python3 -m json.tool | grep "registrationEnabled"
```
```yaml
Plugin policy:
- Only install plugins from the Atlassian Marketplace (verified by Atlassian)
- All new plugins require a security review before installation in production
- Review publisher trust level, data handling claims, and permissions required
- Disable or remove unused plugins — fewer plugins = smaller attack surface
- Keep all installed plugins updated (security patches)
- Plugins that require Confluence REST API tokens should use service accounts, not admin accounts
```
```bash
# Some built-in plugins can be disabled if not needed:
# Administration > Manage Apps > filter by "System"
# Plugins that can be disabled if not used:
# - Confluence Mobile Plugin (if mobile access not required)
# - Office Connector (if Office doc editing not used)
# - Team Calendars (if not licensed)

# Check installed and enabled plugins via REST
curl -u admin:password \
  "https://confluence.example.local/rest/plugins/1.0/?os_authType=basic" \
  | python3 -m json.tool | grep -E "\"key\"|\"enabled\"|\"version\""
```

```text title="Expected output"
{
  "key": "com.atlassian.confluence.plugins.confluence-mobile-plugin",
  "enabled": true,
  "version": "8.2.1"
}
{
  "key": "com.atlassian.confluence.plugins.office-connector",
  "enabled": true,
  "version": "5.4.3"
}
{
  "key": "com.atlassian.confluence.plugins.team-calendars",
  "enabled": false,
  "version": "4.1.8"
}
{
  "key": "com.atlassian.confluence.plugins.confluence-content-formatting-macros",
  "enabled": true,
  "version": "8.2.1"
}
{
  "key": "com.atlassian.confluence.plugins.confluence-default-user-macros",
  "enabled": true,
  "version": "8.2.1"
}
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl to skip certificate verification, or import the self-signed cert into your system's CA bundle. |
    | `jq: command not found` | Install `jq` package (`apt-get install jq` or `yum install jq`) as an alternative to `python3 -m json.tool` for better JSON parsing. |
    | `HTTP 401 Unauthorized` | Verify the admin credentials are correct and the user has API access permissions in Confluence administration settings. |
```bash
# Disable automatic plugin updates in production (require manual review)
# Administration > Manage Apps > Settings > Disable automatic updates

# Restrict UPM to administrators only (default — verify not changed)
# Administration > Manage Apps > no "Allow any logged-in user to install plugins" option

# Scan for outdated plugins
curl -u admin:password \
  "https://confluence.example.local/rest/plugins/1.0/?os_authType=basic" \
  | python3 -m json.tool | grep -E "\"key\"|\"latestVersion\"|\"version\""
```
```yaml
Audit log settings:
- Coverage level: Advanced (captures more detail than Base)
- Retention: 12 months minimum
- Export: Regularly export to SIEM for long-term retention (audit logs in Confluence are not immutable)
```
```bash
# Export audit log via REST API (paginated)
curl -u admin:password \
  "https://confluence.example.local/rest/api/audit?limit=1000&startDate=$(date -d '-1 day' +%Y-%m-%dT00:00:00.000+0000)" \
  -H "Content-Type: application/json" \
  | python3 -m json.tool >> /var/log/confluence-audit-export.json

# Forward to SIEM via rsyslog
# /etc/rsyslog.d/confluence-audit.conf
module(load="imfile")
input(type="imfile"
  File="/var/log/confluence-audit-export.json"
  Tag="confluence-audit"
  Severity="info"
  Facility="local6")

local6.*  @@siem.example.local:514
```

```text title="Expected output"
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2847k  100 2847k    0     0   1.2M      0  0:00:02  0:00:02 --:--:--  0:00:02
{
  "results": [
    {
      "createdDate": 1704067200000,
      "author": {
        "username": "admin",
        "userKey": "557058:a1b2c3d4-e5f6-7890-abcd-ef1234567890"
      },
      "summary": "User jsmith created page 'Security Policy v2.1'",
      "description": "Page created in space SEC",
      "objectType": "page",
      "objectName": "Security Policy v2.1"
    },
    {
      "createdDate": 1704053800000,
      "author": {
        "username": "svc-backup",
        "userKey": "557058:f7g8h9i0-j1k2-3456-lmno-pq7890123456"
      },
      "summary": "Backup export completed",
      "description": "Full space backup initiated",
      "objectType": "space"
    }
  ],
  "size": 2,
  "limit": 1000,
  "start": 0
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `curl: (60) SSL certificate problem: self signed certificate` | Add `-k` flag to curl or import the self-signed certificate into the system CA bundle. |
    | `jq: parse error: Invalid numeric literal at line 1 column 10` | Verify the API response is valid JSON by testing `curl -u admin:password "https://confluence.example.local/rest/api/audit?limit=10"` directly first. |
    | `rsyslog: imfile: cannot open file '/var/log/confluence-audit-export.json'` | Ensure the file exists and rsyslog process has read permissions; create it with `touch /var/log/confluence-audit-export.json && chmod 644 /var/log/confluence-audit-export.json`. |
```bash
# /opt/atlassian/confluence/confluence/WEB-INF/urlrewrite.xml
# Restrict access to admin URLs from management IPs only
# (Implement at reverse proxy level for better control)
```
```nginx
# Nginx — restrict Confluence admin paths to management IPs
location /admin {
    allow 10.10.10.0/24;   # Management VLAN
    allow 10.10.20.5;      # Jump host
    deny all;
    proxy_pass http://127.0.0.1:8090;
    # ... proxy headers ...
}

location /rest/admin {
    allow 10.10.10.0/24;
    deny all;
    proxy_pass http://127.0.0.1:8090;
}
```
```bash
# /opt/atlassian/confluence/bin/setenv.sh — JVM hardening options
JVM_SUPPORT_RECOMMENDED_ARGS="
  -Dfile.encoding=UTF-8
  -Djava.security.egd=file:/dev/./urandom
  -XX:+DisableExplicitGC
  -Djdk.tls.rejectClientInitiatedRenegotiation=true
"

# /opt/atlassian/confluence/conf/server.xml — disable Tomcat server info header
# Add to <Connector> element:
# server="Apache"   (obfuscate Tomcat version)

# Disable Tomcat default pages (host-manager, manager)
# Remove or restrict in /opt/atlassian/confluence/conf/server.xml:
# <Host name="localhost" ... >
#   Remove manager and host-manager Context entries
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `setenv.sh: Permission denied` | Run `chmod +x /opt/atlassian/confluence/bin/setenv.sh` to make the script executable before sourcing it. |
    | `server.xml: No such file or directory` | Verify Confluence installation path with `ls -la /opt/atlassian/confluence/conf/` and confirm the correct CONFLUENCE_HOME directory. |
    | `Tomcat fails to start after server.xml edit` | Validate XML syntax with `xmllint /opt/atlassian/confluence/conf/server.xml` before restarting the service. |
```bash
# Run Confluence as a dedicated non-root service account
# Create service account
useradd -r -s /sbin/nologin -m -d /opt/atlassian confluence

# Restrict Confluence home directory
chmod 750 /var/atlassian/application-data/confluence
chown -R confluence:confluence /var/atlassian/application-data/confluence
chown -R confluence:confluence /opt/atlassian/confluence

# Restrict log directory
chmod 700 /var/atlassian/application-data/confluence/logs
chown confluence:root /var/atlassian/application-data/confluence/logs

# Firewall — Confluence should not be directly internet-facing; reverse proxy handles 443
# Allow only the reverse proxy to reach Tomcat port 8090
iptables -A INPUT -p tcp --dport 8090 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 8090 -j DROP
```

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Confluence — Authentication](../authentication/)
- [Confluence — Access Control](../access-control/)
- [Confluence — Encryption](../encryption/)
