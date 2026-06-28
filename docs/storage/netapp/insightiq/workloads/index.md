---
tags:
  - netapp
---
# InsightIQ — Workload Analysis

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

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
