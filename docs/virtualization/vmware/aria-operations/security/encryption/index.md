# Aria Operations — Encryption

```
┌─────────────────────────────────────────────────────────────┐
│            Aria Operations TLS Encryption Paths             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  UI / API access                                            │
│  ┌─────────────┐  TLS 1.2+  ┌──────────────────────────┐    │
│  │ Admin / API │◄──────────►│ Aria Ops Primary  :443   │    │
│  └─────────────┘            └──────────────────────────┘    │
│                                                             │
│  Collector → Primary node                                   │
│  ┌────────────────────┐  TLS  ┌──────────────────────────┐  │
│  │ Remote Collector   │◄─────►│ Primary node :4505/4506  │  │
│  └────────────────────┘       └──────────────────────────┘  │
│                                                             │
│  Cluster-internal (Cassandra / node replication)            │
│  ┌──────────┐  TLS  ┌──────────┐  TLS  ┌──────────┐         │
│  │ Node-01  │◄─────►│ Node-02  │◄─────►│ Node-03  │         │
│  └──────────┘       └──────────┘       └──────────┘         │
│  (auto-managed certs — no manual replacement needed)        │
│                                                             │
│  Adapter → vCenter / NSX                                    │
│  ┌─────────────┐  TLS  ┌──────────────────────────────┐     │
│  │ Adapter     │──────►│ vCenter :443 / NSX Mgr :443  │     │
│  │ credentials │       │ (CA-signed or accepted cert)  │    │
│  └─────────────┘       └──────────────────────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## TLS Certificate Replacement

Aria Operations ships with a self-signed certificate. Replace with a CA-signed certificate for production to avoid browser warnings, API trust failures, and integration issues with other Aria products.

**Via UI:**

```
Administration → Certificates → Replace Certificate
```

Upload:
- **Certificate (PEM)**: the signed leaf certificate
- **Private Key (PEM)**: must be unencrypted (no passphrase)
- **CA Chain (PEM)**: intermediate(s) and root CA concatenated in order (leaf → intermediate → root)

After upload, Aria Operations restarts the web services. Expect 2–5 minutes of UI unavailability.

**Via CLI (preferred for LCM-managed deployments):**

Use LCM Locker to manage certificates. For standalone deployments:

```bash
ssh admin@vrops-prod-01.corp.local

# Import certificate via vracli
vracli certificate import \
  --cert /tmp/vrops-prod-01.pem \
  --key /tmp/vrops-prod-01.key \
  --ca /tmp/chain.pem

# Verify the certificate was applied
openssl s_client -connect vrops-prod-01.corp.local:443 -servername vrops-prod-01.corp.local 2>/dev/null | \
  openssl x509 -noout -subject -dates
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
echo | openssl s_client -connect vrops-prod-01.corp.local:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check expiry of each cluster node's certificate
for node in vrops-prod-01 vrops-prod-02 vrops-prod-03; do
  echo -n "$node.corp.local: "
  echo | openssl s_client -connect "$node.corp.local:443" 2>/dev/null | \
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
