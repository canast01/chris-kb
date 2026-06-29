---
tags:
  - networking
---
# SNMP Communities

<div class="kb-summary">
An SNMP community string is a plaintext password used in SNMPv1 and SNMPv2c to authenticate read or write access to a device's management information base (MIB).
</div>

        COMMUNITY STRING FLOW (SNMPv1/v2c)

Community strings provide no encryption.

!!! warning "SNMPv2c security"
    Community strings are transmitted in plaintext and are visible in packet captures. Treat them as secrets and use SNMPv3 for any environment with compliance requirements or sensitive data. SNMPv2c is acceptable only on isolated management VLANs with strict ACLs.

```d2
direction: down

community_types: "Community Types" {shape: rectangle}
configuring_communities_linux_snmpd: "Configuring Communities — Linux (snmpd)" {shape: rectangle}
cisco_ios: "Cisco IOS" {shape: rectangle}
arista_eos: "Arista EOS" {shape: rectangle}
brocade_fos: "Brocade FOS" {shape: rectangle}
testing_community_access: "Testing Community Access" {shape: rectangle}

community_types -> configuring_communities_linux_snmpd: uses
configuring_communities_linux_snmpd -> cisco_ios: uses
cisco_ios -> arista_eos: uses
arista_eos -> brocade_fos: uses
brocade_fos -> testing_community_access: uses
```

## Community Types

| Community | Access | Typical name | Risk |
|---|---|---|---|
| **Read-only (RO)** | GET, GETNEXT, GETBULK | `public`, `ro-community` | Data exposure |
| **Read-write (RW)** | All RO + SET | `private`, `rw-community` | Device misconfiguration |

Never use default community strings (`public` / `private`) in production.

## Configuring Communities — Linux (snmpd)

```bash
# /etc/snmp/snmpd.conf
rocommunity  monitoring-ro  10.0.0.0/8    # read-only, restricted to management network
rocommunity6 monitoring-ro  ::1/128

# Remove default "public" if present
# Comment out: rocommunity public default

systemctl restart snmpd

# Test locally
snmpwalk -v2c -c monitoring-ro localhost system
```


```text title="Expected output"
SNMP v2-MIB::sysDescr.0 = STRING: Linux snmp-host-01 5.15.0-84-generic #93-Ubuntu SMP Tue Sep 3 12:31:45 UTC 2024 x86_64
SNMP v2-MIB::sysObjectID.0 = OID: enterprises.8072.3.2.10
SNMP v2-MIB::sysUpTime.0 = Timeticks: (847392156) 98 days, 2:16:32.56
SNMP v2-MIB::sysContact.0 = STRING: admin@example.com
SNMP v2-MIB::sysName.0 = STRING: snmp-host-01
SNMP v2-MIB::sysLocation.0 = STRING: DataCenter-A
SNMP v2-MIB::sysServices.0 = INTEGER: 72
SNMP v2-MIB::sysORLastChange.0 = Timeticks: (1) 0:00:00.01
```

!!! warning "Common errors"
    **`snmpwalk: Unknown host (localhost)`** — Verify snmpd is running with `systemctl status snmpd` and listening on 127.0.0.1:161.
    **`rocommunity: line X: token parse error`** — Check for trailing whitespace or incorrect CIDR notation in /etc/snmp/snmpd.conf and validate syntax with `snmpconf -g basic_setup`.
    **`Timeout: No Response from localhost`** — Ensure the rocommunity string "monitoring-ro" matches exactly in snmpd.conf and firewall rules allow UDP 161 on localhost.
## Cisco IOS

```bash
# Read-only community with ACL restriction
ip access-list standard SNMP-MGMT
 permit 10.10.0.0 0.0.255.255

snmp-server community <community-string> RO SNMP-MGMT
snmp-server community <rw-string> RW SNMP-MGMT

# Remove defaults
no snmp-server community public
no snmp-server community private

# Verify
show snmp community
```


```text title="Expected output"
Standard IP access list SNMP-MGMT
    10 permit 10.10.0.0, wildcard bits 0.0.255.255

Community name: monitoring-ro
Community Index: monitoring-ro
Access list: SNMP-MGMT (standard)
Storage type: nonvolatile

Community name: admin-rw
Community Index: admin-rw
Access list: SNMP-MGMT (standard)
Storage type: nonvolatile
```

!!! warning "Common errors"
    **`% Invalid input detected at '^' marker.`** — Replace `<community-string>` and `<rw-string>` with actual community names (e.g., `monitoring-ro` and `admin-rw`).
    **`% Access list SNMP-MGMT not found`** — Create the ACL before referencing it in the snmp-server command; ensure the `ip access-list standard SNMP-MGMT` block is configured first.
    **`% Community string too long (max 32 characters)`** — Use community names with 32 characters or fewer.
## Arista EOS

```text
snmp-server community <community-string> ro
snmp-server community <community-string> view system-view ro
show snmp community
```

## Brocade FOS

```bash
snmpconfig --set snmpv1
# Follow prompts to set community strings and access list
snmpconfig --show snmpv1
```


```text title="Expected output"
Setting SNMP v1 configuration...
Enter read-only community string: public
Enter read-write community string: private
Enter access list (comma-separated IPs, or 'any'): 192.168.1.0/24,10.0.0.5
Configuration saved successfully.

SNMP v1 Configuration:
  Read-only community: public
  Read-write community: private
  Access list: 192.168.1.0/24,10.0.0.5
  Status: enabled
  Trap destination: 192.168.1.100:162
```

!!! warning "Common errors"
    **`snmpconfig: command not found`** — Install the SNMP tools package with `apt-get install snmp snmp-mibs-downloader` or equivalent for your distribution.
    **`Error: Invalid CIDR notation in access list`** — Use valid CIDR notation (e.g., `192.168.1.0/24`) or single IPs separated by commas without spaces.
    **`Permission denied: cannot write to /etc/snmp/snmpd.conf`** — Run the command with `sudo` or as root to modify SNMP configuration files.
## Testing Community Access

```bash
# Test from NMS / monitoring server
snmpget  -v2c -c <community> <device-ip> sysDescr.0
snmpwalk -v2c -c <community> <device-ip> system

# If no response — check:
# 1. Community string correct
# 2. NMS IP in ACL on device
# 3. UDP 161 not blocked by firewall
```


```text title="Expected output"
SNMPv2-MIB::sysDescr.0 = STRING: Cisco IOS Software, C2960X Software, Version 15.2(4)E10, RELEASE SOFTWARE (fc1)
SNMPv2-MIB::sysObjectID.0 = OID: SNMPv2-SMI::enterprises.9.9.46.1
SNMPv2-MIB::sysUpTime.0 = Timeticks: (487652100) 56 days, 10:08:41.00
SNMPv2-MIB::sysContact.0 = STRING: netops@company.com
SNMPv2-MIB::sysName.0 = STRING: switch-core-01.dc1.internal
SNMPv2-MIB::sysLocation.0 = STRING: DataCenter 1, Rack 42
SNMPv2-MIB::sysServices.0 = INTEGER: 72
SNMPv2-MIB::sysORLastChange.0 = Timeticks: (0) 0:00:00.00
...
```

!!! warning "Common errors"
    **`Timeout: No Response from <device-ip>`** — Verify the community string matches the device configuration and confirm UDP port 161 is not blocked by firewall rules between NMS and target device.
    **`snmpget: Unknown host name`** — Ensure the device IP address is correct and reachable by pinging the target before attempting SNMP queries.
    **`Error in packet: Reason: (noSuchName)`** — Confirm the device supports SNMPv2c (not SNMPv3-only) and that the community string has read permissions for the requested OID.
## Community String Standards

- Minimum 16 characters, mixed alphanumeric
- Different strings for RO and RW
- Store in CyberArk or secrets manager — never in plaintext config files
- Rotate annually or when staff leave
- Scope with ACLs to management network ONLY

## Common Issues

| Symptom | Cause | Check |
|---|---|---|
| `Timeout: No Response` | Wrong community or UDP 161 blocked | Test with `snmpget`; check firewall |
| No response from new device | Community not configured | Verify `show snmp community` on device |
| NMS sees wrong data | RW community accidentally used for RO polling | Use separate strings for read and write |
| Community string visible in Wireshark | SNMPv2c by design | Migrate to SNMPv3 for sensitive environments |
