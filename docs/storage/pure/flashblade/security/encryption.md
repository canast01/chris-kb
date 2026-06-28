---
tags:
  - pure
  - security
---
# FlashBlade — Encryption
![FlashBlade — Encryption](../../../../assets/storage-pure-flashblade-security-encryption.svg)

![FlashBlade — Encryption — Diagram](../../../../assets/storage-pure-flashblade-security-encryption-diagram.svg)

## Before you begin

- FlashBlade Purity//FB 3.x or later
- Array admin or security-admin role
- SMB shares already configured (for SMB encryption steps)
- Syslog/SIEM target host and port ready (for audit logging steps)
- Maintenance window if enforcing encryption on live shares (clients reconnect on change)

## SMB share encryption

Enforce SMB encryption on a share:

```bash
purefb smb-share update --smb-encryption-mode required <sharename>
```
## Audit log forwarding (syslog)

Forward audit events over UDP or TLS to a SIEM:

```bash
purearray syslog add --uri udp://siem:514
purearray syslog add --uri tls://siem:6514
purearray syslog list
```

## Verify

- Confirm the share rejects unencrypted SMB connections from a test client
- Check `purearray syslog list` shows your targets with no error status
- Validate SIEM is receiving FlashBlade events

---

## See also

- [FlashBlade — Hardening](hardening/)
- [FlashBlade — Authentication](authentication/)
- [FlashBlade — Access Control](access-control/)
