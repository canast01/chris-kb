---
tags:
  - jira
  - security
---
# Jira — Hardening

```bash
# Audit current Jira administrators
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/group/member?groupname=jira-administrators&maxResults=100" \
  | jq -r '.values[] | "\(.displayName) - \(.emailAddress)"'

# Cloud: audit administrators
curl -u "user@corp.example.com:API_TOKEN" \
  "https://your-org.atlassian.net/rest/api/3/group/member?groupname=jira-administrators" \
  | jq -r '.values[] | "\(.displayName) - \(.emailAddress)"'
```


```text title="Expected output"
Sarah Chen - sarah.chen@corp.example.com
Marcus Johnson - marcus.johnson@corp.example.com
DevOps Team Lead - devops-lead@corp.example.com
Jira Administrator - jira-admin@corp.example.com
Robert Williams - robert.williams@corp.example.com
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.corp.example.com port 443: Connection refused`** — Verify the Jira instance hostname is correct and the server is running and accessible from your network.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure your authentication token is valid and has API access permissions; an authentication failure returns HTML instead of JSON.
    **`curl: (401) Unauthorized`** — Replace `TOKEN` and `API_TOKEN` with valid credentials and verify the user account has permission to query group membership.
```bash
# List all installed plugins
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/plugins/1.0/" \
  | jq '.plugins[] | {key: .key, name: .name, version: .version, enabled: .enabled}'

# Identify plugins with vendor != Atlassian
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/plugins/1.0/" \
  | jq '.plugins[] | select(.vendor.name != "Atlassian") | {name: .name, vendor: .vendor.name}'
```

```text title="Expected output"
{
  "key": "com.atlassian.jira.plugins.jira-development-panel",
  "name": "Development Panel",
  "version": "1.0.0",
  "enabled": true
}
{
  "key": "com.atlassian.jira.plugins.jira-issue-collector-plugin",
  "name": "Issue Collector",
  "version": "5.0.7",
  "enabled": true
}
{
  "key": "com.example.custom-webhook-plugin",
  "name": "Custom Webhook Handler",
  "version": "2.3.1",
  "enabled": true
}
{
  "key": "com.marketplace.automation-rules",
  "name": "Automation Rules Pro",
  "version": "3.8.4",
  "enabled": false
}
...
{
  "name": "Custom Webhook Handler",
  "vendor": "Example Corp"
}
{
  "name": "Automation Rules Pro",
  "vendor": "Marketplace Vendor Inc"
}
{
  "name": "Advanced Reports",
  "vendor": "Third Party Labs"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or configure proper CA certificates in your environment.
    **`jq: error (at <stdin>:1): Cannot index string with string "plugins"`** — Verify the API endpoint is correct and the response is valid JSON; check that your TOKEN is not expired.
    **`curl: (401) Unauthorized`** — Ensure the admin credentials and TOKEN are correct, and verify the user has API access permissions in Jira.
```bash
# Disable a plugin
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/plugins/1.0/{plugin-key}-key/enabled" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  -d '{"enabled": false}'
```

```text title="Expected output"
{"enabled":false,"key":"com.atlassian.jira.plugins.jira-development-panel-plugin","name":"Development Panel","version":"2.4.1"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl or configure your system to trust the Jira server's certificate.
    **`{"errorMessages":["You do not have permission to administer Jira"]}`** — Ensure the admin user account has global administrator permissions and the API token is valid and not expired.
    **`curl: (7) Failed to connect to jira.corp.example.com port 443: Connection refused`** — Verify the Jira hostname and port are correct and the Jira instance is running and accessible from your network.
```bash
# Export audit log entries via API
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?limit=1000" \
  | jq '.records[] | {created, summary, category, objectItem: .objectItem.name, author: .authorKey}'

# Filter by category
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?category=USER_MANAGEMENT&limit=500"
```

```text title="Expected output"
{
  "created": "2024-01-15T09:23:47.123+0000",
  "summary": "User jsmith created",
  "category": "USER_MANAGEMENT",
  "objectItem": "jsmith",
  "author": "admin"
}
{
  "created": "2024-01-15T10:45:12.456+0000",
  "summary": "Group 'developers' updated",
  "category": "GROUP_MANAGEMENT",
  "objectItem": "developers",
  "author": "admin"
}
{
  "created": "2024-01-15T11:02:33.789+0000",
  "summary": "Permission scheme modified",
  "category": "PERMISSION_SCHEME",
  "objectItem": "Default Permission Scheme",
  "author": "sysadmin"
}
{
  "created": "2024-01-15T14:18:56.234+0000",
  "summary": "User jdoe deactivated",
  "category": "USER_MANAGEMENT",
  "objectItem": "jdoe",
  "author": "admin"
}
{
  "created": "2024-01-15T15:33:21.567+0000",
  "summary": "Project role updated",
  "category": "PROJECT_ROLE",
  "objectItem": "Project Lead",
  "author": "admin"
}
...
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to bypass SSL verification for self-signed certs, or import the certificate into your CA bundle.
    **`jq: parse error: (null) is not defined at line 1, column 0`** — Verify the API token is valid and the endpoint URL is correct; test with `curl -u "admin:TOKEN" https://jira.corp.example.com/rest/api/2/auditing/record -v` to see the actual response.
    **`401 Unauthorized`** — Ensure the API token has audit log read permissions and is not expired; regenerate the token in Jira user settings if needed.
```bash
# Forward Jira audit logs to SIEM (example: syslog export)
# Jira Data Center: catalina.out + audit logs in /var/atlassian/application-data/jira/log/

# Automated log shipping with rsyslog
cat >> /etc/rsyslog.d/jira.conf << 'EOF'
# Ship Jira access logs
input(type="imfile"
      File="/var/atlassian/application-data/jira/log/atlassian-jira-audit.log"
      Tag="jira-audit"
      Severity="info"
      Facility="local3")

local3.*  @siem.corp.example.com:514
EOF

systemctl restart rsyslog
```

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
● rsyslog.service - System Logging Service
     Loaded: loaded (/usr/lib/systemd/system/rsyslog.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2024-01-15 14:32:18 UTC; 2s ago
       Docs: man:rsyslog(8)
   Main PID: 8742 (rsyslog)
      Tasks: 3 (limit: 4915)
     Memory: 2.1M
        CPU: 45ms
     CGroup: /system.slice/rsyslog.service
             └─8742 /usr/sbin/rsyslog -n

Jan 15 14:32:18 jira-dc-01 systemd[1]: Started System Logging Service.
```

!!! warning "Common errors"
    **`/etc/rsyslog.d/jira.conf:1: error: syntax error on token "input" (line 1, column 1)`** — Verify rsyslog version supports RainerScript syntax (v7+); use legacy format `$ModLoad imfile` and `$InputFileName` if on older versions.
    **`rsyslog: action 'action 1': could not create socket for target!`** — Confirm SIEM server `siem.corp.example.com:514` is reachable and listening; test with `nc -zv siem.corp.example.com 514`.
    **`permission denied: /var/atlassian/application-data/jira/log/atlassian-jira-audit.log`** — Ensure rsyslog user (typically `syslog` or `root`) has read permissions on the Jira log directory; run `chmod 644 /var/atlassian/application-data/jira/log/atlassian-jira-audit.log`.
```bash
# Allow only required ports
# Inbound to Jira server
iptables -A INPUT -p tcp --dport 443 -s 0.0.0.0/0 -j ACCEPT  # HTTPS (via proxy)
iptables -A INPUT -p tcp --dport 8080 -s 10.0.0.0/8 -j ACCEPT # Internal only (proxy)
iptables -A INPUT -p tcp --dport 5701 -s 10.10.0.0/24 -j ACCEPT # Hazelcast cluster (nodes only)

# Deny all other inbound
iptables -A INPUT -j DROP

# Outbound: LDAPS to AD
iptables -A OUTPUT -p tcp --dport 636 -d 10.10.1.0/24 -j ACCEPT
# Outbound: SMTP
iptables -A OUTPUT -p tcp --dport 587 -d 10.10.2.50 -j ACCEPT
# Deny all other outbound
iptables -A OUTPUT -j DROP
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`iptables: No chain/target/match by that name`** — Ensure the iptables kernel module is loaded with `modprobe iptables_filter` before running rules.
    **`iptables: Bad rule (does a matching rule exist in that chain?)`** — Verify the exact syntax of port and CIDR notation; use `iptables -L -n` to inspect existing rules before appending duplicates.
    **`Warning: iptables-save does not support ipv6. Saving only ipv4 rules.`** — Add equivalent ip6tables rules or run `ip6tables -A INPUT -j DROP` to prevent IPv6 bypass of firewall policy.
```bash
# Disable issue votes if not used
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/api/2/configuration" \
  -H "Content-Type: application/json" \
  -d '{"votingEnabled": false, "watchingEnabled": false}'
```

```text title="Expected output"
{"self":"https://jira.corp.example.com/rest/api/2/configuration","votingEnabled":false,"watchingEnabled":false,"unassignedIssuesAllowed":true,"subTasksEnabled":true,"issueLinkingEnabled":true,"timeTrackingEnabled":true,"attachmentsEnabled":true,"lastModified":"2024-01-15T14:32:18.447+0000"}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to jira.corp.example.com port 443: Connection refused`** — Verify the Jira instance is running and accessible at the specified hostname/port, or check network/firewall rules.
    **`{"errorMessages":["You do not have permission to edit the system configuration"],"errors":{}}`** — Ensure the admin user has global system administrator permissions in Jira.
    **`curl: (35) OpenSSL SSL_connect: SSL: CERTIFICATE_VERIFY_FAILED in connection to jira.corp.example.com:443`** — Add `-k` flag to curl to skip SSL verification, or ensure the server's SSL certificate is trusted by the system.
```bash
# /opt/atlassian/jira/bin/setenv.sh — JVM hardening options
JAVA_OPTS="$JAVA_OPTS -Djava.awt.headless=true"
JAVA_OPTS="$JAVA_OPTS -Djava.security.egd=file:/dev/./urandom"
JAVA_OPTS="$JAVA_OPTS -Dfile.encoding=UTF-8"

# Disable HTTP TRACE method
JAVA_OPTS="$JAVA_OPTS -Dorg.apache.tomcat.util.http.HeaderParser=false"
```
```xml
<!-- server.xml — remove or secure connectors -->
<!-- Remove AJP connector (CVE-2020-1938 Ghostcat) -->
<!-- <Connector port="8009" protocol="AJP/1.3" redirectPort="8443" /> -->

<!-- Add security headers to ErrorReportValve -->
<Valve className="org.apache.catalina.valves.ErrorReportValve"
       showReport="false"
       showServerInfo="false"/>
```
```bash
# Check current Jira version
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/serverInfo" \
  | jq '{version, buildNumber, deploymentType}'

# Monitor Atlassian security advisories
# RSS: https://www.atlassian.com/trust/security/advisories/rss
# Email: security@atlassian.com notification list

# Check for known CVEs against installed version
# Reference: https://jira.atlassian.com/browse/JRASERVER (Data Center)
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

- [Jira — Authentication](../authentication/)
- [Jira — Access Control](../access-control/)
- [Jira — Encryption](../encryption/)
