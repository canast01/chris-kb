# Management Access Check

Run this check weekly to confirm all management endpoints are reachable and access controls are healthy.

```text
Management Access Check Flow
═══════════════════════════════════════════════════════════

  DNS resolves? ──► HTTPS reachable? ──► Login OK?
        │                │                   │
       FAIL             FAIL                FAIL
        │                │                   │
  Check DNS        Check firewall       Check SSO/AD
  or FQDN          or service           or creds

  Endpoints to verify:
  ┌─────────────────────────────────────────────────────┐
  │  vCenter         https://vcenter.example.local         │
  │  ├─ SSO login    administrator@vsphere.local        │
  │  └─ VAMI         https://vcenter.example.local:5480    │
  │                                                     │
  │  NSX Manager     https://nsx.example.local             │
  │  ├─ Cluster      get cluster status → STABLE        │
  │  └─ Services     get services → running             │
  │                                                     │
  │  Aria Operations https://aria-ops.example.local        │
  │  └─ Collection   State: OK (< 5 min lag)            │
  │                                                     │
  │  VxRail Manager  https://vxrail.example.local          │
  │  └─ Node health  All nodes: Healthy                 │
  │                                                     │
  │  iDRAC nodes     https://idrac-esx-<site>-<##>     │
  │  └─ Hardware     No disk / NIC / PSU alerts         │
  └─────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── Management Access Check ───────────────────────────────────────┐
│                                                                                                       │
│    Run weekly; confirm DNS, HTTPS, and login for every management endpoint                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │        Check Sequence (per endpoint)         │  │             Endpoints to Verify             │   │
│   │        ──────────────────────────────        │  │        ─────────────────────────────        │   │
│   │            1. DNS resolves FQDN?             │  │             vCenter FQDN (HTTPS)            │   │
│   │            FAIL → check DNS / HOSTS          │  │               └─ SSO login test             │   │
│   │         2. HTTPS port 443 reachable?         │  │               └─ VAMI port 5480             │   │
│   │           FAIL → check firewall rule         │  │               NSX Manager FQDN              │   │
│   │              3. Login succeeds?              │  │             Backup console FQDN             │   │
│   │           FAIL → check SSO / AD bind         │  │             Monitoring dashboard            │   │
│   │        4. Session timeout acceptable?        │  │              Storage array FQDN             │   │
│   │           FAIL → check session policy        │  │              vSAN Witness host              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FQDN    = Fully Qualified Domain Name; must resolve in DNS; e.g. vcenter.corp.local                │
│    SSO     = vCenter Single Sign-On; authentication service; default domain: vsphere.local            │
│    VAMI    = vCenter Appliance Management Interface; port 5480; cert and patch management             │
│    AD bind = LDAP/LDAPS connection from SSO to Active Directory; check if login fails                 │
│    Timeout = Session idle timeout; check if users report being logged out too quickly                 │
│    NSX Mgr = NSX Manager UI; HTTPS on port 443; login via admin or LDAP-integrated account            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## vCenter Access

```powershell
# Verify vCenter login (PowerCLI)
Connect-VIServer -Server vcenter.example.local -Credential $cred
if ($?) { Write-Host "vCenter: OK" } else { Write-Host "vCenter: FAIL" }

# Check vCenter certificate validity
$cert = [System.Net.ServicePointManager]::ServerCertificateValidationCallback
$expiry = (Invoke-WebRequest -Uri "https://vcenter.example.local" -UseBasicParsing).Headers
```

Checks to perform in vCenter UI:
- [ ] vCenter SSO Health: Administration → Single Sign On → Diagnostics → Diagnostic Site Connectivity
- [ ] Identity sources: Administration → Single Sign On → Configuration → Identity Sources — all should show Connected
- [ ] System health: Administration → Deployments → System Configuration — all services green

## NSX Manager Access

```bash
# Verify NSX Manager cluster health (SSH to NSX Manager)
get cluster status   # Should show: STABLE
get services         # All critical services should show: running
```

## SDDC Manager Access (VCF)

```bash
# SDDC Manager API health check
curl -k -u admin@local:password https://sddc-manager.example.local/v1/health-summary | python3 -m json.tool
```

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

Alert on > 5 failed logins for any account in a 15-minute window.
