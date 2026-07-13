---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
description: "Troubleshooting vCenter and ESXi login failures — SSO token errors, locked AD accounts, LDAP connectivity, NTP drift breaking Kerberos, and certificate..."
---
# Login and Access Issues

<div class="kb-summary">
Troubleshooting vCenter and ESXi login failures — SSO token errors, locked AD accounts, LDAP connectivity, NTP drift breaking Kerberos, and certificate validation failures.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
cannot_log_into_vcenter: "Cannot Log Into vCenter" {shape: rectangle}
ad_users_cannot_log_in: "AD Users Cannot Log In" {shape: rectangle}
local_admin_works_ad_users_cannot_lo: "Local Admin Works, AD Users Cannot Log In" {shape: rectangle}
permission_denied: "Permission Denied" {shape: rectangle}
session_timeout_constant_relogin_pro: "Session Timeout / Constant Re-Login Prompt" {shape: rectangle}
verify: "Verify" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> cannot_log_into_vcenter: investigate
symptom -> ad_users_cannot_log_in: investigate
symptom -> local_admin_works_ad_users_cannot_lo: investigate
symptom -> permission_denied: investigate
symptom -> session_timeout_constant_relogin_pro: investigate
symptom -> verify: investigate
cannot_log_into_vcenter -> resolution
ad_users_cannot_log_in -> resolution
local_admin_works_ad_users_cannot_lo -> resolution
permission_denied -> resolution
session_timeout_constant_relogin_pro -> resolution
verify -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Cannot Log Into vCenter

**Step 1 — Try the local SSO admin account** (`administrator@vsphere.local` or `administrator@<sso-domain>`). If this works but AD accounts cannot log in, the issue is with the identity source.

**Step 2 — Check vCenter SSO service health:**

```bash
# From VCSA shell — check all services
service-control --status --all | grep -v "STOPPED\|running" 

# Check specifically the SSO/authentication services
service-control --status vmware-sts-idmd
service-control --status vmware-sso

# Restart SSO services if they appear hung (will briefly interrupt all logins)
service-control --restart vmware-sso
service-control --restart vmware-sts-idmd
```


```text title="Expected output"
vmware-analytics-engine                                 STOPPED
vmware-cis-license                                      RUNNING
vmware-cm                                               STOPPED
vmware-eam                                              RUNNING
vmware-envoy                                            RUNNING
vmware-imagebuilder                                     STOPPED
vmware-mbcs                                             RUNNING
vmware-netdump                                          STOPPED
vmware-perfcharts                                       RUNNING
vmware-postgres                                         RUNNING
vmware-rhttpproxy                                       RUNNING
vmware-sso                                              RUNNING
vmware-sts-idmd                                         RUNNING
vmware-vapi-endpoint                                    RUNNING
vmware-vpxd                                             RUNNING
vmware-vpxd-svcs                                        RUNNING
vmware-vsan-health                                      STOPPED
...
Service vmware-sts-idmd is running.
Service vmware-sso is running.
Restarting vmware-sso...
Service vmware-sso stopped successfully.
Service vmware-sso started successfully.
Restarting vmware-sts-idmd...
Service vmware-sts-idmd stopped successfully.
Service vmware-sts-idmd started successfully.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Service vmware-sso is stopped.` | Run `service-control --start vmware-sso` to bring the service online before attempting restart. |
    | `Error: Unable to restart vmware-sts-idmd: Service dependency vmware-sso is not running.` | Ensure vmware-sso is started first, as vmware-sts-idmd depends on it. |
    | `grep: (standard input) is empty` | The grep filter is too restrictive; remove the filter or use `service-control --status --all` without piping to see all services. |
**Step 3 — Check for a locked account:**

```bash
# Check if the SSO admin account is locked
/usr/lib/vmware-vmafd/bin/dir-cli account find-by-name --account administrator --login administrator@vsphere.local
```


```text title="Expected output"
dn: cn=administrator,cn=users,dc=vsphere,dc=local
objectClass: user
userAccountControl: 512
cn: administrator
sAMAccountName: administrator
userPrincipalName: administrator@vsphere.local
pwdLastSet: 133298765432100000
accountExpires: 9223372036854775807
lockoutTime: 0
badPwdCount: 0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Cannot connect to directory service on localhost:389` | Verify the vCenter SSO service is running with `systemctl status vmware-vmafd` and check network connectivity to the SSO endpoint. |
    | `Error: [LDAP_INVALID_CREDENTIALS] Failed to authenticate as administrator@vsphere.local` | Ensure you are running the command as root or with appropriate permissions, and verify the SSO service credentials are correct. |
In vCenter UI (if another admin can log in): Administration → Single Sign-On → Users and Groups → check account status.

---

## AD Users Cannot Log In

**Step 1 — Verify the identity source is still connected:**

vCenter → Administration → Single Sign-On → Configuration → Identity Sources → click the AD source → Test Connection.

If the test fails:

```bash
# From VCSA shell — test LDAP connectivity to domain controller
ldapsearch -H ldap://<dc-ip>:389 -x -b "dc=domain,dc=com" "(objectClass=*)" dn 2>&1 | head -20

# Check if DNS resolves the domain
nslookup <ad-domain-fqdn>
```


```text title="Expected output"
# LDAP Search Results
dn: dc=domain,dc=com
dn: cn=Users,dc=domain,dc=com
dn: cn=Computers,dc=domain,dc=com
dn: cn=Domain Controllers,dc=domain,dc=com
dn: cn=builtin,dc=domain,dc=com
dn: cn=Managed Service Accounts,dc=domain,dc=com
dn: cn=Program Files,dc=domain,dc=com
dn: cn=System,dc=domain,dc=com
dn: cn=Lost and Found,dc=domain,dc=com
...

# DNS Resolution Results
Server:		192.168.1.10
Address:	192.168.1.10#53

Name:	corp.example.com
Address: 192.168.1.50
Address: 192.168.1.51
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ldap_bind: Can't contact LDAP server (-1)` | Verify the DC IP address is correct and port 389 is open in firewall rules between VCSA and domain controller. |
    | `ldapsearch: No such file or directory` | Install the ldap-utils package on VCSA using `yum install openldap-clients`. |
    | `Server can't find <ad-domain-fqdn>: NXDOMAIN` | Confirm the VCSA has the correct DNS server configured in `/etc/resolv.conf` pointing to a working AD-integrated DNS server. |
**Step 2 — Check for AD password expiry on the service account** used by vCenter for LDAP binding. vCenter uses a bind account to query AD — if its password expires, all AD authentication fails.

**Step 3 — Verify time sync** — Kerberos authentication fails if the vCenter appliance is more than 5 minutes out of sync with the domain controllers:

```bash
timedatectl status
ntpq -p
```


```text title="Expected output"
Local time: Thu 2024-01-18 14:32:47 UTC
           Universal time: Thu 2024-01-18 14:32:47 UTC
                 RTC time: Thu 2024-01-18 14:32:47
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 ntp.ubuntu.com  .POOL.          16 p    -   64    0    0.000    0.000   0.000
*time.google.com 216.239.35.0     2 u   52   64  377   18.432   -2.104   3.217
+ntp.nist.gov    132.163.96.1     1 u   58   64  377   42.108    1.847   2.891
-tick.ucla.edu   128.97.55.79     2 u   61   64  377   89.234    8.932   4.156
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `System clock synchronized: no` | Run `timedatectl set-ntp true` to enable NTP synchronization. |
    | `ntpq: read: Connection refused` | Ensure ntpd or systemd-timesyncd is running with `systemctl start ntp` or `systemctl start systemd-timesyncd`. |
    | `No association ID's returned` | Wait 30-60 seconds for NTP to establish peer connections, then rerun `ntpq -p`. |
**Step 4 — Check AD group membership** for the user — vCenter grants access by group, not just individual accounts. Confirm the user is still in the correct AD group.

---

## Local Admin Works, AD Users Cannot Log In

This isolates the fault to the identity source. In vCenter, go to Administration → Single Sign-On → Configuration → Identity Sources.

Common causes:

| Cause | Check | Fix |
|---|---|---|
| LDAP bind account expired | Test connection error mentions "invalid credentials" | Reset the service account password, update in identity source |
| DC unreachable | Test connection timeout | Check DC IP / FQDN, firewall, port 389/636 |
| Certificate issue (LDAPS) | Test connection SSL error | Renew or re-import the DC SSL certificate into vCenter trust store |
| Identity source deleted or misconfigured | Source missing or showing error | Re-add the identity source |

To re-add an identity source:
1. vCenter → Administration → Single Sign-On → Configuration → Identity Sources
2. Click **+** → Active Directory over LDAP → fill in domain details and bind account

---

## Permission Denied

**Step 1 — Check the effective permissions** for the user in vCenter:

vCenter → Administration → Access Control → Global Permissions, or navigate to the specific object (cluster/host/VM), right-click → Edit Permissions.

**Step 2 — Verify group membership** — vCenter typically assigns roles to AD groups. If the user was moved between groups, they may have lost access.

**Step 3 — Check for a deny-level permission** — a lower-level object can override a parent permission if "Propagate to children" is configured incorrectly.

```powershell
# PowerCLI — list all permissions on a specific VM
Get-VM "VMName" | Get-VIPermission | Select Principal, Role, Propagate

# List all permissions for a specific user across all objects
Get-VIPermission | Where-Object {$_.Principal -like "*username*"} | Select Entity, Principal, Role
```

---

## Session Timeout / Constant Re-Login Prompt

**Symptom:** vCenter UI prompts for login every few minutes despite active use.

**Step 1 — Check SSO token lifetime settings:**

vCenter → Administration → Single Sign-On → Configuration → Token Policy. Default max token lifetime is 300 seconds; max reuse count is 10. These are usually sufficient — do not reduce them.

**Step 2 — Check browser/network proxy** — some proxies strip session cookies or close idle TCP connections. Try a different browser or direct connection.

**Step 3 — Verify clock sync** — SSO tokens include a timestamp; clock skew invalidates tokens:

```bash
# On VCSA
timedatectl status
chronyc tracking
```


```text title="Expected output"
Local time: Wed 2024-01-17 14:32:45 UTC
           Universal time: Wed 2024-01-17 14:32:45 UTC
                 RTC time: Wed 2024-01-17 14:32:45
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
           RTC in local TZ: no

Reference ID    : 91.189.89.198 (ntp.ubuntu.com)
Stratum         : 2
Ref time (UTC)  : Wed Jan 17 14:32:40 2024
System time offset : 0.000234567 seconds
Last update     : 8.2 seconds ago
RMS offset      : 0.001234 seconds
Frequency       : -12.456 ppm
Residual freq   : +0.012 ppm
Skew            : 0.089 ppm
Root delay      : 0.045678 seconds
Root dispersion : 0.062345 seconds
Update interval : 1024.0 seconds
Leap status     : Normal
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `chronyc: Could not get tracking data` | Verify chrony service is running with `systemctl status chrony` and check network connectivity to NTP servers. |
    | `System clock synchronized: no` | Wait 2–3 minutes for NTP synchronization to complete, or manually sync with `ntpdate <ntp-server>` if available. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Datastore Issues](datastore-inaccessible.md)
- [Host Disconnected / Not Responding](host-disconnected.md)
- [Virtualization Troubleshooting](index.md)
