---
tags:
  - dell
---
# Dell ECS

<div class="kb-summary">
Scale-out software-defined object storage — S3, Swift, and CAS APIs, geo-distributed Virtual Data Centers, multi-tenant namespaces, and compliance retention for petabyte-scale unstructured data workloads.

*Applies to: ECS 3.x*
</div>

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>

## Overview

Dell ECS (Enterprise Content Storage) is a scale-out, software-defined object storage platform supporting S3, Swift, Atmos, and CAS (Content Addressable Storage) APIs. It is deployed as clusters of commodity nodes and can be stretched across multiple sites as Virtual Data Centers (VDCs) connected into geo-distributed replication groups. ECS is the successor to EMC Atmos and is designed for unstructured data at petabyte scale, providing multi-tenancy through namespaces and buckets.

## Where It Fits

| Use Case |
|---|
| Primary object storage back-end for applications using S3-compatible APIs (analytics, media, archival) |
| Long-term retention and compliance storage with CAS (fixed-content, WORM) |
| Geo-distributed active-active object storage across multiple data centres using VDC replication groups |
| Multi-tenant storage service — separate namespaces and IAM policies per team or application |
| On-premises alternative to public cloud object storage where data sovereignty or latency requirements apply |
| Integration target for backup software (Veeam, Commvault) using S3 or CAS interfaces for immutable backup copies |

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Log in to the ECS Portal and review the Dashboard → Alerts panel for a |  |  |
| Check the ECS Portal Dashboard → Capacity view to confirm cluster util |  |  |
| Check ECS Portal → Geo Monitoring to verify geo-replication lag betwee |  |  |
| Query `GET /vdc/capacity` via the Management REST API to retrieve curr | `GET /vdc/capacity` |  |
| Query `GET /vdc/nodes` to confirm all nodes report as `GOOD` status | `GET /vdc/nodes` |  |
| Review ECS Portal → Hardware to confirm all node disks are healthy wit | `FAILED` |  |
| Check namespace and bucket usage growth trends to identify unexpected |  |  |

## Health Commands

```bash
# Authenticate to the ECS Management REST API (returns X-SDS-AUTH-TOKEN header)
curl -s -k -u "sysadmin:<password>" \
  "https://<ecs-node>:4443/login" -D -

# Retrieve VDC capacity (total, used, available, percent full)
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/capacity"

# List all nodes and their health status
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/nodes"

# Retrieve active alerts for the VDC
curl -s -k -H "X-SDS-AUTH-TOKEN: <token>" \
  "https://<ecs-node>:4443/vdc/alerts"

# List namespaces (ecscli)
ecscli namespace list

# List buckets in a namespace (ecscli)
ecscli bucket list --namespace <namespace>

# Get bucket metadata including versioning, quota, replication group
ecscli bucket get --namespace <namespace> --name <bucket>
```

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Node shows `DEGRADED` or offline in portal | Disk failure, NIC fault, or node OS crash | Check ECS Portal → Hardware for disk state; check node OS logs via SSH; replace failed disk via guided procedure |
| Geo-replication lag growing between VDCs | WAN link saturation, remote VDC node issue, or replication group misconfiguration | Check ECS Portal → Geo Monitoring; review bandwidth utilisation on inter-site link; verify remote VDC is healthy |
| S3 access denied despite correct credentials | IAM policy misconfiguration, wrong namespace, or bucket policy conflict | Confirm namespace and IAM user assignment; check bucket policy with `ecscli bucket get`; verify S3 endpoint and path-style vs virtual-hosted-style addressing |
| Capacity growing unexpectedly | Bucket versioning accumulating old versions, incomplete multipart uploads, or lifecycle policy absent | Check versioning status on buckets; list and abort incomplete multipart uploads via S3 API; add lifecycle policies to expire old versions |
| ECS Portal login fails | Management service down or certificate expired | Check service status on node; restart ECS portal service if needed; verify TLS certificate expiry |
| Bucket quota exceeded, writes failing | Bucket or namespace quota threshold reached | Increase quota via ECS Portal → Buckets → Edit, or expire old objects; review lifecycle rules |

## Operational Tasks

| Task | Command |
|---|---|
| Create a namespace per team or application via ECS Portal → Namespace → New, and |  |
| Create a bucket within a namespace, configure replication group, versioning, and |  |
| Create IAM users and assign S3 access keys within the namespace for application |  |
| Configure a lifecycle policy on a bucket to transition or expire objects after a |  |
| Add a new node to an existing VDC via ECS Portal → Hardware → Add Node; ECS will |  |
| Configure geo-replication by adding a remote VDC to the replication group and se |  |
| Rotate object user secret keys with `ecscli user secret-key create` and update c |  |
| Run capacity and performance reports from ECS Portal → Dashboard for capacity pl |  |

## Upgrade Notes

| Step | Action |
|---|---|
| 1 | Confirm the current ECS software version via ECS Portal → Settings → Software Update and record it before proceeding |
| 2 | Review the Dell ECS release notes for the target version; note any configuration changes or mandatory interim upgrades required |
| 3 | Verify all nodes are healthy (`GOOD`) and geo-replication lag is at zero before starting the upgrade |
| 4 | Download the upgrade package from Dell Support and upload it to the ECS upgrade staging area via the Portal |
| 5 | ECS upgrades are rolling (one node at a time); the portal will indicate per-node progress — do not force simultaneous node upgrades |
| 6 | After all nodes upgrade, confirm all nodes return to `GOOD` status and geo-replication resumes with no lag |
| 7 | Validate S3, Swift, and other API endpoints with a quick functional test from each consuming application or namespace |

## Best Practices

| Recommendation | Detail |
|---|---|
| Separate namespaces per team or application | do not share a single namespace across unrelated workloads |
| Enable bucket versioning only where application recovery requirements demand it | versioning causes unbounded capacity growth without lifecycle policies |
| Always attach a lifecycle policy to versioned buckets to | Always attach a lifecycle policy to versioned buckets to expire non-current versions after the required retention period |
| Use replication groups spanning at least two VDCs for any | Use replication groups spanning at least two VDCs for any production data to achieve geo-redundancy |
| Configure namespace and bucket quotas to prevent a single | Configure namespace and bucket quotas to prevent a single tenant from consuming cluster-wide capacity |
| Authenticate to the Management API with a service account | Authenticate to the Management API with a service account rather than the `sysadmin` default credential in automation scripts |
| Monitor cluster utilisation and plan capacity expansion before reaching 70% of usable space | ECS performance degrades as utilisation approaches 85% |
| Document replication group topology and VDC peering configuration | changes to replication groups are difficult to reverse without data movement |
