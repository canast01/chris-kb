---
tags:
  - dell
  - security
description: "Hardening reference covering Overview, Unisphere Hardening, Solutions Enabler Hardening, Host Connectivity Hardening, SupportAssist and Remote Access..."
---
# PowerMax — Hardening

<div class="kb-summary">
Hardening reference covering Overview, Unisphere Hardening, Solutions Enabler Hardening, Host Connectivity Hardening, SupportAssist and Remote Access Hardening and 3 more sections.

*Applies to: PowerMax 2500 / 8500*
</div>
![PowerMax — Hardening](../../../../../assets/storage-dell-powermax-security-hardening.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Overview

PowerMax hardening focuses on three areas: securing the management interfaces (Unisphere and Solutions Enabler), securing replication and host connectivity, and reducing the attack surface through configuration discipline. PowerMax is a closed, purpose-built appliance — the hardening surface is primarily the management plane, not the array OS itself which is not directly user-accessible.

![Overview](../../../../../assets/storage-dell-powermax-security-hardening-mermaid-svg.svg)

## Unisphere Hardening

### Authentication Hardening

```bash
# 1. Disable the default local 'smc' admin account after LDAP is configured
# Unisphere → Settings → Security → Users → smc → Disable

# 2. Enforce LDAP/AD as primary authentication
# Unisphere → Settings → Security → LDAP Configuration → Enable

# 3. Configure session timeout
# Unisphere → Settings → Security → Session Management
# - Idle timeout: 15 minutes
# - Max session duration: 8 hours

# 4. Test LDAP before disabling local accounts
ldapsearch -H ldaps://ldap.corp.example.com:636 \
  -D "CN=svc-powermax,OU=Service Accounts,DC=corp,DC=example,DC=com" \
  -w 'password' -b "DC=corp,DC=example,DC=com" "(sAMAccountName=<test_user>)"
```


```text title="Expected output"
# extended LDIF
#
# LDAPv3
# base <DC=corp,DC=example,DC=com> with scope subtree
# filter: (sAMAccountName=<test_user>)
# requesting: All userApplicationAttributes
#

dn: CN=Test User,OU=Users,DC=corp,DC=example,DC=com
objectClass: person
objectClass: organizationalPerson
objectClass: user
cn: Test User
sAMAccountName: test_user
userPrincipalName: test_user@corp.example.com
mail: test_user@corp.example.com
memberOf: CN=PowerMax-Admins,OU=Groups,DC=corp,DC=example,DC=com

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked in Active Directory.
    **`Can't contact LDAP server (-1)`** — Confirm the LDAP server hostname/IP is resolvable and port 636 is open from the Unisphere management network.
    **`No such object (32)`** — Ensure the base DN "DC=corp,DC=example,DC=com" matches your Active Directory domain structure exactly.
### TLS Hardening

```bash
# Verify TLS 1.0 and 1.1 are disabled (both should fail)
openssl s_client -connect <unisphere-host>:8443 -tls1   2>&1 | grep -i "failure\|error"
openssl s_client -connect <unisphere-host>:8443 -tls1_1 2>&1 | grep -i "failure\|error"

# Verify TLS 1.2 is functional
openssl s_client -connect <unisphere-host>:8443 -tls1_2 2>&1 | grep -i "Protocol"

# Enumerate active cipher suites — check for weak ciphers
nmap --script ssl-enum-ciphers -p 8443 <unisphere-host>
# Remove any ciphers rated 'C' or lower by nmap
# Acceptable: ECDHE-RSA-AES256-GCM-SHA384, ECDHE-RSA-AES128-GCM-SHA256
# Reject: RC4, 3DES, EXPORT, NULL

# Configure TLS settings in Unisphere:
# Settings → Security → TLS Configuration
# - Minimum Version: TLS 1.2
# - Disabled: TLS 1.0, TLS 1.1
# - Preferred ciphers: GCM-based AEAD suites
```


```text title="Expected output"
depth=0 C = US, ST = California, L = San Jose, O = Dell EMC, CN = unisphere-prod-01.corp.local
verify error:num=20:unable to get local issuer certificate
verify return:1
CONNECTED(00000001)
139876543210496:error:1409E0E5:SSL routines:SSL_CTX_set_tlsext_host_name:tlsv1 alert protocol version:../ssl/statem/statem_clnt.c:1089:
SSL_ERROR_SSL
139876543210496:error:14094410:SSL routines:SSL_CTX_set_cipher_list:sslv3 alert handshake failure:../ssl/statem/statem_clnt.c:1089:
SSL_ERROR_SSL

Protocol  : TLSv1.2
Cipher    : ECDHE-RSA-AES256-GCM-SHA384
Session-ID: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6

Starting Nmap 7.92 ( https://nmap.org ) at 2024-01-15 14:32:15 UTC
Nmap scan report for unisphere-prod-01.corp.local (192.168.1.45)
Host is up (0.0042s latency).

PORT     STATE SERVICE
8443/tcp open  https-alt

| ssl-enum-ciphers:
|   TLSv1.2:
|     ECDHE-RSA-AES256-GCM-SHA384 (256 bits) - A
|     ECDHE-RSA-AES128-GCM-SHA256 (128 bits) - A
|     ECDHE-RSA-CHACHA20-POLY1305 (256 bits) - A
|_    DHE-RSA-AES256-GCM-SHA384 (256 bits) - A

Nmap done at 2024-01-15 14:32:18 UTC; 1 IP address (1 host up) scanned in 3.12 seconds
```

!!! warning "Common errors"
    **`SSL_ERROR_SSL:14094410:SSL routines:SSL_CTX_set_cipher_list:sslv3 alert handshake failure`** — Verify the Unisphere host is reachable on port 8443 and the hostname resolves correctly with `nslookup <unisphere-host>`.
    **`unable to get local issuer certificate`** — Add the Unisphere CA certificate to your system's trusted store with `sudo cp unisphere-ca.pem /etc/ssl/certs/ && sudo update-ca-certificates`.
    **`Nmap done; 0 hosts up`** — Ensure the Unisphere host is online and firewall rules permit outbound connections to port 8443 from your scanning host.
### Certificate Hardening

Replace the factory-installed self-signed certificate before going into production:

```bash
# Step 1: Generate a private key and CSR on the Unisphere vApp
openssl req -new -newkey rsa:4096 -nodes \
  -keyout /tmp/unisphere.key \
  -out /tmp/unisphere.csr \
  -subj "/C=GB/ST=London/O=Example Corp/OU=Storage/CN=unisphere.corp.example.com" \
  -addext "subjectAltName=DNS:unisphere.corp.example.com,IP:192.168.1.100"

# Step 2: Submit CSR to internal CA; receive signed certificate chain

# Step 3: Import into Unisphere
# Settings → Security → Certificates → Import Certificate
# Upload: signed certificate + private key + CA chain

# Step 4: Restart Unisphere web service (may happen automatically after import)
systemctl restart dell-unisphere    # or equivalent on the vApp OS

# Step 5: Verify new certificate is in use
echo | openssl s_client -connect <unisphere-host>:8443 2>/dev/null \
  | openssl x509 -noout -issuer -subject -dates
```


```text title="Expected output"
Generating RSA private key, 4096 bit long modulus (2 primes)
.....................................................................+++++
.......................................................................+++++
e is 65537 (0x010001)

Redirecting to /bin/systemctl restart dell-unisphere
dell-unisphere.service: Stopped.
dell-unisphere.service: Started.

subject=C = GB, ST = London, O = Example Corp, OU = Storage, CN = unisphere.corp.example.com
issuer=C = GB, O = Example Corp, CN = Example Corp Root CA
notBefore=Jan 15 10:23:45 2025 GMT
notAfter=Jan 15 10:23:45 2026 GMT
```

!!! warning "Common errors"
    **`error: /tmp/unisphere.key: No such file or directory`** — Ensure /tmp has write permissions and sufficient disk space; run `ls -ld /tmp` to verify.
    **`unable to load certificate`** — Verify the certificate file is in PEM format and the CA chain is appended in correct order (leaf → intermediate → root) using `openssl x509 -in <cert> -text -noout`.
    **`Connection refused`** — Wait 30–60 seconds after service restart for Unisphere to fully initialize, then retry the s_client command.
| Certificate Parameter | Requirement |
|---|---|
| Key size | RSA 4096 or ECDSA P-256/P-384 |
| Signature algorithm | SHA-256 or stronger |
| SAN (Subject Alternative Name) | Must include the FQDN and IP address used to access Unisphere |
| Validity period | Maximum 2 years (398 days for public CAs) |
| Renewal trigger | 30 days before expiry — monitor with cron or a cert management tool |

### Network Access Hardening

Restrict access to the Unisphere management port (8443) at the network level:

```bash
# Firewall rules — limit Unisphere access to management subnet only
# Example: Linux firewalld on the Unisphere host
firewall-cmd --zone=public --add-rich-rule=\
  'rule family="ipv4" source address="192.168.10.0/24" port protocol="tcp" port="8443" accept' --permanent
firewall-cmd --zone=public --add-rich-rule=\
  'rule family="ipv4" port protocol="tcp" port="8443" drop' --permanent
firewall-cmd --reload

# Verify only management hosts can reach port 8443
nc -zv <management-host-ip> 8443   # should succeed
nc -zv <untrusted-host-ip> 8443    # should fail/timeout
```


```text title="Expected output"
success
success
success
Connection to 192.168.10.45 8443 port [tcp/https] succeeded!
nc: connect to 192.168.10.200 port 8443 (tcp) failed: Connection refused
```

!!! warning "Common errors"
    **`Error: INVALID_RULE`** — Verify the rich rule syntax matches firewalld XML format and escape special characters correctly with backslashes.
    **`nc: connect to <management-host-ip> port 8443 (tcp) failed: Connection refused`** — Confirm Unisphere service is running on the target host with `systemctl status unisphere` and that port 8443 is listening via `netstat -tlnp | grep 8443`.
## Solutions Enabler Hardening

### SYMAPI Daemon Hardening

```bash
# 1. Restrict daemon access to management hosts only
# /var/symapi/config/netcnfg — use SECURE flag and limit by SID
cat > /var/symapi/config/netcnfg <<'EOF'
SYMAPI_SERVER - 192.168.1.10 - 000123456789 - 2707 SECURE
SYMAPI_SERVER - 192.168.1.11 - 000987654321 - 2707 SECURE
EOF

# 2. Restrict daemon_users to named accounts only — no wildcards for admin
cat > /var/symapi/config/daemon_users <<'EOF'
storadm      StorageAdmin   192.168.10.0/24
secadm       SecurityAdmin  192.168.10.0/24
monitor_svc  Monitor        192.168.20.50
root         Administrator  127.0.0.1
EOF

# 3. Remove 'any' / '*' entries for powerful roles
grep -E "Administrator|StorageAdmin" /var/symapi/config/daemon_users | grep '\*'
# If this returns entries, replace '*' with specific IP ranges

# 4. Restart SE daemon after changes
systemctl restart storsrvd

# 5. Verify daemon is listening only on expected interfaces
netstat -tlnp | grep 2707
```


```text title="Expected output"
SYMAPI_SERVER - 192.168.1.10 - 000123456789 - 2707 SECURE
SYMAPI_SERVER - 192.168.1.11 - 000987654321 - 2707 SECURE
tcp        0      0 192.168.1.10:2707      0.0.0.0:*               LISTEN      4521/storsrvd
tcp        0      0 192.168.1.11:2707      0.0.0.0:*               LISTEN      4521/storsrvd
```

!!! warning "Common errors"
    **`grep: /var/symapi/config/daemon_users: No such file or directory`** — Ensure the netcnfg file is written first and the /var/symapi/config directory exists; create it with `mkdir -p /var/symapi/config` if needed.
    **`Failed to restart storsrvd: Unit storsrvd.service not found.`** — Verify the correct daemon name with `systemctl list-units | grep stor` and use the actual service name (may be `Symmetrix` or `emc-storsrvd` depending on version).
    **`netstat: command not found`** — Install net-tools with `apt-get install net-tools` or use `ss -tlnp | grep 2707` as a modern alternative.
### SE Host OS Hardening

The Solutions Enabler host (typically a Linux VM) requires its own OS hardening:

```bash
# Lock down SE installation directory permissions
chmod 750 /usr/symcli/bin
chmod 750 /var/symapi/config
chmod 640 /var/symapi/config/daemon_users
chmod 640 /var/symapi/config/netcnfg
chown root:storadm /var/symapi/config/daemon_users
chown root:storadm /var/symapi/config/netcnfg

# Restrict SYMCLI binaries — only the storadm service account should execute them
chown root:storadm /usr/symcli/bin/sym*
chmod 750 /usr/symcli/bin/sym*

# Audit who has access to SYMCLI
grep -E "storadm|symcli" /etc/sudoers /etc/sudoers.d/*
```


```text title="Expected output"
/etc/sudoers:storadm ALL=(ALL) NOPASSWD: /usr/symcli/bin/symcli
/etc/sudoers.d/powermax-admin:storadm ALL=(ALL) NOPASSWD: /usr/symcli/bin/sym*
/etc/sudoers.d/powermax-admin:%storadm ALL=(ALL) NOPASSWD: /usr/symcli/bin/symacl
/etc/sudoers.d/powermax-admin:%storadm ALL=(ALL) NOPASSWD: /usr/symcli/bin/symdev
/etc/sudoers.d/powermax-admin:%storadm ALL=(ALL) NOPASSWD: /usr/symcli/bin/symrdf
```

!!! warning "Common errors"
    **`grep: /etc/sudoers.d/*: No such file or directory`** — Create the `/etc/sudoers.d/` directory with `mkdir -p /etc/sudoers.d/` if it does not exist, or adjust the grep pattern to `grep -r "storadm\|symcli" /etc/sudoers* 2>/dev/null`.
    **`chown: changing ownership of '/usr/symcli/bin/sym*': No such file or directory`** — Verify the SYMCLI package is installed with `rpm -qa | grep symcli` and install it if missing before applying ownership changes.
    **`chmod: cannot access '/var/symapi/config/daemon_users': No such file or directory`** — Ensure the Symmetrix SE daemon is installed and initialized with `symcfg discover` to create the required configuration files.
### Logging and Audit on SE Host

```bash
# Enable auditd on the SE host to track SYMCLI execution
systemctl enable auditd
systemctl start auditd

# Add audit rules to track SYMCLI executions
cat >> /etc/audit/rules.d/powermax.rules <<'EOF'
# Track all SYMCLI command executions
-a always,exit -F dir=/usr/symcli/bin -F perm=x -F auid>=1000 -F auid!=4294967295 -k symcli
# Track changes to SE config files
-w /var/symapi/config/daemon_users -p wa -k se_config
-w /var/symapi/config/netcnfg -p wa -k se_config
EOF

augenrules --load

# Verify audit rules are active
auditctl -l | grep symcli
```


```text title="Expected output"
Created symlink /etc/systemd/system/multi-user.target.wants/auditd.service → /etc/systemd/system/auditd.service.
(no output — command completes silently)
(no output — command completes silently)
Loading rules from /etc/audit/rules.d/powermax.rules
No rules loaded
-a always,exit -F dir=/usr/symcli/bin -F perm=x -F auid>=1000 -F auid!=4294967295 -k symcli
```

!!! warning "Common errors"
    **`augenrules: No such file or directory`** — Install audit-libs package with `yum install audit-libs` or use `auditctl -R /etc/audit/rules.d/powermax.rules` directly instead.
    **`Error: audit rules directory does not exist: /etc/audit/rules.d`** — Create the directory with `mkdir -p /etc/audit/rules.d` before appending rules.
    **`No rules loaded`** — Restart auditd with `systemctl restart auditd` after loading rules to activate them in the kernel.
## Host Connectivity Hardening

### Zoning and Initiator Group Isolation

```bash
# Principle: each host's initiator group should contain only that host's WWNs
# Never share an initiator group between hosts with different security classifications

# Verify no initiator group contains WWNs from multiple different hosts
# (requires cross-referencing with the SAN fabric zone database)
symaccess list -sid <SID> -type initiator -v \
  > /tmp/ig_audit_$(date +%Y%m%d).txt

# Check for unusually large initiator groups (may indicate shared/misconfigured IG)
symaccess list -sid <SID> -type initiator | awk 'NR>2 && $NF > 4 {print $0}'

# Verify zones match initiator groups (SAN fabric side)
# On Brocade:
# switch:admin> zoneshow | grep <wwn>
# On Cisco MDS:
# switch# show zone member <wwn>
```


```text title="Expected output"
Symmetrix ID: 000297900001

                              Initiator Group
                              ---------------
Name                          Type       Flags  Num WWNs
----                          ----       -----  --------
host-prod-01-ig               Fibre      (*)         2
host-prod-02-ig               Fibre      (*)         2
host-dev-03-ig                Fibre             1
host-backup-04-ig             Fibre      (*)         3
shared-legacy-ig              Fibre             6

host-prod-01-ig               Fibre      (*)         2
  50:00:09:73:a4:2e:1b:c0
  50:00:09:73:a4:2e:1b:c1

host-backup-04-ig             Fibre      (*)         3
  50:00:09:73:a4:2e:1b:d2
  50:00:09:73:a4:2e:1b:d3
  50:00:09:73:a4:2e:1b:d4

shared-legacy-ig              Fibre             6
  50:00:09:73:a4:2e:1b:e0
  50:00:09:73:a4:2e:1b:e1
  50:00:09:73:a4:2e:1b:e2
  50:00:09:73:a4:2e:1b:e3
  50:00:09:73:a4:2e:1b:e4
  50:00:09:73:a4:2e:1b:e5

shared-legacy-ig              Fibre             6
host-backup-04-ig             Fibre      (*)         3
```

!!! warning "Common errors"
    **`SYMCLI_ERROR (5): The specified Symmetrix does not exist`** — Verify the SID value matches your array's actual Symmetrix ID using `symcfg list -v`.
    **`awk: syntax error: unexpected newline or statement`** — Correct the awk syntax; use `awk 'NR>2 && $NF > 4 {print $0}'` with proper field separator if needed.
### Port Group Isolation

```bash
# Separate port groups for different security zones (e.g., production vs dev/test)
# Production hosts should NOT share port groups with dev/test hosts

# List all port groups and their member ports
symaccess list -sid <SID> -type port -v

# Verify production port groups only contain production FA ports
symaccess show PROD_FABRIC_A_PG -sid <SID> -type port

# Identify any port groups with excessive member ports (may indicate misconfiguration)
symaccess list -sid <SID> -type port | awk 'NR>2 {print $1}' | while read pg; do
  ports=$(symaccess show "$pg" -sid <SID> -type port 2>/dev/null | grep -c "Dir\|Port" || echo 0)
  echo "$pg: $ports ports"
done | sort -t: -k2 -rn | head -10
```


```text title="Expected output"
Symmetrix ID: 000297900001

                                Port Group Name
                                ================
                           PROD_FABRIC_A_PG
                           PROD_FABRIC_B_PG
                           DEV_TEST_FABRIC_PG
                           DR_FABRIC_PG
                           BACKUP_FABRIC_PG

Director:Port                                  Port Group
===========                                    ==========
FA-1e:4                                        PROD_FABRIC_A_PG
FA-1e:5                                        PROD_FABRIC_A_PG
FA-2e:4                                        PROD_FABRIC_B_PG
FA-2e:5                                        PROD_FABRIC_B_PG

PROD_FABRIC_A_PG: 24 ports
BACKUP_FABRIC_PG: 18 ports
DR_FABRIC_PG: 16 ports
PROD_FABRIC_B_PG: 14 ports
DEV_TEST_FABRIC_PG: 8 ports
```

!!! warning "Common errors"
    **`symaccess: Error: Invalid Symmetrix ID <SID>`** — Replace `<SID>` with the actual Symmetrix serial number (e.g., `000297900001`) or use `-sid all` to query all arrays.
    **`symaccess: Error: Port group <name> not found`** — Verify the port group name exists with `symaccess list -sid <SID> -type port` and check for typos or case sensitivity.
### Unused Object Cleanup

Regularly remove stale masking views, initiator groups, and port groups from decommissioned hosts:

```bash
# Find masking views with no current host logins (potential orphans)
# Step 1: Get all initiator groups referenced in masking views
symaccess list -sid <SID> view | awk 'NR>2 {print $2}' | sort -u > /tmp/igs_in_mvs.txt

# Step 2: Get all initiator groups that have active host logins
symaccess -sid <SID> list logins | awk '{print $4}' | sort -u > /tmp/igs_with_logins.txt

# Step 3: Find IGs in masking views but with no active logins
diff /tmp/igs_with_logins.txt /tmp/igs_in_mvs.txt | grep "^>" | awk '{print $2}'
# Review each result — these are IGs (and their masking views) with no current fabric logins

# Remove stale masking view after confirming host is decommissioned
symaccess delete view <stale_mv_name> -sid <SID>
symaccess delete -sid <SID> -name <stale_ig_name> -type initiator
```


```text title="Expected output"
symaccess list -sid 000123456789 view | awk 'NR>2 {print $2}' | sort -u > /tmp/igs_in_mvs.txt
symaccess -sid 000123456789 list logins | awk '{print $4}' | sort -u > /tmp/igs_with_logins.txt
IG_prod_web_01
IG_legacy_db_02
IG_test_app_03
symaccess delete view MV_legacy_db_02_prod -sid 000123456789
Masking view MV_legacy_db_02_prod deleted successfully.
symaccess delete -sid 000123456789 -name IG_legacy_db_02 -type initiator
Initiator group IG_legacy_db_02 deleted successfully.
```

!!! warning "Common errors"
    **`symaccess: Command not found`** — Ensure the PowerMax CLI tools are installed and the `$PATH` includes the Symantec/Dell EMC bin directory (typically `/opt/emc/SYMCLI/bin`).
    **`Error: Masking view MV_legacy_db_02_prod is still in use by active host connections`** — Verify the host is truly decommissioned by checking fabric logins with `symaccess list logins -sid <SID>` before deletion.
    **`Error: Initiator group IG_legacy_db_02 not found`** — Confirm the exact initiator group name using `symaccess list -sid <SID> -name IG_legacy_db_02 -type initiator` before attempting deletion.
## SupportAssist and Remote Access Hardening

SupportAssist enables Dell to proactively monitor the array and create automated service requests for hardware faults. It also enables remote support sessions.

```bash
# Verify SupportAssist configuration
# Unisphere → Connectivity → SupportAssist
# - Ensure the proxy server is configured (do not allow direct internet access)
# - Enable Connect Home: Yes (for proactive monitoring)
# - Restrict accepted connection types: Dell Support only (no third-party remote access)
```

| SupportAssist Setting | Recommended Value | Rationale |
|---|---|---|
| Connect Home | Enabled | Enables proactive monitoring and automated SR creation |
| Direct internet access | Disabled | Route through authenticated proxy |
| Proxy server | Corporate proxy with TLS inspection bypass for `dell.com` | Maintains outbound control and logging |
| Allowed inbound IP ranges | Dell support IP ranges only | Restrict who can initiate remote sessions |
| SRS Gateway (SRS-VE) | Deployed | Required for inbound remote sessions; provides DMZ isolation |

### Secure Remote Services (SRS-VE)

SRS Virtual Edition is a gateway appliance that proxies Dell remote support sessions through your DMZ, avoiding direct inbound internet access to the Unisphere management network:

```d2
direction: right

DELL_ENG: "Dell Support\nEngineer" {shape: rectangle}
DELL_CLOUD: "Dell SRS\nCloud Gateway" {shape: rectangle}
SRS_VE: "SRS-VE\n(DMZ VM" {shape: rectangle}
UNI_HOST: "Unisphere / SE Host\n(management network" {shape: rectangle}

DELL_ENG -> DELL_CLOUD
DELL_CLOUD -> SRS_VE
SRS_VE -> UNI_HOST
```

Deploy SRS-VE on a dedicated VM in the DMZ. The SRS-VE makes outbound connections to the Dell SRS cloud and allows inbound sessions only from authenticated Dell support engineers.

## Hardening Checklist

### Critical (Must Complete Before Production)

- [ ] Default `smc` account disabled; named admin accounts configured via LDAP
- [ ] LDAP/AD authentication configured and tested with at least two admin accounts
- [ ] Break-glass local admin account in privileged access vault (CyberArk, Thycotic, etc.)
- [ ] Self-signed certificate replaced with CA-signed certificate on Unisphere HTTPS
- [ ] TLS 1.0 and 1.1 disabled on Unisphere (port 8443)
- [ ] Unisphere session idle timeout set to 15 minutes
- [ ] SYMAPI `daemon_users` file restricts access to named accounts by IP range
- [ ] SYMAPI `netcnfg` configured with SECURE flag; only expected SIDs listed
- [ ] D@RE confirmed enabled (factory default — verify explicitly)
- [ ] SRDF encryption enabled on all RDF groups traversing untrusted networks
- [ ] SupportAssist configured with proxy (no direct internet); SRS-VE deployed
- [ ] Unisphere access restricted to management VLAN at network/firewall level

### Important (Complete Within 30 Days)

- [ ] Syslog/audit log forwarding configured to SIEM
- [ ] Alert thresholds configured in Unisphere (response time, port utilisation, pool capacity)
- [ ] CloudIQ registered and showing healthy status
- [ ] Initiator group review completed — no shared IGs between hosts with different security classifications
- [ ] Port group review — production and dev/test port groups separated
- [ ] SE host OS hardened: auditd enabled, SYMCLI binary permissions set, sudo restrictions applied
- [ ] Service accounts for integrations (Veeam, NetBackup, Ansible) using minimum-required roles
- [ ] Certificate expiry monitoring configured (alert at 30 days before expiry)

### Periodic (Quarterly or Annually)

- [ ] Quarterly access review — audit all masking views, initiator groups, and Unisphere user accounts
- [ ] Annual DR test — SRDF failover and failback; validate RTO/RPO
- [ ] Annual penetration test — include Unisphere REST API and SYMAPI daemon in scope
- [ ] Review and rotate all service account credentials
- [ ] Review Dell security advisories for PowerMaxOS and Solutions Enabler; apply patches
- [ ] KMIP key rotation (if using external key management)
- [ ] Review and purge stale snapshots, orphaned masking views, and unused port groups

## Compliance Mapping

| Framework | Control | PowerMax Hardening Action |
|---|---|---|
| PCI-DSS v4.0 | Req 2.2: System components configured to prevent known security vulnerabilities | Disable TLS 1.0/1.1; replace self-signed cert; disable default `smc` account |
| PCI-DSS v4.0 | Req 7: Restrict access to cardholder data by business need | RBAC roles; masking view isolation; IG-per-host principle |
| PCI-DSS v4.0 | Req 8: Identify users and authenticate access | LDAP/AD authentication; named accounts; no shared credentials |
| PCI-DSS v4.0 | Req 10: Log and monitor all access | Audit log to SIEM; retain 12 months |
| NIST 800-53 | AC-2: Account Management | Disable default accounts; review quarterly; rotate service account creds |
| NIST 800-53 | AC-3: Access Enforcement | RBAC; masking view isolation |
| NIST 800-53 | AU-2: Event Logging | Audit log to SIEM; `symaudit` + `symevent` forwarding |
| NIST 800-53 | CM-7: Least Functionality | Remove unused masking views and port groups; restrict SYMAPI by IP |
| NIST 800-53 | IA-5: Authenticator Management | Rotate passwords; enforce complexity via AD policy |
| ISO 27001:2022 | A.8.2: Privileged access rights | Separate `StorageAdmin` and `SecurityAdmin` roles; review quarterly |
| ISO 27001:2022 | A.8.5: Secure authentication | LDAP/AD + MFA via jump server; session timeout |
| CIS Controls v8 | CIS 4: Secure Configuration | Hardening checklist above; periodic review |
| CIS Controls v8 | CIS 5: Account Management | Named accounts; quarterly review; disable stale accounts |

## Vulnerability Management

Monitor Dell security advisories for PowerMax components:

| Component | Advisory Source | Check Frequency |
|---|---|---|
| PowerMaxOS | Dell Security Advisories: https://www.dell.com/support/security | Monthly |
| Solutions Enabler | Same as above | Monthly |
| Unisphere for PowerMax | Same as above | Monthly |
| Unisphere vApp OS (embedded Linux) | Dell releases patched vApp versions | Per major release |

When a security advisory is published:
1. Assess applicability (is your array at the affected code level?).
2. Review workarounds if a patch is not immediately available.
3. Plan and schedule the patch/upgrade within the risk-appropriate timeframe (critical: within 30 days; high: within 60 days; medium: within 90 days).
4. Test the patch in a non-production environment first if available.
5. Document the patch application in the change management system.

---

## See also

- [Powermax — Authentication](../authentication/)
- [Powermax — Access Control](../access-control/)
- [Powermax — Encryption](../encryption/)
