---
tags:
  - dell
  - deployment
---
# SRDF/A — Initial Deployment

```text
┌────────────────────────────────── Dell SRDF/A — Deployment Sequence ──────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Two PowerMax/VMAX arrays at separate sites with FC or IP connectivity between SRDF director ports    │
│  SRDF licences active on both arrays; matching SRDF group numbers agreed between sites                │
│  Solutions Enabler or Unisphere for PowerMax installed at both sites; WAN link sized for replication  │
│                                                                                                       │
│                                        │  zone SRDF ports and create group                            │
│                                        ▼                                                              │
│  Step 2 · Zone Ports and Create SRDF/A Group                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  FC zoning or IP routing between R1 SRDF director ports and corresponding R2 ports                    │
│  Create group: symrdf createpair -sid <source-sid> -rdfg <n> -rdfgtype asynch -remote_sid <target>    │
│  Add device pairs: symrdf addpair -sid <source> -rdfg <n> -dev <R1-devs> -remote_dev <R2-devs>        │
│  Enable DSE: symrdf -sid <sid> -rdfg <n> dse enable — throttles bandwidth to protect production       │
│                                                                                                       │
│                                        │  establish replication and validate                          │
│                                        ▼                                                              │
│  Step 3 · Establish and Validate                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Start initial copy: symrdf -sid <source> -rdfg <n> establish — full copy from R1 to R2               │
│  Monitor progress: symrdf -sid <source> -rdfg <n> query — wait for Consistent state                   │
│  Verify RPO within configured cycle time; test failover on non-production pair                        │
│  Record: RDFG numbers, device pairs, RPO target, WAN bandwidth allocation per group                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

Two PowerMax/VMAX arrays at separate sites, Fibre Channel or IP connectivity between arrays (SRDF WAN links), SRDF licences on both arrays, matching SRDF group numbers agreed between sites, Solutions Enabler or Unisphere for PowerMax on both sites.

## Zone the SRDF Ports

Configure Fibre Channel zoning or IP routing between the R1 (source) and R2 (target) SRDF director ports — each R1 port zones to corresponding R2 port.

## Create the SRDF Group

On R1 array: `symrdf createpair -sid <source-sid> -rdfg <group-num> -rdfgtype asynch -remote_sid <target-sid>` — define group type as SRDF/A.

## Add Devices to the SRDF Group

`symrdf addpair -sid <source-sid> -rdfg <group-num> -dev <R1-devices> -remote_dev <R2-devices>` — pair source and target LUNs.

## Start Replication

`symrdf -sid <source-sid> -rdfg <group-num> establish` — begins initial full copy from R1 to R2.

## Verify Initial Sync

`symrdf -sid <source-sid> -rdfg <group-num> query` — wait for RDF State to show Synchronized or Consistent; monitor tracks remaining.

## Configure DSE (Dynamic Synchronization Enabler)

Enable DSE for minimal I/O impact: `symrdf -sid <sid> -rdfg <group> dse enable` — throttles replication bandwidth to protect production.

## Validate the Deployment

Check RPO is within configured cycle time, verify `symrdf query` shows all pairs Consistent, test failover on a non-production device pair.
