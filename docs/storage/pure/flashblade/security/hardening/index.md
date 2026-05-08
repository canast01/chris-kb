# FlashBlade — Hardening

> Part of the [FlashBlade Security](../) reference.

---

## Hardening Checklist

- Disable unused data protocols — if the array only serves S3, disable NFS and SMB in the Purity//FB protocol configuration to reduce attack surface
- Enforce HTTPS for all management access; confirm HTTP redirect is disabled in the array management settings
- Rotate API tokens for all service accounts on a defined schedule (90 days recommended); revoke tokens for departed staff immediately
- Disable or rename default local accounts; all operational access should use named accounts or SSO/SAML integration
- Restrict management network access to a dedicated out-of-band management VLAN; do not expose the management interface on data networks
- Enable SafeMode for snapshots where supported — requires Pure Support to modify or destroy protected snapshots, protecting against ransomware
- Review and restrict S3 bucket policies to minimum required permissions; avoid wildcard (`*`) principal grants on production buckets
- Confirm NFS exports are restricted to specific client IP ranges or subnets; avoid exporting with `*` (all hosts) in production
