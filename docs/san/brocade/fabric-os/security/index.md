# FabricOS — Security


<div class="kb-summary">
FabricOS — Security reference.
</div>

```
┌───────────────────────────────────────── FabricOS — Security ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          FabricOS security: authentication, fabric access control, and audit logging          │   │
│   │     Auth: LDAP/RADIUS integration for admin/operator/user roles; SSH key auth recommended     │   │
│   │     Fabric security: FC-SP between ISL switches; DCC policy controls device login per port    │   │
│   │      Audit: secauditlog for all config changes; syslog to SIEM; Secure Fabric mode option     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Admin auth → switch CLI access control → fabric device auth → audit logging                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │            Audit            │   │
│   │         LDAP/RADIUS         │  │        FC-SP ISL auth       │  │         secauditlog         │   │
│   │         SSH key auth        │  │          DCC policy         │  │        Syslog export        │   │
│   │        Local accounts       │  │          SCC policy         │  │         Login events        │   │
│   │         Role: admin         │  │       Zone enforcement      │  │        Config changes       │   │
│   │        Role: operator       │  │        Secure Fabric        │  │         Port events         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    DCC + SCC policies prevent unauthorised device fabric login without explicit permit                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │     Standard     │    FOS command    │   Verification   │      Notes       │   │
│   │   Auth method    │   LDAP primary   │     aaaconfig     │ aaaconfig --show │ RADIUS fallback  │   │
│   │    DCC policy    │   Enabled prod   │   dccpolicyshow   │   dccpolicyadd   │ Per-port binding │   │
│   │    Audit log     │  Syslog + local  │    syslogdipadd   │ secauditlogshow  │  SIEM retention  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: out-of-band management via SSH from jump host; HTTPS for SANnav                          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FC-SP         = Fibre Channel Security Protocol; mutual auth between ISL-connected switches        │
│    DCC policy    = Device Connection Control; binds specific WWNs to specific ports                   │
│    SCC policy    = Switch Connection Control; restricts which switches can join via ISL               │
│    secauditlog   = FabricOS security audit log; records all security-relevant CLI events              │
│    aaaconfig     = FabricOS command for configuring LDAP/RADIUS authentication order                  │
│    RADIUS        = Alternative to LDAP; supports accounting for auth logging per session              │
│    SSH key auth  = Public key authentication for admin SSH; no password over the wire                 │
│    Secure Fabric = Optional FabricOS mode requiring DCC and SCC policies to be active                 │
│    Admin role    = Full switch access: zoning, port admin, firmware, user management                  │
│    Operator role = Limited to monitoring; no zone or config changes                                   │
│    Syslog        = FabricOS event log forwarded to SIEM; syslogdipadd sets destination IP             │
│    LDAP          = Centralised directory auth; maps LDAP groups to FabricOS admin/operator            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>LDAP, RADIUS, SSH key, and local account configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>FC-SP, DCC/SCC policies, roles, and zone enforcement.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>Management plane TLS and in-flight data protection.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baseline, audit logging, and SIEM integration.</span>
</a>

</div>

> Part of the [Brocade Fabric OS](../index.md) reference.
