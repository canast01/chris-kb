# Dell ECS — Overview

Dell ECS (Enterprise Content Storage) is a scale-out, software-defined object storage platform built on commodity x86 nodes. It exposes S3, Swift, Atmos, and CAS (Content Addressable Storage) APIs over standard HTTPS. The software stack runs entirely on commodity hardware and provides geo-distribution across sites via Virtual Data Centers (VDCs) linked into replication groups.

## Scale-Out Object Storage Topology

```mermaid
graph TB
  CLT(["S3 / Swift / Atmos Clients"]) --> GW["Load Balancer\n(optional)"]
  GW --> N1["ECS Node 1"] & N2["ECS Node 2"] & N3["ECS Node 3"] & NN["Node N…"]
  N1 & N2 & N3 & NN --> RING[("Object Ring\ndistributed erasure coding")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class GW,RING net
  class CLT host
```

## How It Works

ECS writes incoming objects by chunking them into fixed-size chunks, applying erasure coding (typically 12+4 or 10+2 depending on node count and VDC span), and distributing coded fragments across nodes. For geo-replication, ECS asynchronously or synchronously replicates chunk journals to remote VDCs according to the replication group policy.

- **Single-site deployment**: All nodes in one VDC. Erasure coding protects against disk and node failure. No geographic redundancy.
- **Multi-site (geo) deployment**: Two or more VDCs in a replication group. Active-active writes are possible; object consistency uses a geo-replication journal. VDC-level failures do not cause data loss if replication lag is near zero.
- **Temporary Site Failure (TSF) mode**: When a VDC is unreachable, the remaining VDC enters TSF mode, continues serving data from local copies, and queues a replication backlog to replay on reconnection.

## Connectivity and Integration Points

| Interface | Protocol / Port | Purpose |
|---|---|---|
| S3 API endpoint | HTTPS 443 or 9021 | Object read/write for applications and backup tools |
| Swift API endpoint | HTTPS 9024 | OpenStack-compatible object access |
| Management REST API | HTTPS 4443 | Administration, monitoring, and automation |
| ECS Portal | HTTPS 443 | Web-based administration console |
| Geo-replication | TCP 9100 | Inter-VDC replication traffic between nodes |
| LDAP/AD | TCP 389 / 636 | Optional namespace-level user authentication |
| Syslog | UDP/TCP 514 | External log forwarding for SIEM integration |
