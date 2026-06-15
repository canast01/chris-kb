---
tags:
  - reference
---
# VMware Platform Gotchas

<div class="kb-summary">
Known VMware platform pitfalls, unexpected behaviours, and operational traps. Each entry documents the symptom, root cause, and corrective or preventive action.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌─────────────────────────────────── Virtualization Vmware Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                        Vmware: Virtualization Vmware Reference platform                       │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                 Management: Virtualization Vmware Reference management console                │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Vmware Reference infrastructure · management network · monitoring         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Vmware             = Virtualization Vmware Reference platform overview and core concepts           │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


Known pitfalls, unexpected behaviours, and non-obvious operational traps across the VMware platform. Each entry documents the symptom, root cause, and corrective or preventive action.

---

## vSAN — clomRepairDelay Catches Admins Off Guard

**Symptom:** A host goes down during maintenance; no rebuild starts for 60 minutes. Alerts fire. Team panics.

**Cause:** `clomRepairDelay` (default 60 min) is intentional — vSAN waits to see if the host returns before triggering a rebuild. It is not a bug; it prevents unnecessary I/O churn when a host bounces briefly.

**Fix / Avoid:** For planned maintenance, put the host in Maintenance Mode (Full Data Migration or Ensure Accessibility) before powering off — this triggers an immediate, orderly resync. For an emergency outage where you need to force an early rebuild, reduce the delay temporarily:

```bash
esxcli vsan cluster set --clom-repair-delay-minutes 0
```

Reset to the original value (60) after the resync completes.

---

## vSAN — ESA and OSA Are Mutually Exclusive per Disk Group

**Symptom:** Attempting to enable ESA on a cluster that has OSA disk groups fails with a cryptic error.

**Cause:** ESA (Express Storage Architecture) and OSA (Original Storage Architecture) cannot coexist in the same cluster. Migrating requires evacuating all data, removing existing disk groups, and re-claiming disks under the new architecture.

**Fix / Avoid:** Plan ESA adoption from day 0. Migrating an existing OSA cluster to ESA is a destructive operation — all data must be migrated off the cluster first. There is no in-place upgrade path between architectures.

---

## vSAN — Stretched Cluster Witness Must Not Be Domain-Joined

**Symptom:** Witness VM is joined to Active Directory; SSO replication fails or the witness loses connectivity intermittently.

**Cause:** The witness VM should never be domain-joined. DNS round-robin or AD load balancing can interfere with the dedicated witness heartbeat network, causing the witness to be unreachable on the expected IP.

**Fix / Avoid:** Deploy the witness VM in workgroup mode. Use a dedicated management IP and a static DNS entry. Do not apply domain GPOs or domain-based NTP sources to the witness.

---

## NSX — DFW Policy Must Be Published to Take Effect

**Symptom:** A new DFW rule is visible in the UI but traffic is not being blocked or allowed as expected.

**Cause:** In Policy mode, rules are saved as drafts by default and require an explicit **Publish** action before they are pushed to the dataplane. A rule that is saved but not published has no enforcement effect.

**Fix / Avoid:** Always click **Publish** after saving rule changes. Verify enforcement via Traceflow. Via API: send a `PATCH` to the policy endpoint to update the rule, then a `POST` to the `?action=publish` endpoint to push it to the dataplane.

---

## NSX — Transport Node Reboot Required After Host Profile Application

**Symptom:** After applying an NSX host profile to ESXi hosts via vLCM, transport nodes show as "Out of Sync" until a maintenance window is completed.

**Cause:** Some NSX kernel module parameters require a full host reboot to take effect. Applying the profile via vLCM updates the configuration on disk but does not automatically reboot the host.

**Fix / Avoid:** Schedule a rolling reboot of ESXi hosts after host profile application. Include this reboot requirement explicitly in the change window plan so stakeholders are not surprised by the Out of Sync state.

---

## NSX — Edge VM CPU Must Be Pinned to a Dedicated NUMA Node for BFD

**Symptom:** BFD sessions flap intermittently; BGP reconverges randomly with no clear network event.

**Cause:** Edge VMs sharing NUMA nodes with high-CPU workload VMs can experience BFD timer inconsistency. The default 300 ms BFD hello interval is violated under CPU contention, causing the peer to declare the session down.

**Fix / Avoid:** Pin Edge VMs to a dedicated NUMA node using CPU affinity, or run them on dedicated ESXi hosts. Reserve CPU resources for Edge VMs in vSphere to prevent scheduler starvation. Validate BFD timer stability after any workload density change on Edge hosts.

---

## vCenter — Expired Certificate Causes Cascade Failure

**Symptom:** vCenter services fail to start; hosts disconnect; SSO authentication fails; the web UI shows a certificate error on login.

**Cause:** VMCA issues machine certificates with a 2-year validity by default. When the machine SSL certificate expires, the `vpxd` daemon, lookup service, and SSO token service all fail simultaneously because they mutually authenticate using the same certificate chain.

**Fix / Avoid:** Monitor VMCA certificate expiry proactively:

```bash
/usr/lib/vmware-vmafd/bin/vecs-cli entry list --store MACHINE_SSL_CERT | grep -i valid
```

Set a 60-day alert. Renew certificates proactively using `certificate-manager` before expiry. Do not wait for services to fail.

---

## vCenter — vCLS Agent VMs Cannot Be Deleted from Inventory

**Symptom:** An admin deletes or powers off vCLS agent VMs to reclaim resources; DRS immediately stops working for the affected cluster.

**Cause:** vCLS (vSphere Cluster Services) agent VMs are automatically managed by vCenter and are required for DRS and HA to function. vCenter will attempt to recreate any deleted agent VMs, but DRS operates in a degraded state until they are healthy.

**Fix / Avoid:** Never delete vCLS agent VMs. If troubleshooting requires temporarily disabling vCLS, use Retreat Mode by setting the following key in vCenter advanced settings:

```text
config.vcls.clusters.<cluster-id>.enabled = false
```

Re-enable after troubleshooting is complete. vCenter will automatically recreate healthy agent VMs when Retreat Mode is disabled.

---

## vLCM — Image and Baseline Management Are Mutually Exclusive

**Symptom:** After migrating a cluster to image-based management, the Baselines tab disappears; team members attempt to apply a patch via baseline and cannot find the option.

**Cause:** vLCM image mode and baseline mode cannot coexist in the same cluster. Once a cluster is migrated to desired-state image management, all patching must go through image updates and the software depot. There is no way to revert to baseline mode without rebuilding the cluster.

**Fix / Avoid:** This is by design. Plan all patch application via image updates and the depot. Train all team members on the image workflow before migrating clusters — the Baselines tab will not return.

---

## vLCM — Quick Boot Requires UEFI and No PCI Passthrough

**Symptom:** The Quick Boot option is greyed out for a host, or a host configured for Quick Boot falls back to a full reboot during remediation.

**Cause:** Quick Boot requires UEFI firmware, compatible hardware (listed on the VMware HCL), and no PCI passthrough devices attached to any VMs on the host. Any PCI passthrough assignment disables Quick Boot for the entire host.

**Fix / Avoid:** Check Quick Boot compatibility:

```bash
vim-cmd hostsvc/quickboot/enabled
```

Remove PCI passthrough device assignments from all VMs on the host before enabling Quick Boot. Verify against the HCL if the host is borderline-compatible.

---

## SRM — Placeholder VMs Must Be Refreshed After vCenter Upgrade

**Symptom:** After upgrading vCenter at the recovery site, some placeholder VMs show as orphaned or missing in SRM.

**Cause:** A vCenter upgrade can change VM MoRef IDs or datastore associations. Placeholder VM registration in SRM references these identifiers directly, and the stale references cause placeholder VMs to appear orphaned in inventory.

**Fix / Avoid:** After any vCenter upgrade at the recovery site, run **Configure All** on each Protection Group to force SRM to recreate stale placeholder VMs. Include this step in the vCenter upgrade runbook for the recovery site.

---

## SRM — Test Cleanup Must Complete Before Running a Real Failover

**Symptom:** Attempting to run a Recovery Plan while a test is in progress fails with "Plan is in test state".

**Cause:** SRM holds the replicated datastore in snapshot mode during a test recovery. A real failover cannot proceed until the test snapshot is released and the datastore is returned to a consistent state.

**Fix / Avoid:** Always initiate **Cleanup** after a test completes and allow it to finish fully before declaring the plan ready for production use. Never leave a Recovery Plan in a partial test state. Build Cleanup into the DR test runbook as a mandatory final step.

---

## Horizon — ClonePrep Domain Join Fails if Pre-Staged Account Limit Is Reached

**Symptom:** Instant clone desktops fail to provision; the ClonePrep log shows "account creation failed" or an LDAP error during domain join.

**Cause:** The domain-join account has exhausted the default AD limit of 10 computer accounts creatable by a non-admin user, or the target OU has an explicit quota set. ClonePrep cannot create new computer objects and the provisioning job fails silently at the AD step.

**Fix / Avoid:** Use a dedicated service account with explicit delegation to create and manage computer accounts in the Horizon OU. Do not rely on default user permissions. Verify the account has no join limit and that the OU has no object quota before deploying a new pool.

---

## Horizon — Parent VM Must Stay Powered On for Instant Clone Pools

**Symptom:** After powering off the parent VM for maintenance, new desktop provisioning stalls; existing desktops are unaffected.

**Cause:** Instant clone uses `vmFork` against the live memory state of the parent VM. If the parent VM is powered off, the memory fork source does not exist and no new desktops can be created. The parent VM is not interchangeable with a template.

**Fix / Avoid:** The parent VM must remain running at all times while the pool is active. Schedule parent VM maintenance only during off-peak windows with an agreed brief provisioning outage. Communicate the outage to the pool's users in advance.

---

## VCF — Precheck Failures Block All LCM Operations

**Symptom:** An upgrade is queued in SDDC Manager; it is marked as blocked and no upgrade steps can proceed.

**Cause:** VCF's Precheck validates DNS (forward and reverse), NTP sync, certificate expiry, password rotation status, and vSAN health before any LCM operation. Any single failure blocks the entire upgrade chain — there is no way to skip individual precheck items.

**Fix / Avoid:** Run Precheck on demand regularly, not just before upgrades. Resolve DNS reverse-lookup failures, expired certificates, and credential rotation issues proactively. Treat Precheck failures as P2 incidents so they are addressed before an upgrade window arrives.

---

## VCF — NSX Manager Upgrade Must Follow SDDC Manager Upgrade

**Symptom:** After upgrading SDDC Manager, NSX Manager shows as "Unsupported version" in the SDDC Manager UI.

**Cause:** VCF enforces strict BOM (Bill of Materials) ordering. NSX must be upgraded after SDDC Manager and vCenter, never before. Upgrading NSX outside of SDDC Manager orchestration, or upgrading it first, breaks the BOM alignment and puts the environment into an unsupported state.

**Fix / Avoid:** Always follow the VCF upgrade sequence:

```text
SDDC Manager → vCenter → ESXi → NSX → vSAN on-disk format
```

Never upgrade any component outside of SDDC Manager orchestration. If a component was upgraded out of order, open a VMware support case before proceeding — attempting to continue LCM operations in a mismatched BOM state can cause further failures.

---

## Horizon — UAG Certificate Mismatch Breaks HTML Access and Client Connections Silently

**What catches admins:** Users report that Horizon Client connects intermittently, or HTML Access shows a certificate warning that users click through, while the admin console shows all UAG services as healthy.

**Why it happens:** Unified Access Gateway (UAG) uses three independent certificate stores: the external-facing TLS certificate, the Horizon Connection Server pairing certificate, and the admin UI certificate. Replacing only the external TLS certificate (the most visible one) leaves the Connection Server pairing certificate unchanged. When that pairing certificate expires or mismatches the Connection Server's expected thumbprint, the back-end session tunnel to Connection Server breaks — but UAG continues to report itself as healthy because the health check probes the admin port, not the tunnel.

**How to avoid / fix:** When replacing any UAG certificate, audit all three certificate bindings in the UAG admin UI (HTTPS/TLS, Connection Server pairing, and admin UI) in the same change window. Set monitoring on all three certificate expiry dates independently. If tunnel failures are suspected, check the UAG gateway logs under `/opt/vmware/gateway/logs/` for `TUNNEL_DISCONNECT` events alongside the Connection Server event logs.

---

## Horizon — App Volumes Agent Version Must Match the App Volumes Manager Version Exactly

**What catches admins:** After upgrading App Volumes Manager, existing desktops function normally but new instant clone desktops fail to attach AppStacks or writable volumes. The App Volumes event log shows "Agent version mismatch" or attachments silently fail with no error surfaced to the end user.

**Why it happens:** App Volumes enforces a strict version lock between the agent installed in the gold image (and thus in every instant clone derived from it) and the App Volumes Manager. When Manager is upgraded, desktops running the previous agent version are tolerated for existing sessions, but new desktops forked from an unupdated parent VM present the old agent version, which the upgraded Manager refuses to service.

**How to avoid / fix:** Always update the gold image (parent VM) agent version in the same maintenance window as the App Volumes Manager upgrade. The update sequence is: upgrade Manager first, then update the agent in the parent VM, push the updated parent VM to all pools. Do not upgrade Manager and leave the gold image update for a later window — any new desktops provisioned in the gap will fail volume attachment silently.

---

## Tanzu — Supervisor Namespace IP Range Exhaustion Stalls All Workload Cluster Creation

**What catches admins:** New TKC (Tanzu Kubernetes Cluster) creation requests hang at "Pending" indefinitely. Existing clusters are unaffected. The Supervisor control plane shows no error in the vCenter UI.

**Why it happens:** The Supervisor Namespace IP range is configured during Workload Management enablement and is fixed at that point. Each Supervisor VM, each TKC control plane VM, and each TKC worker node consumes an IP from this range. In environments where the initial range was sized for a pilot and then expanded with additional TKCs, the range becomes exhausted. When all IPs are consumed, new cluster creation requests wait for an IP indefinitely with no explicit "out of IP addresses" error surfaced to the administrator.

**How to avoid / fix:** Size the Supervisor Namespace IP range to at least 5x the anticipated peak number of TKC nodes, including control planes, at design time. To check current consumption:

```bash
kubectl get virtualmachinesetresourcepolicies -A
```

If the range is exhausted, the only remediation is to remove unused TKCs to free IPs, or to re-enable Workload Management with a larger range — which requires destroying all existing TKCs. Plan the range generously at initial deployment.

---

## Tanzu — TKC Upgrades Cannot Skip Minor Versions

**What catches admins:** An administrator attempts to upgrade a TKC from Kubernetes 1.25 to 1.27 in a single operation to catch up after a period of deferred upgrades. The upgrade request is rejected or silently queued without explanation.

**Why it happens:** Tanzu Kubernetes Grid enforces the same sequential minor-version upgrade constraint as upstream Kubernetes. A TKC on 1.25 must be upgraded to 1.26 before it can be upgraded to 1.27. Unlike vSphere component upgrades which can be batched, Kubernetes minor version skipping is not supported and will be blocked by the TKG service even if the target image is available in the content library.

**How to avoid / fix:** Establish a Kubernetes version lifecycle policy that limits the acceptable age of a running TKC to no more than two minor versions behind the current supported release. Check TKC versions regularly:

```bash
kubectl get tkc -A
```

For clusters that have fallen behind, plan sequential upgrade windows rather than attempting a single jump. Each minor version upgrade should be validated (workloads running, kube-system pods healthy) before proceeding to the next step.

---

## VxRail — LCM Bundle Download Failures Leave the Cluster in a Partial Upgrade State

**What catches admins:** A VxRail LCM upgrade is initiated through the VxRail Manager plugin in vCenter. The bundle download phase fails partway through (connectivity loss, timeout, or proxy authentication error). The administrator retries the upgrade — but VxRail LCM reports a conflict because a partial bundle exists, and subsequent attempts fail with a generic "bundle validation error."

**Why it happens:** VxRail LCM stages bundle files to the VxRail Manager VM local filesystem during download. If the download is interrupted, partial files remain on disk. The LCM engine validates bundle checksums before proceeding and correctly rejects partial downloads — but the error message does not clearly identify the partial file as the cause or explain how to clean it up. Retrying the download via the UI attempts to write to the same path and fails the same validation.

**How to avoid / fix:** Ensure stable internet connectivity or a local Dell update repository is configured before initiating any LCM bundle download. If a partial download occurs, SSH to the VxRail Manager VM, navigate to `/data/store/` (or the configured bundle staging path), and remove incomplete bundle files before retrying. Verify the proxy configuration and firewall egress rules permit access to `dl.dell.com` and `downloads.vmware.com` without authentication challenges. Use the Dell Update Repository (DUP) offline bundle method for environments with restricted egress.

---

## VxRail — Mixed Hardware Generations in a Single Cluster Are Not Supported After Initial Build

**What catches admins:** An existing VxRail cluster is partially refreshed with newer-generation nodes (e.g., VxRail E Series Gen 2 added to an existing Gen 1 cluster) to expand capacity. The new nodes initially join and appear healthy. After the next LCM upgrade cycle, SDDC Manager or VxRail Manager flags the cluster as invalid or blocks the upgrade entirely.

**Why it happens:** VxRail clusters are validated and certified as a homogeneous hardware unit. VxRail Manager's LCM pipeline selects a single firmware and driver bundle for the entire cluster based on the cluster's registered hardware profile. When mixed hardware generations are present, no single bundle satisfies all node models, and the LCM validation fails. While the hosts may function at the vSphere layer, VxRail's integrated lifecycle management cannot manage a heterogeneous cluster.

**How to avoid / fix:** All nodes in a VxRail cluster must be from a compatible hardware profile within the same generation as defined in the VxRail compatibility matrix. To expand with newer hardware, create a new VxRail cluster (a new VCF Workload Domain or a standalone cluster) using the new-generation nodes exclusively. Workloads can then be migrated using vMotion from the old cluster to the new cluster. Never add nodes of a different model family to an existing VxRail cluster mid-lifecycle.

---

## Aria — LCM Certificate Rotation Breaks Product Registrations Silently

**What catches admins:** After rotating certificates in Aria Suite Lifecycle Manager (LCM), Aria Operations, Aria Automation, or Aria Operations for Logs appears healthy in LCM but inter-product API calls begin failing. Workflows that depend on cross-product integration (e.g., Aria Automation calling Aria Operations for placement decisions) stop working without any alert in the product UIs.

**Why it happens:** Aria LCM stores certificate thumbprints for all registered products in its internal trust store. When a product certificate is rotated, LCM updates that product's certificate but does not automatically propagate the new thumbprint to all other registered products that communicate with it. Products that cached the old thumbprint for mutual TLS validation continue to reject connections from the rotated product, causing silent integration failures at the API layer rather than at the product health check layer.

**How to avoid / fix:** After any certificate rotation in Aria LCM, trigger a **Sync** operation on all other registered products to force LCM to refresh cross-product trust store entries. Verify inter-product connectivity from the LCM Inventory view. Include a post-rotation integration test (e.g., trigger a test Aria Automation cloud template deployment that exercises Aria Operations placement) in the certificate rotation runbook. Do not close the change window until all integration checks pass.

---

## Aria — Adapter Credential Drift Causes Silent Data Collection Gaps in Aria Operations

**What catches admins:** Aria Operations dashboards show stale metrics for a subset of monitored objects — the objects are present in inventory, the adapter instance shows as "Collecting," but metric graphs flatline or show gaps. No alert is raised because the adapter reports a healthy collection state.

**Why it happens:** Aria Operations adapter instances cache credentials locally when they are configured. If the target system's service account password is rotated (Active Directory password expiry, vCenter service account rotation, NSX Manager credential update) but the adapter instance in Aria Operations is not updated simultaneously, the adapter's authentication attempts begin failing. Many adapter types treat repeated authentication failures as transient network errors and continue reporting "Collecting" rather than transitioning to a "Credential Error" state, masking the data gap.

**How to avoid / fix:** Maintain a registry of all Aria Operations adapter instances and their associated service accounts. Synchronise adapter credential updates with password rotation events — treat Aria Operations as a dependency that must be updated in the same change window as any monitored system's service account rotation. After a rotation, validate adapter collection health by confirming that the most recent metric timestamp for a representative monitored object is current:

From Aria Operations UI: **Administration → Solutions → [Adapter Instance] → Test Connection**, then confirm the last collected timestamp in the monitored object's metric browser.
