---
tags:
  - tanzu
  - troubleshooting
  - vmware
search:
  boost: 1.5
---
# Tanzu — Escalation

<div class="kb-summary">
How to escalate VMware Tanzu / TKG issues to Broadcom support: what data to collect, how to run the Tanzu diagnostics bundle, step-by-step case creation on support.broadcom.com, and the escalation path when progress stalls.

*Applies to: Tanzu Kubernetes Grid (TKG) 2.x / 3.x · vSphere with Tanzu 8.x*
</div>
![Tanzu — Escalation](../../../../assets/virtualization-vmware-tanzu-troubleshooting-escalation.svg)




---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
preescalation_selfcheck: "Pre-Escalation Self-Check" {shape: rectangle}
stepbystep_data_collection: "Step-by-Step Data Collection" {shape: rectangle}
how_to_open_the_sr_on_supportbroadco: "How to Open the SR on support.broadcom.com" {shape: rectangle}
escalation_path: "Escalation Path" {shape: rectangle}
what_not_to_do: "What NOT to Do" {shape: rectangle}
useful_commands_for_case_updates: "Useful Commands for Case Updates" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> preescalation_selfcheck: investigate
symptom -> stepbystep_data_collection: investigate
symptom -> how_to_open_the_sr_on_supportbroadco: investigate
symptom -> escalation_path: investigate
symptom -> what_not_to_do: investigate
symptom -> useful_commands_for_case_updates: investigate
preescalation_selfcheck -> resolution
stepbystep_data_collection -> resolution
how_to_open_the_sr_on_supportbroadco -> resolution
escalation_path -> resolution
what_not_to_do -> resolution
useful_commands_for_case_updates -> resolution
```

## Before you begin

- **Access required:** Tanzu CLI configured with kubeconfig for the management cluster; kubectl access to affected clusters; Broadcom support account at support.broadcom.com with active TKG/Tanzu entitlement
- **Do NOT delete a failed workload cluster** without GSS guidance — the cluster VMs may still be running with workloads on them; deletion destroys them without a clean drain
- **Do NOT run `tanzu mc reset`** without explicit GSS direction — this factory-resets the management cluster, deleting all workload cluster registration
- **Collect data from BOTH the management cluster and the affected workload cluster** — GSS will need both for any workload cluster issue

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| Tanzu CLI version | `tanzu version` | Note full version string |
| Management cluster health | `tanzu cluster list --include-management-cluster` | MC shows `Running` |
| Workload cluster health | `tanzu cluster list` | All WC show `Running` |
| Cluster node status | `kubectl get nodes -A --kubeconfig <cluster-kubeconfig>` | All nodes `Ready` |
| Pod status | `kubectl get pods -A --kubeconfig <cluster-kubeconfig>` | No pods stuck `Pending` or `CrashLoopBackOff` |
| Supervisor health (vSphere with Tanzu) | vSphere Client → Workload Management → Supervisors | Supervisor shows `Running` |
| NSX networking | `kubectl get ns -A` | Namespaces accessible |
| Harbor registry health (if used) | Harbor UI → System Health | All components green |
| vCenter version | vCenter → Help → About | Note full vCenter version |

---

## Step-by-Step Data Collection

### 1. Get the Tanzu CLI version and Kubernetes versions

```bash
# Tanzu CLI version — include in every case description
tanzu version

# Kubernetes versions across clusters
tanzu cluster list --include-management-cluster
kubectl version --kubeconfig <management-cluster-kubeconfig>

# For vSphere with Tanzu: check Supervisor version
kubectl get ns -A 2>&1 | head -20
```

### 2. Collect the Tanzu diagnostics bundle

```bash
# Tanzu CLI built-in diagnostics collection
# For management cluster issues:
tanzu diagnostics collect --management-cluster <mgmt-cluster-name>

# For workload cluster issues:
tanzu diagnostics collect --cluster <workload-cluster-name>

# Bundle is saved to the current directory as:
# diagnostics-<cluster-name>-<timestamp>.tar.gz
ls -lh diagnostics-*.tar.gz

# Alternative: collect with verbose logging enabled
TANZU_LOG_LEVEL=debug tanzu cluster get <cluster-name> 2>&1 | tee tanzu-verbose-$(date +%Y%m%d).log
```

### 3. Collect the Kubernetes cluster dump

```bash
# Full cluster dump — all namespaces (can be large)
kubectl cluster-info dump \
  --output-directory=/tmp/cluster-dump-$(date +%Y%m%d) \
  --all-namespaces \
  --kubeconfig <cluster-kubeconfig>

# Compress for upload
tar czf /tmp/cluster-dump-$(date +%Y%m%d).tar.gz /tmp/cluster-dump-$(date +%Y%m%d)/
```

### 4. Collect vCenter and NSX events for cluster VMs

In vSphere Client: navigate to the **datacenter or cluster** hosting the Tanzu node VMs.
- Click **Monitor → Events**
- Filter by the time range covering the failure
- Export all events to a CSV file

For NSX-related networking failures:

```bash
# In the Supervisor or workload cluster:
kubectl get events -A --sort-by='.lastTimestamp' --kubeconfig <cluster-kubeconfig> | tail -100

# Check pod logs for failing control-plane pods
kubectl get pods -n kube-system --kubeconfig <cluster-kubeconfig>
kubectl logs <failing-pod-name> -n kube-system --kubeconfig <cluster-kubeconfig> | tail -200
```

### 5. Write the timeline

```text
Tanzu CLI version: v0.29.0
TKG version: v2.3.1
Management cluster: tkg-mgmt-01
Platform: TKG on vSphere 8.0
vCenter version: 8.0.2 (build 22385739)
Issue first observed: 2026-06-14 10:30 UTC
Last known good state: 2026-06-14 09:00 UTC
Changes in 24h before the issue:
  - 09:00: TKG 2.3.0 → 2.3.1 upgrade applied to the management cluster
  - 10:30: All new workload cluster create attempts fail with error:
    "Error: Cluster API provider reconciliation failed — machine not provisioning"
  - Existing workload clusters are still running
Steps already taken:
  - kubectl get nodes -A: MC nodes all show Ready
  - tanzu cluster list: existing WCs show Running; new cluster create hangs
  - Did NOT delete the failed cluster objects or run tanzu mc reset
Blast radius: New Kubernetes workload cluster creation completely blocked
```

---

## How to Open the SR on support.broadcom.com

1. Go to **support.broadcom.com** and sign in with your Broadcom account.

2. Click **Open a Support Request**.

3. Under **Product Group**, select **VMware Cloud Foundation and Virtualization** → **VMware Tanzu Kubernetes Grid** (for TKG standalone or TKGm) or **VMware vSphere with Tanzu** (for Supervisor-based deployments).

4. Under **Version**, select your TKG or vSphere version from Step 1.

5. Under **Severity**, select:
   - **Severity 1 — Critical**: Supervisor completely down; all workload clusters inaccessible; no cluster creation possible; production workloads halted; no workaround
   - **Severity 2 — High**: Management cluster degraded; workload cluster creation failing; significant pod scheduling failures; existing workloads running but degraded
   - **Severity 3 — Medium**: Single workload cluster in error state; Harbor registry down; specific namespace failing; workaround exists
   - **Severity 4 — Low**: How-to question, pre-upgrade planning, interop compatibility question

6. In the **Summary** field: TKG version + symptom + scope. Example: `TKG 2.3.1 tkg-mgmt-01 — new workload cluster creation failing after MC upgrade, Cluster API reconciliation error, cluster creation blocked`.

7. In the **Description** field, paste:
   - TKG CLI version and Kubernetes version from Step 1
   - The exact error message from `tanzu cluster list` or `kubectl get events`
   - The timeline from Step 5

8. Under **Attachments**, upload:
   - The Tanzu diagnostics bundle from Step 2
   - The Kubernetes cluster dump from Step 3

9. Click **Submit**. You will receive a case number by email immediately.

10. **Severity 1 only:** call Broadcom/VMware support after submission:
    - North America: +1 877-486-9273 (24×7 for Severity 1)
    - EMEA: +44 (0)3453 700 100
    - State "Severity 1 — Tanzu Supervisor/management cluster down, production halted" at the start of the call.

---

## Escalation Path

```text
Step 1 — Open case at support.broadcom.com with diagnostics bundle attached
         ↓
Step 2 — T1 support engineer acknowledges (Sev1: < 30 min; Sev2: < 2 hr)
         ↓
Step 3 — If no meaningful progress in 30 minutes for Sev1 or 2 hours for Sev2:
         → Reply: "Requesting escalation to Tanzu Senior Engineer"
         → State: "[Supervisor down / cluster creation blocked / production halted]"
         ↓
Step 4 — Tanzu T2 Senior Engineer is assigned; they may request kubectl access
         → Have kubeconfig for the management cluster available for a shared session
         → Have vCenter credentials ready in case the issue involves vSphere networking
         ↓
Step 5 — If issue involves a specific component:
         → NSX networking issue: GSS may open a parallel NSX case
         → Harbor registry issue: escalates to Harbor team within Broadcom GSS
         → vSphere integration issue: may involve the vSphere team
         ↓
Step 6 — For Sev1 with no resolution after 2 hours:
         → Request CritSit escalation; contact your Broadcom TAM
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Delete a failed workload cluster without GSS direction | Cluster VMs may still be running workloads; deletion destroys them without a clean drain | Report the cluster state to GSS; they will direct the exact delete/reprovision sequence |
| Run `tanzu mc reset` without GSS | Factory-resets the management cluster; deletes all workload cluster registration | Only run if GSS explicitly instructs after all diagnostic data is collected |
| `kubectl delete` pods on the management cluster | May interrupt Cluster API reconciliation mid-operation | Let GSS diagnose the pod failures before any pod restarts |
| Upgrade the TKG version during an active incident | Changes the version GSS is diagnosing; upgrade may be blocked by the current issue | Freeze all upgrades until the incident is resolved |
| Remove NSX or load balancer integration mid-case | Changes the networking topology GSS is analysing | Hold all infrastructure integration changes until GSS advises |
| Apply Harbor configuration changes during investigation | Changes the registry state if the issue involves Harbor | Freeze all Harbor config changes during the case |

---

## Useful Commands for Case Updates

```bash
# Cluster state summary — paste into every case update
tanzu version
tanzu cluster list --include-management-cluster

# Management cluster node and pod health
kubectl get nodes -A --kubeconfig <mgmt-kubeconfig>
kubectl get pods -A --kubeconfig <mgmt-kubeconfig> | grep -v Running | grep -v Completed

# Workload cluster node state
kubectl get nodes --kubeconfig <workload-kubeconfig>

# Cluster API machine state (in management cluster)
kubectl get machines -A --kubeconfig <mgmt-kubeconfig>
kubectl get machinedeployments -A --kubeconfig <mgmt-kubeconfig>

# Recent events across all namespaces
kubectl get events -A --sort-by='.lastTimestamp' --kubeconfig <mgmt-kubeconfig> | tail -50

# Package installs (if carvel packages are involved)
tanzu package installed list -A
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 — Critical | Supervisor down; all workloads inaccessible; no cluster creation possible | < 30 min (24×7) |
| Sev 2 — High | MC degraded; WC creation failing; significant scheduling failures | < 2 hours (24×7) |
| Sev 3 — Medium | Single cluster/namespace failing; workaround exists | < 8 hours |
| Sev 4 — Low | How-to, planning, compatibility question | Next business day |

---

## Component-Specific Support

| Component | Owner within Broadcom GSS |
|---|---|
| Supervisor / vSphere with Tanzu | vSphere team (may involve NSX team) |
| TKG management / workload cluster | Tanzu team |
| Harbor Registry | Harbor team (within Tanzu group) |
| NSX load balancer (Supervisor) | NSX/NSX ALB team |
| Pinniped authentication | Tanzu team |
| carvel packages | Tanzu team |

---

## See also

- [Tanzu — Diagnostics](diagnostics/)
- [Tanzu — Common Issues](common-issues/)

---

## Verify resolution

- Run `tanzu cluster list --include-management-cluster` and confirm all clusters show `Running`
- Run `kubectl get nodes -A --kubeconfig <mgmt-kubeconfig>` and confirm all nodes are `Ready`
- Attempt to create a new small workload cluster and confirm it provisions successfully
- Run `kubectl get pods -A` on both the MC and an existing WC and confirm no pods stuck in `Pending` or `CrashLoopBackOff`
- Monitor for 15 minutes to confirm no new failures appear
