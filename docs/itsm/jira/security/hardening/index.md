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
```bash
# Disable a plugin
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/plugins/1.0/{plugin-key}-key/enabled" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  -d '{"enabled": false}'
```
```bash
# Export audit log entries via API
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?limit=1000" \
  | jq '.records[] | {created, summary, category, objectItem: .objectItem.name, author: .authorKey}'

# Filter by category
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?category=USER_MANAGEMENT&limit=500"
```
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
```bash
# Disable issue votes if not used
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/api/2/configuration" \
  -H "Content-Type: application/json" \
  -d '{"votingEnabled": false, "watchingEnabled": false}'
```
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
