# MDS — Encryption

> Part of the [Cisco MDS](../../index.md) reference.

---

## Overview

Encryption on the MDS platform operates at multiple layers:

- **Management plane**: SSH and HTTPS for all CLI and API access; SNMP traffic encrypted via SNMPv3 authPriv
- **Control plane**: TACACS+ key encryption; FC-SP DHCHAP for fabric authentication
- **Data plane**: MACsec or FC-SP for in-flight FC frame encryption (MDS 9700 series hardware required for FC encryption)
- **Long-distance FC**: FCIP with IPSec for encrypted Fibre Channel over IP tunnels

---

## SSH (Management Access Encryption)

SSH is the only permitted remote management protocol. Telnet transmits credentials in cleartext and must be disabled.

```bash
# Verify SSH is enabled
show feature | include ssh
# Expected: ssh   enabled

# Disable Telnet explicitly
no feature telnet

# Verify Telnet is disabled
show feature | include telnet
# Expected: telnet   disabled

# Generate or verify RSA key pair (required for SSH server)
crypto key generate rsa
show crypto key mypubkey rsa

# Set minimum SSH version to 2 (v1 is insecure)
ssh version 2

# View active SSH sessions
show ssh server
show users
```
┌─────────────────────────────────── Cisco MDS — Security Encryption ───────────────────────────────────┐
│                                                                                                       │
│  Management-plane TLS and FC-SP fabric encryption protecting MDS switch communications.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Management Encryption             │  │         Fabric Encryption (FC-SP-2)         │   │
│   │         SSH: AES-128/256-CTR ciphers         │  │         FC-SP-2: AES-256-GCM frames         │   │
│   │            HTTPS: TLS 1.2 minimum            │  │        IKE: key exchange between ISLs       │   │
│   │         SNMP: v3 authPriv (AES-128)          │  │          Per-ISL encryption enable          │   │
│   │         Syslog: TLS transport option         │  │         Rekey interval configurable         │   │
│   │        Disable weak ciphers: RC4/DES         │  │         GCM: integrity + encryption         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Management TLS protects CLI/API; FC-SP-2 protects ISL data in transit                                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Management                │  │              Compliance Posture             │   │
│   │        Local key store on supervisor         │  │          FIPS 140-2 mode available          │   │
│   │       KMS: external key server option        │  │          Common Criteria validation         │   │
│   │        Key rotation: scheduled rekey         │  │        Audit: cipher negotiation log        │   │
│   │       PKI trustpoint for cert storage        │  │         No plaintext mgmt protocols         │   │
│   │        Entropy: hardware RNG on ASIC         │  │         Annual cipher review policy         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  MDS supervisor ASIC (hardware RNG) · ISL fiber links · management Ethernet · KMS server              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FC-SP-2        = Fibre Channel Security Protocol v2; adds ISL frame encryption                       │
│  GCM            = Galois/Counter Mode; AES cipher mode providing auth + encryption                    │
│  IKE            = Internet Key Exchange; negotiates session keys for FC-SP-2                          │
│  ISL            = Inter-Switch Link; E_Port connection between two MDS switches                       │
│  FIPS 140-2     = US federal standard for cryptographic module security                               │
│  KMS            = Key Management Server; centralizes key lifecycle for encryption                     │
│  authPriv       = SNMPv3 security level: authentication + privacy (encryption)                        │
│  Trustpoint     = Named PKI anchor; stores CA cert and associated key material                        │
│  Rekey interval = How often session encryption keys are rotated to limit exposure                     │
│  Hardware RNG   = Crypto-grade random number generator built into ASIC                                │
│  Common Criteria= International security evaluation standard (ISO/IEC 15408)                          │
│  TLS            = Transport Layer Security; encrypts management-plane sessions                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## HTTPS (Web and API Access)

NX-OS supports HTTPS for the web GUI and NDFC REST API. HTTP (cleartext) must be disabled.

```bash
# Disable HTTP server
no feature http-server

# Enable HTTPS server
feature https-server

# Verify
show feature | include http
# http-server    disabled
# https-server   enabled
```

### HTTPS Certificate Management

NX-OS uses a self-signed certificate by default. For enterprise environments, replace with a CA-signed certificate.

```bash
# Generate a new self-signed certificate
crypto ca trustpoint LOCAL-CA
  enrollment self-signed
  subject-name CN=mds-sw01.corp.example.com

# Generate the keypair and certificate
crypto key generate rsa label mds-ssl-key modulus 2048
crypto ca enroll LOCAL-CA

# Display the current certificate
show crypto ca certificates

# Import a CA-signed certificate (PEM format via TFTP/SCP)
copy tftp://<server>/mds-sw01.pem bootflash:mds-sw01.pem
crypto ca import LOCAL-CA certificate
```

---

## SNMPv3 (Encrypted SNMP)

SNMPv1 and v2c transmit community strings and OID data in cleartext. SNMPv3 with `authPriv` security level provides both authentication (SHA) and privacy encryption (AES).

### Disable SNMPv1/v2c

```bash
# Remove default community strings
no snmp-server community public
no snmp-server community private

# If v2c is required for a legacy NMS: restrict to a named ACL
# ip access-list SNMP-LEGACY-NMS
#   permit udp 10.10.2.5/32 any eq 161
# snmp-server community <string> group network-operator use-acl SNMP-LEGACY-NMS
```

### Configure SNMPv3 Users

```bash
# Create an SNMPv3 user with authPriv (SHA auth, AES-128 privacy)
snmp-server user nms_monitor network-operator v3 auth sha <auth-password> priv aes-128 <priv-password>

# Create a trap receiver using SNMPv3
snmp-server host 10.10.2.50 traps version 3 priv nms_monitor

# Verify SNMPv3 user configuration
show snmp user

# Verify trap host configuration
show snmp host

# Test SNMP from the monitoring server (Linux)
# snmpwalk -v3 -u nms_monitor -l authPriv -a SHA -A <auth-pass> -x AES -X <priv-pass> <switch-ip> sysDescr
```

### SNMP Trap Configuration

```bash
# Enable specific trap categories
snmp-server enable traps link
snmp-server enable traps entity
snmp-server enable traps vsan
snmp-server enable traps zone

# Verify trap configuration
show snmp trap

# Check that traps are being sent (look for SNMP events in log)
show logging | grep -i snmp
```

---

## TACACS+ Key Encryption

TACACS+ shared keys must be stored encrypted in the NX-OS configuration. NX-OS uses type-7 (Vigenere-based) obfuscation for `key 7` stored values.

```bash
# Enter key as plaintext (NX-OS encrypts automatically in running-config)
tacacs-server host 10.10.1.10 key 0 <plaintext-key>

# The stored config shows an encrypted form
show running-config | grep tacacs
# tacacs-server host 10.10.1.10 key 7 <encrypted-string>

# Rotating TACACS+ key
no tacacs-server host 10.10.1.10 key
tacacs-server host 10.10.1.10 key 0 <new-plaintext-key>
copy running-config startup-config
```

Note: NX-OS type-7 keys are obfuscated, not cryptographically secure. The security relies on the confidentiality of the configuration file itself. Store configuration backups in an access-controlled, encrypted repository.

---

## FC-SP / DHCHAP (Fabric Authentication Encryption)

FC-SP uses DHCHAP (Diffie-Hellman Challenge Handshake Authentication Protocol) to authenticate FC devices before permitting fabric login. The DHCHAP exchange is cryptographically signed — it does not encrypt FC frames but prevents unauthenticated devices from logging in.

```bash
# Enable FC-SP
feature fcsp

# Configure per-interface (F_Port connections to hosts/storage)
interface fc1/1
  fcsp dhchap mode on      # Require authentication — reject unauthenticated devices
  # or
  fcsp dhchap mode auto    # Negotiate — accept unauthenticated if peer doesn't support

# Set a DHCHAP password for a specific device (by PWWN)
fcsp dhchap devicename-password pwwn 21:00:00:24:ff:a1:b2:c3 password 0 <secret>

# Verify
show fcsp interface fc1/1
show fcsp dhchap vsan 10
```

---

## FCIP with IPSec (FC over IP Encryption)

FCIP (Fibre Channel over IP) tunnels FC frames over IP networks for long-distance replication and campus extension. Without IPSec, FCIP traffic is transmitted in cleartext. Add IPSec to encrypt the IP tunnel.

### FCIP with IPSec — Overview

FCIP is typically deployed on MDS 9700-series switches with the Storage Services Module (SSM) or IPS modules. The configuration defines a tunnel interface that maps an FC VSAN to an IP tunnel endpoint.

```bash
# Enable FCIP feature
feature fcip

# Create FCIP interface
interface fcip 1
  peer-info ipaddr 10.20.0.2    # remote MDS management IP for FCIP
  use-profile 1
  vsan 20                        # associate with replication VSAN

# Define FCIP profile (TCP parameters)
fcip profile 1
  ip address 10.20.0.1

# Enable IPSec on the FCIP interface
# (Requires IKE and IPSec policy configuration — see below)
```

### IPSec Policy for FCIP

```bash
# Define IKE proposal
crypto ike proposal FCIP-IKE-PROP
  encryption aes-256-cbc
  hash sha256
  lifetime 86400

# Define IKE policy
crypto ike policy 10
  proposal FCIP-IKE-PROP
  peer 10.20.0.2
  pre-shared-key 0 <pre-shared-key>

# Define IPSec transform set
crypto ipsec transform-set FCIP-XFORM esp-aes-256 esp-sha256-hmac

# Define IPSec profile
crypto ipsec profile FCIP-PROFILE
  set transform-set FCIP-XFORM

# Apply to FCIP interface
interface fcip 1
  ipsec crypto-map FCIP-PROFILE

# Verify IPSec SA establishment
show crypto ike sa
show crypto ipsec sa
show interface fcip 1
```

---

## Encryption Standards Summary

| Layer | Protocol | Standard |
|---|---|---|
| Management CLI | SSH v2 | RSA 2048-bit; SSH v1 disabled |
| Management Web/API | HTTPS TLS 1.2+ | CA-signed certificate preferred |
| SNMP | SNMPv3 authPriv | SHA auth; AES-128 minimum |
| TACACS+ key | Type-7 stored | Config backup stored encrypted |
| Fabric device auth | FC-SP DHCHAP | Enabled on F_Ports in high-security VSANs |
| FCIP tunnel | IPSec | AES-256; SHA-256; IKEv2 |
| FC frame encryption | MACsec / FC-SP | MDS 9700 with hardware encryption module |

---

## Encryption Checklist

- [ ] Telnet disabled: `show feature | include telnet` returns `disabled`
- [ ] SSH enabled; RSA key generated: `show crypto key mypubkey rsa`
- [ ] SSH version 2 enforced: `show ssh server | include version`
- [ ] HTTP disabled; HTTPS enabled: `show feature | include http`
- [ ] HTTPS certificate current and from a trusted CA (or self-signed documented in CMDB)
- [ ] SNMPv1/v2c community strings removed: `show snmp community` returns none
- [ ] SNMPv3 authPriv configured with SHA + AES-128: `show snmp user`
- [ ] TACACS+ keys stored encrypted in config; config backup stored in encrypted, access-controlled repository
- [ ] FC-SP DHCHAP enabled on F_Ports in high-security VSANs: `show fcsp interface`
- [ ] FCIP tunnels using IPSec if traversing untrusted networks: `show crypto ipsec sa`
