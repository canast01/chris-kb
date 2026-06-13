---
tags:
  - aria-automation
  - operations
  - vmware
---
# Aria Automation — Install & Upgrade


<div class="kb-summary">
Install & Upgrade reference covering Version Matrix, Initial Deployment (New Environment), Pre-Upgrade Checklist, Post-Upgrade Validation, EOL Tracking and 2 more sections.
</div>

## Version Matrix

| Product Name | Version | vSphere Compatibility | Notes |
|---|---|---|---|
| vRealize Automation | 8.10 | vSphere 7.0 U3+ | LTS release |
| vRealize Automation | 8.11 | vSphere 7.0 U3+, 8.0 | |
| Aria Automation | 8.12 | vSphere 7.0 U3+, 8.0 U1+ | Rebranded from vRA |
| Aria Automation | 8.13 | vSphere 7.0 U3+, 8.0 U2+ | |
| Aria Automation | 8.14+ | vSphere 8.0 U2+ | Current GA |
| Aria Automation (SaaS) | Always current | N/A — cloud-hosted | No patching required |

Always verify the VMware Product Interoperability Matrix before upgrading: [https://interopmatrix.vmware.com](https://interopmatrix.vmware.com)

---

## Initial Deployment (New Environment)

### Via vRealize Easy Installer (Recommended for Greenfield)

The Easy Installer ISO automates the end-to-end deployment of LCM + VIDM + Aria Automation in a single wizard:

1. Download the Easy Installer ISO from Broadcom Support Portal
2. Mount the ISO on a Windows or Linux installer machine
3. Launch the installer UI: `./install.exe` or `./install.sh`
4. The wizard collects all network parameters (IPs, FQDNs, DNS, NTP, vCenter targets) in a single workflow
5. Easy Installer deploys: Aria Suite Lifecycle → Workspace ONE Access → Aria Automation
6. After completion, log into LCM to manage the environment

### Via LCM (Adding Aria Automation to Existing LCM Environment)

If LCM is already deployed and Aria Automation needs to be added:

```text
┌──────────────────────────────── Aria Automation — Install and Upgrade ────────────────────────────────┐
│                                                                                                       │
│  Aria Automation is deployed and upgraded via Aria Suite LCM; manual OVA only for new installs.       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Pre-Install / Pre-Upgrade           │  │           Install / Upgrade Steps           │   │
│   │          DNS: fwd+rev for vRA FQDN           │  │        LCM: Environment → Add product       │   │
│   │          NTP: appliance time synced          │  │        Select version from LCM depot        │   │
│   │      vCenter: resource pool + datastore      │  │        LCM pre-checks must pass green       │   │
│   │        TLS cert: SAN matches vRA FQDN        │  │      Deploy OVA → power on → VAMI init      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Post-install: configure vIDM, cloud accounts, projects, and catalog before handover.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Post-Install Config              │  │              Upgrade Validation             │   │
│   │          VAMI: set FQDN, NTP, proxy          │  │        vracli status --all: all green       │   │
│   │         vIDM integration: SAML/LDAP          │  │      Catalog items visible post-upgrade     │   │
│   │       Cloud accounts: add vCenter/AWS        │  │        Test request: deploy small VM        │   │
│   │      Projects and quotas: set per team       │  │        Orchestrator: workflows intact       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vRA OVA (4 vCPU/25 GB RAM min) · vCenter · DNS/NTP · LCM appliance · TLS CA                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM depot         = Aria Suite LCM binary repository; download product OVAs for managed deploy       │
│  Environment       = LCM grouping of related Aria products sharing vIDM and certificates              │
│  OVA deployment    = vCenter deploy from OVA; used for initial install only (not upgrades)            │
│  VAMI init         = First-boot configuration wizard setting hostname, NTP, password                  │
│  Pre-checks        = LCM automated validation of DNS, NTP, cert, and resource before deploy           │
│  vIDM integration  = SAML trust configured in vRA VAMI; enables SSO for all Aria products             │
│  Cloud account add = vRA wizard adding vCenter/AWS/Azure credentials and verifying connectivity       │
│  Project quota     = Resource limits set per project after install; not set by default                │
│  Upgrade sequence  = LCM handles version ordering; do not upgrade vRA before vIDM                     │
│  Rollback point    = VM snapshot taken before LCM upgrade; revert if upgrade fails                    │
│  Greenfield install = New vRA in a new LCM environment; no migration from older vRA 7.x               │
│  SAN cert          = Subject Alternative Name; must include vRA FQDN for browser trust                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
---

## Pre-Upgrade Checklist

Run this checklist before initiating any upgrade:

- [ ] Current version and target version interoperability verified in the VMware Interop Matrix
- [ ] LCM version supports the target Aria Automation version (check LCM release notes)
- [ ] All Aria Automation services are healthy: `vracli status` — no failed pods or services
- [ ] All cloud accounts show a green status: **Infrastructure → Connections → Cloud Accounts**
- [ ] No deployments in **CREATING**, **UPDATING**, or **DELETING** state
- [ ] No approval requests stuck in **PENDING_APPROVAL** for more than the auto-reject window
- [ ] Backup completed successfully within last 24 hours (VAMI → Lifecycle Management → Backup)
- [ ] Backup passphrase documented and accessible
- [ ] VM snapshots taken for all Aria Automation appliance nodes
- [ ] Sufficient free disk space on appliance: `df -h /` — minimum 20 GB free recommended
- [ ] Maintenance window communicated to users (catalog will be unavailable during upgrade)
- [ ] Downstream integrations notified: ServiceNow, Ansible Tower, monitoring systems

```bash
# Pre-upgrade disk and service check on appliance
ssh root@vra-prod-01.example.local

# Disk space
df -h / /var

# Pod health — no CrashLoopBackOff or Pending pods
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"

# Service health
vracli status

# Confirm backup is current
vracli backup status
```

---

## Post-Upgrade Validation

Run immediately after the upgrade completes:

```bash
# Confirm installed version matches target
ssh root@vra-prod-01.example.local
vracli version

# Confirm all pods are Running
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"
# Expected: no output (all pods healthy)

# Confirm cluster node status (3-node deployments)
vracli cluster health
```

Via UI validation:

- [ ] Log into Aria Automation UI — authentication works (VIDM redirect succeeds)
- [ ] Version string in Administration → About matches the target version
- [ ] All cloud accounts show green status: **Infrastructure → Connections → Cloud Accounts**
- [ ] Re-enter credentials for each cloud account and validate: **Edit → Validate**
- [ ] Cloud zones and image/flavor mappings are intact
- [ ] Templates present in **Design → Cloud Templates**
- [ ] Existing deployment records visible in **Deployments → All Deployments**
- [ ] Test a simple deployment from a non-production catalog item (smoke test)
- [ ] ABX actions and event broker subscriptions are active
- [ ] Pipeline definitions are intact (if Automation Pipelines is in use)
- [ ] Remove VM snapshots within 48 hours of a confirmed successful upgrade

---

## EOL Tracking

VMware/Broadcom product lifecycle pages are the authoritative source for version EOS dates:
- [https://lifecycle.vmware.com](https://lifecycle.vmware.com)
- [https://support.broadcom.com/group/ecx/productlifecycle](https://support.broadcom.com/group/ecx/productlifecycle)

Key lifecycle phases:

| Phase | Definition | Action |
|---|---|---|
| General Support | Full patches, updates, and security fixes | Maintain within this phase |
| Technical Guidance | Security patches only; no new features | Plan upgrade before this phase |
| End of Life | No patches or support | Upgrade immediately |

Alert at 90 days before the End of General Support date for the installed version.

---

## Patch Cadence

On-premises deployments receive updates via LCM. SaaS deployments receive updates automatically from VMware.

For on-premises:
- Review Broadcom Security Advisories monthly: [https://support.broadcom.com/web/ecx/security-advisory](https://support.broadcom.com/web/ecx/security-advisory)
- Apply critical security patches within the change freeze exception window (do not wait for the next planned upgrade cycle for critical-severity patches)
- Apply non-critical patches during scheduled quarterly maintenance windows
- Test all patches in a non-production environment before applying to production

---

## Rollback Procedure

If an upgrade fails or post-upgrade validation reveals critical issues:

**Via LCM (recommended):**

If LCM managed the upgrade:
1. Navigate to **Lifecycle Operations → Requests → select the failed upgrade request**
2. Click **Rollback** — LCM reverts all Aria Automation VMs to the pre-upgrade snapshots
3. Monitor rollback progress in **Requests**
4. After rollback completes, verify the previous version is running: `vracli version`

**Manual snapshot revert:**

If LCM rollback is not available:
1. Power off all Aria Automation VMs (coordinate — all services will stop)
2. Revert each VM to the pre-upgrade snapshot from vCenter
3. Power on the VMs in order: node 1 → node 2 → node 3 (for 3-node clusters)
4. Wait 5 minutes for services to start
5. Verify services: `vracli status` and `kubectl get pods --all-namespaces`
6. Open a Broadcom SR if the rollback succeeds but the root cause of the upgrade failure needs investigation before retrying
