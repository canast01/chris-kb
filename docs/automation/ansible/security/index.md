# Ansible — Security



<div class="kb-summary">
Ansible — Security reference: Authentication, Access Control, Encryption, Hardening.
</div>

```
┌───────────────────────────────────────── Ansible — Security ──────────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Ansible security: protect credentials, restrict execution, audit changes, harden control node │   │
│   │   All secrets in Vault or AWX credential store — never plain text in playbooks or inventory   │   │
│   │      RBAC in AWX: assign job templates to teams; prevent cross-team access to credentials     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Authentication       │  │        Access Control       │  │          Hardening          │   │
│   │     SSH key per service     │  │       AWX teams + RBAC      │  │     Pin Ansible version     │   │
│   │      Vault for secrets      │  │      No shared accounts     │  │       Audit task logs       │   │
│   │     AWX credential store    │  │    Least privilege become   │  │      no_log on secrets      │   │
│   │    Rotate keys regularly    │  │    Approval gates in AWX    │  │       MFA on AWX login      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Ansible Vault = AES-256 encryption for variable files and strings; password stored separately │   │
│   │       AWX RBAC     = Role-Based Access Control; roles: admin, execute, read per template      │   │
│   │    no_log: true  = prevents task arguments and return values from appearing in AWX job logs   │   │
│   │   become sudo   = privilege escalation; apply narrowly; log all sudo usage on managed nodes   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="authentication/"><strong>Authentication</strong><span>SSO, LDAP, local accounts, and identity sources.</span></a>
<a class="kb-card" href="access-control/"><strong>Access Control</strong><span>Roles, permissions, and least privilege access.</span></a>
<a class="kb-card" href="encryption/"><strong>Encryption</strong><span>TLS certificate management and data encryption.</span></a>
<a class="kb-card" href="hardening/"><strong>Hardening</strong><span>Security baselines and compliance configuration.</span></a>
</div>
