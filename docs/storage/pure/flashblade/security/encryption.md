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

```text title="Expected output"
SMB share '<sharename>' updated
  Encryption Mode: required
  Updated at: 2024-01-15T14:32:47Z
```

!!! warning "Common errors"
    **`Error: SMB share '<sharename>' not found`** — Verify the share name exists with `purefb smb-share list` and use the correct name.
    **`Error: Command failed: Invalid encryption mode 'required'. Valid modes are: disabled, preferred, required`** — Ensure the encryption mode parameter matches exactly (check for typos or unsupported values).
    **`Error: You do not have permission to perform this operation`** — Confirm your FlashBlade user account has admin or security policy modification privileges.
## Audit log forwarding (syslog)

Forward audit events over UDP or TLS to a SIEM:

```bash
purearray syslog add --uri udp://siem:514
purearray syslog add --uri tls://siem:6514
purearray syslog list
```


```text title="Expected output"
Syslog server added: udp://siem:514
Syslog server added: tls://siem:6514
Name                          Facility  Severity  URI
siem-udp                      local0    info      udp://siem:514
siem-tls                      local1    info      tls://siem:6514
```

!!! warning "Common errors"
    **`Error: Connection refused to siem:514`** — Verify the syslog server hostname/IP is reachable and the syslog service is listening on the specified port.
    **`Error: TLS certificate verification failed for tls://siem:6514`** — Ensure the FlashBlade has the correct CA certificate installed and the syslog server's TLS certificate is valid and trusted.
## Verify

- Confirm the share rejects unencrypted SMB connections from a test client
- Check `purearray syslog list` shows your targets with no error status
- Validate SIEM is receiving FlashBlade events

---

## See also

- [FlashBlade — Hardening](../hardening/)
- [FlashBlade — Authentication](../authentication/)
- [FlashBlade — Access Control](../access-control/)
