---
tags:
  - ansible
  - learning-path
---
# Ansible — Learning Path

<div class="kb-summary">
Recommended reading order for Ansible. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Ansible 2.x*
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
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Agentless model, inventory, playbook execution | 3–4 h |
| 2 — Deployment | AWX/AAP setup, project sync, inventory sources | 2–3 h |
| 3 — Operations | Job health, CLI, playbook lifecycle | ongoing |
| 4 — Security | Vault, RBAC, credential types, signing | 2–3 h |
| 5 — Troubleshooting | Verbosity, connectivity, idempotency debug | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Ansible's agentless push model — how the control node, inventory, playbooks, and SSH/WinRM transport work together before writing a single task.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — control node, managed nodes, SSH/WinRM transport, inventory evaluation order, variable precedence (22 levels), and the module execution model (copy → execute → fetch → cleanup)
- [Design Standards](../architecture/design-standards/) — inventory structure (static INI/YAML vs dynamic plugins), role directory layout (`tasks/`, `handlers/`, `defaults/`, `vars/`, `files/`, `templates/`), collection namespacing, and idempotency patterns
- [Integrations](../architecture/integrations/) — AWX/Ansible Automation Platform (AAP) as a GUI and API control plane, HashiCorp Vault for secrets injection via the Vault lookup plugin, and CI/CD pipeline triggering via AAP API or `ansible-playbook` in runners

**Key concepts before moving on**:

- Ansible is agentless — it connects over SSH (Linux) or WinRM/SSH (Windows) and runs modules on the target in a temporary Python environment
- Variable precedence is the most common source of bugs; `extra_vars` (highest) → playbook `vars` → inventory vars → role `defaults` (lowest)
- Idempotency means running a playbook twice produces the same end state — if a task changes on every run, it is broken
- Collections (`namespace.collection.module`) are the modern way to distribute and pin module versions

**Why first**: Ansible's apparent simplicity hides subtle ordering and scoping rules. Understanding the execution model prevents hard-to-debug variable precedence and connection failures before they appear in production.

---

## Stage 2 — Deployment

**Goal**: Stand up AWX or AAP and structure your automation project correctly from the start.

**Read**:

- [Deploy](../deploy/) — AWX installation via Kubernetes operator or AAP installer, project sync from Git, inventory source configuration (dynamic cloud inventory), and initial credential type setup
- [Install & Upgrade](../operations/install-upgrade/) — Ansible version pinning in `requirements.txt`, collection updates via `ansible-galaxy collection install -r requirements.yml`, and AWX/AAP upgrade sequence

**Deployment principles**:

- Store all playbooks and roles in version control (Git) — AWX projects sync from a repository, not from local files
- Pin collection versions in `requirements.yml` to prevent unexpected behaviour after upstream updates
- Use separate AWX organisations for dev and production automation to enforce access boundaries

---

## Stage 3 — Operations

**Goal**: Run, monitor, and maintain Ansible automation reliably across a managed fleet on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; AWX job template recent run status, failed hosts in the last 24 hours, unreachable inventory nodes, and Galaxy sync status
- [CLI Reference](../operations/cli-reference/) — `ansible`, `ansible-playbook`, `ansible-galaxy`, `ansible-vault`, `ansible-doc`, `ansible-inventory` command patterns for daily operations
- [Procedures](../operations/procedures/) — playbook promotion workflow (dev → test → prod), ad-hoc command approval process, inventory group restructuring, and scheduled job configuration in AWX
- [Backup & Restore](../operations/backup-restore/) — AWX PostgreSQL database backup procedure, project Git repository backup, and credential object export via AWX API
- [Scripts](../operations/scripts/) — dynamic inventory scripts for VMware and AWS, compliance check playbooks, scheduled maintenance playbooks, and AWX job launch wrappers

**Daily rhythm**: AWX dashboard for recent failures → unreachable hosts → scheduled job queue → project sync status.

---

## Stage 4 — Security

**Goal**: Protect secrets, restrict playbook execution scope, and audit all automation activity end to end.

**Read**:

- [Access Control](../security/access-control/) — AWX RBAC model (organisations, teams, role assignments), limiting playbook scope with `--limit` and `tags`, and preventing privilege escalation via `become` controls
- [Authentication](../security/authentication/) — AWX credential types (machine, source control, vault, cloud), SSH key management with key rotation, and LDAP/SAML SSO integration for AAP access
- [Encryption](../security/encryption/) — Ansible Vault for encrypting `vars_files` and individual variable values, AWX credential storage (AES-256 in the database), and TLS for AWX API and UI
- [Hardening](../security/hardening/) — disabling fact caching on shared controllers, audit log forwarding to a SIEM, job isolation with container-based execution environments (EE), and approval-gated workflows in AWX

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose playbook failures, connectivity problems, and idempotency regressions without re-running blindly against production.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — SSH authentication failures (key permission, host key mismatch), module not found on target (Python version mismatch), variable undefined, task not idempotent on re-run
- [Diagnostics](../troubleshooting/diagnostics/) — `-vvv` verbosity output, `ANSIBLE_DEBUG=1` environment variable, AWX job stdout in full, `ansible -m ping` connectivity test, and `ansible --list-hosts` for inventory inspection
- [Escalation](../troubleshooting/escalation/) — Red Hat support for AAP subscriptions, upstream GitHub issues for Ansible Core and collections, and community Ansible forum for unsubscribed environments

**Why last**: Troubleshooting makes most sense once you know how Ansible evaluates inventory, variables, and task order under normal execution — then deviations are obvious.

---

## See also

- [Ansible — Deploy](../deploy/)
- [Ansible — Procedures](../operations/procedures/)
- [Ansible — Common Issues](../troubleshooting/common-issues/)
