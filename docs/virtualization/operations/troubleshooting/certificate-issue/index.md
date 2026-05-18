# Certificate Issues

> Part of the [Troubleshooting](../) hub.

```
┌─────────────────────────────────────────────────────────────────┐
│                  CERTIFICATE ISSUE TRIAGE FLOW                  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────▼────────────┐
              │  Symptom: Browser warn  │
              │  Login fail / API error │
              │  Integration broken     │
              └────────────┬────────────┘
                           │
              ┌────────────▼────────────┐
              │  Identify Component     │
              │  VCSA Machine SSL       │
              │  STS / VMCA / ESXi host │
              │  NSX / Aria cert        │
              └────────────┬────────────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────────┐
    │ Expired? │    │ Thumbprt │    │  CA Untrusted│
    │ Renew via│    │ Mismatch?│    │  Push root   │
    │ VAMI/CLI │    │ Re-register│  │  to clients  │
    └────┬─────┘    └────┬─────┘    └──────┬───────┘
         └───────────────┴──────────────────┘
                          │
              ┌───────────▼───────────┐
              │  Validate             │
              │  Browser clean        │
              │  Integrations OK      │
              │  Update cert inventory│
              └───────────────────────┘
```

---
## Quick Diagnosis

```bash
# Check vCenter certificate expiry (run from VCSA shell)
for store in MACHINE_SSL_CERT VMCA_ROOT data-encipherment; do
  echo "=== $store ==="
  /usr/lib/vmware-vmafd/bin/vecs-cli entry list --store $store --text | grep -E "Subject:|Not After"
done

# Check current Machine SSL cert expiry via OpenSSL
openssl s_client -connect <vcenter-fqdn>:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

---

## Browser Certificate Warning on vCenter Login

**Symptom:** Browser shows `NET::ERR_CERT_AUTHORITY_INVALID` or an untrusted certificate warning when opening the vCenter FQDN.

**Likely cause:** Machine SSL certificate is self-signed, expired, or the CA is not trusted by the browser.

**Step 1 — Check expiry:**

```bash
openssl s_client -connect <vcenter-fqdn>:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -dates
```

**Step 2 — Renew via VAMI if expired:**

1. Browse to `https://<vcenter-fqdn>:5480`
2. Go to **Certificate Management**
3. Under Machine SSL Certificate, click **Renew** (VMCA-signed certs) or **Import and Replace** (custom CA)

**Step 3 — If using custom CA**, push the trusted root to client browsers via GPO or add to the OS trust store.

---

## Login Failure After Certificate Renewal

Renewing the Machine SSL cert can break SSO if the STS (Security Token Service) certificate is also expired or not updated.

```bash
# Check STS signing certificate expiry
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store TRUSTED_ROOTS --text | grep "Not After"

# Restart all vCenter services after cert changes
service-control --stop --all && service-control --start --all
```

**If STS cert is expired** — this requires special remediation:

1. Reference VMware KB 79248 for the `fixsts.sh` procedure.
2. This requires SSH access to VCSA as root.
3. The STS cert is replaced via LDAP update or the `fixsts.sh` script depending on vCenter version.
4. After replacement, restart all vCenter services.

---

## Product Integration Broken After Certificate Change

**Affected integrations:** Aria Operations, Aria Ops for Logs, Veeam, SRM, NSX, Horizon.

When the Machine SSL cert is replaced, products registered against the old thumbprint will fail.

**Step 1 — Get current cert thumbprint:**

```bash
openssl s_client -connect <vcenter-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -fingerprint -sha256 -noout
```

**Step 2 — Re-register or accept the new certificate in each product:**

| Product | Where to update |
|---|---|
| Aria Operations | Admin → Solutions → Cloud Accounts → Edit vCenter → Accept new certificate |
| Veeam B&R | Managed Servers → vCenter → Rescan → accept new fingerprint |
| SRM | SRM plugin → re-pair sites → accept new certs on both sides |
| NSX | Infrastructure → vCenter Server → Actions → Resync |

---

## NSX Certificate Thumbprint Mismatch

```bash
# Check compute manager status via NSX API
GET /api/v1/fabric/compute-managers
# Look for connection_status — should be "UP"
```

If the thumbprint mismatch persists after resync:
1. Remove the compute manager from NSX Manager (Infrastructure → vCenter Server → Delete).
2. Re-add it — NSX will prompt to accept the new certificate.
3. Allow time for transport node re-sync before making any NSX fabric changes.

---

## ESXi Host Certificate Issues

ESXi host certificates can expire independently. An expired host cert causes vCenter warnings, breaks vSAN encryption, and can disrupt HA heartbeats.

```bash
# Check ESXi host cert expiry from the host CLI
openssl s_client -connect <esxi-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -dates
```

**Renew from vCenter UI:**
- Select host → Configure → Certificate → Renew

**Bulk renewal via VCSA certificate-manager:**

```bash
# On VCSA — renew all host certificates (re-issues via VMCA)
/usr/lib/vmware-vmca/bin/certificate-manager
# Choose option 3 — Replace Machine SSL certificate with VMCA Certificate
# Or option 8 — Reset all certificates (use only in break-glass scenarios)
```

---

## Certificate Expiry Monitoring

Key lead times:

| Timeline | Action |
|---|---|
| 60 days out | Plan renewal, raise change ticket |
| 30 days out | Schedule maintenance window |
| 7 days out | Treat as P2 — renew immediately |
| Expired | Emergency procedure — services may already be failing |

```powershell
# PowerCLI — quick check on vCenter Machine SSL expiry
$certBytes = (Connect-VIServer -Server <vcenter-fqdn>).ExtensionData.Config.Certificate
$cert = [System.Security.Cryptography.X509Certificates.X509Certificate2]::new([byte[]]$certBytes)
$cert | Select Subject, NotBefore, NotAfter
```
