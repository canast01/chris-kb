# FOD — Diagnostics


<div class="kb-summary">
> Part of the [Flex on Demand](../../index.md) reference.
</div>

---

```bash
# CloudIQ REST API — get capacity metrics for a system (requires CloudIQ API token)
curl -s -H "Authorization: Bearer <cloudiq_token>" \
  "https://cloudiq.dell.com/cloudiq/rest/v1/storage-systems?system_id=<system_id>" | jq .

# PowerMax — show current thin pool utilisation (metered capacity is tracked here)
symcfg -sid <SID> -pool -dp list

# PowerStore — show capacity summary via PowerStore REST API
curl -s -k -u "admin:<pass>" \
  "https://<powerstore-host>/api/rest/capacity" | jq .

# PowerScale — show total cluster usable capacity and used
isi storagepool list

# Confirm CloudIQ telemetry is active (check SCG/CloudIQ agent status)
systemctl status dell-cloudiq-agent 2>/dev/null || \
  service dell-cloudiq-agent status 2>/dev/null || echo "Agent not found on this host"
```

## Log Locations

| Log | Location |
|---|---|
| SCG telemetry logs | `/var/log/dsagw/` on the SCG host |
| Unisphere audit log | Unisphere GUI → Settings → Audit Log |
| APEX Console audit | APEX Console → Administration → Audit |
