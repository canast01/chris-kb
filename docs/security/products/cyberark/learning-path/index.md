---
tags:
  - learning-path
  - security
---
# CyberArk PAM — Learning Path

<div class="kb-summary">
Recommended reading order for CyberArk Privileged Access Management. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: CyberArk PAM*
</div>

```d2
direction: right

S1: "Architecture" {shape: rectangle}
S2: "Deploy" {shape: rectangle}
S3: "Operations" {shape: rectangle}
S4: "Security" {shape: rectangle}
S5: "Troubleshoot" {shape: rectangle}

S1 -> S2
S2 -> S3
S3 -> S4
S4 -> S5
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Stage 1 — Architecture

**Goal**: Understand the CyberArk component model — Vault, CPM, PVWA, PSM, and AIM — and how they work together to secure, rotate, and mediate privileged access.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — CyberArk Digital Vault as the credential store, Central Policy Manager (CPM) for automated credential rotation, Privileged Web Access (PVWA) as the user-facing portal, Privileged Session Manager (PSM) for session isolation and recording, Application Identity Manager (AIM) for app credential injection without hardcoded passwords
- [Design Standards](../architecture/design-standards/) — Safe hierarchy design (by team, system class, environment), platform assignment for credential types, CPM rotation schedule design, PSM connection component selection, DR Vault placement and replication topology
- [Integrations](../architecture/integrations/) — Active Directory for user authentication and managed account discovery, LDAP, RADIUS, SAML/SSO, syslog to SIEM for audit events, Conjur for cloud-native app secrets, REST API for DevOps pipeline integration

**Why first**: CyberArk's safe and platform model determines every operational workflow — who can access what, how credentials are rotated, and where sessions are recorded. Misdesigning safes early causes painful restructuring later.

---

## Stage 2 — Deployment

**Goal**: Install and connect all CyberArk components, onboard initial accounts, and validate the rotation-access-record cycle end-to-end.

**Read**:

- [Deploy](../deploy/) — Vault server installation, PVWA web app deployment, CPM and PSM component installation, Vault-to-CPM-to-PSM connectivity validation, initial platform and safe configuration, DR Vault pairing
- [Install & Upgrade](../operations/install-upgrade/) — CyberArk version upgrade sequence (Vault first, then components), upgrade validation, DR Vault upgrade coordination

---

## Stage 3 — Operations

**Goal**: Onboard accounts, manage safe membership, monitor CPM rotation health, respond to session recording requests, and manage AIM credential retrieval.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check CPM rotation failures, accounts with rotation exceptions, PSM session queue, Vault replication lag to DR, PVWA service health
- [CLI Reference](../operations/cli-reference/) — CyberArk REST API: account onboard, password retrieve, safe member add/remove, session list; `PrivateArk Client` for Vault admin; `PACli` for scripted operations
- [Procedures](../operations/procedures/) — Onboard a new privileged account (Windows local admin, Linux root, network device), add a safe member, investigate a CPM rotation failure, retrieve a session recording, configure a dual-control approval workflow
- [Backup & Restore](../operations/backup-restore/) — Vault backup (metadata + encrypted credential store), DR Vault failover procedure, Vault restore from backup, CPM configuration recovery
- [Scripts](../operations/scripts/) — Bulk account onboarding via REST API, rotation failure alerting, safe membership audit reports, session recording expiry management

---

## Stage 4 — Security

**Goal**: Harden the Vault, enforce least-privilege safe access, and ensure session recordings are tamper-proof.

**Read**:

- [Access Control](../security/access-control/) — Safe permission model (List Accounts, Retrieve Password, Add Accounts, Manage Safe Members), owner vs user vs auditor role patterns, dual-control approval for sensitive accounts
- [Authentication](../security/authentication/) — PVWA authentication methods (AD, LDAP, RADIUS, SAML), PKI certificate authentication, MFA enforcement for privileged access, Vault admin account MFA
- [Encryption](../security/encryption/) — Vault server-side encryption (AES-256), server key and recovery key management, TLS for all component communications, session recording encryption at rest
- [Hardening](../security/hardening/) — Vault OS hardening (minimal services, dedicated server), firewall rules (only required ports to/from Vault), disable Vault debug mode in production, SIEM integration for Vault audit trail

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose CPM rotation failures, PSM connection errors, PVWA login issues, and AIM retrieval failures.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — CPM cannot rotate (account locked, password policy conflict, target unreachable), PSM connection failing (RDP/SSH proxy error), PVWA login loop after AD change, AIM app not retrieving credential (safe permission missing)
- [Diagnostics](../troubleshooting/diagnostics/) — CPM trace logs (`PM_Error.log`), PSM session logs, PVWA IIS application event logs, Vault audit log (`italog.log`), AIM CyberArk Provider service log
- [Escalation](../troubleshooting/escalation/) — CyberArk support case process, Vault diagnostic info export, component version matrix for support, DR Vault failover as last resort for Vault unavailability

**Why last**: Most CyberArk operational failures are permission or connectivity problems between components — diagnosed much faster once you understand the component trust model from the Architecture stage.
