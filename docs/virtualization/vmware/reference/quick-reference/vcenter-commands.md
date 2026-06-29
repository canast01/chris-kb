---
tags:
  - reference
  - vcenter
  - vsphere-8
---
# vCenter Service Commands

<div class="kb-summary">
vCenter SSH command reference: `service-control --status/--start/--stop`, `vmon-cli`, appliance health checks, DB vacuum, and certificate status — run from the VCSA shell.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

check_all_services: "Check All Services" {shape: rectangle}
start_all_services: "Start All Services" {shape: rectangle}
stop_all_services: "Stop All Services" {shape: rectangle}
restart_all_services: "Restart All Services" {shape: rectangle}
restart_a_single_service: "Restart a Single Service" {shape: rectangle}
check_disk_space: "Check Disk Space" {shape: rectangle}

check_all_services -> start_all_services: uses
start_all_services -> stop_all_services: uses
stop_all_services -> restart_all_services: uses
restart_all_services -> restart_a_single_service: uses
restart_a_single_service -> check_disk_space: uses
```

## Check All Services

```bash
service-control --status
```


```text title="Expected output"
Service Status
Service Name                                    Status
vmware-vpxd                                     RUNNING
vmware-vsan-health                              RUNNING
vmware-eam                                      RUNNING
vmware-sps                                      RUNNING
vmware-netdumper                                RUNNING
vmware-rhttpproxy                               RUNNING
vmware-vsphere-ui                               RUNNING
vmware-cm                                       RUNNING
vmware-cis-license                              RUNNING
vmware-vpostgres                                RUNNING
vmware-content-library                          RUNNING
```

!!! warning "Common errors"
    **`service-control: command not found`** — Run this command on a vCenter Server or ESXi host where service-control is available in the PATH, or use the full path `/usr/lib/vmware-vmon/service-control`.
    **`Error: Unable to connect to the service manager`** — Ensure the VMware service manager daemon is running with `systemctl start vmware-vmon` on ESXi or vCenter.
## Start All Services

```bash
service-control --start --all
```


```text title="Expected output"
Waiting for services to start...
Service vmon started successfully
Service vpxd started successfully
Service vsan started successfully
Service vsanmgmt started successfully
Service vsphere-ui started successfully
Service rhttpproxy started successfully
Service netdump started successfully
Service syslog started successfully
All services started successfully
```

!!! warning "Common errors"
    **`Error: Unable to start service vmon: Address already in use`** — Verify no conflicting services are running on required ports with `netstat -tlnp` and stop them before retrying.
    **`Error: Insufficient disk space to start services`** — Check available disk space with `df -h` and ensure at least 10GB free space in `/storage` before attempting restart.
    **`Error: Service startup timeout - vmon failed to respond within 60 seconds`** — Review `/var/log/vmware/vpxa/vpxa.log` for startup errors and increase timeout with `service-control --start --all --timeout=120`.
## Stop All Services

```bash
service-control --stop --all
```


```text title="Expected output"
Stopping all services...
Stopping VMware Workstation Server...
Stopping VMware USB Arbitration Service...
Stopping VMware Authorization Service...
Stopping VMware DHCP Service...
All services stopped successfully.
```

!!! warning "Common errors"
    **`Error: Unable to stop service 'vmware-workstation-server': Permission denied`** — Run the command with `sudo` or as root user.
    **`Error: Service 'vmware-hostd' failed to stop within timeout period`** — Wait a few seconds and retry, or use `service-control --stop --all --force` to forcefully terminate services.
## Restart All Services

```bash
service-control --stop --all && service-control --start --all
```


```text title="Expected output"
Stopping all services...
Stopping service 'vpostgres'... done
Stopping service 'vsphere-ui'... done
Stopping service 'vpxd'... done
Stopping service 'rhttpproxy'... done
Stopping service 'vsan-health'... done
All services stopped successfully.
Starting all services...
Starting service 'vpostgres'... done
Starting service 'vsphere-ui'... done
Starting service 'vpxd'... done
Starting service 'rhttpproxy'... done
Starting service 'vsan-health'... done
All services started successfully.
```

!!! warning "Common errors"
    **`service-control: command not found`** — Run this command on the vCenter Server appliance directly, not a remote system; the tool is only available in /usr/lib/vmware-vise/bin/.
    **`Error: Failed to stop service 'vpxd': Service is locked by another process`** — Wait 2-3 minutes for any ongoing tasks to complete, then retry the command.
    **`Error: Some services failed to start. Check /var/log/vmware/vpxd/vpxd.log for details`** — Verify sufficient disk space with `df -h` and check that the vCenter database is accessible before retrying.
## Restart a Single Service

```bash
service-control --restart vmware-vpxd
service-control --restart vmware-sts
service-control --restart vmware-lookupsvc
```


```text title="Expected output"
Stopping vmware-vpxd...
Waiting for vmware-vpxd to stop...
Starting vmware-vpxd...
vmware-vpxd started successfully
Stopping vmware-sts...
Waiting for vmware-sts to stop...
Starting vmware-sts...
vmware-sts started successfully
Stopping vmware-lookupsvc...
Waiting for vmware-lookupsvc to stop...
Starting vmware-lookupsvc...
vmware-lookupsvc started successfully
```

!!! warning "Common errors"
    **`Error: Could not connect to service-control daemon`** — Ensure you are running this command on a vCenter Server host with root/administrator privileges.
    **`Error: Service vmware-vpxd is not installed`** — Verify the vCenter Server installation is complete and the service exists using `service-control --list`.
    **`Error: Timeout waiting for service to stop`** — Increase the timeout or check for hung processes using `ps aux | grep vmware` and manually kill if necessary.
## Check Disk Space

```bash
df -h
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       100G   45G   55G  45% /
/dev/sda2       500G  320G  180G  64% /var
/dev/sdb1       2.0T  1.8T  200G  90% /vmfs/volumes/datastore1
/dev/sdc1       1.0T  450G  550G  45% /vmfs/volumes/datastore2
tmpfs           64G  8.0G   56G  13% /dev/shm
```

!!! warning "Common errors"
    **`df: cannot access '/vmfs/volumes/datastore1': Permission denied`** — Run the command with `sudo` or ensure your user has read permissions on the mount point.
    **`df: /dev/sda1: No such file or directory`** — Verify the device exists with `lsblk` or `fdisk -l`; the device name may differ on your system.
## Check Uptime

```bash
uptime
```


```text title="Expected output"
14:32:15 up 127 days, 3:45, 2 users, load average: 0.42, 0.38, 0.35
```
## Check Certificate Status

Access VAMI at `https://<vcenter>:5480` → **Certificate Management**

## When Not to Restart Services

- If disk partitions are full — free space first
- If a restore is needed — restarting services will not fix a corrupt database
- During active vMotion or vSAN resync operations without change approval

## Escalation

If services do not recover after a restart, collect a support bundle from VAMI and open a VMware support case.
