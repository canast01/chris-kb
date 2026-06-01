# Venafi — Encryption


<div class="kb-summary">
HSM integration protects the CA private keys and Venafi service credentials. Keys for high-value services (CA certificates, wildcard certificates, code signing) must be stored in an HSM or managed within CyberArk with controlled retrieval.
</div>
```bash
┌──────────────────────────────── Security Venafi Security — Encryption ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Venafi encryption: data at rest and in transit encryption for all stored data         │   │
│   │          At rest: AES-256 encryption using controller-managed or external key manager         │   │
│   │          In transit: TLS 1.2+ for management; protocol encryption for data in flight          │   │
│   │         Key management: external KMIP-compatible KMS or built-in key lifecycle manager        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Enable encryption → configure KMS → verify → audit → rotate keys                                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │     Standard     │     Key source    │       KMS        │      Notes       │   │
│   │     At rest      │     AES-256      │     Controller    │  Internal/KMIP   │    Always on     │   │
│   │    In transit    │     TLS 1.2+     │      PKI cert     │   Internal CA    │   Mgmt + data    │   │
│   │   Key rotation   │      Annual      │     KMS policy    │   External KMS   │    Automated     │   │
│   │    Key escrow    │     Required     │     KMS vault     │   External KMS   │    DR access     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Security Venafi Security infrastructure · management network · monitoring                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Venafi             = Security Venafi Security platform overview and core concepts                  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Encryption Controls

| Control | Detail |
|---|---|
| HSM integration | Private key protection for CA trust anchors and Venafi credentials; PKCS#11 interface to on-premises HSM or cloud KMS (e.g., AWS CloudHSM, Thales Luna) |
| Certificate pinning | Policy enforcement for pinned certificate use cases; Venafi policy folders enforce Subject and SAN constraints to prevent mis-issuance |
| TLS enforcement | All Venafi Trust Protection Platform (TPP) web interfaces enforce TLS 1.2 minimum; TLS 1.0/1.1 disabled in IIS bindings and TPP `appsettings.json` |
| Key protection tiers | CA signing keys: HSM-resident only; issued end-entity private keys: encrypted at rest in SQL using AES-256 column encryption; never stored in clear text |
| Certificate lifecycle encryption | Private keys generated for managed certificates are transmitted only over mTLS to the requesting system or injected via encrypted payload in the provisioning workflow |
| Credential storage for service accounts | Venafi service account credentials (SDK API keys, IIS app pool identity) stored in CyberArk PAM; rotated on 90-day schedule via CPM |
| Database encryption | TPP SQL database configured with Transparent Data Encryption (TDE); backup files encrypted with a separate key managed outside the database server |

## HSM Configuration Reference

| Parameter | Value |
|---|---|
| Interface | PKCS#11 (Luna Network HSM) or CNG provider (Thales) |
| Key type for CA root | RSA-4096 or ECDSA P-384; generated and non-exportable |
| Key type for issuing CA | RSA-2048 minimum; P-256 preferred for new deployments |
| HSM slot assignment | Dedicated slot per environment (prod / non-prod); separate partition credentials |
| Failover | Active-passive HSM cluster with synchronised key material |
| Audit | HSM audit logs forwarded to SIEM alongside TPP event logs |

## Key Rotation and Lifecycle

| Item | Rotation Cadence | Responsibility |
|---|---|---|
| Venafi API keys (user / application) | 90 days | Venafi admin via Access Management UI |
| IIS application pool identity password | 90 days (CPM-managed) | CyberArk CPM + Venafi admin |
| TPP encryption key for SQL | Annual; or on suspected compromise | DBA + Venafi admin; requires TPP service restart |
| HSM partition PIN | On personnel change or annual | Security team |
| Issuing CA certificate | Per CA validity period (typically 5 years) | PKI team; requires re-enrollment of all issued certificates |
