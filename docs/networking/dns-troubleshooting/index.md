# DNS Troubleshooting

## Symptoms

- Hostname fails to resolve; application errors by name but not by IP
- Intermittent resolution failures — services randomly unreachable
- NFS/CIFS mounts failing (PTR record missing)
- Authentication failures (Kerberos requires working forward + reverse DNS)

## Triage Steps

### 1. Test Resolution Directly

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```

### 2. Check Configured DNS Servers

**Linux:**
```bash
cat /etc/resolv.conf
resolvectl status
```

**Windows:**
```powershell
Get-DnsClientServerAddress
ipconfig /all | findstr DNS
```

### 3. Test DNS Server Reachability

```bash
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```

### 4. Forward and Reverse Resolution

```bash
# Forward: name → IP
dig <hostname>

# Reverse: IP → name (PTR)
dig -x <ip>
nslookup <ip>
```

Missing PTR records cause Kerberos failures and NFS/CIFS auth issues.

### 5. Flush DNS Cache

**Windows:**
```cmd
ipconfig /flushdns
```

**Linux (systemd-resolved):**
```bash
resolvectl flush-caches
# or
systemctl restart systemd-resolved
```

### 6. Test from Multiple Systems

If one server resolves but another doesn't, the issue is host-specific — wrong server configured, stale cache, or host firewall blocking UDP 53.

## Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| NXDOMAIN | Record missing or wrong zone | Add/fix DNS record |
| Timeout | DNS server unreachable | Check firewall and DNS health |
| Wrong IP returned | Stale or duplicate record | Flush cache; fix record |
| Reverse lookup fails | Missing PTR record | Add PTR in DNS |
| Works by IP not name | Wrong DNS configured | Fix `/etc/resolv.conf` or DHCP |
