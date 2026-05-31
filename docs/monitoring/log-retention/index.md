# Log Retention Policy

```text
┌───────────────────────────────────── Monitoring — Log Retention ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              Log Retention — Policies, Storage Tiers, and Compliance Requirements             │   │
│   │       Log types: syslog · vCenter events · API audit · security audit · performance data      │   │
│   │     Tiers: hot (NFS/local, 30 days) · warm (object store, 90 days) · cold (archive, 1 yr)     │   │
│   │           Compliance: SOC2/ISO27001 require 12-month minimum for security audit logs          │   │
│   │           Tools: Aria Log Insight · rsyslog · Splunk forward · S3-compatible archive          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Retention tiers balance query speed vs. storage cost — hot for ops, cold for compliance            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Hot Tier (30 days)     │  │     Warm Tier (90 days)     │  │     Cold Tier (1 year+)     │   │
│   │       NFS or local SSD      │  │      Object store (S3)      │  │     Glacier/deep archive    │   │
│   │       Full-text search      │  │       Compressed gzip       │  │      Encrypted at rest      │   │
│   │       Sub-second query      │  │      Index retained 30d     │  │      Restore: 4-hr SLA      │   │
│   │      Log Insight bucket     │  │       Policy-auto-move      │  │       Legal hold flag       │   │
│   │      Syslog stream live     │  │     Security audit logs     │  │       Compliance audit      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Aria Log Insight VM on vSphere · NFS datastore for hot tier · MinIO/S3 for warm/cold tiers           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Hot tier          = Fast-access storage for recent logs; supports real-time search                   │
│  Warm tier         = Compressed object storage; slower but cost-efficient for 30-90 day range         │
│  Cold tier         = Deep archive; minimal cost; long restore times; used for compliance              │
│  Retention policy  = Rule defining how long a log type is kept and when it transitions tiers          │
│  Log Insight       = VMware Aria Log Insight; on-prem log aggregation and search platform             │
│  rsyslog           = Linux syslog daemon; ingests and forwards RFC-5424 syslog messages               │
│  Legal hold        = Flag preventing log deletion regardless of retention policy expiry               │
│  SOC2              = Service Organization Control 2; audit framework requiring log retention          │
│  ISO 27001         = Information security management standard with log evidence requirements          │
│  Gzip compression  = Lossless compression reducing warm-tier storage by 60-80%                        │
│  Object store      = S3-compatible storage backend for warm/cold log archiving                        │
│  Auto-move policy  = Lifecycle rule automatically migrating logs between tiers on schedule            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
