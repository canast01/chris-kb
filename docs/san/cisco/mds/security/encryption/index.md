# MDS — Encryption

> Part of the [Cisco MDS](../../) reference.

---

## SNMP Hardening

```
# Disable default SNMPv1/v2c community strings
no snmp-server community public
no snmp-server community private

# Configure SNMPv3 with auth + priv
snmp-server user nms_user network-operator auth sha <auth-password> priv aes-128 <priv-password>
snmp-server host <nms-ip> traps version 3 priv nms_user

# Restrict SNMP to monitoring subnet
ip access-list SNMP-RESTRICT
  permit udp <nms-subnet>/<prefix> any eq 162
  deny udp any any eq 162 log
```

---

## SSH Key Management

```
# Generate RSA keys for SSH
crypto key generate rsa

# Verify public key
show crypto key mypubkey rsa

# Restrict SSH access by source IP
ip access-list <acl_name>
  permit ip <mgmt_subnet> any
line vty 0 4
  access-class <acl_name> in
```

---

## Standards

- SNMPv3 only; SNMPv1/v2 disabled
- Auth protocol: SHA; Privacy protocol: AES-128 minimum
- Community strings (if SNMPv2 legacy required): in vault, quarterly rotation
- SSH only for management access; Telnet disabled
