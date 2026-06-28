---
tags:
  - networking
---
# Networking — Load Balancer & Services

<div class="kb-summary">
Network services reference for load balancer VIP management, pool health monitoring, and IPAM. For DNS and DHCP protocol coverage, see <a href="../protocols/dns/">Protocols → DNS</a> and <a href="../protocols/dhcp/">Protocols → DHCP</a>.
</div>

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
