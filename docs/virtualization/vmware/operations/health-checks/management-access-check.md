---
tags:
  - operations
---
# Management Access Check

<div class="kb-summary">
Run this check weekly to confirm all management endpoints are reachable and access controls are healthy.

*Applies to: vSphere 7.x / 8.x*
</div>

Checks to perform in vCenter UI:
- [ ] vCenter SSO Health: Administration → Single Sign On → Diagnostics → Diagnostic Site Connectivity
- [ ] Identity sources: Administration → Single Sign On → Configuration → Identity Sources — all should show Connected
- [ ] System health: Administration → Deployments → System Configuration — all services green

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
nsx_manager_access: "NSX Manager Access" {shape: rectangle}
sddc_manager_access_vcf: "SDDC Manager Access (VCF)" {shape: rectangle}
aria_operations_access: "Aria Operations Access" {shape: rectangle}
adldap_identity_source_health: "AD/LDAP Identity Source Health" {shape: rectangle}
access_control_review: "Access Control Review" {shape: rectangle}
failed_login_monitoring: "Failed Login Monitoring" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> nsx_manager_access
nsx_manager_access -> sddc_manager_access_vcf
sddc_manager_access_vcf -> aria_operations_access
aria_operations_access -> adldap_identity_source_health
adldap_identity_source_health -> access_control_review
access_control_review -> failed_login_monitoring
failed_login_monitoring -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## NSX Manager Access

```bash
# Verify NSX Manager cluster health (SSH to NSX Manager)
get cluster status   # Should show: STABLE
get services         # All critical services should show: running
```


```text title="Expected output"
cluster status: STABLE
cluster id: 36b8c4a2-7f1e-4d9a-b2e1-5c9d8f3a2b1e
cluster role: PRIMARY
cluster size: 3
node 1: nsx-mgr-01.lab.local (192.168.1.10) - ACTIVE
node 2: nsx-mgr-02.lab.local (192.168.1.11) - ACTIVE
node 3: nsx-mgr-03.lab.local (192.168.1.12) - ACTIVE

services:
  management-plane: running
  control-plane: running
  data-plane: running
  api-service: running
  persistence-service: running
  messaging-service: running
```

!!! warning "Common errors"
    **`cluster status: UNSTABLE`** — Check node connectivity with `get cluster nodes` and verify network connectivity between cluster members.
    **`service <service-name> status: stopped`** — Restart the service with `restart service <service-name>` and check logs with `get service <service-name> logs`.
    **`Connection refused`** — Verify SSH access to NSX Manager and confirm the management IP is reachable with `ping <nsx-mgr-ip>`.
## SDDC Manager Access (VCF)

```bash
# SDDC Manager API health check
curl -k -u admin@local:password https://sddc-manager.example.local/v1/health-summary | python3 -m json.tool
```


```text title="Expected output"
{
  "status": "HEALTHY",
  "timestamp": "2024-01-15T09:42:33.847Z",
  "components": [
    {
      "name": "vCenter",
      "status": "HEALTHY",
      "lastChecked": "2024-01-15T09:41:15.000Z"
    },
    {
      "name": "NSX Manager",
      "status": "HEALTHY",
      "lastChecked": "2024-01-15T09:40:52.000Z"
    },
    {
      "name": "vSAN",
      "status": "HEALTHY",
      "lastChecked": "2024-01-15T09:39:28.000Z"
    },
    {
      "name": "Cluster Compute",
      "status": "HEALTHY",
      "lastChecked": "2024-01-15T09:38:45.000Z"
    }
  ],
  "overallHealth": "GREEN"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to skip certificate verification (already present in example; if error persists, verify SDDC Manager hostname matches certificate CN).
    **`curl: (7) Failed to connect to sddc-manager.example.local port 443: Name or service not known`** — Verify DNS resolution with `nslookup sddc-manager.example.local` and confirm the SDDC Manager FQDN is correct.
    **`401 Unauthorized`** — Confirm credentials are correct and the admin@local user has API access permissions in SDDC Manager.
## Aria Operations Access

Confirm Aria Ops is receiving telemetry:
1. Log in to `https://aria-ops.example.local`
2. Environment → Object Browser → confirm vCenter adapter shows `Collection State: OK`
3. Check last collection time — should be within the last 5 minutes

## AD/LDAP Identity Source Health

```bash
# Test LDAP connectivity (run from a Linux admin host)
ldapsearch -H ldaps://dc1.example.local:636 -D "cn=svc_vcenter,ou=service_accounts,dc=corp,dc=local" \
    -w '<password>' -b "dc=corp,dc=local" "(sAMAccountName=admin)" sAMAccountName
# Should return at least one result
```


```text title="Expected output"
# extended LDIF
#
# LDAPv3
# base <dc=corp,dc=local> with scope subtree
# filter: (sAMAccountName=admin)
# requesting: sAMAccountName
#

# admin, Users, corp.local
dn: CN=admin,CN=Users,DC=corp,DC=local
sAMAccountName: admin

# search result
search: 2
result: 0 Success
matchedDN: dc=corp,dc=local
```

!!! warning "Common errors"
    **`ldap_bind: Invalid credentials (49)`** — Verify the service account password is correct and the account is not locked; check Active Directory for failed login attempts.
    **`Can't contact LDAP server (-1)`** — Confirm the DC hostname resolves (use `nslookup dc1.example.local`), port 636 is open (use `nc -zv dc1.example.local 636`), and the firewall allows LDAPS from your admin host.
## Access Control Review

Run monthly (in addition to weekly connectivity checks):

- [ ] Review stale user accounts: Administration → Users and Groups — remove leavers
- [ ] Review service account usage: confirm all service accounts still needed
- [ ] Verify MFA is enforced for admin console access (via SSO policy or Workspace ONE Access)
- [ ] Review vCenter role assignments: Administration → Access Control → Roles
- [ ] Confirm no direct permission grants to individual users (should be via group memberships)
- [ ] Check break-glass accounts: password still in vault; access log reviewed

## Failed Login Monitoring

```bash
# Check vCenter SSO audit log for failed logins
# /storage/log/vmware/sso/vmware-sts-idmd.log on vCenter appliance
grep "AuthenticationException\|failed.*login\|InvalidCredentials" /var/log/vmware/sso/vmware-sts-idmd.log | tail -20
```


```text title="Expected output"
2024-01-15T09:23:47.123Z ERROR [com.vmware.identity.idm.server.provider.ActiveDirectoryProvider] AuthenticationException: Failed to authenticate user admin@vsphere.local
2024-01-15T09:24:12.456Z WARN [com.vmware.identity.idm.server.provider.LdapProvider] InvalidCredentials: Bind failed for user svc-vcenter@corp.local
2024-01-15T09:25:33.789Z ERROR [com.vmware.identity.idm.server.provider.ActiveDirectoryProvider] failed login attempt for user jsmith@vsphere.local from 192.168.1.45
2024-01-15T09:26:01.234Z WARN [com.vmware.identity.idm.server.provider.ActiveDirectoryProvider] AuthenticationException: User account locked after 5 failed attempts
2024-01-15T09:27:44.567Z ERROR [com.vmware.identity.idm.server.provider.LdapProvider] InvalidCredentials: LDAP server unreachable at ldap.corp.local:389
2024-01-15T09:28:15.890Z WARN [com.vmware.identity.idm.server.provider.ActiveDirectoryProvider] failed login attempt for user automation@vsphere.local from 10.0.5.22
2024-01-15T09:29:22.012Z ERROR [com.vmware.identity.idm.server.provider.ActiveDirectoryProvider] AuthenticationException: Password expired for user dchen@vsphere.local
```

!!! warning "Common errors"
    **`grep: /var/log/vmware/sso/vmware-sts-idmd.log: No such file or directory`** — Verify the correct log path on your vCenter version (may be `/var/log/vmware/sso/` or `/storage/log/vmware/sso/`) and check that the vCenter appliance is running.
    **`Permission denied`** — Run the command with `sudo` or as root, since SSO logs typically require elevated privileges to read.
Alert on > 5 failed logins for any account in a 15-minute window.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Alert Health Check](alert-review.md)
- [Capacity Review](capacity-review.md)
- [Daily Health Check](daily-health-check.md)
- [Virtualization Health Checks](index.md)
