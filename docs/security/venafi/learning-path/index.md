---
tags:
  - learning-path
  - security
---
# Venafi — Learning Path

<div class="kb-summary">
Recommended reading order for Venafi machine identity management. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Venafi TLS Protect*
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

**Goal**: Understand how Venafi TLS Protect discovers, classifies, and enforces certificate policy across the enterprise, and how it integrates with CAs and downstream consumers.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — Venafi Trust Protection Platform (TPP) or TLS Protect Cloud architecture: certificate discovery engine, policy tree structure, CA connector model, certificate lifecycle automation (request, approve, issue, install, renew, revoke)
- [Design Standards](../architecture/design-standards/) — Policy tree design (by environment, team, certificate type), CA connector assignment per policy folder, certificate validity and key algorithm enforcement, discovery scope design for network scanners and Kubernetes clusters
- [Integrations](../architecture/integrations/) — CA integrations (Microsoft ADCS, DigiCert, Entrust, Let's Encrypt via ACME), HashiCorp Vault PKI connector, Kubernetes cert-manager integration, Terraform provider, ITSM ticketing for approval workflows, syslog for audit events

**Why first**: Venafi's policy tree determines which CA issues which certificate type and who can approve requests — understanding this model before deployment prevents certificate issuance policy gaps.

---

## Stage 2 — Deployment

**Goal**: Install Venafi TPP, configure CA connectors, build the policy tree, and run initial certificate discovery.

**Read**:

- [Deploy](../deploy/) — TPP server installation, SQL database configuration, CA connector setup, policy tree creation, network discovery configuration, Aperture management console setup
- [Install & Upgrade](../operations/install-upgrade/) — TPP version upgrade procedure, database backup before upgrade, CA connector re-validation after upgrade, Venafi Agent update to endpoints

---

## Stage 3 — Operations

**Goal**: Run discovery, manage certificate requests and renewals, enforce policy violations, and report on machine identity inventory.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check certificates expiring within 30/60/90 days, review policy violations, validate CA connector health, check discovery job completion
- [CLI Reference](../operations/cli-reference/) — Venafi REST API (WebSDK): certificate request, renew, revoke, policy read/write; `vcert` CLI tool for certificate operations from the command line
- [Procedures](../operations/procedures/) — Request a new certificate through Venafi policy, approve a certificate request in the workflow, renew an expiring certificate, revoke a compromised certificate, configure auto-renewal for a certificate
- [Backup & Restore](../operations/backup-restore/) — TPP database backup, policy tree export, CA connector configuration backup, restore after TPP server failure
- [Scripts](../operations/scripts/) — Automated renewal trigger scripts via REST API, expiry report generation, policy violation remediation scripts, Kubernetes cert-manager secret sync

---

## Stage 4 — Security

**Goal**: Enforce certificate policy, protect Venafi's own credentials, and ensure only authorised users can request or approve certificates.

**Read**:

- [Access Control](../security/access-control/) — Venafi RBAC: Master Admin vs Policy Owner vs Certificate Owner vs Read-Only; policy folder permission inheritance; approval workflow roles
- [Authentication](../security/authentication/) — AD/LDAP integration for TPP login, service account management for CA connector credentials, API key management for automation access
- [Encryption](../security/encryption/) — HTTPS enforcement for TPP portal and REST API, encrypted CA connector credentials in TPP database, TLS for CA communication
- [Hardening](../security/hardening/) — Restrict TPP server network access to management and CA subnets, audit log export to SIEM, enforce policy violation alerts to security team, rate-limit API key usage

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose failed certificate requests, CA connector errors, missed renewals, and discovery gaps.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Certificate request stuck in pending approval, CA connector returning error (credential expired, CA unreachable), auto-renewal not triggering, discovery not finding certificates on known hosts
- [Diagnostics](../troubleshooting/diagnostics/) — TPP application logs (`C:\Program Files\Venafi\logs`), CA connector test from Aperture, `vcert` CLI request test, network connectivity check from TPP to CA server
- [Escalation](../troubleshooting/escalation/) — Venafi support case process, log bundle export from TPP, CA vendor support for connector-side failures

**Why last**: Venafi troubleshooting maps errors back to policy tree configuration and CA connector state — context established in the Architecture and Operations stages.
