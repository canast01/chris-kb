---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "DNS Resolution Failures reference covering Overview, Failure Classification, Diagnostic Flowchart, DNS Server Health Checks, Zone Transfer Verification..."
---
# DNS Resolution Failures

<div class="kb-summary">
DNS Resolution Failures reference covering Overview, Failure Classification, Diagnostic Flowchart, DNS Server Health Checks, Zone Transfer Verification and 6 more sections.
</div>

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

DNS failures cascade rapidly across infrastructure: Kerberos authentication breaks without PTR records, NFS mounts fail, application service discovery stops, and vMotion can fail. This guide provides structured diagnosis from failure type through to resolution across Windows DNS and BIND/named environments.

---

## Failure Classification

| Failure Type | DNS Response | Symptom | Likely Cause |
|---|---|---|---|
| NXDOMAIN | Name does not exist | App cannot connect; "unknown host" | Missing A/AAAA record; wrong zone |
| SERVFAIL | Server failed | Intermittent failures; slow resolution | Forwarding loop; zone load failure |
| Timeout (no response) | No DNS answer | Complete resolution failure | DNS server down; firewall on UDP 53 |
| Wrong record returned | Resolves but wrong IP | App connects to wrong host; auth fails | Stale record; split-brain misconfiguration |
| PTR missing | Reverse lookup fails | Kerberos fails; NFS mount denied; SMTP rejected | PTR not created; reverse zone missing |
| Conditional forwarder broken | NXDOMAIN for external domain | Cross-domain trust auth fails | Forwarder IP wrong; firewall blocks |
| Cache poisoning | Incorrect cached answer | Security incident; intermittent wrong routing | DNSSEC failure; rogue response injected |

---

## Diagnostic Flowchart

```d2
direction: right

A: "DNS Failure Reported" {shape: rectangle}
B: "Identify failure type" {shape: rectangle}
P: "Check all DNS zones\nSplit-brain DNS?" {shape: rectangle}
Q: "Compare internal vs external answers\ndig @internal vs dig @8.8.8.8" {shape: rectangle}
R: "Identify reverse zone\ndig -x IP" {shape: rectangle}
S: "Add PTR record to reverse zone\nVerify delegated reverse zone" {shape: rectangle}
D: "Record missing?\nCheck zone for A/AAAA record" {shape: rectangle}
F: "Check zone file syntax\nReload zone: rndc reload" {shape: rectangle}
G: "Record genuinely missing\nAdd DNS record" {shape: rectangle}
H: "Check DNS server health\nsystemctl status named" {shape: rectangle}
J: "Start service\nCheck named.conf syntax: named-checkconf" {shape: rectangle}
K: "Check forwarder chain\ndig @forwarder hostname" {shape: rectangle}
L: "Verify UDP 53 open\nnc -zu dnsserver 53" {shape: rectangle}
N: "Fix firewall rule\nCheck ACL on DNS server" {shape: rectangle}
O: "Check DNS server load\nRestart if overloaded" {shape: rectangle}
T: "Test forwarder directly\ndig @forwarder-ip domain" {shape: rectangle}
V: "Fix forwarder IP\nCheck connectivity to remote DNS" {shape: rectangle}
W: "Check local forwarder config\nnslookup -type=SOA domain" {shape: rectangle}

A -> B
P -> Q
R -> S
```

### SRV Records (critical for AD/Kerberos)

```bash
# Locate Kerberos KDC for a domain
dig _kerberos._tcp.corp.example.com SRV

# Expected output:
# _kerberos._tcp.corp.example.com. 600 IN SRV 0 100 88 dc01.corp.example.com.
# _kerberos._tcp.corp.example.com. 600 IN SRV 0 100 88 dc02.corp.example.com.

# Locate LDAP servers
dig _ldap._tcp.corp.example.com SRV

# Locate PDC emulator
dig _kerberos._tcp.dc._msdcs.corp.example.com SRV
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> _kerberos._tcp.corp.example.com SRV
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 2

;; QUESTION SECTION:
;_kerberos._tcp.corp.example.com. IN	SRV

;; ANSWER SECTION:
_kerberos._tcp.corp.example.com. 600 IN SRV 0 100 88 dc01.corp.example.com.
_kerberos._tcp.corp.example.com. 600 IN SRV 0 100 88 dc02.corp.example.com.

;; ADDITIONAL SECTION:
dc01.corp.example.com.	3600 IN A	192.168.1.10
dc02.corp.example.com.	3600 IN A	192.168.1.11

; <<>> DiG 9.16.1-Ubuntu <<>> _ldap._tcp.corp.example.com SRV
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 41923

;; ANSWER SECTION:
_ldap._tcp.corp.example.com. 600 IN SRV 0 100 389 dc01.corp.example.com.
_ldap._tcp.corp.example.com. 600 IN SRV 0 100 389 dc02.corp.example.com.

; <<>> DiG 9.16.1-Ubuntu <<>> _kerberos._tcp.dc._msdcs.corp.example.com SRV
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37654

;; ANSWER SECTION:
_kerberos._tcp.dc._msdcs.corp.example.com. 600 IN SRV 0 100 88 dc01.corp.example.com.
```

!!! warning "Common errors"
    **`; <<>> DiG 9.16.1-Ubuntu <<>> _kerberos._tcp.corp.example.com SRV ... status: NXDOMAIN`** — Verify the domain name is correct and that DNS SRV records exist; check with your DNS administrator or use `nslookup -type=SRV` to confirm record presence.
    **`; connection timed out; trying next origin`** — Confirm the DNS server is reachable and responding; add `@<dns-server-ip>` to the dig command to explicitly query a specific nameserver (e.g., `dig @8.8.8.8 _kerberos._tcp.corp.example.com SRV`).
---

## DNS Server Health Checks

### Windows DNS (PowerShell)

```powershell
# Get DNS server configuration
Get-DnsServer -ComputerName dc01.corp.example.com | Select-Object *

# List all zones
Get-DnsServerZone -ComputerName dc01.corp.example.com |
    Select-Object ZoneName, ZoneType, IsAutoCreated, DynamicUpdate, ReplicationScope |
    Format-Table -AutoSize

# Check zone for specific record
Resolve-DnsName -Name app01.corp.example.com -Server dc01.corp.example.com -Type A

# Check conditional forwarders
Get-DnsServerZone -ComputerName dc01 | Where-Object {$_.ZoneType -eq 'Forwarder'} |
    Select-Object ZoneName, MasterServers

# Test DNS resolution and measure response time
Measure-Command { Resolve-DnsName -Name app01.corp.example.com -Server dc01 }

# Clear DNS server cache
Clear-DnsServerCache -ComputerName dc01 -Force

# Check DNS debug logging (enable for detailed diagnostics)
Set-DnsServerDiagnostics -ComputerName dc01 -All $true
# Logs to: C:\Windows\System32\dns\dns.log
```

### Linux (BIND / named)

```bash
# Check service status
systemctl status named
# or
systemctl status bind9

# Validate configuration syntax before restart
named-checkconf /etc/named.conf

# Validate zone file
named-checkzone corp.example.com /var/named/corp.example.com.zone

# Reload zones without restarting
rndc reload

# Flush DNS cache
rndc flush

# Check named statistics
rndc stats
cat /var/named/data/named_stats.txt | grep -E "queries|errors"

# Live query logging (enable temporarily)
rndc querylog on
tail -f /var/log/named/queries.log
```


```text title="Expected output"
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Thu 2024-01-18 14:32:15 UTC; 2 days ago
   Main PID: 2847 (named)
      Tasks: 13 (limit: 4915)
     Memory: 48.3M
        CPU: 2min 34s
     CGroup: /system.slice/named.service
             └─2847 /usr/sbin/named -f -u named

(no output — command completes silently)

zone corp.example.com/IN: loaded serial 2024011801
OK

(no output — command completes silently)

(no output — command completes silently)

 ++  Statistics Dump  ++
 (created Thu Jan 18 14:35:22 2024)
 Success: 1247
 AuthQuery: 892
 RecursiveQuery: 355
 QueryErrors: 3
 Queries: 1250
 Errors: 8

query logging is now on
Jan 18 14:35:45 ns1 named[2847]: client 192.168.1.105#54321 (mail.corp.example.com): query: mail.corp.example.com IN A +E (192.168.1.10)
Jan 18 14:35:46 ns1 named[2847]: client 192.168.1.106#52847 (api.corp.example.com): query: api.corp.example.com IN A +E (192.168.1.11)
```

!!! warning "Common errors"
    **`rndc: connect failed: 127.0.0.1#953: connection refused`** — Ensure named is running with `systemctl start named` and rndc key is configured in `/etc/rndc.conf`.
    **`zone corp.example.com/IN: loading from master file /var/named/corp.example.com.zone failed: file not found`** — Verify the zone file path exists and the filename matches the zone name in `/etc/named.conf`.
    **`named: error (SERVFAIL) resolving 'example.com/A/IN': 192.0.2.1#53: timed out`** — Check network connectivity to upstream nameservers and firewall rules allowing outbound DNS on port 53.
---

## Zone Transfer Verification

```bash
# Test if zone transfer is permitted (AXFR)
dig AXFR corp.example.com @dc01.corp.example.com

# If permitted, output shows all zone records
# If blocked:
# ; Transfer failed.
# corp.example.com.  0  IN  SOA  dc01... (and no records)

# Check SOA serial number matches between primary and secondary
dig SOA corp.example.com @dc01.corp.example.com
dig SOA corp.example.com @dc02.corp.example.com
# Serial numbers must match after replication; mismatch = replication issue
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> AXFR corp.example.com @dc01.corp.example.com
; (1 server found)
;; global options: +cmd
corp.example.com.		3600	IN	SOA	dc01.corp.example.com. hostmaster.corp.example.com. 2024011501 3600 1800 604800 86400
corp.example.com.		3600	IN	NS	dc01.corp.example.com.
corp.example.com.		3600	IN	NS	dc02.corp.example.com.
corp.example.com.		3600	IN	A	192.168.1.10
mail.corp.example.com.		3600	IN	A	192.168.1.20
web.corp.example.com.		3600	IN	A	192.168.1.30
...
corp.example.com.		3600	IN	SOA	dc01.corp.example.com. hostmaster.corp.example.com. 2024011501 3600 1800 604800 86400
;; Query time: 2 msec
;; SERVER: 192.168.1.5#53(192.168.1.5)
;; WHEN: Mon Jan 15 14:32:18 UTC 2024
;; XFR size: 12 records (messages 1, bytes 287)

; <<>> DiG 9.16.1-Ubuntu <<>> SOA corp.example.com @dc01.corp.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54321
corp.example.com.		3600	IN	SOA	dc01.corp.example.com. hostmaster.corp.example.com. 2024011501 3600 1800 604800 86400
;; Query time: 1 msec
;; SERVER: 192.168.1.5#53(192.168.1.5)

; <<>> DiG 9.16.1-Ubuntu <<>> SOA corp.example.com @dc02.corp.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
corp.example.com.		3600	IN	SOA	dc02.corp.example.com. hostmaster.corp.example.com. 2024011501 3600 1800 604800 86400
;; Query time: 3 msec
;; SERVER: 192.168.1.6#53(192.168.1.6)
```

!!! warning "Common errors"
    **`; Transfer failed.`** — Verify the secondary DNS server is configured as an authorized zone transfer recipient in the primary's ACL (allow-transfer directive in named.conf).
    **`; status: SERVFAIL`** — Check that the DNS server at the specified IP is running and listening on port 53 using `netstat -tuln | grep :53` or `ss -tuln | grep :53`.
    **`connection timed out; no servers could be reached`**
---

## Conditional Forwarder Testing

```bash
# Test resolution through a conditional forwarder
# Example: corp.example.com forwarder should reach 10.10.1.10
dig @10.10.1.10 host.corp.example.com

# Test forwarder for external partner domain
dig @10.10.1.10 server.partner.com

# Trace the full path (shows if forwarder is being used)
dig +trace @dc01 server.partner.com
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> @10.10.1.10 host.corp.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;host.corp.example.com.		IN	A

;; ANSWER SECTION:
host.corp.example.com.	300	IN	A	10.20.5.42

;; Query time: 12 msec
;; SERVER: 10.10.1.10#53(10.10.1.10)
;; WHEN: Wed Jan 15 14:23:18 UTC 2025
;; MSG SIZE  rcvd: 58

; <<>> DiG 9.16.1-Ubuntu <<>> @10.10.1.10 server.partner.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19234
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;; QUESTION SECTION:
;server.partner.com.		IN	A

;; ANSWER SECTION:
server.partner.com.	3600	IN	A	203.45.67.89

;; Query time: 45 msec
;; SERVER: 10.10.1.10#53(10.10.1.10)
;; WHEN: Wed Jan 15 14:23:19 UTC 2025
;; MSG SIZE  rcvd: 54

; <<>> DiG 9.16.1-Ubuntu <<>> +trace @dc01 server.partner.com
; (trying to find the name server address for dc01)
; (1 server found)
;; global options: +cmd
;.			518400	IN	NS	a.root-servers.net.
;.			518400	IN	NS	b.root-servers.net.
;; Received 512 bytes from 10.10.1.10#53(dc01) in 89 ms
;com.			172800	IN	NS	a.gtld-servers.net.
;; Received 512 bytes from a.root-servers.net#53(a.root-servers.net) in 78 ms
;partner.com.		172800	IN	NS	ns1.partner.com.
;; Received 512 bytes from a.gtld-servers.net#53(a.gtld-servers.net) in 92 ms
;server.partner.com.	3600	IN	A	203.45.67.89
;; Received 54 bytes from ns1.partner.com#53(ns1.partner.com) in 156 ms
```

!!! warning "Common errors"
    **`dig: couldn't get address for 'dc01': not found`** — Use the full FQDN or IP address of the DNS server (e.g.,
---

## Split-Brain DNS Verification

Split-brain DNS serves different answers internally vs externally (common for public services with private back-ends).

```bash
# Compare internal resolution
dig @dc01.corp.example.com app.example.com

# Compare external resolution
dig @8.8.8.8 app.example.com

# If answers differ — this is intentional split-brain
# Document expected internal vs external IPs
# If they should match and don't — investigate zone records

# Check which view is being served (BIND views)
dig @nameserver app.example.com +short  # from internal IP
dig @nameserver app.example.com +short  # from external IP (via VPN off)
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> @dc01.corp.example.com app.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 0

;; ANSWER SECTION:
app.example.com.		300	IN	A	10.42.1.15

; <<>> DiG 9.16.1-Ubuntu <<>> @8.8.8.8 app.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19234
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 4, ADDITIONAL: 0

;; ANSWER SECTION:
app.example.com.		3600	IN	A	203.0.113.42

10.42.1.15
203.0.113.42
```

!!! warning "Common errors"
    **`dig: couldn't get address for 'dc01.corp.example.com': not known`** — Verify the internal nameserver hostname is resolvable or use its IP address directly (e.g., `dig @10.20.0.5 app.example.com`).
    **`; <<>> DiG 9.16.1-Ubuntu <<>> @nameserver app.example.com` followed by `; connection timed out; trying next origin`** — Replace the placeholder `@nameserver` with an actual IP or hostname (e.g., `@10.20.0.5` or `@dc01.corp.example.com`).
---

## PTR Record Validation

PTR records are mandatory for Kerberos mutual authentication and NFS access control.

```bash
# Verify PTR exists for all servers in a subnet
for ip in 10.10.1.{50..60}; do
    result=$(dig -x $ip +short)
    echo "$ip -> ${result:-MISSING}"
done

# Example output:
# 10.10.1.50 -> app01.corp.example.com.
# 10.10.1.51 -> MISSING          ← will cause Kerberos/NFS failures
# 10.10.1.52 -> db01.corp.example.com.

# Add missing PTR (Windows DNS)
Add-DnsServerResourceRecordPtr -ZoneName "1.10.10.in-addr.arpa" `
    -Name "51" -PtrDomainName "app02.corp.example.com" `
    -ComputerName dc01.corp.example.com
```


```text title="Expected output"
10.10.1.50 -> app01.corp.example.com.
10.10.1.51 -> MISSING
10.10.1.52 -> db01.corp.example.com.
10.10.1.53 -> web02.corp.example.com.
10.10.1.54 -> MISSING
10.10.1.55 -> cache01.corp.example.com.
10.10.1.56 -> MISSING
10.10.1.57 -> ntp01.corp.example.com.
10.10.1.58 -> MISSING
10.10.1.59 -> app03.corp.example.com.
10.10.1.60 -> mon01.corp.example.com.
```

!!! warning "Common errors"
    **`dig: couldn't get address for 'dc01.corp.example.com': not known`** — Verify the DNS server hostname is resolvable or use its IP address instead in the -ComputerName parameter.
    **`Access Denied`** — Ensure your user account has DNS admin privileges on the domain controller or run PowerShell as Administrator.
---

## Common Failure Scenarios

| Scenario | Root Cause | Fix |
|---|---|---|
| Kerberos KRB5KDC_ERR_C_PRINCIPAL_UNKNOWN | Missing PTR for client IP | Add PTR record in reverse zone |
| NFS mount fails with "access denied" | NFS server cannot reverse-resolve client | Add PTR for NFS client |
| vMotion fails "destination host not reachable" | Hostname of destination host not resolvable | Verify A and PTR for ESXi management IP |
| App can ping IP but not hostname | Missing or wrong A record | Check zone; correct A record |
| Cross-forest auth fails | Conditional forwarder for partner domain broken | Re-create conditional forwarder |
| Intermittent failures same hostname | DNS round-robin; one server down | Check all A records; remove unhealthy IP |
| New server not resolving | Dynamic DNS registration failed | Run `ipconfig /registerdns`; check DHCP scope DNS |
| External name resolves internally to public IP | Missing internal split-brain zone entry | Add internal zone record |
| SMTP email rejected | PTR for mail server IP missing | Add PTR matching MX hostname |

---

## DNS Cache Poisoning Checks

```bash
# Check DNSSEC validation status (Linux resolver)
dig +dnssec corp.example.com

# Look for AD (Authenticated Data) flag in response
# ;; flags: qr rd ra ad;   ← 'ad' flag = DNSSEC validated

# Check DNSSEC on Windows DNS
Get-DnsServerDnsSecZone -ComputerName dc01

# Verify response source matches expected nameserver
dig corp.example.com | grep "SERVER:"
# ;; SERVER: 10.10.1.10#53(10.10.1.10)
```


```text title="Expected output"
; <<>> DiG 9.16.1-Ubuntu <<>> +dnssec corp.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 1

;; QUESTION SECTION:
;corp.example.com.		IN	A

;; ANSWER SECTION:
corp.example.com.	3600	IN	A	192.168.10.45
corp.example.com.	3600	IN	RRSIG	A 8 3 3600 20240215120000 20240201120000 12847 example.com. M7x...

;; AUTHORITY SECTION:
example.com.		86400	IN	NS	ns1.example.com.
example.com.		86400	IN	RRSIG	NS 8 2 86400 20240215120000 20240201120000 12847 example.com. K9p...

;; Query time: 45 msec
;; SERVER: 10.10.1.10#53(10.10.1.10)
;; WHEN: Wed Feb 07 14:32:18 UTC 2024
;; MSG SIZE  rcvd: 287
```

!!! warning "Common errors"
    **`status: SERVFAIL`** — Check that the recursive resolver has DNSSEC validation enabled and can reach the root nameservers; disable DNSSEC temporarily with `dig +no-dnssec` to isolate the issue.
    **`dig: couldn't get address for 'corp.example.com': not found`** — Verify the domain name spelling and that the resolver can reach authoritative nameservers using `dig @8.8.8.8 corp.example.com` to test with a public resolver.
    **`flags: qr rd ra;` (no 'ad' flag present)`** — The resolver is not validating DNSSEC; check resolver configuration with `systemctl status systemd-resolved` on Linux or enable DNSSEC in `/etc/resolv.conf`.
---

## Escalation Criteria

Escalate to DNS / AD team or network team when:

- All DNS servers for a zone are unreachable simultaneously
- Zone serial number divergence persists after 30 minutes (replication broken)
- DNSSEC validation failures indicate potential cache poisoning or key rollover issue
- AD-integrated DNS zone is not replicating (check AD replication health: `repadmin /replsummary`)
- DNS resolution fails only for specific VLANs (ACL or scoped response misconfiguration)
- Wildcard records or unexpected record changes discovered (security incident)
- PTR record inconsistencies affect more than 20 hosts (systematic reverse zone issue)

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Network Connectivity Troubleshooting](../network-connectivity/)
- [Networking — Known Issues](../known-issues.md)
- [Networking — Troubleshooting Overview](../)
