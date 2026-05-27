# ESXi CLI Reference

```text
ESXi CLI Tool Map
┌─────────────────────────────────────────────────────────┐
│  esxcli — structured CLI for host management            │
│  ├── system    hostname, ntp, syslog, accounts           │
│  ├── network   nic, vswitch, ip, firewall, route         │
│  ├── storage   core (devices, paths), nmp, vmfs, san     │
│  ├── software  vib list/install/update, acceptance       │
│  ├── hardware  platform, cpu, memory, sensors, ipmi      │
│  └── vsan      cluster, health, storage, network         │
│                                                          │
│  vim-cmd — VM and host operations                        │
│  ├── vmsvc/   power, snapshot, config, summary           │
│  └── hostsvc/ storage, maintenance mode, datastore       │
│                                                          │
│  vmkfstools — VMDK operations                            │
│  ├── -c  create  -i  clone  -X  extend  -k  check        │
│  └── -p  partition info  -e  check and fix               │
│                                                          │
│  esxtop — real-time performance (interactive)            │
│  ├── c  CPU view  (%RDY, %CSTP, %USED)                   │
│  ├── m  Memory view (MCTLSZ balloon, SWCUR swap)         │
│  ├── d  Disk I/O view (DAVG latency)                     │
│  └── n  Network view (drops, throughput)                 │
│                                                          │
│  Logs  /var/log/vmkernel.log  hostd  vpxa  fdm  auth     │
└─────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────────── ESXi — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│  esxcli on-host, vim-cmd, govc (remote), and PowerCLI automation commands.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               esxcli (on-host)               │  │              vim-cmd (on-host)              │   │
│   │          esxcli system version get           │  │           vim-cmd vmsvc/getallvms           │   │
│   │         esxcli network ip interface          │  │          vim-cmd vmsvc/power.on ID          │   │
│   │           esxcli storage core path           │  │         vim-cmd hostsvc/maintenance         │   │
│   │            esxcli vm process list            │  │          vim-cmd hostsvc/firmware/          │   │
│   │           esxcli software vib list           │  │           vim-cmd solo/registervm           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  govc (remote vCenter API) and PowerCLI for scripted multi-host operations.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              govc (remote CLI)               │  │              PowerCLI (remote)              │   │
│   │                govc host.info                │  │           Get-VMHost | select Name          │   │
│   │              govc datastore.ls               │  │          Get-Datastore | sort Name          │   │
│   │            govc vm.migrate -host             │  │           Move-VM -Destination $h           │   │
│   │         govc host.maintenance.enter          │  │           Set-VMHost -State Maint           │   │
│   │         govc events -type HostEvent          │  │            Get-VIEvent -Entity $h           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ESXi hosts on x86; management network for SSH/API access to host/vCenter                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  esxcli    = on-host CLI; namespaces: system, network, storage, vm, software                          │
│  vim-cmd   = on-host; wraps vSphere API calls (hostsvc/vmsvc namespaces)                              │
│  govc      = open-source Go CLI for vCenter API; runs from any workstation                            │
│  PowerCLI  = VMware PowerShell module for scripted vSphere management                                 │
│  VIB       = vSphere Installation Bundle; ESXi extension/driver package                               │
│  GOVC_URL  = env var pointing govc at vCenter: https://user:pass@vc/sdk                               │
│  maintenance = host state; vCenter migrates VMs before maintenance tasks                              │
│  hostsvc   = vim-cmd namespace for host-level service operations                                      │
│  vmsvc     = vim-cmd namespace for VM lifecycle operations                                            │
│  PSC       = Platform Services Controller; SSO/certs (pre-7.0)                                        │
│  fdm       = Fault Domain Manager; HA agent queried via vim-cmd                                       │
│  vCenter API = REST + SOAP endpoint; govc/PowerCLI both use it                                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```bash
# Restart management agents
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
/etc/init.d/ntpd restart
/etc/init.d/ssh start
/etc/init.d/ssh stop

# All services
services.sh restart
services.sh status

# Check host version
vmware -v
vmware -l

# Uptime
uptime
```

```bash
# Maintenance mode
esxcli system maintenanceMode get
esxcli system maintenanceMode set --enabled true
esxcli system maintenanceMode set --enabled false

# Via vim-cmd
vim-cmd hostsvc/maintenance_mode_enter
vim-cmd hostsvc/maintenance_mode_exit
```

## Network

```bash
# Physical NICs
esxcli network nic list
esxcli network nic get -n vmnic0
esxcli network nic stats get -n vmnic0
esxcli network nic up -n vmnic0
esxcli network nic down -n vmnic0

# vSwitches
esxcli network vswitch standard list
esxcli network vswitch standard add -v vSwitch1
esxcli network vswitch standard remove -v vSwitch1
esxcli network vswitch standard uplink add -v vSwitch0 -u vmnic1
esxcli network vswitch standard uplink remove -v vSwitch0 -u vmnic1

# Port groups
esxcli network vswitch standard portgroup list
esxcli network vswitch standard portgroup add -v vSwitch0 -p "VM Network"
esxcli network vswitch standard portgroup remove -v vSwitch0 -p "VM Network"

# VMkernel interfaces
esxcli network ip interface list
esxcli network ip interface ipv4 get
esxcli network ip interface ipv4 set -i vmk0 -I <ip> -N <netmask> -t static
esxcli network ip interface add -i vmk1 -p "vMotion"
esxcli network ip interface remove -i vmk1

# Routing
esxcli network ip route ipv4 list
esxcli network ip route ipv4 add -n 0.0.0.0/0 -g <gateway>
esxcli network ip route ipv4 remove -n 0.0.0.0/0 -g <gateway>

# DNS
esxcli network ip dns server list
esxcli network ip dns server add --server <ip>
esxcli network ip dns server remove --server <ip>
esxcli network ip dns search list

# Connections and neighbors
esxcli network ip connection list
esxcli network ip neighbor list

# esxcfg equivalents
esxcfg-vmknic -l
esxcfg-vswitch -l
esxcfg-nics -l
esxcfg-route
esxcfg-route -a <subnet> <gateway>
```

## Storage — Devices & Paths

```bash
# Devices
esxcli storage core device list
esxcli storage core device list -d <device_id>
esxcli storage core device stats get -d <device_id>

# Paths
esxcli storage core path list
esxcli storage core path list -d <device_id>
esxcli storage core path stats get -A vmhba0

# Adapters
esxcli storage core adapter list
esxcli storage core adapter rescan --adapter vmhba0
esxcli storage core adapter rescan --all

# NMP (Native Multipathing)
esxcli storage nmp device list
esxcli storage nmp path list
esxcli storage nmp satp list
esxcli storage nmp psp list
esxcli storage nmp psp roundrobin deviceconfig set --device <device_id> --type iops --iops 1

# VMFS / filesystems
esxcli storage vmfs extent list
esxcli storage filesystem list
esxcli storage filesystem mount -v <uuid>
esxcli storage filesystem unmount -v <uuid>
esxcli storage filesystem rescan

# Legacy
esxcfg-scsidevs -l
esxcfg-scsidevs -m
```

## Datastores & VMDK

```bash
# List all datastores visible to the host
ls /vmfs/volumes/
esxcli storage filesystem list

# List contents of a datastore
ls /vmfs/volumes/<datastore>/
ls -lah /vmfs/volumes/<datastore>/<vm_folder>/

# Disk usage per directory
du -sh /vmfs/volumes/<datastore>/*
du -sh /vmfs/volumes/<datastore>/<vm_folder>/
```

```bash
# vmkfstools — VMDK operations
vmkfstools -l /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -c 100G -d thin /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -i source.vmdk dest.vmdk
vmkfstools -X 200G /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -k /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -p /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -e /vmfs/volumes/<ds>/<vm>/<vm>.vmdk

# Datastore info via vim-cmd
vim-cmd hostsvc/datastore/listsummary
vim-cmd hostsvc/datastore/info <datastore_name>
esxcli storage core adapter rescan --all
vim-cmd hostsvc/storage/refresh

# Snapshot delta files
find /vmfs/volumes/<ds>/ -name "*-delta.vmdk" -o -name "*-0000*.vmdk" 2>/dev/null

# VMFS troubleshooting
esxcli storage vmfs extent list
esxcli storage vmfs snapshot list
esxcli storage vmfs snapshot resignature -l <label>
esxcli storage filesystem unmount -l <datastore_label>
```

## SAN Connectivity (iSCSI / FC)

```bash
# Fibre Channel — HBAs and WWPNs
esxcli storage san fc list
esxcli storage san fc stats get -A vmhba0
esxcli storage san fc stats get -A vmhba1
esxcli storage nmp device list | grep vmhba
esxcli storage nmp path list
esxcli storage nmp path list -d <naa.xxx>
esxcli storage core path list | grep "dead\|Dead"

# iSCSI
esxcli iscsi adapter list
esxcli iscsi adapter get -A vmhba64
esxcli iscsi adapter discovery sendtarget list -A vmhba64
esxcli iscsi adapter discovery sendtarget add \
    --address <iscsi_target_ip>:3260 -A vmhba64
esxcli iscsi adapter discovery sendtarget remove \
    --address <iscsi_target_ip>:3260 -A vmhba64
esxcli iscsi session list
esxcli iscsi logicalnetworkportal list -A vmhba64

# Multipathing
esxcli storage core path list
esxcli storage nmp device list
esxcli storage nmp device list | grep -E "Device:|PSP:"
esxcli storage nmp device set -d <naa.xxx> -P VMW_PSP_RR
esxcli storage core adapter rescan --all
esxcli storage core adapter rescan -A vmhba0

# LUN and device info
esxcli storage core device list
esxcli storage core device list -d <naa.xxx>
esxcli storage core device vaai status get -d <naa.xxx>
esxcli storage core device list | grep "Queue Full Threshold"
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=64

# APD / PDL troubleshooting
grep -i "APD\|PDL\|lost path" /var/log/vmkernel.log | tail -20
esxcli storage core path list | grep -A 5 "State: dead"
esxcli storage core adapter rescan --all
esxcli storage core path list | grep -c "State: active"
```

## VM Management (vim-cmd)

```bash
# List all VMs
vim-cmd vmsvc/getallvms

# Power state
vim-cmd vmsvc/power.getstate <vmid>
vim-cmd vmsvc/power.on <vmid>
vim-cmd vmsvc/power.off <vmid>
vim-cmd vmsvc/power.shutdown <vmid>
vim-cmd vmsvc/power.reboot <vmid>
vim-cmd vmsvc/power.suspend <vmid>
vim-cmd vmsvc/power.reset <vmid>

# VM details
vim-cmd vmsvc/get.summary <vmid>
vim-cmd vmsvc/get.config <vmid>
vim-cmd vmsvc/get.guest <vmid>
vim-cmd vmsvc/get.tasklist <vmid>

# Snapshots
vim-cmd vmsvc/snapshot.get <vmid>
vim-cmd vmsvc/snapshot.create <vmid> <name> <description> <memory> <quiesce>
vim-cmd vmsvc/snapshot.removeall <vmid>

# Register / unregister
vim-cmd vmsvc/unregister <vmid>
vim-cmd solo/registervm /vmfs/volumes/<ds>/<vm>/<vm>.vmx

# Host summary
vim-cmd hostsvc/hostsummary
vim-cmd hostsvc/net/info
```

## vSAN Commands

```bash
# Cluster status
esxcli vsan cluster get
esxcli vsan health cluster get
esxcli vsan health summary get
esxcli vsan health cluster get | grep -v "GREEN\|green"

# Storage and disk groups
esxcli vsan storage list
esxcli vsan storage stats get
esxcli vsan storage list | grep -E "Is SSD|Disk Group"

# Objects and resyncing
esxcli vsan debug object list
esxcli vsan debug object list | grep -v "healthy"
esxcli vsan debug resync list
esxcli vsan debug resync list | grep -E "Total Bytes|Remaining"

# Networking
esxcli vsan network list
esxcli vsan network ipconfig list
esxcli vsan debug network test

# Datastore
esxcli vsan datastore list
esxcli vsan trace get
```

| vSAN Indicator | Meaning |
|---|---|
| Health: GREEN | Check passing |
| Health: YELLOW | Warning — monitor |
| Health: RED | Failure — action required |
| Resync bytes > 0 | Rebuild or repair active — avoid maintenance |
| Object state: absent | Component missing — check disk/host |
| Object state: degraded | Redundancy reduced — replace disk before next failure |

## Performance & Troubleshooting

```bash
# Interactive top
esxtop

# Kill a VM process
esxcli vm process list
esxcli vm process kill --type soft --world-id <id>
esxcli vm process kill --type hard --world-id <id>
esxcli vm process kill --type force --world-id <id>

# Kernel stats
vsish -e get /world/<worldid>/sched/statsSummary
vsish -e ls /vm/
vsish -e ls /net/pNics/

# Check for dropped packets
esxcli network nic stats get -n vmnic0 | grep -i drop

# CPU ready
esxcli sched group list
```

## Logs

```bash
# Key log files
# /var/log/vmkernel.log  — Storage, network, driver-level events
# /var/log/hostd.log     — Host management agent (API, VM operations)
# /var/log/vpxa.log      — vCenter agent communication
# /var/log/vobd.log      — Hardware/system observation (IPMI, sensors)
# /var/log/esxi.log      — ESXi core syslog
# /var/log/syslog.log    — General system syslog
# /var/log/auth.log      — SSH logins, sudo
# /var/log/fdm.log       — HA agent (Fault Domain Manager)

# Live tailing
tail -f /var/log/vmkernel.log
tail -f /var/log/hostd.log
tail -f /var/log/vpxa.log
tail -f /var/log/fdm.log
tail -f /var/log/vmkernel.log /var/log/hostd.log

# Searching for issues
grep -i "error\|warning\|fail\|fault" /var/log/vmkernel.log | tail -30
grep -i "error" /var/log/hostd.log | tail -20
grep -i "disconnected\|lost connectivity" /var/log/vpxa.log | tail -10
grep -i "lost path\|path down\|APD\|PDL" /var/log/vmkernel.log | tail -20
grep -i "link down\|carrier\|vmnic" /var/log/vmkernel.log | tail -20
grep -i "isolation\|restart\|fdm" /var/log/fdm.log | tail -20

# Collect support bundle
vm-support -n -w /tmp/
# Output: /tmp/esx-<hostname>-<date>.tgz

# Remote syslog
esxcli system syslog config get
esxcli system syslog config set --loghost=udp://syslog.example.local:514
esxcli system syslog reload
esxcli system syslog config set --loghost="udp://syslog1.example.local:514,tcp://syslog2.example.local:514"

# Log rotation and persistence
esxcli system syslog config get | grep -E "rotate\|size"
ls /scratch/log/
cat /etc/vmware/locker.conf
```

## Hardware & Health

```bash
# Platform info
esxcli hardware platform get
esxcli hardware clock get

# CPU
esxcli hardware cpu global get
esxcli hardware cpu list

# Memory
esxcli hardware memory get

# PCI devices
esxcli hardware pci list

# IPMI / BMC
esxcli hardware ipmi bmc get
esxcli hardware ipmi fru list
esxcli hardware ipmi sel list

# Sensors (temp, power, fan)
esxcli hardware sensor list
esxcli hardware sensor list --type Temperature
esxcli hardware sensor list --type Fan
esxcli hardware sensor list --type Power
```

## Firewall & NTP

```bash
# Firewall status
esxcli network firewall get
esxcli network firewall set --enabled true
esxcli network firewall set --enabled false

# Rulesets
esxcli network firewall ruleset list
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
esxcli network firewall ruleset set --enabled false --ruleset-id sshServer

# Allowed IPs per ruleset
esxcli network firewall ruleset allowedip list --ruleset-id sshServer
esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address <ip>
esxcli network firewall ruleset allowedip remove --ruleset-id sshServer --ip-address <ip>

# NTP
esxcli system ntp get
esxcli system ntp set --enabled true --server <ntp_server>
esxcli system ntp set --enabled false
ntpq -p
cat /etc/ntp.conf
/etc/init.d/ntpd restart
```

## Certificates & SSH

```bash
# View current certificate
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -dates
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -subject
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -fingerprint

# Regenerate self-signed cert
/sbin/generate-certificates

# List cert files
ls -la /etc/vmware/ssl/

# Enable / disable SSH via vim-cmd
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/disable_ssh

# Enable / disable SSH via service
/etc/init.d/SSH start
/etc/init.d/SSH stop

# Enable SSH via esxcli firewall
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
```
