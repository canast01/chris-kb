# Network Security

<div class="kb-summary">
Network security knowledge base covering firewalls, VPN, rule validation, and network access control.
</div>

## Firewall Rule Validation

### Overview

This runbook verifies firewall rules allow required traffic.

### Pre-Checks

- Confirm source and destination
- Confirm port and protocol
- Identify firewall device

### Commands

```bash
nc -zv destination-host port
telnet destination-host port
ss -tulnp
```
```
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
```sql

### Test Connectivity Through a Firewall

```bash
# From a host behind the firewall
ping <destination>
traceroute <destination>
curl -v telnet://<dest>:<port>    # test specific TCP port

# From Linux — test TCP port
nc -zv <host> <port>
```

### Review Deny Logs

```bash
# PAN-OS
show log traffic action=deny | last 100

# Linux iptables
iptables -L -v -n | grep DROP
journalctl | grep "DPT=<port>"
```

### Common Rule Troubleshooting

```bash
# Identify which policy matched a session (PAN-OS)
show session all filter destination <ip> destination-port <port>
```

### NAT Verification

```bash
show running nat-policy           # PAN-OS
show ip nat translations          # Cisco IOS
```

### Pre-Change Checklist

- [ ] Confirm source, destination, port, and protocol needed
- [ ] Identify which policy/zone applies
- [ ] Capture current rule hit counts
- [ ] Test connectivity before change (baseline)
- [ ] Test connectivity after change

### Common Issues

| Issue | Check | Action |
|---|---|---|
| Traffic blocked | Deny logs | Identify rule; add permit if authorized |
| Rule exists but traffic still blocked | Rule order | Check rule priority — most specific first |
| NAT failing | NAT policy | Verify NAT translation and route |
| VPN tunnel down | IKE/IPSEC logs | Check PSK, crypto policy, peer IP |

## VPN

VPNs provide encrypted connectivity between sites, cloud environments, remote users, and partner networks.

### Tunnel Status

**Cisco ASA / IOS:**
```bash
show vpn-sessiondb                  # all active VPN sessions
show crypto ikev2 sa                # IKEv2 Phase 1 status
show crypto ipsec sa                # IPsec Phase 2 status
show crypto ikev1 sa                # IKEv1 Phase 1
show crypto isakmp sa               # IKEv1 ISAKMP
```

**Palo Alto:**
```bash
show vpn ike-sa
show vpn ipsec-sa
show vpn tunnel
```

### IKE / IPsec Phases

| Phase | Protocol | Purpose |
|---|---|---|
| Phase 1 (IKE) | ISAKMP/IKEv2 | Establish authenticated, encrypted channel |
| Phase 2 | IPsec | Negotiate encryption for data tunnels |

Both phases must complete for a functional tunnel.

### Test Connectivity Through Tunnel

```bash
ping <remote_subnet_ip> source <local_subnet_ip>
traceroute <remote_ip>
```

### Common Phase 1 Issues

| Issue | Cause | Fix |
|---|---|---|
| No response from peer | Firewall blocking UDP 500/4500 | Open UDP 500 and 4500 |
| Authentication failed | Mismatched PSK or certificate | Verify PSK or certificate chain |
| Proposal mismatch | Different encryption/hash settings | Match DH group, encryption, hash on both ends |

### Common Phase 2 Issues

| Issue | Cause | Fix |
|---|---|---|
| Tunnel up, no traffic | Proxy IDs / ACL mismatch | Match encryption domain (interesting traffic) on both ends |
| Traffic one-directional | Asymmetric routing | Check routing on remote peer |
| Tunnel drops intermittently | SA lifetime mismatch | Match Phase 2 lifetime on both peers |

### Certificate-Based VPN

```bash
# Check certificate validity
openssl x509 -in <cert_file> -noout -dates

# Check PKI enrollment status (Cisco IOS)
show crypto pki certificate
```

### Route-Based VPN

Route-based VPNs use virtual tunnel interfaces (VTI) — routing directs traffic into the tunnel rather than ACLs:

```bash
# Cisco IOS — view VTI state
show interface tunnel <id>
show ip route | grep tunnel
```
