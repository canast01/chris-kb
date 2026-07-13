---
title: DNS
tags:
  - networking
description: "Domain Name System (DNS) is the foundational naming protocol of IP networks, resolving hostnames to addresses (and vice versa) over UDP and TCP port 53..."
---

# DNS

<div class="kb-summary">
Domain Name System (DNS) is the foundational naming protocol of IP networks, resolving hostnames to addresses (and vice versa) over UDP and TCP port 53. It is a critical dependency for authentication (Kerberos, LDAP), certificate validation, cloud services, monitoring, and automation — meaning DNS failures cascade across the entire environment. Key operational concerns are zone hygiene, forwarder reliability, recursive vs authoritative role separation, and TTL management.
</div>

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="records/">
  <strong>Records</strong>
  <span>A, AAAA, CNAME, MX, PTR, NS, SOA, TXT, and SRV record types — creation, validation, and TTL tuning.</span>
</a>

<a class="kb-card" href="zones/">
  <strong>Zones</strong>
  <span>Primary, secondary, stub, and conditional forwarder zones — zone transfers, replication, and delegation.</span>
</a>

<a class="kb-card" href="lookups/">
  <strong>Lookups</strong>
  <span>Forward and reverse lookup validation, split-horizon DNS, and resolving recursive vs authoritative responses.</span>
</a>

<a class="kb-card" href="forwarders/">
  <strong>Forwarders</strong>
  <span>Upstream forwarder configuration, conditional forwarders, root hints, and DNS over HTTPS (DoH) forwarding.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>NXDOMAIN, SERVFAIL, stale records, replication failures, split-horizon conflicts, and slow resolution.</span>
</a>

</div>

## Quick Reference

**Record types:**

| Type | Purpose | Example |
|---|---|---|
| A | IPv4 address | `host.example.com → 192.168.1.10` |
| AAAA | IPv6 address | `host.example.com → 2001:db8::1` |
| CNAME | Canonical name alias | `www → host.example.com` |
| MX | Mail exchanger | `example.com → mail.example.com (priority 10)` |
| PTR | Reverse lookup | `10.1.168.192.in-addr.arpa → host.example.com` |
| NS | Nameserver delegation | `example.com → ns1.example.com` |
| SOA | Zone authority | Serial, refresh, retry, expire, minimum TTL |
| TXT | Text records | SPF, DKIM, DMARC, domain verification |
| SRV | Service locator | `_ldap._tcp.example.com → dc01.example.com:389` |

**Zone types:**

| Type | Description |
|---|---|
| Primary | Writable master copy of the zone |
| Secondary | Read-only replica via zone transfer (AXFR/IXFR) |
| Stub | Contains only NS records — used for delegation awareness |
| Conditional forwarder | Forwards specific domain queries to designated servers |

**Port summary:**

| Port | Protocol | Use |
|---|---|---|
| 53/udp | DNS | Standard queries (responses ≤512 bytes or EDNS) |
| 53/tcp | DNS | Large responses, zone transfers (AXFR) |
| 853/tcp | DNS over TLS (DoT) | Encrypted recursive resolution |

## Common Commands / Config

```bash
# Forward lookup with dig
dig A host.example.com

# Reverse lookup (PTR)
dig -x 192.168.1.10

# Query a specific DNS server
dig @192.168.1.10 A host.example.com

# Check authoritative nameservers for a zone
dig NS example.com

# Trace DNS resolution from root
dig +trace host.example.com

# Show full answer with TTL
dig +noall +answer host.example.com

# Check SOA record (serial number, refresh times)
dig SOA example.com

# nslookup (cross-platform)
nslookup host.example.com
nslookup -type=MX example.com

# Windows PowerShell
Resolve-DnsName host.example.com
Resolve-DnsName -Name host.example.com -Server 192.168.1.10 -Type PTR

# Windows: Flush DNS resolver cache
ipconfig /flushdns

# Windows: View DNS cache
ipconfig /displaydns | more

# Linux: Flush systemd-resolved cache
systemd-resolve --flush-caches
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> A host.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52841
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;host.example.com.		IN	A

;; ANSWER SECTION:
host.example.com.	3600	IN	A	192.0.2.45

;; Query time: 12 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Wed Jan 15 14:23:47 UTC 2025
;; MSG SIZE  rcvd: 56

; <<>> DiG 9.16.1-Ubuntu <<>> -x 192.168.1.10
;; ANSWER SECTION:
10.1.168.192.in-addr.arpa. 7200 IN	PTR	router.example.com.

; <<>> DiG 9.16.1-Ubuntu <<>> @192.168.1.10 A host.example.com
;; SERVER: 192.168.1.10#53(192.168.1.10)
;; ANSWER SECTION:
host.example.com.	300	IN	A	192.0.2.45

; <<>> DiG 9.16.1-Ubuntu <<>> NS example.com
;; ANSWER SECTION:
example.com.		172800	IN	NS	ns1.example.com.
example.com.		172800	IN	NS	ns2.example.com.

; <<>> DiG 9.16.1-Ubuntu <<>> +trace host.example.com
.			518400	IN	NS	a.root-servers.net.
.			518400	IN	NS	b.root-servers.net.
example.com.		172800	IN	NS	ns1.example.com.
host.example.com.	3600	IN	A	192.0.2.45

host.example.com.	3600	IN	A	192.0.2.45

; <<>> DiG 9.16.1-Ubuntu <<>> SOA example.com
;; ANSWER SECTION:
example.com.		3600	IN	SOA	ns1.example.com. admin.example.com. 2025011501 10800 3600 604800 86400

Server:		8.8.8.8
Address:	8.8.8.8#53

Name:	host.example.com
Address: 192.0.2.45

Server:		8.8.8.8
Address:	8.8.8.8#53

example.com	nameserver = mail.example.com.
example.com	nameserver = ns1.example.com.

Resolve-DnsName : host.example.com
Name                                           Type   TTL   Section    IPAddress
----                                           ----   ---   -------    ---------
host.example.com                               A      3600  Answer     192.0.2.45

Successfully flushed the DNS Resolver
```
## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `NXDOMAIN` for a known host | Record exists in zone; TTL; split-horizon | Check with `dig @<authoritative-server>`; verify record in zone; check if different internal/external zones exist |
| `SERVFAIL` | Authoritative server unreachable; DNSSEC validation failure | Test with `dig +noedns`; check forwarder connectivity; verify DNSSEC chain if enabled |
| Stale record returning wrong IP | TTL too high; old record not deleted | Flush resolver cache; remove stale record; lower TTL before planned IP changes |
| Zone transfer failing | ACL on primary; TCP 53 blocked | Check `allow-transfer` in BIND config or Windows DNS zone properties; verify TCP port 53 is open |
| Split-horizon conflict | Client resolving external instead of internal | Verify client is using internal DNS servers; check conditional forwarder or zone scope configuration |
| Slow DNS resolution | Forwarder unreachable; recursive resolver overloaded | Test forwarder latency with `dig @<forwarder>`; switch to faster upstream; consider local caching resolver |
