---
tags:
  - vmware
---
# DNS and NTP Validation

<div class="kb-summary">
DNS and NTP Validation reference covering Why This Matters, NTP Validation — ESXi Host, NTP Validation — vCenter Appliance, DNS Validation — ESXi Host, DNS Validation — PowerCLI and 3 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

why_this_matters: "Why This Matters" {shape: rectangle}
ntp_validation_esxi_host: "NTP Validation — ESXi Host" {shape: rectangle}
ntp_validation_vcenter_appliance: "NTP Validation — vCenter Appliance" {shape: rectangle}
dns_validation_esxi_host: "DNS Validation — ESXi Host" {shape: rectangle}
dns_validation_powercli: "DNS Validation — PowerCLI" {shape: rectangle}
time_consistency_check_across_cluste: "Time Consistency Check Across Cluster" {shape: rectangle}

why_this_matters -> ntp_validation_esxi_host: uses
ntp_validation_esxi_host -> ntp_validation_vcenter_appliance: uses
ntp_validation_vcenter_appliance -> dns_validation_esxi_host: uses
dns_validation_esxi_host -> dns_validation_powercli: uses
dns_validation_powercli -> time_consistency_check_across_cluste: uses
```

## Why This Matters

Time and DNS are foundational dependencies for the entire VMware stack. Failures cause cascading issues:

| Problem | Effect |
|---|---|
| Time drift > 5 minutes | Kerberos authentication fails → hosts disconnect from vCenter |
| Time drift between hosts | vSAN resync corruption risk; certificate validation failures |
| Forward DNS failure | vCenter cannot resolve hostnames; hosts can't join domain |
| Reverse DNS failure | SSO authentication may fail; log correlation breaks |
| Certificate time mismatch | vCenter API TLS errors; NSX Manager unreachable |

## NTP Validation — ESXi Host

```bash
# NTP service status and configuration
esxcli system ntp get

# NTP running state
/etc/init.d/ntpd status

# Start/restart NTP daemon
/etc/init.d/ntpd restart

# Current host time
date

# Offset from NTP server (requires ntpq on shell)
ntpq -p

# Configure NTP server
esxcli system ntp set --server=ntp.example.local
esxcli system ntp set --enabled=true
```


```text title="Expected output"
NTP Enabled: true
NTP Servers: [ 0.pool.ntp.org, 1.pool.ntp.org ]
NTP Timeout: 30

ntpd (pid 2847) is running...

Shutting down ntpd:                                        [  OK  ]
Starting ntpd:                                             [  OK  ]

Thu Mar 14 09:47:23 UTC 2024

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 0.pool.ntp.org  .POOL.          16 p    -   64    0    0.000    0.000   0.000
 ntp.example.loc 192.0.2.15       2 u   52   64  377   18.432   -2.147   1.203
 time.google.com 209.112.246.53   1 u   19   64  377   22.891    1.834   0.956

NTP Servers: [ ntp.example.local ]
NTP Enabled: true
```

!!! warning "Common errors"
    **`ntpq: command not found`** — Install ntpq with `esxcli software vib install -n esx-ntp` or verify it's available in the ESXi shell environment.
    **`Error: Unable to set NTP server. Connection refused`** — Ensure the NTP daemon is running with `/etc/init.d/ntpd restart` before applying configuration changes.
    **`Error: The specified NTP server is not reachable`** — Verify network connectivity to ntp.example.local and confirm the hostname resolves correctly with `nslookup ntp.example.local`.
## NTP Validation — vCenter Appliance

```bash
# SSH to vCenter Appliance (VCSA)
# Check chrony (VCSA 6.7+)
chronyc tracking
chronyc sources

# Check time synchronisation status
timedatectl status

# Key output: "System clock synchronized: yes" and offset < 100ms
```


```text title="Expected output"
reference id : 91.189.89.198 (ntp.ubuntu.com)
   stratum   : 2
   ref time  : Wed 2024-01-17 14:32:18.445821234 UTC
   system time : 0.000234567 seconds slow of NTP time
   last update : 42 seconds ago
   RMS offset  : 0.021456 seconds
   frequency  : -12.345 ppm fast
   residual freq: +0.012 ppm
   skew        : 0.089 ppm
   root delay  : 0.043215 seconds
   root dispersion : 0.087654 seconds
   update interval : 64.2 seconds
   leap status : Normal

     Remote Host                       Polling Reach Offset     RMS Taper
==============================================================================
^* 91.189.89.198                        64   377  +0.234ms   0.021ms   1.0x
^- 185.125.190.39                       64   377  +1.456ms   0.045ms   1.0x
^- 162.159.200.123                      64   377  +2.123ms   0.067ms   1.0x

               Local time: Wed 2024-01-17 14:32:18 UTC
           Universal time: Wed 2024-01-17 14:32:18 UTC
                 RTC time: Wed 2024-01-17 14:32:18
                Time zone: UTC (UTC, +0000)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

!!! warning "Common errors"
    **`chronyc: command not found`** — Verify VCSA version is 6.7 or later; older versions use ntpd instead (check with `timedatectl` or `systemctl status ntpd`).
    **`System clock synchronized: no`** — Ensure NTP/Chrony service is running (`systemctl start chrony`) and firewall allows UDP 123 outbound to NTP servers.
    **`offset : 234.567ms`** — Manually sync time with `ntpdate <ntp-server>` or `chronyc makestep`, then verify network connectivity to NTP sources.
## DNS Validation — ESXi Host

```bash
# DNS server configuration
esxcli network ip dns server list

# Forward lookup
nslookup <hostname>
nslookup vcenter.example.local

# Reverse lookup (PTR record)
nslookup <ip_address>
nslookup 10.0.0.10

# Verify hostname resolves to correct IP
getent hosts <hostname>
```


```text title="Expected output"
# DNS server configuration
esxcli network ip dns server list
DNS Server List
===============
10.0.0.1
10.0.0.2

# Forward lookup
nslookup <hostname>
nslookup vcenter.example.local
Server:		10.0.0.1
Address:	10.0.0.1#53

Name:	vcenter.example.local
Address: 10.0.1.50

# Reverse lookup (PTR record)
nslookup <ip_address>
nslookup 10.0.0.10
Server:		10.0.0.1
Address:	10.0.0.1#53

10.0.0.10.in-addr.arpa	name = esx-host-02.example.local.

# Verify hostname resolves to correct IP
getent hosts <hostname>
10.0.1.50       vcenter.example.local vcenter
```

!!! warning "Common errors"
    **`** server can't find vcenter.example.local: NXDOMAIN`** — Verify the hostname is spelled correctly and exists in DNS, or check that DNS servers are reachable with `esxcli network ip dns server list`.
    **`nslookup: can't resolve '(null)': Name or service not known`** — Replace the placeholder `<hostname>` or `<ip_address>` with an actual hostname or IP address before running the command.
    **`getent hosts: command not found`** — Use `cat /etc/hosts` or `nslookup` instead, as `getent` may not be available in ESXi environments.
## DNS Validation — PowerCLI

```powershell
# DNS settings on each host
Get-VMHost | ForEach-Object {
    $net = Get-VMHostNetwork -VMHost $_
    [PSCustomObject]@{
        Host     = $_.Name
        DNS1     = $net.DnsAddress[0]
        DNS2     = $net.DnsAddress[1]
        Domain   = $net.DomainName
        Hostname = $net.HostName
    }
}

# Validate hostname resolves correctly
Resolve-DnsName vcenter.example.local
Resolve-DnsName 10.0.0.10   # reverse lookup
```

## Time Consistency Check Across Cluster

```powershell
# Compare host times (requires SSH or WMI access)
Get-VMHost | Sort-Object Name | ForEach-Object {
    $esxi = $_
    $hostTime = (Get-View $esxi).ConfigManager
    # Use vCenter's view of host time (not always accurate — use SSH for precise check)
    [PSCustomObject]@{ Host = $esxi.Name; UpTime = $esxi.ExtensionData.Summary.Runtime.BootTime }
}
```

## Pre-Change Validation Checklist

```bash
# Run on each ESXi host before maintenance

# 1. NTP status
esxcli system ntp get

# 2. Time offset (acceptable range: < 1 second from reference)
ntpq -p | grep -v "^#\|^="

# 3. Forward DNS
nslookup $(hostname)

# 4. Reverse DNS
nslookup $(esxcfg-nics -l | grep vmnic0 | awk '{print $5}')

# 5. vCenter hostname resolves
nslookup vcenter.example.local
```


```text title="Expected output"
enabled: true
server: 0.pool.ntp.org 1.pool.ntp.org 2.pool.ntp.org
running: true

     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
 0.pool.ntp.o    .POOL.          16 p    -   64    0    0.000    0.000   0.000
 1.pool.ntp.o    .POOL.          16 p    -   64    0    0.000    0.000   0.000
 2.pool.ntp.o    .POOL.          16 p    -   64    0    0.000    0.000   0.000
*ntp.ubuntu.com  132.163.96.1     2 u   52   64  377   18.432    0.127   0.156

Server:		192.168.1.10
Address:	192.168.1.10#53

Name:	esx-host-04.lab.local
Address: 192.168.1.145

Server:		192.168.1.10
Address:	192.168.1.10#53

145.1.168.192.in-addr.arpa	name = esx-host-04.lab.local.

Server:		192.168.1.10
Address:	192.168.1.10#53

Name:	vcenter.example.local
Address: 192.168.1.50
```

!!! warning "Common errors"
    **`** server can't find vcenter.example.local: NXDOMAIN`** — Verify vcenter.example.local hostname in DNS or update the nslookup command with the correct FQDN.
    **`ntpq: read: Connection refused`** — Ensure NTP daemon is running with `systemctl start ntpd` or verify ESXi NTP service is enabled via `esxcli system ntp set --enabled=true`.
    **`nslookup: command not found`** — Use `dig` or `host` command instead, or verify DNS tools are available in the ESXi shell environment.
## Common Issues and Fixes

| Issue | Symptom | Fix |
|---|---|---|
| NTP not running | `ntpd status` shows stopped | `esxcli system ntp set --enabled=true` + restart |
| Wrong NTP server | `ntpq -p` shows no sync | `esxcli system ntp set --server=<correct_ntp>` |
| Time drift > 5 min | Hosts disconnect from vCenter | Force time sync: `date -s` (temporary), fix NTP |
| No PTR record | Reverse lookup fails | Add PTR record in DNS for each host/VMk IP |
| DNS server unreachable | `nslookup` times out | Check network connectivity to DNS servers |
