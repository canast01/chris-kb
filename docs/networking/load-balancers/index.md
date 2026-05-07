# Load Balancers

Load balancers distribute incoming traffic across a pool of backend servers. In enterprise infrastructure they front application servers, storage management APIs, and cloud endpoints.
## Check VIP Availability

```bash
# Test the VIP endpoint
curl -vk https://<vip_fqdn>/
curl -vk http://<vip_fqdn>:<port>/

# Test TCP port reachability
nc -zv <vip_ip> <port>

# Verify DNS resolves to the VIP
dig <vip_fqdn>
```

## Check Pool Member Health

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

## Pool Member Status Values (F5)

| Status | Meaning |
|---|---|
| up | Available and passing health checks |
| down | Failed health check |
| forced-offline | Administratively removed |
| unknown | No health monitor configured |

## SSL Certificate Check

```bash
openssl s_client -connect <vip_fqdn>:443 </dev/null 2>&1 | grep -E "subject|Verify|expire"
echo | openssl s_client -connect <vip_fqdn>:443 2>/dev/null | openssl x509 -noout -dates
```

## Health Monitor Validation

Backend members fail health checks if:
- The service port is not responding
- The health check path returns a non-2xx response
- The member's firewall blocks the health check source IP

```bash
# Test the health check manually from the LB server or another host
curl -o /dev/null -s -w "%{http_code}" http://<member_ip>:<port>/health
```

## Persistence

If sessions are being dropped inconsistently, check persistence profile:
- Cookie persistence — browser-based stickiness
- Source IP — same source always goes to same member
- SSL session ID — for HTTPS without cookie insertion

## Common Issues

| Issue | Check | Action |
|---|---|---|
| VIP unreachable | Firewall, routing | Check path from client to VIP |
| All members down | Health monitor | Check monitor config; test check manually |
| One member down | Backend service | Restart service on failed member |
| Session drops | Persistence | Enable or fix persistence profile |
| SSL error | Certificate expiry | Renew and replace certificate |
