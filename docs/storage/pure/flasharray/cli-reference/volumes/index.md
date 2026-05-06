# Volumes & Snapshots

> Part of the [Pure FlashArray CLI Reference](../).

---

## purevol — Volumes and Snapshots

Displays and manages virtual volumes and snapshots.

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
purevol list --sort serial-
purevol list --sort created
purevol list --sort created-
purevol list --filter "size='20T'"
purevol list --filter "size > 100G"

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
