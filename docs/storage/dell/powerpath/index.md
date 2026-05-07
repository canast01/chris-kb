# Dell PowerPath

<div class="kb-grid kb-grid-12">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>HA topology, components, connectivity, and sizing.</span>
</a>

<a class="kb-card" href="standards/">
  <strong>Standards</strong>
  <span>Naming conventions, build baseline, and configuration checklist.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Command reference by category with syntax and examples.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for daily checks, health, incident triage, and validation.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic commands, log locations, and error codes.</span>
</a>

<a class="kb-card" href="integration/">
  <strong>Integration</strong>
  <span>VMware, backup tools, monitoring, authentication, and API integration.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span>
</a>

<a class="kb-card" href="vendor-support/">
  <strong>Vendor Support</strong>
  <span>Opening a case, information to collect, support portal, and SLA tiers.</span>
</a>


<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Health check procedures and validation steps.</span>
</a>

<a class="kb-card" href="host-validation/">
  <strong>Host Validation</strong>
  <span>Host Validation notes, checks, commands, and references.</span>
</a>
</div>

## Overview

Dell PowerPath is host-based multipath I/O software that manages multiple physical paths between a host and storage arrays from Dell/EMC, providing automatic path failover and dynamic load balancing. It runs on Linux, Windows, AIX, HP-UX, and Solaris, and is controlled via the `powermt` CLI. PowerPath presents a single pseudo device per LUN to the OS, abstracting the underlying physical paths.

## Where It Fits

- Hosts connected to Dell/EMC arrays (PowerMax, VMAX, Unity, PowerStore) over Fibre Channel or iSCSI
- Production environments requiring automatic path failover without host-side intervention
- Performance-sensitive workloads that benefit from intelligent load balancing across multiple HBA paths
- Environments with zoning changes or fabric maintenance where path counts change dynamically
- Any host where native OS multipath (DM-Multipath) is being replaced or supplemented with a vendor-managed solution

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Run `powermt display dev=all` and scan for paths in `dead` or `unlic` | `powermt display dev=all` |  |
| Verify all pseudo devices show the expected number of active paths |  |  |
| Check that load balancing policy is set to CLAROpt (not RoundRobin or |  |  |
| Confirm `powermt check_registration` shows a valid, non-expired licens | `powermt check_registration` |  |
| Review OS system logs (`/var/log/messages` on Linux) for HBA or path e | `/var/log/messages` |  |
| After any fabric or zoning change, recount paths per device and compar |  |  |
| Verify `powermt display ports class=all` shows all HBA ports in an `al | `powermt display ports class=all` |  |

## Health Commands

~~~bash
# Display all PowerPath managed devices and their path states
powermt display dev=all

# Display all HBA port states
powermt display ports class=all

# Show current load balancing policy and PowerPath options
powermt display options

# Check PowerPath license registration status
powermt check_registration

# Show installed PowerPath version
powermt version

# Test and restore all paths (marks dead paths for retry)
powermt restore
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Path shown as `dead` in `powermt display dev=all` | FC cable/SFP failure, switch port error, or zoning misconfiguration | Check fabric switch logs and HBA port state; run `powermt restore` after fix |
| Devices showing as `pseudo` with no paths | LUN not presented to host, or `powermt config` not run after new LUN mapping | Verify LUN masking at array; run `powermt config` to discover new devices |
| Policy shown as `BasicFailover` instead of CLAROpt | License expired or not properly applied | Run `powermt check_registration`; reapply license and run `powermt config` |
| Path state `unlic` | License missing or configured after LUN was already under PowerPath management | Confirm license with `powermt check_registration`; rerun `powermt config` |
| Path thrashing (intermittent dead/alive cycling) | Flapping SFP, marginal FC cable, or oversubscribed switch port | Inspect physical layer; check switch error counters; replace suspect hardware |
| Configuration lost after reboot | `powermt save` was not run after last policy or path change | Always run `powermt save` after any configuration change to persist settings |

## Operational Tasks


| Task | Command |
|---|---|
| After any LUN is added or removed, run `powermt config` followed by `powermt dis |  |
| Change load balancing policy with `powermt set policy=CLAROpt class=all` and per | `powermt save` |
| After fabric maintenance or zoning changes, run `powermt restore` to bring dead |  |
| Verify path counts per device against site baseline documentation after any SAN |  |
| Check registration and license validity with `powermt check_registration` after |  |
| Use `powermt display dev=<device>` to investigate a specific pseudo device in de |  |
| Decommission a device cleanly by removing LUN masking at the array, then running | `powermt remove dev=<device>` |

## Upgrade Notes


| Step | Action |
|---|---|
| 1 | Record the current state before upgrade: run `powermt display dev=all` and `powermt display options` and save the output |
| 2 | Confirm OS and kernel version compatibility against the Dell PowerPath support matrix for the target version |
| 3 | Run `powermt save` to persist current configuration so it can be restored if the upgrade needs to be rolled back |
| 4 | Stop applications or quiesce I/O if the upgrade requires unloading the PowerPath kernel module (check release notes) |
| 5 | Install the new PowerPath package using the OS package manager (e.g., `rpm -Uvh` on RHEL/SLES) |
| 6 | After installation, run `powermt check_registration` to confirm the license is recognised under the new version |
| 7 | Run `powermt display dev=all` and compare path counts and policy against the pre-upgrade baseline; run `powermt restore` if any paths are in `dead` state |

## Best Practices

- Always use the CLAROpt (`co`) policy for Dell/EMC CLARiiON, Unity, and mid-range arrays — do not use RoundRobin, which ignores array-side optimisation
- Run `powermt save` immediately after every policy change, path addition, or `powermt config` operation to ensure settings persist across reboots
- Maintain a documented baseline of expected path counts per host and device; compare after every fabric or zoning change
- Run `powermt check_registration` after any OS upgrade or kernel update to confirm the license is still valid
- After any fabric change, run `powermt restore` before checking path state — this instructs PowerPath to retry paths marked dead
- Do not mix PowerPath and DM-Multipath managing the same devices on the same host; disable DM-Multipath for devices managed by PowerPath
- Review the Dell PowerPath release notes and support matrix before any kernel or OS upgrade to confirm compatibility
