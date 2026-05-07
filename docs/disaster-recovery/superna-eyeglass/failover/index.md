# Superna Eyeglass — Failover

> Part of the [Superna Eyeglass](../) reference.

---

## Overview

Eyeglass DR Assistant orchestrates failover of PowerScale (Isilon) access zones from a production cluster to a DR cluster. Failover includes stopping SyncIQ replication, activating DR access zones, and remapping NFS/SMB shares and DNS entries.

| Failover Type | Description | Disruption |
|---|---|---|
| Planned (Test) | Full DR rehearsal; production cluster is available; tests cutover and cutback | Temporary client disruption during cutover |
| Unplanned (DR Event) | Production cluster unavailable; DR cluster is activated | Service outage until DR cluster is activated |
| Access Zone Failover | Fail over a single access zone without affecting others | Targeted disruption |

---

## Pre-Failover Checklist

```bash
# Confirm DR PowerScale cluster is healthy
ssh admin@<dr-powerscale-cluster> "isi status"

# Confirm SyncIQ replication is current (lag is within RPO)
ssh admin@<production-powerscale> "isi sync policies list"
ssh admin@<production-powerscale> "isi sync jobs list"

# Confirm last successful SyncIQ run time
isi sync policies view <policy_name>

# Confirm Eyeglass services are running
egcli status

# Run Eyeglass DR preflight check
egcli drtest preflight --cluster <dr-cluster>

# Confirm DR access zones are configured and ready
egcli accesszone list --cluster <dr-cluster>
```

---

## Initiating Failover via Eyeglass CLI

```bash
# List all configured DR policies
egcli drpolicy list

# Check the current state of all DR policies
egcli drpolicy status --all

# Run a DR test (non-disruptive rehearsal — confirms readiness without cutting over DNS)
egcli drtest run --policy <policy_name>

# Initiate a full failover (disruptive — activates DR cluster)
egcli drfailover --policy <policy_name> --confirm

# Monitor failover progress
egcli drfailover status --policy <policy_name>

# Watch Eyeglass job log for failover steps
egcli jobs list --type failover
```

---

## Access Zone Activation at DR Site

```bash
# After failover is triggered — confirm DR access zones are active
egcli accesszone status --cluster <dr-cluster>

# Confirm NFS exports are present on DR cluster
ssh admin@<dr-cluster> "isi nfs exports list"

# Confirm SMB shares are present on DR cluster
ssh admin@<dr-cluster> "isi smb shares list"

# Confirm SmartConnect zones are responding on DR VIP pool
nslookup <dr-smartconnect-zone-name>

# Test NFS mount from a client (Linux)
mount -t nfs <dr-smartconnect-ip>:/<export_path> /mnt/test
ls /mnt/test

# Test SMB access from a client (Windows)
net use Z: \\<dr-cluster-ip>\<share_name>
```

---

## DNS Cutover

Eyeglass automates DNS delegation updates if integrated with DNS; manual steps if not.

```bash
# Verify Eyeglass DNS integration is configured
egcli dns status

# If using Eyeglass automated DNS failover — confirm DNS record updated
egcli dns records list --zone <smartconnect_zone>

# If managing DNS manually — update the SmartConnect delegation NS record
# to point to the DR cluster IP pool
# Verify propagation
dig <smartconnect_zone_name> @<internal-dns-server>
nslookup <smartconnect_zone_name>
```

---

## Failover State Reference

| State | Meaning | Action |
|---|---|---|
| Replicating | Normal — SyncIQ running; production active | No action |
| DR Test Running | Preflight or DR test in progress | Monitor to completion |
| Failing Over | Failover in progress | Monitor; do not interrupt |
| Failed Over | DR cluster is active; SyncIQ stopped | Validate client access; plan failback |
| Failback Running | Reverse sync in progress | Monitor to completion |

```bash
# Check policy state at any time
egcli drpolicy status --policy <policy_name>
```
