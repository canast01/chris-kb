---
tags:
  - operations
  - security
description: "Log Retention Policy reference covering journald Retention, Centralised Log Retention (SIEM / Graylog / Splunk), Archive to Object Storage, Validation..."
---
# Log Retention Policy

<div class="kb-summary">
Log Retention Policy reference covering journald Retention, Centralised Log Retention (SIEM / Graylog / Splunk), Archive to Object Storage, Validation Checklist.
</div>

```d2
direction: down

centralised_log_retention_siem_grayl: "Centralised Log Retention (SIEM / Graylog / Splunk)" {shape: rectangle}
archive_to_object_storage: "Archive to Object Storage" {shape: rectangle}
validation_checklist: "Validation Checklist" {shape: rectangle}
verify: "Verify" {shape: rectangle}

centralised_log_retention_siem_grayl -> archive_to_object_storage: uses
archive_to_object_storage -> validation_checklist: uses
validation_checklist -> verify: uses
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Centralised Log Retention (SIEM / Graylog / Splunk)

**Graylog:**
- Set index retention policy: Admin → System → Indices → Index set → Max retention
- Configure message TTL per stream for fine-grained control

**Splunk:**
```bash
# Set retention per index in indexes.conf
[main]
frozenTimePeriodInSecs = 7776000   # 90 days
maxTotalDataSizeMB = 500000
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error in 'main' stanza: attribute 'frozenTimePeriodInSecs' not recognized` | Verify the attribute name matches your Splunk version's indexes.conf schema (some versions use `frozenTimePeriodInDays` instead). |
    | `maxTotalDataSizeMB must be greater than maxMemMB` | Increase `maxTotalDataSizeMB` to a value larger than the index's `maxMemMB` setting (typically at least 20MB higher). |
**Elasticsearch (ELK):**
```bash
# Index Lifecycle Management (ILM) — set delete phase
PUT _ilm/policy/infra-logs-policy
{
  "policy": {
    "phases": {
      "delete": {
        "min_age": "90d",
        "actions": { "delete": {} }
      }
    }
  }
}
```


```text title="Expected output"
{
  "acknowledged": true
}
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `400 Bad Request: [illegal_argument_exception] unknown setting [policy.phases.delete.min_age]` | Use `min_age` directly under the phase object, not nested; the correct structure is `"phases": { "delete": { "min_age": "90d", "actions": {...} } }`. |
    | `403 Forbidden: [security_exception] action [cluster:admin:ilm:put] is unauthorized` | Grant the user or role the `manage_ilm` cluster privilege in Elasticsearch security settings. |
## Archive to Object Storage

```bash
# Compress and upload old logs (AWS S3 example)
tar czf /tmp/logs-$(date +%Y%m).tar.gz /var/log/archive/$(date +%Y%m)/
aws s3 cp /tmp/logs-$(date +%Y%m).tar.gz s3://<bucket>/logs/$(hostname)/

# Verify
aws s3 ls s3://<bucket>/logs/$(hostname)/
```


```text title="Expected output"
tar: Removing leading `/' from member names
logs-202501.tar.gz
2025-01-15 14:32:18       8547291 logs-202501.tar.gz

upload: /tmp/logs-202501.tar.gz to s3://compliance-logs-prod/logs/web-server-03/logs-202501.tar.gz

2025-01-15 14:32:45       8547291 logs-202501.tar.gz
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `fatal error: An error occurred (NoSuchBucket) when calling the PutObject operation: The specified bucket does not exist` | Verify the bucket name in the command matches your actual S3 bucket and that your AWS credentials have s3:PutObject permissions. |
    | `tar: /var/log/archive/202501/: Cannot stat: No such file or directory` | Ensure the archive directory exists for the current month; create it with `mkdir -p /var/log/archive/$(date +%Y%m)/` if logs haven't been rotated yet. |
    | `Unable to locate credentials` | Configure AWS credentials using `aws configure` or set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables. |
## Validation Checklist

- [ ] Log rotation running and not producing errors (`logrotate -d`)
- [ ] journald staying within configured size limit
- [ ] SIEM index retention policies set per standard
- [ ] Archive jobs completing successfully (check last run timestamp)
- [ ] Disk space on log server/index <80% used
- [ ] Security logs accessible for at least 365 days
- [ ] Retention policy document reviewed and approved within last 12 months

---

## Verify

- SIEM retention policy is set to the required minimum (e.g., 365 days for security logs)
- Archive job last-run timestamp is within the scheduled window
- Log server/index disk utilisation is below 80%
- A spot test — querying logs from 12 months ago — returns results, confirming retention is active

## See also

- [Security Operations — Event Correlation](../event-correlation/)
- [Security Operations — Runbooks](../runbooks/)
- [Security Monitoring Overview](../../security-monitoring/)
