# NSX — Encryption

```
┌─────────────────────────────────────────────────────────────┐
│              NSX Encryption Planes                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Management Plane — TLS                                     │
│  ┌─────────────┐  TLS 1.2+  ┌──────────────────────────┐    │
│  │ Client/API  │◄──────────►│ NSX Manager VIP  :443    │    │
│  └─────────────┘            └──────────────────────────┘    │
│                                                             │
│  Control Plane — TLS (inter-node)                           │
│  ┌──────────┐  TLS  ┌──────────┐  TLS  ┌──────────┐         │
│  │ Mgr-01   │◄─────►│ Mgr-02   │◄─────►│ Mgr-03   │         │
│  └──────────┘       └──────────┘       └──────────┘         │
│                                                             │
│  Data Plane — IPsec (optional overlay encryption)           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  ESXi TEP ──── Geneve/IPsec ────► Remote ESXi TEP   │    │
│  │  UDP 6081  (encrypted if transport-zone encryption   │   │
│  │             is enabled — AES-NI hardware required)   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                             │
│  Backup Encryption                                          │
│  Backup bundle ── AES-256 passphrase ──► SFTP target        │
│                                                             │
│  Syslog: Manager/Edge ── TLS :6514 ──► SIEM                 │
└─────────────────────────────────────────────────────────────┘
```

## Data in Transit

### API and UI (TLS)

All NSX Manager API and UI traffic uses TLS. NSX 4.x enforces TLS 1.2 minimum; TLS 1.0 and 1.1 are disabled by default.

Verify TLS configuration:

```bash
# From a client machine — test TLS negotiation
openssl s_client -connect nsx-manager.example.local:443 -tls1   # Should fail (TLS 1.0 rejected)
openssl s_client -connect nsx-manager.example.local:443 -tls1_1 # Should fail (TLS 1.1 rejected)
openssl s_client -connect nsx-manager.example.local:443 -tls1_2 # Should succeed
openssl s_client -connect nsx-manager.example.local:443 -tls1_3 # Should succeed if TLS 1.3 enabled

# Check the presented certificate
openssl s_client -connect nsx-manager.example.local:443 -tls1_2 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer
```

### Geneve Overlay Encryption

By default, Geneve overlay traffic between TEPs is **not encrypted** — it relies on underlay isolation (VLAN segmentation, physical security). For environments that require encryption of east-west VM traffic, NSX supports IPsec-based overlay encryption.

Overlay encryption is configured at the transport zone level and encrypts Geneve packets at the TEP-to-TEP layer:

```bash
# Enable overlay encryption on a transport zone via API
curl -sk -u 'admin:password' \
  -X PATCH \
  -H "Content-Type: application/json" \
  -d '{
    "encryption": {
      "encryption_enabled": true
    }
  }' \
  "https://<nsx-manager>/policy/api/v1/infra/sites/default/enforcement-points/default/transport-zones/tz-overlay-compute"
```

Overlay encryption requires sufficient CPU on ESXi hosts (AES-NI hardware acceleration recommended). Measure the CPU overhead before enabling in production.

### FIPS 140-2 Mode

NSX-T supports FIPS 140-2 mode, which restricts cryptographic algorithms to FIPS-approved ciphers only. Enable during initial deployment — FIPS mode cannot be toggled on a running cluster without re-deployment.

FIPS mode is configured during OVA deployment (set in the OVA properties) or via CLI before the cluster is formed:

```bash
# Check FIPS status
nsxcli
get fips status
# Output: FIPS Mode: ENABLED or DISABLED
```

When FIPS mode is enabled, NSX Manager, Edge nodes, and ESXi host agents must all run FIPS-compliant builds.

---

## Certificate Management

### Certificate Types in NSX

| Certificate | Used For | Default |
|---|---|---|
| API certificate | HTTPS to NSX Manager VIP | Self-signed |
| Cluster certificate | Inter-node cluster communication | Self-signed |
| Node certificate | Individual Manager node identity | Self-signed |
| Principal identity cert | Client cert auth for automation accounts | User-provided |
| LDAP client cert | Mutual TLS to LDAP server | Optional |

### View Current Certificates

```bash
# List all imported certificates
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates" | \
  python3 -c "
import sys, json
d = json.load(sys.stdin)
for c in d.get('results', []):
    cid   = c.get('id', '?')
    name  = c.get('display_name', '?')
    expiry = c.get('not_after', '?')
    print(f'  {cid:<40} {name:<30} expires={expiry}')
"

# Thumbprint of the API certificate (used for vCenter trust)
nsxcli
get certificate api thumbprint
```

### Replace the API Certificate with a CA-Signed Certificate

The default self-signed certificate should be replaced with a certificate from the corporate CA in production environments.

```bash
# Step 1 — Generate a CSR on NSX Manager
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "resource_type": "CsrProperties",
    "display_name": "nsx-api-cert",
    "subject": {
      "attributes": [
        {"key": "CN", "value": "nsx-manager.example.local"},
        {"key": "O",  "value": "Corp Inc"},
        {"key": "C",  "value": "GB"}
      ]
    },
    "key_size": "2048",
    "algorithm": "RSA",
    "extensions": {
      "dns_names": ["nsx-manager.example.local"],
      "ip_addresses": ["10.0.0.50"]
    }
  }' \
  "https://<nsx-manager>/api/v1/trust-management/csrs" | python3 -m json.tool
```

Save the CSR from the response and submit to your CA. Import the signed certificate:

```bash
# Step 2 — Import the signed certificate
CERT_PEM=$(cat nsx-api-signed.crt | awk '{printf "%s\\n", $0}')
KEY_PEM=$(cat nsx-api.key | awk '{printf "%s\\n", $0}')

curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"pem_encoded\": \"${CERT_PEM}\",
    \"private_key\": \"${KEY_PEM}\"
  }" \
  "https://<nsx-manager>/api/v1/trust-management/certificates?action=import"
# Returns the certificate ID
```

```bash
# Step 3 — Apply the certificate to the API endpoint
curl -sk -u 'admin:password' \
  -X POST \
  "https://<nsx-manager>/api/v1/node/services/http?action=apply_certificate&certificate_id=<cert-id>"
```

After applying, the Manager UI/API will present the new certificate. Verify in a browser or via openssl.

### Certificate Expiry Monitoring

```bash
# Check expiry of all NSX-managed certificates
curl -sk -u 'admin:password' \
  "https://<nsx-manager>/api/v1/trust-management/certificates?details=true" | \
  python3 -c "
import sys, json
from datetime import datetime, timezone
d = json.load(sys.stdin)
now = datetime.now(timezone.utc)
for c in d.get('results', []):
    name   = c.get('display_name', c.get('id','?'))
    expiry = c.get('not_after','')
    if expiry:
        exp_dt = datetime.fromisoformat(expiry.replace('Z','+00:00'))
        days   = (exp_dt - now).days
        flag   = '' if days > 60 else '  *** EXPIRING SOON' if days > 14 else '  *** EXPIRED/CRITICAL'
        print(f'  {name:<40} expires={expiry[:10]}  days_remaining={days}{flag}')
"
```

Alert when any certificate has fewer than 60 days remaining.

---

## Syslog over TLS

Configure syslog export over TLS to prevent log data from transiting the network in plaintext:

```bash
# On NSX Manager node
nsxcli
set service syslog exporter siem-tls level info protocol TLS server 10.0.0.100 port 6514

# Verify
get service syslog exporters
```

For mutual TLS syslog (where the syslog server also validates the NSX Manager certificate), import the SIEM server's CA certificate into NSX Manager trust store:

```bash
curl -sk -u 'admin:password' \
  -X POST \
  -H "Content-Type: application/json" \
  -d "{\"pem_encoded\": \"$(cat siem-ca.crt | awk '{printf "%s\\n", $0}')\"}" \
  "https://<nsx-manager>/api/v1/trust-management/certificates?action=import"
```

---

## Backup Encryption

NSX Manager backups are encrypted with the passphrase configured in the backup settings. The passphrase uses AES-256 encryption. Without the passphrase, a backup bundle cannot be decrypted or restored.

Requirements:
- Store the passphrase in a secrets vault (HashiCorp Vault, CyberArk, or equivalent)
- Document where the passphrase is stored in the runbook
- Test restore with the passphrase quarterly

Never store the passphrase in the same system as the backup files.
