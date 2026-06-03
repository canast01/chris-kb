# Networking — Network Services

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```

```text
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
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```
```bash
# Forward: name → IP
dig <hostname>

# Reverse: IP → name (PTR)
dig -x <ip>
nslookup <ip>
```
```cmd
ipconfig /flushdns
```
```bash
resolvectl flush-caches
# or
systemctl restart systemd-resolved
```
```bash
curl -I http://load-balancer
curl http://backend-server
netstat -tulnp
```
```bash
# Test the VIP endpoint
curl -vk https://<vip_fqdn>/
curl -vk http://<vip_fqdn>:<port>/

# Test TCP port reachability
nc -zv <vip_ip> <port>

# Verify DNS resolves to the VIP
dig <vip_fqdn>
```
```bash
tmsh show ltm node
tmsh show ltm pool
tmsh show ltm pool <pool_name> members
```
```bash
echo "show stat" | socat stdio /var/run/haproxy.sock | cut -d ',' -f1,2,18 | column -t -s ','
```
```bash
openssl s_client -connect <vip_fqdn>:443 </dev/null 2>&1 | grep -E "subject|Verify|expire"
echo | openssl s_client -connect <vip_fqdn>:443 2>/dev/null | openssl x509 -noout -dates
```
```bash
# Test the health check manually from the LB server or another host
curl -o /dev/null -s -w "%{http_code}" http://<member_ip>:<port>/health
```
