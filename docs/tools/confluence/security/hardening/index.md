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
