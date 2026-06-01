# Cisco DCNM — Security


<div class="kb-summary">
Cisco DCNM — Security reference.
</div>

```
┌──────────────────────────────────────── Cisco DCNM — Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      DCNM security: RBAC roles, AAA via RADIUS/TACACS+, TLS certs, and switch compliance      │   │
│   │       RBAC roles: network-admin (full), network-operator (read), network-stby (standby)       │   │
│   │            AAA: RADIUS or TACACS+ server; local user fallback if server unreachable           │   │
│   │        Compliance: compare running switch config against golden baseline; report drifts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    AAA auth → RBAC role assignment → feature access control → audit logging                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │         Certificates        │  │          Compliance         │   │
│   │       RBAC role assign      │  │        Self-signed CA       │  │        Baseline snap        │   │
│   │        RADIUS/TACACS+       │  │        CA-signed cert       │  │        Config compare       │   │
│   │        Local fallback       │  │         Cert renewal        │  │         Drift report        │   │
│   │         SSH key mgmt        │  │        HTTPS enforce        │  │         Policy alert        │   │
│   │          Audit log          │  │       Cipher restrict       │  │          Remediate          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    HTTPS only; disable HTTP; use CA-signed cert for browser trust and API clients                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │    Mechanism     │    Config path    │      Verify      │      Notes       │   │
│   │       Auth       │  RADIUS/TACACS+  │     Admin>AAA     │   Login works    │  Local fallback  │   │
│   │      AuthZ       │    RBAC role     │    Admin>Roles    │   Feature test   │    Per group     │   │
│   │       TLS        │  CA-signed cert  │    Admin>Certs    │   Browser lock   │   Annual renew   │   │
│   │    Compliance    │  Baseline diff   │   SAN>Complianc   │   Drift count    │   Alert email    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: RADIUS/TACACS+ server reachable via OOB management · cert private key secured            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC           = Role-Based Access Control; controls which DCNM features each user can access      │
│    network-admin  = Full read-write access to all DCNM functions and switch configuration             │
│    network-operator = Read-only access; cannot push zone changes or config templates                  │
│    RADIUS         = Remote Authentication Dial-In User Service; UDP-based AAA protocol                │
│    TACACS+        = Terminal Access Controller Access-Control System Plus; TCP-based AAA              │
│    Local fallback = DCNM uses local user DB if AAA server is unreachable; keep enabled                │
│    TLS cert       = HTTPS certificate for DCNM web UI; CA-signed prevents browser warnings            │
│    Compliance     = DCNM policy engine comparing switch running config to golden snapshot             │
│    Baseline snap  = Saved golden-state config used as compliance reference point                      │
│    Drift          = Any difference between running config and baseline; flagged in report             │
│    Audit log      = DCNM record of all user actions with timestamp, user, and change detail           │
│    SSH key mgmt   = DCNM stores switch SSH credentials; rotate on schedule, audit access              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell
┌──────────────────────────────────────── Cisco DCNM — Security ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      DCNM security: RBAC roles, AAA via RADIUS/TACACS+, TLS certs, and switch compliance      │   │
│   │       RBAC roles: network-admin (full), network-operator (read), network-stby (standby)       │   │
│   │            AAA: RADIUS or TACACS+ server; local user fallback if server unreachable           │   │
│   │        Compliance: compare running switch config against golden baseline; report drifts       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    AAA auth → RBAC role assignment → feature access control → audit logging                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │         Certificates        │  │          Compliance         │   │
│   │       RBAC role assign      │  │        Self-signed CA       │  │        Baseline snap        │   │
│   │        RADIUS/TACACS+       │  │        CA-signed cert       │  │        Config compare       │   │
│   │        Local fallback       │  │         Cert renewal        │  │         Drift report        │   │
│   │         SSH key mgmt        │  │        HTTPS enforce        │  │         Policy alert        │   │
│   │          Audit log          │  │       Cipher restrict       │  │          Remediate          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    HTTPS only; disable HTTP; use CA-signed cert for browser trust and API clients                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Control      │    Mechanism     │    Config path    │      Verify      │      Notes       │   │
│   │       Auth       │  RADIUS/TACACS+  │     Admin>AAA     │   Login works    │  Local fallback  │   │
│   │      AuthZ       │    RBAC role     │    Admin>Roles    │   Feature test   │    Per group     │   │
│   │       TLS        │  CA-signed cert  │    Admin>Certs    │   Browser lock   │   Annual renew   │   │
│   │    Compliance    │  Baseline diff   │   SAN>Complianc   │   Drift count    │   Alert email    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: RADIUS/TACACS+ server reachable via OOB management · cert private key secured            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RBAC           = Role-Based Access Control; controls which DCNM features each user can access      │
│    network-admin  = Full read-write access to all DCNM functions and switch configuration             │
│    network-operator = Read-only access; cannot push zone changes or config templates                  │
│    RADIUS         = Remote Authentication Dial-In User Service; UDP-based AAA protocol                │
│    TACACS+        = Terminal Access Controller Access-Control System Plus; TCP-based AAA              │
│    Local fallback = DCNM uses local user DB if AAA server is unreachable; keep enabled                │
│    TLS cert       = HTTPS certificate for DCNM web UI; CA-signed prevents browser warnings            │
│    Compliance     = DCNM policy engine comparing switch running config to golden snapshot             │
│    Baseline snap  = Saved golden-state config used as compliance reference point                      │
│    Drift          = Any difference between running config and baseline; flagged in report             │
│    Audit log      = DCNM record of all user actions with timestamp, user, and change detail           │
│    SSH key mgmt   = DCNM stores switch SSH credentials; rotate on schedule, audit access              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
