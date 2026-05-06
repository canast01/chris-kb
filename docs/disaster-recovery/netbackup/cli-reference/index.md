# NetBackup CLI Reference

NetBackup CLI commands run on the Master Server as root (UNIX) or Administrator (Windows). The `bp*` family covers backup and restore operations; `nb*` and `tp*` commands cover EMM, media, and device management. All commands are located in `/usr/openv/netbackup/bin/admincmd/` (UNIX) or `C:\Program Files\Veritas\NetBackup\bin\admincmd\` (Windows).

| Command | Purpose | Common Usage |
|---|---|---|
| `bpjobs` | List active and recent jobs | `bpjobs -summary` |
| `bpdbjobs` | Query job database | `bpdbjobs -report -failed -hoursago 24` |
| `bpbackup` | Initiate manual backup | `bpbackup -p <policy> -s <schedule> -c <client>` |
| `bprestore` | Initiate restore | `bprestore -C <client> -t <type> -L <log>` |
| `bpclient` | Manage client records | `bpclient -L -client <name>` |
| `bppllist` | List policies | `bppllist -allpolicies -L` |
| `bpplinclude` | List policy file list | `bpplinclude -L -p <policy>` |
| `bpstulist` | List storage units | `bpstulist` or `bpstulist -label <stu>` |
| `nbemmcmd` | EMM host management | `nbemmcmd -listhosts` |
| `tpconfig` | Tape device configuration | `tpconfig -d` |
| `vmquery` | Media/volume management | `vmquery -b -m <media_id>` |
| `bptestbpcd` | Test client/media connectivity | `bptestbpcd -client <host>` |
| `bpps` | List NetBackup processes | `bpps -a` |
| `bperror` | Error code lookup | `bperror -backstat -hoursago 24` |
