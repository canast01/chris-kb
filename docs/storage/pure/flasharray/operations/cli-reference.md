---
tags:
  - operations
  - pure
---
# FlashArray — CLI Reference


<div class="kb-summary">
CLI Reference reference covering Admin Accounts, Alerts & Audit, Array & System Management, Configuration & Directory Services, CSV Exports and 5 more sections.

*Applies to: FlashArray Purity 6.x*
</div>
```text
┌─────────────────────────────────── Pure FlashArray — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        FlashArray CLI: command-line interface for all management and operational tasks        │   │
│   │            Access: SSH or REST client to management IP; authenticate as admin role            │   │
│   │        Commands: status, list, create, modify, delete, show, and diagnostic operations        │   │
│   │          Scripting: use REST API or CLI in automation for provisioning and reporting          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH → authenticate → show status → configure → verify → log output                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         Controllers         │  │        Active-active        │  │           No SPOF           │   │
│   │            Drives           │  │         DirectFlash         │  │         NVMe native         │   │
│   │           Volumes           │  │       Thin provisioned      │  │        Instant clone        │   │
│   │        ActiveCluster        │  │       Sync replication      │  │           Zero RPO          │   │
│   │           SafeMode          │  │       Immutable snaps       │  │      Ransomware resist      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Category     │     Command      │      Purpose      │      Output      │      Notes       │   │
│   │      Status      │   show status    │    Health check   │   State/alerts   │    Daily run     │   │
│   │       List       │     list all     │     Inventory     │   Name/ID/size   │    Read-only     │   │
│   │      Create      │  create volume   │     Provision     │    New object    │    Change req    │   │
│   │      Delete      │ delete resource  │    Decommission   │   Confirmation   │   Irreversible   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FlashArray//X or //C controllers · DirectFlash NVMe modules · 25/100 GbE / 32Gb FC       │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashArray         = Pure all-NVMe block/file array; inline dedup and compression always enabled   │
│    DirectFlash        = Pure proprietary NVMe modules; direct flash access without SAS translation    │
│    ActiveCluster      = synchronous active-active stretch cluster; hosts see a single namespace       │
│    ActiveDR           = asynchronous replication to DR site; recovery point objective in seconds      │
│    SafeMode           = admin-locked immutable snapshots; cannot be deleted even by array administr...│
│    Protection group   = set of volumes and hosts sharing a snapshot and replication schedule          │
│    purefa CLI         = REST CLI tool for FlashArray; purefa CLI connects via REST API key            │
│    purearray          = purectl CLI command: purearray list and purearray show monitoring             │
│    Volume tag         = user-defined key-value label on volumes for policy and reporting purposes     │
│    Host group         = logical collection of hosts sharing volume access via a host group object     │
│    Inline dedup       = content-based deduplication performed inline before data is written to flash  │
│    Evergreen          = Pure architecture; controllers upgrade non-disruptively, shelves remain in ...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


```text
Purity CLI Hierarchy
  purity
  ├── purearray   — array identity, NTP, DNS, upgrade, phonehome
  ├── purevol     — volumes: create / resize / connect / snap
  ├── purehost    — host entries: WWN/IQN registration
  ├── purehgroup  — host groups: cluster-level volume masking
  ├── purepgroup  — protection groups: snapshot + replication
  ├── purepod     — ActiveCluster pods: sync replication
  ├── puredrive   — drive health and status
  ├── purehw      — hardware components (fans, PSU, NVRAM)
  ├── pureport    — FC and Ethernet port info + WWNs
  ├── purealert   — alert management
  ├── pureaudit   — audit log
  └── pureadmin   — user accounts, roles, API tokens
```

Commonly used Purity CLI commands for managing Pure FlashArray all-flash storage systems. Connect via SSH to the array's management IP and log in as `pureuser` or another admin account.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Admin Accounts

Admin accounts control who can log in and what they can do. Pure supports role-based access and API tokens for automation.

```bash
# Create user with API token
pureadmin create testuser --api-token
pureadmin create testuser --api-token --timeout 2h
pureadmin create testuser --role storage_admin

# Delete user / token
pureadmin delete --api-token
pureadmin delete testuser
pureadmin delete testuser --api-token

# Global settings
pureadmin global list
pureadmin global list --lockout
pureadmin global disable --single-sign-on
pureadmin global enable --single-sign-on
pureadmin global setattr --lockout-duration 1m
pureadmin global setattr --max-login-attempts 3
pureadmin global setattr --min-password-length 8

# List accounts
pureadmin list
pureadmin list --api-token
pureadmin list --api-token --expose
pureadmin list --lockout

# Manage lockouts and attributes
pureadmin refresh testuser
pureadmin refresh --clear
pureadmin refresh --clear testuser
pureadmin reset testuser --lockout
pureadmin setattr testuser --password
pureadmin setattr testuser --role array_admin
```

---

## Alerts & Audit

Alerts notify you when something needs attention. The audit log records every command run by every user.

### purealert — Alerts

```bash
purealert list
purealert list --flagged
purealert list --filter "state='open'"
purealert list --filter "state='closed'"
purealert list --filter "severity='critical'"
purealert list --filter "issue='failure'"
purealert flag 121212
purealert unflag 121212
purealert acknowledge <ID>
```

### pureaudit — Audit Logs

```bash
pureaudit list
pureaudit list --limit 10
pureaudit list --sort user
pureaudit list --filter 'user = "root"'
pureaudit list --filter 'command="purepod"'
pureaudit list --filter 'command="purepod" and subcommand="create"'
pureaudit list --filter 'command="purepod" and user="pureuser"'
pureaudit list --filter "action='create'"
```

---

## Array & System Management

Shows the array's identity, monitors overall performance, and configures system-level settings.

```bash
# Array identity and attributes
purearray list
purearray list --controller
purearray list --space
purearray list --ntpserver
purearray list --syslogserver
purearray list --banner
purearray list --console-lockout
purearray list --connection-key

# Performance monitoring
purearray monitor
purearray monitor --latency
purearray monitor --bandwidth
purearray monitor --iops
purearray monitor --size
purearray monitor --queue-depth

# Configure array settings
purearray setattr --name <new_name>
purearray setattr --banner <text>
purearray setattr --idle-timeout <mins>
purearray setattr --scsi-timeout <secs>
purearray setattr --proxy <url>

# Upgrades
purearray upgrade list
purearray upgrade download --version <v>

# Phonehome / remote support
purearray phonehome list
purearray phonehome send
purearray remoteassist --action open
purearray remoteassist --action close
purearray remoteassist --status
```

---

## Configuration & Directory Services

`pureconfig` shows you the current array configuration. `pureds` integrates with Active Directory or LDAP. `puredns` sets the array's DNS resolver.

```bash
# pureconfig — current array configuration
pureconfig list
pureconfig list --all
pureconfig list --object
pureconfig list --object <type>
pureconfig list --system

# pureds — directory services (Active Directory / LDAP)
pureds list
pureds check

# puredns — DNS configuration
puredns list
puredns setattr --domain test.com --nameservers 192.168.0.10,192.168.2.11
puredns setattr --domain ""
puredns setattr --nameservers ""
```

---

## CSV Exports

Use `--csv` with any list command to export data. Use SSH redirection to save to a local file.

```bash
ssh pureuser@<array_ip> "purevol list --csv" > local_file.csv
```

### Array & System

```bash
purearray list --csv > array_inventory.csv
purearray list --space --csv >> array_inventory.csv
purearray list --controller --csv >> array_inventory.csv
purearray list --ntpserver --csv >> array_inventory.csv
purearray list --syslogserver --csv >> array_inventory.csv
purearray monitor --csv >> array_performance.csv
purearray monitor --latency --csv >> array_performance.csv
purearray monitor --bandwidth --csv >> array_performance.csv
purearray monitor --iops --csv >> array_performance.csv
purearray monitor --size --csv >> array_performance.csv
purearray monitor --queue-depth --csv >> array_performance.csv
purearray list --connection-key --csv >> array_config.csv
purearray phonehome list --csv >> support_history.csv
purearray upgrade list --csv >> system_updates.csv
purearray list --banner --csv >> security_audit.csv
purearray list --console-lockout --csv >> security_audit.csv
purearray remoteassist --status --csv >> support_history.csv
```

### Volumes & Data

```bash
purevol list --csv > volume_report.csv
purevol list --all --csv >> volume_report.csv
purevol list --snap --csv >> volume_report.csv
purevol list --pending-only --csv >> volume_report.csv
purevol list --space --csv >> volume_report.csv
purevol list --shared --csv >> volume_report.csv
purevol list --snap --space --csv >> snapshot_usage.csv
purevol list --filter "size > 100G" --csv >> filtered_volumes.csv
purevol monitor --csv > volume_performance.csv
purevol monitor --historical 24h --csv >> volume_performance.csv
```

### Hosts & Connectivity

```bash
purehost list --csv > host_mapping.csv
purehost list --all --csv >> host_mapping.csv
purehost list --connect --csv >> active_connections.csv
purehost list --wwn --csv >> initiator_list.csv
purehost list --iqn --csv >> initiator_list.csv
purehost monitor --bandwidth --csv >> host_performance.csv
purehost monitor --iops --csv >> host_performance.csv
purehgroup list --csv > group_mapping.csv
purehgroup list --host --csv >> group_mapping.csv
purehgroup list --space --csv >> group_mapping.csv
```

### Hardware & Health

```bash
purehw list --csv > hardware_health.csv
purehw list --type eth --csv >> hardware_health.csv
purehw list --type fc --csv >> hardware_health.csv
purehw list --type bay --csv >> hardware_health.csv
purehw list --type fan --csv >> hardware_health.csv
purehw list --type psu --csv >> hardware_health.csv
purehw list --type nvram --csv >> hardware_health.csv
purehw list --type sas --csv >> hardware_health.csv
puredrive list --csv > drive_inventory.csv
pureport list --csv > port_config.csv
pureport list --initiator --csv >> port_config.csv
```

### Admin & Security

```bash
pureadmin list --csv > admin_users.csv
pureadmin list --lockout --csv >> security_report.csv
pureadmin list --api-token --csv >> admin_users.csv
purealert list --csv > system_alerts.csv
purealert list --filter "state='open'" --csv >> critical_alerts.csv
pureaudit list --csv > audit_trail.csv
pureds list --csv > directory_services.csv
puredns list --csv >> network_config.csv
```

---

## Drives & Hardware

Shows the health of flash drives and hardware components. Drives are identified by bay (e.g., `CH0.BAY10`).

```bash
# puredrive — flash drives
puredrive list
puredrive list --spec
puredrive list --total
puredrive list CH0.BAY10
puredrive list CH0.BAY10 --pack
puredrive admit

# purehw — hardware components
purehw list
purehw list --spec
purehw list --type bay
purehw list --type bay --spec
purehw list --type ct
purehw list --type eth
purehw list --type fc
purehw list --type fan
purehw list --type psu
purehw list --type nvram
purehw list --type sas
purehw list --spec --type drive
purehw list CT0 --spec
purehw list CT0.FC0
```

---

## Hosts & Host Groups

A host represents a server connecting to the array. Host groups manage access for multiple servers at once.

### purehgroup — Host Groups

```bash
# Create / delete / rename
purehgroup create MY-HOSTS
purehgroup create MY-HOSTS --hostlist MY-HOST-001,MY-HOST-002
purehgroup delete MY-HOSTS
purehgroup delete MY-HOSTS_1 MY-HOSTS-2
purehgroup rename MY-HOSTS YOUR-HOSTS

# List
purehgroup list
purehgroup list --connect
purehgroup list --connect MY-HOSTS
purehgroup list --host
purehgroup list --space
purehgroup list --filter "host_list='MY-SERVER-001'"

# Connect / disconnect volumes
purehgroup connect MY-HOSTS --vol MY_VOL_001
purehgroup connect MY-HOSTS --vol MY_VOL_001 --lun 100
purehgroup disconnect MY-HOSTS --vol MY_VOL_001

# Manage host membership
purehgroup setattr MY-HOSTS --hostlist MY-HOST-002,MY-HOST-003
purehgroup setattr MY-HOSTS --addhostlist MY-HOST-002,MY-HOST-003
purehgroup setattr MY-HOSTS --remhostlist MY-HOST-002,MY-HOST-003
purehgroup setattr MY-HOSTS --hostlist ""
purehgroup addhost --hostlist <h1,h2> <hg>
purehgroup remhost --hostlist <h1> <hg>
```

### purehost — Hosts

```bash
# Create / delete / rename
purehost create MY-SERVER-001
purehost create MY-SERVER-001 --wwnlist 1000000000000001,10:00:00:00:00:00:00:01
purehost create MY-SERVER-001 MY-SERVER-002
purehost delete MY-SERVER-001
purehost delete MY-SERVER-001 MY-SERVER-002
purehost rename MY-SERVER-001 YOUR-SERVER-001

# List
purehost list
purehost list --all
purehost list --connect
purehost list --connect --private
purehost list --connect --shared
purehost list --personality
purehost list --wwn
purehost list --iqn
purehost list MY-SERVER*
purehost list MY-SERVER-001
purehost list MY-SERVER-001 --connect
purehost list MY-SERVER-001 --personality
purehost list --filter "wwn='1000000000000003'"

# Connect / disconnect volumes
purehost connect MY-SERVER-001 --vol MY_VOL_001
purehost connect MY-SERVER-001 --vol MY_VOL_001 --lun 10
purehost connect MY-SERVER-001 MY-SERVER-002 --vol MY_VOL_001
purehost disconnect MY-SERVER-001 --vol MY_VOL_001
purehost disconnect MY-SERVER-001 MY-SERVER-002 --vol MY_VOL_001

# Manage WWNs, iQNs, and personality
purehost setattr MY-SERVER-001 --wwnlist 1000000000000003
purehost setattr MY-SERVER-001 --addwwnlist 1000000000000003
purehost setattr MY-SERVER-001 --remwwnlist 1000000000000003
purehost setattr MY-SERVER-001 --wwnlist ""
purehost setattr MY-SERVER-001 --personality esxi
purehost setattr MY-SERVER-001 --personality solaris
purehost addwwn MY-SERVER-001 --wwn <wwn>
purehost remwwn MY-SERVER-001 --wwn <wwn>
purehost addiqn MY-SERVER-001 --iqn <iqn>

# Monitor
purehost monitor --bandwidth
purehost monitor --iops
```

---

## Network & Ports

`purenetwork` shows IP interfaces. `pureport` shows physical FC and Ethernet ports — needed for SAN zoning.

```bash
# List all network interfaces (management, replication, iSCSI)
purenetwork list
purenetwork list --resolve-hostnames

# List all array ports
pureport list

# FC ports only
pureport list --type fc

# Ethernet ports only
pureport list --type eth

# Filter to a specific controller
pureport list --raw --filter "name='CT0.FC*'"
pureport list --raw --filter "name='CT1.FC*'"

# Show connected host initiator ports
pureport list --initiator

# Filter by WWN
pureport list --initiator --raw --filter "initiator.wwn='1000000000000001'"

# Bandwidth monitoring
pureport monitor --bandwidth
```

### FC Port WWNs (for SAN Zoning)

```bash
pureport list --type fc
# The 'wwn' column shows the array-side WWN for each FC port.
# Zone each host initiator port to the array target WWNs.
```

### Common Port Issues

| Issue | Check | Action |
|---|---|---|
| Host can't see array via FC | Port WWN not zoned | Verify SAN zoning matches `pureport list --type fc` |
| iSCSI sessions not establishing | IP reachability | Ping array iSCSI IP from host |
| Bandwidth below expected | Port speed | `pureport list --type eth` — check link speed |
| Initiator not registering | WWN mismatch | Verify host HBA WWN vs. registered initiator |

---

## Pods (ActiveCluster)

Pods enable synchronous replication between two FlashArray systems (RPO=0, active-active HA across sites).

```bash
# Create / destroy / recover
purepod create MYPOD001
purepod create MYPOD001 MYPOD002
purepod clone MYPOD001 MYPOD002
purepod rename MYPOD001 YOURPOD001
purepod destroy MYPOD001
purepod destroy MYPOD001 MYPOD002
purepod eradicate MYPOD001
purepod eradicate MYPOD001 MYPOD002
purepod recover MYPOD001

# List
purepod list
purepod list MYPOD001
purepod list --pending
purepod list --pending-only
purepod list --footprint
purepod list --mediator
purepod list --failover-preference
purepod list --on ARRAY02
purepod listobj --type vol MYPOD001
purepod listobj --type array MYPOD001

# Stretch / demote / failover
purepod add --array PFAX70-REMOTE MYPOD001
purepod remove --array PFAX70-REMOTE MYPOD001
purepod demote MYPOD001
purepod setattr --failover-preference ARRAY002 MYPOD001

# Replica links
purepod replica-link list
purepod replica-link create PRDPOD001 --remote ARRAY002 --remote-pod DRPOD001
purepod replica-link delete PRDPOD001 --remote-pod DRPOD001
purepod replica-link pause PRDPOD001 --remote ARRAY002 --remote-pod DRPOD001
purepod replica-link resume PRDPOD001 --remote ARRAY002 --remote-pod DRPOD001
purepod replica-link monitor --replication
```

---

## Volumes & Snapshots

Volumes are thin-provisioned block devices. Snapshots are instant, space-efficient point-in-time copies.

```bash
# Create / delete / recover
purevol create --size 10G MY_VOLUME_001
purevol create --size 10G MY_VOLUME_001 --bw-limit 10M
purevol create --size 10G MY_VOLUME_001 MY_VOLUME_002
purevol create --size 1G MYPOD001::MY_VOL_001
purevol create --source <vol> <new_vol>
purevol destroy MY_VOL_001
purevol destroy MY_VOL_001 MY_VOL_002
purevol eradicate MY_VOL_001
purevol eradicate MY_VOL_001 MY_VOL_002
purevol eradicate --all
purevol recover MY_VOL_001
purevol recover --all
purevol rename MY_VOL_001 MY_VOL_002

# List
purevol list
purevol list MY_VOL_001
purevol list MY_VOL*
purevol list --all
purevol list --snap
purevol list --pending
purevol list --pending-only
purevol list --shared
purevol list --obj-name
purevol list --total
purevol list --space --sort size,total
purevol list --snap --space
purevol list --sort size
purevol list --sort size-
purevol list --sort serial
purevol list --sort created
purevol list --filter "size='20T'"
purevol list --filter "size > 100G"

# Connect / disconnect
purevol connect MY_VOL_001 --host MY-SERVER-001
purevol connect MY_VOL_001 --host MY-SERVER-001 --lun 10
purevol connect MY_VOL_001 --hgroup MY-HOSTS
purevol connect MY_VOL_001 MY_VOL_002 --host MY-SERVER-001
purevol disconnect MY_VOL_001 --host MY-SERVER-001
purevol disconnect MY_VOL_001 --hgroup MY-HOSTS

# Modify
purevol setattr --size 2G MY_VOL_001
purevol setattr --size 2G MY_VOL_001 MY_VOL_002
purevol setattr --bw-limit 1M MY_VOL_001
purevol setattr --readonly MY_VOL_001
purevol truncate --size 1G MY_VOL_001

# Copy / move
purevol copy MY_VOL_001 MY_VOL_002
purevol copy MY_VOL_001 MY_VOL_002 --overwrite
purevol copy --snapshot <snap> <target>
purevol move vol001 MYPOD001
purevol move MYPOD001::vol001 ""

# Snapshots
purevol snap MY_VOL_001
purevol snap MY_VOL_001 --suffix PRD
purevol snap MY_VOL_001 --suffix <text>
purevol snap MY_VOL_001 --expiration <time>

# Monitor
purevol monitor
purevol monitor --iops
purevol monitor --latency
purevol monitor --historical 24h

# Pod volume operations
purevol remove --array PFAX70-REMOTE --with-unknown MYPOD001
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
