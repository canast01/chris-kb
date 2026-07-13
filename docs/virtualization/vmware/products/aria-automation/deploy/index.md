---
tags:
  - aria-automation
  - deployment
  - vmware
search:
  boost: 1.5
description: "End-to-end deployment guide for VMware Aria Automation (on-premises). Covers prerequisites, LCM-based deployment, cloud account configuration, project and..."
---
# Aria Automation — Deploy

<div class="kb-summary">
End-to-end deployment guide for VMware Aria Automation (on-premises). Covers prerequisites, LCM-based deployment, cloud account configuration, project and blueprint setup, and end-to-end validation.

*Applies to: Aria Automation 8.x*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_predeployment_prerequisites: "Phase 1 — Pre-Deployment Prerequisites" {shape: rectangle}
phase_2_lcm_deployment: "Phase 2 — LCM Deployment" {shape: rectangle}
phase_3_cloud_account_configuration: "Phase 3 — Cloud Account Configuration" {shape: rectangle}
phase_4_projects_mappings_and_govern: "Phase 4 — Projects, Mappings, and Governance" {shape: rectangle}
phase_5_blueprints_and_service_catal: "Phase 5 — Blueprints and Service Catalogue" {shape: rectangle}
phase_6_endtoend_validation: "Phase 6 — End-to-End Validation" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_predeployment_prerequisites
phase_1_predeployment_prerequisites -> phase_2_lcm_deployment
phase_2_lcm_deployment -> phase_3_cloud_account_configuration
phase_3_cloud_account_configuration -> phase_4_projects_mappings_and_govern
phase_4_projects_mappings_and_govern -> phase_5_blueprints_and_service_catal
phase_5_blueprints_and_service_catal -> phase_6_endtoend_validation
phase_6_endtoend_validation -> validate
```

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


```text title="Expected output"
Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	aac.example.local
Address: 10.20.5.42

Server:		10.0.1.53
Address:	10.0.1.53#53

Name:	service-broker.example.local
Address: 10.20.5.43

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   287  100   287    0     0   1205      0 --:--:-- -- 0:00:00 --:--:-- 0:00:00
"status": "ALIVE"
```

!!! warning "Common errors"
    **`nslookup: can't resolve 'aac.example.local': No address associated with hostname`** — Verify DNS server is reachable and the hostname is registered in your DNS zone; use `nslookup @<dns-ip> aac.example.local` to test a specific server.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag (already present) or import the vIDM certificate into your system's CA bundle with `curl -cacert /path/to/cert.pem https://vidm.example.local/SAAS/auth/heartbeat`.
    **`curl: (7) Failed to connect to vidm.example.local port 443: Connection refused`** — Verify vIDM appliance is running and accessible on port 443 using `telnet vidm.example.local 443` or check firewall rules between LCM and vIDM.
TLS: generate a SAN cert covering all FQDNs above; upload to LCM Certificate Management before deployment.

---

## Phase 2 — LCM Deployment

**Exit criterion:** All Aria Automation services show Running in LCM; `vracli status` returns no errors.

**Option A — Easy Installer (greenfield):** mounts an ISO and deploys LCM + vIDM + Aria Automation in a single wizard. Collects all network parameters (FQDNs, DNS, NTP, vCenter targets) in one workflow.

**Option B — Add to existing LCM:**

![Aria Automation — Deploy — Diagram](../../../../../assets/virtualization-vmware-aria-automation-deploy-diagram.svg)

```bash
# Monitor deployment from LCM appliance
ssh root@lcm.example.local
tail -f /var/log/vmware/lcm/lcm-debug.log | grep -E "DEPLOY|ERROR|WARN"
```


```text title="Expected output"
Connected to lcm.example.local.
2024-01-15T09:42:33.521Z [INFO] DEPLOY: Starting deployment of Aria Automation 8.12.1
2024-01-15T09:42:45.203Z [WARN] DEPLOY: Waiting for vCenter connectivity (attempt 2/5)
2024-01-15T09:43:12.847Z [INFO] DEPLOY: Configuring PostgreSQL database cluster
2024-01-15T09:44:01.556Z [ERROR] DEPLOY: Failed to mount NFS datastore at 192.168.1.50:/exports/aria
2024-01-15T09:44:02.112Z [WARN] DEPLOY: Retrying NFS mount (attempt 1/3)
2024-01-15T09:44:35.891Z [INFO] DEPLOY: Identity provider synchronization complete
2024-01-15T09:45:18.634Z [INFO] DEPLOY: Aria Automation deployment finished successfully
```

!!! warning "Common errors"
    **`Permission denied (publickey).`** — Ensure SSH key is configured or use `ssh-keyscan` to add the host key, then verify root SSH access is enabled on the LCM appliance.
    **`tail: cannot open '/var/log/vmware/lcm/lcm-debug.log' for reading: No such file or directory`** — Verify the LCM service is running with `systemctl status vmware-lcm` and check the correct log path with `find /var/log -name "*lcm*"`.
    **`grep: (standard input): No such device or address`** — The log file may be rotating; use `tail -f /var/log/vmware/lcm/lcm-debug.log*` to follow all rotated logs or increase the buffer with `tail -f -n 100`.
After the 60–90 minute deployment:

```bash
ssh root@aac.example.local
vracli status        # all services: Running
vracli status --all  # detailed pod health
vracli version       # confirm build matches target
kubectl get pods --all-namespaces | grep -v "Running\|Completed\|Succeeded"
# Expected: no output
```


```text title="Expected output"
root@aac.example.local's password: 
vRA Cloud Assembly is running
vRA Service Broker is running
vRA Orchestrator is running
vRA Code Stream is running
vRA Automation Config is running

NAME                                    READY   STATUS    RESTARTS   AGE
vra-automation-config-5d8c7f9b2-kx4m9   1/1     Running   0          14d
vra-service-broker-7f2e1c6a9-jm3k2      1/1     Running   2          21d
vra-orchestrator-9b4c2e5f1-pq7r8        1/1     Running   1          7d
vra-code-stream-6a3d9e2c4-nt5v3         1/1     Running   0          3d

vRA Automation 8.11.2 Build 20231015.1234567
```

!!! warning "Common errors"
    **`vracli: command not found`** — Ensure you are logged in as root and the vRA CLI is installed in the PATH; check `/opt/vmware/vra/bin/vracli` exists.
    **`Unable to connect to Kubernetes cluster`** — Verify kubectl is configured with the correct kubeconfig and the cluster API server is reachable from this node.
    **`pod status shows CrashLoopBackOff or ImagePullBackOff`** — Check pod logs with `kubectl logs <pod-name> -n <namespace>` and verify container images are accessible in your registry.
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


```text title="Expected output"
Cloud Accounts:
ID                                    Name              Type              Status
550e8400-e29b-41d4-a716-446655440000  aws-prod-east     aws               CONNECTED
6ba7b810-9e12-11e1-80d6-4f50646f6c61  azure-dev         azure             CONNECTED
6ba7b811-9e12-11e1-80d6-4f50646f6c61  vsphere-lab       vsphere           CONNECTED
7ba7b812-9e12-11e1-80d6-4f50646f6c61  gcp-staging       gcp               DISCONNECTED

Syncing cloud account 550e8400-e29b-41d4-a716-446655440000...
Sync initiated successfully. Job ID: job-2024-01-15-08-42-5f7e9c
```

!!! warning "Common errors"
    **`Error: Cloud account not found: <id>`** — Verify the account ID with `vracli cloud-account list` and use the exact UUID from the ID column.
    **`Error: Sync already in progress for this account`** — Wait for the previous sync job to complete or check status with `vracli cloud-account show --id <id>`.
    **`Error: Authentication failed for cloud account`** — Re-validate the cloud account credentials in the Aria Automation UI under Infrastructure > Cloud Accounts.
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

![Aria Automation — Deploy — Diagram](../../../../../assets/virtualization-vmware-aria-automation-deploy-d2.svg)

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


```text title="Expected output"
root@aac.example.local's password: 
NAME                                    READY   STATUS    RESTARTS   AGE
vra-automation-config-5d8f9c2b1-xyz9k   1/1     Running   0          14d
vra-iaas-proxy-7c4a2e1f-abc3d           1/1     Running   2          8d
vra-orchestrator-engine-9b2k1m5-def6g   1/1     Running   0          21d

Service Status Report:
  vra-automation-service      Running (healthy)
  vra-iaas-service            Running (healthy)
  vra-orchestrator-service    Running (healthy)
  vra-config-service          Running (healthy)

Cluster Health Status:
  Node: aac-node-01.example.local    Status: Healthy   Quorum: Yes
  Node: aac-node-02.example.local    Status: Healthy   Quorum: Yes
  Node: aac-node-03.example.local    Status: Healthy   Quorum: Yes
  Cluster consensus: ESTABLISHED
```

!!! warning "Common errors"
    **`Connection refused`** — Verify SSH is enabled on the AAC appliance and the hostname/IP is correct with `ping aac.example.local`.
    **`vracli: command not found`** — Ensure you are logged in as root and the vracli binary is in the PATH; check `/opt/vmware/vra/bin/` exists.
    **`CrashLoopBackOff` or `ImagePullBackOff` in pod status** — Check pod logs with `kubectl logs <pod-name> -n <namespace>` and verify image registry connectivity and disk space.
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

---

## See also

- [Aria Automation — How It Works](../architecture/how-it-works/)
- [Aria Automation — Health Checks](../operations/health-checks/)
- [Aria Automation — Common Issues](../troubleshooting/common-issues/)

## Verify

- **vSphere Client:** confirm the component is visible and shows a healthy status
- **Alarms:** Home → Alarms — no new critical alarms after deployment
- **Logs:** review vmware.log / recent events for any errors in the first 5 minutes
