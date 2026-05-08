# COD — Backup & Restore

> Part of the [COD](../../) reference.

---

COD does not manage data backup directly. Key items to protect:

- **COD license files**: store downloaded license key files (`.xml`/`.dat`) in a secure, backed-up location — a secrets vault or a protected network share accessible only to storage admins. Lost license files require re-issuance from the Dell License Portal, which can cause delays during emergency activations.
- **COD inventory record**: maintain and back up the COD inventory tracking spreadsheet or CMDB records for each array including SID, activation dates, and headroom.
- **SYMCLI audit log exports**: periodically export `symaudit -sid <SID> list` output to a file and retain for compliance purposes.
