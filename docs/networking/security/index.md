# Networking — Network Security

```bash
nc -zv destination-host port
telnet destination-host port
ss -tulnp
```
```text
┌──────────────────────────────────── Networking — Network Security ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Network security: validate FW rules, confirm VPN tunnels, audit ACLs, review NAT       │   │
│   │       FW validation: test required traffic with packet tracer; review deny logs for gaps      │   │
│   │     VPN: check tunnel state, phase 1/2, SA lifetime, interesting traffic; test end-to-end     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Firewall Checks                │  │                  VPN & ACL                  │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │              Packet tracer test              │  │            show crypto isakmp sa            │   │
│   │             Review deny log hits             │  │             show crypto ipsec sa            │   │
│   │              Rule order matters              │  │            ACL: show access-list            │   │
│   │            Check NAT translation             │  │            NAT: show ip nat trans           │   │
│   │         Unused rules: review/remove          │  │             Test from both sides            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Packet tracer  = Cisco tool; simulates traffic through FW to determine permit/deny outcome         │
│    IKE phase 1    = VPN control plane; authenticates peers; establishes management SA                 │
│    IKE phase 2    = VPN data plane; negotiates IPsec SA for encrypting user traffic                   │
│    Interesting traffic= VPN traffic selector; defines what source/dest pairs trigger the tunnel       │
│    ACL            = Access Control List; permits or denies traffic by src/dst/port/protocol           │
│    PAT            = Port Address Translation; maps multiple private IPs to one public IP+port         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# From a host behind the firewall
ping <destination>
traceroute <destination>
curl -v telnet://<dest>:<port>    # test specific TCP port

# From Linux — test TCP port
nc -zv <host> <port>
```
```bash
# PAN-OS
show log traffic action=deny | last 100

# Linux iptables
iptables -L -v -n | grep DROP
journalctl | grep "DPT=<port>"
```
```bash
# Identify which policy matched a session (PAN-OS)
show session all filter destination <ip> destination-port <port>
```
```bash
show running nat-policy           # PAN-OS
show ip nat translations          # Cisco IOS
```
```bash
show vpn-sessiondb                  # all active VPN sessions
show crypto ikev2 sa                # IKEv2 Phase 1 status
show crypto ipsec sa                # IPsec Phase 2 status
show crypto ikev1 sa                # IKEv1 Phase 1
show crypto isakmp sa               # IKEv1 ISAKMP
```
```bash
show vpn ike-sa
show vpn ipsec-sa
show vpn tunnel
```
```bash
ping <remote_subnet_ip> source <local_subnet_ip>
traceroute <remote_ip>
```
```bash
# Check certificate validity
openssl x509 -in <cert_file> -noout -dates

# Check PKI enrollment status (Cisco IOS)
show crypto pki certificate
```
```bash
# Cisco IOS — view VTI state
show interface tunnel <id>
show ip route | grep tunnel
```
