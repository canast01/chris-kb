# Aria Automation — Encryption


<div class="kb-summary">
Encryption reference covering Secrets and Encrypted Properties, TLS Certificate Management, Data at Rest Encryption, Kubernetes Secret Management.
</div>

## Secrets and Encrypted Properties

Sensitive values (passwords, API tokens, SSH keys) must not be stored as plaintext in cloud templates. Use one of the following methods:

### Encrypted Property Groups

Encrypted Property Groups store sensitive key-value pairs at the Aria Automation level. Values are encrypted at rest and never appear in deployment event logs or API responses.

```text
Infrastructure → Configure → Property Groups → New Property Group → Encrypted
```
┌──────────────────────────────────── Aria Automation — Encryption ─────────────────────────────────────┐
│                                                                                                       │
│  vRA encrypts data in transit (TLS 1.2+) and at rest (vRA secrets store + vCenter D@RE).              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data in Transit                │  │                 Data at Rest                │   │
│   │       TLS 1.2+ all API and UI traffic        │  │     Secrets store: cloud acct creds enc     │   │
│   │         Internal microservices: mTLS         │  │    Postgres: encrypted volume (vSAN D@RE)   │   │
│   │        ABX to external: TLS required         │  │      vIDM: user data encrypted at rest      │   │
│   │     Cert: CA-signed, no self-signed prod     │  │      Backup archives: GPG or vault enc      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Credential security: cloud account passwords stored in vRA secrets, never plaintext.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Certificate Management            │  │                Secret Storage               │   │
│   │      LCM manages certs for all products      │  │       vRA secrets API stores creds enc      │   │
│   │      Cert rotation via LCM cert manager      │  │       HashiCorp Vault: external option      │   │
│   │        Minimum: RSA 2048 / ECDSA 256         │  │       No plaintext creds in templates       │   │
│   │       Alert: cert expiry <30d warning        │  │     ABX: use encrypted inputs, not vars     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA appliances · vSAN D@RE for storage · LCM cert store · vIDM · CA infrastructure                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  TLS 1.2+          = Transport Layer Security version 1.2 or higher; enforced on all endpoints        │
│  mTLS              = Mutual TLS; both client and server authenticate via cert in internal comms       │
│  Secrets store     = vRA built-in encrypted KV store for cloud account credentials                    │
│  D@RE              = Data at Rest Encryption; vSAN or datastore-level encryption for vRA VMs          │
│  HashiCorp Vault   = External secrets manager; vRA can pull creds from Vault via ABX                  │
│  LCM cert manager  = Aria Suite LCM module managing TLS cert lifecycle for all products               │
│  RSA 2048          = Minimum acceptable key size for vRA TLS certificates                             │
│  Cert rotation     = Replacing expiring cert via LCM; pushes new cert to all Aria products            │
│  Encrypted input   = vRA cloud template input marked as encrypted; value masked in UI and logs        │
│  Backup encryption = GPG or Vault-wrapped archive for offline backup of vRA DB and certs              │
│  CA-signed cert    = Certificate signed by internal or public CA; required in production              │
│  Cert expiry alert = LCM warns 30 days before cert expiry; schedule rotation in advance               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```yaml

Provide:
- Vault URL: `https://vault.example.local:8200`
- Authentication method: AppRole or Kubernetes JWT
- AppRole Role ID and Secret ID

Reference Vault secrets in cloud templates:

```yaml
resources:
  vm:
    type: Cloud.vSphere.Machine
    properties:
      cloudConfig: |
        #cloud-config
        runcmd:
          - DB_PASS=$(vault kv get -field=password secret/app/db) && configure-app.sh
```

### ABX Action Secrets

For ABX actions, store secrets as **Action Constants** (encrypted at rest):

```text
Extensibility → Actions → select action → Constants → Add
```

Constants are injected as environment variables at runtime:

```python
def handler(context, inputs):
    api_key = context.getSecret(inputs["apiKeyConstant"])
    # Never log or return secrets
```

---

## TLS Certificate Management

### Replacing the UI Certificate

**Via LCM (recommended for LCM-managed deployments):**

1. Import the new certificate into LCM Locker
2. **LCM → Lifecycle Operations → Aria Automation product → Replace Certificate**
3. LCM applies the certificate to all Aria Automation nodes

**Via vracli (standalone deployments):**

```bash
ssh root@vra-prod-01.example.local

# Import certificate files
vracli certificate import \
  --cert /tmp/vra-prod-01.pem \
  --key /tmp/vra-prod-01.key \
  --ca /tmp/chain.pem

# Verify the certificate is active
echo | openssl s_client -connect vra-prod-01.example.local:443 2>/dev/null | \
  openssl x509 -noout -subject -dates -issuer
```

### Certificate Requirements

| Requirement | Value |
|---|---|
| Algorithm | RSA 4096-bit (minimum RSA 2048-bit) |
| Signature | SHA-256 |
| SAN entries | All node FQDNs + load balancer VIP (if deployed behind an LB) |
| Maximum validity | 2 years; 1 year preferred |
| Private key | Unencrypted PEM (no passphrase) |
| Chain | Full chain — leaf + intermediate(s) + root in single PEM |

### Tracking Certificate Expiry

```bash
# Check expiry for all cluster nodes
for node in vra-prod-01 vra-prod-02 vra-prod-03; do
  echo -n "$node.example.local: "
  echo | openssl s_client -connect "$node.example.local:443" 2>/dev/null | \
    openssl x509 -noout -enddate 2>/dev/null
done
```

Set a calendar reminder or monitoring alert 60 days before expiry.

---

## Data at Rest Encryption

Aria Automation stores all state in its embedded PostgreSQL database. Native application-level encryption of the database is not included. Apply encryption at the storage layer:

- **vSAN Data-at-Rest Encryption**: enable on the datastore hosting Aria Automation VMs
- **SAN/NAS volume encryption**: enable at the array level for external storage
- **vSphere VM Encryption**: encrypt VM virtual disks via a vSphere encryption storage policy

```powershell
# PowerCLI — verify VM disk encryption
Get-VM | Where-Object { $_.Name -like "vra-*" } | Get-HardDisk |
  Select-Object @{N="VM";E={$_.Parent.Name}}, Name,
  @{N="Encrypted";E={$_.ExtensionData.Backing.KeyId -ne $null}}
```

---

## Kubernetes Secret Management

Aria Automation stores internal service credentials in Kubernetes secrets. These are base64-encoded by default — not encrypted at rest unless the Kubernetes data store (etcd) has encryption at rest enabled.

```bash
# List Kubernetes secrets in the prelude namespace (admin access only)
kubectl get secrets -n prelude

# Never expose Kubernetes secrets externally — they contain internal service credentials
```

The embedded Kubernetes cluster on Aria Automation appliances does not expose etcd encryption configuration to administrators. Protect the appliance disk using storage-layer encryption as the primary control.
