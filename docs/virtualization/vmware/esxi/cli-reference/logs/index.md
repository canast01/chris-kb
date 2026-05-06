# Logs

> Part of the [VMware ESXi CLI Reference](../).

## Key Log Files

| Log | Path | Content |
|---|---|---|
| vmkernel | `/var/log/vmkernel.log` | Storage, network, driver-level events |
| hostd | `/var/log/hostd.log` | Host management agent (API, VM operations) |
| vpxa | `/var/log/vpxa.log` | vCenter agent communication |
| vobd | `/var/log/vobd.log` | Hardware/system observation (IPMI, sensors) |
| esxi.log | `/var/log/esxi.log` | ESXi core syslog |
| syslog.log | `/var/log/syslog.log` | General system syslog |
| auth.log | `/var/log/auth.log` | SSH logins, sudo |
| fdm.log | `/var/log/fdm.log` | HA agent (Fault Domain Manager) |

## Live Tailing

```bash
# Follow key logs in real time
tail -f /var/log/vmkernel.log
tail -f /var/log/hostd.log
tail -f /var/log/vpxa.log
tail -f /var/log/fdm.log

# Multiple logs at once (busybox tail on ESXi)
tail -f /var/log/vmkernel.log /var/log/hostd.log
```

## Searching for Issues

```bash
# Errors and warnings
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
```

## Collect Support Bundle

```bash
# Generate ESXi support bundle (vm-support)
vm-support -n -w /tmp/
# Output: /tmp/esx-<hostname>-<date>.tgz

# Or trigger from vSphere Client: Host → Actions → Export System Logs
```

## Remote Syslog

```bash
# Check current syslog configuration
esxcli system syslog config get

# Set a remote syslog target
esxcli system syslog config set --loghost=udp://syslog.corp.local:514
esxcli system syslog reload

# Add a second syslog target (comma-separated)
esxcli system syslog config set --loghost="udp://syslog1.corp.local:514,tcp://syslog2.corp.local:514"
```

## Log Rotation and Persistence

```bash
# Log size and rotation config
esxcli system syslog config get | grep -E "rotate\|size"

# Persistent log location (survives reboots — if scratch disk configured)
ls /scratch/log/

# Check scratch disk assignment
esxcli system syslog config get | grep "local0"
cat /etc/vmware/locker.conf
```
