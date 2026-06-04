# Brocade SANnav — Design Standards

```bash
# Add SNMPv3 user matching SANnav credentials
snmpconfig --set snmpv3 -index 1 -username sannav_mgmt \
  -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> \
  -rwcommunity sannav_rw

# Add SANnav as trap recipient
snmpconfig --set trapdest -index 1 \
  -trapdest <sannav-ip> -severity 4 \
  -username sannav_mgmt -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> -trapport 162

# Verify
snmpconfig --show snmpv3
snmpconfig --show trapdest
```text
┌────────────────────────────────── Brocade SANnav — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│  Design principles: HA deployment, dedicated management VLAN, RBAC, TLS, backups.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Deployment Standards             │  │              Security Standards             │   │
│   │        HA pair: primary + standby VM         │  │         TLS 1.2+ for all web traffic        │   │
│   │           Separate management VLAN           │  │         TACACS+ mandatory; no local         │   │
│   │          4 vCPU / 16 GB RAM minimum          │  │        RBAC: read-only for operators        │   │
│   │            NTP for all timestamps            │  │         SNMPv3 only; disable v1/v2c         │   │
│   │          Dedicated mgmt DNS entries          │  │         IP whitelist for API access         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  HA ensures continuity; dedicated VLAN isolates management traffic from data plane.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Operational Standards             │  │            Scalability Guidelines           │   │
│   │        Backup: daily NFS; 30-day ret.        │  │         Max 1,000 switches per node         │   │
│   │        Alert review: daily MAPS check        │  │          Max 100,000 ports per node         │   │
│   │         Zone changes: change ticket          │  │        Separate instances per fabric        │   │
│   │        Firmware mgmt via SANnav only         │  │           Scale-out: additional VM          │   │
│   │           Quarterly SANnav upgrade           │  │        Storage: 2 TB for 90-day perf        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere host · shared datastore (2 TB+) · management Ethernet switch · NFS backup                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  HA pair         = SANnav primary+standby VMs; standby syncs config and takes over                    │
│  Management VLAN = isolated VLAN for switch OOB and SANnav traffic; no user VLAN                      │
│  RBAC            = Role-Based Access Control; admin/operator/read-only roles in SANnav                │
│  NTP             = Network Time Protocol; all events timestamped; required for SIEM                   │
│  SNMPv3          = SNMP version 3; auth + privacy mode; disable v1/v2c in SANnav                      │
│  IP whitelist     = restrict REST API and management access to known source IPs                       │
│  TLS 1.2+        = minimum TLS version for SANnav HTTPS management GUI                                │
│  NFS backup      = daily SANnav configuration and database backup to NFS share                        │
│  MAPS check      = daily review of Monitoring and Alerting Policy Suite events                        │
│  Change ticket   = ITSM requirement; all zone changes need approved change record                     │
│  90-day perf     = SANnav default performance data retention; requires ~2 TB storage                  │
│  Scale-out       = deploy additional SANnav instances when port count exceeds limit                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
