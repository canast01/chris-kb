# Network Security

<div class="kb-summary">
Network security knowledge base covering firewalls, VPN, rule validation, and network access control.
</div>

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Network Security Zones                          │
│                                                                      │
│  ┌────────────┐                                                      │
│  │  Internet  │  (untrusted)                                         │
│  └─────┬──────┘                                                      │
│        │  Allow: HTTPS/443, SMTP/25 inbound only                    │
│  ┌─────▼──────────────────────────────────────┐                     │
│  │  DMZ Zone (VLAN 10-99)                     │  ◄── WAF / IDS     │
│  │  Reverse proxies · Public APIs · Bastion   │                     │
│  └─────┬──────────────────────────────────────┘                     │
│        │  Allow: specific app ports only                            │
│  ┌─────▼──────────────────────────────────────┐                     │
│  │  Production Zone (VLAN 100-199)            │  ◄── ACLs          │
│  │  App servers · Databases · Services        │                     │
│  └─────┬──────────────────────┬───────────────┘                     │
│        │ iSCSI/NFS            │ Veeam agent                        │
│  ┌─────▼──────────┐   ┌───────▼──────────┐                          │
│  │ Storage Zone   │   │  Backup Zone     │                          │
│  │ (VLAN 300-310) │   │  (VLAN 500-510)  │                          │
│  └────────────────┘   └──────────────────┘                          │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  NSX-T DFW: micro-segmentation within each zone             │    │
│  └─────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
```

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

### Validation

1. Confirm connection allowed
2. Confirm application connectivity restored
3. Document firewall change if required

## Firewalls

### Overview

Firewalls control traffic between zones using rules, policies, NAT, and inspection profiles. In enterprise infrastructure, firewalls govern traffic between:
- Production and management networks
- On-premises and cloud
- Internet egress
- Storage replication paths across sites

### Check Traffic Sessions

```bash
# Active sessions (Palo Alto / PAN-OS)
show session all
show session id <id>

# Traffic logs
show log traffic
```

### View Security Policy

```bash
show running security-policy    # PAN-OS
show security policies          # Juniper SRX
show access-list                # Cisco ASA
```

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
