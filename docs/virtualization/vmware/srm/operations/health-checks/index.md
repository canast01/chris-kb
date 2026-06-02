# SRM — Health Checks


<div class="kb-summary">
Health Checks reference covering Protection Group Health, RPO Compliance Check, SRA Status (Array-Based Replication), Placeholder VMs at Recovery Site, Recovery Plan Pre-Check and 2 more sections.
</div>

  Health Check Chain
                        │  │ target?    │  │
                        │  │ Placeholder│  │    ┌──────────────────┐
                        │  │ VMs exist? │  │    │  SRA / Array     │
                        │  └────────────┘  │    │  Pair healthy?   │
                        └──────────────────┘    │  Last discovery  │
                                                │  recent?         │
                                                └──────────────────┘
```text
┌───────────────────────────────────── VMware SRM — Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│  SRM health checks verify site pair connectivity, replication status, plan test                       │
│  compliance, and protection group coverage across all protected VMs.                                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Site Pair Health               │  │              Replication Health             │   │
│   │         Site pair: Connected status          │  │             All VMs: replicating            │   │
│   │          Both SRM servers: running           │  │             No replication error            │   │
│   │        vCenter: reachable both sites         │  │            RPO met: within target           │   │
│   │          Datastore mappings: valid           │  │            Lag: within acceptable           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Site pair connectivity and replication status are the primary daily health checks.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Plan Compliance                │  │                Coverage Audit               │   │
│   │           Last test: <90 days ago            │  │          All critical VMs protected         │   │
│   │          RTO achieved in last test           │  │          Protection groups: no VMs          │   │
│   │            Plan valid: no errors             │  │          Network mappings: complete         │   │
│   │         Cleanup: completed post-test         │  │            IP rules: all defined            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  WAN link quality affects replication health; monitor replication lag on slow links;                  │
│  storage arrays report replication status to SRA.                                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Site pair     = bidirectional link between two SRM Servers                                           │
│  RPO met       = replication lag < configured RPO for each VM                                         │
│  Last test     = date of most recent successful recovery plan test                                    │
│  90-day SLA    = common DR test compliance requirement                                                │
│  RTO achieved  = actual recovery time met target RTO in test                                          │
│  Plan valid    = no VM, mapping, or datastore errors in plan                                          │
│  Cleanup       = SRM removes test VMs after successful test                                           │
│  Protection group= all VMs that should be protected                                                   │
│  Network mapping= required for VMs to connect post-failover                                           │
│  IP rules      = IP customisation for re-IP on failover                                               │
│  Replication lag= seconds since last sync; must be < RPO target                                       │
│  Datastore map = recovery datastore for each protected datastore                                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

```text
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

```bash
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

```bash
vCenter (Recovery Site) → VMs and Templates
  Look for VMs with names matching protected VMs — these are placeholder VMs
  They appear as "shadow" VMs with minimal resources

# Placeholder VMs missing = protection group needs reconfiguration
# Site Recovery → Protection → [PG] → Configure → Reconfigure
```

---

## Recovery Plan Pre-Check

Run the built-in pre-check before any recovery:

```text
Site Recovery → Recovery Plans → [plan] → Test or Recover
  Step 1: Run validation checks (pre-check)
  Verify: no errors before proceeding
  Common warnings: network mapping not set, no IP customization defined
```

---

## Certificate Expiry

```bash
# Check SRM Server certificate
echo | openssl s_client -connect srm-protected.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates

echo | openssl s_client -connect srm-recovery.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates

# Check vSphere Replication appliance cert
echo | openssl s_client -connect vra-protected.example.local:443 2>/dev/null \
  | openssl x509 -noout -dates
```

---

## Monthly Test Recovery Verification

Run a test failover monthly on at least one non-critical Recovery Plan:

```yaml
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
