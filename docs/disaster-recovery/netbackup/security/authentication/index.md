# NetBackup — Authentication

## NetBackup Certificate Authority

All clients authenticate to the master server via certificates issued by the NetBackup CA:

```bash
# List all certificates in the NetBackup CA
nbcertcmd -listCACertDetails

# Re-issue client certificate (if expired or lost)
nbcertcmd -getCertificate -server <master_server> -force

# Check certificate expiry across all clients
nbcertcmd -listCerts | grep -E "Host|Expiry"
```
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

### Map AD Groups to NetBackup Roles

In the NetBackup Web UI: **Security** → **Access Control** → **Smart Groups** — map AD security groups to built-in NetBackup roles (Administrator, Security Administrator, Default User, etc.).

| NetBackup Role | Typical AD Group | Permissions |
|---|---|---|
| NetBackup Administrator | `grp-netbackup-admins` | Full access; manage policies, storage, catalog |
| Security Administrator | `grp-netbackup-security` | CA, certificates, RBAC config only |
| Default User | `grp-netbackup-operators` | View jobs, submit restores for owned assets |
| Backup Operator | `grp-netbackup-operators` | Run manual backups, monitor jobs |

---

## API Token Authentication

The NetBackup REST API uses JWT-based API tokens (not the same as CA certificates).

### Create an API Token

```bash
# Create a token via REST API (authenticate first with username/password)
curl -s -X POST "https://<master>:1556/netbackup/login" \
  -H "Content-Type: application/vnd.netbackup+json;version=9.0" \
  -d '{"userName":"admin","password":"<pass>","domainType":"vx","domainName":"<master>"}' \
  | jq -r '.token'

# Create a named API token with expiry (via Web UI: Security → API Tokens → Add)
# Or via API:
curl -s -X POST "https://<master>:1556/netbackup/security/api-tokens" \
  -H "Authorization: Bearer <login_token>" \
  -H "Content-Type: application/vnd.netbackup+json;version=9.0" \
  -d '{"tokenName":"ci-pipeline","expiryInHours":720}'
```

### List and Revoke API Tokens

```bash
# List all API tokens (admin only)
curl -s -X GET "https://<master>:1556/netbackup/security/api-tokens" \
  -H "Authorization: Bearer <token>"

# Revoke a specific token by name
curl -s -X DELETE "https://<master>:1556/netbackup/security/api-tokens/ci-pipeline" \
  -H "Authorization: Bearer <token>"
```

### Token Expiry and Best Practices

| Setting | Recommendation | Notes |
|---|---|---|
| Default session token | 24 hours | Login tokens for interactive use |
| Named API tokens | 30–90 days max | Used for automation/CI; rotate on schedule |
| Service account tokens | 90 days | Store in secrets manager; revoke on rotation |

---

## NetBackup Web UI Authentication

The Web UI (port 1556 HTTPS) issues JWT session tokens upon successful login.

| Parameter | Default | Tuning Location |
|---|---|---|
| Session timeout | 30 minutes idle | `nbsetconfig -add WEB_SERVER_SESSION_TIMEOUT_MINUTES <n>` |
| Concurrent sessions per user | Unlimited (default) | Controlled via RBAC role configuration |
| JWT signing key rotation | On upgrade | Invalidates all active sessions; plan maintenance windows accordingly |

Authentication flow: browser → NetBackup Web Server → Auth broker → LDAP/AD or local OS → JWT issued. For SSO, configure a SAML 2.0 identity provider in **Security** → **Identity Provider**.

---

## External CA Support

By default NetBackup uses its built-in CA. External CA is supported when your security policy mandates certificates from a corporate PKI.

### When to Use External CA

- Organization prohibits self-signed or non-corporate CAs
- Certificate lifecycle managed centrally (e.g., Microsoft ADCS, Vault PKI)
- Audit requirement for CA chain visibility

### Configure External CA

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

Once external CA is configured, the NetBackup built-in CA is not used for new enrollments. Existing built-in certificates must be revoked and replaced during the transition.

---

## Service Account Security

NetBackup daemons run under specific OS accounts with minimum required permissions.

| Daemon | Default Account | Minimum OS Permissions |
|---|---|---|
| `bprd` (request daemon) | `root` (UNIX) / `SYSTEM` (Windows) | Must bind to privileged ports; cannot be reduced below root/SYSTEM |
| `bpdbm` (database manager) | `root` (UNIX) / `SYSTEM` (Windows) | Full access to catalog directories; restrict filesystem ACLs externally |
| `nbwmc` (web management) | `nbwebsvc` (dedicated account) | Read access to NetBackup binaries; write to log directories only |
| `nbsl` (security service) | `nbwebsvc` | Read/write to `/usr/openv/netbackup/var/global/` |
| `bpjava-msvc` (Java GUI) | `root`/`SYSTEM` | Avoid — use Web UI instead; disable if not needed |

### Hardening Recommendations

- Restrict `nbwebsvc` home directory to `700` and owned by `nbwebsvc`
- Do not allow interactive login for `nbwebsvc` — set shell to `/sbin/nologin`
- Audit `/usr/openv/netbackup/db/` ACLs — only `root` and `bpdbm` should write
- Run `bpps -a` periodically to verify daemon process ownership has not drifted
---

## Related Reference

- [Standard LDAP Integration](../../../../security/ldap-integration/index.md) — field reference, service account standards, TLS requirements, and connectivity testing
- [Standard SAML Configuration](../../../../security/saml-configuration/index.md) — SP/IdP setup, Azure AD and Okta steps, attribute mapping, and security requirements
