---
tags:
  - pure
  - security
---
# FlashBlade — Encryption
![FlashBlade — Encryption](../../../../assets/storage-pure-flashblade-security-encryption.svg)




```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  Data in Transit                                                                                      │
│  ├── NFS v4.1: Kerberos GSSAPI privacy (optional)                                                     │
│  ├── SMB 3.0: end-to-end SMB encryption (AES-128-GCM)                                                 │
│  ├── S3: HTTPS (TLS 1.2+)                                                                             │
│  ├── Management GUI/API: HTTPS (443)                                                                  │
│  └── Replication (ActiveDR): TLS between FlashBlades                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

> Part of the [FlashBlade Security](index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Data at Rest

All data written to FlashBlade drives is encrypted using XTS-AES-256. Encryption is always on and cannot be disabled. Drives are self-encrypting; when a drive is removed or replaced, data is cryptographically erased by destroying the drive encryption key.

## Data in Flight — NFS

NFS v4.1 Kerberos authentication modes supported:

- `krb5` — authentication only
- `krb5i` — authentication + integrity
- `krb5p` — authentication + integrity + privacy (full encryption)

Configure Kerberos in the NFS export policy to enforce encrypted NFS sessions. Requires an Active Directory or MIT Kerberos KDC.

## Data in Flight — SMB

SMB encryption (AES-128-CCM or AES-256-GCM) is configurable per share. Enable SMB encryption to protect data in transit between Windows clients and FlashBlade:

```

```bash
purefb smb-share update --smb-encryption-mode required <sharename>
```
```bash
purearray syslog add --uri udp://siem:514
```
```bash
purearray syslog add --uri tls://siem:6514
```
```bash
purearray syslog list
```

---

## See also

- [FlashBlade — Hardening](hardening/)
- [FlashBlade — Authentication](authentication/)
- [FlashBlade — Access Control](access-control/)
