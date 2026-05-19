# Aria Automation — Install & Upgrade

```
┌─────────────────────────────────────────────────────────────┐
│         Aria Automation Upgrade Sequence (ASLM)             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Step 1: Upgrade LCM first (required)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Aria Suite Lifecycle Manager (LCM) upgraded         │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  Step 2: LCM takes VM snapshots automatically               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Snapshots: aria-auto-dc1-01/02/03 pre-upgrade       │   │
│  └────────────────────────┬─────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  Step 3: LCM upgrades nodes sequentially (rolling)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │
│  │ Node-01  │  │ Node-02  │  │ Node-03  │                   │
│  │ upgrade  │  │ upgrade  │  │ upgrade  │                   │
│  │ restart  │  │ restart  │  │ restart  │                   │
│  └──────────┘  └──────────┘  └──────────┘                   │
│  Cluster partially available during upgrade                 │
│                           │                                 │
│                           ▼                                 │
│  Step 4: Post-upgrade validation                            │
│  vracli version  ·  kubectl get pods  ·  cloud accts green  │
│  Rollback: LCM revert to snapshots if validation fails      │
└─────────────────────────────────────────────────────────────┘
```

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

```
LCM → Lifecycle Operations → Environments → select or create environment → Add Product → Aria Automation
```

1. Select the Aria Automation version from the available bundles
2. Choose deployment size: Small (1 node) or Medium/Large (3 nodes)
3. Provide vCenter target: cluster, datastore, network, static IPs, FQDNs
4. Provide admin credentials (stored automatically in the LCM Locker)
5. LCM runs pre-checks (DNS, NTP, vCenter, disk space) — all must pass
6. LCM deploys the OVAs and configures the cluster
7. Monitor via: **Lifecycle Operations → Requests**

### Manual OVA Deployment (Standalone)

For environments without LCM:

1. Deploy the Aria Automation OVA via vSphere Client: **Actions → Deploy OVF Template**
2. Complete the OVA customisation: hostname, IP, gateway, DNS, NTP, root password
3. Power on and wait for first-boot (10–15 minutes)
4. Open VAMI: `https://<vra-fqdn>:5480`
5. Configure VIDM integration: VAMI → Identity Provider → Configure
6. For 3-node clusters: deploy all three OVAs, then join the second and third nodes to the first

---

## Upgrade Paths

### Via Aria Suite Lifecycle (Recommended)

Upgrades through LCM are orchestrated, validated with pre-checks, and include automatic rollback capability via snapshots.

1. Upgrade LCM itself to the version that supports the target Aria Automation version (LCM must always be upgraded first)
2. In LCM: **Lifecycle Operations → Environments → select environment → Aria Automation → Upgrade**
3. Select the target version from the bundle list
4. Resolve any pre-check failures before proceeding
5. LCM takes VM snapshots automatically before beginning the upgrade
6. Monitor upgrade progress: **Lifecycle Operations → Requests**

LCM upgrades nodes sequentially for 3-node clusters. The cluster remains partially available during the upgrade (2 of 3 nodes active), but requests should be paused during the upgrade window.

### In-Product Upgrade (Standalone, No LCM)

For environments not managed by LCM:

**Via VAMI:**

```
https://<vra-fqdn>:5480 → Lifecycle Management → System Upgrade → Upload PAK file
```

Upload the Aria Automation `.pak` file from Broadcom Support Portal. The VAMI validates the file and presents a pre-upgrade compatibility check. Click **Upgrade** if all checks pass.

**Via CLI:**

```bash
# Copy PAK file to the appliance
scp VMware-vRealize-Automation-*.pak root@vra-prod-01.example.local:/tmp/

# SSH to the appliance and trigger upgrade via vracli
ssh root@vra-prod-01.example.local
vracli software-update install --file /tmp/VMware-vRealize-Automation-*.pak
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
- [https://support.broadcom.com/lifecycle-management](https://support.broadcom.com/lifecycle-management)

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
- Review Broadcom Security Advisories monthly: [https://support.broadcom.com/security-advisory](https://support.broadcom.com/security-advisory)
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
