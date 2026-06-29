---
tags:
  - networking
  - security
---
# Networking — Network Security

```bash
nc -zv destination-host port
telnet destination-host port
ss -tulnp
```


```text title="Expected output"
nc: connect to destination-host port 22 (tcp) succeeded!
Trying destination-host...
Connected to destination-host.
Escape character is '^]'.
Connection closed by foreign host.
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      1024/sshd           
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      2048/nginx          
tcp        0      0 0.0.0.0:443             0.0.0.0:*               LISTEN      2048/nginx          
tcp        0      0 127.0.0.1:5432          0.0.0.0:*               LISTEN      3072/postgres       
tcp6       0      0 :::22                   :::*                    LISTEN      1024/sshd           
udp        0      0 0.0.0.0:53              0.0.0.0:*               UNCONN      512/systemd-resolve
```

!!! warning "Common errors"
    **`nc: getaddrinfo: Name or service not known`** — Verify the hostname is correct and resolvable with `nslookup destination-host` or use an IP address instead.
    **`telnet: Unable to connect to remote host: Connection refused`** — Confirm the service is running on the target port with `ss -tulnp | grep :port` on the destination host.
    **`Permission denied`** — Run `ss -tulnp` with `sudo` to view process names and PIDs for all listening ports.
```bash
# From a host behind the firewall
ping <destination>
traceroute <destination>
curl -v telnet://<dest>:<port>    # test specific TCP port

# From Linux — test TCP port
nc -zv <host> <port>
```

```text title="Expected output"
PING 10.45.200.15 (10.45.200.15) 56(84) bytes of data.
64 bytes from 10.45.200.15: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 10.45.200.15: icmp_seq=2 ttl=64 time=2.41 ms
64 bytes from 10.45.200.15: icmp_seq=3 ttl=64 time=2.38 ms
--- 10.45.200.15 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.34/2.37/2.41/0.03 ms

traceroute to 10.45.200.15 (10.45.200.15), 30 hops max, 60 byte packets
 1  gateway.internal (10.0.1.1)  1.23 ms  1.19 ms  1.25 ms
 2  core-router-02.dc1 (10.20.0.5)  3.45 ms  3.52 ms  3.48 ms
 3  10.45.200.15 (10.45.200.15)  2.38 ms  2.41 ms  2.39 ms

*   Trying 10.45.200.15:8443...
* Connected to 10.45.200.15 port 8443 (#0)
* Trying to connect to 10.45.200.15 port 8443...

Connection to 10.45.200.15 22 [tcp/ssh] succeeded!
```

!!! warning "Common errors"
    **`ping: sendto: Operation not permitted`** — Verify ICMP is not blocked by host firewall rules (check `iptables -L` or security group rules).
    **`nc: getaddrinfo: Name or service not known`** — Confirm the hostname resolves correctly with `nslookup <host>` or use the IP address directly.
    **`curl: (7) Failed to connect to <dest> port <port>: Connection refused`** — Verify the service is running on the target host and listening on that port with `netstat -tlnp` or `ss -tlnp`.
```bash
# PAN-OS
show log traffic action=deny | last 100

# Linux iptables
iptables -L -v -n | grep DROP
journalctl | grep "DPT=<port>"
```

```text title="Expected output"
=== PAN-OS Traffic Log (Last 100 Denied) ===
2024/01/15 14:32:18 192.168.1.105 203.0.113.42 tcp/443 deny application=ssl-tls action=deny rule=BlockMalware
2024/01/15 14:31:52 10.0.2.50 198.51.100.89 tcp/22 deny application=ssh action=deny rule=DenySSH_External
2024/01/15 14:30:15 172.16.0.200 192.0.2.15 udp/53 deny application=dns action=deny rule=BlockDNS_Tunneling
2024/01/15 14:29:44 192.168.1.110 203.0.113.100 tcp/445 deny application=smb action=deny rule=BlockSMB
2024/01/15 14:28:33 10.0.3.75 198.51.100.200 tcp/3389 deny application=rdp action=deny rule=DenyRDP_Inbound
...
Total denied: 847 entries in last 24 hours

=== Linux iptables DROP Rules ===
Chain INPUT (policy ACCEPT 1250K packets, 890M bytes)
    0  0 DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:22
    0  0 DROP       tcp  --  *      *       0.0.0.0/0            0.0.0.0/0            tcp dpt:3389
    0  0 DROP       udp  --  *      *       0.0.0.0/0            0.0.0.0/0            udp dpt:53
Chain FORWARD (policy DROP 0 packets, 0 bytes)

=== Journalctl Filtered Output ===
Jan 15 14:32:18 web-server-01 kernel: [UFW BLOCK] IN=eth0 OUT= MAC=52:54:00:12:34:56:08:00:45:00 SRC=203.0.113.42 DST=192.168.1.105 PROTO=TCP SPT=54821 DPT=443 WINDOW=65535
Jan 15 14:31:52 web-server-01 kernel: [UFW BLOCK] IN=eth0 OUT= MAC=52:54:00:12:34:57:08:00:45:00 SRC=198.51.100.89 DST=10.0.2.50 PROTO=TCP SPT=49152 DPT=22 WINDOW=64240
Jan 15 14:30:15 web-server-01 kernel: [UFW BLOCK] IN=eth0 OUT= MAC=52:54:00:12:34:58:08:00:45:00 SRC=192.0.2.15 DST=172.16.0.200 PROTO=UDP SPT=53 DPT=53 WINDOW=0
```

!!! warning "Common errors"
    **`Error: command not found`** — Verify you are connected to the PAN-OS device via SSH or CLI and have proper credentials;
```bash
# Identify which policy matched a session (PAN-OS)
show session all filter destination <ip> destination-port <port>
```

```text title="Expected output"
ID    Application    Source              Destination         Sport  Dport  State      Type      Timeout
1234  ssh            192.168.1.50        203.0.113.42        54321  22     ACTIVE     FLOW      1800
5678  http           192.168.1.51        203.0.113.42        54322  80     ACTIVE     FLOW      1800
9012  https          192.168.1.52        203.0.113.42        54323  443    ACTIVE     FLOW      1800

Policy matched: "Allow-SSH-Outbound" (Policy ID: 5)
Action: allow
Log Setting: default-log-forwarding
```

!!! warning "Common errors"
    **`Unknown command: show session all filter`** — Verify you are in the correct operational mode (use `set cli operational-mode normal` if in XML mode).
    **`No matching session found`** — Confirm the destination IP and port are correct, and that an active session exists (use `show session all` to list all sessions).
```bash
show running nat-policy           # PAN-OS
show ip nat translations          # Cisco IOS
```

```text title="Expected output"
# PAN-OS output:
Total rules: 12
Rule Name                          Source Zone    Dest Zone    Action
nat-rule-01                        trust          untrust      dynamic-ip-and-port
nat-rule-02                        dmz            untrust      dynamic-ip
nat-rule-03                        guest          untrust      dynamic-ip-and-port
nat-rule-04                        trust          dmz          none
nat-rule-05                        untrust        trust        static-ip

# Cisco IOS output:
Pro Inside global      Inside local       Outside local      Outside global
tcp 203.0.113.45:8080  192.168.1.100:80   10.20.30.40:443    10.20.30.40:443
tcp 203.0.113.46:22    192.168.1.101:22   10.20.30.41:22     10.20.30.41:22
udp 203.0.113.47:53    192.168.1.50:53    0.0.0.0:0          0.0.0.0:0
tcp 203.0.113.48:443   192.168.1.102:443  10.20.30.50:443    10.20.30.50:443
```

!!! warning "Common errors"
    **`% Invalid command`** — Verify the device is in the correct mode (enable mode for Cisco, operational mode for PAN-OS) and check the exact command syntax for your OS version.
    **`% Incomplete command`** — Add required parameters or use `?` to view available options for the specific command variant.
```bash
show vpn-sessiondb                  # all active VPN sessions
show crypto ikev2 sa                # IKEv2 Phase 1 status
show crypto ipsec sa                # IPsec Phase 2 status
show crypto ikev1 sa                # IKEv1 Phase 1
show crypto isakmp sa               # IKEv1 ISAKMP
```

```text title="Expected output"
Total VPN-Sessiondb: 2

Session Type: IPsecOverTcp
Username    : vpn_user_01
Tunnel IP   : 10.8.45.12
Public IP   : 203.0.113.87
Duration    : 0h:45m:32s
Bytes Sent  : 2847392
Bytes Rcvd  : 5124768

Session Type: IPsecOverUdp
Username    : vpn_user_02
Tunnel IP   : 10.8.45.13
Public IP   : 198.51.100.42
Duration    : 2h:12m:15s
Bytes Sent  : 891245
Bytes Rcvd  : 3456789

IKEv2 Phase-1 Status:
Tunnel Name: SITE-A-TO-SITE-B
Peer IP    : 192.0.2.50
Status     : UP
Encryption : AES-GCM-256
Integrity  : SHA512
DH Group   : 20

IPsec Phase-2 Status:
Tunnel Name: SITE-A-TO-SITE-B
Peer IP    : 192.0.2.50
Status     : UP
Encryption : AES-GCM-256
Protocol   : ESP
SPI        : 0x4a2b1c3d
Bytes In   : 15728640
Bytes Out  : 8912384

IKEv1 Phase-1 Status:
(no active sessions)

IKEv1 ISAKMP Status:
(no active sessions)
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Verify the device supports these commands; older ASA/Cisco models may use different syntax like `show crypto ipsec transform-set`.
    **`% Incomplete command.`** — Add a specific tunnel name or use `all` keyword; some devices require `show crypto ipsec sa detail` for full output.
```bash
show vpn ike-sa
show vpn ipsec-sa
show vpn tunnel
```

```text title="Expected output"
Tunnel ID    State      Peer Address      Encapsulation
1            up         203.0.113.42      tunnel
2            up         198.51.100.88     tunnel
3            down       192.0.2.15        tunnel

IKE SA Information:
  Tunnel 1: IKEv2, DPD enabled, Rekey in 3421s
  Tunnel 2: IKEv2, DPD enabled, Rekey in 7834s
  Tunnel 3: IKEv2, DPD enabled, Rekey in 0s (inactive)

IPSec SA Information:
  Tunnel 1: AES-GCM-256, Replay window 64, Bytes in: 2.4GB, Bytes out: 1.8GB
  Tunnel 2: AES-GCM-256, Replay window 64, Bytes in: 856MB, Bytes out: 923MB
  Tunnel 3: (no active SAs)
```

!!! warning "Common errors"
    **`show: command not found`** — Verify you are in the correct CLI mode (use `configure` or `operational` mode as appropriate for your platform).
    **`VPN subsystem not initialized`** — Ensure VPN services are running with `systemctl status vpn` or equivalent platform command.
```bash
ping <remote_subnet_ip> source <local_subnet_ip>
traceroute <remote_ip>
```

```text title="Expected output"
PING 192.168.45.10 from 192.168.10.5: 56 data bytes
64 bytes from 192.168.45.10: icmp_seq=0 ttl=64 time=12.345 ms
64 bytes from 192.168.45.10: icmp_seq=1 ttl=64 time=11.892 ms
64 bytes from 192.168.45.10: icmp_seq=2 ttl=64 time=12.156 ms
^C
--- 192.168.45.10 statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 11.892/12.131/12.345/0.187 ms

traceroute to 203.0.113.42 (203.0.113.42), 30 hops max, 60 byte packets
 1  gateway.internal (10.0.0.1)  2.341 ms  2.156 ms  2.289 ms
 2  isp-router-01.net (198.51.100.1)  8.923 ms  9.045 ms  8.756 ms
 3  core-backbone-02.isp.net (198.51.100.65)  18.234 ms  18.567 ms  18.401 ms
 4  203.0.113.42 (203.0.113.42)  22.145 ms  21.987 ms  22.334 ms
```

!!! warning "Common errors"
    **`ping: invalid option -- 's'`** — Use `-S` (uppercase) instead of `source` for the source IP parameter: `ping -S <local_subnet_ip> <remote_subnet_ip>`.
    **`traceroute: command not found`** — Install traceroute with `apt-get install traceroute` (Debian/Ubuntu) or `yum install traceroute` (RHEL/CentOS).
```bash
# Check certificate validity
openssl x509 -in <cert_file> -noout -dates

# Check PKI enrollment status (Cisco IOS)
show crypto pki certificate
```

```text title="Expected output"
notBefore=Jan 15 10:23:45 2024 GMT
notAfter=Jan 15 10:23:45 2025 GMT

Certificate Information for router.example.com
  Status: Available
  Certificate serial number: 0x4A2B1C9E7F3D5A1B
  Certificate Usage: General Purpose
  Issuer: CN=Internal-CA, O=Example Corp, C=US
  Subject: CN=router.example.com, O=Example Corp, C=US
  Validity: Jan 15 10:23:45 2024 GMT to Jan 15 10:23:45 2025 GMT
  Public Key Size: 2048 bits
  Fingerprint (SHA1): A1:B2:C3:D4:E5:F6:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D:7E:8F:9A:0B
```

!!! warning "Common errors"
    **`unable to load certificate`** — Verify the certificate file path is correct and readable with `ls -la <cert_file>`.
    **`error in x509 certificate`** — Ensure the file is in PEM or DER format; convert with `openssl x509 -inform DER -in <cert_file> -out cert.pem` if needed.
```bash
# Cisco IOS — view VTI state
show interface tunnel <id>
show ip route | grep tunnel
```

```d2
direction: down

external: External / Untrusted {shape: rectangle}
perimeter_controls: "Perimeter Controls" {shape: rectangle}
identity_access: "Identity & Access" {shape: rectangle}
audit_logging: "Audit & Logging" {shape: rectangle}
core: "Security Core" {shape: hexagon}

external -> perimeter_controls: traffic in
perimeter_controls -> identity_access
identity_access -> audit_logging
audit_logging -> core: secured path
```

## Before you begin

- **Access:** Network admin credentials; console or SSH to devices
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

