# NSX — Access Control

## RBAC Model

NSX-T uses role-based access control (RBAC) with a flat role hierarchy. Roles are assigned to users or groups at the system level — there is no per-object permission granularity in base NSX (Project-scoped permissions are available with NSX Multitenancy in NSX 4.1+).

### Built-in Roles

| Role | API Name | Permissions |
|---|---|---|
| Enterprise Admin | `enterprise_admin` | Full read/write; user management |
| Network Engineer | `network_engineer` | Segments, gateways, routing, load balancer |
| LB Admin | `lb_admin` | Load balancer only |
| Security Admin | `security_admin` | DFW policies, groups, tags, IPFIX |
| VPN Admin | `vpn_admin` | IPsec and L2 VPN only |
| GI Partner Admin | `gi_partner_admin` | Guest Introspection only |
| Operator | `operator` | Read-only + restart services, clear statistics |
| Auditor | `auditor` | Read-only across all objects |
| NETX Partner Admin | `netx_partner_admin` | NetX (3rd party service insertion) |
| Cloud Service Admin | `cloud_service_admin` | VMware Cloud Director integration |

### Recommended Role Assignments

| Team | Role | Account Type |
|---|---|---|
| NSX Administrators | Enterprise Admin | Named AD group (`NSX-Admins`) |
| Network Engineering | Network Engineer | Named AD group (`NSX-Network`) |
| Security Engineering | Security Admin | Named AD group (`NSX-Security`) |
| NOC / L1 Operations | Operator | Named AD group (`NSX-Ops`) |
| Compliance / Audit | Auditor | Named AD group (`NSX-Audit`) |
| Automation / CI-CD | Network Engineer or Security Admin | Service principal identity (cert-based) |

Do not assign Enterprise Admin to automation accounts. Use the most restrictive role that allows the required operations.

---

## Viewing Current Role Assignments

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

---

## Managing Role Assignments

### Add a Role Binding (LDAP Group)

```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "name": "CN=NSX-Security,OU=Groups,DC=corp,DC=local",
    "type": "remote_group",
    "identity_source_type": "LDAP",
    "identity_source_id": "<ldap-source-id>",
    "roles": [{"role": "security_admin"}]
  }' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings"
```

### Remove a Role Binding

```bash
# First, find the binding ID
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/role-bindings" | python3 -m json.tool

# Delete by binding ID
curl -sk -u 'admin:password' \
  -X DELETE \
  "https://<nsx-manager>/api/v1/aaa/role-bindings/<binding-id>"
```

---

## NSX Multitenancy Projects (NSX 4.1+)

NSX 4.1 introduced Projects, which provide per-tenant scoped access. A Project administrator can manage networking within their project scope without visibility to other projects or the infrastructure tier.

### Create a Project

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

### Assign Project Admin Role

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

Project admins can create segments, groups, and DFW policies within their project. They cannot see or modify other projects or infrastructure objects (T0 gateways, transport nodes, Edge clusters).

---

## Firewall-Enforced Access Control

Restrict which hosts can reach the NSX Manager API (port 443) and SSH (port 22) using the NSX Manager built-in firewall.

### Configure API Access Restrictions

**System → Appliance → Management Network Firewall**

Or via CLI:

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

### Network-Layer Enforcement

Beyond the appliance firewall, enforce access control at the network layer:

| Traffic | Source Restriction |
|---|---|
| HTTPS (443) to NSX Manager VIP | Admin jump host subnet only |
| SSH (22) to NSX Manager nodes | Admin jump host subnet only |
| UDP 6081 (Geneve) | TEP VLANs only — not accessible from VM subnets |
| BGP (179) on Edge uplinks | Physical router IPs only |

---

## Principal Identities for Automation

Automation systems should not use the shared `admin` account. Use certificate-based principal identities:

```bash
# List existing principal identities
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/principal-identities"

# Verify certificate binding for an identity
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/aaa/principal-identities/<pi-id>"
```

Certificate rotation for a principal identity:

1. Generate a new key/cert pair (same CN as original)
2. Import the new certificate: `POST /api/v1/trust-management/certificates?action=import`
3. Update the principal identity binding with the new cert ID
4. Retire the old certificate

---

## Access Control Audit Checklist

Perform this review quarterly or after any personnel change:

- [ ] List all Enterprise Admin role bindings — verify only named individuals/groups are assigned
- [ ] Verify no shared service accounts have admin roles
- [ ] Confirm LDAP source is reachable and binding is working (test login with an AD account)
- [ ] Review principal identities — verify automation certs are not expired
- [ ] Check for any local users beyond admin, audit — delete or disable unused local accounts
- [ ] Confirm audit log is being forwarded to SIEM
- [ ] Review role assignments against current team membership — remove leavers

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

Remove former employees from AD groups promptly — NSX inherits permissions from AD group membership in real-time.
