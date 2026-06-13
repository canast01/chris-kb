# Dell PowerPath — Learning Path

<div class="kb-summary">
Recommended reading order for Dell PowerPath. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```

## Stage 1 — Architecture
**Goal**: Understand how PowerPath intercepts host I/O at the multipath driver level, how it selects paths using load-balancing policies, and how PowerPath/VE handles the VMware case.

**Read in this order**:
- [How It Works](../architecture/how-it-works/) — PowerPath driver placement in the host I/O stack (between application and OS disk layer), path discovery and registration, load-balancing policy engine (Adaptive, CLARiiON, Round Robin, Least Blocks), path failover mechanism (dead path detection and traffic rerouting), and PowerPath/VE (Virtual Edition) architecture for VMware ESXi.
- [Design Standards](../architecture/design-standards/) — Minimum path count requirements (4 paths per LUN recommended), load-balancing policy selection by array type (PowerMax, PowerStore, Unity), PowerPath/VE deployment model (vSphere plugin), registration and licensing per host, and co-existence with native MPIO.
- [Integrations](../architecture/integrations/) — Integration with PowerMax, PowerStore, Unity, and VNX/CLARiiON arrays, VMware vSphere (PowerPath/VE), Windows MPIO co-existence rules, and PowerPath Management Server (PPME) for fleet-wide path management.

**Why first**: PowerPath is a host-level driver. Understanding its position in the I/O stack prevents conflicts with native MPIO and explains why path selection looks different from OS-level tools.

---

## Stage 2 — Deployment
**Goal**: Install and register PowerPath on Linux, Windows, and VMware hosts, validate path discovery, and confirm load balancing is active.

**Read**:
- [Install & Upgrade](../operations/install-upgrade/) — PowerPath installation (RPM, DEB, or MSI), registration key entry, path discovery validation (powermt display dev=all), PowerPath/VE vSphere plugin installation, version upgrade procedure, and uninstall/replacement with native MPIO.

**Why second**: Registration must be completed before PowerPath enters production; unregistered PowerPath operates in limited mode with reduced path count and no load balancing.

---

## Stage 3 — Operations
**Goal**: Monitor path health across the SAN fleet, diagnose dead paths, adjust load-balancing policies, and manage PowerPath through maintenance events.

**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers active path count per LUN (powermt display), dead or degraded paths, load-balancing policy in use, and PowerPath/VE health in vSphere.
- [CLI Reference](../operations/cli-reference/) — powermt commands: display, manage, restore, check, set policy; and PowerPath Management Server (PPME) commands for fleet-wide management.
- [Procedures](../operations/procedures/) — Changing load-balancing policy per device, removing dead paths, restoring paths after SAN maintenance, PowerPath/VE migration during vSphere upgrades, and replacing a failed HBA without disrupting I/O.
- [Backup & Restore](../operations/backup-restore/) — PowerPath configuration export (powermt save), restoration after OS rebuild, and ensuring path configuration survives host reboots via powermt restore.
- [Scripts](../operations/scripts/) — Automation: fleet-wide dead path detection via PPME API, load-balancing policy audit across hosts, and path count compliance reporting.

**Why third**: Dead paths silently reduce redundancy. Without daily path health checks, a host can reach a single-path state before the next HBA failure causes an outage.

---

## Stage 4 — Security
**Goal**: Restrict PowerPath management access and secure PowerPath Management Server.

**Read**:
- [Access Control](../security/access-control/) — PowerPath Management Server (PPME) user roles, host-level access restriction for powermt commands (root/admin only), and change control gate for load-balancing policy changes.
- [Authentication](../security/authentication/) — PPME user authentication, LDAP integration for PPME console access, and registration key management for licensed hosts.
- [Encryption](../security/encryption/) — PPME management traffic encryption (HTTPS), PowerPath registration communication security, and interaction with array-side D@RE (PowerPath is transparent to at-rest encryption).
- [Hardening](../security/hardening/) — Restrict powermt CLI to root/administrator, PPME management network isolation, audit logging of path policy changes, and change management gate for production host modifications.

**Why fourth**: PowerPath load-balancing policy changes affect host I/O performance immediately. Access controls prevent unauthorised policy modifications.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose dead paths, path count drops below minimum, load-balancing policy not applying, and PowerPath/VE issues in vSphere.

**Read**:
- [Common Issues](../troubleshooting/common-issues/) — Dead paths not recovering after SAN fix (powermt restore needed), load-balancing policy reverting to default after host reboot, PowerPath/VE not discovering new LUNs after storage provisioning, and registration key failure after OS rebuild.
- [Diagnostics](../troubleshooting/diagnostics/) — powermt display dev=all output analysis, PPME path health dashboard, HBA driver event log review, vSphere Storage Views for PowerPath/VE, and Dell SupportAssist bundle collection.
- [Escalation](../troubleshooting/escalation/) — When to open a Dell support case for PowerPath driver issues, required diagnostic outputs (powermt display, HBA driver logs), and escalation path for array-side path table issues.

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
