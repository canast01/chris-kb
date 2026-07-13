---
tags:
  - architecture
  - san
---
# Brocade SANnav — Design Standards

*Applies to: Brocade FOS 9.x*
![Brocade SANnav — Design Standards](../../../../assets/san-brocade-sannav-architecture-design-standards.svg)

```bash
# Add SNMPv3 user matching SANnav credentials
snmpconfig --set snmpv3 -index 1 -username sannav_mgmt \
  -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> \
  -rwcommunity sannav_rw

# Add SANnav as trap recipient
snmpconfig --set trapdest -index 1 \
  -trapdest <sannav-ip> -severity 4 \
  -username sannav_mgmt -authtype MD5 -authpasswd <auth-pass> \
  -privtype AES128 -privpasswd <priv-pass> -trapport 162

# Verify
snmpconfig --show snmpv3
snmpconfig --show trapdest
```


```text title="Expected output"
SNMPv3 user configuration applied successfully.
Index: 1
Username: sannav_mgmt
Auth Type: MD5
Auth Password: ********
Priv Type: AES128
Priv Password: ********
RW Community: sannav_rw

Trap destination configuration applied successfully.
Index: 1
Trap Destination: 192.168.100.45
Severity Level: 4
Username: sannav_mgmt
Auth Type: MD5
Auth Password: ********
Priv Type: AES128
Priv Password: ********
Trap Port: 162

SNMPv3 Configuration:
Index 1: sannav_mgmt (MD5/AES128)

Trap Destinations:
Index 1: 192.168.100.45:162 (sannav_mgmt)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid password length for MD5 authentication` | Ensure auth-pass is at least 8 characters and priv-pass is at least 8 characters for AES128. |
    | `Error: Trap destination already exists at index 1` | Use a different index value or remove the existing entry with `snmpconfig --delete trapdest -index 1` first. |
    | `Error: SNMPv3 user sannav_mgmt does not exist` | Create the SNMPv3 user before configuring it as a trap recipient, or verify the username spelling matches exactly. |
---

## See also

- [Sannav — How It Works](../how-it-works/)
- [Sannav — Integrations](../integrations/)
- [Sannav — Deploy](../../deploy/)
