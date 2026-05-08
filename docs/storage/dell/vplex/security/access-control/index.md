# Dell VPLEX — Access Control

> Roles, permissions, and least privilege access for Dell VPLEX.

## Management Roles

VPLEX access control is managed through Unisphere for VPLEX and VMS local accounts:

| Role | Access Level | Notes |
|---|---|---|
| Administrator | Full read/write access to all VPLEX configuration | Assign only to storage administrators |
| Monitor | Read-only access to cluster health, volumes, and configuration | Suitable for operations teams |
| Service | SSH-based `vplexcli` access for CLI management | Default service account for automation |

## Host Access Control

Host access to VPLEX virtual volumes is controlled via storage views:

- Each storage view maps specific virtual volumes to specific host initiator ports (WWNs)
- Hosts can only see volumes included in a storage view to which their HBA WWN is registered
- Follow least-privilege: only map the volumes a host needs; do not create catch-all storage views
- Review storage view membership after any host decommission to remove orphaned initiators

## Zoning

Fibre Channel zoning enforces access at the SAN level before VPLEX storage views:

- Zone each host HBA to only the VPLEX front-end ports required for its storage views
- Do not zone hosts directly to backend array ports; all host access should pass through VPLEX
- Implement single-initiator, multiple-target zoning for clarity and security
