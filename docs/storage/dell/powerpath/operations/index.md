# PowerPath — Operations


```text
┌────────────────────────────────────── Dell PowerPath Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Day-2 operations: path monitoring, dead path investigation, policy tuning, registration    │   │
│   │       powermt display: shows all multipath devices, path states, active I/O distribution      │   │
│   │     Policy changes: powermt set policy=X dev=all; save immediately after with powermt save    │   │
│   │     Registration: powermt check_registration; license tied to host; re-register on rebuild    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check path state → investigate dead paths → adjust policy → save config → verify distribution      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Path Monitoring       │  │      Policy Management      │  │       License / Config      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       powermt display       │  │         powermt set         │  │      check_registration     │   │
│   │       Dead path check       │  │      Per-device policy      │  │         powermt save        │   │
│   │      Path count verify      │  │       powermt restore       │  │       powermt restore       │   │
│   │       I/O distribution      │  │        Policy verify        │  │        License renew        │   │
│   │        powermt check        │  │       Reset to default      │  │       Emulation audit       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    powermt display → identify dead paths → resolve root cause → verify path recovery                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │     Command      │  Output / Action  │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Path check    │ powermt display  │  Path state list  │      Daily       │ Check dead paths │   │
│   │    Policy set    │   powermt set    │   Policy applied  │    On change     │  Save after set  │   │
│   │   Registration   │  check_registr.  │   License valid   │    On install    │  Bound to host   │   │
│   │   Config save    │   powermt save   │  Persists config  │ After any change │ Survives reboot  │   │
│                                                                                                       │
│    Physical: paths shown as hdiskX (AIX), sdX (Linux), or disk# (Windows) in powermt output           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    powermt display= List all PowerPath devices with path health and I/O distribution per path         │
│    Dead path      = Path that failed I/O; shown as Dead in powermt output; polled for recovery        │
│    powermt set    = Change path policy: powermt set policy=adaptive dev=all class=emc_symm            │
│    powermt save   = Write config to /etc/powermt.custom; must run after every policy change           │
│    powermt restore= Apply config from /etc/powermt.custom; run manually or at boot via init           │
│    powermt check  = Verify PowerPath sees all expected paths; report any discrepancies                │
│    check_registration= Validate license key registration on the host (powermt check_registration)     │
│    Emulation      = Array class (emc_symm, emc_clariion, etc.) assigned to each device                │
│    I/O distribution= Per-path I/O count shown by powermt; should be roughly balanced for LB           │
│    Path recovery  = PowerPath re-enables dead path after successful I/O probe to the array port       │
│    powermt.custom = Config file persisted by powermt save; read at boot by powermt restore            │
│    License renew  = Obtain new key from Dell licensing portal; powermt remove + re-register           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Dell PowerPath Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Day-2 operations: path monitoring, dead path investigation, policy tuning, registration    │   │
│   │       powermt display: shows all multipath devices, path states, active I/O distribution      │   │
│   │     Policy changes: powermt set policy=X dev=all; save immediately after with powermt save    │   │
│   │     Registration: powermt check_registration; license tied to host; re-register on rebuild    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check path state → investigate dead paths → adjust policy → save config → verify distribution      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Path Monitoring       │  │      Policy Management      │  │       License / Config      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       powermt display       │  │         powermt set         │  │      check_registration     │   │
│   │       Dead path check       │  │      Per-device policy      │  │         powermt save        │   │
│   │      Path count verify      │  │       powermt restore       │  │       powermt restore       │   │
│   │       I/O distribution      │  │        Policy verify        │  │        License renew        │   │
│   │        powermt check        │  │       Reset to default      │  │       Emulation audit       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    powermt display → identify dead paths → resolve root cause → verify path recovery                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │     Command      │  Output / Action  │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Path check    │ powermt display  │  Path state list  │      Daily       │ Check dead paths │   │
│   │    Policy set    │   powermt set    │   Policy applied  │    On change     │  Save after set  │   │
│   │   Registration   │  check_registr.  │   License valid   │    On install    │  Bound to host   │   │
│   │   Config save    │   powermt save   │  Persists config  │ After any change │ Survives reboot  │   │
│                                                                                                       │
│    Physical: paths shown as hdiskX (AIX), sdX (Linux), or disk# (Windows) in powermt output           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    powermt display= List all PowerPath devices with path health and I/O distribution per path         │
│    Dead path      = Path that failed I/O; shown as Dead in powermt output; polled for recovery        │
│    powermt set    = Change path policy: powermt set policy=adaptive dev=all class=emc_symm            │
│    powermt save   = Write config to /etc/powermt.custom; must run after every policy change           │
│    powermt restore= Apply config from /etc/powermt.custom; run manually or at boot via init           │
│    powermt check  = Verify PowerPath sees all expected paths; report any discrepancies                │
│    check_registration= Validate license key registration on the host (powermt check_registration)     │
│    Emulation      = Array class (emc_symm, emc_clariion, etc.) assigned to each device                │
│    I/O distribution= Per-path I/O count shown by powermt; should be roughly balanced for LB           │
│    Path recovery  = PowerPath re-enables dead path after successful I/O probe to the array port       │
│    powermt.custom = Config file persisted by powermt save; read at boot by powermt restore            │
│    License renew  = Obtain new key from Dell licensing portal; powermt remove + re-register           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌────────────────────────────────────── Dell PowerPath Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Day-2 operations: path monitoring, dead path investigation, policy tuning, registration    │   │
│   │       powermt display: shows all multipath devices, path states, active I/O distribution      │   │
│   │     Policy changes: powermt set policy=X dev=all; save immediately after with powermt save    │   │
│   │     Registration: powermt check_registration; license tied to host; re-register on rebuild    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check path state → investigate dead paths → adjust policy → save config → verify distribution      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Path Monitoring       │  │      Policy Management      │  │       License / Config      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       powermt display       │  │         powermt set         │  │      check_registration     │   │
│   │       Dead path check       │  │      Per-device policy      │  │         powermt save        │   │
│   │      Path count verify      │  │       powermt restore       │  │       powermt restore       │   │
│   │       I/O distribution      │  │        Policy verify        │  │        License renew        │   │
│   │        powermt check        │  │       Reset to default      │  │       Emulation audit       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    powermt display → identify dead paths → resolve root cause → verify path recovery                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │     Command      │  Output / Action  │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Path check    │ powermt display  │  Path state list  │      Daily       │ Check dead paths │   │
│   │    Policy set    │   powermt set    │   Policy applied  │    On change     │  Save after set  │   │
│   │   Registration   │  check_registr.  │   License valid   │    On install    │  Bound to host   │   │
│   │   Config save    │   powermt save   │  Persists config  │ After any change │ Survives reboot  │   │
│                                                                                                       │
│    Physical: paths shown as hdiskX (AIX), sdX (Linux), or disk# (Windows) in powermt output           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    powermt display= List all PowerPath devices with path health and I/O distribution per path         │
│    Dead path      = Path that failed I/O; shown as Dead in powermt output; polled for recovery        │
│    powermt set    = Change path policy: powermt set policy=adaptive dev=all class=emc_symm            │
│    powermt save   = Write config to /etc/powermt.custom; must run after every policy change           │
│    powermt restore= Apply config from /etc/powermt.custom; run manually or at boot via init           │
│    powermt check  = Verify PowerPath sees all expected paths; report any discrepancies                │
│    check_registration= Validate license key registration on the host (powermt check_registration)     │
│    Emulation      = Array class (emc_symm, emc_clariion, etc.) assigned to each device                │
│    I/O distribution= Per-path I/O count shown by powermt; should be roughly balanced for LB           │
│    Path recovery  = PowerPath re-enables dead path after successful I/O probe to the array port       │
│    powermt.custom = Config file persisted by powermt save; read at boot by powermt restore            │
│    License renew  = Obtain new key from Dell licensing portal; powermt remove + re-register           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>
