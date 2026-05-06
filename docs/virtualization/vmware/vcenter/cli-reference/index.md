# vCenter CLI Reference (PowerCLI & DCLI)

Commonly used PowerCLI and vCenter shell commands for managing vSphere environments.

> Requires VMware.PowerCLI module. Use `Connect-VIServer -Server <vcenter>` before running PowerCLI commands.

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="connection/">
  <strong>Connection & Session</strong>
  <span>Install PowerCLI, Connect-VIServer, Disconnect-VIServer, and session info.</span>
</a>

<a class="kb-card" href="hosts/">
  <strong>Hosts</strong>
  <span>List, select, details, maintenance mode, services, NTP, and syslog.</span>
</a>

<a class="kb-card" href="clusters/">
  <strong>Clusters</strong>
  <span>Get-Cluster, HA/DRS info, host list per cluster, and New-Cluster.</span>
</a>

<a class="kb-card" href="vms/">
  <strong>Virtual Machines</strong>
  <span>List, power ops, config (CPU/RAM), move, clone, and guest OS info.</span>
</a>

<a class="kb-card" href="snapshots/">
  <strong>Snapshots</strong>
  <span>Get/New/Remove-Snapshot and revert with Set-VM.</span>
</a>

<a class="kb-card" href="datastores/">
  <strong>Datastores</strong>
  <span>List with capacity/usage, threshold filter, and datastore clusters.</span>
</a>

<a class="kb-card" href="networks/">
  <strong>Networks</strong>
  <span>Standard/distributed switches, port groups, and VMkernel adapters.</span>
</a>

<a class="kb-card" href="alarms/">
  <strong>Alarms & Events</strong>
  <span>Get-AlarmDefinition, triggered alarms, Get-VIEvent with filters.</span>
</a>

<a class="kb-card" href="permissions/">
  <strong>Permissions & Roles</strong>
  <span>Get-VIRole, Get-VIPermission, and New-VIPermission assignment.</span>
</a>

<a class="kb-card" href="inventory/">
  <strong>Inventory & Reporting</strong>
  <span>Export VM and host inventory to CSV with custom calculated fields.</span>
</a>

<a class="kb-card" href="appliance/">
  <strong>vCenter Appliance (SSH)</strong>
  <span>service-control, VCSA disk usage, logs, SSO identity, and cert check.</span>
</a>

</div>
