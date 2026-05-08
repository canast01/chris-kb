# PowerScale — Encryption

> TLS certificate management and data encryption for Dell PowerScale.

## Encryption Layers

| Layer | Mechanism | Notes |
|---|---|---|
| Data at Rest | Self-Encrypting Drives (SED) with AES-256 | Hardware-based; configured at factory order time. Cannot be enabled retroactively on spinning drives. |
| Data in Transit (SyncIQ) | TLS-encrypted SyncIQ replication channel | Enable with `isi sync policies modify <name> --encryption-required true` |
| Management Traffic | HTTPS (TLS 1.2+) for web UI; SSH for CLI | Disable TLS 1.0/1.1; restrict cipher suites to strong options |
| SMB Encryption | SMB3 end-to-end encryption | Enable per-share: `isi smb shares modify <share> --encrypt-data true` |

## SyncIQ Encryption

```bash
# Require encryption on a SyncIQ policy
isi sync policies modify <policy_name> --encryption-required true

# List replication peer certificates
isi sync target policies list

# Check SyncIQ service
isi services synciq status
```

## SMB Encryption

```bash
# Enable SMB signing (required for all Windows client access)
isi smb settings global modify --server-signing required

# Enable SMB3 encryption per share
isi smb shares modify <share_name> --encrypt-data true
```

## Management TLS

- Enable HTTPS-only access to the OneFS web administration GUI; disable HTTP.
- Disable TLS 1.0 and TLS 1.1; restrict cipher suites to strong options.
- Configure session timeout on the web UI (recommended: 15 minutes).
