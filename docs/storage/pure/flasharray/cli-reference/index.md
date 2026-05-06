# Pure Storage CLI Reference

Commonly used Purity CLI commands for managing Pure FlashArray systems.

---

## pureadmin — Administrative Accounts

Displays and manages administrative accounts.

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

## purealert — Alerts

Manages alert history and notification email recipients.

```bash
purealert list
purealert list --flagged
purealert list --filter "state='open'"
purealert list --filter "state='closed'"
purealert list --filter "severity='critical'"
purealert list --filter "issue='failure'"
purealert flag 121212
purealert unflag 121212
```

---

## pureaudit — Audit Logs

Displays and manages audit log records.

```bash
pureaudit list
pureaudit list --limit 10
pureaudit list --sort user
pureaudit list --filter 'user = "root"'
pureaudit list --filter 'command="purepod"'
pureaudit list --filter 'command="purepod" and subcommand="create"'
pureaudit list --filter 'command="purepod" and user="pureuser"'
```

---

## pureconfig — Configuration

Reproduces the current array configuration.

```bash
pureconfig list
pureconfig list --all
pureconfig list --object
pureconfig list --system
```

---

## puredns — DNS

Manages DNS attributes for the array's administrative network.

```bash
puredns list
puredns setattr --domain test.com --nameservers 192.168.0.10,192.168.2.11
puredns setattr --domain ""
puredns setattr --nameservers ""
```

---

## puredrive — Drives

Displays information about Flash Drives and NVRAM modules.

```bash
puredrive list
puredrive list --spec
puredrive list --total
puredrive list CH0.BAY10
puredrive list CH0.BAY10 --pack
puredrive admit
```

---

## purehgroup — Host Groups

Displays and manages Host Group objects.

```bash
# Create / delete
purehgroup create MY-HOSTS
purehgroup create MY-HOSTS --hostlist MY-HOST-001,MY-HOST-002
purehgroup delete MY-HOSTS
purehgroup delete MY-HOSTS_1 MY-HOSTS-2
purehgroup rename MY-HOSTS YOUR-HOSTS

# List
purehgroup list
purehgroup list --connect
purehgroup list --connect MY-HOSTS
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
```

---

## purehost — Hosts

Displays and manages Host objects.

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

# Manage WWNs and personality
purehost setattr MY-SERVER-001 --wwnlist 1000000000000003
purehost setattr MY-SERVER-001 --addwwnlist 1000000000000003
purehost setattr MY-SERVER-001 --remwwnlist 1000000000000003
purehost setattr MY-SERVER-001 --wwnlist ""
purehost setattr MY-SERVER-001 --personality esxi
```

---

## purehw — Hardware

Displays hardware components and manages visual identification.

```bash
purehw list
purehw list --spec
purehw list --type bay
purehw list --type bay --spec
purehw list --type ct
purehw list --type eth
purehw list --type fc
purehw list CT0 --spec
purehw list CT0.FC0
```

---

## purepod — ActiveCluster / Pods

Creates and manages Pods for synchronous replication.

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

## pureport — Ports

Displays array host connection ports.

```bash
pureport list
pureport list --initiator
pureport list --raw --filter "name='*FC*'"
pureport list --raw --filter "name='*ETH*'"
pureport list --raw --filter "name='CT0.FC*'"
pureport list --initiator --raw --filter "name='CT0.FC0'"
pureport list --initiator --raw --filter "initiator.wwn='1000000000000001'"
```

---

## purevol — Volumes and Snapshots

Displays and manages virtual volumes and snapshots.

```bash
# Create / delete / recover
purevol create --size 10G MY_VOLUME_001
purevol create --size 10G MY_VOLUME_001 --bw-limit 10M
purevol create --size 10G MY_VOLUME_001 MY_VOLUME_002
purevol create --size 1G MYPOD001::MY_VOL_001
purevol destroy MY_VOL_001
purevol destroy MY_VOL_001 MY_VOL_002
purevol eradicate MY_VOL_001
purevol eradicate MY_VOL_001 MY_VOL_002
purevol recover MY_VOL_001
purevol rename MY_VOL_001 MY_VOL_002

# List
purevol list
purevol list MY_VOL_001
purevol list MY_VOL*
purevol list --snap
purevol list --pending
purevol list --pending-only
purevol list --space --sort size,total
purevol list --sort size
purevol list --sort size-
purevol list --sort serial
purevol list --sort serial-
purevol list --sort created
purevol list --sort created-
purevol list --filter "size='20T'"

# Connect / disconnect
purevol connect MY_VOL_001 --host MY-SERVER-001
purevol connect MY_VOL_001 --host MY-SERVER-001 --lun 10
purevol connect MY_VOL_001 --hgroup MY-HOSTS
purevol connect MY_VOL_001 MY_VOL_002 --host MY-SERVER-001
purevol disconnect MY_VOL_001 --host MY-SERVER-001
purevol disconnect MY_VOL_001 --hgroup MY-HOSTS
purevol discconnect MY_VOL_001 MY_VOL_002 --host MY-SERVER-001

# Modify
purevol setattr --size 2G MY_VOL_001
purevol setattr --size 2G MY_VOL_001 MY_VOL_002
purevol setattr --bw-limit 1M MY_VOL_001
purevol setattr --bw-limit 1M MY_VOL_001 MY_VOL_002
purevol truncate --size 1G MY_VOL_001

# Copy / move
purevol copy MY_VOL_001 MY_VOL_002
purevol copy MY_VOL_001 MY_VOL_002 --overwrite
purevol move vol001 MYPOD001
purevol move MYPOD001::vol001 ""

# Snapshots
purevol snap MY_VOL_001
purevol snap MY_VOL_001 --suffix PRD

# Pod volume operations
purevol remove --array PFAX70-REMOTE --with-unknown MYPOD001
```
