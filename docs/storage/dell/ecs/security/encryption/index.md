# Dell ECS — Encryption

## Encryption Layers

| Layer | Method | Notes |
|---|---|---|
| Data in transit | TLS 1.2+ | Enforced on S3 (443), Management API (4443); configure minimum TLS version in ECS Portal → Settings → Security |
| Data at rest | Software AES-256 (ECS encryption at rest) | Enable per-namespace in ECS Portal → Namespace → Edit → Encryption; key management via internal or external KMIP KMS |
| Key management | Internal ECS KMS or external KMIP server | For compliance, use an external KMIP-compatible KMS (e.g., Dell PowerProtect Data Manager, HashiCorp Vault) |

Enable encryption at rest on namespaces that hold regulated data (PCI, HIPAA, GDPR). Note that enabling encryption on an existing namespace does not retroactively encrypt already-stored objects.

## TLS Configuration

- Minimum TLS version: TLS 1.2; disable TLS 1.0 and 1.1 in ECS Portal → Settings → Security
- Replace self-signed certificates on the Management API (4443) and S3 endpoint (443) with certificates signed by the corporate CA
- Disable HTTP (port 9021) in production; require HTTPS for all S3 access
- Monitor certificate expiry: renew TLS certificates at least 30 days before expiry (ECS Portal → Settings → Certificates)

## Key Management

**Internal ECS KMS:**
- Default key management built into the ECS cluster
- Keys are stored within the ECS cluster itself
- Suitable for environments without an external KMS requirement

**External KMIP KMS:**
- Required for compliance environments (PCI DSS, HIPAA)
- Supported KMS platforms: Dell PowerProtect Data Manager, HashiCorp Vault, Thales CipherTrust, and other KMIP-compatible servers
- Configure in ECS Portal → Settings → Key Management
- Verify connectivity to the KMIP server before enabling encryption on production namespaces
