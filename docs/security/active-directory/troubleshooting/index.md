# AD Troubleshooting

AD failures typically trace back to replication, DNS, time sync, or Kerberos. This page covers the most common failure categories with diagnostic commands.

## Replication Errors

AD replication failures cause inconsistent directory state across DCs. Start with `repadmin` to identify the scope.

```cmd
# Show replication status for all partners
repadmin /showrepl

# Show replication summary (good overview)
repadmin /replsummary

# Force replication from a specific source DC
repadmin /replicate dc02.corp.example.com dc01.corp.example.com "DC=corp,DC=example,DC=com"

# Force full sync from all partners
repadmin /syncall /AdeP

# Show replication errors only
repadmin /showrepl * /csv > C:\repl-errors.csv
```

## Common Replication Error Codes

| Error Code | Meaning | Common Fix |
|---|---|---|
| 8453 | Replication access denied | Check AD permissions on NC head |
| 1722 | RPC server unavailable | Check firewall, DNS, DC connectivity |
| 8606 | Insufficient attributes | USN rollback — restore or demote DC |
| 8614 | Replication quarantine | DC offline too long — check tombstone lifetime |
| -2146893022 | Target principal name incorrect | Time skew or SPN issue |

## Dcdiag Tests

```cmd
# Full dcdiag run
dcdiag /test:all /v /f:C:\dcdiag-output.txt

# DNS-specific test
dcdiag /test:dns /v

# Connectivity test only
dcdiag /test:connectivity

# Run against a remote DC
dcdiag /s:dc02.corp.example.com /test:replications
```

## Kerberos Failures

Most Kerberos errors stem from time skew (>5 min), DNS, or SPN issues.

```cmd
# Check Kerberos tickets on a client
klist

# Purge Kerberos ticket cache
klist purge

# Check time difference between client and DC
w32tm /stripchart /computer:dc01.corp.example.com /samples:5

# List SPNs for a service account
setspn -L svc-webapp

# Find duplicate SPNs (common cause of Kerberos failures)
setspn -X -F
```

## Time Sync Issues

```cmd
# Check current sync status
w32tm /query /status

# Force resync
w32tm /resync /force

# Check time source hierarchy
w32tm /query /peers

# Configure a workstation to use the domain hierarchy
w32tm /config /syncfromflags:domhier /update
net stop w32tm && net start w32tm
```

## Event Log References

```powershell
# Check Directory Service log for replication errors
Get-WinEvent -LogName "Directory Service" |
    Where-Object {$_.Level -le 3} | Select-Object -First 20 TimeCreated, Id, Message

# Check System log for Netlogon errors
Get-WinEvent -LogName System -ProviderName Netlogon |
    Select-Object -First 20 TimeCreated, Id, Message

# Check for Kerberos errors in Security log
Get-WinEvent -LogName Security |
    Where-Object {$_.Id -in @(4768,4769,4771)} |
    Select-Object -First 20 TimeCreated, Id, Message
```
