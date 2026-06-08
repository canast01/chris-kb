# MDS — Security


<div class="kb-summary">
Cisco MDS hardening — AAA, SSH, port security, fabric binding, RBAC, and VSAN access control.
</div>

```text
┌────────────────────────────────────── Cisco MDS 9000 — Security ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        MDS security: fabric binding, port security, FC-SP-2 auth, RBAC, AAA, audit log        │   │
│   │      Fabric binding: restrict which switch WWNs may join fabric; prevents rogue switches      │   │
│   │              Port security: restrict which device WWNs may login to each FC port              │   │
│   │        FC-SP-2: DHCHAP mutual authentication between switches; prevents fabric spoofing       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    AAA login → RBAC role → feature group access → audit logging → compliance check                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Fabric Security       │  │        Access Control       │  │         Audit / Acct        │   │
│   │        Fabric binding       │  │          RBAC roles         │  │        Accounting log       │   │
│   │        Port security        │  │        RADIUS/TACACS+       │  │        AAA acct start       │   │
│   │        FC-SP-2 DHCHAP       │  │         SSH key auth        │  │        Syslog export        │   │
│   │        VSAN isolation       │  │        Local fallback       │  │          SNMP traps         │   │
│   │        Zoning enforce       │  │       Password policy       │  │         Audit review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Enable accounting for all exec and config sessions; export to centralised syslog                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │    Mechanism     │   NX-OS command   │      Verify      │      Notes       │   │
│   │   Fabric bind    │    Switch WWN    │   fabric-binding  │   show f-bind    │     Per VSAN     │   │
│   │    Port sec.     │    Device WWN    │   port-security   │  show port-sec   │   Activate DB    │   │
│   │     FC-SP-2      │  DHCHAP secret   │    fcsp enable    │    show fcsp     │  Both switches   │   │
│   │     AAA auth     │  RADIUS/TACACS+  │   aaa group sv.   │    Test login    │   Local backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: RADIUS/TACACS+ server on OOB management · SSH keys on jump host · syslog server          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Fabric binding  = Allowlist of switch WWNs permitted to join fabric via E_port; VSAN-scoped        │
│    Port security   = Allowlist of device pWWNs permitted to login on a specific FC port               │
│    FC-SP-2         = Fibre Channel Security Protocol v2; DHCHAP mutual auth between FC switches       │
│    DHCHAP          = DH-CHAP: Diffie-Hellman Challenge Handshake Auth Protocol; no password TX        │
│    VSAN isolation  = Traffic in one VSAN cannot cross into another; intrinsic security boundary       │
│    RBAC roles      = network-admin (full), network-operator (read), custom feature groups             │
│    AAA             = Authentication, Authorisation, Accounting; Cisco switches support both           │
│    Accounting log  = NX-OS audit log; records all exec commands and config changes with user          │
│    SSH key auth    = Public-key authentication for switch management; disable password auth           │
│    Syslog export   = Forward accounting and system logs to centralised syslog for SIEM                │
│    SNMP trap       = Fault notification; restrict SNMP community to read-only on OOB only             │
│    Password policy = Enforce min length, complexity, rotation on all local accounts                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="authentication/">
  <strong>Authentication</strong>
  <span>TACACS+/RADIUS, local accounts, and AAA configuration.</span>
</a>

<a class="kb-card" href="access-control/">
  <strong>Access Control</strong>
  <span>RBAC roles, privilege levels, and zone security.</span>
</a>

<a class="kb-card" href="encryption/">
  <strong>Encryption</strong>
  <span>SSH, TLS, and in-flight FC encryption configuration.</span>
</a>

<a class="kb-card" href="hardening/">
  <strong>Hardening</strong>
  <span>Security baseline, audit logging, and NIST/DISA alignment.</span>
</a>

</div>
