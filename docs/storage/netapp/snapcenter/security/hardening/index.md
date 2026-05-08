# SnapCenter — Hardening

> Part of the [SnapCenter Security](../) reference.

---

## Hardening Checklist

- [ ] Default `admin` password changed from installation default; stored in a secrets vault
- [ ] AD groups used for SnapCenter access; no individual AD user accounts unless required
- [ ] MFA enabled if SnapCenter 6.0+ is deployed and an IdP is available
- [ ] Default self-signed TLS certificate replaced with CA-signed certificate on port 8146
- [ ] TLS 1.2 minimum enforced in IIS
- [ ] ONTAP service account uses least-privilege custom role (not `vsadmin` or `admin`)
- [ ] Plugin host credentials stored in SnapCenter Credential Store; no plaintext passwords in scripts
- [ ] Audit log review included in weekly operational checks
- [ ] SnapCenter Server VM is hardened per Windows Server CIS benchmark; not used for other workloads
- [ ] Network access to port 8146 restricted to admin workstations and automation hosts (firewall or NSG rule)
