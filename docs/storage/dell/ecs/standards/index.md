# ECS Standards
## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| VDC name | `<site-code>-ecs-vdc<n>` | `lon01-ecs-vdc1` |
| Replication group | `<primary-site>-<secondary-site>-rg<n>` | `lon01-ams01-rg1` |
| Namespace | `<team>-<env>` (lowercase, hyphen-separated) | `analytics-prod` |
| Bucket | `<namespace>-<purpose>-<optional-tier>` | `analytics-prod-raw-s3` |
| IAM user (object user) | `svc-<app>-<env>` | `svc-veeam-prod` |
| ECS node hostname | `<site>-ecs-n<node-number>` | `lon01-ecs-n01` |
| Management service account | `svc-ecs-mgmt` | — |
| Replication policy profile | `<rpo-minutes>min-<consistency>` | `15min-async` |

## Build and Deployment Baseline

- Deploy ECS via the Dell ECS Installation and Configuration Guide; do not deviate from the supported hardware bill of materials
- Each VDC must have a minimum of 4 nodes for production; 3-node clusters are not supported for the default 12+4 erasure coding scheme
- All nodes in a VDC must run the same ECS software version; mixed-version clusters are unsupported
- Assign a dedicated management IP and data IP per node; separate management and data traffic onto different VLANs or NICs
- Configure NTP on all nodes to a consistent time source — ECS geo-replication consistency depends on clock synchronisation across VDCs
- Enable syslog forwarding from ECS nodes to a centralised log management platform at deployment
- Create a dedicated management service account (`svc-ecs-mgmt`) for API automation; never use `sysadmin` in automation scripts
- Document the replication group topology (VDC names, replication mode, RPO) in the site runbook before go-live
- Configure namespace and bucket quotas from the outset; unconstrained namespaces are a capacity risk

## Configuration Checklist

- [ ] All nodes visible in ECS Portal → Hardware with status `GOOD`
- [ ] NTP configured and synchronised on all nodes (`date` output matches across nodes)
- [ ] Syslog forwarding configured and events visible in the SIEM
- [ ] Management REST API accessible over HTTPS on port 4443; self-signed certificate replaced with a signed certificate
- [ ] Admin service account `svc-ecs-mgmt` created; default `sysadmin` password changed
- [ ] Replication group created and remote VDC connectivity verified (geo-replication lag = 0 at steady state)
- [ ] Each namespace has an assigned replication group and a quota (hard or advisory)
- [ ] Bucket versioning enabled only on buckets with a corresponding lifecycle policy to expire non-current versions
- [ ] Lifecycle policies configured on all versioned buckets
- [ ] S3 API endpoint TLS certificate is signed and trusted by consuming applications
- [ ] Baseline `GET /vdc/nodes` and `GET /vdc/capacity` outputs captured and stored in the runbook
- [ ] SNMP or syslog alerting configured for node or disk failure events
- [ ] IAM users created per application with least-privilege bucket policies; no use of the root/admin object user in applications
- [ ] Geo-replication tested: write an object to one VDC and confirm it is readable from the remote VDC
