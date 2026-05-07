# DNS and NTP Validation
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
esxcli system ntp set --server=ntp.corp.local
esxcli system ntp set --enabled=true
```

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

## DNS Validation — ESXi Host

```bash
# DNS server configuration
esxcli network ip dns server list

# Forward lookup
nslookup <hostname>
nslookup vcenter.corp.local

# Reverse lookup (PTR record)
nslookup <ip_address>
nslookup 10.0.0.10

# Verify hostname resolves to correct IP
getent hosts <hostname>
```

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
Resolve-DnsName vcenter.corp.local
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
nslookup vcenter.corp.local
```

## Common Issues and Fixes

| Issue | Symptom | Fix |
|---|---|---|
| NTP not running | `ntpd status` shows stopped | `esxcli system ntp set --enabled=true` + restart |
| Wrong NTP server | `ntpq -p` shows no sync | `esxcli system ntp set --server=<correct_ntp>` |
| Time drift > 5 min | Hosts disconnect from vCenter | Force time sync: `date -s` (temporary), fix NTP |
| No PTR record | Reverse lookup fails | Add PTR record in DNS for each host/VMk IP |
| DNS server unreachable | `nslookup` times out | Check network connectivity to DNS servers |
