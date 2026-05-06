# InsightIQ Architecture

InsightIQ is a performance analytics platform for NetApp PowerScale (Isilon) clusters, deployed as a virtual appliance (OVA) or via a Linux installer on a dedicated VM. Metrics are collected from OneFS clusters via the InsightIQ data connector and stored in a local PostgreSQL database. The web-based dashboard presents throughput, latency, CPU, and protocol-level breakdowns, allowing capacity planners and storage administrators to trend performance over time. A single InsightIQ instance can monitor multiple PowerScale clusters.

| Component | Details |
|---|---|
| Deployment | OVA or Linux installer on dedicated VM |
| Database | PostgreSQL (local to appliance) |
| Data Collection | OneFS InsightIQ data connector (pull) |
| Presentation | Web dashboard (HTTP/HTTPS) |
| Multi-cluster | Yes — multiple clusters per instance |
