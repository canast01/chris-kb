---
tags:
  - nsx
  - nsx-4
  - security
  - vmware
---
# NSX — Access Control
![NSX — Access Control](../../../../assets/virtualization-vmware-nsx-security-access-control.svg)

```bash
# List all role bindings (users and groups with assigned roles)
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for r in d.get('results', []):
    name  = r.get('name', r.get('id', '?'))
    rtype = r.get('type', '?')
    roles = ', '.join(x.get('role','?') for x in r.get('roles', []))
    src   = r.get('identity_source_type', 'LOCAL')
    print(f'  {name:<50} type={rtype:<15} roles={roles:<25} source={src}')
"
```

```bash
curl -sk -u 'admin:password' \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "project-tenant-a",
    "short_id": "tenant-a",
    "tier_0_gateway_paths": ["/infra/tier-0s/t0-prod"]
  }' \
  "https://<nsx-manager>/policy/api/v1/orgs/default/projects/project-tenant-a"
```
```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CN=TenantA-Admins,OU=Groups,DC=corp,DC=local",
    "type": "remote_group",
    "identity_source_type": "LDAP",
    "roles": [{
      "role": "project_admin",
      "role_type": "ORG_ROLE",
      "org_id": "default",
      "project_ids": ["project-tenant-a"]
    }]
  }' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings"
```
```bash
# SSH to NSX Manager node
nsxcli

# Allow API access only from admin jump hosts and monitoring
set firewall rule 1 source-ip 10.0.1.0/24 dest-port 443 action allow
set firewall rule 2 source-ip 10.0.2.10/32 dest-port 443 action allow
set firewall rule 3 dest-port 443 action deny

# Allow SSH from jump hosts only
set firewall rule 10 source-ip 10.0.1.0/24 dest-port 22 action allow
set firewall rule 11 dest-port 22 action deny

get firewall rules
```
```bash
# List existing principal identities
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/principal-identities"

# Verify certificate binding for an identity
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/principal-identities/<pi-id>"
```
```powershell
# PowerCLI — cross-check NSX role bindings against AD group membership
# (runs from a machine with AD RSAT tools and NSX API access)
$groups = @("NSX-Admins", "NSX-Network", "NSX-Security", "NSX-Ops")
foreach ($g in $groups) {
    $members = Get-ADGroupMember -Identity $g | Select-Object SamAccountName, distinguishedName
    Write-Host "=== $g ==="
    $members | ForEach-Object { Write-Host "  $($_.SamAccountName)" }
}
```

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## See also

- [NSX — Authentication](../authentication/)
- [NSX — Hardening](../hardening/)
