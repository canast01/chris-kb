# Nexus Dashboard Security

```
┌───────────────────────────────────── Nexus Dashboard — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │               Network Security              │   │
│   │             Local + LDAP/TACACS              │  │              HTTPS only TCP 443             │   │
│   │             RBAC: role per team              │  │                Mgmt VLAN only               │   │
│   │             APIC read-only user              │  │                TLS inter-node               │   │
│   │               MFA integration                │  │                gRPC auth MDT                │   │
│   │             Annual access review             │  │               Audit log in ND               │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  ND cluster on management network · APIC observer account · gRPC on data network                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TACACS+ = AAA protocol for ND admin authentication; integrates with Cisco ISE                        │
│  LDAP = Directory authentication for ND UI login via AD/OpenLDAP                                      │
│  RBAC = Admin/Operator/Viewer roles; scoped to site or global                                         │
│  APIC Observer = Minimum-privilege read-only role for NDI APIC integration                            │
│  MFA = Multi-factor auth via SAML/SSO; ND supports external IdP                                       │
│  TLS inter-node = All ND cluster internal traffic encrypted                                           │
│  gRPC auth = MDT streaming uses TLS with certificate authentication                                   │
│  Audit log = ND records logins, config changes, and user actions                                      │
│  Mgmt VLAN = ND admin UI on management network; data network for fabric only                          │
│  Annual review = Yearly audit of ND accounts and APIC service account                                 │
│  Custom cert = Replace ND self-signed with CA cert in ND admin > Certificate                          │
│  SSH restriction = Limit SSH to ND master nodes to jump-host IPs only                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Nexus Dashboard RBAC supports Domain Admin, Tenant Admin, and Read-only roles, scoped to specific fabrics or globally. LDAP and TACACS+ integration are supported for centralised authentication and authorisation. All management access to the ND cluster is HTTPS-only; the management IP should be reachable only from the operations management subnet. TLS certificates for the ND cluster should be replaced with organisation-issued certificates (not self-signed) for production environments. The audit log captures all admin actions, policy changes, and login events and should be exported to the SIEM. Fabric isolation is enforced via tenant VRFs in ACI to prevent cross-tenant traffic.

| Role | Capabilities |
|---|---|
| Domain Admin | Full ND platform and fabric administration |
| Tenant Admin | Manage assigned tenant policies and resources |
| Read-only | View fabric health, faults, and dashboards only |

- Authentication: LDAP or TACACS+ (no shared local accounts in production)
- Access: HTTPS-only, restricted to ops management subnet
- Certificates: organisation-issued TLS certificates
- Audit log: exported to SIEM, retained 12 months minimum
- Fabric isolation: tenant VRFs in ACI
