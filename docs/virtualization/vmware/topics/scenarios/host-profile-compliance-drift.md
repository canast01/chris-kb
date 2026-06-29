---
tags:
  - scenarios
  - vmware
---
# Host Profile Compliance Drift

<div class="kb-summary">
One or more ESXi hosts show as non-compliant against the cluster's host profile after a
patch cycle, manual configuration change, or hardware replacement. This scenario covers
how to identify which settings have drifted, determine whether the drift is intentional
or accidental, and remediate by applying the host profile — or by updating the profile
to capture the intended new state.

*Applies to: vSphere 7.x / 8.x*
</div>

!!! warning "Hosts reboot during remediation"
    Applying a host profile that changes kernel parameters or drivers requires a host reboot. Ensure DRS can evacuate each host before remediation begins.

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_run_the_compliance_report: "1. Run the Compliance Report" {shape: rectangle}
2_identify_common_drift_categories: "2. Identify Common Drift Categories" {shape: rectangle}
3a_accidental_drift_apply_the_host_p: "3a. Accidental Drift — Apply the Host Profile" {shape: rectangle}
3b_intentional_drift_update_the_host: "3b. Intentional Drift — Update the Host Profile" {shape: rectangle}
4_recheck_and_validate: "4. Re-Check and Validate" {shape: rectangle}

products_involved -> 1_run_the_compliance_report: uses
1_run_the_compliance_report -> 2_identify_common_drift_categories: uses
2_identify_common_drift_categories -> 3a_accidental_drift_apply_the_host_p: uses
3a_accidental_drift_apply_the_host_p -> 3b_intentional_drift_update_the_host: uses
3b_intentional_drift_update_the_host -> 4_recheck_and_validate: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Host Profiles UI; compliance check; remediation orchestration |
| ESXi | Host configuration; remediation target; profile application |
| vLCM | May replace host profiles for cluster image management in vSphere 7+ |
| Aria Operations | Configuration drift alerting; compliance trend tracking |

---

## 1. Run the Compliance Report

Navigate to **vCenter → Policies and Profiles → Host Profiles** and select the profile applied to the cluster.

```text
Host profile compliance check steps:
  1. Select the host profile
  2. Actions → Check Host Profile Compliance
  3. Wait for check to complete (seconds to minutes depending on cluster size)
  4. Click "Non-Compliant" hosts to expand the compliance detail
```

The compliance report shows each non-compliant setting as a separate row:

```text
Compliance report columns:
  Policy Name    — the specific configuration category (NTP, DNS, vSwitch, security)
  Host Setting   — current value on the host
  Profile Value  — value defined in the host profile
  Status         — Non-Compliant (shows divergence) or Compliant
```

Look for: group the failures by category. A cluster-wide failure affecting all hosts at the same time usually means the profile was updated without reflecting a recent patch or hardware change. A single-host failure points to a local configuration change on that host.

---

## 2. Identify Common Drift Categories

```text
Most frequent drift categories after a patch cycle:
  NTP / time configuration       — new pool server in profile vs actual
  Security profile / lockdown    — lockdown mode changed after emergency SSH access
  vSwitch / port group settings  — MTU or teaming policy changed for troubleshooting
  Kernel module parameters       — patch changes module version or parameter defaults
  SNMP community string          — infrastructure team changed strings without updating profile
  DNS suffix list                — DNS change not propagated via profile
  Syslog host                    — log target changed during an incident
  SSH / DCUI state               — SSH left enabled after troubleshooting
```

For each non-compliant setting, determine whether the host's current value or the profile's value represents the desired state going forward.

---

## 3a. Accidental Drift — Apply the Host Profile

If the host's current value is wrong and the profile is correct, remediate by applying the profile to the host.

```text
Remediation prerequisites:
  - Host must be in Maintenance Mode OR vMotion available for VMs
  - Storage vMotion may be required for VMs with local storage
  - Some profile settings require a host reboot (kernel parameters, VIB changes)
  - Check if remediation will require a reboot before scheduling
```

Check whether remediation requires a reboot:

```text
vCenter → Host Profiles → select profile → Actions → Pre-check Remediation
Output shows: which settings require reboot vs which are applied live
```

Apply the profile:

```text
vCenter → Hosts and Clusters → right-click host → Host Profile → Remediate
Select profile → review task list → confirm
```

For a full cluster remediation, use the **Remediate** button from within the host profile view — vCenter will coordinate maintenance mode and vMotion automatically.

---

## 3b. Intentional Drift — Update the Host Profile

If the host's current value is the desired state and the profile is outdated, update the profile from the reference host.

```text
Option A: Update profile from reference host
  Host Profiles → select profile → Actions → Update from Reference Host
  Select the host with the correct configuration
  Review changes before saving — compare old vs new profile values

Option B: Edit profile directly
  Host Profiles → select profile → Edit Settings
  Navigate to the specific policy category and update the value
  More surgical — preserves all other profile settings
```

After updating the profile, re-run the compliance check to confirm all hosts are now compliant against the updated profile.

Look for: if multiple hosts made the same change independently (e.g., all had SSH enabled after an incident), the right action is usually to update the profile rather than revert all hosts — the change was operationally necessary and should become the new baseline.

---

## 4. Re-Check and Validate

After remediation or profile update, confirm compliance:

```text
vCenter → Policies and Profiles → Host Profiles → select profile
Actions → Check Host Profile Compliance
All hosts should show: Compliant
```

For post-patch validation in a large cluster, use PowerCLI to check compliance across all hosts at once:

```powershell
# Check host profile compliance for all hosts in a cluster
$cluster = Get-Cluster -Name "production-cluster"
$profile = Get-VMHostProfile -Entity $cluster

foreach ($vm in Get-VMHost -Location $cluster) {
    $compliance = Test-VMHostProfileCompliance -VMHost $vm
    [PSCustomObject]@{
        Host         = $vm.Name
        Status       = $compliance.ComplianceStatus
        Failures     = ($compliance.IncomplianceElementList | Measure-Object).Count
    }
} | Format-Table -AutoSize
```

Look for: any host remaining non-compliant after remediation may have a locked setting (e.g., set via `esxcli` and persisted outside normal config) or require a reboot to fully apply the profile.

---

## 5. Host Profiles vs vLCM

In vSphere 7.0 and later, clusters can be managed by vSphere Lifecycle Manager (vLCM) with cluster images instead of host profiles for patch management. The two systems are mutually exclusive per cluster.

```text
vLCM manages:    ESXi image (VIBs, firmware), patch level, driver versions
Host profiles manage: network configuration, security, NTP, storage adapters, SNMP

If using vLCM:
  - The vLCM cluster image handles ESXi software compliance
  - Host profiles can still be applied alongside vLCM for configuration (non-image) settings
  - Or use vLCM Host Configuration (vSphere 8+) as a full replacement for host profiles
```

---

## Key Terms

| Term | Definition |
|---|---|
| Host profile | A vCenter object that captures the desired configuration state of an ESXi host; applied to one or more hosts as the compliance baseline |
| Reference host | The ESXi host from which the host profile was originally extracted; used to update the profile when the desired state changes |
| Compliance check | vCenter operation that compares each host's current configuration against the host profile and reports any divergence |
| Remediation | The process of applying a host profile to a non-compliant host to bring its configuration back into alignment with the profile |
| Non-compliant | Host profile compliance state indicating that one or more settings on the host differ from the profile value |
| vLCM | vSphere Lifecycle Manager; manages ESXi software (patches, VIBs, firmware) using cluster images; separate from host profile configuration management |
| Lockdown mode | ESXi security setting enforced by host profiles that restricts direct host access; Normal allows DCUI, Strict disables all local access |
| Profile answer file | Per-host data stored alongside a host profile that captures settings which differ between hosts (e.g., management IP, hostname); required for stateless ESXi deployments |

---

## Common Mistakes

- **Applying the profile without checking whether a reboot is required.** Some kernel parameter changes require a host reboot. Applying without warning will trigger unexpected maintenance mode and VM evacuations during production hours.
- **Updating the profile from the wrong reference host.** If a host had an accidental change and you update the profile from it, you bake the mistake into the profile and all other hosts will become compliant with the wrong configuration.
- **Using host profiles and vLCM image management together incorrectly.** In vSphere 7+, enabling vLCM image management on a cluster automatically disables the ability to use host profiles for software management. Configuration-only host profiles can still apply, but the two systems must not be confused.
- **Ignoring drift in development clusters.** Non-compliant development hosts often carry temporary configuration changes that get forgotten. These accumulate and make production drift harder to identify.

---

## Related Scenarios

- [Host Maintenance and Patching](host-maintenance-patching.md) — patching frequently introduces host profile drift; check compliance after every patch cycle.
- [ESXi Host Disconnected](esxi-host-disconnected.md) — a host that disconnected from vCenter may have stale configuration that shows as drift after reconnection.
- [NTP Drift / SSO Certificate Errors](ntp-drift-sso-certificate.md) — NTP configuration drift in host profiles is a common trigger for SSO and certificate failures.
