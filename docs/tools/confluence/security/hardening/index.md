# Confluence — Hardening


<div class="kb-summary">
Admin account hardening, plugin/marketplace control, audit log configuration, and security settings.
</div>

## System Administrator Account Hardening

The `confluence-administrators` group has full access to all spaces, settings, and user data. Its membership must be tightly controlled.

```yaml
Administrator account policy:
- Maximum 3–4 accounts in confluence-administrators
- All admin accounts use LDAP/SSO — no local admin accounts (except break-glass)
- One break-glass local admin account stored in PAM vault; reviewed monthly
- Admin accounts must not be shared — one account per person
- Admin accounts reviewed and recertified quarterly
- Admin sessions expire after 60–120 minutes (configure via session timeout)
```
```text
┌─────────────────────────────────────── Confluence — Hardening ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Confluence Hardening Guide                                  │   │
│   │                 Disable anonymous access and guest users in global permissions                │   │
│   │             Restrict /admin path to corp IP ranges via reverse proxy or WAF rules             │   │
│   │                Apply all Atlassian security advisories; keep within n-1 version               │   │
│   │               Remove default admin account; use named accounts with MFA via IdP               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Hardening reduces the attack surface across network, application, and OS layers                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Application Hardening             │  │             OS/Network Hardening            │   │
│   │             Disable anon access              │  │           Firewall: allow 443 only          │   │
│   │             Remove default admin             │  │              SSH key auth only              │   │
│   │           Enforce strong passwords           │  │             SELinux/AppArmor on             │   │
│   │              Audit log enabled               │  │             Minimal OS packages             │   │
│   │              Plugin allow-list               │  │             Regular OS patching             │   │
│   │          Headers: CSP/HSTS/X-Frame           │  │             WAF rules for /admin            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Reverse proxy (WAF) · Confluence VMs with SELinux · DB VM · firewall segmentation                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Anonymous access = global toggle; disable to require login for all page views                        │
│  CSP              = Content Security Policy header; prevents XSS by restricting script sources        │
│  X-Frame-Options  = HTTP header preventing clickjacking via iframe embedding                          │
│  WAF              = Web Application Firewall; inspects HTTP and blocks malicious requests             │
│  Plugin allow-list = restrict UPM to approved Marketplace apps; block unsigned plugins                │
│  Audit log        = Confluence Admin > Audit Log; records admin actions and permission changes        │
│  SELinux          = mandatory access control on RHEL/CentOS; enforcing mode recommended               │
│  AppArmor         = MAC on Debian/Ubuntu; profile-based confinement for Tomcat process                │
│  n-1 version      = stay within one major version behind latest; apply critical patches same-day      │
│  Default admin    = built-in admin account in fresh installs; rename and rotate password              │
│  SSH key auth     = disable password SSH; require public key for all admin access                     │
│  MFA              = enforced at IdP; admins must pass MFA before receiving SAML assertion             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql

## Security Configuration Hardening

Navigate to **General Configuration** > **Security Configuration**.

| Setting | Recommended Value | Reason |
|---|---|---|
| Allow people to sign up to create their own account | Disabled | Prevent unauthorised self-registration |
| Show system information in 500-error pages | Disabled | Prevent info disclosure |
| Show full name of user in page content | As required | Limit PII exposure |
| Secure cookies | Enabled | Prevent cookie theft over HTTP |
| Maximum Authentication Attempts | 5 | Lockout after brute force attempts |
| Enable XSRF protection | Enabled | Protect against cross-site request forgery |
| Enable HTTPS required for system administrator | Enabled | Force admin actions over HTTPS |

### Disable User Registration

```bash
# Verify user registration is disabled via REST
curl -u admin:password \
  "https://confluence.example.local/rest/api/settings/lookandfeel" \
  | python3 -m json.tool | grep "registrationEnabled"
```

## Plugin / Marketplace Control

Plugins (apps) extend Confluence functionality but can introduce security risks. All plugins run in the same JVM as Confluence with access to the same data.

### Plugin Management Policy

```yaml
Plugin policy:
- Only install plugins from the Atlassian Marketplace (verified by Atlassian)
- All new plugins require a security review before installation in production
- Review publisher trust level, data handling claims, and permissions required
- Disable or remove unused plugins — fewer plugins = smaller attack surface
- Keep all installed plugins updated (security patches)
- Plugins that require Confluence REST API tokens should use service accounts, not admin accounts
```

### Disable Unused Built-In Plugins

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

### UPM (Universal Plugin Manager) Security

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

## Audit Log Configuration

Confluence's audit log records significant administrative and content events.

### Enable and Configure Audit Logging

Navigate to **Administration** > **Audit Log** > **Configure**.

```yaml
Audit log settings:
- Coverage level: Advanced (captures more detail than Base)
- Retention: 12 months minimum
- Export: Regularly export to SIEM for long-term retention (audit logs in Confluence are not immutable)
```

### Key Events Captured by Audit Log

| Category | Events |
|---|---|
| Users | Login, logout, password change, account created/disabled |
| Groups | Group created/deleted, member added/removed |
| Permissions | Space permission granted/revoked, Global permission change |
| Spaces | Space created, archived, or deleted |
| Configuration | System configuration changed |
| Plugins | Plugin installed, enabled, disabled, or removed |
| Authentication | SAML/LDAP configuration changes |

### Export Audit Logs to SIEM

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

## Webwork / Request Filtering

Protect against common web attacks via the whitelist and request filtering.

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

## JVM and Tomcat Hardening

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

## Operating System Hardening for Confluence Host

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

## Hardening Checklist

| Control | Status Check |
|---|---|
| HTTPS enforced | `curl -I http://confluence.example.local` redirects to HTTPS |
| Anonymous access disabled | General Config > Global Permissions |
| User self-registration disabled | General Config > Security Configuration |
| Admin accounts < 5 | Count members of `confluence-administrators` |
| Audit log enabled (Advanced) | Administration > Audit Log > Configure |
| Unused plugins disabled | Manage Apps > filter by enabled status |
| Admin paths restricted by IP | Nginx/proxy config |
| Confluence runs as non-root | `ps aux | grep confluence` |
| TLS 1.0/1.1 disabled | `openssl s_client -connect host:443 -tls1` |
| Session timeout configured | General Config > Security Config |

## Quick Reference

| Topic | Location / Command |
|---|---|
| Security settings | General Configuration > Security Configuration |
| Admin group members | User Management > Groups > confluence-administrators |
| Audit log | Administration > Audit Log |
| Plugin management | Administration > Manage Apps |
| Audit log REST API | `GET /rest/api/audit?limit=1000` |
| Plugin list REST API | `GET /rest/plugins/1.0/` |
| Restrict admin URLs | Nginx `location /admin { allow ...; deny all; }` |
| Confluence service user | `ps aux | grep confluence` (should not be root) |
