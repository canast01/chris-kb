---
tags:
  - netbackup
  - security
---
# NetBackup — Authentication

```bash
# List all certificates in the NetBackup CA
nbcertcmd -listCACertDetails

# Re-issue client certificate (if expired or lost)
nbcertcmd -getCertificate -server <master_server> -force

# Check certificate expiry across all clients
nbcertcmd -listCerts | grep -E "Host|Expiry"
```
```text
┌───────────────────────────────────── NetBackup — Authentication ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               NetBackup — Authentication Methods                              │   │
│   │               NBU CA host-ID certificates; AD/LDAP for web UI login; RBAC roles               │   │
│   │                   Management UI: HTTPS on 443 (Web UI) — browser-based login                  │   │
│   │               API: bearer token or service account; rotate credentials quarterly              │   │
│   │                 Inter-component: certificate-based mutual TLS between engines                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Human Access                 │  │                Machine Access               │   │
│   │            AD / LDAP integration             │  │               Service account               │   │
│   │              SAML SSO optional               │  │               API key / token               │   │
│   │                 MFA via IdP                  │  │               Certificate auth              │   │
│   │            Session timeout 15 min            │  │              Rotate every 90 d              │   │
│   │              Audit login events              │  │             Vault-stored secrets            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# On each NetBackup host — generate a CSR
nbcertcmd -createCSR -cn <hostname> -out /tmp/<hostname>.csr

# Submit CSR to your CA; retrieve the signed cert and CA chain
# Install the signed certificate
nbcertcmd -enrollCertificate \
  -server <master> \
  -cert /tmp/<hostname>.crt \
  -certChain /tmp/ca-chain.pem

# Verify external cert is in use
nbcertcmd -listCerts -CAType EXTERNAL
```

## Before you begin

- **Access:** Backup admin role on backup server; target system credentials
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Netbackup — Access Control](../access-control/)
- [Netbackup — Hardening](../hardening/)
- [Netbackup — Encryption](../encryption/)
