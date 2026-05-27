# Aria Operations — Encryption

## TLS Certificate Replacement

Aria Operations ships with a self-signed certificate. Replace with a CA-signed certificate for production to avoid browser warnings, API trust failures, and integration issues with other Aria products.

**Via UI:**

```text
Administration → Certificates → Replace Certificate
```
┌───────────────────────────────────── Aria Operations Encryption ──────────────────────────────────────┐
│                                                                                                       │
│  TLS, LDAPS, certificate management, and data encryption for Aria Operations (vROps).                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            In-Transit Encryption             │  │            Certificate Management           │   │
│   │             TLS 1.2+ UI and API              │  │            VAMI: Admin > SSL cert           │   │
│   │          TLS between cluster nodes           │  │         Upload CA-signed cert + key         │   │
│   │           LDAPS for directory auth           │  │          Monitor expiry proactively         │   │
│   │            HTTPS for all adapters            │  │         LCM can manage cert rotation        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  TLS protects all comms; D@RE protects stored data; certs managed via VAMI or LCM.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Data-at-Rest Encryption            │  │               Cipher Hardening              │   │
│   │          vSphere D@RE on datastore           │  │            Disable TLS 1.0 / 1.1            │   │
│   │           vSAN encryption optional           │  │             Enforce AES-256-GCM             │   │
│   │         KMS manages encryption keys          │  │          openssl: verify negotiated         │   │
│   │         No native app-level encrypt          │  │            Disable weak RC4/3DES            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere with D@RE; KMS server; CA for cert issuance; LCM for cert lifecycle mgmt                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+            = Minimum transport encryption for all vROps communications                      │
│  LDAPS               = LDAP over TLS; required for secure directory authentication                    │
│  D@RE                = Data-at-Rest Encryption; vSphere storage-layer encryption                      │
│  KMS                 = Key Management Server; manages D@RE encryption keys                            │
│  CA-Signed Cert      = Certificate from trusted CA; replaces self-signed default                      │
│  VAMI SSL Page       = Location in VAMI to upload new TLS cert and private key                        │
│  LCM Cert Mgmt       = Aria Suite LCM rotates vROps cert across all nodes                             │
│  Cipher Suite        = Algorithm set for key exchange + encryption + MAC                              │
│  AES-256-GCM         = Preferred bulk cipher for TLS in vROps                                         │
│  Cert Expiry Monitor = Proactively track cert validity; alert at 60/30/14 days                        │
│  Inter-node TLS      = Encrypted comms between master, data, and replica nodes                        │
│  Self-Signed Default = vROps ships with self-signed cert; replace for production                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Cluster-Internal TLS

All inter-node communication within the Aria Operations cluster is encrypted using TLS. The cluster uses internally generated certificates for node-to-node communication — these are managed automatically and do not require manual replacement.

To verify cluster nodes are communicating over TLS:

```bash
# From primary node — check Cassandra inter-node encryption
grep -i "ssl\|tls\|encrypt" /storage/db/cassandra/cassandra.yaml | grep -v "#"
```

---

## Data at Rest Encryption

Aria Operations does not natively encrypt metric data at rest. Apply encryption at the storage layer:

- **vSAN**: enable vSAN Data-at-Rest Encryption on the datastore hosting Aria Operations VMs
- **External storage (SAN/NAS)**: enable volume-level encryption on the LUN or NFS export
- **VM-level encryption**: vSphere VM Encryption can encrypt the VM's virtual disks independently of the storage layer

Verify VM encryption status:

```powershell
# PowerCLI — check if Aria Operations VMs have encrypted disks
Get-VM "vrops-prod-01" | Get-HardDisk | Select-Object Name, StorageFormat,
  @{N="Encrypted";E={$_.ExtensionData.Backing.KeyId -ne $null}}
```

---

## Credential Encryption in Adapters

Adapter credentials (vCenter, NSX, storage) are stored encrypted in the Aria Operations Postgres database. The encryption key is derived from the node's unique identifier.

- Do not move adapter credentials between cluster deployments by copying the database directly
- After a restore, re-enter all adapter credentials via the UI — they cannot be decrypted on a different cluster instance

---

## Certificate Expiry Monitoring

Check certificate expiry from the command line or via API:

```bash
# Check expiry of the current UI certificate
echo | openssl s_client -connect vrops-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check expiry of each cluster node's certificate
for node in vrops-prod-01 vrops-prod-02 vrops-prod-03; do
  echo -n "$node.example.local: "
  echo | openssl s_client -connect "$node.example.local:443" 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null
done
```

Set a monitoring alert in Aria Operations itself for the synthetic metric `ssl_certificate_days_until_expiry` on the self-monitoring adapter.

---

## FIPS Mode

Aria Operations 8.x supports FIPS 140-2 compliant cryptography. Enable FIPS only at deployment time — it cannot be enabled on an existing cluster without redeployment.

If FIPS is required:
- Deploy a new cluster with FIPS mode selected in the OVA deployment wizard
- All management pack integrations must also support FIPS — verify compatibility before enabling
- Note: FIPS mode disables some cipher suites and hash algorithms — test all adapter connections after deployment
