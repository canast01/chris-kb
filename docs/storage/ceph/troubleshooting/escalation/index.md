# Ceph — Escalation

<div class="kb-summary">
Ceph support escalation: Red Hat Ceph Storage support case process, community resources, severity levels, and required diagnostic data for support cases.
</div>

```text
┌────────────────────────────────────── Ceph — Support Escalation ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Red Hat Ceph Storage: full commercial support for RHCS; similar to RHEL support model       │   │
│   │   Community Ceph: upstream issues go to ceph-users ML or GitHub issues                        │   │
│   │   Data loss risk: any HEALTH_ERR with inactive PGs → open Sev 1 immediately                   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Red Hat RHCS  = Red Hat Ceph Storage; commercial distribution with SLA-backed enterprise support     │
│  Sev 1         = Production down; data at risk or I/O halted; 24×7 immediate response required        │
│  Sev 2         = Degraded production; reduced redundancy; 2–4 hour initial response SLA               │
│  sosreport     = Linux system diagnostics collector; required attachment for all Red Hat cases        │
│  ceph report   = Full cluster state JSON snapshot; ceph report > ceph-report.json for support         │
│  ceph crash    = Daemon crash report store; ceph crash info <id> provides traceback and context       │
│  ceph-users ML = Upstream mailing list; community support for non-RHCS Ceph deployments               │
│  GitHub issues = ceph/ceph repository; upstream bug tracking and community Ceph case management       │
│  IRC/Slack     = #ceph on OFTC IRC and ceph.io Slack; real-time community support channel             │
│  vendor TAM    = Technical Account Manager; Red Hat named escalation contact for Premier subscribers  │
│  support bundle= sosreport + ceph report + OSD journal; standard data set for vendor cases            │
│  HEALTH_ERR    = Threshold for Sev 1 escalation; any HEALTH_ERR with inactive PGs → immediate case    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Severity Levels

| Severity | Definition | Response SLA |
|---|---|---|
| Sev 1 | Cluster down; all I/O blocked; data at risk | 1 hour (24×7) |
| Sev 2 | Major function degraded; partial I/O loss | 4 business hours |
| Sev 3 | Non-critical warnings; HEALTH_WARN with workaround | 1 business day |
| Sev 4 | General question or planning guidance | 2 business days |

## Required Data for Support Case

```bash
# Run before opening any Red Hat Ceph case:

# 1. Ceph status bundle
ceph status > /tmp/ceph-status.txt
ceph health detail >> /tmp/ceph-status.txt
ceph osd dump >> /tmp/ceph-status.txt
ceph osd tree >> /tmp/ceph-status.txt
ceph pg dump >> /tmp/ceph-status.txt
ceph config dump >> /tmp/ceph-status.txt
ceph crash ls >> /tmp/ceph-status.txt

# 2. Ceph version
ceph version > /tmp/ceph-version.txt
ceph versions >> /tmp/ceph-version.txt

# 3. Affected daemon logs (last 2000 lines per daemon)
ceph orch daemon logs osd.5 > /tmp/osd5.log
journalctl -u ceph-mon@$(hostname) -n 2000 --no-pager > /tmp/mon.log

# 4. OS and hardware info from affected nodes
sos report --batch --label ceph  # Red Hat sosreport (RHCS nodes)

# 5. Crash dumps
ceph crash info $(ceph crash ls | awk '{print $1}') > /tmp/crash-dumps.txt

# Compress for upload
tar czf ceph-case-data-$(date +%F).tar.gz /tmp/ceph-*.txt /tmp/osd*.log /tmp/mon.log
```

## Escalation Path

```text
1. Open case at access.redhat.com (RHCS subscription required)
   - Set severity based on impact
   - Attach ceph-case-data bundle
   - Provide: Ceph version, cluster size (#nodes, #OSDs), symptoms, timeline

2. For Sev 1: call Red Hat support immediately after opening case
   - Phone number on access.redhat.com

3. If no progress in 2-4 hours: request case escalation
   - Ask CEE (Customer Engagement Engineer) to escalate to Ceph team

4. If TAM assigned: contact TAM directly for critical situations

Community Ceph (upstream, no support contract):
  - ceph-users mailing list: ceph-users@ceph.io
  - IRC: #ceph on OFTC
  - GitHub: https://github.com/ceph/ceph/issues (for bugs)
  - Forum: https://forum.ceph.io
```

## Emergency Recovery Commands

```bash
# Cluster completely unresponsive — emergency recovery steps:

# 1. Check MON quorum (minimum 2 of 3 must be up)
ceph mon stat

# 2. If no quorum: check MON services
for host in ceph-node1 ceph-node2 ceph-node3; do
    ssh $host "systemctl status ceph-mon@$host"
done

# 3. Recover MON from monmap (advanced — contact support first)
# ceph-mon --extract-monmap /tmp/monmap --mon-data /var/lib/ceph/mon/ceph-$host

# 4. If OSDs won't start after cluster crash
# Set cluster as active even without full quorum
# WARNING: risk of data inconsistency — contact Red Hat first

# 5. Cluster full stop (halt all writes for investigation)
ceph osd set pause  # pause all OSD I/O
# Resume:
ceph osd unset pause
```
