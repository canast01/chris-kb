# Nexus Dashboard Security

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
