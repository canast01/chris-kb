# Horizon — Encryption


<div class="kb-summary">
Encryption reference covering Connection Server Certificate, UAG Certificate, Clipboard Encryption and Control, USB Redirection Encryption, Persistent Disk Encryption and 2 more sections.
</div>

  TLS Encryption Path: Client to Desktop
```
```
┌──────────────┐  TLS 1.2+   ┌───────────┐  TLS 1.2+  ┌──────────────────┐
│  Horizon     │─────────────►│  UAG      │────────────►│  Connection      │
│  Client      │  443 (HTTPS)│  (DMZ)    │  443/proxy  │  Server           │
│  (external)  │             └───────────┘             └──────────────────┘
└──────────────┘                                                 │
```text
                                                        TLS / Blast AES-256
```
┌──────────────┐  Blast AES  ┌───────────┐                      ▼
│  Horizon     │─────────────►│  UAG      │─────────────►┌──────────────────┐
│  Client      │  8443/TCP   │  Blast GW │  8443 proxy  │  Desktop VM      │
│  (Blast)     │             └───────────┘              │  (Blast agent)   │
└──────────────┘                                        └──────────────────┘
```
┌───────────────────────────────────── VMware Horizon — Encryption ─────────────────────────────────────┐
│                                                                                                       │
│  Horizon encrypts all sessions via Blast Extreme (TLS) or PCoIP; management traffic                   │
│  is TLS 1.2+; VM disk encryption is handled by vSphere/vSAN layer.                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Session Encryption              │  │            Management Encryption            │   │
│   │           Blast Extreme: TLS + AES           │  │              CS to CS: TLS 1.2+             │   │
│   │             PCoIP: AES-256 + UDP             │  │              CS to vCenter: TLS             │   │
│   │          HTML Access: WebSocket TLS          │  │                CS to UAG: TLS               │   │
│   │         USB redirection: TLS tunnel          │  │              REST API: TLS 1.2+             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  All Horizon traffic is encrypted; PCoIP UDP uses AES-256 even without TLS wrapper.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │                 Data at Rest                │   │
│   │         CS cert: replace in Windows          │  │            Desktop VMDK: vSAN enc           │   │
│   │           UAG cert: import via UI            │  │            Profile share: SMB enc           │   │
│   │           TLS 1.2 minimum: enforce           │  │          BitLocker: full clone VMs          │   │
│   │          Cert expiry: monitor 30d+           │  │          AppStack: enc on datastore         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Certificate replacement on CS triggers IIS restart; brief service interruption;                      │
│  UAG cert import via admin UI on port 9443 (no restart needed).                                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Blast Extreme = VMware display protocol; TLS 1.2+ with AES-256                                       │
│  PCoIP         = Teradici protocol; AES-256; UDP-based                                                │
│  HTML Access   = WebSocket over HTTPS; TLS-protected Blast                                            │
│  TLS 1.2+      = minimum for all Horizon management traffic                                           │
│  UAG cert      = public cert on UAG; presented to external clients                                    │
│  CS cert       = Windows cert store on Connection Server                                              │
│  IIS restart   = required after cert replace on CS; brief downtime                                    │
│  vSAN enc      = disk-level AES-256; transparent to Horizon                                           │
│  BitLocker     = Windows full-disk encryption on persistent VMs                                       │
│  SMB enc       = encryption on CIFS profile shares                                                    │
│  AppStack      = App Volumes VMDK; encrypt at vSAN/datastore level                                    │
│  USB tunnel    = redirected USB over TLS tunnel to desktop                                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## UAG Certificate

UAG serves the HTTPS termination point for external connections. Replace the self-signed cert:

```bash
# Option 1: Via UAG Admin UI (port 9443) → SSL Server Certificate → Upload
# Upload PKCS12 (.pfx) or PEM (cert + key)

# Option 2: Via UAG REST API
curl -sk -X PUT "https://uag.example.local:9443/rest/v1/config/certs/ssl" \
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

```yaml
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

```text
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

```text
Group Policy → Computer Configuration → VMware Horizon Agent
  Drive Redirection: Disabled
```
