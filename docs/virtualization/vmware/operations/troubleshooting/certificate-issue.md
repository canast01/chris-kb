---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Certificate Issues

<div class="kb-summary">
Diagnosing and resolving certificate errors across the VMware platform — VCSA certificate expiry, ESXi thumbprint mismatches, NSX certificate chains, and Aria certificate rotation.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
quick_diagnosis: "Quick Diagnosis" {shape: rectangle}
browser_certificate_warning_on_vcent: "Browser Certificate Warning on vCenter Login" {shape: rectangle}
login_failure_after_certificate_rene: "Login Failure After Certificate Renewal" {shape: rectangle}
product_integration_broken_after_cer: "Product Integration Broken After Certificate Change" {shape: rectangle}
nsx_certificate_thumbprint_mismatch: "NSX Certificate Thumbprint Mismatch" {shape: rectangle}
esxi_host_certificate_issues: "ESXi Host Certificate Issues" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> quick_diagnosis: investigate
symptom -> browser_certificate_warning_on_vcent: investigate
symptom -> login_failure_after_certificate_rene: investigate
symptom -> product_integration_broken_after_cer: investigate
symptom -> nsx_certificate_thumbprint_mismatch: investigate
symptom -> esxi_host_certificate_issues: investigate
quick_diagnosis -> resolution
browser_certificate_warning_on_vcent -> resolution
login_failure_after_certificate_rene -> resolution
product_integration_broken_after_cer -> resolution
nsx_certificate_thumbprint_mismatch -> resolution
esxi_host_certificate_issues -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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


```text title="Expected output"
=== MACHINE_SSL_CERT ===
Subject: CN=vcenter.corp.local,O=VMware,C=US
Not After: 2025-12-15T23:59:59Z

=== VMCA_ROOT ===
Subject: CN=VMware-VCSA-CSR,O=VMware,C=US
Not After: 2026-03-22T23:59:59Z

=== data-encipherment ===
Subject: CN=vcenter.corp.local,O=VMware,C=US
Not After: 2025-12-15T23:59:59Z

subject=CN = vcenter.corp.local, O = VMware, C = US
notBefore=Dec 15 10:30:45 2023 GMT
notAfter=Dec 15 23:59:59 2025 GMT
```

!!! warning "Common errors"
    **`vecs-cli: command not found`** — Run the command directly on the VCSA appliance shell (SSH to vCenter), not from a remote host.
    **`unable to get local issuer certificate`** — Add `-CAfile /etc/ssl/certs/ca-bundle.crt` to the openssl command or use `-servername <vcenter-fqdn>` for SNI support on the vCenter host.
    **`Connection refused`** — Verify vCenter is running and accessible on port 443 by testing with `curl -k https://<vcenter-fqdn>` first.
---

## Browser Certificate Warning on vCenter Login

**Symptom:** Browser shows `NET::ERR_CERT_AUTHORITY_INVALID` or an untrusted certificate warning when opening the vCenter FQDN.

**Likely cause:** Machine SSL certificate is self-signed, expired, or the CA is not trusted by the browser.

**Step 1 — Check expiry:**

```bash
openssl s_client -connect <vcenter-fqdn>:443 -showcerts </dev/null 2>/dev/null \
  | openssl x509 -noout -dates
```


```text title="Expected output"
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2026 GMT
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the vCenter FQDN is correct and the host is reachable on port 443 with `nc -zv <vcenter-fqdn> 443`.
    **`error:14090086:SSL routines:SSL3_GET_SERVER_CERTIFICATE:certificate verify failed`** — This is expected if vCenter uses a self-signed cert; add `-servername <vcenter-fqdn>` to the openssl command for SNI support and ignore verification warnings for lab environments.
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


```text title="Expected output"
Not After: 2026-03-15T23:59:59Z
Not After: 2025-08-22T14:30:22Z
Not After: 2027-11-09T18:45:10Z
Stopping all services...
Stopped: vmware-vpostgres
Stopped: vmware-vsan-health
Stopped: vmware-mbcs
Stopped: vsan
Stopped: vsphere-ui
Stopped: vpxd
Stopped: vmonapi
Starting all services...
Started: vmware-vpostgres
Started: vmware-vsan-health
Started: vmware-mbcs
Started: vsan
Started: vsphere-ui
Started: vpxd
Started: vmonapi
All services started successfully.
```

!!! warning "Common errors"
    **`vecs-cli: command not found`** — Verify the vmafd service is running with `systemctl status vmware-vmafd` and ensure you're executing on the vCenter appliance, not a remote host.
    **`Error: Failed to start service vpxd. Check /var/log/vmware/vpxd/vpxd.log for details.`** — Review the vpxd log for startup errors (often certificate or database connectivity issues) before attempting to restart dependent services.
    **`Error: Cannot stop all services — some services are locked by running processes.`** — Wait 30–60 seconds for in-flight requests to complete, then retry `service-control --stop --all`, or use `service-control --stop --all --force` if the delay is unacceptable.
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


```text title="Expected output"
SHA256 Fingerprint=AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify the vCenter FQDN is correct and the host is reachable on port 443 using `ping` or `nc -zv <vcenter-fqdn> 443`.
    **`unable to load certificate`** — The server is not responding with a valid SSL certificate; check that vCenter is running and accessible with `curl -kv https://<vcenter-fqdn>`.
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


```text title="Expected output"
{
  "results": [
    {
      "id": "compute-manager-1",
      "display_name": "vCenter-Prod-01",
      "server": "vcenter.prod.local",
      "connection_status": "UP",
      "origin_type": "vCenter",
      "version": "7.0.3"
    },
    {
      "id": "compute-manager-2",
      "display_name": "vCenter-DR-01",
      "server": "vcenter.dr.local",
      "connection_status": "DOWN",
      "origin_type": "vCenter",
      "version": "7.0.3"
    }
  ],
  "result_count": 2
}
```

!!! warning "Common errors"
    **`{"error_code": 401, "error_message": "Unauthorized"}`** — Verify NSX API credentials and ensure the user account has API access permissions.
    **`{"error_code": 404, "error_message": "Not Found"}`** — Confirm the NSX Manager hostname/IP is correct and the API endpoint is accessible on port 443.
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


```text title="Expected output"
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2025 GMT
```

!!! warning "Common errors"
    **`connect: Connection refused`** — Verify the ESXi host is reachable on port 443 and the management network is accessible (ping the FQDN first).
    **`unable to load certificate`** — Ensure you're piping valid SSL certificate data; replace `<esxi-fqdn>` with the actual ESXi hostname or IP address.
    **`Name or service not known`** — Resolve the ESXi FQDN to an IP address by checking DNS or using the IP directly instead of the hostname.
**Renew from vCenter UI:**
- Select host → Configure → Certificate → Renew

**Bulk renewal via VCSA certificate-manager:**

```bash
# On VCSA — renew all host certificates (re-issues via VMCA)
/usr/lib/vmware-vmca/bin/certificate-manager
# Choose option 3 — Replace Machine SSL certificate with VMCA Certificate
# Or option 8 — Reset all certificates (use only in break-glass scenarios)
```


```text title="Expected output"
vSphere Certificate Manager for vCenter Server Appliance

1. Replace Machine SSL certificate with VMCA Certificate
2. Replace VMCA Root certificate with Custom Certificate
3. Replace Machine SSL certificate with Custom Certificate
4. Replace Smart Card certificate with Custom Certificate
5. Regenerate a new VMCA Root certificate and all certificates
6. Replace root certificate of an external PSC with Custom Certificate
7. Replace Machine SSL certificate of an external PSC with Custom Certificate
8. Reset all certificates

Please select an option [1 to 8]: 3
Retrieving Machine SSL certificate details...
Machine SSL certificate will be replaced with VMCA Certificate.
Please provide the following details:
PNID (Fully Qualified Domain Name) [vcsa.corp.local]: vcsa.corp.local
IP Address [192.168.1.50]: 192.168.1.50
Common Name (CN) [vcsa.corp.local]: vcsa.corp.local
Organization Name [VMware]: VMware
Organization Unit [vSphere]: vSphere
State [CA]: CA
Country [US]: US
Email [admin@corp.local]: admin@corp.local
Hostname [vcsa-01]: vcsa-01

Generating new Machine SSL certificate...
Certificate generated successfully.
Updating vCenter services...
Services restarted successfully.
Certificate replacement completed.
```

!!! warning "Common errors"
    **`Error: VMCA service is not running`** — Start the VMCA service with `systemctl start vmware-vmca` before running certificate-manager.
    **`Error: Certificate generation failed - Invalid PNID`** — Ensure the PNID matches the FQDN exactly and that DNS resolves correctly with `nslookup vcsa.corp.local`.
    **`Error: vCenter services failed to restart`** — Check service status with `systemctl status vmware-*` and manually restart critical services if needed.
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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Datastore Issues](datastore-inaccessible.md)
- [Host Disconnected / Not Responding](host-disconnected.md)
- [Known Issues and Fix Patterns](known-issues.md)
- [Virtualization Troubleshooting](index.md)
