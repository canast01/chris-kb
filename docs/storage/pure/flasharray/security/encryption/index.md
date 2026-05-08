# FlashArray — Encryption

> TLS certificate management and data encryption.

## Encryption at Rest

- FlashArray //X and //C series use NVMe Self-Encrypting Drives (SEDs) with hardware AES-256 encryption
- Encryption is always-on and requires no configuration; drive data is unreadable without the Purity-managed encryption keys
- Verify encryption status: `purearray list --encryption`
- Key management: Purity manages drive encryption keys internally; external KMIP key manager integration is supported on Purity//FA 6.x for organisations requiring external key custody (e.g., for FIPS or compliance requirements)

## Encryption in Transit

- All management traffic (HTTPS, REST API) uses TLS 1.2 or 1.3; configure a trusted certificate (`purearray setattr --tls-certificate`)
- Replication traffic between FlashArray arrays uses TLS encryption by default
- iSCSI data traffic is not encrypted by Purity — use IPsec at the network layer if encryption of iSCSI data-in-transit is required
- FC and NVMe/FC data traffic encryption is handled at the fabric layer (FC-SP-2 / link encryption on compatible HBAs and switches)

## TLS Certificate Management

```bash
# Install a certificate from an internal or public CA
purearray setattr --tls-certificate <cert_file>

# Verify current TLS certificate
purearray list --ssl-certificate
```

Steps:
1. Generate a CSR from the array or prepare a certificate from your CA
2. Import the signed certificate using `purearray setattr --tls-certificate`
3. Verify the certificate is applied and trusted by your browser/admin workstation
4. Do not use self-signed certificates in production environments

## Compliance Notes

| Framework | Relevant Controls |
|---|---|
| **FIPS 140-2** | FlashArray //X supports FIPS 140-2 Level 2 validated cryptographic modules; confirm with Pure account team for specific model certification status |
| **PCI DSS** | Encryption at rest (Req. 3.5), TLS in transit (Req. 4.2), access control RBAC (Req. 7), audit logging (Req. 10), vulnerability management via Purity patches (Req. 6) |
| **ISO 27001** | Supported by access control policies (RBAC), encryption at rest and in transit, audit logging, and SafeMode for data integrity |
| **SOC 2 Type II** | Pure1 and the Evergreen//One service operate under SOC 2 Type II; on-premises array controls must be implemented per this document |
| **HIPAA** | Encryption at rest and in transit, audit logging, and access control satisfy the primary technical safeguard requirements for PHI stored on FlashArray |
| **NIS2 / DORA** | Audit trail, encryption, and availability controls (ActiveCluster) support NIS2 and DORA operational resilience requirements |
