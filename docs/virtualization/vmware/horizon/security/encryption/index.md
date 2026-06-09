# VMware Horizon — Encryption

```text
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
```text
┌──────────────┐  Blast AES  ┌───────────┐                      ────────────────────────────────────────▼
│  Horizon     │─────────────►│  UAG      │─────────────►┌──────────────────┐
│  Client      │  8443/TCP   │  Blast GW │  8443 proxy  │  Desktop VM                                   │
│  (Blast)     │             └───────────┘              │  (Blast agent)                                │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
## Option 1: Via UAG Admin UI (port 9443) → SSL Server Certificate → Upload
## Upload PKCS12 (.pfx) or PEM (cert + key)

## Option 2: Via UAG REST API
curl -sk -X PUT "https://uag.example.local:9443/rest/v1/config/certs/ssl" \
  -u admin:<password> \
  -F "file=@/path/to/uag.pfx" \
  -F "password=pfxpassword"
```
```yaml
Group Policy → Computer Configuration → Policies → VMware Blast
  Clipboard Redirection:
    - Disabled: no clipboard between client and desktop
    - Client to Agent only: paste from client → desktop, not reverse
    - Agent to Client only: paste from desktop → client, not reverse
    - Enabled (bidirectional): default — not recommended for sensitive data
```
```text
Group Policy → User Configuration → VMware Horizon Client Configuration → USB
  Allow USB Redirection: Enabled
  Exclude Device Family: Storage (block USB mass storage to prevent data exfiltration)
  Allow specific VID/PID: <CAC reader VID:PID> (allow smart card readers only)
```
```powershell
## Restrict TLS on Connection Server to 1.2 and 1.3 only
## Edit locked.properties file:
$lockedProps = "C:\Program Files\VMware\VMware View\Server\sslgateway\conf\locked.properties"

Add-Content $lockedProps "`nsslprotocols=TLSv1.2,TLSv1.3"
Add-Content $lockedProps "enabledCipherSuites=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256"

## Restart Connection Server service
Restart-Service "VMware Horizon View Connection Server"
```
```text
Group Policy → Computer Configuration → VMware Horizon Agent
  Drive Redirection: Disabled
```
