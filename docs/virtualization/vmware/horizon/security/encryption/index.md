# Horizon — Encryption

---

## Display Protocol Encryption

| Protocol | Encryption | Notes |
|---|---|---|
| Blast Extreme | AES-128 or AES-256 | Configured per-pool or globally; AES-256 via GPO |
| PCoIP | AES-128 via TLS 1.2 | Default; no weak cipher fallback |
| RDP (if enabled) | TLS 1.2 | Not recommended — use Blast or PCoIP |

Set Blast cipher strength via Horizon group policy (ADMX templates):
```
Computer Configuration → Policies → VMware Blast
  Encryption Algorithms: AES-256-GCM:AES-128-GCM
  H264 Encoding: Enabled (reduce bandwidth without reducing encryption)
```

---

## Connection Server Certificate

```powershell
# Install PFX certificate on Connection Server
Import-PfxCertificate -FilePath "horizon-cs01.pfx" -CertStoreLocation Cert:\LocalMachine\My -Password (ConvertTo-SecureString "pfxpassword" -AsPlainText -Force)

# Get thumbprint of installed cert
Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -match "horizon-cs01" }

# Update Horizon Connection Server to use the new cert:
# Windows Certificate Manager → Lock the cert for vdm service:
# Set the Friendly Name to "vdm" on the certificate
# Restart VMware Horizon View Connection Server service
Restart-Service -Name "VMwareVDMDS"
```

---

## UAG Certificate

UAG serves the HTTPS termination point for external connections. Replace the self-signed cert:

```bash
# Option 1: Via UAG Admin UI (port 9443) → SSL Server Certificate → Upload
# Upload PKCS12 (.pfx) or PEM (cert + key)

# Option 2: Via UAG REST API
curl -sk -X PUT "https://uag.corp.local:9443/rest/v1/config/certs/ssl" \
  -u admin:<password> \
  -F "file=@/path/to/uag.pfx" \
  -F "password=pfxpassword"
```

UAG requires separate certificates for:
- HTTPS admin interface (port 9443)
- Blast Extreme gateway (port 8443) — can share with HTTPS cert or be separate

---

## Clipboard Encryption and Control

Clipboard direction can be restricted via GPO to prevent data exfiltration:

```
Group Policy → Computer Configuration → Policies → VMware Blast
  Clipboard Redirection:
    - Disabled: no clipboard between client and desktop
    - Client to Agent only: paste from client → desktop, not reverse
    - Agent to Client only: paste from desktop → client, not reverse
    - Enabled (bidirectional): default — not recommended for sensitive data
```

For high-security environments: set to "Client to Agent only" — users can copy instructions into the desktop but cannot exfiltrate data by copying out.

---

## USB Redirection Encryption

USB traffic is tunneled through the Blast or PCoIP protocol connection (encrypted). Restrict USB device types via policy:

```
Group Policy → User Configuration → VMware Horizon Client Configuration → USB
  Allow USB Redirection: Enabled
  Exclude Device Family: Storage (block USB mass storage to prevent data exfiltration)
  Allow specific VID/PID: <CAC reader VID:PID> (allow smart card readers only)
```

---

## Persistent Disk Encryption

Persistent disks (Full Clone pool dedicated disks or App Volumes writable volumes) should use storage-layer encryption:

- **vSAN encryption**: apply encrypted storage policy to the pool datastore
- **vSphere VM Encryption**: encrypt the VM including its disks
- **BitLocker in guest**: requires TPM 2.0 or virtual TPM in VM — adds complexity for VDI

App Volumes writable volumes (VHD/VMDK files on a datastore) are not encrypted by default — protect via vSAN or datastore encryption.

---

## TLS Version Enforcement on Connection Server

```powershell
# Restrict TLS on Connection Server to 1.2 and 1.3 only
# Edit locked.properties file:
$lockedProps = "C:\Program Files\VMware\VMware View\Server\sslgateway\conf\locked.properties"

Add-Content $lockedProps "`nsslprotocols=TLSv1.2,TLSv1.3"
Add-Content $lockedProps "enabledCipherSuites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"

# Restart Connection Server service
Restart-Service "VMware Horizon View Connection Server"
```

---

## Drive Mapping Encryption

Drive redirection (mapping client drives in the desktop) goes through the encrypted display protocol tunnel. To disable drive mapping entirely for compliance:

```
Group Policy → Computer Configuration → VMware Horizon Agent
  Drive Redirection: Disabled
```
