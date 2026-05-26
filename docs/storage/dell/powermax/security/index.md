# PowerMax — Security

┌─────────────────────────────────────── Dell PowerMax Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      PowerMax security: DARE (drive-level encryption), masking views, LDAP/AD, audit log      │   │
│   │       DARE: self-encrypting drives; keys managed by external KMIP server or local vault       │   │
│   │  Host access: masking views (storage group + port group + initiator group) — no masking view  │   │
│   │     LDAP/AD integration for Unisphere GUI roles; local accounts for emergency break-glass     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    DARE encrypts drives at rest → masking view controls host access → LDAP controls admin auth        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Encryption         │  │        Access Control       │  │         Auth / Audit        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      DARE (SED drives)      │  │        Storage group        │  │       LDAP / AD roles       │   │
│   │       KMIP key server       │  │          Port group         │  │      Local break-glass      │   │
│   │         Key rotation        │  │       Initiator group       │  │       Audit log export      │   │
│   │         Crypto erase        │  │         Masking view        │  │        SYSLOG forward       │   │
│   │        TLS mgmt plane       │  │       No access = deny      │  │           SNMP v3           │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SED key rotation → masking view review → LDAP role audit → syslog review cycle                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Encryption    │   DARE + KMIP    │    All volumes    │ Key server down  │  Key audit log   │   │
│   │   Host access    │   Masking view   │  Deny by default  │   None allowed   │  Masking report  │   │
│   │    Admin auth    │    LDAP / AD     │     Role-based    │    Local only    │   Login events   │   │
│   │     Logging      │   Syslog/SNMP    │    Offsite SIEM   │        —         │   All changes    │   │
│                                                                                                       │
│    Physical: SEDs in drive bays; KMIP server on isolated security VLAN; mgmt on OOB network           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DARE           = Data At Rest Encryption; drive-level encryption using self-encrypting drives      │
│    SED            = Self-Encrypting Drive; encryption/decryption in drive controller hardware         │
│    KMIP           = Key Management Interoperability Protocol; standard for external key servers       │
│    Crypto erase   = Destroy SED encryption key making all data unrecoverable; used for decommission   │
│    Masking view   = Binding of storage group + port group + initiator group; controls host access     │
│    Storage group  = Logical collection of volumes presented to a host via masking view                │
│    Port group     = Collection of array FA director ports included in a masking view                  │
│    Initiator group= Collection of host HBA WWNs or iSCSI IQNs mapped in masking view                  │
│    Break-glass    = Local admin account for emergency access when LDAP is unavailable                 │
│    SIEM           = Security Information and Event Management; receives syslog from PowerMax          │
│    TLS mgmt plane = Unisphere REST API and GUI encrypted with TLS 1.2+ on management NIC              │
│    SNMP v3        = Encrypted/authenticated SNMP for monitoring integration                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌─────────────────────────────────────── Dell PowerMax Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      PowerMax security: DARE (drive-level encryption), masking views, LDAP/AD, audit log      │   │
│   │       DARE: self-encrypting drives; keys managed by external KMIP server or local vault       │   │
│   │  Host access: masking views (storage group + port group + initiator group) — no masking view  │   │
│   │     LDAP/AD integration for Unisphere GUI roles; local accounts for emergency break-glass     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    DARE encrypts drives at rest → masking view controls host access → LDAP controls admin auth        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Encryption         │  │        Access Control       │  │         Auth / Audit        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      DARE (SED drives)      │  │        Storage group        │  │       LDAP / AD roles       │   │
│   │       KMIP key server       │  │          Port group         │  │      Local break-glass      │   │
│   │         Key rotation        │  │       Initiator group       │  │       Audit log export      │   │
│   │         Crypto erase        │  │         Masking view        │  │        SYSLOG forward       │   │
│   │        TLS mgmt plane       │  │       No access = deny      │  │           SNMP v3           │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SED key rotation → masking view review → LDAP role audit → syslog review cycle                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │    Mechanism     │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Encryption    │   DARE + KMIP    │    All volumes    │ Key server down  │  Key audit log   │   │
│   │   Host access    │   Masking view   │  Deny by default  │   None allowed   │  Masking report  │   │
│   │    Admin auth    │    LDAP / AD     │     Role-based    │    Local only    │   Login events   │   │
│   │     Logging      │   Syslog/SNMP    │    Offsite SIEM   │        —         │   All changes    │   │
│                                                                                                       │
│    Physical: SEDs in drive bays; KMIP server on isolated security VLAN; mgmt on OOB network           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    DARE           = Data At Rest Encryption; drive-level encryption using self-encrypting drives      │
│    SED            = Self-Encrypting Drive; encryption/decryption in drive controller hardware         │
│    KMIP           = Key Management Interoperability Protocol; standard for external key servers       │
│    Crypto erase   = Destroy SED encryption key making all data unrecoverable; used for decommission   │
│    Masking view   = Binding of storage group + port group + initiator group; controls host access     │
│    Storage group  = Logical collection of volumes presented to a host via masking view                │
│    Port group     = Collection of array FA director ports included in a masking view                  │
│    Initiator group= Collection of host HBA WWNs or iSCSI IQNs mapped in masking view                  │
│    Break-glass    = Local admin account for emergency access when LDAP is unavailable                 │
│    SIEM           = Security Information and Event Management; receives syslog from PowerMax          │
│    TLS mgmt plane = Unisphere REST API and GUI encrypted with TLS 1.2+ on management NIC              │
│    SNMP v3        = Encrypted/authenticated SNMP for monitoring integration                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>Active Directory, LDAP integration, and audit logging.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles and permissions for Unisphere and Solutions Enabler.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Data at rest, data in flight, and key management.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security hardening checklist and compliance notes.</span>
</a>

</div>
