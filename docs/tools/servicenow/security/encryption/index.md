# ServiceNow — Encryption

ServiceNow encryption covers transport security (TLS), field-level data encryption, credential storage, and integration channel security. The platform is SaaS — many controls are handled by Atlassian, but field-level and integration encryption are customer-configured.

---

## Transport Encryption

ServiceNow enforces TLS for all browser and API traffic on the cloud platform.

### Default Transport Security (SaaS)

| Layer | Protocol | Notes |
|---|---|---|
| Browser access | TLS 1.2 / TLS 1.3 | Enforced by ServiceNow |
| REST API | TLS 1.2 / TLS 1.3 | Enforced by ServiceNow |
| MID Server to instance | TLS 1.2+ | Configurable on MID Server |
| SMTP (outbound email) | STARTTLS / SMTPS | Configurable |
| LDAP to AD | LDAPS / StartTLS | Customer-configured |
| Outbound REST integrations | TLS (configurable per endpoint) | Customer-configured |

### TLS Verification Setting

```javascript
// Verify TLS certificate validation is enforced for outbound calls
// System Properties → glide.http.ssl_check_cert = true (default)

gs.getProperty('glide.http.ssl_check_cert')  // Should return 'true'

// For a specific REST message — verify SSL is enforced
// System Web Services → Outbound → REST Messages
// Open REST Message → HTTP Methods → SSL enforcement: Enforce SSL/TLS
```
┌──────────────────────────────────────── ServiceNow Encryption ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                       Encryption Layers                                       │   │
│   │                  Transit: TLS 1.2+ browser↔instance; TLS on all integrations                  │   │
│   │                  At rest: AES-256 DB encryption (ServiceNow managed or BYOK)                  │   │
│   │                Field-level: Edge Encryption proxy encrypts before cloud upload                │   │
│   │                  Attachments: encrypted in object storage; scanned on upload                  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    In-transit TLS → at-rest DB encryption → field-level Edge Encryption                               │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐                                                    │
│   │               Edge Encryption                │                                                    │
│   │              On-prem proxy node              │                                                    │
│   │            Encrypts before cloud             │                                                    │
│   │              Customer holds key              │                                                    │
│   │             AES-256 field cipher             │                                                    │
│   └──────────────────────────────────────────────┘                                                    │
│                                                     ┌─────────────────────────────────────────────┐   │
│                                                     │                Key Management               │   │
│                                                     │           ServiceNow KMS (default)          │   │
│                                                     │           BYOK via AWS KMS / Azure          │   │
│                                                     │            Key rotation schedule            │   │
│                                                     │           HSM integration optional          │   │
│                                                     └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ServiceNow SaaS datacentres · HSM appliances (BYOK) · TLS termination at load balancer               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Edge Encryption = on-prem proxy that encrypts field values before sending to ServiceNow              │
│  BYOK       = Bring Your Own Key; customer manages encryption keys in their KMS                       │
│  KMS        = Key Management Service; stores and rotates encryption keys                              │
│  HSM        = Hardware Security Module; tamper-proof key storage device                               │
│  AES-256    = Advanced Encryption Standard 256-bit; symmetric cipher for data at rest                 │
│  TLS 1.2+   = Transport Layer Security; encrypts data in transit                                      │
│  Field-level= per-field encryption; fields marked "encrypted" stored as ciphertext                    │
│  Attachment = files stored in object storage; encrypted independently of DB records                   │
│  BYOK proxy = Edge Encryption node hosted on-prem; only encrypted data leaves network                 │
│  Key rotation= periodic replacement of encryption keys; reduces exposure window                       │
│  Object store= S3-compatible storage for attachments; AES-256 server-side encryption                  │
│  Cipher suite= agreed TLS algorithms; ServiceNow enforces strong suites only                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
# Verify MID Server is using TLS 1.2+
openssl s_client -connect <instance>.service-now.com:443 \
  -tls1_2 -servername <instance>.service-now.com 2>&1 | grep "Protocol"

# Check MID Server certificate trust store
$JAVA_HOME/bin/keytool -list -keystore /opt/servicenow/mid/agent/security/keystore.jks \
  -storepass midserver
```

---

## Field-Level Encryption

ServiceNow supports field-level encryption for sensitive data stored in database fields. This is distinct from transport encryption — it protects data at rest in the database.

### Enabling Field Encryption

Requires: System Encryption Context feature activated on the instance.

```javascript
// Enable field encryption on a specific field
// Navigate to: Dictionary Entry for the field
// System Definition → Dictionary → find table/field
// Set: Encryption context = Default Encryption Context

// Example: encrypt the 'password' field on an integration table
// Table: u_integration_credentials
// Field: u_password
// In Dictionary: Encryption context → select encryption context
```

### Encryption Contexts

Navigate to: System Security → Encryption Contexts

| Context | Use Case | Key Type |
|---|---|---|
| Default | General sensitive fields | Instance-managed AES-256 |
| HR Sensitive | HR / PII fields | Separate key rotation |
| Financial | Financial data fields | Compliance-isolated key |

```javascript
// Script to list fields with encryption enabled
var dictRec = new GlideRecord('sys_dictionary');
dictRec.addQuery('encryption_type', 'ENCRYPT');
dictRec.query();
while (dictRec.next()) {
    gs.info('Table: ' + dictRec.name + ' | Field: ' + dictRec.element);
}
```

### Data Classification and Encryption Requirements

| Data Type | ServiceNow Table | Fields to Encrypt |
|---|---|---|
| Integration credentials | `discovery_credentials` | `password`, `ssh_passphrase` |
| Service account passwords | `u_service_accounts` | `u_password` |
| Certificate private keys | `sc_cert_credential_alias` | `private_key` |
| PII (names, emails) | `sys_user` | As required by data classification |
| API keys | Custom integration tables | Credential fields |

---

## Credential Storage

ServiceNow provides a Credential Store for integration credentials. Never store credentials in plain-text fields or workflow variables.

### Discovery Credentials

Navigate to: Discovery → Credentials

```javascript
// Retrieve a credential programmatically (Script Include)
var credMgr = new CredentialResolver();
var creds = credMgr.getCredentials('basic', 'target-host.corp.example.com');
// Returns: {user_name: '...', password: '...'}  — encrypted in transit within the instance
```

```bash
# List all discovery credentials via REST API
curl -u "admin:TOKEN" \
  -H "Accept: application/json" \
  "https://<instance>.service-now.com/api/now/table/discovery_credentials" \
  | jq '.result[] | {name: .name, type: .type, active: .active}'
```

**Credential controls:**

- Passwords are stored encrypted using the field encryption context.
- Credentials are accessed at runtime only — not exposed in exports or logs.
- Rotate credentials via the Credential Manager, not direct DB edits.
- Grant access to credential records using ACLs (role: `discovery_admin`).

### Connection Aliases (External Credential Storage)

For integration with CyberArk, HashiCorp Vault, or Azure Key Vault:

```javascript
// External credential resolver — CyberArk integration
// Plugin: com.snc.integration.credential_resolver.cyberark

// System Properties:
// credential_resolver.cyberark.url = https://cyberark.corp.example.com
// credential_resolver.cyberark.app_id = SNOW-Integration
// credential_resolver.cyberark.safe = SNOW-Credentials
// credential_resolver.cyberark.certificate = <path to cert>
```

---

## Outbound Integration Encryption

All outbound REST, SOAP, and JDBC connections must use TLS.

### REST Message Security Configuration

Navigate to: System Web Services → Outbound → REST Messages

```javascript
// Enforce per REST message via script
var sm = new sn_ws.RESTMessageV2('MyIntegration', 'get_data');
sm.setEndpoint('https://api.corp.example.com/data');
sm.setHttpMethod('GET');

// These are set in the UI on the REST Message record:
// Authentication Type: Basic | OAuth 2.0 | Mutual Authentication
// Mutual Authentication: Select certificate alias
// Enforce SSL: true

var response = sm.execute();
gs.info('Status: ' + response.getStatusCode());
```

### Certificate Management for mTLS

```bash
# Import a CA certificate into ServiceNow trust store
# Navigate to: System Definition → Certificates → New
# Type: CA certificate
# PEM certificate: paste CA certificate PEM

# Import a client certificate for mTLS
# Navigate to: System Definition → Certificates → New
# Type: Client certificate
# PEM certificate: paste client cert
# PEM private key: paste private key (stored encrypted)
```

---

## Email Encryption

### Outbound SMTP with TLS

Navigate to: System Mailboxes → Outbound → SMTP Accounts

| Setting | Value |
|---|---|
| Port | 587 (STARTTLS) or 465 (SMTPS) |
| Use TLS | Yes |
| Authentication | Yes |
| Username | `svc-snow-smtp@corp.example.com` |
| Password | Stored in credential store |

```javascript
// Test SMTP configuration
var mailer = new GlideEmailOutbound();
mailer.setSubject('Test email from ServiceNow');
mailer.setBody('TLS connectivity test');
mailer.addAddress('to', 'admin@corp.example.com', 'Admin');
mailer.send();
```

---

## Backup and Export Encryption

### Export Encryption

ServiceNow data exports (CSV, XML, Excel) are unencrypted by default. Control who can export:

```javascript
// ACL preventing export of sensitive tables
// Name: read_sc_request.export
// Operation: export (custom operation)
// Condition:
gs.hasRole('report_admin') || gs.hasRole('admin')
```

### Scheduled Export Security

Navigate to: System Import Sets → Scheduled Exports

- All scheduled exports should target encrypted destinations (SFTP over TLS, S3 with SSE).
- Restrict scheduled export creation to report_admin role.
- Log all export operations to the audit table.

---

## Encryption Checklist

| Control | Type | Status |
|---|---|---|
| TLS 1.2+ enforced on all endpoints | Transport | SaaS — managed by ServiceNow |
| MID Server uses TLS 1.2+ | Transport | Verify in config.xml |
| SSL certificate verification enabled | Transport | Check `glide.http.ssl_check_cert` |
| LDAP connection uses LDAPS | Transport | Configure in LDAP Server config |
| SMTP uses STARTTLS / SMTPS | Transport | Configure in SMTP account |
| Credential fields use field encryption | At-rest | Configure in Dictionary |
| Integration passwords stored in Credential Store | At-rest | Audit credential records |
| mTLS for high-assurance integrations | Transport | Configure per REST Message |
| Client certs stored with encrypted private keys | At-rest | ServiceNow certificate manager |
| Export access restricted by ACL | Data leakage | Configure export ACL |
| CyberArk / Vault integration for secrets | At-rest | Install credential resolver plugin |

---

## Related Pages

- [ServiceNow — Authentication](../authentication/index.md)
- [ServiceNow — Access Control](../access-control/index.md)
- [ServiceNow — Hardening](../hardening/index.md)
