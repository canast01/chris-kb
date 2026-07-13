---
tags:
  - security
  - vcenter
  - vmware
  - vsphere-8
description: "Encryption reference covering vSAN Encryption, Certificate Encryption, VM Encryption Key Flow, vSphere Trust Authority (vTA), Certificate Management and 3..."
---
# vCenter Security — Encryption

<div class="kb-summary">
Encryption reference covering vSAN Encryption, Certificate Encryption, VM Encryption Key Flow, vSphere Trust Authority (vTA), Certificate Management and 3 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
![vCenter Security — Encryption](../../../../../assets/virtualization-vmware-vcenter-security-encryption.svg)

## Before you begin

- **Access:** vCenter Administrator role
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## vSphere Trust Authority (vTA)

vSphere Trust Authority (vTA), available from vSphere 7.0+, provides hardware-attested trust for ESXi hosts. A dedicated Trust Authority cluster attests that ESXi hosts are running trusted firmware and software before they are allowed to receive encryption keys.

Use cases:
- Prevent rogue or compromised ESXi hosts from decrypting encrypted VMs
- Enable attestation-based key release (hosts must pass TPM 2.0 attestation)
- Meets requirements for regulated environments requiring hardware root of trust

Configuration is more complex than NKP — requires a dedicated Trust Authority cluster and proper TPM 2.0 hardware on all compute hosts.

---

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

---

## Certificate Replacement Procedures

### Machine SSL Certificate (VMCA-Signed Renewal)

The simplest replacement — use when VMCA is the CA and no custom CA is required:

```bash
# SSH to VCSA
/usr/lib/vmware-vmca/bin/certificate-manager

# Select option 6: Replace Machine SSL certificate with VMCA Certificate
# Enter administrator@vsphere.local credentials
# Accept default certificate parameters or customise CN/SAN
# The tool will replace the cert and restart required services
```


```text title="Expected output"
VMware Certificate Manager
Version 7.0.3 Build 21958341

1. Generate Certificate Signing Request (CSR)
2. Create a Self-Signed Certificate
3. Replace Machine SSL Certificate
4. Replace VMCA Root Certificate
5. Replace Solution User Certificates
6. Replace Machine SSL certificate with VMCA Certificate
7. Regenerate VMCA Root Certificate
8. Reset all Certificates
9. Exit

Select an option [1-9]: 6

Retrieving VMCA Certificate...
Enter username [Administrator@vsphere.local]: administrator@vsphere.local
Enter password: 

Certificate Details:
  Subject: CN=vcsa-01.corp.local,O=VMware,C=US
  Issuer: CN=VMCA,O=VMware,C=US
  Valid From: 2024-01-15 10:30:00 UTC
  Valid Until: 2026-01-15 10:30:00 UTC

Do you want to replace the Machine SSL Certificate? (Y/N): Y

Replacing Machine SSL Certificate...
Certificate replaced successfully.

Restarting services:
  - vmware-vpxd
  - vmware-vsan-health
  - vmware-rhttpproxy

All services restarted successfully.
```

!!! warning "Common errors"
    **`Authentication failed for user administrator@vsphere.local`** — Verify the password is correct and the user account is not locked; reset credentials via DCUI if needed.
    **`Certificate replacement failed: Certificate chain validation error`** — Ensure VMCA root certificate is valid and not expired by checking `/etc/vmware-vpx/ssl/vmca_issued_certs.pem`.
    **`Service restart timeout: vmware-vpxd did not respond within 120 seconds`** — Wait 2-3 minutes for services to stabilize, then manually restart with `service-control --restart --all` if the issue persists.
After renewal:
```bash
# Verify new certificate dates
echo | openssl s_client -connect vcenter.example.local:443 2>/dev/null \
    | openssl x509 -noout -dates

# Confirm services recovered
service-control --status --all
```


```text title="Expected output"
notBefore=Jan 15 10:23:45 2024 GMT
notAfter=Jan 15 10:23:45 2025 GMT
Service vpxd is running
Service vsan-health is running
Service wcp is running
Service vsphere-ui is running
Service rhttpproxy is running
Service vmonapi is running
Service sps is running
Service pschealth is running
```

!!! warning "Common errors"
    **`error in x509 lookup v3 extensions`** — Ensure the certificate chain is complete; use `openssl s_client -connect vcenter.example.local:443 -showcerts` to verify all intermediate certificates are present.
    **`Service vpxd is stopped`** — Restart the vCenter service with `service-control --start --all` and wait 2–3 minutes for dependent services to initialize.
### Machine SSL Certificate (Custom CA)

When your organisation uses an enterprise CA (Microsoft CA, DigiCert, etc.):

```bash
# Step 1 — Generate a CSR
/usr/lib/vmware-vmca/bin/certificate-manager
# Select option 1: Generate Certificate Signing Request(s) and Key(s) for Machine SSL certificate

# The tool outputs a CSR file at /tmp/vmca_issued_csr.csr
# Submit this CSR to your enterprise CA

# Step 2 — After receiving the signed certificate
# Place the cert chain and key in a temp location on VCSA

# Step 3 — Replace the certificate
/usr/lib/vmware-vmca/bin/certificate-manager
# Select option 5: Replace Machine SSL certificate with Custom Certificate
# Provide path to: certificate file, key file, and root CA chain
```


```text title="Expected output"
vCenter Certificate Manager

Please select an option:

1. Generate Certificate Signing Request(s) and Key(s) for Machine SSL certificate
2. Generate Certificate Signing Request(s) and Key(s) for all certificates
3. Regenerate a new Machine SSL certificate
4. Replace Machine SSL certificate with Custom Certificate
5. Replace all Certificates with Custom Certificates
6. Regenerate all certificates
7. Reset all Certificates to default
8. List all certificates

Option [1]: 1

Generating Certificate Signing Request for Machine SSL certificate...
CSR generated successfully at: /tmp/vmca_issued_csr.csr
Key generated at: /tmp/vmca_issued_key.key

Please submit the CSR to your enterprise CA and return with the signed certificate.

---

vCenter Certificate Manager

Please select an option:

1. Generate Certificate Signing Request(s) and Key(s) for Machine SSL certificate
2. Generate Certificate Signing Request(s) and Key(s) for all certificates
3. Regenerate a new Machine SSL certificate
4. Replace Machine SSL certificate with Custom Certificate
5. Replace all Certificates with Custom Certificates
6. Regenerate all certificates
7. Reset all Certificates to default
8. List all certificates

Option [1]: 5

Provide the following paths:
Certificate file path: /tmp/vcenter.crt
Key file path: /tmp/vmca_issued_key.key
Root CA chain file path: /tmp/ca-chain.crt

Validating certificate and key...
Certificate validation: PASSED
Key validation: PASSED
Chain validation: PASSED

Replacing Machine SSL certificate...
Certificate replacement completed successfully.
Services will restart automatically. Please wait...
```

!!! warning "Common errors"
    **`Error: Certificate file not found at /tmp/vcenter.crt`** — Verify the signed certificate file path is correct and readable by the root user.
    **`Error: Private key does not match certificate`** — Ensure the key file corresponds to the CSR that was signed by your CA.
    **`Error: Certificate chain validation failed: untrusted root`** — Include the complete CA chain from intermediate to root CA in the chain file, in order from leaf to root.
### STS Signing Certificate

The STS (Security Token Service) signing certificate is the most impactful — its expiry causes complete login failure for all vSphere accounts. It has a 10-year validity by default but may have been set shorter on older installations.

```bash
# Check STS certificate expiry
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store STS_INTERNAL_SSL_CERT --text \
    | grep -E "Alias|Not After"

# If expired — this requires special recovery steps
# See VMware KB 2112283 for the STS certificate renewal procedure
# Summary:
# 1. Stop all services
# 2. Run the certificate-manager STS renewal
# 3. Restart all services

service-control --stop --all
/usr/lib/vmware-vmca/bin/certificate-manager
# Select option 8: Reset all certificates
service-control --start --all
```


```text title="Expected output"
Alias                                    : STS_INTERNAL_SSL_CERT
Not After                                : Dec 18 14:32:15 2025 GMT
(no output — command completes silently)
Stopping all services...
Service vmon stopped
Service vmafdd stopped
Service vmdird stopped
Service vmcad stopped
Service vpostgres stopped
All services stopped successfully.

2019-01-01T08:45:23.456Z - certificate-manager
======================================
VMware Certificate Manager
======================================
1. Replace Machine SSL certificate
2. Replace VMCA Root certificate
3. Replace PSC SSL certificate
4. Replace Solution User certificates
5. Regenerate a new VMCA Root certificate and all certificates
6. Replace Smart Card certificate
7. Replace Authentication Proxy Server certificate
8. Reset all certificates
9. Exit
Select an option [1-9]: 8
Resetting all certificates...
All certificates reset successfully.
Starting all services...
Service vmon started
Service vmafdd started
Service vmdird started
Service vmcad started
Service vpostgres started
All services started successfully.
```

!!! warning "Common errors"
    **`vecs-cli: command not found`** — Verify you are running this command on the vCenter Server appliance (not a remote host) and that VMware vSphere Authentication Daemon is installed.
    **`Error: Failed to stop service — timeout waiting for service to stop`** — Increase the timeout or manually kill lingering processes with `pkill -9 vmware` before retrying service-control.
    **`certificate-manager: Permission denied`** — Run the command with `sudo` or as root user, as certificate operations require elevated privileges.
**Warning**: If the STS certificate is already expired, the `certificate-manager` may not be able to authenticate. In this case, use the `fix_sts_cert.py` script from VMware KB 79248 or engage VMware Support directly.

---

## NKP Backup and Recovery

The Native Key Provider key material is embedded in vCenter. If vCenter is restored from backup or rebuilt, the NKP must also be restored for encrypted VMs to be accessible.

```bash
# Backup procedure (do this immediately after creating NKP, and after any key rotation)
# vSphere Client → vCenter → Configure → Key Providers → <NKP name> → Back Up
# Download the backup file and store securely (offline or in a separate secrets manager)
# The backup is password-protected — store the password separately from the file
```

Recovery procedure:
1. Deploy new VCSA (or restore from vCenter backup)
2. **vCenter → Configure → Key Providers → Restore Key Provider**
3. Provide the backup file and the backup password
4. Encrypted VMs will become accessible once the NKP is restored

If the NKP backup is lost and vCenter cannot be restored: encrypted VM disks are permanently inaccessible. This is by design — encryption without key recovery is irreversible.

---

## VM Encryption Storage Policy

VM encryption is applied through a Storage Policy:

1. Create a storage policy: **vCenter → Policies and Profiles → VM Storage Policies → Create**
2. In the policy rules, enable **Encryption** and select the key provider
3. Apply the policy to a VM: **VM → Edit Settings → VM Options → Encryption → Encrypt VM**

```powershell
# Check VM encryption status across the environment
Get-VM | ForEach-Object {
    $encrypted = $_.ExtensionData.Config.KeyId -ne $null
    [PSCustomObject]@{
        Name = $_.Name
        Encrypted = $encrypted
        KeyId = $_.ExtensionData.Config.KeyId.KeyId
        ProviderId = $_.ExtensionData.Config.KeyId.ProviderId.Id
    }
} | Where-Object { $_.Encrypted } | Format-Table -AutoSize
```

vSAN encryption is preferred over per-VM encryption in all-vSAN environments — it is more performant and simpler to manage at scale.

## See also

- [vCenter Security — Hardening](../hardening/)
- [vCenter — Health Checks](../../operations/health-checks/)
