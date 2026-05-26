# Jira — Hardening

Hardening Jira reduces the attack surface of the instance by disabling unnecessary features, tightening configuration, enforcing auditability, and controlling plugin exposure.

---

## Admin Account Hardening

### Principle of Least Admin

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
┌────────────────────────────────────────── Jira — Hardening ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                      Jira Hardening Guide                                     │   │
│   │               Disable public sign-up and anonymous access in global permissions               │   │
│   │              Restrict /secure/admin to corporate IP ranges via reverse proxy/WAF              │   │
│   │                  Apply Atlassian security advisories; stay within n-1 version                 │   │
│   │               Remove default admin account; named accounts with MFA via SAML IdP              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardening reduces attack surface at network, application, and OS layers                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Application Hardening             │  │             OS/Network Hardening            │   │
│   │             Disable anon access              │  │              Firewall: 443 only             │   │
│   │             Remove default admin             │  │              SSH key auth only              │   │
│   │            Disable public signup             │  │              SELinux enforcing              │   │
│   │               Enable audit log               │  │             Minimal OS packages             │   │
│   │              Plugin allow-list               │  │              OS patch schedule              │   │
│   │               Security headers               │  │             WAF for /admin path             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  WAF/reverse proxy · Jira VMs with SELinux · DB VM · firewall segmentation                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Public sign-up   = Admin > Global Permissions; remove Anyone can sign up                             │
│  Anonymous access = Admin > Global Permissions; remove Browse Projects for Anyone                     │
│  Security headers = CSP, X-Frame-Options, X-Content-Type-Options at proxy                             │
│  Plugin allow-list = Admin > Manage Apps; disable unsigned / unapproved plugins                       │
│  Audit log        = Admin > Audit Log; enable for all admin and config changes                        │
│  WAF              = Web Application Firewall; restrict /secure/admin to corp IPs                      │
│  SELinux          = enforcing mode on RHEL/CentOS; confines Tomcat process                            │
│  SSH key auth     = disable password SSH login on Jira server OS                                      │
│  n-1 version      = stay one version behind latest max; patch critical CVEs                           │
│  Default admin    = rename or delete; create named admin accounts                                     │
│  CSP              = Content-Security-Policy header; prevents cross-site scripting                     │
│  MFA              = multi-factor auth enforced at IdP; Jira trusts SAML assertion                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## System Configuration Hardening

### Administration → System → General Configuration

| Setting | Recommended Value |
|---|---|
| Base URL | `https://jira.corp.example.com` (HTTPS only) |
| Allow public signup | Disabled |
| Mode | Private |
| External user management | Enabled (if using AD/LDAP) |
| CAPTCHA on signup | Enabled (if signup is enabled) |
| Send email on new user | Disabled |
| Allow people to email into Jira | Disabled unless explicitly needed |
| Show user email addresses | Disabled (hide from non-admins) |

### Security Settings

Administration → System → Security Settings:

```properties
# jira-config.properties — additional security settings

# Disable WebSudo prompts after N minutes
jira.websudo.timeout=10

# Require re-authentication for admin actions
jira.websudo.is.disabled=false

# Content Security Policy header
jira.webresource.batching.enabled=true
```

**WebSudo** forces administrators to re-enter credentials before accessing admin areas — always leave enabled.

---

## Plugin and Marketplace Hardening

Marketplace plugins run with the same JVM privileges as Jira itself. Uncontrolled plugins are a major attack vector.

### Plugin Audit

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

### Plugin Controls

| Control | Action |
|---|---|
| Only approved plugins installed | Maintain approved plugin list in CMDB |
| Plugins reviewed before installation | Security review required |
| Universal Plugin Manager locked | Disable UPM on prod — deploy via change mgmt |
| Plugin updates tested in staging | Test in staging before prod |
| Unused plugins disabled | Disable or uninstall |

```bash
# Disable a plugin
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/plugins/1.0/{plugin-key}-key/enabled" \
  -H "Content-Type: application/vnd.atl.plugins+json" \
  -d '{"enabled": false}'
```

---

## Audit Logging

### Enabling Audit Log (Data Center)

Administration → System → Audit Log

| Event Category | Recommendation |
|---|---|
| User management | Enabled |
| Group management | Enabled |
| Project management | Enabled |
| Permission scheme changes | Enabled |
| Global configuration changes | Enabled |
| Plugin management | Enabled |
| Login/logout | Enabled |

```bash
# Export audit log entries via API
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?limit=1000" \
  | jq '.records[] | {created, summary, category, objectItem: .objectItem.name, author: .authorKey}'

# Filter by category
curl -u "admin:TOKEN" \
  "https://jira.corp.example.com/rest/api/2/auditing/record?category=USER_MANAGEMENT&limit=500"
```

### Audit Log Retention and SIEM Integration

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

**Retention requirements:**

| Log Type | Minimum Retention |
|---|---|
| Audit logs | 1 year |
| Access logs (nginx/proxy) | 90 days |
| Application logs | 30 days |
| Security incident logs | 3 years |

---

## Network Hardening

### Firewall Rules (Data Center)

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

### Disable Unused Jira Features

Administration → Issues → Issue Features:

```bash
# Disable issue votes if not used
curl -u "admin:TOKEN" \
  -X PUT \
  "https://jira.corp.example.com/rest/api/2/configuration" \
  -H "Content-Type: application/json" \
  -d '{"votingEnabled": false, "watchingEnabled": false}'
```

---

## JVM and Tomcat Hardening

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

---

## Hardening Checklist

| Control | Priority | Status |
|---|---|---|
| Public signup disabled | Critical | Check |
| WebSudo enabled | Critical | Check |
| Admin count ≤ 5 | Critical | Check |
| All admins have MFA | Critical | Check |
| LDAPS configured (not LDAP) | Critical | Check |
| TLS 1.2+ enforced at proxy | Critical | Check |
| HSTS header enabled | High | Check |
| Audit log enabled for all categories | High | Check |
| Audit logs shipped to SIEM | High | Check |
| Plugin install restricted | High | Check |
| Unused plugins disabled | High | Check |
| AJP connector disabled | High | Check |
| Default admin password changed | Critical | Check |
| User email addresses hidden | Medium | Check |
| X-Frame-Options SAMEORIGIN set | Medium | Check |
| CSP header configured | Medium | Check |
| Application link inventory current | Medium | Check |
| Attachment directory permissions | Medium | Check |
| Quarterly admin access review | High | Schedule |
| Penetration test annually | High | Schedule |

---

## Security Patching

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

**Patch policy:**

| Severity | Maximum Time to Patch |
|---|---|
| Critical (CVSS 9+) | 72 hours |
| High (CVSS 7–8.9) | 7 days |
| Medium (CVSS 4–6.9) | 30 days |
| Low (CVSS < 4) | Next maintenance window |

Notable historical CVEs requiring immediate patching: CVE-2021-26084 (OGNL injection), CVE-2022-26134 (OGNL injection RCE), CVE-2023-22515 (broken access control — Confluence but indicative of Atlassian risk).

---

## Related Pages

- [Jira — Authentication](../authentication/index.md)
- [Jira — Access Control](../access-control/index.md)
- [Jira — Encryption](../encryption/index.md)
