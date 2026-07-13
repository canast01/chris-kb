---
tags:
  - san
  - security
---
# Cisco MDS — Security Encryption

*Applies to: Cisco MDS / NX-OS*
![Cisco MDS — Security Encryption](../../../../assets/san-cisco-mds-security-encryption.svg)

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


```text title="Expected output"
ssh   enabled
(no output — command completes silently)
telnet   disabled
Generating RSA key pair... (this may take a minute)
% RSA key pair generation completed successfully
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC7vK9mN2pQrxT8jK4hL9mN3oP5qR2sT4uV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oP5qR6sT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3aB4cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN3oP4qR5sT6uV7wX8yZ9aB0cD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ5aB6cD7eF8gH9iJ0kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5oP6qR7sT8uV9wX0yZ1aB2cD3eF4gH5iJ6kL7mN8oP9qR0sT1uV2wX3yZ4aB5cD6eF7gH8iJ9kL0mN1oP2qR3sT4uV5wX6yZ7aB8cD9eF0gH1iJ2kL3mN4oP5qR6sT7uV8wX9yZ0aB1cD2eF3gH4iJ5kL6mN7oP8qR9sT0uV1wX2yZ3aB4cD5eF6gH7iJ8kL9mN0oP1qR2sT3uV4wX5yZ6aB7cD8eF9gH0iJ1kL2mN3oP4qR5sT6uV7wX8yZ9aB0cD1eF2gH3iJ4kL5mN6oP7qR8sT9uV0wX1yZ2aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ5aB6cD7eF8gH9iJ0kL1mN2oP3qR4sT5uV6wX7yZ8aB9cD0eF1gH2iJ3kL4mN5
```
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

```text title="Expected output"
Generating RSA key pair...
Key pair generation completed successfully.
% Generating Self-signed certificate...
% Certificate request sent to your Certificate Authority
% The certificate has been installed.

Certificate Information:
  Issuer:   CN=mds-sw01.corp.example.com
  Subject:  CN=mds-sw01.corp.example.com
  Validity: Not Before: Jan 15 09:42:33 2025 GMT
            Not After:  Jan 15 09:42:33 2026 GMT
  Serial Number: 0x6A7F8C2D
  Fingerprint: A4:2B:9E:F1:7C:D3:5A:88:92:E6:4F:1B:C9:D7:3A:5E

Copying tftp://192.168.100.50/mds-sw01.pem to bootflash:mds-sw01.pem
[####################] 100% 2847 bytes copied in 1.23 seconds

% Certificate imported successfully
% You must restart the switch for the new certificate to take effect.
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Error: Trustpoint LOCAL-CA does not exist` | Create the trustpoint with `crypto ca trustpoint LOCAL-CA` before attempting enrollment. |
    | `% Error: Certificate file not found: bootflash:mds-sw01.pem` | Verify the file was copied successfully with `dir bootflash:` and check TFTP server connectivity. |
    | `% Error: Invalid certificate format - PEM header not found` | Ensure the certificate file is in valid PEM format (begins with `-----BEGIN CERTIFICATE-----`) and was not corrupted during transfer. |
```bash
# Remove default community strings
no snmp-server community public
no snmp-server community private

# If v2c is required for a legacy NMS: restrict to a named ACL
# ip access-list SNMP-LEGACY-NMS
#   permit udp 10.10.2.5/32 any eq 161
# snmp-server community <string> group network-operator use-acl SNMP-LEGACY-NMS
```

```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify you are in the correct configuration mode (config-if or config) and that SNMP is licensed on your MDS switch. |
    | `% Community string already removed` | If the command fails on the second run, the community strings were already deleted; this is expected and not an error. |
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

```text title="Expected output"
mds9148-switch# snmp-server user nms_monitor network-operator v3 auth sha <auth-password> priv aes-128 <priv-password>
(no output — command completes silently)
mds9148-switch# snmp-server host 10.10.2.50 traps version 3 priv nms_monitor
(no output — command completes silently)
mds9148-switch# show snmp user
User name: nms_monitor
Engine ID: 800007E5-7B2A-4A8C-9F1C-2D3E4F5A6B7C
storage-type: nonVolatile
status: active
authentication protocol: sha
privacy protocol: aes-128

mds9148-switch# show snmp host
10.10.2.50 traps version 3 priv nms_monitor udp-port 162
mds9148-switch# snmpwalk -v3 -u nms_monitor -l authPriv -a SHA -A <auth-pass> -x AES -X <priv-pass> 10.10.2.48 sysDescr
SNMPv3 User-based Security Model (USM) User Table
sysDescr.0 = STRING: Cisco MDS 9148 Multilayer Fabric Switch
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid password length for SHA authentication` | Ensure the auth password is at least 8 characters long. |
    | `Error: SNMP trap delivery failed to 10.10.2.50` | Verify network connectivity to the trap receiver and confirm the SNMP community/user credentials match on both devices. |
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

```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)

Trap Information:
  link traps enabled
  entity traps enabled
  vsan traps enabled
  zone traps enabled

2024 Jan 15 10:23:45 +00:00 mds9710-1 %SNMP-5-TRAP_SENT: SNMP trap sent to 192.168.1.50:162 (linkDown)
2024 Jan 15 10:24:12 +00:00 mds9710-1 %SNMP-5-TRAP_SENT: SNMP trap sent to 192.168.1.50:162 (entityMIB)
2024 Jan 15 10:25:03 +00:00 mds9710-1 %SNMP-5-TRAP_SENT: SNMP trap sent to 192.168.1.50:162 (vsanMembershipChange)
2024 Jan 15 10:26:41 +00:00 mds9710-1 %SNMP-5-TRAP_SENT: SNMP trap sent to 192.168.1.50:162 (zoneActivate)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify you are in the correct configuration mode (use `configure terminal` first if running from user EXEC mode). |
    | `% SNMP is not configured` | Configure SNMP community strings and trap destinations with `snmp-server community` and `snmp-server host` before enabling trap categories. |
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

```text title="Expected output"
tacacs-server host 10.10.1.10 key 7 $1$abcd1234efgh5678ijkl90mn$pqrstuvwxyz123456789012
[OK]
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify you are in global configuration mode with `configure terminal` before entering tacacs-server commands. |
    | `% Incomplete command` | Ensure the plaintext key is provided after `key 0`; the syntax requires both the encryption type (0 for plaintext) and the actual key string. |
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

```text title="Expected output"
mds9710(config)# feature fcsp
(no output — command completes silently)
mds9710(config)# interface fc1/1
mds9710(config-if)# fcsp dhchap mode on
(no output — command completes silently)
mds9710(config-if)# fcsp dhchap devicename-password pwwn 21:00:00:24:ff:a1:b2:c3 password 0 MySecureP@ss123
(no output — command completes silently)
mds9710(config-if)# exit
mds9710(config)# show fcsp interface fc1/1
VSAN 1:
  Interface fc1/1
    FCSP Status: enabled
    DHCHAP Mode: on
    Authentication Protocol: DHCHAP
    Peer Authentication: required
mds9710(config)# show fcsp dhchap vsan 10
VSAN 10:
  Device PWWN                    Auth Status    Last Auth Time
  21:00:00:24:ff:a1:b2:c3       authenticated  2024-01-15 14:32:18
  50:00:09:73:00:1a:2b:3c       unauthenticated 2024-01-15 14:28:05
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify the switch supports FC-SP (MDS 9000 series required); check NX-OS version with `show version`. |
    | `% DHCHAP password must be at least 16 characters` | Use a password with minimum 16 characters; special characters and mixed case are recommended. |
    | `% Device PWWN not found in database` | Ensure the PWWN is correctly formatted (48 hex digits with colons) and the device has logged into the fabric at least once. |
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

```text title="Expected output"
mds-switch# feature fcip
(no output — command completes silently)
mds-switch# interface fcip 1
mds-switch(config-if)# peer-info ipaddr 10.20.0.2
(no output — command completes silently)
mds-switch(config-if)# use-profile 1
(no output — command completes silently)
mds-switch(config-if)# vsan 20
(no output — command completes silently)
mds-switch(config-if)# exit
mds-switch(config)# fcip profile 1
mds-switch(config-fcip-profile)# ip address 10.20.0.1
(no output — command completes silently)
mds-switch(config-fcip-profile)# exit
mds-switch(config)#
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify the switch supports FCIP licensing and run `show feature | grep fcip` to confirm the feature is available. |
    | `% VSAN 20 does not exist` | Create the VSAN first with `vsan 20` in config mode before associating it to the FCIP interface. |
    | `% Profile 1 is already in use` | Check existing profiles with `show fcip profile` and use an unused profile number. |
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


```text title="Expected output"
IKE Exchanges:
 peer 10.20.0.2
  ESTABLISHED 0 minutes 23 seconds ago
  Encryption: aes-256-cbc  Hash: sha256  Auth: pre-shared-key
  Lifetime: 86400 seconds

IPSec SAs:
 Crypto map tag: FCIP-PROFILE, 1 sa, 1 active transform
  peer 10.20.0.2 local 10.20.0.1
   INBOUND:  SPI 0x4a2c1f89(1244053385)
    transform: esp-aes-256 esp-sha256-hmac
    in use settings ={Tunnel, }
    conn id: 1, flow_id: 1, crypto map: FCIP-PROFILE
   OUTBOUND: SPI 0x7f3e5d12(2139029778)
    transform: esp-aes-256 esp-sha256-hmac
    in use settings ={Tunnel, }
    conn id: 1, flow_id: 1, crypto map: FCIP-PROFILE

fcip1 is up, line protocol is up
  Hardware is Fibre Channel over IP
  MTU 2500 bytes, BW 1000000 Kbit/sec
  Encapsulation FCIP, loopback not set
  IPSec crypto-map FCIP-PROFILE attached
  Input packets 4521, bytes 2847392
  Output packets 4389, bytes 2756104
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `% Invalid command` | Verify the MDS switch supports FCIP licensing and that crypto commands are available in your software version. |
    | `% Incomplete command` | Replace `<pre-shared-key>` with an actual pre-shared key string (e.g., `pre-shared-key 0 MySecureKey123`). |
    | `IKE SA not established` | Confirm peer IP 10.20.0.2 is reachable, firewall allows UDP 500/4500, and both sides use identical IKE proposals and pre-shared keys. |
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

---

## See also

- [Mds — Hardening](../hardening/)
- [Mds — Authentication](../authentication/)
- [Mds — Access Control](../access-control/)
