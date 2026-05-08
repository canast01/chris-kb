# ONTAP — Encryption

## Volume and Aggregate Encryption

**NetApp Volume Encryption (NVE)**: Software-based, per-volume encryption using AES-256. Each volume has a unique data encryption key (DEK) stored in the key manager. Transparent to applications and protocols.

**NetApp Aggregate Encryption (NAE)**: Encrypts at the aggregate level; all volumes within the aggregate share an aggregate key. Required for deduplication cross-volume savings to persist with encryption.

```bash
# Enable NVE on an existing volume
volume modify -volume <vol> -encrypt true

# Check encryption status
volume show -fields encryption-state

# Verify key manager status
security key-manager show-key-query
security key-manager external show   # for KMIP
security key-manager onboard show    # for OKM
```

## Key Management

- **Onboard Key Manager (OKM)**: Built-in ONTAP key manager; passphrase-protected; suitable for single-cluster environments
- **KMIP External Key Manager**: Integrate with external KMS (Thales CipherTrust, IBM SKLM, HashiCorp Vault via KMIP); required for multi-cluster or compliance mandates (FIPS, PCI-DSS)

```bash
# Configure external KMIP key manager
security key-manager external enable -vserver <admin-svm> -key-servers <kmip-server>:5696 -client-cert <cert-name> -server-ca-certs <ca-name>
```

## TLS and SSH Hardening

```bash
# Enforce TLS 1.2 minimum for HTTPS management
security config modify -interface HTTPS -min-protocol-version TLSv1.2

# Check current TLS/SSL configuration
security config show

# Restrict SSH ciphers and MACs
security ssh modify -vserver <cluster-name> -ciphers aes256-ctr,aes192-ctr,aes128-ctr -macs hmac-sha2-256,hmac-sha2-512

# Disable Telnet and RSH (should be off by default)
security protocol show
# Ensure telnet and rsh show enabled=false

# Rotate admin SSH host key
security ssh server key regenerate
```

## Certificate Management

```bash
# List installed certificates
security certificate show
security certificate show -vserver <svm>

# Install a certificate
security certificate install -vserver <svm> -type server

# Generate a CSR
security certificate generate-csr \
    -common-name <cn> \
    -size 2048 \
    -country US \
    -state <state> \
    -locality <city> \
    -organization <org>
```
