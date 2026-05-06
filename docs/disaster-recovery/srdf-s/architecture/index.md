# SRDF/S Architecture

> Part of the [SRDF/S](../) reference.

---

## Overview

SRDF/S (Synchronous) provides zero-data-loss replication between two PowerMax arrays. Every host write is committed to both the source (R1) and target (R2) before an acknowledgement is returned to the host. This guarantees **RPO = 0** at the cost of write latency, which is directly proportional to the inter-site round-trip time (RTT).

**Use case:** Applications that cannot tolerate any data loss — financial transaction systems, active-active cluster workloads, and DR configurations where RPO = 0 is contractually required.

---

## Write Commit Model

```
Host write request
      ↓
R1 (source PowerMax) accepts write
      ↓
R1 transmits write to R2 over SRDF link
      ↓
R2 (target PowerMax) commits the write
      ↓
R2 sends acknowledgement to R1
      ↓
R1 sends ACK to host
```

Every additional millisecond of RTT adds directly to host write latency. The **recommended maximum RTT is 5ms** — beyond this, write response times degrade to the point of impacting most production workloads.

---

## Key Components

| Component | Role |
|---|---|
| R1 device | Source (production) SRDF device |
| R2 device | Target (DR) SRDF device |
| RDF group | Logical pairing of devices sharing synchronous write semantics |
| SRDF director | PowerMax back-end ports handling SRDF I/O |
| SRDF/S link | Dark fibre or DWDM optical connection between sites (FCIP adds latency) |

---

## Pair States

| State | Meaning | Normal? |
|---|---|---|
| Synchronized | R2 is fully in sync; all writes are current | Yes — normal SRDF/S state |
| SyncInProg | Initial synchronisation or re-sync in progress | Transient — after establish or resume |
| Suspended | Replication suspended (temporarily async or halted) | Only expected during maintenance |
| Failed Over | R1 read-only; R2 R/W — active failover | During planned or unplanned failover |
| Split | Both R1 and R2 are R/W — data diverges from this point | Planned split only; data diverges |

---

## RTT and Latency Budget

SRDF/S write latency = host-to-array latency + array processing time + **2 × RTT** (round trip to R2 and back).

| RTT | Additional Write Latency |
|---|---|
| 1ms | ~2ms added |
| 3ms | ~6ms added |
| 5ms | ~10ms added (upper recommended limit) |
| 10ms | ~20ms added — typically not acceptable for OLTP |

To measure current RTT between arrays:

```bash
# From R1 array — ping the R2 SRDF director IP
symcfg -sid <r1_sid> list -rdfg <group_num> -v
# Review "Remote Array" connectivity details

# Or use SYMCLI to check the SRDF link performance metrics
symrdf -sid <r1_sid> -rdfg <group_num> list -v
```

---

## Connectivity

SRDF/S requires low-latency inter-site connectivity. Suitable link types:

| Link Type | Typical Use |
|---|---|
| Dark fibre (FC) | Metropolitan distances — lowest latency |
| DWDM optical | Extended metropolitan distances up to ~100km |
| FCIP over MPLS | WAN — only viable if guaranteed latency ≤3ms |

FCIP (FC over IP) introduces additional protocol encapsulation overhead and is generally not suitable for SRDF/S at distances beyond a metro campus.

---

## Cascade Architecture (SRDF/S + SRDF/A)

A common tiered protection architecture uses SRDF/S to a local DR site (RPO = 0, low RTT) and SRDF/A from the local DR site to a remote third site (RPO = minutes, tolerates WAN latency):

```
Production (R1)  ──SRDF/S──►  Metro DR (R21/R1)  ──SRDF/A──►  Remote DR (R2)
     RPO = 0                      RPO = 0 from prod             RPO = ~30s
```

This provides:
- Zero data loss between production and metro DR
- Cost-effective remote protection without requiring synchronous WAN bandwidth to the remote site

---

## Licensing

- SRDF/S license required on both arrays (separate from SRDF/A license)
- SRDF director ports must be licensed for synchronous replication
- SRDF/Metro (active-active SRDF/S variant) requires an additional license
