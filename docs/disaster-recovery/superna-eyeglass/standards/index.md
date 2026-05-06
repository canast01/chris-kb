# Superna Eyeglass Standards

Eyeglass configuration objects should follow a consistent naming convention: SyncIQ policy names use the format `<source-cluster>-<target-cluster>-<zone-or-path>`, and Eyeglass DR configuration groups mirror this naming. SyncIQ policy alignment is mandatory — all policies managed by Eyeglass must have matching share and quota configurations on both clusters before DR readiness can be confirmed.

DNS zone delegation for automated cutover must be pre-configured and validated before any failover test. RPO targets should be defined per SyncIQ policy and configured in Eyeglass to trigger alerts when replication lag exceeds the threshold.

| Standard | Requirement |
|---|---|
| SyncIQ policy naming | `<source>-<target>-<zone>` format |
| Share mapping validation | All shares mapped in Eyeglass before declaring DR-ready |
| Quota mapping validation | All quotas aligned between primary and DR cluster |
| DNS zone delegation | Pre-configured and tested before any failover exercise |
| RPO target | Defined per policy; alert on breach |
| DR readiness score | Must be 100% before scheduled failover tests |
