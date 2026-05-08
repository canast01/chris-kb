# vCenter Security — Encryption

## Data in Transit

vCenter enforces TLS 1.2 minimum by default (vSphere 7.0+). TLS 1.0 and 1.1 are disabled.

All API and UI traffic to vCenter uses HTTPS on port 443. VAMI traffic uses HTTPS on port 5480. LDAPS (port 636) is required for Active Directory identity source connections.

Verify TLS configuration after upgrading from older vSphere versions using the `tls-reconfigurator` tool available in the VCSA.

## Data at Rest — VM Encryption

vCenter manages VM-level encryption through vSphere Native Key Provider (NKP) or an external KMS.

### vSphere Native Key Provider (NKP)

Available from vSphere 7.0 U2+. No external KMS required. The key is stored in vCenter and distributed to ESXi hosts.

- Enable from **vCenter → Configure → Key Providers → Add Native Key Provider**
- Back up the NKP immediately after creation — the backup passphrase is required for recovery
- Used for VM encryption, vSAN encryption (where supported), and TPM attestation

### External KMS Integration

For compliance environments requiring an external KMIP-compatible KMS:

- Supported KMS: Thales CipherTrust, Entrust nShield, HyTrust KeyControl
- Register at **vCenter → Configure → Key Providers → Add Standard Key Provider**
- vCenter acts as KMIP client; ESXi hosts retrieve keys via vCenter

### Encrypted VM Management

```powershell
# Check VM encryption status
Get-VM | Get-View | Select-Object -Property Name,
    @{N="Encrypted";E={$_.Config.KeyId -ne $null}}

# Encrypt a VM (requires key provider configured)
# Use vSphere Client: VM → Edit Settings → VM Options → Encryption
```

## vSAN Encryption

vSAN data-at-rest encryption is configured at the cluster level and requires a key provider (NKP or external KMS). Encryption is applied at the disk group layer.

Configure at **vCenter → Cluster → Configure → vSAN → Services → Data Encryption**.

## Certificate Encryption

All vCenter-issued certificates (VMCA) use RSA 2048-bit minimum. Certificate chain of trust is maintained through the VMCA root certificate and STS signing certificate.

See [Authentication](../authentication/) for certificate management procedures.

## Certificate Management

### Certificates to Track

| Certificate | Location | Risk if Expired |
|---|---|---|
| vCenter Machine SSL | VAMI → Certificate Management | Browser warnings, API failures |
| VMCA Root Certificate | VAMI → Certificate Management | Breaks all VMCA-issued certs |
| STS Certificate | vSphere Client → SSO → Certificates | Login failures platform-wide |
| Solution User Certificates | VAMI → Certificate Management | Service-to-service auth failures |
| NSX Manager Certificate | NSX Manager → System | NSX UI and API failures |
| Aria Endpoint Certificates | Aria Suite Lifecycle | Integration and access failures |

### Expiration Tracking Schedule

- Review all certificate expiration dates monthly
- Flag certificates expiring within 60 days — plan replacement
- Escalate certificates expiring within 30 days — urgent action required
- Document next renewal date after each replacement

### Certificate Replacement Process

1. Identify the certificate and replacement method (VMCA, custom CA, or self-signed)
2. Confirm backup of vCenter is current
3. Schedule a maintenance window
4. Replace the certificate using the appropriate method
5. Restart affected services
6. Validate all integrations and logins

### Validation After Replacement

- Browser access to vCenter confirmed with no certificate warning
- All ESXi hosts Connected
- SSO login working for both local and AD accounts
- Aria, NSX, and backup integrations confirmed working

### Emergency Escalation

If certificate expiry causes a login or service failure:
- Check if the local administrator account (`administrator@vsphere.local`) still works
- Engage VMware support if SSO or STS cannot be recovered in place
