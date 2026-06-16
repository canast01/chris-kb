---
tags:
  - troubleshooting
  - dr-operations
  - backup
  - known-issues
---
# DR Operations — Known Issues and Error Codes

<div class="kb-summary">
Catalog of known issues in DR runbook operations covering failover testing, network re-IP, DNS cutover, and application restart sequencing.

*Applies to: DR operations across all platforms*
</div>

```text
┌──────────────────────────────────────────── DR Operations ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Cross-platform DR runbooks — failover testing, re-IP, DNS cutover, app sequencing       │   │
│   │            Protocols: DNS · replication-specific (SRDF/SnapMirror/Veeam) · AD/LDAP            │   │
│   │               Management: DR runbook documents / SRM or equivalent orchestration              │   │
│   │          Declare DR -> Storage failover -> Network cutover -> App startup -> Validate         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Storage           │  │     Array/VM replication    │  │   SRDF, SnapMirror, Veeam   │   │
│   │           Network           │  │      Re-IP / L2 stretch     │  │   DNS delegation per site   │   │
│   │           Identity          │  │      AD/DNS at DR site      │  │     Writable DC required    │   │
│   │          Sequencing         │  │        Runbook order        │  │      DB-mid.ware-app-LB     │   │
│   │          Validation         │  │         Smoke tests         │  │     App-specific checks     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    DR runbook    │ Documented steps │        N/A        │   Change appr.   │  Test quarterly  │   │
│   │   DNS cutover    │  Redirect to DR  │      DNS (53)     │      Admin       │Pre-stage records │   │
│   │     AD at DR     │ Auth continuity  │   LDAP/Kerberos   │   Domain admin   │ Need writable DC │   │
│   │   App sequence   │ Ordered startup  │    App-specific   │  Service accts   │ Doc dependencies │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: production site - DR site - WAN/replication link - DR test network                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RPO            = Recovery Point Objective; max acceptable data loss in time                          │
│  RTO            = Recovery Time Objective; max acceptable time to restore service                     │
│  Runbook        = step-by-step documented procedure for executing DR failover                         │
│  Failover test  = isolated-network DR exercise that does not impact production                        │
│  Re-IP          = changing a host IP to match the DR site network                                     │
│  L2 extension   = stretching a VLAN across sites so DR keeps the same IP space                        │
│  Writable DC    = AD domain controller that can process auth, not just RODC                           │
│  DNS delegation = authority for a DNS zone handed to the DR site name servers                         │
│  CDP            = Continuous Data Protection; near-zero RPO replication                               │
│  Reprotect      = re-establishing replication reverse direction after failover                        │
│  Dependency map = documented start order required for an app to come up                               │
│  Tabletop test  = DR test run as discussion only, without an actual failover                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- DR test failures are almost always sequencing or network issues, not storage failures.
- Always verify: DNS cutover, network re-IP, application dependency order, and authentication (AD/LDAP) at DR site before declaring DR success.

## Failover Testing

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Application accessible but returning stale data | Test failover using isolated network; production data not replicated to test environment | Use production replicas for tests; or create a dedicated DR test environment with data clone |
| DNS not resolving DR site FQDNs | DNS delegation to DR site DNS not configured | Pre-configure DR DNS servers with all application FQDNs before DR test |
| AD authentication failing at DR site | AD DCs at DR site not reachable or not promoted | Ensure at least one writable DC is at DR site; test AD replication health before failover |
| Applications start in wrong order (dependency failures) | Runbook sequence incorrect | Document and test startup sequence: DB → middleware → app → load balancer |

## Network Re-IP

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| Servers have same IP at DR as production (IP conflict) | DR network is a copy of production; L2 extension used | Use L3 re-IP at DR site; or L2 extension with appropriate isolation |
| Load balancer VIPs not responding at DR | VIP not migrated or physical LB not configured at DR | Configure DR load balancer VIPs in advance; test via DR network before production failover |

## Storage

| Error / Symptom | Cause | Workaround / Fix |
|---|---|---|
| DR VM starts but filesystem read-only | Replication-based copy has filesystem journal in unclean state | Mount with recovery: `mount -o remount,rw /dev/<device>` (Linux) or run `chkdsk` (Windows) |

## See also

- [DR Operations — Common Issues](common-issues.md)
- [Veeam — Known Issues](../../veeam/troubleshooting/known-issues/)
- [VMware SRM — Known Issues](../../../virtualization/vmware/srm/troubleshooting/known-issues/)
