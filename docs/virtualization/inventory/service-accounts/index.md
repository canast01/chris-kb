# VMware Service Account Inventory

| Account Name | Purpose | System | Permission Level | Owner | Password Rotation | Vault Managed | Last Reviewed |
|---|---|---|---|---|---|---|---|
| svc-vcenter | vCenter API access | Backup platform | Read-only + snapshot | infra-team | 90 days | Yes | YYYY-MM-DD |
| svc-aria-ops | Aria Operations integration | vCenter | Read-only | infra-team | 90 days | Yes | YYYY-MM-DD |
| svc-backup | Backup job account | vCenter, Datastores | Backup role | infra-team | 90 days | Yes | YYYY-MM-DD |
| svc-nsx | NSX-vCenter integration | NSX Manager | Admin | infra-team | 90 days | Yes | YYYY-MM-DD |

## Review Process

- Review the service account inventory quarterly
- Remove or disable accounts for decommissioned tools
- Confirm password rotation is current
- Confirm vault or credential management is in place for all accounts
