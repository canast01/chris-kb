# Certificate Expiry and Rotation

<div class="kb-summary">
Certificate expiry causes cascading failures across VMware products — SSO authentication breaks,
product-to-product API calls fail, and browsers show trust warnings. Rotation must be done in the
right order because each Aria product and ESXi host trusts the vCenter VMCA as its root authority.
Replace the root before the leaf certs, or all products immediately distrust the new root and break
again. This scenario covers identification, rotation order, and validation across all affected products.
</div>

```text
┌──────────────────────────────── Certificate Expiry and Rotation — Order of Operations ─────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Certificate expiry detected — Aria SuiteLC alert, browser warning, or scheduled audit            ││
│   └────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                                        ▼                                                              │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 1 — Identify expiry: run openssl against vCenter, ESXi, NSX, Aria Ops — record all notAfter dates  ││
│   └────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                                        ▼                                                              │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 2 — Rotation order (top to bottom — NEVER reverse this sequence)                                  ││
│   │                                                                                                          ││
│   │   1. Internal CA / Aria SuiteLC trust store   ──────────────────────────────────── root of all trust    ││
│   │           │                                                                                              ││
│   │           ▼                                                                                              ││
│   │   2. vCenter VMCA (Machine SSL + solution certs)  ──────────── signed by internal CA or self-signed     ││
│   │           │                                                                                              ││
│   │           ▼                                                                                              ││
│   │   3. ESXi host certs (via vCenter certificate manager)  ─────── provisioned by vCenter VMCA             ││
│   │           │                                                                                              ││
│   │           ▼                                                                                              ││
│   │   4. NSX Manager certificate  ──────────────────────────────── independent from VMCA                    ││
│   │           │                                                                                              ││
│   │           ▼                                                                                              ││
│   │   5. Aria Suite products (via Aria SuiteLC)  ────────────────── trust vCenter VMCA as CA                ││
│   └─────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                        │                                                              │
│                                        ▼                                                              │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 3 — Post-rotation: run openssl against all products to confirm notAfter dates updated              ││
│   └──────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| Aria Suite Lifecycle | Certificate manager for all Aria products; manages rotation across the Aria Suite in sequence |
| vCenter Server | VMCA (VMware Certificate Authority) — root CA for ESXi hosts and vCenter solution certs |
| ESXi | Leaf certificates provisioned by VMCA; shows thumbprint warnings in vCenter if stale |
| NSX Manager | TLS certificates for the Manager UI, API, and edge nodes — independent from VMCA |

---

## 1. Identify Expiring Certificates

Run this audit against every VMware product in the environment. Certificates expiring within
60 days should be scheduled for rotation immediately.

```bash
# vCenter certificate expiry
echo | openssl s_client -connect vcenter.domain.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# ESXi host certificate
echo | openssl s_client -connect esxi-host.domain.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# NSX Manager certificate
echo | openssl s_client -connect nsxmanager.domain.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Aria Operations
echo | openssl s_client -connect ariaops.domain.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Aria Operations for Logs
echo | openssl s_client -connect arialogs.domain.local:443 2>/dev/null \
  | openssl x509 -noout -dates
```

```bash
# Batch audit across all known VMware hosts — outputs hostname and notAfter date
for host in vcenter.domain.local nsxmanager.domain.local ariaops.domain.local arialogs.domain.local; do
  printf "%-40s " "$host:"
  echo | openssl s_client -connect $host:443 2>/dev/null \
    | openssl x509 -noout -dates 2>/dev/null | grep notAfter
done
```

---

## 2. Rotate vCenter VMCA Certificate

Two approaches. Option A (CA-signed) is recommended for all production environments. Option B
(renew self-signed) is acceptable for isolated lab environments.

**Option A — Replace with CA-signed certificate (recommended):**

```bash
# SSH into vCenter VCSA, then run the certificate manager
/usr/lib/vmware-vmca/bin/certificate-manager
```

In the certificate manager menu:

1. Select **Option 1**: Replace Machine SSL Certificate with Custom Certificate
2. Follow prompts to generate a CSR
3. Sign the CSR with your internal CA (Active Directory CS, HashiCorp Vault, etc.)
4. Import the signed certificate and CA chain
5. The VCSA services restart automatically after import

**Option B — Renew VMCA self-signed certificate (lab use only):**

```bash
/usr/lib/vmware-vmca/bin/certificate-manager
# Select Option 8: Regenerate all certificates
```

Option 8 regenerates the VMCA root and all solution user certificates. This is fast but the cert
remains self-signed — browsers will still show trust warnings unless you distribute the new VMCA
root to all clients manually.

---

## 3. Rotate ESXi Host Certificates

ESXi host certificates are provisioned by the vCenter VMCA. After replacing the VMCA cert in
step 2, regenerate all ESXi host certificates so they are signed by the new VMCA root.

```powershell
# PowerCLI — renew ESXi certificates from vCenter for all hosts in a cluster
foreach ($vmhost in Get-Cluster "cluster-name" | Get-VMHost) {
    $certMgr = Get-View -Id $vmhost.ExtensionData.ConfigManager.CertificateManager
    Write-Host "Renewing cert on $($vmhost.Name)"
    $certMgr.InstallServerCertificate($null)
}
```

Alternatively via the vCenter UI: **Administration → Certificate Management → Renew**. This
triggers vCenter to push a new VMCA-signed cert to every connected ESXi host.

After renewal, the thumbprint warning banner on each host in vCenter should clear.

---

## 4. Rotate NSX Manager Certificate

NSX uses its own TLS certificate, independent from vCenter VMCA. Replace it through the NSX
Manager UI:

1. NSX Manager → **System** → **Certificates** → **Import Certificate**
2. Paste the signed certificate and private key
3. After import, go to **Service Certificates** → **Edit** next to the API/Manager certificate
4. Select the newly imported certificate and save
5. NSX Manager UI and API will restart — the new cert is active after the restart

NSX edge node certificates (used for BGP and load balancer TLS) are managed separately under
**System → Certificates → Node Certificates**.

---

## 5. Rotate Aria Suite Product Certificates via Aria SuiteLC

Aria Suite Lifecycle manages certificate rotation for all registered Aria products (Aria Operations,
Aria Ops for Logs, Aria Networks, Aria Automation) as a coordinated operation.

Aria SuiteLC → **Lifecycle Operations** → **Environments** → select the Aria environment →
**Certificates** → **Replace**.

Aria SuiteLC will:
1. Validate connectivity to each product
2. Replace certificates in the correct dependency order within the Aria Suite
3. Restart affected services per product
4. Validate that each product is reachable with the new cert before proceeding to the next

**Do not replace Aria product certificates individually outside Aria SuiteLC.** Manual replacement
of individual product certs without updating the SuiteLC trust store causes the products to lose
mutual trust with each other and with vCenter.

---

## 6. Verify Rotation Order Was Followed

The rotation order must be: CA trust store → vCenter VMCA → ESXi hosts → NSX → Aria Suite products.

The reason: every Aria product and every ESXi host trusts the vCenter VMCA as an authority.
If you replace an Aria product cert before replacing the VMCA root, the Aria product receives a
cert signed by the new VMCA root, but the product's trust store still contains only the old VMCA
root. The new cert is immediately untrusted, breaking product-to-vCenter communication.

| Stage | What trusts what | Must come before |
|---|---|---|
| Internal CA / SuiteLC store | Root of all trust chains | Everything else |
| vCenter VMCA | Signs ESXi and solution certs | ESXi, Aria Suite |
| ESXi host certs | Signed by VMCA | — |
| NSX cert | Independent; trusts external CA | — |
| Aria Suite certs | Trust vCenter VMCA | vCenter VMCA rotated first |

---

## Post-Task Validation

```bash
# Verify new expiry dates on all products after rotation
for host in vcenter.domain.local nsxmanager.domain.local ariaops.domain.local arialogs.domain.local; do
  printf "%-40s " "$host:"
  echo | openssl s_client -connect $host:443 2>/dev/null \
    | openssl x509 -noout -dates 2>/dev/null | grep notAfter
done
```

| Check | Location | Expected Result |
|---|---|---|
| vCenter cert expiry | `openssl s_client` against vCenter | notAfter > 1 year from today |
| ESXi host thumbprint warnings | vCenter → Hosts → each host | No thumbprint warning banner |
| NSX Manager cert | `openssl s_client` against NSX | notAfter > 1 year from today |
| Aria Ops UI accessible | Browser to Aria Ops FQDN | No certificate warning |
| vCenter → Aria Ops trust | Aria Ops → Administration → vCenter connection | Connected, no auth errors |

---

## Common Mistakes

- **Replacing Aria product certs before vCenter VMCA.** Aria products immediately distrust the new
  root CA and lose connectivity to vCenter. Always rotate vCenter VMCA first.
- **Forgetting ESXi host certs after VMCA rotation.** Hosts continue presenting certs signed by
  the old VMCA root. vCenter shows thumbprint warnings and HA communication degrades over time.
- **Not updating the SuiteLC trust store before rotating.** If SuiteLC's trust store still
  contains the old CA root when new certs are deployed, SuiteLC validation fails and the rotation
  operation rolls back.
- **Manually replacing Aria certs outside SuiteLC.** Individual product cert replacement breaks the
  inter-product trust chain. Always use Aria SuiteLC for the Aria Suite.

---

## Related Scenarios

- NTP Drift and SSO Certificate Issues
- Provision a New Workload
- DR Test and Planned Failover
