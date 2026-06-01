# PowerPath — Troubleshooting

<div class="kb-summary">
PowerPath — Troubleshooting navigation for Common Issues, Diagnostics, Escalation.
</div>

```
┌─────────────────────────────────── Dell PowerPath Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Common issues: dead paths, LUN not visible, registration failure, I/O imbalance        │   │
│   │        Dead path: check HBA port state, SAN zone, and array FA port; remove then rescan       │   │
│   │         LUN missing: verify masking view at array; rescan after masking; powermt check        │   │
│   │      Registration: expired or wrong host ID; re-register with valid key from Dell portal      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom reported → powermt display → identify affected path/device → trace to root cause           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Path Issues         │  │         LUN / Device        │  │         Registration        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        All paths dead       │  │       LUN not visible       │  │       License expired       │   │
│   │       Single path dead      │  │          Ghost path         │  │        Wrong host ID        │   │
│   │        Path imbalance       │  │       Masking missing       │  │       Key file missing      │   │
│   │           Slow I/O          │  │       Wrong emulation       │  │       Portal mismatch       │   │
│   │        Trespass loop        │  │        Rescan needed        │  │         Re-register         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    powermt display → check dead path layer (HBA / fabric / array) → fix at source → verify            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │      Command      │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  All paths dead  │  HBA port state  │  powermt display  │   Fix HBA/zone   │ Array port down  │   │
│   │   LUN missing    │  Array masking   │   powermt check   │   Fix masking    │ Rescan no result │   │
│   │  I/O imbalance   │   Policy check   │  powermt display  │    Set policy    │  Persists after  │   │
│   │   Reg. failure   │   Key validity   │   check_registr.  │   Re-register    │   Key rejected   │   │
│                                                                                                       │
│    Physical: check HBA port LED, SAN switch port counters, array FA port LEDs for dead path           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    All paths dead = No active path to device; I/O queued or returned error to host OS                 │
│    Trespass loop  = Active/passive array SP ownership conflict; path oscillates between SPs           │
│    Ghost path     = Dead path entry for LUN that was unmapped; powermt remove to clean up             │
│    Wrong emulation= Device assigned wrong array class; set correct emulation with powermt config      │
│    I/O imbalance  = Most I/O on one path; caused by Basic policy or sticky preferred path             │
│    check_registr. = powermt check_registration; validates license key is active on this host          │
│    Re-register    = powermt remove license + powermt check_registration with new key                  │
│    Rescan         = Host OS HBA rescan after masking change; picks up new or removed LUNs             │
│    Portal mismatch= Dell portal shows key assigned to different host ID; contact Dell licensing       │
│    Path imbalance = powermt set policy=adaptive dev=all to re-enable load balancing                   │
│    FA port LED    = Array Front-End director port indicator; dark/amber = fault in path               │
│    HBA port state = fcinfo hba-port (Solaris), systool (Linux), Get-InitiatorPort (Windows)           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell
┌─────────────────────────────────── Dell PowerPath Troubleshooting ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Common issues: dead paths, LUN not visible, registration failure, I/O imbalance        │   │
│   │        Dead path: check HBA port state, SAN zone, and array FA port; remove then rescan       │   │
│   │         LUN missing: verify masking view at array; rescan after masking; powermt check        │   │
│   │      Registration: expired or wrong host ID; re-register with valid key from Dell portal      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Symptom reported → powermt display → identify affected path/device → trace to root cause           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Path Issues         │  │         LUN / Device        │  │         Registration        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        All paths dead       │  │       LUN not visible       │  │       License expired       │   │
│   │       Single path dead      │  │          Ghost path         │  │        Wrong host ID        │   │
│   │        Path imbalance       │  │       Masking missing       │  │       Key file missing      │   │
│   │           Slow I/O          │  │       Wrong emulation       │  │       Portal mismatch       │   │
│   │        Trespass loop        │  │        Rescan needed        │  │         Re-register         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    powermt display → check dead path layer (HBA / fabric / array) → fix at source → verify            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Symptom      │   First check    │      Command      │       Fix        │   Escalate if    │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │  All paths dead  │  HBA port state  │  powermt display  │   Fix HBA/zone   │ Array port down  │   │
│   │   LUN missing    │  Array masking   │   powermt check   │   Fix masking    │ Rescan no result │   │
│   │  I/O imbalance   │   Policy check   │  powermt display  │    Set policy    │  Persists after  │   │
│   │   Reg. failure   │   Key validity   │   check_registr.  │   Re-register    │   Key rejected   │   │
│                                                                                                       │
│    Physical: check HBA port LED, SAN switch port counters, array FA port LEDs for dead path           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    All paths dead = No active path to device; I/O queued or returned error to host OS                 │
│    Trespass loop  = Active/passive array SP ownership conflict; path oscillates between SPs           │
│    Ghost path     = Dead path entry for LUN that was unmapped; powermt remove to clean up             │
│    Wrong emulation= Device assigned wrong array class; set correct emulation with powermt config      │
│    I/O imbalance  = Most I/O on one path; caused by Basic policy or sticky preferred path             │
│    check_registr. = powermt check_registration; validates license key is active on this host          │
│    Re-register    = powermt remove license + powermt check_registration with new key                  │
│    Rescan         = Host OS HBA rescan after masking change; picks up new or removed LUNs             │
│    Portal mismatch= Dell portal shows key assigned to different host ID; contact Dell licensing       │
│    Path imbalance = powermt set policy=adaptive dev=all to re-enable load balancing                   │
│    FA port LED    = Array Front-End director port indicator; dark/amber = fault in path               │
│    HBA port state = fcinfo hba-port (Solaris), systool (Linux), Get-InitiatorPort (Windows)           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="diagnostics/"><strong>Diagnostics</strong><span>Diagnostic procedures and log analysis.</span></a>
<a class="kb-card" href="escalation/"><strong>Escalation</strong><span>Vendor escalation procedures and support contacts.</span></a>
</div>
