# Network Services

<div class="kb-summary">
Network services knowledge base covering DNS, load balancers, and network service management.
</div>

## DNS Troubleshooting

### Symptoms

- Hostname fails to resolve; application errors by name but not by IP
- Intermittent resolution failures — services randomly unreachable
- NFS/CIFS mounts failing (PTR record missing)
- Authentication failures (Kerberos requires working forward + reverse DNS)

### Triage Steps

#### 1. Test Resolution Directly

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```
```
┌──────────────────────────────────── Networking — Network Services ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Network services: DNS (name resolution), DHCP (IP assignment), load balancers, IPAM      │   │
│   │      DNS: every server needs forward + reverse records; split-horizon for internal names      │   │
│   │       Load balancer: health checks must match app check; monitor pool member state daily      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                     DNS                      │  │             Load Balancer & DHCP            │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │             A record: name → IP              │  │           VIP: virtual IP for pool          │   │
│   │            PTR record: IP → name             │  │            Pool: backend servers            │   │
│   │             CNAME: alias record              │  │            Health check: HTTP/TCP           │   │
│   │             Test: nslookup / dig             │  │           DHCP: scope + exclusions          │   │
│   │        TTL: lower for planned changes        │  │           IPAM: track allocations           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    A record     = DNS forward lookup; hostname → IPv4 address                                         │
│    PTR record   = DNS reverse lookup; IP → hostname; needed for SMTP and some auth                    │
│    TTL          = Time To Live; how long resolvers cache the record; lower before cutover             │
│    Split-horizon= Different DNS answers for internal vs external queries for same name                │
│    VIP          = Virtual IP; load balancer frontend; clients connect here, not to backend            │
│    SNAT         = Source NAT on load balancer; ensures response traffic returns via LB                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

#### 3. Test DNS Server Reachability

```bash
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```

#### 4. Forward and Reverse Resolution

```bash
# Forward: name → IP
dig <hostname>

# Reverse: IP → name (PTR)
dig -x <ip>
nslookup <ip>
```

Missing PTR records cause Kerberos failures and NFS/CIFS auth issues.

#### 5. Flush DNS Cache

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

#### 6. Test from Multiple Systems

If one server resolves but another doesn't, the issue is host-specific — wrong server configured, stale cache, or host firewall blocking UDP 53.

### Common Issues

| Symptom | Cause | Fix |
|---|---|---|
| NXDOMAIN | Record missing or wrong zone | Add/fix DNS record |
| Timeout | DNS server unreachable | Check firewall and DNS health |
| Wrong IP returned | Stale or duplicate record | Flush cache; fix record |
| Reverse lookup fails | Missing PTR record | Add PTR in DNS |
| Works by IP not name | Wrong DNS configured | Fix `/etc/resolv.conf` or DHCP |

## Load Balancer Health

### Overview

This runbook validates load balancer health and backend availability.

### Pre-Checks

- Confirm load balancer IP or hostname
- Identify backend servers
- Confirm service port

### Commands

```bash
curl -I http://load-balancer
curl http://backend-server
netstat -tulnp
```

### Validation

1. Confirm backend servers responding
2. Confirm load balancer distributing traffic
3. Monitor application response time

## Load Balancers

Load balancers distribute incoming traffic across a pool of backend servers. In enterprise infrastructure they front application servers, storage management APIs, and cloud endpoints.

### Check VIP Availability

```bash
# Test the VIP endpoint
curl -vk https://<vip_fqdn>/
curl -vk http://<vip_fqdn>:<port>/

# Test TCP port reachability
nc -zv <vip_ip> <port>

# Verify DNS resolves to the VIP
dig <vip_fqdn>
```

### Check Pool Member Health

On F5 BIG-IP:
```bash
tmsh show ltm node
tmsh show ltm pool
tmsh show ltm pool <pool_name> members
```

On HAProxy:
```bash
echo "show stat" | socat stdio /var/run/haproxy.sock | cut -d ',' -f1,2,18 | column -t -s ','
```

### Pool Member Status Values (F5)

| Status | Meaning |
|---|---|
| up | Available and passing health checks |
| down | Failed health check |
| forced-offline | Administratively removed |
| unknown | No health monitor configured |

### SSL Certificate Check

```bash
openssl s_client -connect <vip_fqdn>:443 </dev/null 2>&1 | grep -E "subject|Verify|expire"
echo | openssl s_client -connect <vip_fqdn>:443 2>/dev/null | openssl x509 -noout -dates
```

### Health Monitor Validation

Backend members fail health checks if:
- The service port is not responding
- The health check path returns a non-2xx response
- The member's firewall blocks the health check source IP

```bash
# Test the health check manually from the LB server or another host
curl -o /dev/null -s -w "%{http_code}" http://<member_ip>:<port>/health
```

### Persistence

If sessions are being dropped inconsistently, check persistence profile:
- Cookie persistence — browser-based stickiness
- Source IP — same source always goes to same member
- SSL session ID — for HTTPS without cookie insertion

### Common Issues

| Issue | Check | Action |
|---|---|---|
| VIP unreachable | Firewall, routing | Check path from client to VIP |
| All members down | Health monitor | Check monitor config; test check manually |
| One member down | Backend service | Restart service on failed member |
| Session drops | Persistence | Enable or fix persistence profile |
| SSL error | Certificate expiry | Renew and replace certificate |
