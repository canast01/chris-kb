# vSAN Degraded Object Runbook


<div class="kb-summary">
vSAN Degraded Object Runbook reference covering Confirm vSAN Health State, Identify Affected Objects, Check Failed Disks, Check Host Availability, Check Resync Status and 5 more sections.
</div>

```text
┌──────────────────────────────────── vSAN Snapshot Cleanup Runbook ────────────────────────────────────┐
│                                                                                                       │
│    Identify degraded vSAN objects; check disks and hosts; restore or rebuild                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Step       │      Action      │       Check       │     On FAIL      │       Tool       │   │
│   │  ──────────────  │  ──────────────  │  ───────────────  │  ──────────────  │  ──────────────  │   │
│   │  1  vSAN health  │   Open Skyline   │   No red checks   │  Note failures   │    vCenter UI    │   │
│   │    2  Objects    │ Virtual Objects  │   Degraded list   │  Note VM names   │    vCenter UI    │   │
│   │  3  Disk check   │  Physical Disk   │  No failed disks  │   Replace disk   │    iDRAC / UI    │   │
│   │  4  Host check   │   Host status    │   All connected   │  Rejoin cluster  │    vCenter UI    │   │
│   │    5  Rebuild    │  Policy repair   │  Objects rebuild  │ Escalate VMware  │    vCenter UI    │   │
│   │    6  Verify     │  Skyline green   │  No degraded obj  │   Re-run steps   │    vCenter UI    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Skyline Health = vSAN built-in health checks UI; vCenter → Cluster → vSAN → Skyline                │
│    Degraded obj   = vSAN object with fewer mirrors than the storage policy requires                   │
│    Non-compliant  = vSAN object exists but does not meet current storage policy                       │
│    Absent         = vSAN object has no accessible components; VM may be impacted                      │
│    Policy repair  = vSAN automatically rebuilds objects after a host or disk returns                  │
│    FTT            = Failures To Tolerate; storage policy setting; FTT=1 needs 3 hosts min             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Confirm vSAN Health State

- Open vCenter → Cluster → vSAN → Skyline Health
- Identify which health checks are failing
- Open Virtual Objects view and filter by Degraded, Non-compliant, or Absent

## Identify Affected Objects

- Note the VM name, object type, and storage policy for each affected object
- Check if the VM is still running or if it has failed

## Check Failed Disks

- Review Skyline Health → Physical Disk section
- Check iDRAC for disk health on all VxRail nodes

## Check Host Availability

- Confirm all hosts are Connected in vCenter
- Check if any host is in maintenance mode unexpectedly

## Check Resync Status

```bash
esxcli vsan debug resync summary get
```

Active resync is expected after a host returns from maintenance — wait for it to complete before taking further action.

## Check Capacity

- Confirm vSAN usable capacity is within safe limits
- If capacity is the cause of non-compliance, expansion may be needed

## Review Storage Policy

- Confirm the storage policy assigned to affected objects is achievable with current cluster state
- If FTT=1 and only one host or disk is available, the policy cannot be met

## Avoid Unsafe Actions

- Do not take additional hosts into maintenance mode while objects are degraded
- Do not delete VMs or disks without VMware support guidance

## Engage VMware Support

- Collect a vSAN support bundle if objects remain degraded after the expected recovery period
- Open a VMware support case and provide the bundle, timeline, and Skyline Health screenshots

## Validate Object Compliance After Recovery

- Return to Virtual Objects view and confirm all objects are Healthy
- Run Skyline Health and confirm no remaining failures
