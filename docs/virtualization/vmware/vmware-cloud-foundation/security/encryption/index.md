# VCF — Encryption

## Certificate Management

All VCF component certificates are managed through SDDC Manager. Do not replace certificates directly through component UIs — SDDC Manager will lose track of the state.

```
SDDC Manager → Security → Certificate Management
```

**Replacement procedure:**

1. Generate CSR in SDDC Manager for the target component
2. Submit CSR to internal CA and receive signed certificate + CA chain
3. Import the signed cert and chain back into SDDC Manager
4. SDDC Manager installs the certificate and restarts affected services

**Check certificate expiry:**

```bash
openssl s_client -connect <vcenter-fqdn>:443 </dev/null 2>/dev/null \
  | openssl x509 -noout -subject -dates
```

**Lead times:**

| Timeline | Action |
|---|---|
| 60 days | Plan renewal — raise change ticket |
| 30 days | Schedule maintenance window |
| 7 days | Treat as P2 — renew immediately |

## vSAN Encryption

For workload domains handling sensitive data:

1. Deploy and configure a KMS (Key Management Server)
2. In vCenter: Cluster → Configure → vSAN → Services → Data-at-Rest Encryption → Enable
3. Define a key rotation schedule (annual minimum or per policy)
4. Ensure the KMS is highly available — KMS loss makes the vSAN datastore inaccessible

Key rotation: vCenter → vSAN → Key Management → Rotate Keys (live operation, no downtime required).
