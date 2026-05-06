# VMware ESXi CLI Reference

Commonly used ESXi shell and ESXCLI commands for managing VMware ESXi hosts.

---

## System & Host Info

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
```

---

## Services

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

---

## Maintenance Mode

```bash
esxcli system maintenanceMode get
esxcli system maintenanceMode set --enabled true
esxcli system maintenanceMode set --enabled false

# Via vim-cmd
vim-cmd hostsvc/maintenance_mode_enter
vim-cmd hostsvc/maintenance_mode_exit
```

---

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

---

## Firewall

```bash
# Status
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
```

---

## NTP

```bash
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

---

## iSCSI

```bash
esxcli iscsi adapter list
esxcli iscsi adapter get -A vmhba64
esxcli iscsi adapter discovery sendtarget list -A vmhba64
esxcli iscsi adapter discovery sendtarget add --address <ip>:<port> -A vmhba64
esxcli iscsi adapter discovery sendtarget remove --address <ip>:<port> -A vmhba64
esxcli iscsi session list
esxcli iscsi logicalnetworkportal list -A vmhba64
```

---

## Fibre Channel

```bash
esxcli storage san fc list
esxcli storage san fc stats get -A vmhba0
esxcli storage san iscsi list
```

---

## Datastores & VMDK

```bash
# Browse datastores
ls /vmfs/volumes/
ls /vmfs/volumes/<datastore>/
du -sh /vmfs/volumes/<datastore>/*

# vmkfstools — disk operations
vmkfstools -l /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -c 100G -d thin /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -i source.vmdk dest.vmdk
vmkfstools -X 200G /vmfs/volumes/<ds>/<vm>/<vm>.vmdk
vmkfstools -e /vmfs/volumes/<ds>/<vm>/<vm>.vmdk

# Datastore info via vim-cmd
vim-cmd hostsvc/datastore/listsummary
vim-cmd hostsvc/datastore/info <datastore_name>
```

---

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

---

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

---

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

# CPU ready (via esxtop, or)
esxcli sched group list
```

---

## vSAN

```bash
esxcli vsan cluster get
esxcli vsan health cluster get
esxcli vsan health summary get
esxcli vsan storage list
esxcli vsan network list
esxcli vsan network ipconfig list
esxcli vsan trace get
esxcli vsan datastore list
esxcli vsan debug object list
esxcli vsan debug resync list
```

---

## Logs

```bash
# Live tailing
tail -f /var/log/vmkernel.log
tail -f /var/log/hostd.log
tail -f /var/log/vpxa.log
tail -f /var/log/vobd.log
tail -f /var/log/esxi.log
tail -f /var/log/syslog.log

# Grep for issues
grep -i "error" /var/log/vmkernel.log
grep -i "warning" /var/log/hostd.log
grep -i "disconnected" /var/log/vpxa.log
grep -i "lost connectivity" /var/log/vmkernel.log
grep <vm_name> /var/log/vmkernel.log

# Log locations
ls /var/log/
ls /scratch/log/
```

---

## Certificates

```bash
# View current cert
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -dates
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -subject
openssl x509 -in /etc/vmware/ssl/rui.crt -noout -fingerprint

# Regenerate self-signed cert
/sbin/generate-certificates

# List cert files
ls -la /etc/vmware/ssl/
```

---

## SSH

```bash
# Enable / disable SSH via vim-cmd
vim-cmd hostsvc/enable_ssh
vim-cmd hostsvc/disable_ssh

# Enable / disable SSH via service
/etc/init.d/SSH start
/etc/init.d/SSH stop

# Enable SSH via esxcli firewall
esxcli network firewall ruleset set --enabled true --ruleset-id sshServer
```
