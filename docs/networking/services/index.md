# Networking — Load Balancer & Services

<div class="kb-summary">
Network services reference for load balancer VIP management, pool health monitoring, and IPAM. For DNS and DHCP protocol coverage, see <a href="../protocols/dns/">Protocols → DNS</a> and <a href="../protocols/dhcp/">Protocols → DHCP</a>.
</div>

```text
┌──────────────────────────────── Networking — Load Balancer & Services ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Load balancer: health checks must match app check; monitor pool member state daily     │   │
│   │        VIP is the client-facing address; backend pool members serve the actual traffic        │   │
│   │        SNAT ensures return traffic flows back through the LB for stateful session tracking    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Load Balancer                 │  │                   IPAM                      │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           VIP: virtual IP for pool          │  │          Subnet allocation tracking         │    │
│   │            Pool: backend servers            │  │          DHCP scope management              │    │
│   │            Health check: HTTP/TCP           │  │          IP address inventory               │    │
│   │           SNAT: return path via LB          │  │          DNS integration via IPAM           │    │
│   │          SSL offload: TLS termination       │  │          See Protocols for DNS/DHCP         │    │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VIP          = Virtual IP; load balancer frontend; clients connect here, not to backend            │
│    SNAT         = Source NAT on load balancer; ensures response traffic returns via LB                │
│    Pool member  = Backend server registered in the LB pool; receives forwarded traffic                │
│    Health check = Probe LB sends to each pool member; removes unhealthy members from rotation         │
│    SSL offload  = LB terminates TLS; backend receives plain HTTP; reduces cert management scope       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Test the VIP Endpoint

```bash
# Test the VIP endpoint
curl -vk https://<vip_fqdn>/
curl -vk http://<vip_fqdn>:<port>/

# Test TCP port reachability
nc -zv <vip_ip> <port>

# Verify DNS resolves to the VIP
dig <vip_fqdn>
```

## F5 BIG-IP Pool Status

```bash
tmsh show ltm node
tmsh show ltm pool
tmsh show ltm pool <pool_name> members
```

## HAProxy Pool Status

```bash
echo "show stat" | socat stdio /var/run/haproxy.sock | cut -d ',' -f1,2,18 | column -t -s ','
```

## TLS Certificate on VIP

```bash
openssl s_client -connect <vip_fqdn>:443 </dev/null 2>&1 | grep -E "subject|Verify|expire"
echo | openssl s_client -connect <vip_fqdn>:443 2>/dev/null | openssl x509 -noout -dates
```

## Test Pool Member Health Check

```bash
# Test the health check manually from the LB server or another host
curl -o /dev/null -s -w "%{http_code}" http://<member_ip>:<port>/health
```

## LB Status at a Glance

```bash
curl -I http://load-balancer
curl http://backend-server
netstat -tulnp
```
