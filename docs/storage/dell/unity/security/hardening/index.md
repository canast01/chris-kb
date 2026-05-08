# Unity — Hardening

## Hardening Overview

Apply these hardening steps to all Unity deployments before handing over to production operations. Each step reduces the attack surface, limits privilege exposure, or ensures audit trails are in place.

## Hardening Checklist

| Category | Control | How to Verify |
|---|---|---|
| Credentials | Change default admin password on first login | Confirm password meets policy; store in secrets manager |
| Credentials | Rename or restrict built-in admin account | Avoid predictable account names for privileged access |
| Transport | Disable TLS 1.0 and 1.1 | `openssl s_client -connect <ip>:443 -tls1` should fail |
| Transport | Enforce TLS 1.2 or higher | `openssl s_client -connect <ip>:443 -tls1_2` should succeed |
| Protocols | Disable FTP on management interfaces | `uemcli /sys/security show | grep ftp` |
| Protocols | Disable Telnet on management interfaces | `uemcli /sys/security show | grep telnet` |
| Protocols | Disable unused SP ports (FC, iSCSI) | Unisphere > **System > Hardware > Ports** |
| Access | Restrict management access to known subnets | Unisphere > **Settings > Security > Management Interfaces** |
| Access | Implement RBAC — no shared administrator accounts | `uemcli /user show` — each operator has an individual account |
| Access | Integrate LDAP/AD — no local accounts for operational use | `uemcli /user/ldap show` |
| Encryption | Enable D@RE on all flash and SAS SED pools | `uemcli /stor/config/pool show -detail | grep encrypt` |
| Encryption | CHAP for iSCSI (mutual where supported) | `uemcli /remote/host show -detail | grep chap` |
| Encryption | NFS Kerberos for sensitive NFS exports | `uemcli /prot/nfs show -detail | grep security` |
| Audit | Enable syslog forwarding to SIEM | `uemcli /sys/syslog show` |
| Audit | Enable email alerting for CRITICAL and ERROR alerts | Unisphere > **Settings > Alerts > Email Notifications** |
| Support | Enable SupportAssist (ESRS) | Unisphere > **Settings > Support > SupportAssist** |
| Patching | Run current recommended OE version | `uemcli /sys/sw show` |
| Certificates | Replace self-signed management certificate (optional, for regulated environments) | Unisphere > **Settings > Security > Certificates** |

## Credentials

### Default Admin Password

Change the built-in `admin` password immediately after first login. The factory default password is documented in Dell's installation guides and is publicly known.

```bash
# Change the admin password
uemcli -d <ip> -u admin /user -name admin set -passwd "NewStrongPassword1!"
```

Requirements for a strong password:
- Minimum 16 characters.
- Mix of uppercase, lowercase, digits, and special characters.
- Not based on dictionary words, product names, or predictable patterns.
- Store in a secrets manager (HashiCorp Vault, CyberArk, or equivalent). Do not store in spreadsheets or plain-text files.

### Service Account Accounts

For LDAP integration and automation scripts:

- Use dedicated service accounts for LDAP bind operations — do not use personal accounts or domain admin accounts.
- Assign the minimum role necessary: most monitoring and automation needs only **Operator** or **Storage Administrator** — not **Administrator**.
- Rotate service account credentials at least annually or after any personnel change.

## Transport Security

### Disabling TLS 1.0 and 1.1

TLS 1.0 and 1.1 contain known vulnerabilities (POODLE, BEAST) and have been deprecated by all major standards bodies. Disable them explicitly.

In Unisphere: **Settings > Security > TLS Settings**

```bash
# Set minimum TLS version (varies by OE version; consult release notes)
uemcli -d <ip> -u admin /sys/security set -tlsMinVersion TLSv1_2

# Verify TLS version after change (from a separate Linux host)
openssl s_client -connect <sp-ip>:443 -tls1    2>&1 | grep -E "handshake|alert"
openssl s_client -connect <sp-ip>:443 -tls1_1  2>&1 | grep -E "handshake|alert"
openssl s_client -connect <sp-ip>:443 -tls1_2  2>&1 | grep "CONNECTED"
```

### Replacing the Self-Signed Management Certificate

By default, Unity uses a self-signed certificate for the Unisphere HTTPS management interface. For production environments, replace this with a certificate signed by your internal CA or a commercial CA:

1. Generate a Certificate Signing Request (CSR) in Unisphere: **Settings > Security > Certificates > Generate CSR**.
2. Submit the CSR to your CA and obtain a signed certificate.
3. Import the signed certificate: **Settings > Security > Certificates > Import Certificate**.
4. Verify the certificate is applied: access Unisphere via HTTPS and confirm the browser shows the correct certificate.

Replacing the certificate eliminates certificate warnings for operators and allows certificate pinning in monitoring tools.

## Protocol Restrictions

### Disabling FTP and Telnet

Unity management interfaces may optionally support FTP and Telnet for legacy compatibility. Both protocols transmit credentials in plain text and must be disabled.

In Unisphere: **Settings > Security > Management Protocols**

```bash
# Verify current management protocol configuration
uemcli -d <ip> -u admin /sys/security show -detail | grep -E "ftp|telnet|ssh"
```

Only SSH and HTTPS should be enabled for management access.

### Disabling Unused Host Ports

Unused FC or iSCSI host ports expose additional attack surface. If specific SFP-equipped ports are permanently unused, consider:

1. Not installing SFPs in unused port bays.
2. Tracking unused ports in your asset inventory and reviewing quarterly.
3. If software-level port disable is supported, disable the port in Unisphere: **System > Hardware > Storage Processors > [SP] > Ports**.

```bash
# List all FC ports and their status
uemcli -d <ip> -u admin /net/port/fc show -detail

# List all iSCSI ports and their status
uemcli -d <ip> -u admin /net/port/eth show -detail
```

## Management Access Restrictions

Restrict which source IP addresses can access Unity management interfaces. Only the storage management VLAN, jump hosts, and monitoring servers should have access.

In Unisphere: **Settings > Security > Management Interfaces**

Configuration approach:
- Define an allowlist of management source subnets.
- Block access from production workload VLANs.
- Verify the restriction does not block SupportAssist outbound connectivity — SupportAssist uses HTTPS outbound to Dell; incoming management access restrictions do not affect it.

```bash
# Show current management interface configuration
uemcli -d <ip> -u admin /net/if show -detail | grep -i mgmt
```

## Alerting and Monitoring

Configure email and SNMP alerting to ensure all security-relevant events are actioned promptly.

### Email Notifications

In Unisphere: **Settings > System > Notifications > Email**

Configure email alerts for:
- **CRITICAL** severity: immediate on-call notification.
- **ERROR** severity: within-hours response.
- **WARNING** severity: daily digest review.

```bash
# List configured email notification rules
uemcli -d <ip> -u admin /sys/email show

# Create an email notification
uemcli -d <ip> -u admin /sys/email create \
    -smtpServer mail.corp.local \
    -smtpPort 25 \
    -toList storage-alerts@corp.local \
    -fromAddress unity-alerts@corp.local
```

### SNMP

```bash
# Configure SNMP v2c
uemcli -d <ip> -u admin /sys/snmp create \
    -version v2c \
    -community public \
    -addr <snmp_manager_ip>

# Configure SNMP v3 (recommended over v2c)
uemcli -d <ip> -u admin /sys/snmp create \
    -version v3 \
    -username snmpmonitor \
    -authProto SHA \
    -authPasswd "AuthPassword1!" \
    -privProto AES \
    -privPasswd "PrivPassword1!" \
    -addr <snmp_manager_ip>

# List SNMP configuration
uemcli -d <ip> -u admin /sys/snmp show
```

Use SNMP v3 with authentication and privacy (authPriv) in all environments. SNMP v2c community strings are transmitted in plain text and are vulnerable to interception.

## SupportAssist (ESRS)

SupportAssist (formerly ESRS/SRS) enables Dell to proactively monitor Unity health, auto-create cases for hardware faults, and provide remote diagnostic access when requested.

```bash
# Check SupportAssist status
uemcli -d <ip> -u admin /sys/esrs show

# Enable SupportAssist
uemcli -d <ip> -u admin /sys/esrs set -enabled true

# Send a test heartbeat to verify connectivity to Dell
uemcli -d <ip> -u admin /sys/esrs callhome -type heartbeat
```

SupportAssist does not provide Dell with unrestricted access to the array. Remote diagnostic sessions require explicit acceptance from an administrator before Dell support can connect.

## OE Patching

Run the current recommended Unity OE version. Outdated OE versions contain known security vulnerabilities and bugs that are fixed in later releases.

```bash
# Check current OE version
uemcli -d <ip> -u admin /sys/sw show

# Check for available upgrades (if connected to Dell network via SupportAssist)
# Unisphere > Maintenance > Software Upgrades > Check for Updates
```

Maintain a Unity OE upgrade cadence:
- Apply security-focused patch releases within 90 days of availability.
- Apply major OE version upgrades within the lifecycle support window.
- Review Dell Security Advisories for Unity at [https://www.dell.com/support/security](https://www.dell.com/support/security).

## Compliance Notes

| Standard | Unity Capability | Key Controls |
|---|---|---|
| FIPS 140-2 | Unity OE uses FIPS 140-2 validated cryptographic modules; FIPS mode available | Enable FIPS mode in Unisphere > Settings > Security |
| DISA STIG | Dell publishes Unity STIGs for DoD environments | Download from DISA STIG Viewer; apply applicable findings |
| PCI DSS | D@RE, TLS enforcement, RBAC, audit logging, and network segmentation support PCI DSS controls | Controls span multiple requirement areas; map Unity capabilities to PCI scope boundary |
| HIPAA | Encryption at rest and in transit, access logging, and RBAC support HIPAA technical safeguards | Document encryption and access control as part of your HIPAA technical safeguard evidence |
| ISO 27001 | Unity's RBAC, audit logging, and encryption controls support multiple ISO 27001 Annex A controls | Map Unity controls to your ISMS in the Statement of Applicability |

For regulated environments, supplement Unity's built-in controls with:
- Network segmentation (dedicated storage VLAN with ACLs).
- Vulnerability scanning of the management interface IPs.
- Quarterly review of Unity user accounts and role assignments.
- Annual penetration testing of the storage management network segment.
