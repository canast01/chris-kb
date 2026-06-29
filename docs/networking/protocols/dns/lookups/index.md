---
tags:
  - networking
---
# DNS Lookups

<div class="kb-summary">
DNS Lookups reference covering Overview, nslookup, dig, Resolve-DnsName (PowerShell), TTL Debugging and 1 more sections.
</div>

        FORWARD vs REVERSE LOOKUPS

```d2
direction: down

nslookup: "nslookup" {shape: rectangle}
dig: "dig" {shape: rectangle}
resolvednsname_powershell: "Resolve-DnsName (PowerShell)" {shape: rectangle}
ttl_debugging: "TTL Debugging" {shape: rectangle}
known_issues: "Known Issues" {shape: rectangle}

nslookup -> dig: uses
dig -> resolvednsname_powershell: uses
resolvednsname_powershell -> ttl_debugging: uses
ttl_debugging -> known_issues: uses
```

## Overview

DNS lookups translate hostnames to IPs (forward) and IPs to hostnames (reverse). Tools vary by OS: `nslookup` is universal, `dig` is preferred on Linux/macOS for detailed output, and `Resolve-DnsName` is the PowerShell equivalent on Windows. TTL inspection is essential when debugging stale cache issues.

## nslookup

```bash
# Forward lookup using default resolver
nslookup www.example.com

# Forward lookup against a specific server
nslookup www.example.com 10.0.0.53

# Reverse lookup (PTR)
nslookup 192.168.10.55

# Query a specific record type
nslookup -type=MX example.com 10.0.0.53
nslookup -type=SRV _ldap._tcp.example.local 10.0.0.53

# Interactive mode — query multiple records
nslookup
> server 10.0.0.53
> set type=A
> host.example.local
> exit
```


```text title="Expected output"
Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
Name:	www.example.com
Address: 203.0.113.42

Server:		10.0.0.53
Address:	10.0.0.53#53

Name:	www.example.com
Address: 203.0.113.42

Server:		192.168.1.1
Address:	192.168.1.1#53

Non-authoritative answer:
55.10.168.192.in-addr.arpa	name = mail.example.local.

Server:		10.0.0.53
Address:	10.0.0.53#53

example.com	preference = 10, mail exchanger = mail.example.com.
example.com	preference = 20, mail exchanger = mail2.example.com.

Server:		10.0.0.53
Address:	10.0.0.53#53

_ldap._tcp.example.local	service = 0 100 389 ldap01.example.local.
_ldap._tcp.example.local	service = 0 100 389 ldap02.example.local.

> Default server set to 10.0.0.53
> Default query type set to A
> Server:		10.0.0.53
> Address:	10.0.0.53#53
> 
> Name:	host.example.local
> Address: 10.20.30.15
```

!!! warning "Common errors"
    **`** server can't find www.example.com: NXDOMAIN`** — Verify the domain name is correct and the DNS server is reachable with `ping 10.0.0.53`.
    **`** Timed out`** — Check network connectivity to the DNS server and ensure port 53 is not blocked by a firewall.
    **`** connection timed out; try again`** — Increase the timeout or switch to a working DNS server; verify the IP address with `nslookup 10.0.0.53`.
## dig

```bash
# Basic forward lookup
dig www.example.com

# Lookup against specific server
dig @10.0.0.53 www.example.local

# Reverse lookup
dig -x 192.168.10.55

# Query specific type with short output
dig @10.0.0.53 MX example.com +short

# Check TTL remaining in a response
dig @10.0.0.53 www.example.local | grep -A1 "ANSWER SECTION"

# Trace full resolution path
dig +trace www.example.com
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;www.example.com.		IN	A

;; ANSWER SECTION:
www.example.com.	3600	IN	A	93.184.216.34

;; Query time: 45 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
;; WHEN: Mon Jan 15 14:22:31 UTC 2024
;; MSG SIZE  rcvd: 60

10.0.0.53 www.example.local. 300 IN A 10.20.30.40

55.10.168.192.in-addr.arpa. 7200 IN PTR host-55.internal.local.

10 IN MX 10 mail.example.com.
20 IN MX 20 mail2.example.com.

;; ANSWER SECTION:
www.example.local.	300	IN	A	10.20.30.40

;; Trace output:
.			518400	IN	NS	a.root-servers.net.
com.			172800	IN	NS	a.gtld-servers.net.
example.com.		172800	IN	NS	ns1.example.com.
www.example.com.	3600	IN	A	93.184.216.34
```

!!! warning "Common errors"
    **`dig: couldn't get address for '@10.0.0.53': not known`** — Verify the DNS server IP is reachable and correct; check network connectivity with `ping 10.0.0.53`.
    **`; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com ; (SERVFAIL)`** — The DNS server returned SERVFAIL, indicating it cannot resolve the query; verify the domain exists and the DNS server has proper zone configuration or forwarders.
    **`; <<>> DiG 9.16.1-Ubuntu <<>> www.example.com ; (NXDOMAIN)`** — The domain does not exist in the DNS system; confirm the correct domain name and check if it is registered and properly configured.
## Resolve-DnsName (PowerShell)

```powershell
# Basic forward lookup
Resolve-DnsName www.example.local

# Query a specific DNS server
Resolve-DnsName www.example.local -Server 10.0.0.53

# Reverse lookup
Resolve-DnsName 192.168.10.55

# Query specific record type
Resolve-DnsName corp.local -Type MX -Server 10.0.0.53
Resolve-DnsName _ldap._tcp.example.local -Type SRV

# Bypass cache (go direct to server)
Resolve-DnsName www.example.local -Server 10.0.0.53 -DnsOnly
```

## TTL Debugging

| Symptom | Check |
|---------|-------|
| Old IP returned after DNS update | TTL not yet expired — wait or flush cache |
| TTL shows 0 or very low | Record set for rapid expiry (e.g. during migration) |
| Different TTL from different servers | Secondary not yet replicated from primary |
| Negative cache (NXDOMAIN) | Negative TTL (SOA minimum) is caching the miss |

```bash
# Flush DNS cache on Windows client
ipconfig /flushdns

# Flush DNS cache on Linux (systemd-resolved)
resolvectl flush-caches

# Check cached TTL with dig (TTL column in answer section)
dig @8.8.8.8 www.example.com

# Clear DNS server cache on Windows DNS
Clear-DnsServerCache -Force
```


```text title="Expected output"
Windows IP Configuration

Successfully flushed the DNS Resolver Cache.

Flushed all of the following DNS caches:
  LLMNR Cache

; <<>> DiG 9.16.1-Ubuntu <<>> @8.8.8.8 www.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;www.example.com.			IN	A

;; ANSWER SECTION:
www.example.com.		3599	IN	A	93.184.216.34

;; Query time: 45 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Jan 15 14:32:18 UTC 2024
;; MSG SIZE  rcvd: 60
```

!!! warning "Common errors"
    **`command not found: resolvectl`** — Install systemd-resolved with `sudo apt install systemd-resolved` or use `sudo systemctl restart systemd-resolved` if already installed.
    **`The term 'Clear-DnsServerCache' is not recognized`** — Run PowerShell as Administrator and ensure you are on a Windows DNS server with the DnsServer module installed via `Import-Module DnsServer`.
    **`connection timed out; no servers could be reached`** — Verify network connectivity and that the DNS server 8.8.8.8 is reachable with `ping 8.8.8.8` before retrying the dig command.
## Known Issues

- `nslookup` and `Resolve-DnsName` may return different results because `Resolve-DnsName` uses the Windows DNS client cache while `nslookup` queries the resolver directly. Always specify `-Server` to rule out cache differences.
- A forward lookup succeeds but reverse lookup fails: the PTR record is missing or the reverse zone does not exist. Check `10.168.192.in-addr.arpa` exists on the DNS server.
- `dig +trace` follows from root hints; results may differ from what an internal forwarder returns. Use `dig @<internal-server>` for split-brain validation.
