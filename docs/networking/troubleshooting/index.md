---
tags:
  - networking
  - troubleshooting
search:
  boost: 1.5
description: "Networking troubleshooting — Layer 1-3 diagnostics, DNS/DHCP failures, routing issues, VLAN misconfigurations, and connectivity tools."
---
# Networking — Troubleshooting

<div class="kb-summary">
Networking troubleshooting — Layer 1-3 diagnostics, DNS/DHCP failures, routing issues, VLAN misconfigurations, and connectivity tools.
</div>

```bash
nslookup <hostname>
dig <hostname>
dig <hostname> @<dns_server_ip>    # query a specific server directly
```


```text title="Expected output"
Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	api.example.com
Address: 192.0.2.45
Address: 192.0.2.46

; <<>> DiG 9.16.1-Ubuntu <<>> api.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 52847
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:
;api.example.com.			IN	A

;; ANSWER SECTION:
api.example.com.		300	IN	A	192.0.2.45
api.example.com.		300	IN	A	192.0.2.46

;; Query time: 45 msec
;; SERVER: 8.8.8.8#53(8.8.8.8)
;; WHEN: Mon Jan 15 14:32:19 UTC 2024
;; MSG SIZE  rcvd: 89

; <<>> DiG 9.16.1-Ubuntu <<>> api.example.com @203.0.113.10
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 18392
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 0

;; QUESTION SECTION:
;api.example.com.			IN	A

;; ANSWER SECTION:
api.example.com.		3600	IN	A	192.0.2.45

;; Query time: 12 msec
;; SERVER: 203.0.113.10#53(203.0.113.10)
;; WHEN: Mon Jan 15 14:32:20 UTC 2024
;; MSG SIZE  rcvd: 67
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nslookup: can't resolve '<hostname>': Non-existent domain` | Verify the hostname spelling and that DNS resolution is working by testing with a known domain like google.com. |
    | `dig: couldn't get address for '<dns_server_ip>': not known` | Ensure the DNS server IP address is correct and reachable; verify connectivity with `ping <dns_server_ip>`. |
    | `connection timed out; no servers could be reached` | Check that your network connectivity is active and the DNS server is accessible; try querying a public DNS server like 8.8.8.8 to isolate the issue. |
```bash
ping <dns_server_ip>
nslookup <hostname> <dns_server_ip>
```

```text title="Expected output"
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=12.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=11.8 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=12.1 ms
^C
--- 8.8.8.8 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
rtt min/avg/max/stddev = 11.8/12.1/12.4/0.2 ms

Server:		8.8.8.8
Address:	8.8.8.8#53

Non-authoritative answer:
Name:	api.example.com
Address: 192.168.1.45
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: unknown host <dns_server_ip>` | Replace `<dns_server_ip>` with an actual IP address like `8.8.8.8` or verify the DNS server is reachable. |
    | `** server can't find <hostname>: NXDOMAIN` | Verify the hostname is correct and exists in the DNS server's zone; check with `nslookup <hostname>` against a known working DNS server. |
    | `connection timed out; no servers could be reached` | Confirm the DNS server IP is correct and accessible on port 53, and check firewall rules allow DNS traffic. |
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

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Failed to flush caches: Access denied` | Run the command with `sudo` since cache flushing requires root privileges. |
    | `Unit systemd-resolved.service not found.` | Ensure systemd-resolved is installed and enabled with `systemctl enable systemd-resolved` on your distribution. |
```bash
# Linux — check interface link state
ip link show
ethtool <interface>    # speed, duplex, link detected
```

```text title="Expected output"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group 0
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP mode DEFAULT group 0
    link/ether 08:00:27:a4:2b:1c brd ff:ff:ff:ff:ff:ff
3: eth1: <BROADCAST,MULTICAST> mtu 1500 qdisc mq state DOWN mode DEFAULT group 0
    link/ether 08:00:27:a4:2b:1d brd ff:ff:ff:ff:ff:ff

Settings for eth0:
	Supported ports: [ TP ]
	Supported link modes:   1000baseT/Full
	Speed: 1000Mb/s
	Duplex: Full
	Link detected: yes
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ethtool: command not found` | Install ethtool with `sudo apt install ethtool` (Debian/Ubuntu) or `sudo yum install ethtool` (RHEL/CentOS). |
    | `Cannot get device settings: No such device` | Verify the interface name is correct by running `ip link show` first; common typos include `eth0` vs `en0` or `ens0`. |
```bash
# Check ARP table (confirm MAC resolved)
arp -a
ip neigh show

# Check interface is in correct VLAN
# On switch: show interface status, show vlan brief
```

```text title="Expected output"
? (192.168.1.1) at 00:1a:2b:3c:4d:5e [ether] on eth0
? (192.168.1.254) at 08:9a:bc:de:f0:12 [ether] on eth0
? (10.0.0.1) at 34:56:78:9a:bc:de [ether] on eth1
? (10.0.0.50) at <incomplete> on eth1

INCOMPLETE ENTRY (10.0.0.100) on eth1
REACHABLE (192.168.1.5) lladdr 5c:7d:8e:9f:0a:1b dev eth0
REACHABLE (192.168.1.10) lladdr 6e:8f:9a:0b:1c:2d dev eth0
STALE (10.0.0.200) lladdr 7f:9a:0b:1c:2d:3e dev eth1
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `INCOMPLETE ENTRY` | Run `ping <IP>` to trigger ARP resolution, then check `arp -a` again. |
    | `No ARP entries found` | Verify the interface is up with `ip link show` and the network is reachable with `ping`. |
```bash
# Confirm IP configuration
ip addr show

# Confirm route exists
ip route show
ip route get <destination_ip>

# Default gateway
ip route show default
ping <gateway_ip>
```

```text title="Expected output"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
    inet6 ::1/128 scope host
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 08:00:27:a4:2b:19 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.45/24 brd 192.168.1.255 scope global dynamic eth0
    inet6 fe80::a00:27ff:fea4:2b19/64 scope link

default via 192.168.1.1 dev eth0 proto dhcp metric 100
192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.45 metric 100

192.168.1.50 via 192.168.1.1 dev eth0 src 192.168.1.45 uid 0
    cache

default via 192.168.1.1 dev eth0 proto dhcp metric 100

PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=1.89 ms
64 bytes from 192.168.1.1: icmp_seq=3 ttl=64 time=2.12 ms
--- 192.168.1.1 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2004ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `RTNETLINK answers: No such file or directory` | Ensure the network interface exists with `ip link show` and verify the interface name is correct. |
    | `ping: unknown host <gateway_ip>` | Replace `<gateway_ip>` with an actual IP address (e.g., `192.168.1.1`) instead of the placeholder variable. |
    | `Network is unreachable` | Verify the default gateway is configured with `ip route show default` and that the interface is UP with `ip link show`. |
```bash
# Test specific TCP port
nc -zv <host> <port>
telnet <host> <port>
curl -v http://<host>:<port>/

# Check local firewall
iptables -L -n | grep <port>
firewall-cmd --list-all
```

```text title="Expected output"
nc -zv example.com 443
Connection to example.com 443 port [tcp/https] succeeded!

telnet example.com 80
Trying 192.0.2.45...
Connected to example.com.
Escape character is '^]'.

curl -v http://example.com:8080/
*   Trying 192.0.2.45:8080...
* Connected to example.com (192.0.2.45) port 8080 (#0)
> GET / HTTP/1.1
> Host: example.com:8080
> User-Agent: curl/7.68.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/html
< Content-Length: 1247

iptables -L -n | grep 8080
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            tcp dpt:8080

firewall-cmd --list-all
public (active)
  target: default
  icmp-block-inversion: no
  interfaces: eth0
  sources:
  services: ssh http https
  ports: 8080/tcp 9000/tcp
  protocols:
  forward: yes
  masquerade: no
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `nc: getaddrinfo: Name or service not known` | Verify the hostname is correct and resolvable with `nslookup <host>` or `dig <host>`. |
    | `Connection refused` | Confirm the service is running on the target host with `netstat -tlnp | grep <port>` or `ss -tlnp | grep <port>`. |
    | `firewall-cmd: command not found` | Use `iptables -L -n` instead if firewalld is not installed, or install firewalld with `dnf install firewalld` on RHEL/Fedora systems. |
```bash
traceroute <destination>    # Linux/Mac
tracert <destination>       # Windows
mtr <destination>           # continuous path trace
```

```text title="Expected output"
traceroute to example.com (93.184.216.34), 30 hops max, 60 byte packets
 1  gateway.local (192.168.1.1)  2.341 ms  2.156 ms  2.089 ms
 2  isp-router-01.net (10.0.0.1)  8.742 ms  8.651 ms  8.923 ms
 3  core-backbone-12.isp.net (203.45.67.89)  15.234 ms  15.412 ms  15.089 ms
 4  peer-exchange-04.net (198.51.100.45)  22.567 ms  22.341 ms  22.678 ms
 5  example.com (93.184.216.34)  28.123 ms  27.945 ms  28.234 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `traceroute: command not found` | Install traceroute with `apt-get install traceroute` (Linux) or `brew install traceroute` (macOS). |
    | `traceroute: sendto: Operation not permitted` | Run the command with `sudo` to obtain the necessary raw socket permissions. |
    | `traceroute: getaddrinfo: Name or service not known` | Verify the destination hostname or IP address is correct and reachable from your network. |
```bash
# ICMP ping
ping -c 4 <host>

# MTU test (verify no fragmentation)
ping -M do -s 1472 <host>    # Linux (1500 MTU = 1472 payload + 28 headers)
ping -f -l 1472 <host>       # Windows

# DNS and then connect
curl -v https://<fqdn>/
```
```powershell
Test-NetConnection -ComputerName <host> -Port <port>
Test-NetConnection <host>    # ICMP test
Resolve-DnsName <host>
```
```bash
# Extended ping to observe loss pattern
ping -c 100 <destination>

# Continuous path trace with loss stats per hop
mtr <destination>
mtr --report --report-cycles 100 <destination>
```

```text title="Expected output"
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=119 time=12.4 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=119 time=11.9 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=119 time=12.1 ms
...
64 bytes from 8.8.8.8: icmp_seq=100 ttl=119 time=12.3 ms

--- 8.8.8.8 statistics ---
100 packets transmitted, 100 received, 0% packet loss, time 99234ms
rtt min/avg/max/stddev = 11.8/12.1/13.7/0.4 ms

                                      My traceroute  [v0.93]
router.local (192.168.1.1)                                   Wed Jan 15 14:32:10 2025
Host                                           Loss%   Snt   Last   Avg  Best  Wrst StDev
 1. router.local                                0.0%   100    1.2   1.3   1.1   2.1   0.2
 2. isp-gw.example.com                          0.0%   100    8.4   8.6   8.2   9.8   0.3
 3. core-router-02.isp.net                      0.0%   100   11.2  11.5  11.0  12.9   0.4
 4. 8.8.8.8                                     0.0%   100   12.1  12.3  11.8  13.7   0.4
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: unknown host <destination>` | Replace `<destination>` with an actual hostname or IP address (e.g., `8.8.8.8` or `google.com`). |
    | `mtr: command not found` | Install mtr using your package manager (`apt install mtr` on Debian/Ubuntu or `brew install mtr` on macOS). |
    | `ICMP administratively prohibited` | Verify the destination allows ICMP traffic; some firewalls block ping requests, so check network policies or use `mtr --tcp` as an alternative. |
```bash
# Linux
ethtool -S <interface> | grep -i error
ip -s link show <interface>

# Show interface errors
netstat -i

# Network interface stats
cat /proc/net/dev
```

```text title="Expected output"
# ethtool -S eth0 | grep -i error
     rx_errors: 12
     tx_errors: 3
     rx_crc_errors: 2
     tx_carrier_errors: 1

# ip -s link show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:a4:2b:f9 brd ff:ff:ff:ff:ff:ff
    RX: bytes  packets  errors  dropped overrun mcast
    1847293847 2341029 12      5       0       0
    TX: bytes  packets  errors  dropped carrier collsns
    923847102  1829384 3       2       1       0

# netstat -i
Kernel Interface table
Iface      MTU    RX-OK RX-ERR RX-DRP RX-OVR    TX-OK TX-ERR TX-DRP TX-OVR Flg
eth0      1500  2341029     12      5      0  1829384      3      2      0 BMRU
lo       65536    18402      0      0      0    18402      0      0      0 LRU

# cat /proc/net/dev
Inter-|   Receive                                                |  Transmit
 face |bytes    packets errs drop fifo frame compressed multicast|bytes    packets errs drop fifo colls carrier compressed
  eth0: 1847293847 2341029   12    5    0     2    0          0 923847102 1829384    3    2    0     0       1          0
    lo: 2847102    18402    0    0    0     0    0          0 2847102    18402    0    0    0     0       0          0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ethtool: operation not permitted` | Run the command with `sudo` or as root user. |
    | `Device "eth0" does not exist` | Replace `eth0` with the correct interface name from `ip link show` or `ifconfig`. |
```bash
ethtool <interface>
# Look for: Speed: 1000Mb/s, Duplex: Full
```

```text title="Expected output"
Settings for eth0:
	Supported ports: [ TP ]
	Supported link modes:   10baseT/Half 10baseT/Full
	                        100baseT/Half 100baseT/Full
	                        1000baseT/Full
	Supported pause frame use: No
	Supports auto-negotiation: Yes
	Advertised link modes:  1000baseT/Full
	Advertised pause frame use: No
	Advertised auto-negotiation: Yes
	Speed: 1000Mb/s
	Duplex: Full
	Port: Twisted Pair
	PHYAD: 0
	Transceiver: internal
	Auto-negotiation: on
	MDI-X: on (auto)
	Link detected: yes
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `No such device` | Verify the interface name with `ip link show` and use the correct interface (e.g., eth0, ens3, wlan0). |
    | `Operation not permitted` | Run the command with `sudo` or as root: `sudo ethtool <interface>`. |
    | `Speed: Unknown!` | Check physical cable connection and NIC driver; restart the interface with `sudo ip link set <interface> down && sudo ip link set <interface> up`. |
```bash
show interface <int>
# Look for: duplex full, 1000 Mbps
```

```text title="Expected output"
Interface GigabitEthernet0/0/1
  Hardware is Gigabit Ethernet, address is 00:1a:2b:3c:4d:5e
  Internet address is 192.168.1.42/24
  MTU 1500 bytes, BW 1000000 Kbit/sec
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 1000Mb/s, media type is RJ45
  output flow-control is unsupported, input flow-control is unsupported
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:03, output 00:00:01, output hang never
  Last clearing of "show interface" counters 2d14h
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue: 0/40 (size/max)
  5 minute input rate 2341000 bits/sec, 285 packets/sec
  5 minute output rate 1847000 bits/sec, 156 packets/sec
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid input detected at '^' marker.` | Verify the interface name format matches your device type (e.g., `GigabitEthernet0/0/1`, `eth0`, or `Ethernet1/1`). |
    | `% Incomplete command.` | Provide the full interface identifier after the command (e.g., `show interface GigabitEthernet0/0/1`). |
    | `Interface <int> does not exist.` | Confirm the interface exists on the device using `show ip interface brief` to list all available interfaces. |
```bash
# Linux — show interface TX/RX drops
ip -s link show <interface>
```

```text title="Expected output"
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500
    link/ether 08:00:27:a4:2b:f1 brd ff:ff:ff:ff:ff:ff
    RX: bytes  packets  errors  dropped overrun mcast
        2847361024 1924531 12      8       0       0
    TX: bytes  packets  errors  dropped carrier collsns
        1563892481 1456782 0       3       0       0
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Device "eth0" does not exist.` | Verify the interface name with `ip link show` and substitute the correct interface name. |
    | `RTNETLINK answers: Operation not permitted` | Run the command with `sudo` or as root user. |
```bash
show interface <int> counters    # Cisco
show interface <int>             # look for output drops
```

```text title="Expected output"
Interface GigabitEthernet0/0/1
  MTU 1500 bytes, BW 1000000 Kbit/sec
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 1000Mb/s, media type is RJ45
  output drops: 0
  input drops: 0
  Last input 00:00:03, output 00:00:01
  Last clearing of "show interface" counters 2d14h
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  5 minute input rate 2341000 bits/sec, 156 packets/sec
  5 minute output rate 1872000 bits/sec, 142 packets/sec
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid input detected at '^' marker.` | Verify the interface name matches your platform syntax (e.g., `GigabitEthernet0/0/1` vs `Ethernet0/0`). |
    | `% Incomplete command.` | Add the full interface identifier after the command; `show interface` alone may not work on all Cisco IOS versions. |
```bash
# Check SFP/cable on the switch port
show interface <int> transceiver    # Cisco
# Check Rx power — should be within spec
```

```text title="Expected output"
Interface GigabitEthernet0/0/1 SFP Information:
  Transceiver Type: SFP-10G-SR
  Vendor Name: JDSU
  Vendor OUI: 00:05:1E
  Vendor PN: PLRXPL-VI-S4
  Vendor SN: AD123456789
  Connector Type: LC
  Encoding: 64B66B
  Nominal Bit Rate: 10300 MBps
  Link Length SM: 300m
  Link Length MM: 33m

RX Power: -2.5 dBm (within spec: -6.5 to -0.5 dBm)
TX Power: 3.2 dBm (within spec: -1.0 to 4.0 dBm)
Temperature: 42°C
Voltage: 3.28V
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid input detected at '^' marker.` | Verify the interface name syntax matches your platform (e.g., `GigabitEthernet0/0/1` vs `Ethernet1/1`) and check device documentation. |
    | `% Transceiver information not available.` | Reseat the SFP module or replace it; the transceiver may not be fully inserted or is faulty. |
    | `RX Power: -15.2 dBm (below spec: -6.5 to -0.5 dBm)` | Check cable connections for dirt/damage, verify the remote end is transmitting, and test with a known-good cable. |
```bash
ping -M do -s 8972 <destination>    # iSCSI/NFS MTU test (9000 bytes)
ping -M do -s 1472 <destination>    # standard MTU test
```


```text title="Expected output"
PING 192.168.1.50 (192.168.1.50) 8972(9000) bytes of data.
8980 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=2.34 ms
8980 bytes from 192.168.1.50: icmp_seq=2 ttl=64 time=2.41 ms
8980 bytes from 192.168.1.50: icmp_seq=3 ttl=64 time=2.38 ms
^C
--- 192.168.1.50 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.34/2.38/2.41/0.04 ms

PING 192.168.1.50 (192.168.1.50) 1472(1500) bytes of data.
1480 bytes from 192.168.1.50: icmp_seq=1 ttl=64 time=2.35 ms
1480 bytes from 192.168.1.50: icmp_seq=2 ttl=64 time=2.39 ms
1480 bytes from 192.168.1.50: icmp_seq=3 ttl=64 time=2.37 ms
^C
--- 192.168.1.50 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/stddev = 2.35/2.37/2.39/0.02 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ping: sendto: Message too long` | Reduce packet size or verify the interface MTU supports jumbo frames with `ip link show` and increase with `ip link set dev <interface> mtu 9000`. |
    | `ping: unknown host <destination>` | Verify the hostname or IP address is correct and reachable on the network. |
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="network-connectivity/"><strong>Network Connectivity</strong><span>End-to-end connectivity troubleshooting — L1 through L7 diagnostic procedures and tools.</span></a>
<a class="kb-card" href="dns-resolution/"><strong>DNS Resolution Failures</strong><span>DNS resolution failure diagnosis — resolver, zone, and client-side troubleshooting steps.</span></a>
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
protocol_symptom_index: "Protocol Symptom Index" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> protocol_symptom_index: investigate
protocol_symptom_index -> resolution
```

## Protocol Symptom Index

| Symptom | Protocol | First command |
|---|---|---|
| Name resolution fails | DNS | `dig @<server> A hostname` |
| Kerberos auth fails | DNS / Kerberos | `dcdiag /test:dns`, check NTP sync |
| TLS handshake fails | TLS | `openssl s_client -connect host:443` |
| Certificate not trusted | TLS/PKI | `openssl verify -CAfile ca.crt cert.crt` |
| LDAP bind fails | LDAP | `ldapsearch -H ldap://dc -x -b "dc=corp,dc=local"` |
| FC port not online | Fibre Channel | `fcinfo hba-port`, `show interface fc` |
| iSCSI target unreachable | iSCSI | `iscsiadm -m discovery`, check port 3260 |
| NTP time drift | NTP | `timedatectl status`, `ntpq -pn` |
