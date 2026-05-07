# ONTAP Security
## RBAC

ONTAP has two RBAC scopes: **cluster-level** (managed by the `admin` account) and **SVM-level** (managed by `vsadmin` accounts within a specific SVM). Built-in roles:

| Role | Scope | Access Level |
|---|---|---|
| `admin` | Cluster | Full cluster administration — all commands |
| `readonly` | Cluster | Read-only cluster view — no configuration changes |
| `vsadmin` | SVM | Full SVM administration within one SVM |
| `vsadmin-readonly` | SVM | Read-only view of one SVM |
| `vsadmin-backup` | SVM | Snapshot and SnapMirror operations within one SVM |
| `vsadmin-snaplock` | SVM | SnapLock volume administration within one SVM |
| `vsadmin-protocol` | SVM | Protocol configuration (NFS, CIFS, iSCSI) within one SVM |

Create custom roles with minimum required permissions for automation service accounts:

```bash
# Create a custom read-only monitoring role
security login role create -role monitor-role -cmddirname "DEFAULT" -access none
security login role create -role monitor-role -cmddirname "version" -access readonly
security login role create -role monitor-role -cmddirname "volume show" -access readonly
security login role create -role monitor-role -cmddirname "snapmirror show" -access readonly

# Create a service account using the custom role
security login create -username svc-monitor -application ssh -authmethod publickey -role monitor-role
```

## Encryption

**NetApp Volume Encryption (NVE)**: Software-based, per-volume encryption using AES-256. Each volume has a unique data encryption key (DEK) stored in the key manager. Transparent to applications and protocols.

**NetApp Aggregate Encryption (NAE)**: Encrypts at the aggregate level; all volumes within the aggregate share an aggregate key. Required for deduplication cross-volume savings to persist with encryption.

```bash
# Enable NVE on an existing volume
volume modify -volume <vol> -encrypt true

# Check encryption status
volume show -fields encryption-state

# Verify key manager status
security key-manager show-key-query
security key-manager external show   # for KMIP
security key-manager onboard show    # for OKM
```

**Key Management**: 
- **Onboard Key Manager (OKM)**: Built-in ONTAP key manager; passphrase-protected; suitable for single-cluster environments
- **KMIP External Key Manager**: Integrate with external KMS (Thales CipherTrust, IBM SKLM, HashiCorp Vault via KMIP); required for multi-cluster or compliance mandates (FIPS, PCI-DSS)

```bash
# Configure external KMIP key manager
security key-manager external enable -vserver <admin-svm> -key-servers <kmip-server>:5696 -client-cert <cert-name> -server-ca-certs <ca-name>
```

## TLS and SSH Hardening

```bash
# Enforce TLS 1.2 minimum for HTTPS management
security config modify -interface HTTPS -min-protocol-version TLSv1.2

# Check current TLS/SSL configuration
security config show

# Restrict SSH ciphers and MACs
security ssh modify -vserver <cluster-name> -ciphers aes256-ctr,aes192-ctr,aes128-ctr -macs hmac-sha2-256,hmac-sha2-512

# Disable Telnet and RSH (should be off by default)
security protocol show
# Ensure telnet and rsh show enabled=false

# Rotate admin SSH host key
security ssh server key regenerate
```

## SNMPv3

```bash
# Configure SNMPv3 user with authentication and privacy
system snmp user create -username snmpv3user -authmethod md5 -authpassword <auth-pass> -privmethod aes128 -privpassword <priv-pass>

# Add SNMPv3 trap host
system snmp traphost add -ipaddr <monitoring-host> -username snmpv3user
```

Disable SNMPv1/v2c if enabled:
```bash
system snmp community delete -community-name public
system snmp community delete -community-name <any-other-v1v2-community>
```

## Audit Logging

**Admin action auditing**: All CLI, API, and System Manager operations by authenticated users are captured in the ONTAP audit log:

```bash
# View recent administrative audit events
security audit log show
security audit log show -user admin -time-range 24h
```

**File access auditing via ONTAP Audit Framework**: Captures NFS and SMB file access events to an EVTX audit log on a designated NAS volume:

```bash
# Configure SVM-level file access auditing
vserver audit create -vserver <svm> -destination /audit_logs -events file-ops,cifs-logon-logoff
vserver audit enable -vserver <svm>
```

**FPolicy for file access control and monitoring**: FPolicy intercepts file operations and can send them to an external FPolicy server (DLP, ransomware detection, archiving):

```bash
# Show FPolicy configuration
fpolicy show
fpolicy policy show
fpolicy policy scope show
```

## Hardening Checklist

- [ ] Password authentication disabled for `admin`; public key only
- [ ] Built-in `diag` and `maintenance` accounts locked
- [ ] SSH idle session timeout configured: `security session timeout modify -timeout 600`
- [ ] TLS 1.2 minimum enforced for HTTPS
- [ ] SNMPv1/v2c communities deleted; SNMPv3 only
- [ ] AutoSupport using HTTPS (not HTTP/SMTP) for data transmission
- [ ] NVE or NAE enabled on all production volumes containing sensitive data
- [ ] External KMIP key manager configured (OKM acceptable for non-regulated environments)
- [ ] Admin audit logging enabled and log forwarding to SIEM configured
- [ ] FPolicy configured for production NAS SVMs if file access auditing is required by compliance
- [ ] RBAC service accounts with minimum required permissions for all automation and monitoring tools
