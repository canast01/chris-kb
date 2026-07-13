---
tags:
  - networking
description: "Network services reference for load balancer VIP management, pool health monitoring, and IPAM. For DNS and DHCP protocol coverage, see Protocols → DNS and..."
---
# Networking — Load Balancer & Services

<div class="kb-summary">
Network services reference for load balancer VIP management, pool health monitoring, and IPAM. For DNS and DHCP protocol coverage, see <a href="../protocols/dns/">Protocols → DNS</a> and <a href="../protocols/dhcp/">Protocols → DHCP</a>.
</div>

```d2
direction: down

test_the_vip_endpoint: "Test the VIP Endpoint" {shape: rectangle}
f5_bigip_pool_status: "F5 BIG-IP Pool Status" {shape: rectangle}
haproxy_pool_status: "HAProxy Pool Status" {shape: rectangle}
tls_certificate_on_vip: "TLS Certificate on VIP" {shape: rectangle}
test_pool_member_health_check: "Test Pool Member Health Check" {shape: rectangle}
lb_status_at_a_glance: "LB Status at a Glance" {shape: rectangle}

test_the_vip_endpoint -> f5_bigip_pool_status: uses
f5_bigip_pool_status -> haproxy_pool_status: uses
haproxy_pool_status -> tls_certificate_on_vip: uses
tls_certificate_on_vip -> test_pool_member_health_check: uses
test_pool_member_health_check -> lb_status_at_a_glance: uses
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


```text title="Expected output"
* Trying 10.45.23.15...
* TCP_NODELAY set
* Connected to lb-prod-vip.internal (10.45.23.15) port 443 (#0)
* ALPN, offering h2
* successfully set certificate verify locations
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* Server certificate:
*  subject: CN=lb-prod-vip.internal; O=Internal CA
*  start date: Jan 15 12:34:56 2024 GMT
*  expire date: Jan 15 12:34:56 2025 GMT
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
> GET / HTTP/1.1
< HTTP/1.1 200 OK
< Content-Type: text/html
Connection #0 to host lb-prod-vip.internal left intact

Ncat: Version 7.80 ( https://nmap.org/ncat )
Ncat: Connected to 10.45.23.15:8080.
Ncat: 0 bytes sent, 0 bytes received in 0.01 seconds.

; <<>> DiG 9.16.1-Ubuntu <<>> lb-prod-vip.internal
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 54321
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

;lb-prod-vip.internal.		IN	A

lb-prod-vip.internal.	300	IN	A	10.45.23.15

;; Query time: 2 msec
;; SERVER: 127.0.0.53#53(127.0.0.53)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to <vip_fqdn> port 443: Connection refused`** — Verify the load balancer service is running with `systemctl status` and check firewall rules allow inbound traffic on port 443.
    **`Ncat: Connection refused.`** — Confirm the backend pool members are healthy and the VIP listener is configured for the specified port using your load balancer admin interface.
    **`dig: couldn't get address for '<vip_fqdn>': not known`** — Ensure DNS records are created for the VIP FQDN and verify your resolver is configured to query the correct nameserver with `cat /etc/resolv.conf`.
## F5 BIG-IP Pool Status

```bash
tmsh show ltm node
tmsh show ltm pool
tmsh show ltm pool <pool_name> members
```


```text title="Expected output"
Ltm::Node: node1
  Ltm::Node: node2
  Ltm::Node: node3
  Ltm::Node: node4

Ltm::Pool: pool_web_prod
  Ltm::Pool: pool_api_backend
  Ltm::Pool: pool_db_replica
  Ltm::Pool: pool_cache_layer

Ltm::Pool Member: 10.45.12.8:8080
  State: up
  Session Status: enabled
  Ltm::Pool Member: 10.45.12.9:8080
  State: up
  Session Status: enabled
  Ltm::Pool Member: 10.45.12.10:8080
  State: down
  Session Status: enabled
```

!!! warning "Common errors"
    **`tmsh: command not found`** — Ensure you are logged into the BIG-IP system directly or use the F5 iControl REST API instead.
    **`Pool <pool_name> not found`** — Verify the pool name exists by running `tmsh show ltm pool` first and use the exact pool name from the output.
## HAProxy Pool Status

```bash
echo "show stat" | socat stdio /var/run/haproxy.sock | cut -d ',' -f1,2,18 | column -t -s ','
```


```text title="Expected output"
# pxname,svname,status
stats,FRONTEND,OPEN
stats,BACKEND,UP
web-api,web-01,UP
web-api,web-02,UP
web-api,web-03,DOWN
web-api,BACKEND,UP
db-pool,db-primary,UP
db-pool,db-secondary,UP
db-pool,BACKEND,UP
```

!!! warning "Common errors"
    **`socat: E_NOACCES error in function openfile() with address "/var/run/haproxy.sock"`** — Run the command with sudo or ensure your user is in the haproxy group.
    **`socat: E_NOENT error in function openfile() with address "/var/run/haproxy.sock"`** — Verify HAProxy is running with `systemctl status haproxy` and check the socket path in your HAProxy configuration.
## TLS Certificate on VIP

```bash
openssl s_client -connect <vip_fqdn>:443 </dev/null 2>&1 | grep -E "subject|Verify|expire"
echo | openssl s_client -connect <vip_fqdn>:443 2>/dev/null | openssl x509 -noout -dates
```


```text title="Expected output"
subject=CN = *.example.com, O = Example Corp, C = US
Verify return code: 0 (ok)
notBefore=Jan 15 10:23:45 2023 GMT
notAfter=Jan 15 10:23:45 2025 GMT
```

!!! warning "Common errors"
    **`verify error:num=20:unable to get local issuer certificate`** — Add the intermediate CA certificate to your system's trusted store or use `openssl s_client -connect <vip_fqdn>:443 -CAfile /path/to/ca-bundle.crt`.
    **`connect: Connection refused`** — Verify the VIP is reachable and the service is listening on port 443 with `nc -zv <vip_fqdn> 443`.
    **`Verify return code: 1 (unable to get local issuer certificate)`** — Install the missing CA certificate chain or use `-showcerts` flag to inspect the full certificate chain being presented.
## Test Pool Member Health Check

```bash
# Test the health check manually from the LB server or another host
curl -o /dev/null -s -w "%{http_code}" http://<member_ip>:<port>/health
```


```text title="Expected output"
200
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to 10.45.23.18 port 8080: Connection refused`** — Verify the service is running on the target member with `systemctl status <service>` and check that the port is correct.
    **`curl: (28) Operation timeout. The timeout was reached`** — Increase the curl timeout with `-m 10` flag or verify network connectivity and firewall rules allow traffic between the LB and member servers.
    **`000`** — The service returned an invalid HTTP response; check service logs with `journalctl -u <service> -n 50` to identify application errors.
## LB Status at a Glance

```bash
curl -I http://load-balancer
curl http://backend-server
netstat -tulnp
```


```text title="Expected output"
HTTP/1.1 200 OK
Server: nginx/1.24.0
Date: Thu, 15 Feb 2024 10:32:45 GMT
Content-Type: text/html; charset=UTF-8
Content-Length: 4521
Connection: keep-alive

<!DOCTYPE html>
<html>
<head><title>Backend Service</title></head>
<body><h1>Service Status: OK</h1></body>
</html>

Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      892/sshd
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2341/nginx
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      2341/nginx
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      1205/mysqld
tcp6       0      0 :::22                   :::*                    LISTEN      892/sshd
...
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to load-balancer port 80: Connection refused`** — Verify the load balancer service is running with `systemctl status nginx` and check firewall rules with `sudo ufw status`.
    **`curl: (6) Could not resolve host: backend-server`** — Ensure DNS resolution is working by checking `/etc/hosts` or running `nslookup backend-server`, and verify the hostname is correct.
    **`netstat: command not found`** — Install net-tools with `sudo apt install net-tools` or use the modern alternative `ss -tulnp` instead.