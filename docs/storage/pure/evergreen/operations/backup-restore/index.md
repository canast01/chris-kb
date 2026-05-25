# Evergreen — Backup & Restore

```text
Evergreen Configuration Backup + Restore
  Configuration export (before controller refresh / migration):
  ├── pureconfig list --all  ──► export array config to file
  ├── purepgroup list --schedule ──► document PGroup schedules
  └── purehost list + purehgroup list ──► host/group inventory
          │
          ▼
  Store offline: CMDB / Git / secure file share

  Post-refresh validation:
  ├── purearray list --controller ──► new gen controllers
  ├── purealert list ──► no residual alerts
  └── purehost list --connection ──► all host paths restored
```

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
