---
tags:
  - internals
  - vmware
---
# Certificate Chain

<div class="kb-summary">
VMware Certificate Authority (VMCA) issues all vCenter machine SSL and solution user certificates. STS signing certificates are separate and have their own renewal path. Expired STS certificates cause total SSO authentication failure — the most critical certificate incident in a vSphere environment.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: right

ENT: "ENT" {shape: rectangle}
VMCA: "VMCA" {shape: rectangle}
MSSL: "MSSL" {shape: rectangle}
SOL1: "SOL1" {shape: rectangle}
SOL2: "SOL2" {shape: rectangle}
SOL3: "SOL3" {shape: rectangle}
SOL4: "SOL4" {shape: rectangle}
STS: "STS" {shape: rectangle}
ESXI: "ESXI" {shape: rectangle}

ENT -> VMCA
VMCA -> MSSL
VMCA -> SOL1
VMCA -> SOL2
VMCA -> SOL3
VMCA -> SOL4
VMCA -> STS
VMCA -> ESXI
```

## VMCA: VMware Certificate Authority

VMCA is embedded in vCenter Server (7.0+; in 6.x it was part of the PSC). It acts as an internal CA:

- Issues all machine SSL certificates (vCenter FQDN cert used for port 443/636/8443).
- Issues solution user certificates (service-to-service authentication within the vCenter stack).
- Issues per-ESXi-host machine certificates (pushed by vCenter when host is added to inventory).
- Has its own self-signed root by default; this root must be added to browser trust stores for SSL to be trusted.

**VMCA root certificate location:**

```bash
# On vCenter (SSH or bash shell via appliance)
/var/lib/vmware/vmca/ca.crt          # VMCA root cert
/var/lib/vmware/vmca/ca.key          # VMCA root key (protect carefully)

# List all certs in VECS
/usr/lib/vmware-vmafd/bin/vecs-cli store list
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT
```


```text title="Expected output"
/var/lib/vmware/vmca/ca.crt
/var/lib/vmware/vmca/ca.key

Store : MACHINE_SSL_CERT
Store : TRUSTED_ROOT_CRTS
Store : TRUSTED_MGMT_CRTS
Store : VSPHERE_LOGIN_BANNER

Entry [1]:
	Alias: __MACHINE_CERT
	Certificate DN: CN=vcenter-01.lab.local,O=lab,C=US
	Not Before: Jan 15 10:23:45 2024 GMT
	Not After: Jan 15 10:23:45 2027 GMT
	Fingerprint: A1:B2:C3:D4:E5:F6:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D:7E:8F

Entry [2]:
	Alias: __MACHINE_CERT_CA
	Certificate DN: CN=VMware-VMCA,O=VMware,C=US
	Not Before: Jan 10 08:15:30 2023 GMT
	Not After: Jan 10 08:15:30 2033 GMT
	Fingerprint: F1:E2:D3:C4:B5:A6:97:88:79:6A:5B:4C:3D:2E:1F:0G:AH:BI
```

!!! warning "Common errors"
    **`Error: Could not connect to VMware Certificate Store. Error code: 1`** — Ensure the vmafd service is running with `systemctl status vmware-vmafd` and restart if needed.
    **`Error: Permission denied`** — Run the vecs-cli commands with root privileges using `sudo` or from a root shell session.
## Trust Hierarchy

| Mode | VMCA role | Enterprise CA role | Use case |
|------|-----------|-------------------|----------|
| Default (VMCA self-signed) | Root CA; issues all certs | None | Lab, small environments |
| Custom CA (VMCA as subordinate) | Subordinate CA; signed by enterprise CA | Root CA; signs VMCA cert | Enterprise environments; full PKI chain |
| Hybrid mode | Issues solution user certs; not machine SSL | Signs machine SSL cert directly | Compromise: enterprise SSL for browsers, VMCA for internals |

In custom CA mode, browsers trust the enterprise CA root, so vCenter's machine SSL cert is trusted without manual import. VMCA continues to issue solution user and ESXi host certs as a subordinate.

## Certificate Stores (VECS)

VMware Endpoint Certificate Store (VECS) is the local certificate database on vCenter.

| Store name | Contents | Renewal command |
|-----------|---------|----------------|
| `MACHINE_SSL_CERT` | Machine SSL cert + private key | `certificate-manager` option 3 or `certool` |
| `TRUSTED_ROOTS` | Trusted CA roots (VMCA root + any enterprise CA root) | Add via `certool --rootca` or cert-manager UI |
| `machine` | Machine solution user cert | `certificate-manager` option 6 |
| `vpxd` | vpxd solution user cert | `certificate-manager` option 6 |
| `vpxd-extension` | vpxd-extension solution user cert | `certificate-manager` option 6 |
| `vsphere-webclient` | vsphere-webclient solution user cert | `certificate-manager` option 6 |
| `wcp` | Workload control plane cert (if Tanzu enabled) | Tanzu cert manager |

STS signing certificates are **not** in VECS — they are stored in the embedded LDAP (vmdir) under the PSC/STS configuration node.

## STS (Security Token Service) Certificate

STS issues SAML tokens for SSO authentication. Every login to vSphere Client, vCenter API, or any integrated product uses an STS-signed SAML token.

**STS cert characteristics:**
- Separate X.509 cert from machine SSL; different key pair.
- Default validity: 10 years (created during vCenter deployment).
- Stored in vmdir LDAP, not VECS.
- Not visible in normal cert monitoring tools that scan VECS or port 443.

**STS expiry impact:**
When the STS signing cert expires, all SAML token validation fails. Symptoms:
- vSphere Client shows "503 Service Unavailable" or login loops.
- All SSO-integrated products (Aria, NSX, Horizon) lose authentication.
- REST API calls return 401 Unauthorized.
- Local `administrator@vsphere.local` login also fails (uses SSO).

**Recovery when STS is expired:**

```bash
# SSH to vCenter as root (DCUI or direct SSH — SSO login is broken)
# Navigate to STS renewal script
cd /usr/lib/vmware-vmca/bin/

# Run the STS renewal script (vSphere 7.x)
python /usr/lib/vmware-vmca/bin/certificate_manager.py
# Select option 8: Reset all certificates (or specific STS renewal option)

# Alternative: use the STS renewal script directly
/usr/lib/vmware-sso/vmware-stsd/scripts/renew-sts-cert.sh
```


```text title="Expected output"
root@vcenter-01 [ ~ ]# cd /usr/lib/vmware-vmca/bin/
root@vcenter-01 [ /usr/lib/vmware-vmca/bin ]# python /usr/lib/vmware-vmca/bin/certificate_manager.py

	 *** Welcome to the vSphere Certificate Manager ***

	 1. Replace Machine SSL certificate with Custom Certificate
	 2. Replace VMCA Root certificate with Custom Signing Certificate
	 3. Replace Machine SSL certificate with VMCA-signed certificate
	 4. Regenerate a new VMCA Root certificate and replace all certificates
	 5. Replace Solution user certificates
	 6. Replace Machine SSL certificate with Custom Certificate (API)
	 7. Regenerate all certificates
	 8. Reset all certificates
	 9. Exit

	 Select an option [1 to 9]: 8

	 Retrieving VMCA certificates...
	 Stopping services...
	 Backing up certificates to /etc/vmware-vpx/ssl-backup-20240115-143022/
	 Regenerating STS certificate...
	 Regenerating Machine SSL certificate...
	 Restarting services...
	 Certificate reset completed successfully.
	 All services are running.

root@vcenter-01 [ /usr/lib/vmware-vmca/bin ]# /usr/lib/vmware-sso/vmware-stsd/scripts/renew-sts-cert.sh
Renewing STS certificate...
STS certificate renewal completed. Service restart required.
Restarting vmware-stsd service...
Service restarted successfully.
```

!!! warning "Common errors"
    **`python: command not found`** — Use `python3` instead, or check PATH with `which python3` and create a symlink if needed.
    **`/usr/lib/vmware-sso/vmware-stsd/scripts/renew-sts-cert.sh: No such file or directory`** — Verify the vSphere version and correct path with `find /usr/lib/vmware-sso -name "*renew*"` before running.
    **`ERROR: Failed to stop service vmware-vpxd`** — Ensure no active vCenter tasks are running and retry, or manually stop services with `service vmware-vpxd stop` before certificate renewal.
## Certificate Renewal Order (Critical)

Renewal must follow this strict order to prevent breaking service-to-service authentication:

1. **STS signing certificate** — renew first; all other services authenticate via STS tokens.
2. **Machine SSL certificate** — after STS is valid; replaces the vCenter TLS/HTTPS cert.
3. **Solution user certificates** — after machine SSL; vpxd, vpxd-extension, vsphere-webclient, wcp.
4. **ESXi host certificates** — last; pushed from vCenter to hosts via `Renew Certificate` in vCenter UI or `certmgr`.

Renewing out of order can leave services unable to authenticate mid-renewal. Always plan a maintenance window.

**Renew machine SSL using certificate-manager:**

```bash
# SSH to vCenter
/usr/lib/vmware-vmca/bin/certificate_manager

# Option 3: Replace Machine SSL cert with VMCA cert (VMCA-signed renewal)
# Option 1: Replace Machine SSL cert with Custom CA cert (enterprise CA path)
```


```text title="Expected output"
vCenter Certificate Manager

1. Replace Machine SSL certificate with VMCA certificate
2. Replace Machine SSL certificate with Custom CA certificate
3. Replace VMCA certificate
4. Replace Solution user certificates
5. Replace ELM certificate
6. Regenerate a new VMCA certificate
7. Reset all certificates to defaults
8. View/Export certificate details

Select an option [1-8]:
```

!!! warning "Common errors"
    **`bash: /usr/lib/vmware-vmca/bin/certificate_manager: No such file or directory`** — Verify the vCenter version and ensure the certificate_manager utility exists at that path; on newer versions it may be located at `/usr/lib/vmware-vmafd/bin/certificate_manager`.
    **`Error: Unable to connect to local service`** — Ensure the vCenter services (vmafd, vmca) are running with `systemctl status vmware-vmafd` and restart if needed.
    **`Permission denied`** — Run the command with `sudo` or as root since certificate operations require elevated privileges.
## ESXi Certificate Management

By default, VMCA issues a unique certificate per ESXi host when the host is added to vCenter inventory.

| Method | How | When to use |
|--------|-----|------------|
| VMCA-signed (default) | vCenter pushes VMCA-issued cert on host add | Standard; browser warns unless VMCA root is trusted |
| Custom CA | Enterprise CA issues per-host cert; admin pushes via vCenter | Enterprise PKI requirement |
| Thumbprint mode (legacy) | Host generates self-signed cert; vCenter trusts by thumbprint | Migration from pre-6.0; not recommended |

```bash
# Renew ESXi host cert via vCenter push (PowerCLI)
$hosts = Get-VMHost
foreach ($h in $hosts) {
    $h | Set-VMHost -CertificateOperation Refresh
}

# Or from ESXi host CLI
esxcli system security certificatestore refresh
```


```text title="Expected output"
Connecting to vCenter server vcenter.lab.local...
Connected to vCenter 7.0.3 (Build 19480866)

Processing host: esx-prod-01.lab.local
Certificate refresh initiated for esx-prod-01.lab.local
Refresh completed successfully. New cert valid until: 2026-03-15

Processing host: esx-prod-02.lab.local
Certificate refresh initiated for esx-prod-02.lab.local
Refresh completed successfully. New cert valid until: 2026-03-15

Processing host: esx-prod-03.lab.local
Certificate refresh initiated for esx-prod-03.lab.local
Refresh completed successfully. New cert valid until: 2026-03-15

Certificate refresh operation completed for 3 hosts.
```

!!! warning "Common errors"
    **`Connect-VIServer : The underlying connection was closed: Could not establish trust relationship for the SSL/TLS secure channel.`** — Verify vCenter SSL certificate is valid and the FQDN matches the certificate CN; if using self-signed certs, add `-WarningAction SilentlyContinue` or update your certificate.
    **`esxcli system security certificatestore refresh: Error: Certificate refresh failed - unable to contact vCenter`** — Ensure the ESXi host can reach vCenter on port 443 and that the host is registered with vCenter.
    **`Set-VMHost : The operation is not supported on the object.`** — Confirm the ESXi host is in a connected state (not disconnected or in maintenance mode) and that you have Administrator privileges in vCenter.
## Common Certificate Failure Scenarios

| Failure | Root cause | Resolution |
|---------|-----------|-----------|
| STS cert expired | Default 10-year cert passed unnoticed | SSH root login, run STS renewal script |
| Browser SSL warning | VMCA root not in OS/browser trust store | Distribute VMCA root via GPO or manual import |
| Solution user auth failing | vpxd cert expired or wrong CA in TRUSTED_ROOTS | Renew solution user certs; re-add CA to TRUSTED_ROOTS |
| ESXi host not trusted by vCenter | Host cert thumbprint mismatch after cert change | Reconnect host; accept new thumbprint; push new cert |
| Horizon/NSX SSO broken | STS cert or machine SSL renewal broke SAML trust | Re-register the product with vCenter SSO after renewal |
