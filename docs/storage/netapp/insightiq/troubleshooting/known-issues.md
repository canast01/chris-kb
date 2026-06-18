---
tags:
  - troubleshooting
  - insightiq
  - netapp
  - known-issues
---
# NetApp InsightIQ — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known InsightIQ bugs, error codes, and workarounds covering data collection, API connectivity, and reporting.

*Applies to: NetApp InsightIQ 4.x (formerly Isilon InsightIQ)*
</div>

```text
┌────────────────────────────────────────── NetApp InsightIQ ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             OneFS performance analytics — data collection, trending, and reporting            │   │
│   │                  Protocols: HTTPS (UI) · REST API · PAPI (OneFS cluster API)                  │   │
│   │                Management: InsightIQ web UI · CLI (iiq) · PostgreSQL DB backend               │   │
│   │            Cluster PAPI poll -> InsightIQ ingest -> PostgreSQL -> report dashboard            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Collection         │  │         PAPI poller         │  │     Queries cluster API     │   │
│   │           Storage           │  │        PostgreSQL DB        │  │     Metrics time series     │   │
│   │          Analytics          │  │        Report engine        │  │      Aggregates DB data     │   │
│   │              UI             │  │        Web dashboard        │  │      Charts and exports     │   │
│   │            Export           │  │       PDF / CSV report      │  │      Scheduled delivery     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   InsightIQ VM   │  Analytics host  │     HTTPS 443     │   Local / LDAP   │VMware OVA deploy │   │
│   │   PAPI poller    │Metric collection │    HTTPS (PAPI)   │   OneFS creds    │Per-cluster config│   │
│   │    PostgreSQL    │   Metric store   │     Local TCP     │     DB user      │Grows by retention│   │
│   │  Report engine   │Charting / export │      Internal     │    User role     │ PDF / CSV output │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: InsightIQ VM -> OneFS cluster PAPI (HTTPS) -> PostgreSQL DB -> web UI                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InsightIQ    = NetApp analytics appliance for PowerScale/Isilon performance                          │
│  PAPI         = Platform API; OneFS REST interface used by InsightIQ for data                         │
│  OneFS        = PowerScale (Isilon) operating system; PAPI is its management API                      │
│  Datastore    = InsightIQ monitored cluster + data retention config                                   │
│  Collection interval = how often InsightIQ polls the cluster (default 30 s)                           │
│  Report       = scheduled or on-demand summary of node/disk/protocol metrics                          │
│  Retention    = how long metric data is kept; affects PostgreSQL DB disk usage                        │
│  iiq CLI      = InsightIQ command-line tool for status and config tasks                               │
│  Quota report = InsightIQ report showing directory quota utilization                                  │
│  Protocol report = breakdown of NFS/SMB/HDFS throughput per cluster node                              │
│  DB vacuum    = PostgreSQL maintenance task reclaiming space from old metrics                         │
│  VM snapshot  = InsightIQ backup method; also DB dump for portability                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- InsightIQ errors appear in the web UI under `Administration → Data Collections`.
- Check the InsightIQ appliance system log: `tail -f /var/log/insightiq/insightiq.log`.

## Data Collection

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Cluster data collection showing `No data` | InsightIQ 4.x | InsightIQ cannot reach PowerScale platform API on 8080 | Verify TCP 8080 from InsightIQ to PowerScale SmartConnect IP | N/A |
| `Authentication failed` for managed cluster | InsightIQ 4.x | PowerScale API credentials changed or user locked out | Update cluster credentials in InsightIQ → Clusters → Edit | N/A |
| Performance graphs empty after OneFS upgrade | InsightIQ 4.x | OneFS upgrade changed platform API version; InsightIQ not updated | Upgrade InsightIQ to version compatible with new OneFS release | N/A |

## Reporting

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Report generation times out for long date ranges | InsightIQ 4.x | Database query timeout for large time ranges | Reduce report window to ≤30 days; archive older data to free DB space | N/A |
| Scheduled email report not delivered | InsightIQ 4.x | SMTP relay not configured or port 25 blocked from InsightIQ | Configure SMTP relay in InsightIQ → Administration → Email Settings | N/A |

## See also

- [Dell PowerScale — Known Issues](../../../dell/powerscale/troubleshooting/known-issues.md)
- [NetApp ONTAP — Known Issues](../../ontap/troubleshooting/known-issues.md)
