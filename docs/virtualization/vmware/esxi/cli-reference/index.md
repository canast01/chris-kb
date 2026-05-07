# VMware ESXi CLI Reference

The ESXi shell gives you direct access to a hypervisor host via SSH. `esxcli` is the primary command-line framework — it organizes commands into namespaces like `esxcli storage`, `esxcli network`, and `esxcli vsan`. `vim-cmd` provides VM management without vCenter. Most commands require root access.

> SSH to the ESXi host management IP. Enable SSH via vSphere Client → Host → Actions → Services → Enable Secure Shell (SSH), or via the ESXi DCUI console.

---

## System, Services & Maintenance

Get host identity, manage local accounts, control services, and put the host into maintenance mode. These are the first commands to run when connecting to a host you're unfamiliar with.

```bash
# Version and identity
esxcli system version get
esxcli system hostname get
esxcli system hostname set --host <hostname> --domain <domain>
esxcli system uuid get
esxcli system uptime get
esxcli system time get

# Accounts and permissions
esxcli system account list
esxcli system account add -i <username> -p <password> -d "Description"
esxcli system account remove -i <username>
esxcli system permission list
esxcli system permission set -i <username> -r Admin

# Kernel modules
esxcli system module list
esxcli system module get -m <module>

# Syslog
esxcli system syslog config get
esxcli system syslog config set --loghost udp://<ip>:514
esxcli system syslog reload

# Restart management agents (fixes vCenter connectivity issues)
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

# Maintenance mode
esxcli system maintenanceMode get
esxcli system maintenanceMode set --enabled true
esxcli system maintenanceMode set --enabled false

# Via vim-cmd
vim-cmd hostsvc/maintenance_mode_enter
vim-cmd hostsvc/maintenance_mode_exit
```

---

## Network

Manage physical NICs, standard vSwitches, port groups, VMkernel interfaces, routing, and DNS. Most networking changes require caution — misconfiguring the management interface can disconnect you from the host.

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

# VMkernel interfaces (management, vMotion, vSAN, iSCSI)
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

# Active connections and ARP table
esxcli network ip connection list
esxcli network ip neighbor list

# Legacy esxcfg commands (still widely used)
esxcfg-vmknic -l
esxcfg-vswitch -l
esxcfg-nics -l
esxcfg-route
esxcfg-route -a <subnet> <gateway>
```

---

## Firewall & NTP

The ESXi firewall controls which services are reachable on the host. NTP keeps the host clock in sync — critical for vCenter connectivity, certificates, and log correlation.

```bash
# Firewall status and toggle
esxcli network firewall get
esxcli network firewall set --enabled true
esxcli network firewall set --enabled false

# Rulesets (named rules for specific services like SSH, vMotion)
esxcli network firewall ruleset list
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
esxcli network firewall ruleset set --enabled false --ruleset-id sshServer

# Allowed IPs per ruleset
esxcli network firewall ruleset allowedip list --ruleset-id sshServer
esxcli network firewall ruleset allowedip add --ruleset-id sshServer --ip-address <ip>
esxcli network firewall ruleset allowedip remove --ruleset-id sshServer --ip-address <ip>

# NTP configuration
esxcli system ntp get
esxcli system ntp set --enabled true --server <ntp_server>
esxcli system ntp set --enabled false

# Check sync status
ntpq -p
cat /etc/ntp.conf

# Restart NTP
/etc/init.d/ntpd restart
```

---

## Storage — Devices & Paths

List storage devices, check multipath state, manage VMFS filesystems, and configure path selection policies. A storage device is a LUN — each device can have multiple paths for redundancy.

```bash
# Devices (LUNs visible to the host)
esxcli storage core device list
esxcli storage core device list -d <device_id>
esxcli storage core device stats get -d <device_id>

# Paths (one device can have multiple paths via different HBAs)
esxcli storage core path list
esxcli storage core path list -d <device_id>
esxcli storage core path stats get -A vmhba0

# Adapters (HBAs)
esxcli storage core adapter list
esxcli storage core adapter rescan --adapter vmhba0
esxcli storage core adapter rescan --all

# NMP — Native Multipathing Plugin
esxcli storage nmp device list
esxcli storage nmp path list
esxcli storage nmp satp list
esxcli storage nmp psp list
esxcli storage nmp psp roundrobin deviceconfig set --device <device_id> --type iops --iops 1

# VMFS filesystems
esxcli storage vmfs extent list
esxcli storage filesystem list
esxcli storage filesystem mount -v <uuid>
esxcli storage filesystem unmount -v <uuid>
esxcli storage filesystem rescan

# Legacy
esxcfg-scsidevs -l
esxcfg-scsidevs -m
```

---

## SAN Connectivity (iSCSI / FC)

Check Fibre Channel HBA WWPNs, iSCSI initiator IQNs, and configure target discovery. Run these when adding a host to a SAN fabric or troubleshooting LUN visibility.

```bash
# Fibre Channel
esxcli storage san fc list                          # list HBAs with WWPNs
esxcli storage san fc stats get -A vmhba0           # FC HBA stats (errors, logins)
esxcli storage san fc stats get -A vmhba1
esxcli storage nmp path list                        # path status to all LUNs
esxcli storage nmp path list -d <naa.xxx>           # paths to a specific device
esxcli storage core path list | grep "dead\|Dead"   # dead paths

# iSCSI
esxcli iscsi adapter list
esxcli iscsi adapter get -A vmhba64                 # IQN and status
esxcli iscsi adapter discovery sendtarget list -A vmhba64
esxcli iscsi adapter discovery sendtarget add \
    --address <iscsi_target_ip>:3260 -A vmhba64     # add static discovery target
esxcli iscsi adapter discovery sendtarget remove \
    --address <iscsi_target_ip>:3260 -A vmhba64
esxcli iscsi session list
esxcli iscsi logicalnetworkportal list -A vmhba64   # bound VMkernel adapters

# Multipathing and PSP
esxcli storage nmp device list | grep -E "Device:|PSP:"
esxcli storage nmp device set -d <naa.xxx> -P VMW_PSP_RR   # set Round Robin PSP
esxcli storage core adapter rescan --all

# LUN and device info
esxcli storage core device list -d <naa.xxx>              # vendor, model, size, queue depth
esxcli storage core device vaai status get -d <naa.xxx>   # VAAI (offload) support
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=64

# Troubleshooting — check for APD / PDL
grep -i "APD\|PDL\|lost path" /var/log/vmkernel.log | tail -20
esxcli storage core path list | grep -A 5 "State: dead"
```

---

## Datastores & VMDK

Browse datastore contents, create and clone VMDKs with `vmkfstools`, and manage VMFS filesystem metadata.

```bash
# Browse datastores
ls /vmfs/volumes/
esxcli storage filesystem list
ls /vmfs/volumes/<datastore>/
ls -lah /vmfs/volumes/<datastore>/<vm_folder>/
du -sh /vmfs/volumes/<datastore>/*

# vmkfstools — VMDK operations
vmkfstools -l /vmfs/volumes/<ds>/<vm>/<vm>.vmdk       # list VMDK info
vmkfstools -c 100G -d thin /vmfs/volumes/<ds>/<vm>/<vm>.vmdk   # create thin VMDK
vmkfstools -i source.vmdk dest.vmdk                   # clone
vmkfstools -X 200G /vmfs/volumes/<ds>/<vm>/<vm>.vmdk  # expand
vmkfstools -k /vmfs/volumes/<ds>/<vm>/<vm>.vmdk       # inflate thin to thick
vmkfstools -p /vmfs/volumes/<ds>/<vm>/<vm>.vmdk       # defragment
vmkfstools -e /vmfs/volumes/<ds>/<vm>/<vm>.vmdk       # check consistency

# Datastore info via vim-cmd
vim-cmd hostsvc/datastore/listsummary
vim-cmd hostsvc/datastore/info <datastore_name>
esxcli storage core adapter rescan --all
vim-cmd hostsvc/storage/refresh

# Find snapshot delta files (large delta files indicate unconsolidated snapshots)
find /vmfs/volumes/<ds>/ -name "*-delta.vmdk" -o -name "*-0000*.vmdk" 2>/dev/null

# VMFS troubleshooting
esxcli storage vmfs extent list
esxcli storage vmfs snapshot list
esxcli storage vmfs snapshot resignature -l <label>   # resignature VMFS copy after LUN clone
esxcli storage filesystem unmount -l <datastore_label>
```

---

## VM Management (vim-cmd)

`vim-cmd` is the host-level VM management tool — use it when vCenter is unavailable or when you need to register/unregister VMs directly on a host.

```bash
# List all VMs registered on this host
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

# Register / unregister (when a VM is orphaned or needs to be added back)
vim-cmd vmsvc/unregister <vmid>
vim-cmd solo/registervm /vmfs/volumes/<ds>/<vm>/<vm>.vmx

# Host summary
vim-cmd hostsvc/hostsummary
vim-cmd hostsvc/net/info
```

---

## Hardware & Health

Query physical hardware inventory, CPU and memory info, PCI devices, and IPMI/BMC (out-of-band management). Use these for hardware inventory or when investigating sensor alerts.

```bash
# Platform info
esxcli hardware platform get
esxcli hardware clock get

# CPU details
esxcli hardware cpu global get
esxcli hardware cpu list

# Memory
esxcli hardware memory get

# PCI devices
esxcli hardware pci list

# IPMI / BMC (out-of-band management interface)
esxcli hardware ipmi bmc get
esxcli hardware ipmi fru list
esxcli hardware ipmi sel list

# Environmental sensors (temp, power, fan)
esxcli hardware sensor list
esxcli hardware sensor list --type Temperature
esxcli hardware sensor list --type Fan
esxcli hardware sensor list --type Power
```

---

## Performance & Troubleshooting

`esxtop` is the top-level performance monitor for ESXi — shows CPU, memory, network, storage, and power in real time. Use it for latency investigation and resource contention analysis.

```bash
# Interactive performance monitor (like top but for ESXi)
esxtop

# VM process list and kill (use when a VM is stuck)
esxcli vm process list
esxcli vm process kill --type soft --world-id <id>    # graceful
esxcli vm process kill --type hard --world-id <id>    # immediate
esxcli vm process kill --type force --world-id <id>   # last resort

# Kernel-level stats (advanced troubleshooting)
vsish -e get /world/<worldid>/sched/statsSummary
vsish -e ls /vm/
vsish -e ls /net/pNics/

# Network packet drops
esxcli network nic stats get -n vmnic0 | grep -i drop

# CPU scheduling
esxcli sched group list
```

---

## vSAN Commands

vSAN-specific commands run directly on the ESXi host shell. These complement the dedicated vSAN CLI Reference and are useful when you're already SSH'd into a host.

```bash
# Cluster membership and UUID
esxcli vsan cluster get

# Health checks
esxcli vsan health cluster get
esxcli vsan health summary get
esxcli vsan health cluster get | grep -v "GREEN\|green"   # failures only

# Storage and disk groups
esxcli vsan storage list
esxcli vsan storage stats get
esxcli vsan storage list | grep -E "Is SSD|Disk Group"

# Objects and resyncing
esxcli vsan debug object list
esxcli vsan debug object list | grep -v "healthy"         # non-healthy only
esxcli vsan debug resync list
esxcli vsan debug resync list | grep -E "Total Bytes|Remaining"

# Networking
esxcli vsan network list
esxcli vsan network ipconfig list
esxcli vsan debug network test

# vSAN datastore
esxcli vsan datastore list
esxcli vsan trace get
```

---

## Logs

ESXi logs are the first place to look when a VM fails to power on, a host disconnects from vCenter, or storage issues appear. Key logs are in `/var/log/`.

| Log | Path | Content |
|---|---|---|
| vmkernel | `/var/log/vmkernel.log` | Storage, network, driver-level events |
| hostd | `/var/log/hostd.log` | Host management agent (API, VM operations) |
| vpxa | `/var/log/vpxa.log` | vCenter agent communication |
| vobd | `/var/log/vobd.log` | Hardware/system observation (IPMI, sensors) |
| fdm | `/var/log/fdm.log` | HA agent (Fault Domain Manager) |
| auth.log | `/var/log/auth.log` | SSH logins |

```bash
# Live tail
tail -f /var/log/vmkernel.log
tail -f /var/log/hostd.log
tail -f /var/log/vpxa.log
tail -f /var/log/fdm.log

# Search for problems
grep -i "error\|warning\|fail\|fault" /var/log/vmkernel.log | tail -30
grep -i "error" /var/log/hostd.log | tail -20
grep -i "disconnected\|lost connectivity" /var/log/vpxa.log | tail -10

# Storage path errors
grep -i "lost path\|path down\|APD\|PDL" /var/log/vmkernel.log | tail -20

# Network errors
grep -i "link down\|carrier\|vmnic" /var/log/vmkernel.log | tail -20

# HA events
grep -i "isolation\|restart\|fdm" /var/log/fdm.log | tail -20

# VM-specific events
grep "<vm_name>" /var/log/vmkernel.log | tail -20
grep "<vm_name>" /var/log/hostd.log | tail -20

# Generate support bundle
vm-support -n -w /tmp/
# Output: /tmp/esx-<hostname>-<date>.tgz

# Remote syslog
esxcli system syslog config get
esxcli system syslog config set --loghost=udp://syslog.corp.local:514
esxcli system syslog reload
```

---

## Certificates & SSH

Manage the ESXi host's SSL certificate (used for the web UI and API) and enable/disable SSH access.

```bash
# View current certificate details
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -dates
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -subject
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -fingerprint

# Regenerate self-signed cert
/sbin/generate-certificates

# List cert files
ls -la /etc/vmware/ssl/

# Enable / disable SSH
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/disable_ssh

# Via service
/etc/init.d/SSH start
/etc/init.d/SSH stop

# Via firewall ruleset
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
```
