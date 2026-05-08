# Dell VPLEX — Standards

## Sizing Guidelines

| Parameter | Guidance |
|---|---|
| Virtual volume size | Maximum virtual volume size determined by GeoSynchrony version; check release notes |
| Write cache per director | Cache size is fixed per director model; do not exceed 70% cache utilisation under sustained write workloads |
| Backend IOPS budget | Sum of all virtual volume IOPS must not exceed the backend array's rated IOPS after accounting for RAID overhead |
| ICL bandwidth (Metro) | ICL bandwidth must exceed peak write throughput at either site; provision 2× expected write bandwidth for headroom |
| Director port count | Allocate front-end ports based on host count and bandwidth requirements; maintain port balance across directors within an engine |
| Consistency groups | One consistency group per multi-volume application; do not exceed documented CG limits per GeoSynchrony version |

## Naming Conventions

| Object | Format | Example |
|---|---|---|
| Virtual Volume | `vv-<app>-<env>-<nn>` | `vv-oracle-prod-01`, `vv-sql-dev-02` |
| Local Device | `ld-<app>-<env>-<nn>` | `ld-oracle-prod-01` |
| Distributed Device (Metro) | `dd-<vv-name>` | `dd-vv-oracle-prod-01` |
| Consistency Group | `cg-<app>-<env>` | `cg-oracle-prod`, `cg-sql-dev` |
| Storage View | `sv-<hostname>` | `sv-db-prod-01`, `sv-esxi-prod-04` |
| Initiator | `<hostname>-hba<n>` | `db-prod-01-hba0`, `db-prod-01-hba1` |
| Port (front-end) | `<cluster>-director-<n>-<port>` | Follows VPLEX default naming; document in CMDB |
| Extent | `ext-<storage-volume-name>` | Follows VPLEX auto-naming convention |
| Storage Volume | `sv-<array>-<lun-id>` | Descriptive name matching backend array LUN |

## Build Baseline

Every VPLEX deployment should be configured to the following baseline before handover to operations:

**Consistency Group Policy**

- All multi-volume applications must be in a consistency group to ensure write-order fidelity across volumes.
- Single-volume applications should still be placed in a consistency group for Metro deployments to enable coordinated failover.
- Consistency group membership is set at provisioning time and should not change without a change record.

**Metro Configuration**

- All production distributed devices must span both Metro clusters.
- The Witness VM must be deployed in a third failure domain (not co-located at either Metro site) and connectivity from both clusters must be verified before go-live.
- ICL links must be redundant (minimum two physical paths); link utilisation should be monitored and must remain below 70% under peak load.

**WAN Link Redundancy**

- Provision at least two independent ICL paths between Metro clusters using different physical routes.
- Configure ICL link monitoring and alert on any link failure immediately.

## Configuration Checklist

Complete this checklist before signing off a new VPLEX deployment or a post-change validation:

- [ ] All directors online and healthy: `ll /engines/*/directors/*/hardware/`
- [ ] Inter-cluster link (ICL) healthy and RTT ≤5ms for Metro: `ll /clusters/*/inter-cluster-links/`
- [ ] Witness reachable from both clusters and quorum status healthy
- [ ] All distributed devices in a healthy sync state: `ll /distributed-storage/distributed-devices/*/health-indications/`
- [ ] All consistency groups healthy and containing the correct distributed devices
- [ ] All storage views contain the correct initiators, front-end ports, and virtual volumes
- [ ] Hosts can see virtual volumes and multipath drivers report all expected paths active
- [ ] Backend array storage volumes correctly claimed and not directly visible to hosts outside of VPLEX
- [ ] Full health check passing: `health-check --full`
- [ ] CMDB updated with storage view-to-host-to-virtual volume mappings
- [ ] VMS VM is backed up and backup verified
