# InsightIQ: Workload Classification, Top Talkers, and Client Analysis

InsightIQ provides client-level visibility into who is consuming PowerScale cluster resources. This page covers workload classification, identifying top-consuming clients, and using client analysis data for capacity and performance planning.

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
```

Workload classification criteria:

| I/O Pattern | Read % | Block Size | Latency Tolerance | Example |
|---|---|---|---|---|
| Streaming Read | > 80% | > 256 KB | Moderate | Backup restore, media playout |
| Streaming Write | < 20% | > 256 KB | Moderate | Video ingest, log aggregation |
| Random Mixed | 40–60% | < 64 KB | Low | VMware NFS, databases |
| Metadata Heavy | ~50% | < 8 KB | Very low | HOME dirs, many small files |
| Batch Analytics | Variable | > 1 MB | High | Hadoop/Spark HDFS jobs |

## Client Node Affinity and SmartConnect

Clients connect to PowerScale via SmartConnect DNS zones, which load-balance connections across nodes. An imbalanced distribution is visible in InsightIQ.

```bash
# Check current SmartConnect zone configuration
ssh admin@powerscale.example.com
isi network pools list

# Check per-node client count
isi statistics node list --stats=node.clientstats.connected --format table

# Manually check client connection distribution
isi statistics client list --format csv | awk -F',' '{print $2}' | sort | uniq -c | sort -rn
```

## Using Client Data for Capacity Planning

Combine client analysis with capacity growth data to project per-tenant or per-application growth rates:

```bash
# Identify which directories are growing fastest
ssh admin@powerscale.example.com

# Top 10 directories by size under /ifs/data
du -s /ifs/data/* | sort -rn | head -10

# Watch directory growth over time using InsightIQ directory quota reports
# Navigate to: InsightIQ > Reports > Quota > Directory Usage Trend
```

## Common Workload Analysis Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Client not appearing in statistics | Client uses UDP NFS (rare) | Switch client to TCP NFS mount |
| Latency high for single client | Network path issue or slow client disk | Traceroute from client; check client storage |
| Throughput cap at ~1 GB/s per client | Single 10G NIC on client | Add second NIC or enable LACP bonding |
| Node hotspot (one node carrying all load) | SmartConnect imbalance | Rebalance using `isi network pools modify` or change SmartConnect policy |
| InsightIQ client report empty | Protocol statistics not enabled | Enable on PowerScale: `isi statistics settings modify --enable-protocols true` |
