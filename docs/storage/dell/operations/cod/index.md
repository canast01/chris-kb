# COD — Capacity on Demand

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Bash license inventory checker, Python activation tracker, and Ansible COD validation playbook.</span>
</a>

</div>

## Purpose

Operational runbook for tracking, auditing, and activating Dell Capacity on Demand (COD) licenses across the storage estate. COD licenses gate access to pre-installed but reserved capacity — this page covers how to verify what is installed, what is activated, and how to act when activation is needed.

## Common Checks

- **License inventory**: Run `symlicense -sid <SID> list` on each PowerMax/VMAX to confirm which COD licenses are installed and their activation state
- **Utilisation headroom**: Check how far current pool usage is from the activated ceiling — if above 75%, plan the next activation
- **Reserve remaining**: Confirm that un-activated COD drives are still physically present and not misreported
- **License expiry**: Some time-limited COD licenses have expiry dates — review for any approaching expiry in the next 90 days
- **CloudIQ capacity forecast**: Review CloudIQ → Capacity for the relevant system to see the projected days until the activated pool is exhausted

## COD Activation Procedure

1. Confirm the array SID and the exact capacity increment needed (e.g., 24 × 3.84 TB NVMe drives)
2. Contact the Dell account team or submit a request via Dell MyAccount to purchase the COD activation license
3. Receive the license file (`.xml` or `.dat`) and verify the SID in the file matches the target array
4. Apply the license:
   - **PowerMax via SYMCLI**: `symlicense -sid <SID> install -file <license.xml>`
   - **PowerMax via Unisphere**: Administration → Licenses → Install License
   - **Unity via uemcli**: `uemcli /sys/license upload`
5. Verify the new capacity is visible: `symcfg -sid <SID> show` and confirm pool size has increased
6. Add newly activated drives to the appropriate thin pool or storage tier
7. Update the COD inventory runbook with the activation date, key reference, and new activated ceiling

## Incident Notes

If a COD activation is urgently needed (capacity event in progress):

- **Symptom**: Pool utilisation at or above 90%; write failures beginning or imminent
- **Impact**: Applications writing to the affected pool may experience errors or throttling
- **Start time**: When did pool utilisation cross 80%? (Check CloudIQ capacity trend)
- **What changed**: Any unexpected data growth — new backups, snapshots, database growth?
- **What was checked**: `symcfg -pool -dp list`, CloudIQ capacity page, license inventory
- **Resolution**: Emergency COD activation via Dell account team (reference contract number); document activation key and new ceiling

## Change Notes

For planned COD activations:

- **Approval**: COD activation is a licensed capacity change — confirm with the budget owner and log in the change management system
- **Rollback plan**: COD activation is not reversible — once activated, the capacity is licensed; document the pre-activation pool state
- **Validation steps**: After activation, confirm pool size increase with `symcfg -sid <SID> -pool -dp list` and verify no change to replication or snapshot schedules

## Best Practices

- Keep a spreadsheet of every array, its installed COD drives, activated ceiling, and remaining reserve — this is not visible in a single CLI command
- Set a CloudIQ capacity alert at 70% of the activated pool so there is time to procure the next activation key before an incident
- Store COD license files in a versioned, backed-up secrets store — lost keys require Dell re-issuance which can take days
- Coordinate COD activations with the capacity planning cycle, not reactively — reactive activations often occur during incidents
