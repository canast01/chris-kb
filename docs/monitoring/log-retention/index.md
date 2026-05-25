# Log Retention Policy

```text
Log Retention Tiers
┌─────────────────────────────────────────────────────┐
│  Collect                                            │
│  (rsyslog / syslog-ng / agent)                      │
└───────────────────────────┬─────────────────────────┘
                            ▼
          ┌─────────────────────────────────┐
          │  Hot storage  (0–30 days)        │
          │  SIEM index / fast query         │
          └─────────────────┬───────────────┘
                            ▼
          ┌─────────────────────────────────┐
          │  Warm storage  (30–90 days)      │
          │  Compressed, searchable          │
          └─────────────────┬───────────────┘
                            ▼
          ┌─────────────────────────────────┐
          │  Cold archive  (90 days–1 yr)   │
          │  Object storage (S3 / NFS)       │
          └─────────────────┬───────────────┘
                            ▼
          ┌─────────────────────────────────┐
          │  Delete / purge                  │
          │  (per retention policy)          │
          └─────────────────────────────────┘
```

## Standard Retention Periods

| Log Type | Minimum Retention | Notes |
|---|---|---|
| System / OS logs | 90 days | Extend if security incident in progress |
| Application logs | 90 days | Per-app requirement may vary |
| Security / auth logs | 365 days | Required for most compliance frameworks |
| Firewall / network logs | 180 days | |
| Audit logs (privileged access) | 1–7 years | Depends on regulatory requirement |
| Backup job logs | 90 days | |
| Change management logs | 7 years | Typically in ITSM, not syslog |

**Regulatory baselines:**
- PCI-DSS: 1 year (3 months immediately accessible)
- ISO 27001: typically 1 year minimum
- GDPR: retain only as long as necessary — purge on schedule

## Linux Log Rotation (logrotate)

```bash
# View current rotation config
cat /etc/logrotate.conf
ls /etc/logrotate.d/

# Test without executing
logrotate -d /etc/logrotate.conf

# Force rotation now
logrotate -f /etc/logrotate.conf
```

**Example custom rule (`/etc/logrotate.d/myapp`):**
```text
/var/log/myapp/*.log {
    daily
    rotate 90
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        systemctl reload myapp
    endscript
}
```

## journald Retention

```bash
# Current disk usage
journalctl --disk-usage

# Set retention in /etc/systemd/journald.conf:
# SystemMaxUse=2G
# MaxRetentionSec=90day

# Apply immediately
systemctl restart systemd-journald

# Manual vacuum
journalctl --vacuum-time=90d
journalctl --vacuum-size=2G
```

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

## Archive to Object Storage

```bash
# Compress and upload old logs (AWS S3 example)
tar czf /tmp/logs-$(date +%Y%m).tar.gz /var/log/archive/$(date +%Y%m)/
aws s3 cp /tmp/logs-$(date +%Y%m).tar.gz s3://<bucket>/logs/$(hostname)/

# Verify
aws s3 ls s3://<bucket>/logs/$(hostname)/
```

## Validation Checklist

- [ ] Log rotation running and not producing errors (`logrotate -d`)
- [ ] journald staying within configured size limit
- [ ] SIEM index retention policies set per standard
- [ ] Archive jobs completing successfully (check last run timestamp)
- [ ] Disk space on log server/index <80% used
- [ ] Security logs accessible for at least 365 days
- [ ] Retention policy document reviewed and approved within last 12 months
