# CloudWatch

```text
CloudWatch CLI: Metrics → Alarms → Logs
──────────────────────────────────────────────────────────────

  AWS Service (EC2/RDS/Lambda...)
       │  emits
       ▼
  ┌──────────────────────┐     put-metric-data (custom)
  │  Metrics             │◄──────────────────────────────
  │  list-metrics        │
  │  get-metric-statistics│
  └──────────┬───────────┘
             │  threshold breach
             ▼
  ┌──────────────────────┐
  │  Alarms              │
  │  describe-alarms     │
  │  ┌────────────────┐  │
  │  │ OK / ALARM /   │  │───► SNS / Auto Scaling / EC2
  │  │ INSUFFICIENT   │  │     action
  │  └────────────────┘  │
  │  set-alarm-state     │
  └──────────────────────┘

  Application / Service logs
       │
       ▼
  ┌──────────────────────┐
  │  Log Groups / Streams│
  │  describe-log-groups │
  │  get-log-events      │
  │  filter-log-events   │
  │  logs tail --follow  │
  └──────────────────────┘
```

> Part of the AWS CLI Reference.

---

```bash
# Alarms
aws cloudwatch describe-alarms
aws cloudwatch describe-alarms --state-value ALARM
aws cloudwatch set-alarm-state --alarm-name <name> --state-value OK --state-reason "manual reset"

# Metrics
aws cloudwatch list-metrics --namespace AWS/EC2
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization \
  --dimensions Name=InstanceId,Value=<id> \
  --start-time $(date -u -d '1 hour ago' +%FT%TZ) \
  --end-time $(date -u +%FT%TZ) \
  --period 300 --statistics Average

# Logs
aws logs describe-log-groups
aws logs describe-log-streams --log-group-name <group>
aws logs get-log-events --log-group-name <group> --log-stream-name <stream>
aws logs tail <log_group> --follow
aws logs filter-log-events --log-group-name <group> --filter-pattern "ERROR"
```
