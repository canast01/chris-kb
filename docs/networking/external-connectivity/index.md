---
tags:
  - networking
---
# External Connectivity

<div class="kb-summary">
Covers infrastructure paths for internet egress, WAN/MPLS, cloud direct connections, and partner API connectivity.
</div>

---

```d2
direction: down

onpremises_to_cloud_network_topology: "On-Premises to Cloud — Network Topology" {shape: rectangle}
connectivity_paths: "Connectivity Paths" {shape: rectangle}
health_check_commands: "Health Check Commands" {shape: rectangle}
firewall_rule_verification: "Firewall Rule Verification" {shape: rectangle}
troubleshooting: "Troubleshooting" {shape: rectangle}

onpremises_to_cloud_network_topology -> connectivity_paths: uses
connectivity_paths -> health_check_commands: uses
health_check_commands -> firewall_rule_verification: uses
firewall_rule_verification -> troubleshooting: uses
```

## On-Premises to Cloud — Network Topology

How traffic flows from an ESXi host through your core network out to AWS or Azure over a VPN tunnel.

---

## Connectivity Paths

| Path Type | Description | Typical Components |
|---|---|---|
| **Internet egress (NAT/proxy)** | Outbound traffic from servers or VMs to the public internet, routed via NAT gateway or explicit proxy | NAT gateway, forward proxy (Squid/Zscaler), firewall outbound policy |
| **WAN / MPLS** | Private layer-3 connectivity between data centres or branch offices without traversing the public internet | MPLS PE router, CE router, BGP or OSPF peering, QoS policy |
| **Cloud Direct Connect / ExpressRoute** | Dedicated private circuit from on-premises to AWS (Direct Connect) or Azure (ExpressRoute) — bypasses the public internet | Direct Connect hosted connection or dedicated connection, Virtual Private Gateway or Transit Gateway; Azure: ExpressRoute circuit, virtual network gateway |
| **Partner API connections** | Outbound HTTPS calls from internal systems to third-party APIs (payment processors, SaaS platforms, suppliers) | Application server, proxy or NAT, firewall allow rule for destination CIDR/FQDN, partner-provided credentials |

---

## Health Check Commands

### Outbound internet reachability

```bash
# HTTP/HTTPS reachability and response code
curl -o /dev/null -s -w "%{http_code}  %{time_total}s\n" https://api.example.com/health

# TLS certificate expiry check (days remaining)
echo | openssl s_client -connect api.example.com:443 -servername api.example.com 2>/dev/null \
  | openssl x509 -noout -dates

# MTU path discovery — detect PMTUD black holes (Linux)
ping -M do -s 1400 -c 4 8.8.8.8

# Windows equivalent
ping -f -l 1400 8.8.8.8
```


```text title="Expected output"
200  0.342s
notBefore=Jan 15 10:22:33 2024 GMT
notAfter=Jan 14 10:22:33 2025 GMT
PING 8.8.8.8 (8.8.8.8) 1400(1428) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=12.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=12.1 ms
64 bytes from 8.8.8.8: icmp_seq=4 ttl=119 time=11.9 ms

--- 8.8.8.8 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 11.8/12.05/12.4/0.24 ms
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to api.example.com port 443: Connection refused`** — Verify the API endpoint is reachable and listening; check firewall rules and DNS resolution with `ndig api.example.com`.
    **`ping: sendmsg: Operation not permitted`** — The `-M do` flag requires root or CAP_NET_RAW capability; run with `sudo` or adjust system capabilities.
    **`notAfter=Jan 14 10:22:33 2024 GMT` (certificate expired)`** — Renew the TLS certificate immediately using your certificate provider or `certbot renew` for Let's Encrypt certificates.
### Route and latency

```bash
# Traceroute to confirm path and hop count (Linux)
traceroute -n api.example.com

# Windows equivalent
tracert -d api.example.com

# Test TCP reachability on a specific port (Windows)
Test-NetConnection -ComputerName api.example.com -Port 443

# Test TCP port reachability (Linux)
nc -zv api.example.com 443
```


```text title="Expected output"
traceroute to api.example.com (203.0.113.42), 30 hops max, 60 byte packets
 1  10.0.0.1 (10.0.0.1)  2.341 ms  2.156 ms  2.089 ms
 2  192.168.1.254 (192.168.1.254)  5.623 ms  5.401 ms  5.512 ms
 3  203.0.113.1 (203.0.113.1)  12.845 ms  12.756 ms  12.934 ms
 4  203.0.113.42 (203.0.113.42)  18.234 ms  18.156 ms  18.401 ms

Tracing route to api.example.com [203.0.113.42]
over a maximum of 30 hops:
  1    <1 ms    <1 ms    <1 ms  10.0.0.1
  2     5 ms     4 ms     6 ms  192.168.1.254
  3    12 ms    13 ms    12 ms  203.0.113.1
  4    18 ms    17 ms    19 ms  203.0.113.42

ComputerName     : api.example.com
RemoteAddress    : 203.0.113.42
RemotePort       : 443
InterfaceAlias   : Ethernet
SourceAddress    : 10.0.0.50
TcpTestSucceeded : True

Connection to api.example.com 443 port [tcp/https] succeeded!
```

!!! warning "Common errors"
    **`traceroute: command not found`** — Install traceroute using `apt-get install traceroute` on Debian/Ubuntu or `yum install traceroute` on RHEL/CentOS.
    **`nc: command not found`** — Install netcat using `apt-get install netcat-openbsd` or verify the correct package name for your distribution.
    **`Test-NetConnection : The term 'Test-NetConnection' is not recognized`** — Ensure you are running PowerShell 4.0 or later on Windows; use `$PSVersionTable.PSVersion` to verify.
### DNS resolution

```bash
# Confirm DNS resolves to expected addresses
dig +short api.example.com

# Test with a specific resolver (check split-DNS behaviour)
dig @10.0.0.53 api.example.com

# Windows
Resolve-DnsName api.example.com
```


```text title="Expected output"
93.184.216.34
93.184.216.35

93.184.216.34

Name                                           Type   TTL   Section    IPAddress
----                                           ----   ---   -------    ---------
api.example.com                                A      300   Answer     93.184.216.34
api.example.com                                A      300   Answer     93.184.216.35
```

!!! warning "Common errors"
    **`dig: couldn't get address for '10.0.0.53': not known`** — Verify the resolver IP is reachable and correct with `ping 10.0.0.53` before running dig.
    **`SERVFAIL`** — Check that the DNS resolver at 10.0.0.53 has zone authority or conditional forwarding rules configured for api.example.com.
### Cloud Direct Connect / ExpressRoute

```bash
# AWS: verify BGP session state on a virtual interface
aws directconnect describe-virtual-interfaces --query 'virtualInterfaces[*].[virtualInterfaceId,bgpPeers[*].bgpStatus]'

# Azure: verify ExpressRoute circuit peering state
az network express-route show --name <circuit-name> --resource-group <rg> --query 'serviceProviderProvisioningState'
```


```text title="Expected output"
[
    [
        "vif-0a1b2c3d4e5f6g7h8",
        [
            "Available"
        ]
    ],
    [
        "vif-9i8j7k6l5m4n3o2p1q",
        [
            "Available",
            "Available"
        ]
    ],
    [
        "vif-2r3s4t5u6v7w8x9y0z",
        [
            "Down"
        ]
    ]
]
"Provisioned"
```

!!! warning "Common errors"
    **`An error occurred (InvalidParameterValue) when calling the DescribeVirtualInterfaces operation: Invalid virtual interface ID`** — Verify the virtual interface exists in your AWS account and region using `aws directconnect describe-virtual-interfaces` without filters.
    **`The following arguments are required: --name, --resource-group`** — Replace `<circuit-name>` and `<rg>` with actual ExpressRoute circuit name and resource group name, or use `az network express-route list` to find valid values.
---

## Firewall Rule Verification

| Platform | Command / Method | What to Confirm |
|---|---|---|
| **Cisco ASA** | `show access-list <acl-name>` | Rule exists, hit count is non-zero (confirms traffic is matching). |
| **Cisco ASA** | `packet-tracer input <interface> tcp <src-ip> 1024 <dst-ip> 443 detail` | Simulates a packet — confirm result is `ALLOW`. |
| **Palo Alto (PAN-OS)** | `show running security-policy \| match <destination>` | Confirm the expected rule name appears. |
| **Palo Alto** | Traffic log query: source, destination, port, action=allow | Verify recent hits. Absence of hits when traffic is expected points to a routing or DNS issue. |
| **Windows Firewall** | `Get-NetFirewallRule -DisplayName "*<name>*" \| Get-NetFirewallPortFilter` | Confirm rule is enabled and port/protocol match expected values. |
| **iptables (Linux)** | `iptables -L OUTPUT -v -n \| grep <destination>` | Confirm the rule is present and packet/byte counts are incrementing. |

---

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| DNS resolution fails for external hostname | `dig` returns SERVFAIL or NXDOMAIN | Confirm the resolver can reach upstream DNS. For split-DNS environments, check whether the FQDN should be resolved internally or externally. |
| TCP connection times out (no RST) | `traceroute` loses packets at a firewall hop | A firewall is silently dropping the traffic. Identify the hop and verify the outbound rule allows the destination port. |
| TCP connection refused (RST received) | `nc -zv` reports `Connection refused` | The destination host is reachable but the service is not listening on that port, or a host-based firewall is sending RST. |
| TLS handshake fails | `openssl s_client` shows `handshake failure` | Check TLS version compatibility. Some older servers reject TLS 1.3. Try forcing TLS 1.2: `openssl s_client -tls1_2 -connect host:443`. |
| Proxy authentication error | Application logs show `407 Proxy Authentication Required` | Confirm proxy credentials are current. Check whether the application is configured to use the proxy (`http_proxy`/`HTTPS_PROXY` env vars or system proxy settings). |
| Intermittent packet loss on WAN/MPLS | `ping` shows variable loss, `traceroute` shows jitter at WAN hops | Engage the WAN carrier. Collect `mtr` output over 60 seconds to share with the provider: `mtr -r -c 60 <remote-ip>`. |
| Direct Connect / ExpressRoute BGP down | AWS/Azure portal shows circuit state as `Not provisioned` or BGP peer as `Down` | Confirm physical layer is up with the carrier. Verify BGP peer config (ASN, auth key) on the CE router matches the cloud-side configuration. |
| Partner API returns 403 Forbidden | Authentication succeeds but requests are rejected | Confirm the source egress IP is on the partner's allowlist. Check whether the API key has expired or the required scope is missing. |
