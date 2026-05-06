# InsightIQ Operations

Daily operational checks ensure all cluster connections are active and collecting data. Log into the InsightIQ web dashboard each morning, confirm all monitored clusters show a green connection status, and review latency and throughput trends for anomalies versus the previous 7-day baseline. Check disk usage on the InsightIQ appliance to ensure the PostgreSQL data volume is below 80% capacity. Weekly, generate a utilisation report per cluster for capacity planning review.

**Daily Checklist**
- Log into InsightIQ web dashboard
- Confirm all cluster connections are Active (green)
- Review latency and throughput dashboards — flag anomalies vs. 7-day baseline
- Check appliance disk usage (alert at 80%)

**Weekly Tasks**
- Generate per-cluster utilisation report for capacity planning
- Review top protocol clients for unexpected load patterns
- Validate InsightIQ appliance backup completed successfully
