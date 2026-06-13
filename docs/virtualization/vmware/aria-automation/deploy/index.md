---
tags:
  - aria-automation
  - deployment
  - vmware
---
# Aria Automation — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Aria Automation (on-premises). Covers prerequisites, LCM-based deployment, cloud account configuration, project and blueprint setup, and end-to-end validation.

*Applies to: Aria Automation 8.x*
</div>

```text
┌───────────────────────────────── Aria Automation — Deployment Phases ─────────────────────────────────┐
│                                                                                                       │
│  Six phases from prerequisites to a fully validated Aria Automation environment. Each phase has a     │
│  clear exit criterion. Do not proceed until the current phase validates clean.                        │
│                                                                                                       │
│   ┌───────────────────────────┐  ┌────────────────────────────┐  ┌────────────────────────────────┐   │
│   │   Phase 1: Pre-Deploy     │  │   Phase 2: LCM Deployment  │  │  Phase 3: Cloud Accounts       │   │
│   │  DNS: FQDNs for all svcs  │  │  Easy Installer or LCM UI  │  │  Add vCenter cloud account     │   │
│   │  TLS: SAN cert from CA    │  │  Select version from depot │  │  Accept thumbprint, sync data  │   │
│   │  vIDM: deployed + AD sync │  │  Map vCenter/datastore/net │  │  Verify hosts/VMs discovered   │   │
│   │  Datastore: ≥250 GB free  │  │  LCM pre-checks: all green │  │  Add AWS/Azure if multi-cloud  │   │
│   │  Ports: 443, 5480 open    │  │  Deploy takes 60–90 min    │  │  Cloud zones: define per clstr │   │
│   └───────────────────────────┘  └────────────────────────────┘  └────────────────────────────────┘   │
│                                                                                                       │
│                ▼                              ▼                                ▼                      │
│                                                                                                       │
│   ┌───────────────────────────┐  ┌────────────────────────────┐  ┌────────────────────────────────┐   │
│   │  Phase 4: Projects &      │  │  Phase 5: Blueprints &     │  │  Phase 6: Validation           │   │
│   │  Flavour/Image Mappings   │  │  Service Catalogue         │  │                                │   │
│   │  Create projects per team │  │  Blueprint YAML authoring  │  │  vracli status --all green     │   │
│   │  Assign cloud zones       │  │  Inputs and cloud config   │  │  Cloud accounts: sync OK       │   │
│   │  Flavour/image mappings   │  │  Publish to Service Broker │  │  Test deployment end-to-end    │   │
│   │  Network profiles + IPs   │  │  ABX actions (if needed)   │  │  Approval policy fires         │   │
│   │  Approval policies: RBAC  │  │  Approval + lease policies │  │  Lease policy applied          │   │
│   └───────────────────────────┘  └────────────────────────────┘  └────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure: Aria Automation VMs on vSphere · vPostgres DB (internal)                    │
│  NSX network segments · Workspace ONE Access (vIDM) · Aria Suite LCM · DNS/NTP/CA                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM        = Aria Suite Lifecycle Manager; orchestrates all Aria product deployments                 │
│  vIDM       = Workspace ONE Access; SSO provider for all Aria products                                │
│  Cloud Zone = Subset of a cloud account (cluster + datastore + network) available to a project        │
│  ABX action = Serverless Python/JS function triggered on deployment lifecycle events                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access:** vCenter Administrator role and SSH access to VCSA/ESXi hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Phase 1 — Pre-Deployment Prerequisites

**Exit criterion:** DNS resolves for all service FQDNs, CA-signed TLS cert is ready, vIDM is operational, and LCM pre-checks pass green.

Create forward A and PTR records for every Aria Automation service component. LCM pre-checks fail on missing DNS.

| FQDN | Service |
|---|---|
| `aac.example.local` | Aria Automation VIP (ports 443, 5480) |
| `aap.example.local` | Aria Automation Pipelines |
| `service-broker.example.local` | Service Broker catalogue |
| `orchestrator.example.local` | Aria Orchestrator (port 8281) |
| `vidm.example.local` | Workspace ONE Access |

```bash
# Verify from LCM appliance before starting
nslookup aac.example.local && nslookup service-broker.example.local
curl -sk https://vidm.example.local/SAAS/auth/heartbeat | grep -i alive
```

TLS: generate a SAN cert covering all FQDNs above; upload to LCM Certificate Management before deployment.

---

## Phase 2 — LCM Deployment

**Exit criterion:** All Aria Automation services show Running in LCM; `vracli status` returns no errors.

**Option A — Easy Installer (greenfield):** mounts an ISO and deploys LCM + vIDM + Aria Automation in a single wizard. Collects all network parameters (FQDNs, DNS, NTP, vCenter targets) in one workflow.

**Option B — Add to existing LCM:**

```text
LCM → Lifecycle Operations → Environments → Add Product → Aria Automation
→ Select version from depot → enter service FQDNs
→ Map vCenter, datastore, resource pool, port group
→ Upload TLS certificates → Run Pre-Checks (all green)
→ Submit deployment
```

```bash
# Monitor deployment from LCM appliance
ssh root@lcm.example.local
tail -f /var/log/vmware/lcm/lcm-debug.log | grep -E "DEPLOY|ERROR|WARN"
```

After the 60–90 minute deployment:

```bash
ssh root@aac.example.local
vracli status        # all services: Running
vracli status --all  # detailed pod health
vracli version       # confirm build matches target
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"
# Expected: no output
```

---

## Phase 3 — Cloud Account Configuration

**Exit criterion:** vCenter cloud account shows green status; hosts, VMs, and datastores are visible in Infrastructure → Resources.

```text
Infrastructure → Connections → Cloud Accounts → Add → vCenter
→ FQDN: vcenter.example.local
→ Credentials: svc-aria-automation@example.local
→ Accept thumbprint → Save
```

```bash
vracli cloud-account list          # STATUS: OK
vracli cloud-account sync --id <id>  # force re-sync if needed
```

Create Cloud Zones — define per-cluster subsets available to projects:

```text
Infrastructure → Configure → Cloud Zones → New Cloud Zone
→ Name: CZ-vSphere-Prod → Cloud Account: vcenter.example.local
→ Capability tags: env:prod
```

---

## Phase 4 — Projects, Mappings, and Governance

**Exit criterion:** At least one project with cloud zones, flavour and image mappings, and an approval policy are configured.

```text
Infrastructure → Configure → Projects → New Project
→ Members: add AD groups (roles: Administrator, Member, Viewer)
→ Cloud Zones: assign CZ-vSphere-Prod
```

Flavour and image mappings translate logical sizes and OS names to vCenter specs and VM templates:

```text
Flavor Mappings: small → 2 vCPU/4 GB  ·  medium → 4 vCPU/8 GB  ·  large → 8 vCPU/16 GB
Image Mappings: ubuntu-22 → Ubuntu-22-Template  ·  rhel-9 → RHEL-9-Template
```

Approval policy (gate large deployments):

```text
Service Broker → Policies → New Policy → Approval Policy
→ Criteria: flavor == large OR vmCount > 3
→ Approvers: AD group infra-approvers  ·  Mode: Any one approver
```

---

## Phase 5 — Blueprints and Service Catalogue

**Exit criterion:** A blueprint is published to Service Broker and a test catalogue request completes successfully.

Minimal YAML cloud template:

```yaml
formatVersion: 1
inputs:
  flavour: { type: string, enum: [small, medium, large], default: small }
  image: { type: string, enum: [ubuntu-22, rhel-9], default: ubuntu-22 }
resources:
  Cloud_vSphere_Machine_1:
    type: Cloud.vSphere.Machine
    properties:
      image: ${input.image}
      flavor: ${input.flavour}
      cloudConfig: |
        #cloud-config
        runcmd:
          - echo "Provisioned by Aria Automation" >> /etc/motd
```

```text
Design → Cloud Templates → Version → Create Version → Release: 1.0.0
Service Broker → Content Sources → New → Aria Automation → sync
Service Broker → Content → select item → Share → Project-AppTeam-Prod
```

---

## Phase 6 — End-to-End Validation

**Exit criterion:** All checks below pass. Backup configured. Hand off to operations.

```bash
ssh root@aac.example.local
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"
# Expected: no output (all pods healthy)
vracli status          # all services: Running
vracli cluster health  # 3-node deployments: all members healthy
```

Submit a smoke-test deployment from Service Broker and confirm it reaches `DEPLOYMENT_SUCCESSFUL`, then delete it.

| Check | Command / Location | Expected |
|---|---|---|
| All pods healthy | `kubectl get pods --all-namespaces` | No non-Running pods |
| Service status | `vracli status` | All services: Running |
| Cloud accounts syncing | `vracli cloud-account list` | STATUS: OK |
| vIDM SSO working | Browser login | SAML redirect succeeds |
| Test deployment | Service Broker → Catalogue → Request | DEPLOYMENT_SUCCESSFUL |
| Approval policy | Request large-VM item | Approval email sent |
| Lease policy | Deployment details | Expiry date set |
| ABX subscriptions | Extensibility → Subscriptions | Status: Enabled |
| Backup configured | VAMI → Lifecycle → Backup | Schedule set |
