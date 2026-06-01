# InsightIQ: Workload Classification, Top Talkers, and Client Analysis


<div class="kb-summary">
InsightIQ provides client-level visibility into who is consuming PowerScale cluster resources. This page covers workload classification, identifying top-consuming clients, and using client analysis data for capacity and performance planning.
</div>

## Workload and Client Visibility Overview

InsightIQ collects per-client statistics from the OneFS platform statistics API, allowing visibility into which hosts and protocols are driving the most load.

Navigation: **InsightIQ > Reports > Clients**

Data available per client:

| Metric | Description |
|---|---|
| Read Throughput (MB/s) | Bytes read per second from the cluster |
| Write Throughput (MB/s) | Bytes written per second to the cluster |
| Operations/s | Total NFS, SMB, or HDFS operations per second |
| Average Latency (ms) | Round-trip time experienced by the client |
| Protocol | NFS, SMB, HDFS, or S3 |
| Node Affinity | Which PowerScale node the client is pinned to |

## Identifying Top-Consuming Clients

```bash
# On PowerScale OneFS — real-time top clients by total throughput
ssh admin@powerscale.example.com

# Sort by total bytes (in + out)
isi statistics client list \
  --sort=bytes_in+bytes_out \
  --limit=20 \
  --format table

# Top NFS clients by operations per second
isi statistics client list \
  --protocol=nfs \
  --sort=ops \
  --limit=10

# Top SMB clients by write throughput
isi statistics client list \
  --protocol=smb2 \
  --sort=bytes_out \
  --limit=10 \
  --human-readable

# Identify high-latency clients (may indicate slow network path)
isi statistics client list \
  --sort=latency \
  --limit=10 \
  --format table
```
┌──────────────────────────────────── InsightIQ — Workload Analysis ────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Workload Identification            │  │               Workload Sizing               │   │
│   │                Top-IO clients                │  │              IOPS per workload              │   │
│   │                Top-IO shares                 │  │              Latency SLA check              │   │
│   │              Protocol by client              │  │             Throughput required             │   │
│   │             Time-of-day pattern              │  │              Capacity per team              │   │
│   │                Growth per dir                │  │              Chargeback report              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Workload data from InsightIQ client stats · per-share and per-directory tracking                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Workload = IO pattern from a specific client, application, or directory                              │
│  Top-IO client = Client IP or hostname generating highest IOPS or throughput                          │
│  Top-IO share = NFS export or SMB share with highest IO activity                                      │
│  Protocol by client = Which protocol (NFS/SMB/S3) each client uses                                    │
│  Time-of-day pattern = IO activity profile over 24h; identifies batch window vs real-time             │
│  Growth per directory = Capacity growth rate for specific directories; useful for chargeback          │
│  Latency SLA = Target latency for a workload; InsightIQ used to verify compliance                     │
│  Chargeback = Attributing storage cost to departments using per-client/share IO data                  │
│  Capacity per team = Space consumption breakdown by team based on directory hierarchy                 │
│  Client stats = isi_clientstats on PowerScale; must be enabled for per-client data                    │
│  IOPS per workload = Average and peak IOPS for a specific application or team                         │
│  Throughput required = Peak bandwidth needed; used for network and controller sizing                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Common Workload Analysis Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Client not appearing in statistics | Client uses UDP NFS (rare) | Switch client to TCP NFS mount |
| Latency high for single client | Network path issue or slow client disk | Traceroute from client; check client storage |
| Throughput cap at ~1 GB/s per client | Single 10G NIC on client | Add second NIC or enable LACP bonding |
| Node hotspot (one node carrying all load) | SmartConnect imbalance | Rebalance using `isi network pools modify` or change SmartConnect policy |
| InsightIQ client report empty | Protocol statistics not enabled | Enable on PowerScale: `isi statistics settings modify --enable-protocols true` |
