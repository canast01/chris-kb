# SRDF/S — Initial Deployment

```text
┌────────────────────────────── Dell SRDF/S — Deployment Sequence ──────────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Two PowerMax/VMAX arrays within low-latency WAN (<10ms RTT between SRDF director ports)              │
│  FC or IP SRDF links between sites; SRDF synchronous licence on both arrays                           │
│  R2 (target) must have capacity equal to all R1 devices planned for SRDF/S protection                 │
│                                                                                                       │
│                                        │  zone ports and create group                                 │
│                                        ▼                                                              │
│  Step 2 · Zone Ports and Create SRDF/S Group                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  FC zoning between R1 SRDF director ports and corresponding R2 ports (one-to-one per director)        │
│  Create group: symrdf createpair -sid <source-sid> -rdfg <n> -rdfgtype synchronous -remote_sid <t>    │
│  Add devices: symrdf addpair -sid <source> -rdfg <n> -dev <R1-devs> -remote_dev <R2-devs>             │
│                                                                                                       │
│                                        │  establish and validate                                      │
│                                        ▼                                                              │
│  Step 3 · Establish and Validate                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Start sync: symrdf -sid <source> -rdfg <n> establish — all host writes held until R2 acknowledges    │
│  Monitor: symrdf query — all pairs must reach Synchronized state before declaring production-ready    │
│  Measure host write latency before/after; confirm RTT stable <10ms; verify no SLA breach              │
│  Test failover on non-production pair; record RTO achieved; document in DR runbook                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

Two PowerMax/VMAX arrays within low-latency WAN (<10ms RTT between SRDF ports), Fibre Channel or IP SRDF links, SRDF synchronous licence on both arrays, capacity on R2 equal to R1 devices being protected.

## Zone SRDF Director Ports

FC zoning between R1 SRDF ports and R2 SRDF ports — each director port on source zones to matching port on target.

## Create the SRDF/S Group

`symrdf createpair -sid <source-sid> -rdfg <group-num> -rdfgtype synchronous -remote_sid <target-sid>`

## Add Devices

`symrdf addpair -sid <source-sid> -rdfg <group-num> -dev <R1-devices> -remote_dev <R2-devices>`

## Establish Synchronous Replication

`symrdf -sid <source-sid> -rdfg <group-num> establish` — full initial copy; all writes to R1 must be acknowledged by R2 before returning to host.

## Verify Synchronization

`symrdf -sid <source-sid> -rdfg <group-num> query` — all pairs must show RDF State: Synchronized. WAN RTT should be stable <10ms.

## Test Write Latency Impact

Measure host write latency before and after establishing SRDF/S — expect additional RTT delay. Confirm acceptable for workloads.

## Validate the Deployment

Verify `symrdf query` shows all Synchronized, confirm no write latency SLA breach, test failover on non-production pair, document RTO achieved.
