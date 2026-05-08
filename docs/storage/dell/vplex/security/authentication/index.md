# Dell VPLEX — Authentication

> SSO, LDAP, local accounts, and identity sources for Dell VPLEX.

## Local Accounts

VPLEX management access is provided through local accounts on the VPLEX Management Server (VMS):

- **service**: The primary SSH user for `vplexcli` access; used for all CLI-based management operations
- **admin**: Administrative user for VMS OS-level access; restrict to break-glass use only
- Change default passwords immediately after deployment
- Create named service accounts for automation; do not use shared credentials

## LDAP / Active Directory

VPLEX supports LDAP/AD integration for Unisphere for VPLEX web UI authentication. Configure under Unisphere → Settings → Authentication.

- CLI access (`vplexcli` via SSH) always uses local VMS accounts
- LDAP integration applies to the Unisphere web interface only
- Map LDAP groups to VPLEX management roles

## Audit Logging

- VPLEX management actions are logged in VMS logs: `/var/log/VPlex/vplexmanagement.log`
- CLI command history is logged in: `/var/log/VPlex/cli/vplexcli.log`
- Forward VMS syslog to a centralised SIEM for management action auditing
