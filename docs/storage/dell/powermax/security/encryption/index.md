# PowerMax — Encryption

## Encryption Layers

| Layer | Mechanism | Notes |
|---|---|---|
| Data at Rest (D@RE) | AES-256; hardware-based encryption on NVMe drives | Enabled by factory default on PowerMax 2000/8000; key management via embedded EKMS or external KMIP server |
| Data in Flight (SRDF) | SRDF Encryption (AES-256 over FC or IP) | Must be explicitly enabled on RDF group; requires both arrays to be at a compatible code level |
| Management Traffic | TLS 1.2/1.3 for Unisphere REST API and HTTPS | Enforce strong ciphers; disable legacy TLS via Unisphere security settings |

## KMIP Integration

For KMIP integration (external key manager such as Thales CipherTrust or Vormetric):
- Configure under Unisphere → Settings → Security → Encryption Key Management.
- Test key retrieval before placing array into production.
