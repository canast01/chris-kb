# Unity — Authentication

## Active Directory / LDAP

Unity supports LDAP/AD integration for two distinct purposes:

| Integration | Purpose | Configuration |
|---|---|---|
| Unisphere AD authentication | Admin users log in to Unisphere with AD credentials | Unisphere: **Settings > Access > Directory Services** |
| NAS server AD domain join | CIFS/SMB shares use AD for share permissions and Kerberos auth | `uemcli /net/nas/ad join` per NAS server |

For CIFS/SMB, each NAS server must be independently joined to the AD domain with a machine account in the appropriate OU. Ensure the NAS server's DNS is configured to resolve the domain controllers.

## Audit Logging

Unity OE records all administrative actions — login/logout, configuration changes, and alert acknowledgements — in an audit log.

**Viewing the audit log:**

In Unisphere, navigate to **System > Events** to review recent administrative events. The event log can be filtered by severity and time range.

**Syslog forwarding for SIEM integration:**

```bash
# Create a syslog destination for audit log forwarding
uemcli -d <sp_ip> -u admin -p <password> /sys/syslog create \
  -addr <syslog_server_ip> -protocol udp -port 514 -facility local0

# Confirm the syslog configuration
uemcli -d <sp_ip> -u admin -p <password> /sys/syslog show
```

Retain audit log data for a minimum of 90 days. For regulated environments (PCI DSS, SOX, HIPAA), ensure the syslog destination retains logs for the required compliance period.
