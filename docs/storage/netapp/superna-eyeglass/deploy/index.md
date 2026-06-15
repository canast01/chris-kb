---
tags:
  - deployment
  - netapp
search:
  boost: 1.5
---

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Superna Eyeglass — Initial Deployment

```text
┌─────────────────────────────── Superna Eyeglass — Deployment Sequence ────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Prerequisites                                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  PowerScale (Isilon) clusters at both sites (production and DR) running OneFS 8.0+                    │
│  vSphere environment for Eyeglass virtual appliance OVA deployment                                    │
│  Network: HTTPS (8080/443) from Eyeglass VM to both cluster management IPs                            │
│  Eyeglass licence obtained from Superna portal; DNS entries for both cluster SmartConnect zones       │
│                                                                                                       │
│                                        │  deploy appliance                                            │
│                                        ▼                                                              │
│  Step 2 · Deploy Eyeglass Virtual Appliance                                                           │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Download OVA from Superna support portal; deploy via vCenter Deploy OVF Template                     │
│  Complete wizard: assign static IP, DNS, gateway, NTP; power on VM                                    │
│  Complete first-boot wizard via console: set admin password, network details, hostname                │
│  Access Eyeglass UI: https://<Eyeglass-IP>:8080; log in and activate licence                          │
│                                                                                                       │
│                                        │  connect clusters                                            │
│                                        ▼                                                              │
│  Step 3 · Connect Source and DR Clusters                                                              │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Eyeglass → Configuration → Add Cluster; enter source PowerScale management IP/FQDN + credentials     │
│  Test connectivity → Save; add second (DR) cluster in the same way                                    │
│  Eyeglass discovers shares, NFS exports, quotas, and users from both clusters                         │
│                                                                                                       │
│                                        │  configure replication and sync                              │
│                                        ▼                                                              │
│  Step 4 · Configure Replication Jobs and User Sync                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Configuration Replication → New Job: select source cluster, shares/exports/quotas, DR cluster        │
│  Set schedule (e.g. every 15 minutes); save; trigger manual sync to verify first replication          │
│  User and Group Replication → enable; select source and target clusters; test sync                    │
│  Verify shares and exports appear on DR cluster; verify ACLs and quota settings preserved             │
│                                                                                                       │
│                                        │  validate and baseline                                       │
│                                        ▼                                                              │
│  Step 5 · Validation and DR Readiness                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Eyeglass → DR Testing → Runbook: generate DR readiness report; verify all jobs show Ready            │
│  Document last sync timestamp; confirm configuration lag is within acceptable window                  │
│  Schedule first non-production DR test; record Eyeglass VM IP, version, cluster list                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Prerequisites

PowerScale (Isilon) clusters at both sites (production and DR), vSphere for Eyeglass virtual appliance, network access between Eyeglass and both clusters (HTTPS 8080/443), Eyeglass licence, DNS entries for both cluster SmartConnect zones.

## Deploy the Eyeglass Appliance

Download OVA from Superna portal, deploy to vSphere, assign IP/DNS/gateway, power on, complete first-boot wizard.

## Connect to Source Cluster

Eyeglass Configuration → Add Cluster → enter source PowerScale management IP/FQDN → credentials (admin or service account with appropriate role) → test connectivity → save.

## Connect to DR Cluster

Add second cluster (DR PowerScale) → credentials → test → save.

## Configure Replication Jobs

Eyeglass → Configuration Replication → New Job → select source cluster → select shares/exports/quotas to replicate → select DR cluster as target → set schedule → save.

## Configure User and Group Sync

Eyeglass → User and Group Replication → enable → select source and target clusters → test sync.

## Run First Sync

Trigger manual sync for all replication jobs → verify shares/exports/quotas appear on DR cluster → verify ACLs are preserved.

## Validate the Deployment

Eyeglass → DR Testing → Runbook → generate DR readiness report → verify all jobs show Ready → document last sync timestamp → schedule first DR test.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Superna Eyeglass — Procedures](../operations/procedures/)
- [Superna Eyeglass — Common Issues](../troubleshooting/common-issues/)
- [Superna Eyeglass — How It Works](../architecture/how-it-works/)
