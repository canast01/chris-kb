# CloudWatch


<div class="kb-summary">
CloudWatch reference.
</div>

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
┌──────────────────────────────────────── AWS CLI — CloudWatch ─────────────────────────────────────────┐
│                                                                                                       │
│  CloudWatch CLI commands for metrics, alarms, log groups, dashboards, and insights.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Metrics Commands               │  │                Alarm Commands               │   │
│   │           list-metrics: available            │  │            describe-alarms: list            │   │
│   │         get-metric-statistics: query         │  │           put-metric-alarm: create          │   │
│   │           put-metric-data: publish           │  │            set-alarm-state: test            │   │
│   │         get-metric-data: bulk query          │  │            delete-alarms: remove            │   │
│   │          list-dashboards: overview           │  │            describe-alarm-history           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Metrics queried with namespace+dimension; alarms reference metric and threshold                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Logs Commands                 │  │              Insights Commands              │   │
│   │          describe-log-groups: list           │  │            start-query: run query           │   │
│   │          describe-log-streams: list          │  │           get-query-results: fetch          │   │
│   │          get-log-events: raw events          │  │          describe-queries: history          │   │
│   │          filter-log-events: search           │  │            stop-query: cancel run           │   │
│   │          put-log-events: write logs          │  │           create-log-group: setup           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  CloudWatch service · S3 (log export) · SNS (alarm action) · Lambda (alarm action)                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Namespace       = Grouping for metrics, e.g. AWS/EC2, AWS/RDS, Custom/App                            │
│  Dimension       = Key-value pair identifying metric source, e.g. InstanceId=i-xxx                    │
│  get-metric-data = Bulk metric query with math expressions; preferred over statistics                 │
│  put-metric-data = Publishes custom application metrics to CloudWatch                                 │
│  set-alarm-state = Forces alarm state for testing SNS/Lambda alarm actions                            │
│  filter-log-events= Searches log streams with pattern filter and time range                           │
│  Insights query  = SQL-like syntax for querying structured log data                                   │
│  Log group       = Container for log streams; has retention policy                                    │
│  Log stream      = Sequence of log events from one source (EC2 instance, Lambda)                      │
│  Retention policy= Days to keep log events before automatic deletion                                  │
│  describe-alarm-history= Shows state transitions for debugging alarm behavior                         │
│  put-metric-alarm= Creates/updates alarm; defines threshold, period, evaluation count                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
