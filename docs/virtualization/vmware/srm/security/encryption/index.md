# SRM — Encryption

```text
  TLS Encryption Coverage
┌───────────────────────────────────────────────────────────────┐
│  Traffic Path                        Encryption               │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ SRM ↔ SRM (site pairing, TCP 9086)    TLS 1.2+       │     │
│  │ SRM ↔ vCenter (TCP 443)               TLS 1.2+       │     │
│  │ SRM ↔ Storage Array SRA (TCP 443)     TLS 1.2+       │     │
│  │ VRA ↔ VRA mgmt (TCP 44046)            TLS 1.2+       │     │
│  │ ESXi ──► VRA replication (TCP 31031)  Optional AES   │     │
│  └──────────────────────────────────────────────────────┘     │
│                                                               │
│  Enable per-VM replication encryption:                        │
│  ┌──────────────────────────────────────────────────────┐     │
│  │ vCenter → [VM] → Configure Replication → Edit        │     │
│  │   Enable Replication Data Encryption: Yes (AES-256)  │     │
│  └──────────────────────────────────────────────────────┘     │
└───────────────────────────────────────────────────────────────┘
```

---

## Data in Transit

| Traffic Path | Encryption | Notes |
|---|---|---|
| SRM Server ↔ SRM Server (site pairing) | TLS 1.2+ | TCP 9086 — always encrypted |
| SRM Server ↔ vCenter | TLS 1.2+ | TCP 443 |
| SRM Server ↔ Storage Array (SRA) | TLS 1.2+ | HTTPS to array management IP |
| VRA ↔ VRA (replication control) | TLS 1.2+ | TCP 44046 |
| ESXi ↔ Target VRA (replication data) | Optional | TCP 31031 — can be encrypted or unencrypted per VM config |

---

## vSphere Replication Data Encryption

VR replication can encrypt data in transit between source ESXi and target VRA:

```text
vCenter → [VM] → right-click → Configure Replication → Edit
  Enable Replication Data Encryption: Yes
  (adds AES-256 encryption to the replication stream)
  Note: encryption adds ~5-10% CPU overhead on source host
```

Enable encryption for VMs replicating over untrusted WAN links. For on-premises replication over private LAN, rely on network-level security instead.

---

## Encryption at Recovery Site

When VMs fail over to the recovery site, they inherit the storage encryption state from the source:

- **vSAN encrypted at source → recovered VMs on encrypted vSAN at recovery:** encrypted throughout
- **vSAN encrypted at source → recovered VMs on unencrypted datastore at recovery:** data is unencrypted at recovery — apply an encrypted storage policy at recovery site
- **vSphere VM Encryption:** VM encryption keys are managed by vCenter KMS — if the KMS is unavailable at recovery site, encrypted VMs cannot start. Always include KMS in DR plan or use a shared KMS accessible from both sites.

---

## Certificate Management for SRM Server

SRM Server uses an SSL certificate for HTTPS access (port 443) and inter-site communication (port 9086).

### Replace Certificate (Windows SRM)

```powershell
# Import new cert to Windows Certificate Store
Import-PfxCertificate -FilePath srm-server.pfx `
  -CertStoreLocation Cert:\LocalMachine\My `
  -Password (ConvertTo-SecureString "pfxpassword" -AsPlainText -Force)

# Get thumbprint of new cert
$cert = Get-ChildItem Cert:\LocalMachine\My | Where-Object { $_.Subject -match "srm-protected" }
$cert.Thumbprint

# Configure SRM to use new cert via SRM admin interface:
# https://srm-protected.example.local:9086/admin → Certificate → Replace
# Or re-run SRM installer → Modify → update certificate
```

After replacing the SRM Server cert, update the thumbprint at the remote site:
```text
Recovery Site → Site Recovery → Site Pair → Edit → Accept new thumbprint
```

---

## SRA Credential Storage Encryption

SRA credentials (array username/password or API token) are stored encrypted by SRM. The encryption key is tied to the SRM installation — do not restore SRM from a backup to a different machine without re-entering SRA credentials.

---

## FIPS Mode

SRM 8.x and later support FIPS 140-2 mode when deployed on FIPS-enabled vSphere. Requirements:
- vCenter must be in FIPS mode
- All SRM components must be on FIPS-capable versions
- VRA appliances must be configured for FIPS mode during deployment

Check VMware FIPS compliance documentation before enabling.
