```bash
ssh root@dcnm-dc1.corp.example.com

# DCNM service status
/usr/local/cisco/dcm/dcnm/sbin/dcnm-server status
# All services should show as running

# Disk usage
df -h
# Alert if /var/lib/pgsql or /var/dcnm is > 80% used

# Database size
du -sh /var/lib/pgsql/data/

# Check DCNM server log for errors
grep -i "ERROR\|SEVERE\|Exception" /var/log/dcnm/server.log | tail -50

# NTP status
timedatectl status
# Expected: synchronized: yes
```

```text
┌───────────────────────────────────── Cisco DCNM — Health Checks ──────────────────────────────────────┐
│                                                                                                       │
│  DCNM health checks: dashboard alerts, switch status, ISL load, zone consistency.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            DCNM Dashboard Health             │  │             Switch-Level Health             │   │
│   │       SNMP alerts: active by severity        │  │          show system health: all OK         │   │
│   │        Fabric topology: no split VSAN        │  │          show environment: temp/PSU         │   │
│   │          Port inventory: no offline          │  │          show interface: no errors          │   │
│   │         NX-OS currency: < 2 versions         │  │          show version: verify build         │   │
│   │          Zone set: saved == active           │  │         show flogi database: logins         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DCNM dashboard and MDS show commands are first-line health checks; run daily.                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              ISL & VSAN Health               │  │             DCNM Platform Health            │   │
│   │        show interface trunk: ISL util        │  │          DCNM services: all running         │   │
│   │           ISL > 70% util: add more           │  │             DB: disk usage < 80%            │   │
│   │            show vsan: all active             │  │          HA sync: primary = standby         │   │
│   │        Credit starvation: pause check        │  │           Backup: last job success          │   │
│   │           Port error rate < 10/day           │  │          Cert expiry > 60 days left         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Cisco MDS switch chassis · SFP transceivers · ISL FC cables · DCNM VM resources                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  show system health= MDS NX-OS command; reports module and fabric health status                       │
│  show environment = MDS NX-OS; shows temperature, fan, and PSU sensor readings                        │
│  show flogi database= FC login database; verifies all HBAs are logged into fabric                     │
│  show vsan        = VSAN state; confirms all VSANs are active and not suspended                       │
│  show interface trunk= ISL trunk status and utilisation counters                                      │
│  Credit starvation= FC flow control issue; BB credits exhausted; causes pause                         │
│  Zone set saved   = saved zone database should match active; divergence = risk                        │
│  DCNM HA sync    = primary and standby DCNM databases must be synchronised                            │
│  Cert expiry      = TLS certificate monitored; alert 60 days before expiry                            │
│  NX-OS currency   = keep MDS within 2 major versions of latest supported release                      │
│  Backup status    = nightly DCNM backup job result; alert on failure                                  │
│  VSAN split       = VSAN partition causing isolation; major incident requiring fix                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# On MDS switch to verify zone set consistency
show zoneset active vsan <vsan-id>
# Compare against expected zone set exported from DCNM
```
