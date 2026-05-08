# COD — Common Issues

> Part of the [COD](../../) reference.

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
