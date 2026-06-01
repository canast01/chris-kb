# Login and Access Issues


<div class="kb-summary">
> Part of the [Troubleshooting](../index.md) hub.
</div>

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

**Step 3 — Check for a locked account:**

```bash
# Check if the SSO admin account is locked
/usr/lib/vmware-vmafd/bin/dir-cli account find-by-name --account administrator --login administrator@vsphere.local
```

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

**Step 2 — Check for AD password expiry on the service account** used by vCenter for LDAP binding. vCenter uses a bind account to query AD — if its password expires, all AD authentication fails.

**Step 3 — Verify time sync** — Kerberos authentication fails if the vCenter appliance is more than 5 minutes out of sync with the domain controllers:

```bash
timedatectl status
ntpq -p
```

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
