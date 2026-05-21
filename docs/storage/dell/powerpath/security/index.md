# PowerPath — Security


```
┌─────────────────────────────────────── Dell PowerPath Security ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     PowerPath security: access control for powermt CLI, license key protection, path audit    │   │
│   │       powermt requires root (Linux) or Administrator (Windows); no non-privileged access      │   │
│   │          License keys are host-bound; protect key file; track via Dell support portal         │   │
│   │    Audit: log powermt commands via OS auditing (auditd/Windows Event Log); alert on changes   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Restrict CLI access → protect license file → enable OS audit logging → review path changes         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Access Control       │  │       License Security      │  │       Audit / Logging       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      Root-only powermt      │  │        Host-bound key       │  │         auditd rules        │   │
│   │         Sudo policy         │  │       Portal tracking       │  │          Event log          │   │
│   │       No non-priv exec      │  │        Key file perms       │  │         SIEM forward        │   │
│   │       PAM integration       │  │        License expiry       │  │        Policy changes       │   │
│   │        MFA for admin        │  │        Renewal alerts       │  │       Path add/remove       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Privilege control → audit logging → license monitoring → periodic path count reconciliation        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Control      │  Implementation  │      Standard     │    Exception     │      Audit       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    CLI access    │   Root / sudo    │   Named accounts  │  No shared root  │     Sudo log     │   │
│   │     License      │  Host-bound key  │  Stored securely  │    No sharing    │   Portal audit   │   │
│   │    Path audit    │   OS audit log   │    SIEM ingest    │        —         │  Weekly review   │   │
│   │  Policy change   │  Change control  │    CR required    │  Emergency proc  │ Post-change log  │   │
│                                                                                                       │
│    Physical: powermt binary at /sbin (Linux); license file at /etc; restrict file permissions         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Host-bound key = PowerPath license cryptographically tied to host system ID; not transferable      │
│    auditd         = Linux kernel auditing daemon; log all execve calls matching powermt binary        │
│    Sudo policy    = /etc/sudoers rule granting named storage admin powermt exec without full root     │
│    Key file perms = /etc/powermt.custom should be root:root 600; world-readable is a risk             │
│    PAM integration= Pluggable Authentication Module; enforce MFA for storage admin login              │
│    SIEM           = Security Information and Event Management; receives powermt audit events          │
│    License expiry = PowerPath subscription license; expired license disables new registrations        │
│    Named accounts = No shared root; each admin has own account with sudo to powermt                   │
│    CR required    = Change Request; formal change control approval before policy modification         │
│    Portal audit   = Dell support portal shows all registered hosts and license key assignments        │
│    Path count recn= Periodic reconcile of expected vs. actual paths per host to detect removals       │
│    Emergency proc = Out-of-band change process for production incidents; still post-log required      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
