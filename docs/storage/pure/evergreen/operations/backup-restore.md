---
tags:
  - operations
  - pure
---
# Evergreen — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Evergreen//Forever — No Traditional Backup Required, Export Array Configuration, Pre-Upgrade Configuration Snapshot, Restore After Model Swap, Pure1 Configuration Audit and 1 more sections.

*Applies to: Evergreen*
</div>
![Evergreen — Backup & Restore](../../../../assets/storage-pure-evergreen-operations-backup-restore.svg)




![Evergreen — Backup & Restore — Diagram](../../../../assets/storage-pure-evergreen-operations-backup-restore-diagram.svg)

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Evergreen//Forever — No Traditional Backup Required

Evergreen//Forever is a subscription model, not a product you reinstall. "Backup" here covers:

- Configuration export (alert policies, host connections, protection groups)
- Pure1 telemetry archive
- Array configuration snapshot before a model swap or controller upgrade

## Export Array Configuration

```bash
# Via purearray CLI — export support bundle (includes config snapshot)
purearray list --api-token <token> --address <array-ip>

# Via REST API — get array info
curl -s -k -H "x-auth-token: <token>" https://<array-ip>/api/2.16/arrays | jq .

# Export protection groups
curl -s -k -H "x-auth-token: <token>" https://<array-ip>/api/2.16/protection-groups | jq .

# Export host and host group mappings
curl -s -k -H "x-auth-token: <token>" https://<array-ip>/api/2.16/hosts | jq .
curl -s -k -H "x-auth-token: <token>" https://<array-ip>/api/2.16/host-groups | jq .
```

## Pre-Upgrade Configuration Snapshot

Run before a scheduled controller or model swap to capture current state.

```bash
#!/usr/bin/env bash
# evergreen-config-snapshot.sh
ARRAY_IP="<array-ip>"
TOKEN="<api-token>"
OUT_DIR="./pure-config-$(date +%Y%m%d)"
mkdir -p "$OUT_DIR"

for endpoint in arrays hosts host-groups volumes protection-groups network-interfaces; do
    curl -s -k -H "x-auth-token: $TOKEN" \
        "https://$ARRAY_IP/api/2.16/$endpoint" | jq . > "$OUT_DIR/$endpoint.json"
    echo "Saved: $OUT_DIR/$endpoint.json"
done
echo "Config snapshot complete: $OUT_DIR"
```

## Restore After Model Swap

After a new controller ships under Evergreen//Forever:

1. Dell/Pure engineer connects new hardware and migrates shelf
2. Restore configuration from snapshot if custom settings were overwritten:
   - Re-apply alert email addresses
   - Re-apply SMTP relay settings
   - Re-verify host/host group mappings
   - Confirm protection group schedules

## Pure1 Configuration Audit

Use Pure1 to review historical configuration changes before a restore decision.

- **Pure1 Portal** → select array → **History** tab shows all config events
- Filter by date range to identify what changed before an issue occurred
- Use as reference when re-applying settings manually

## Checklist

- [ ] Export config snapshot before any controller swap
- [ ] Confirm protection group replication targets are intact post-upgrade
- [ ] Verify host connectivity (iSCSI/FC) after hardware replacement
- [ ] Re-register array in Pure1 if hardware serial number changed

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Evergreen — Procedures](procedures/)
- [Evergreen — Health Checks](health-checks/)
