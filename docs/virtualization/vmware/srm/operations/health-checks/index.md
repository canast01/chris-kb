# SRM — Health Checks

```
  Health Check Chain
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│  Site Pairing    │    │  Protection      │    │  Recovery Plan   │
│  (Connected?)    │───►│  Groups (OK?)    │───►│  Pre-check       │
│                  │    │  ┌────────────┐  │    │  (no errors)     │
└──────────────────┘    │  │ RPO within │  │    └──────────────────┘
                        │  │ target?    │  │
                        │  │ Placeholder│  │    ┌──────────────────┐
                        │  │ VMs exist? │  │    │  SRA / Array     │
                        │  └────────────┘  │    │  Pair healthy?   │
                        └──────────────────┘    │  Last discovery  │
                                                │  recent?         │
                                                └──────────────────┘
```

---

## Site Pairing Status

```
vCenter (Protected Site) → Site Recovery → Summary
  Site Pairing: should show "Connected" to recovery site
  SRM Server status: "Running" on both sites
```

If site pairing shows error:
```powershell
# Check SRM service health
Get-Service -ComputerName srm-protected.corp.local -Name "VMware vCenter Site Recovery Manager"
Get-Service -ComputerName srm-recovery.corp.local -Name "VMware vCenter Site Recovery Manager"
```

---

## Protection Group Health

```
Site Recovery → Protection → Protection Groups
  All groups should show Status: OK
  Any warning or error: click group → View issues
```

```powershell
# PowerCLI: check all protection group states
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $info = $srm.ExtensionData.Protection.QueryProtectionGroupState($pg)
    if ($info.State -ne "OK") {
        Write-Warning "PG $($pg.Name): $($info.State)"
    }
}
```

---

## RPO Compliance Check

All protected VMs must be within their configured RPO. VMs outside RPO appear in amber/red:

```
Site Recovery → Replication → vSphere Replication
  Filter by: RPO violation
  Any VMs shown: investigate immediately — replication is lagging

Site Recovery → Protection → Protection Groups → [group] → VMs
  Check "Last Sync" column against RPO setting
```

```powershell
# Check VM replication lag vs configured RPO
$pgs = $srm.ExtensionData.Protection.ListProtectionGroups()
foreach ($pg in $pgs) {
    $vms = $srm.ExtensionData.Protection.ListProtectedVms($pg)
    foreach ($vm in $vms) {
        $state = $vm.ReplicationState
        if ($state -and $state -ne "OK") {
            Write-Warning "$($vm.Vm.Name): replication state = $state"
        }
    }
}
```

---

## SRA Status (Array-Based Replication)

```
Site Recovery → Storage → Array Pairs
  All array pairs should show: Enabled, Healthy
  Last discovery: recent timestamp

# If SRA shows error:
# Site Recovery → Storage → Array Pairs → [pair] → Discover Devices
# This re-runs the SRA discovery against the storage array
```

---

## Placeholder VMs at Recovery Site

Placeholder VMs must exist at the recovery site for each protected VM:

```
vCenter (Recovery Site) → VMs and Templates
  Look for VMs with names matching protected VMs — these are placeholder VMs
  They appear as "shadow" VMs with minimal resources

# Placeholder VMs missing = protection group needs reconfiguration
# Site Recovery → Protection → [PG] → Configure → Reconfigure
```

---

## Recovery Plan Pre-Check

Run the built-in pre-check before any recovery:

```
Site Recovery → Recovery Plans → [plan] → Test or Recover
  Step 1: Run validation checks (pre-check)
  Verify: no errors before proceeding
  Common warnings: network mapping not set, no IP customization defined
```

---

## Certificate Expiry

```bash
# Check SRM Server certificate
echo | openssl s_client -connect srm-protected.corp.local:443 2>/dev/null \
  | openssl x509 -noout -dates

echo | openssl s_client -connect srm-recovery.corp.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check vSphere Replication appliance cert
echo | openssl s_client -connect vra-protected.corp.local:443 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Monthly Test Recovery Verification

Run a test failover monthly on at least one non-critical Recovery Plan:

```
Site Recovery → Recovery Plans → [test-plan] → Test
  Mode: Test
  Network: isolated (do not connect test VMs to production network)

After test:
  Verify: all VMs powered on in isolated network
  Check: IP addresses correct per IP customization rules
  Check: application-level connectivity within isolated network (ping, service check)

Cleanup:
  Site Recovery → Recovery Plans → [test-plan] → Cleanup
```

Document test results and any issues found. Track trend of test durations — increasing duration indicates scaling issues.
