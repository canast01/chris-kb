# RecoverPoint — Health Checks

```bash
# SSH to RPA cluster management IP
ssh admin@<rpa-cluster-ip>

# RPA cluster and node health
system status

# All CGs — expect ACTIVE for all production CGs
groups status

# Detailed CG view including lag, RPO, and journal fill
groups status detail

# Journal utilization for all CGs
journals list

# Active alarms (hardware and software)
alarms list

# Inter-site link statistics (latency, bandwidth)
links statistics

# Cluster quorum state
cluster quorum check
```text
┌──────────────────────────────────── RecoverPoint — Health Checks ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Health check cadence: daily CG lag/journal, weekly test copy, monthly failover drill     │   │
│   │       Critical alerts: CG in error state, journal >90% full, RPA node failure, link down      │   │
│   │         Check sources: Unisphere for RP, vCenter plugin, SNMP traps, REST API polling         │   │
│   │            Baseline: all CGs Active; lag <30 s; journal <70%; all RPA nodes Online            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          RPA Health         │  │          CG Health          │  │         Link Health         │   │
│   │      Node state: Online     │  │        State: Active        │  │        Link state: Up       │   │
│   │          CPU < 80%          │  │         Lag < 30 sec        │  │       Latency < 100 ms      │   │
│   │         Memory < 85%        │  │        Journal < 70%        │  │        Packet loss 0%       │   │
│   │          Fan/PSU OK         │  │       Splitter loaded       │  │        BW util < 80%        │   │
│   │          NTP synced         │  │        No errors 24 h       │  │        Compression OK       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Physical: RPA hardware health viewable in Unisphere; splitter state visible per ESXi host          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CG state Active  = Replication is running; writes being journaled; lag within RPO target           │
│    Lag (RPO lag)    = Seconds between last source write and journal apply on target; primary KPI      │
│    Journal fill %   = Consumed / allocated journal VMDK; >90% causes CG to pause replication          │
│    Splitter loaded  = ESXi kernel module active; check per host in Unisphere splitter view            │
│    SNMP traps       = RPA sends traps to NMS on CG error, journal fill, and RPA node failure          │
│    Link utilisation = WAN replication bandwidth; sustained >80% may cause lag increase                │
│    NTP sync         = Critical for journal timestamps and cross-site consistency; must be in sync     │
│    Packet loss      = Any loss on replication link degrades throughput; investigate immediately       │
│    RPA node failure = Surviving RPA takes over all CGs; CGs continue with reduced throughput          │
│    Unisphere alert  = Red badge in Unisphere dashboard; drill down to CG, link, or hardware           │
│    REST poll        = GET /system/clusters; /groups; /links; use for monitoring integration           │
│    Monthly drill    = Full failover test with VM power-on at DR site; documents RTO achieved          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# List journal volumes with utilization
journals list

# Expected output columns:
#   Journal Name   CG Name         Used%   Free%   Status
#   JRN-CG-ORA-DR  CG-ORACLE-PROD  34%     66%     OK
```
```bash
# Confirm splitter health (for RP4VM software splitters on ESXi)
esxcli software vib list | grep -i rp

# Confirm RPA software versions are consistent across cluster
boxmgmt verify_rpa_version

# Review audit log for unexpected operations (logins, image access events)
get_audit_log -last 500

# Confirm DR site RPA cluster is also healthy
ssh admin@<dr-rpa-cluster-ip> "system status"
ssh admin@<dr-rpa-cluster-ip> "groups status"
```
