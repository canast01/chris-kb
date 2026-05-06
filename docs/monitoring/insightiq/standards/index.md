# InsightIQ Standards

InsightIQ appliance sizing is based on the number of monitored clusters and the desired data retention period: allocate a minimum of 4 vCPU, 8 GB RAM, and 200 GB disk per 5 clusters with 90-day hot retention. The standard data retention policy is 90 days of high-resolution data. Cluster connection credentials should use a dedicated read-only OneFS service account (`svc-insightiq`) rather than shared admin credentials. Alert thresholds for latency should be set at 5 ms (warn) and 10 ms (critical) for NFS/SMB workloads; throughput thresholds are environment-specific.

- Minimum sizing: 4 vCPU / 8 GB RAM / 200 GB per 5 clusters
- Data retention: 90 days hot (high-resolution)
- Cluster credentials: dedicated `svc-insightiq` read-only account
- Latency thresholds: 5 ms warn / 10 ms critical
- Report schedules: weekly utilisation, monthly capacity review
