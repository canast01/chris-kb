# RecoverPoint Security

RecoverPoint cluster access is role-based, with admin and monitor roles assigned through the management console; admin access should be restricted to named accounts and not shared. API token management is required for any automation integrating with the RecoverPoint REST API; tokens should be rotated on a defined schedule and scoped to minimum required permissions. SSH access to RPA appliances is hardened by disabling root login, restricting access to management jump hosts, and ensuring SSH host keys are documented in the configuration record.

- **RBAC:** Admin and monitor roles; no shared credentials; individual accounts mapped to roles
- **API tokens:** Generated per integration; stored in secrets vault (e.g., CyberArk or HashiCorp Vault); rotated quarterly
- **Journal encryption:** At-rest encryption for journal volumes configured at the storage array level
- **Network segmentation:** Production-to-replica replication traffic isolated on dedicated VLAN or WAN circuit; management traffic separate
- **SSH hardening:** Root login disabled; SSH access restricted to bastion/jump host source IPs; idle session timeout configured
- **Certificate management:** Management console certificate replaced with CA-signed certificate; renewal tracked in certificate inventory
