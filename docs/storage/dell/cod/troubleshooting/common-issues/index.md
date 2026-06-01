# COD — Common Issues


<div class="kb-summary">
COD — Common Issues reference.
</div>

```
┌────────────────────────────────────── Dell CoD — Common Issues ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Common CoD issues: key rejection, capacity not visible after apply, alert misconfiguration  │   │
│   │     Key rejection: most common cause is SN mismatch; verify via array GUI or chassis label    │   │
│   │  Capacity not visible: check firmware version compatibility; may require array upgrade first  │   │
│   │  Alert issues: CloudIQ threshold misconfigured; ops team not notified until capacity critical │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key rejected → verify SN → re-download key → apply corrected key → confirm capacity shown          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Key Problems        │  │      Capacity Problems      │  │        Alert Problems       │   │
│   │         SN mismatch         │  │         Not visible         │  │       Wrong threshold       │   │
│   │       Corrupt download      │  │         Old firmware        │  │     Alert to wrong team     │   │
│   │       Wrong key scope       │  │        Partial unlock       │  │       No email config       │   │
│   │       Already applied       │  │          Wrong pool         │  │       Webhook missing       │   │
│   │       Account mismatch      │  │       License conflict      │  │         Stale alert         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Check array event log and CloudIQ alert history for timestamps and error message detail            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Issue       │    Root Cause    │     Diagnostic    │    Resolution    │    Prevention    │   │
│   │   Key rejected   │   SN mismatch    │    Array GUI SN   │   Re-download    │Confirm SN pre-buy│   │
│   │   No capacity    │   Old firmware   │     FW version    │  Upgrade array   │Check compat first│   │
│   │     No alert     │  Bad threshold   │   CloudIQ policy  │  Fix threshold   │  Review monthly  │   │
│   │  Key duplicate   │ Already applied  │  License history  │   Contact Dell   │  Track in CMDB   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: always confirm array SN from chassis label, not documentation which may be outdated      │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SN mismatch    = Key file SN vs array SN differ; most common CoD failure; re-download correct key  │
│    Corrupt download = Key file incomplete; browser or network issue; always re-download over HTTPS    │
│    Wrong key scope = Key unlocks different pool or capacity tier than intended; verify before purchase│
│    Already applied = Key was previously used; array shows duplicate; contact Dell licensing team      │
│    Account mismatch = Key purchased under different Dell account than managing the array              │
│    Old firmware   = Array firmware below minimum required for CoD key; upgrade before applying key    │
│    Partial unlock = Key scope smaller than expected; array unlocks only a subset of purchased capacity│
│    Wrong pool     = Key targets a different pool; check key details in licensing portal before import │
│    License conflict = Two keys active for same pool; contact Dell TAC; do not apply additional keys   │
│    Wrong threshold = CloudIQ alert threshold set too high; team not alerted until critically low      │
│    Stale alert    = Alert fires for old condition already resolved; acknowledge and review policy     │
│    Webhook missing = CloudIQ webhook to ITSM not configured; alerts go to email only or nowhere       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [COD](../../index.md) reference.

---

| Symptom | Likely Cause | First Action |
|---|---|---|
| COD license not activating | Wrong SID in license file; license already consumed; SYMCLI version mismatch | Verify SID: `symcfg -sid <SID> show`; check `symlicense -sid <SID> list` for existing licenses |
| Capacity shows as unavailable after license applied | Array still binding new devices; may take several minutes | Wait 5–10 minutes; run `symcfg discover`; check Unisphere for device enumeration progress |
| `symlicense install` fails with permission error | Solutions Enabler running under user without SYMCLI admin rights | Run as root or with an account holding StorageAdmin role in Unisphere |
| COD drives not visible after activation | Firmware needs to enumerate new devices; requires `symcfg discover` | `symcfg -sid <SID> discover` — triggers device rediscovery; check Unisphere for newly available devices |
| License key rejected (wrong SID) | License file was issued for a different array SID | Contact Dell License Management portal or account team for re-issuance to correct SID |
| Capacity available in SYMCLI but not usable in Unisphere | New devices not yet bound to a thin pool | Add newly discovered devices to the appropriate thin pool via Unisphere or SYMCLI |
| CloudIQ shows COD headroom as 0 but license portal shows available | CloudIQ telemetry not reflecting latest license activation | Allow 30–60 minutes for CloudIQ to refresh; confirm SCG is forwarding telemetry |
| COD activation audit trail missing | Activation performed without a change ticket or outside SYMCLI | Review SYMCLI audit log; correlate with Unisphere session logs; update CMDB retroactively |
